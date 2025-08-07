
import streamlit as st
import os
import json
import io
from datetime import datetime
from dotenv import load_dotenv
import openai
from resume_parser import ResumeParser
from resume_generator import ResumeGenerator
from keyword_extractor import KeywordExtractor

# Load environment variables
load_dotenv()

class ResumeCustomizer:
    def __init__(self):
        self.parser = ResumeParser()
        self.generator = ResumeGenerator()
        self.keyword_extractor = KeywordExtractor()

    def process_resume_tailoring(self, resume_content, job_description, openai_key):
        """Main processing function for resume tailoring"""

        # Set OpenAI API key
        openai.api_key = openai_key

        # Get model from environment, with a fallback
        model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

        # Extract keywords and context from job description
        job_analysis = self.keyword_extractor.analyze_job_description(job_description)

        # Parse existing resume
        parsed_resume = self.parser.parse_resume_content(resume_content)

        # Generate tailored content
        tailored_content = self.generator.tailor_resume(
            parsed_resume,
            job_analysis,
            openai_key,
            model_name=model_name
        )

        return tailored_content

def main():
    st.set_page_config(
        page_title="Resume Tailoring Tool",
        page_icon="📄",
        layout="wide"
    )

    st.title("🎯 AI-Powered Resume Tailoring Tool")
    st.markdown("Upload your resume and job description to get a perfectly tailored resume!")

    # Sidebar for OpenAI API key
    with st.sidebar:
        st.header("Configuration")
        openai_key = st.text_input("OpenAI API Key", type="password", 
                                 help="Enter your OpenAI API key to enable AI features")

        st.markdown("---")
        st.markdown("### Instructions")
        st.markdown("""
        1. Upload your current resume (.docx or .txt)
        2. Upload job description (.pdf, .txt) or paste text
        3. Enter your OpenAI API key
        4. Click 'Tailor Resume' to generate optimized version
        """)

    # Main interface
    col1, col2 = st.columns(2)

    with col1:
        st.header("📋 Upload Resume")
        resume_file = st.file_uploader(
            "Choose your resume file", 
            type=['docx', 'txt'],
            help="Upload your current resume in .docx or .txt format"
        )

        if resume_file:
            st.success(f"Resume uploaded: {resume_file.name}")

    with col2:
        st.header("💼 Job Description")

        # Option to upload file or paste text
        input_method = st.radio("Input method:", ["Upload File", "Paste Text"])

        job_description = ""
        if input_method == "Upload File":
            jd_file = st.file_uploader(
                "Upload job description", 
                type=['pdf', 'txt'],
                help="Upload the job description file"
            )
            if jd_file:
                st.success(f"Job description uploaded: {jd_file.name}")
        else:
            job_description = st.text_area(
                "Paste job description here:",
                height=300,
                placeholder="Paste the complete job description..."
            )

    # Processing section
    if st.button("🚀 Tailor Resume", type="primary", use_container_width=True):
        if not openai_key:
            st.error("Please provide your OpenAI API key in the sidebar")
            return

        if not resume_file:
            st.error("Please upload your resume")
            return

        if not job_description and input_method == "Paste Text":
            st.error("Please provide a job description")
            return

        with st.spinner("Analyzing job requirements and tailoring your resume..."):
            try:
                # Initialize the resume customizer
                customizer = ResumeCustomizer()

                # Process the tailoring
                result = customizer.process_resume_tailoring(
                    resume_file, job_description, openai_key
                )

                # Display results
                st.success("Resume tailored successfully!")

                # Show the tailored content
                st.markdown("## 📋 Tailored Resume Content")

                # Key themes section
                if 'key_themes' in result:
                    st.markdown("### ✅ Key Themes From the Role & Company:")
                    st.markdown(result['key_themes'])

                # Tailored experience
                if 'experience' in result:
                    st.markdown("### 🛠 Tailored Resume Content:")
                    st.markdown(result['experience'])

                # Tailored projects
                if 'projects' in result:
                    st.markdown("### 🎓 Tailored Projects:")
                    st.markdown(result['projects'])

                # Extra keywords
                if 'missing_keywords' in result:
                    st.markdown("### 🧩 Extra Keywords to Add to Skills Section:")
                    st.markdown(", ".join(result['missing_keywords']))

                # Download button for the tailored resume
                if 'docx_content' in result:
                    st.download_button(
                        label="📥 Download Tailored Resume",
                        data=result['docx_content'],
                        file_name=f"tailored_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.error("Please check your API key and try again")

if __name__ == "__main__":
    main()
