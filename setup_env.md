# Environment Setup Guide

## 1. Create Virtual Environment

### Windows (PowerShell):
```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows (Command Prompt):
```cmd
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate.bat
```

### macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

## 2. Install Dependencies

```bash
# Install all packages
pip install -r requirements.txt

# Or install core packages only:
pip install requests python-dotenv openai
```

## 3. Set Up Environment Variables

```bash
# Copy the template
cp env_template.txt .env

# Edit .env with your actual keys
# OPENAI_API_KEY=sk-your-actual-key-here
# GOOGLE_APPS_SCRIPT_URL=your-actual-url-here
```

## 4. Test Your Setup

```bash
# Test the fetcher
python code/fetcher.py

# Test embeddings (after setting OPENAI_API_KEY)
python code/embed_responses.py
```

## 5. Deactivate Environment

```bash
deactivate
```

## Notes:
- Always activate your virtual environment before working
- The `.env` file is gitignored for security
- Use `pip freeze > requirements.txt` to update dependencies
