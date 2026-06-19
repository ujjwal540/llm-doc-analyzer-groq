#!/usr/bin/env python3
"""
Simple script to ask questions about a PDF using Groq API
"""

import sys
from pathlib import Path
from process import read_input_file, call_groq, save_output, default_output_path

def query_pdf(pdf_path: str, question: str, model: str = "llama-3.3-70b-versatile"):
    """
    Ask a question about a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        question: Your question about the PDF
        model: Groq model to use (default: llama-3.3-70b-versatile)
    """
    try:
        # Read the PDF
        print(f"📄 Reading: {pdf_path}")
        content = read_input_file(pdf_path)
        print(f"✓ Loaded {len(content):,} characters\n")
        
        # Call the API
        print(f"🚀 Querying {model}...\n")
        response_text, usage = call_groq(
            file_content=content,
            prompt=question,
            model=model,
            max_tokens=1024,
        )
        
        # Display result
        print("=" * 70)
        print(response_text)
        print("=" * 70)
        print(f"\n📊 Tokens used: {usage['total_tokens']} "
              f"(prompt: {usage['prompt_tokens']}, completion: {usage['completion_tokens']})")
        
        # Save output
        output_path = default_output_path(pdf_path)
        save_output(response_text, output_path)
        print(f"✓ Response saved to: {output_path}")
        
        return response_text
        
    except FileNotFoundError:
        print(f"❌ Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Example usage
    query_pdf(
        pdf_path="sample-local-pdf.pdf",
        question="Please summarize this document in one line"
    )
