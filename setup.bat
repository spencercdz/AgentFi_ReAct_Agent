@echo off
echo 🚀 Setting up your Ollama + LangChain agent...

:: Create virtual environment
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate

:: Upgrade pip
python -m pip install --upgrade pip

:: Install dependencies
pip install -r requirements.txt

:: Pull the Ollama model (adjust if needed)
ollama pull mistral

echo ✅ Setup complete! To start using the environment, run:
echo venv\Scripts\activate