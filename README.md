# AI-Powered Resume Tailoring Tool

A comprehensive Streamlit application that uses AI to tailor resumes to specific job descriptions, making your applications more targeted and effective.

## Features

- **Resume Upload**: Support for .docx, .txt, and .pdf resume formats
- **Job Description Analysis**: Intelligent parsing of job requirements and keywords
- **AI-Powered Tailoring**: Uses local open-source GPT models (via [Ollama](https://ollama.com)) to rewrite experience bullets and generate relevant projects
- **Keyword Optimization**: Identifies missing keywords and suggests improvements for ATS systems
- **Document Generation**: Creates downloadable Word documents with tailored content
- **Multiple Input Methods**: Upload files or paste text directly

## Installation

### Option 1: Direct Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/resume-tailoring-tool.git
cd resume-tailoring-tool
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Install spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

4. Install and run a local language model using [Ollama](https://ollama.com):
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gpt-oss:20b
```

### Option 2: Using Setup.py

```bash
pip install -e .
python -m spacy download en_core_web_sm
```

## Usage

### Local Development

1. Run the Streamlit app:
```bash
streamlit run streamlit_resume_tailor.py
```

2. Open your browser to `http://localhost:8501`

3. Follow the on-screen instructions:
   - Ensure your local model (e.g., `gpt-oss:20b`) is running via Ollama
   - Upload your resume (.docx or .txt format)
   - Upload job description or paste the text
   - Click "Tailor Resume" to generate optimized content

### Configuration

The application uses a local model served by Ollama. You can override the default model name by setting the `MODEL_NAME` environment variable.

## Project Structure

```
resume-tailoring-tool/
├── streamlit_resume_tailor.py      # Main Streamlit application
├── resume_parser.py                # Resume parsing and text extraction
├── keyword_extractor.py            # Job description analysis and keyword extraction
├── resume_generator.py             # AI-powered content generation and document creation
├── requirements.txt                # Python dependencies
├── setup.py                       # Package installation script
├── .env.template                  # Environment variables template
└── README.md                      # This file
```

## Key Components

### ResumeParser
- Extracts text from DOCX, TXT, and PDF files
- Parses resume sections (experience, education, skills, projects)
- Handles various resume formats and structures

### KeywordExtractor
- Analyzes job descriptions using NLP techniques
- Extracts technical skills, soft skills, and requirements
- Uses spaCy and NLTK for comprehensive text analysis
- Identifies industry and job level context

### ResumeGenerator
- Uses local GPT models via Ollama for content generation
- Tailors experience bullets to match job requirements
- Generates relevant projects based on job context
- Creates formatted Word documents for download

## Features in Detail

### Resume Analysis
- **Contact Information**: Extracts name, email, phone
- **Experience Parsing**: Identifies companies, positions, dates, and bullet points
- **Skills Extraction**: Finds technical and soft skills
- **Education Detection**: Locates degree information
- **Project Identification**: Parses academic and personal projects

### Job Description Analysis
- **Company Information**: Extracts company name and industry
- **Role Requirements**: Identifies responsibilities and qualifications
- **Technical Skills**: Finds required programming languages, frameworks, tools
- **Experience Level**: Determines seniority level (Junior/Mid/Senior)
- **Keyword Extraction**: Uses multiple NLP techniques for comprehensive analysis

### AI-Powered Tailoring
- **Experience Rewriting**: Transforms existing bullets to highlight relevant skills
- **Project Generation**: Creates 1-2 new projects relevant to the target role
- **Keyword Integration**: Naturally incorporates important terms from job descriptions
- **Formatting Consistency**: Maintains professional resume structure

## Deployment Options

### Streamlit Community Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click
5. Ensure the deployment environment can access the Ollama service and required model

### Other Platforms

The application can be deployed on:
- Heroku
- AWS EC2
- Google Cloud Platform
- Azure App Service
- Railway
- Render

## Customization

### Adding New Resume Formats
Extend the `ResumeParser` class to support additional file formats:

```python
def _extract_from_new_format(self, file_obj) -> str:
    # Implementation for new format
    pass
```

### Modifying AI Prompts
Update prompts in `ResumeGenerator` to change how content is generated:

```python
def _tailor_experience_bullets(self, experience, job_analysis):
    prompt = f"""
    Your custom prompt here...
    """
```

### Adding New Analysis Features
Extend `KeywordExtractor` with domain-specific analysis:

```python
def _extract_domain_specific_keywords(self, text):
    # Custom extraction logic
    pass
```

## Troubleshooting

### Common Issues

1. **spaCy Model Not Found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Ollama Model Errors**
   - Verify the Ollama service is running
   - Ensure the requested model is installed (e.g., `ollama pull gpt-oss:20b`)

3. **File Upload Issues**
   - Ensure files are in supported formats (.docx, .txt, .pdf)
   - Check file size limits (Streamlit default: 200MB)

4. **PDF Parsing Problems**
   - Some complex PDFs may not parse correctly
   - Try converting to .docx format for better results

### Performance Optimization

- Use `gpt-3.5-turbo` instead of `gpt-4` for faster responses
- Implement caching for repeated job descriptions
- Optimize text preprocessing for large documents

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Ollama and the open-source model community
- spaCy and NLTK for natural language processing
- Streamlit for the web framework
- python-docx for Word document manipulation

## Support

For support, please open an issue on GitHub or contact [your-email@example.com].

## Roadmap

- [ ] Support for more file formats (RTF, HTML)
- [ ] Integration with job boards (LinkedIn, Indeed)
- [ ] Advanced ATS scoring and optimization
- [ ] Multiple language support
- [ ] Resume template customization
- [ ] Batch processing for multiple applications
- [ ] Analytics dashboard for application tracking

---

**Note**: This tool requires a locally running language model (e.g., via Ollama). Ensure the service is running and the appropriate model is installed.
