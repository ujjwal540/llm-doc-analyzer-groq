# llm-doc-analyzer-groq

An AI-powered document processing tool that reads PDFs and text files, sends them to the Groq LLM API, and provides intelligent responses.

## Features

 **Multi-Format Support**: Process PDFs and text files seamlessly  
 **Fast LLM Processing**: Uses Groq's free-tier models for rapid inference  
 **Custom Prompts**: Ask specific questions or provide custom instructions  
 **Auto-Save**: Responses are automatically saved with timestamps  
 **CLI & Programmatic**: Use as a command-line tool or import as a Python module  
 **Token Tracking**: Monitor API token usage  

## Supported Models

- `llama-3.3-70b-versatile`  (recommended - best quality)
- `llama-3.1-8b-instant` (fastest)
- `llama-4-scout-17b-16e-instruct` (512K context)
- `gemma2-9b-it` (efficient)
- `deepseek-r1-distill-llama-70b` (reasoning & math)
- `mistral-samba-24b` (multilingual)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/groq-pdf-processor.git
cd groq-pdf-processor
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirement.txt
```

4. Set up your Groq API key:
```bash
# Create a .env file
echo GROQ_API_KEY=your_api_key_here > .env
```

Get your free API key at: https://console.groq.com/keys

## Usage

### Command Line

**Process a PDF or text file:**
```bash
python process.py sample-local-pdf.pdf --prompt "Summarize this document"
```

**List available models:**
```bash
python process.py --list-models
```

**Dry-run (preview without API call):**
```bash
python process.py input.txt --dry-run
```

**Custom output file:**
```bash
python process.py input.txt --output my_response.txt
```

**Change model:**
```bash
python process.py input.txt --model llama-3.1-8b-instant
```

### Python Script

```python
from query_pdf import query_pdf

response = query_pdf(
    pdf_path="sample-local-pdf.pdf",
    question="What is the main topic?",
    model="llama-3.3-70b-versatile"
)
print(response)
```

Or use `main.py`:
```bash
python main.py sample-local-pdf.pdf --prompt "Your question here"
```

## File Structure

```
groq-pdf-processor/
├── process.py              # Main processing engine
├── main.py                 # Entry point
├── query_pdf.py            # Simple PDF query script
├── requirement.txt         # Python dependencies
├── .env                    # API keys (not committed)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Examples

**One-line summary:**
```bash
python process.py sample-local-pdf.pdf --prompt "Tell me one line about this"
```

**Extract key points:**
```bash
python process.py document.txt --prompt "List 5 key points from this document"
```

**Translation:**
```bash
python process.py text.txt --prompt "Translate to Spanish" --model mistral-samba-24b
```

**Code analysis:**
```bash
python process.py code.py --prompt "Explain what this code does"
```

## Configuration

### Default Settings (in `process.py`)

```python
DEFAULT_MODEL  = "llama-3.3-70b-versatile"
DEFAULT_TOKENS = 1024
DEFAULT_PROMPT = "Please read the following text and provide a thoughtful response:"
```

Modify these to change defaults.

## API Limits (Free Tier)

- **Rate**: 30 requests/min
- **Tokens**: 6,000 tokens/min
- **Max tokens per request**: No strict limit, but respect rate limits

## Troubleshooting

**"Authentication failed (401)"**
- Check your `GROQ_API_KEY` in `.env`
- Get a new key at: https://console.groq.com/keys

**"Rate limit hit (429)"**
- Wait a moment and try again
- Use a smaller model: `--model llama-3.1-8b-instant`

**"No extractable text found in PDF"**
- PDF may contain only images (scanned document)
- Try OCR tools first or manually extract text

**"PyPDF2 not installed"**
```bash
pip install PyPDF2
```

## Requirements

- Python 3.8+
- `groq>=0.9.0`
- `python-dotenv>=1.0.0`
- `PyPDF2>=3.0.0`

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


