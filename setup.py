
from setuptools import setup, find_packages

setup(
    name="resume-tailoring-tool",
    version="1.0.0",
    description="AI-powered resume tailoring tool built with Streamlit",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.32.0",
        "python-docx>=0.8.11",
        "PyPDF2>=3.0.1",
        "pdfplumber>=0.10.0",
        "openai>=1.10.0",
        "spacy>=3.7.0",
        "nltk>=3.8",
        "python-dotenv>=1.0.0",
        "fpdf2>=2.7.8"
    ],
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/resume-tailoring-tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
