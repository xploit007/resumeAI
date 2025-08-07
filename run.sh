#!/bin/bash

# Resume Tailoring Tool Launch Script

echo "🎯 Starting AI-Powered Resume Tailoring Tool..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model if needed
echo "🧠 Setting up NLP model..."
python -m spacy download en_core_web_sm

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Copy .env.template to .env and add your OpenAI API key."
    cp .env.template .env
fi

# Launch the app
echo "🚀 Launching Resume Tailoring Tool..."
streamlit run streamlit_resume_tailor.py

echo "✅ Tool launched successfully! Open your browser to the URL shown above."
