# llm-doc-analyzer-groq

AI tool that reads PDFs and text files and lets you query them using Groq LLMs.  
It extracts content, sends it to a model, and returns focused, useful answers.

---

## What it does

- Reads PDF and text files
- Sends extracted content to Groq LLM API
- Lets you ask questions or give instructions
- Saves responses locally with timestamps
- Works via CLI or Python import

---

## Models you can use

- llama-3.3-70b-versatile (best quality)
- llama-3.1-8b-instant (fast)
- llama-4-scout-17b-16e-instruct (large context)
- gemma2-9b-it
- deepseek-r1-distill-llama-70b
- mistral-samba-24b

---

## Setup

```bash
git clone https://github.com/yourusername/groq-pdf-processor.git
cd groq-pdf-processor

python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

## Create .env file:

GROQ_API_KEY=your_api_key_here

## How to use
CLI
python process.py file.pdf --prompt "Summarize this"

## List models:

python process.py --list-models

## Change model:

python process.py file.txt --model llama-3.1-8b-instant

## Python
from query_pdf import query_pdf

print(query_pdf(
    pdf_path="sample.pdf",
    question="What is this about?",
    model="llama-3.3-70b-versatile"
))

