


"""
process.py — Read a text file, send it to the Groq API, save the response.

Usage:
    python process.py input.txt
    python process.py input.txt --output response.txt
    python process.py input.txt --prompt "Summarize this" --model gemma2-9b-it
    python process.py input.txt --dry-run
    python process.py --list-models
"""

from __future__ import annotations

import argparse
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path

import groq
from groq import Groq

from dotenv import load_dotenv
load_dotenv()


# ── Configuration ─────────────────────────────────────────────────────────────

DEFAULT_MODEL  = "llama-3.3-70b-versatile"
DEFAULT_TOKENS = 1024
DEFAULT_PROMPT = "Please read the following text and provide a thoughtful response:"

# Free-tier models available on Groq (as of mid-2026)
AVAILABLE_MODELS = {
    "llama-3.3-70b-versatile": "Llama 3.3 70B — best overall quality (recommended)",
    "llama-3.1-8b-instant":    "Llama 3.1 8B  — fastest, lightest",
    "llama-4-scout-17b-16e-instruct": "Llama 4 Scout 17B — 512K context window",
    "gemma2-9b-it":            "Gemma 2 9B    — fast, efficient",
    "deepseek-r1-distill-llama-70b": "DeepSeek R1 Distill 70B — reasoning & math",
    "mistral-samba-24b":       "Mistral Samba 24B — multilingual",
}


# ── File helpers ──────────────────────────────────────────────────────────────

def read_pdf_file(path: str) -> str:
    """Extract text from a PDF file using PyPDF2."""
    try:
        import PyPDF2
    except ImportError as exc:
        raise RuntimeError(
            "PDF support requires the PyPDF2 package. Install it with:\n"
            "  pip install PyPDF2"
        ) from exc

    reader = PyPDF2.PdfReader(path)
    if not reader.pages:
        raise ValueError(f"PDF file contains no pages: {path}")

    pages: list[str] = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")

    text = "\n\n".join(pages).strip()
    if not text:
        raise ValueError(
            f"No extractable text found in PDF: {path}. "
            "The file may contain scanned images or protected content."
        )
    return text


def read_input_file(path: str) -> str:
    """Read text from a file with clear error messages."""
    file = Path(path)

    if not file.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    if not file.is_file():
        raise ValueError(f"Path is not a file: {path}")
    if file.stat().st_size == 0:
        raise ValueError(f"Input file is empty: {path}")

    if file.suffix.lower() == ".pdf":
        return read_pdf_file(path)

    try:
        return file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return file.read_text(encoding="latin-1")


def save_output(text: str, path: str) -> None:
    """Write response to a file, creating any missing parent directories."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"✓ Response saved to: {out.resolve()}")


def default_output_path(input_path: str) -> str:
    """Derive a timestamped output filename from the input path."""
    stem = Path(input_path).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{stem}_response_{timestamp}.txt"


# ── API call ──────────────────────────────────────────────────────────────────

def call_groq(
    file_content: str,
    prompt: str,
    model: str,
    max_tokens: int,
) -> tuple[str, dict]:
    """
    Send file content to the Groq API and return (response_text, usage_stats).

    Raises:
        EnvironmentError          – GROQ_API_KEY not set
        groq.AuthenticationError  – invalid API key (401)
        groq.PermissionDeniedError – key lacks access (403)
        groq.RateLimitError        – free-tier quota hit (429)
        groq.BadRequestError       – bad model name or params (400)
        groq.APIConnectionError    – network / connectivity issues
        groq.APIStatusError        – any other non-2xx response
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY environment variable is not set.\n"
            "  1. Get a free key at: https://console.groq.com/keys\n"
            "  2. Export it: export GROQ_API_KEY='your_api_key_here'"
        )

    client = Groq(api_key=api_key)

    user_message = f"{prompt}\n\n--- FILE CONTENT ---\n\n{file_content}"

    response = client.chat.completions.create(  #request to server
        model=model,
        max_completion_tokens=max_tokens,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Analyse the text provided by the "
                    "user and respond clearly and accurately."
                ),
            },
            {"role": "user", "content": user_message},
        ],  #request to api
    )

    text = response.choices[0].message.content or ""  #response to server and response to client
    usage = {
        "prompt_tokens":     response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens":      response.usage.total_tokens,
    }
    return text, usage


