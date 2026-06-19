from __future__ import annotations

"""
process.py — Read a text/PDF file, send it to Groq API, and save response.

Usage:
    python process.py input.txt
    python process.py input.pdf
    python process.py input.txt --output response.txt
    python process.py input.txt --prompt "Summarize this"
    python process.py --list-models
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

import groq
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ── Config ─────────────────────────────────────────────
DEFAULT_MODEL = "llama-3.3-70b-versatile"
DEFAULT_TOKENS = 1024
DEFAULT_PROMPT = "Please read the following text and provide a clear response."

AVAILABLE_MODELS = {
    "llama-3.3-70b-versatile": "Best quality",
    "llama-3.1-8b-instant": "Fast model",
    "llama-4-scout-17b-16e-instruct": "Long context",
    "gemma2-9b-it": "Efficient model",
    "deepseek-r1-distill-llama-70b": "Reasoning model",
}

# ── File Reading ──────────────────────────────────────

def read_pdf(path: str) -> str:
    try:
        import PyPDF2
    except ImportError:
        raise RuntimeError("Install PyPDF2: pip install PyPDF2")

    reader = PyPDF2.PdfReader(path)
    text = "\n".join([(p.extract_text() or "") for p in reader.pages])
    return text.strip()


def read_file(path: str) -> str:
    file = Path(path)

    if not file.exists():
        raise FileNotFoundError("File not found")

    if file.suffix.lower() == ".pdf":
        return read_pdf(path)

    return file.read_text(encoding="utf-8", errors="ignore")


def save_file(text: str, path: str):
    Path(path).write_text(text, encoding="utf-8")


def default_output(input_path: str) -> str:
    name = Path(input_path).stem
    time = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name}_response_{time}.txt"

# ── Groq API ──────────────────────────────────────────

def call_groq(content: str, prompt: str, model: str, max_tokens: int):

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing GROQ_API_KEY in environment")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        max_completion_tokens=max_tokens,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": f"{prompt}\n\n{content}"
            }
        ],
    )

    return response.choices[0].message.content


# ── CLI ───────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?")
    parser.add_argument("--output", "-o")
    parser.add_argument("--prompt", "-p", default=DEFAULT_PROMPT)
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL)
    parser.add_argument("--max-tokens", "-t", type=int, default=DEFAULT_TOKENS)
    parser.add_argument("--list-models", action="store_true")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.list_models:
        for k, v in AVAILABLE_MODELS.items():
            print(k, ":", v)
        return 0

    if not args.input:
        print("Input file required")
        return 1

    try:
        content = read_file(args.input)
    except Exception as e:
        print("Error:", e)
        return 1

    if args.dry_run:
        print("MODEL:", args.model)
        print("PROMPT:", args.prompt)
        print("CONTENT PREVIEW:", content[:300])
        return 0

    try:
        result = call_groq(
            content,
            args.prompt,
            args.model,
            args.max_tokens
        )
    except Exception as e:
        print("API Error:", e)
        return 1

    out_file = args.output or default_output(args.input)
    save_file(result, out_file)

    print("Saved:", out_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())