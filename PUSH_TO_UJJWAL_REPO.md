# Push Code to GitHub Repository

## Your Repository
🔗 https://github.com/ujjwal540/llm-doc-analyzer-groq

## Commands to Push (Copy & Paste in PowerShell)

```powershell
# Navigate to your project
cd "C:\Users\kumari rekha das\OneDrive\AI_agent"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Add Groq PDF Processor: LLM-powered document analysis tool"

# Add your repository as remote
git remote add origin https://github.com/ujjwal540/llm-doc-analyzer-groq.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

## If Repository Already Has Code

If the repo already has content, use:

```powershell
cd "C:\Users\kumari rekha das\OneDrive\AI_agent"

# Fetch existing content first
git fetch origin main

# If you want to replace everything:
git init
git add .
git commit -m "Add Groq PDF Processor: LLM-powered document analysis tool"
git remote add origin https://github.com/ujjwal540/llm-doc-analyzer-groq.git
git branch -M main
git push -u origin main --force

# OR if you want to merge:
git pull origin main --rebase
git push origin main
```

## Troubleshooting

**If git remote already exists:**
```powershell
# Check existing remotes
git remote -v

# Remove old remote
git remote remove origin

# Add correct one
git remote add origin https://github.com/ujjwal540/llm-doc-analyzer-groq.git
```

**If authentication fails:**
```powershell
# Use GitHub CLI (recommended)
gh auth login
# Follow prompts and select HTTPS

# Then retry push
git push -u origin main
```

## Verify Success

After pushing, check: https://github.com/ujjwal540/llm-doc-analyzer-groq

You should see:
- ✅ process.py
- ✅ main.py
- ✅ query_pdf.py
- ✅ README.md
- ✅ requirement.txt
- ✅ .gitignore
- ✅ .env.example

---

## Files Being Pushed

```
✓ process.py              - Main LLM processor
✓ main.py                 - Entry point
✓ query_pdf.py            - PDF query script
✓ requirement.txt         - Dependencies
✓ .gitignore              - Git ignore rules
✓ .env.example            - Config template
✓ README.md               - Documentation
✓ GITHUB_PUSH_GUIDE.md    - This guide
```

**NOT being pushed (in .gitignore):**
- ✗ .env (contains API keys - safe!)
- ✗ *.pdf (to save space)
- ✗ __pycache__/
- ✗ *_response_*.txt files

---

## Quick Start (Just Copy-Paste This)

```powershell
cd "C:\Users\kumari rekha das\OneDrive\AI_agent"
git init
git add .
git commit -m "Add Groq PDF Processor: LLM-powered document analysis tool"
git remote add origin https://github.com/ujjwal540/llm-doc-analyzer-groq.git
git branch -M main
git push -u origin main
```

**Done! Check your repo in 10 seconds.** ✨