# ── CLI ───────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Send a text file to the Groq API and save the response.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "input", nargs="?",
        help="Path to the input text file",
    )
    p.add_argument(
        "--output", "-o",
        help="Path for the output file (auto-named if omitted)",
    )
    p.add_argument(
        "--prompt", "-p", default=DEFAULT_PROMPT,
        help="Instruction prepended to the file content",
    )
    p.add_argument(
        "--model", "-m", default=DEFAULT_MODEL,
        help=f"Groq model to use (default: {DEFAULT_MODEL})",
    )
    p.add_argument(
        "--max-tokens", "-t", type=int, default=DEFAULT_TOKENS,
        help=f"Max tokens for the response (default: {DEFAULT_TOKENS})",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Read the file and show what would be sent — no API call",
    )
    p.add_argument(
        "--list-models", action="store_true",
        help="Print available free-tier Groq models and exit",
    )
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # ── List models shortcut ──────────────────────────────────────────────────
    if args.list_models:
        print("\nAvailable Groq free-tier models:\n")
        for model_id, desc in AVAILABLE_MODELS.items():
            print(f"  {model_id}")
            print(f"    {desc}\n")
        print("Get your free API key at: https://console.groq.com/keys")
        return 0

    if not args.input:
        parser.error("the following argument is required: input")

    # ── 1. Read input file ────────────────────────────────────────────────────
    try:
        print(f"\nReading: {args.input}")
        content = read_input_file(args.input)
        print(f"  {len(content):,} characters loaded.")
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error reading file: {exc}", file=sys.stderr)
        return 1

    # ── 2. Dry-run shortcut ───────────────────────────────────────────────────
    if args.dry_run:
        print("\n── Dry run — request that would be sent ──")
        print(f"  Model      : {args.model}")
        print(f"  Max tokens : {args.max_tokens}")
        print(f"  Prompt     : {args.prompt}")
        preview = content[:300].replace("\n", " ")
        print(f"  Content    : {preview}{'...' if len(content) > 300 else ''}")
        return 0

    # ── 3. Call the Groq API ──────────────────────────────────────────────────
    try:
        print(f"Sending to Groq API  (model: {args.model}) …")
        response_text, usage = call_groq(
            file_content=content,
            prompt=args.prompt,
            model=args.model,
            max_tokens=args.max_tokens,
        )
        print(
            f"  Done.  tokens used — "
            f"prompt: {usage['prompt_tokens']}, "
            f"completion: {usage['completion_tokens']}, "
            f"total: {usage['total_tokens']}"
        )
    except EnvironmentError as exc:
        print(f"\nConfiguration error:\n  {exc}", file=sys.stderr)
        return 1
    except groq.AuthenticationError:
        print(
            "Authentication failed (401): your GROQ_API_KEY is invalid or expired.\n"
            "  Get a new key at: https://console.groq.com/keys",
            file=sys.stderr,
        )
        return 1
    except groq.PermissionDeniedError:
        print(
            "Permission denied (403): your key does not have access to this model.",
            file=sys.stderr,
        )
        return 1
    except groq.RateLimitError:
        print(
            "Rate limit hit (429): free tier allows 30 requests/min, 6K tokens/min.\n"
            "  Wait a moment and try again, or switch to a lighter model with --model.",
            file=sys.stderr,
        )
        return 1
    except groq.BadRequestError as exc:
        print(
            f"Bad request (400): {exc.message}\n"
            f"  Check the model name with --list-models.",
            file=sys.stderr,
        )
        return 1
    except groq.APIConnectionError as exc:
        print(f"Connection error: could not reach Groq API.\n  {exc}", file=sys.stderr)
        return 1
    except groq.APIStatusError as exc:
        print(
            f"API error {exc.status_code}: {exc.message}",
            file=sys.stderr,
        )
        return 1

    # ── 4. Save output ────────────────────────────────────────────────────────
    output_path = args.output or default_output_path(args.input)
    try:
        save_output(response_text, output_path)
    except OSError as exc:
        print(f"Failed to write output file: {exc}", file=sys.stderr)
        print("\n── Response (stdout fallback) ──\n")
        print(response_text)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())