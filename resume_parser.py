
import os
import docx
import PyPDF2
import pdfplumber
import re
from typing import Dict, List, Any
import streamlit as st

class ResumeParser:
    """Handles parsing of resume files in various formats"""

    def __init__(self):
        self.supported_formats = ['.docx', '.txt', '.pdf']

    def parse_resume_content(self, file_obj) -> Dict[str, Any]:
        """Parse resume content from uploaded file"""

        if not file_obj:
            raise ValueError("No file provided")

        file_extension = os.path.splitext(file_obj.name)[1].lower()

        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")

        # Extract text based on file type
        if file_extension == '.docx':
            text = self._extract_from_docx(file_obj)
        elif file_extension == '.txt':
            text = self._extract_from_txt(file_obj)
        elif file_extension == '.pdf':
            text = self._extract_from_pdf(file_obj)

        # Parse the extracted text into structured data
        parsed_data = self._parse_text_content(text)
        parsed_data['original_text'] = text
        parsed_data['file_name'] = file_obj.name

        return parsed_data

    def _extract_from_docx(self, file_obj) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_obj)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text)
        except Exception as e:
            raise ValueError(f"Error reading DOCX file: {str(e)}")

    def _extract_from_txt(self, file_obj) -> str:
        """Extract text from TXT file"""
        try:
            # Read as string
            content = file_obj.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            return content
        except Exception as e:
            raise ValueError(f"Error reading TXT file: {str(e)}")

    def _extract_from_pdf(self, file_obj) -> str:
        """Extract text from PDF file"""
        try:
            # Try with pdfplumber first (better for complex layouts)
            text = ""
            with pdfplumber.open(file_obj) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            # If pdfplumber didn't work well, try PyPDF2
            if len(text.strip()) < 100:  # Fallback if extraction was poor
                file_obj.seek(0)  # Reset file pointer
                pdf_reader = PyPDF2.PdfReader(file_obj)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"

            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")

    def _parse_text_content(self, text: str) -> Dict[str, Any]:
        """Parse text content into structured resume sections"""

        # Convert to lowercase for pattern matching
        text_lower = text.lower()

        # Initialize sections
        sections = {
            'contact_info': self._extract_contact_info(text),
            'experience': self._extract_experience_section(text),
            'education': self._extract_education_section(text),
            'skills': self._extract_skills_section(text),
            'projects': self._extract_projects_section(text),
            'summary': self._extract_summary_section(text),
        }

        return sections

    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information"""
        contact_info = {}

        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group()

        # Phone pattern (various formats)
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',
            r'\+1[-.\s]?\d{3}[-.]?\d{3}[-.]?\d{4}'
        ]

        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact_info['phone'] = phone_match.group()
                break

        # Name extraction (first few words before email/phone)
        lines = text.split('\n')
        if lines:
            # Usually name is in the first few lines
            for line in lines[:3]:
                line = line.strip()
                if line and len(line.split()) <= 4 and len(line) > 2:
                    # Likely a name
                    if not any(char.isdigit() for char in line):
                        contact_info['name'] = line
                        break

        return contact_info

    def _extract_experience_section(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience section"""
        experience_keywords = ['experience', 'work history', 'professional experience', 
                             'employment', 'work experience', 'career history']

        # Find experience section
        experience_section = self._find_section(text, experience_keywords)

        if not experience_section:
            return []

        # Parse individual experiences
        experiences = []

        # Split by common patterns that indicate new job entries
        job_patterns = [
            r'\n\n(?=[A-Z][^\n]*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))',
            r'\n(?=[A-Z][^\n]*\b\d{4}\b)',
            r'\n(?=[A-Z][^\n]*(?:Present|Current))'
        ]

        for pattern in job_patterns:
            if re.search(pattern, experience_section):
                job_entries = re.split(pattern, experience_section)
                break
        else:
            job_entries = [experience_section]

        for entry in job_entries:
            if entry.strip():
                experiences.append(self._parse_job_entry(entry.strip()))

        return experiences

    def _parse_job_entry(self, entry: str) -> Dict[str, Any]:
        """Parse individual job entry"""
        lines = entry.split('\n')

        job_info = {
            'company': '',
            'position': '',
            'dates': '',
            'bullets': [],
            'location': ''
        }

        # Extract company, position, dates from first few lines
        for i, line in enumerate(lines[:3]):
            line = line.strip()
            if not line:
                continue

            # Look for date patterns
            date_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{1,2}/).*?\d{4}\b'
            if re.search(date_pattern, line):
                job_info['dates'] = line
                continue

            # If we haven't found company/position yet
            if not job_info['company']:
                job_info['company'] = line
            elif not job_info['position']:
                job_info['position'] = line

        # Extract bullet points
        for line in lines:
            line = line.strip()
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                job_info['bullets'].append(line[1:].strip())
            elif line.startswith('◦') or line.startswith('‣'):
                job_info['bullets'].append(line[1:].strip())

        return job_info

    def _extract_education_section(self, text: str) -> List[Dict[str, Any]]:
        """Extract education section"""
        education_keywords = ['education', 'academic background', 'qualifications', 
                            'degrees', 'academic history']

        education_section = self._find_section(text, education_keywords)

        if not education_section:
            return []

        education_entries = []
        lines = education_section.split('\n')

        for line in lines:
            line = line.strip()
            if line and (any(degree in line.lower() for degree in 
                           ['bachelor', 'master', 'phd', 'doctorate', 'associate', 'bs', 'ms', 'ba', 'ma'])):
                education_entries.append({'degree': line})

        return education_entries

    def _extract_skills_section(self, text: str) -> List[str]:
        """Extract skills section"""
        skills_keywords = ['skills', 'technical skills', 'core competencies', 
                          'technologies', 'expertise', 'proficiencies']

        skills_section = self._find_section(text, skills_keywords)

        if not skills_section:
            return []

        # Extract skills - they're often comma or bullet separated
        skills = []

        # Remove section headers
        skills_text = re.sub(r'^.*?(?:skills|technologies|expertise).*?:?\n', '', 
                           skills_section, flags=re.IGNORECASE)

        # Split by common separators
        if ',' in skills_text:
            skills = [skill.strip() for skill in skills_text.split(',')]
        elif '•' in skills_text:
            skills = [skill.strip().lstrip('•').strip() for skill in skills_text.split('•')]
        else:
            # Split by lines and clean up
            skills = [line.strip() for line in skills_text.split('\n') if line.strip()]

        return [skill for skill in skills if skill and len(skill) < 50]

    def _extract_projects_section(self, text: str) -> List[Dict[str, Any]]:
        """Extract projects section"""
        projects_keywords = ['projects', 'personal projects', 'academic projects', 
                           'relevant projects', 'key projects']

        projects_section = self._find_section(text, projects_keywords)

        if not projects_section:
            return []

        projects = []

        # Split into individual projects
        project_entries = re.split(r'\n(?=[A-Z][^\n]*(?:Project|\w+\s*[-–]|\w+,))', projects_section)

        for entry in project_entries:
            if entry.strip():
                project = self._parse_project_entry(entry.strip())
                if project:
                    projects.append(project)

        return projects

    def _parse_project_entry(self, entry: str) -> Dict[str, Any]:
        """Parse individual project entry"""
        lines = entry.split('\n')

        project_info = {
            'title': '',
            'description': '',
            'technologies': [],
            'dates': '',
            'bullets': []
        }

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            if i == 0:  # First line is usually the title
                project_info['title'] = line
            elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
                project_info['bullets'].append(line[1:].strip())
            else:
                if not project_info['description']:
                    project_info['description'] = line

        return project_info

    def _extract_summary_section(self, text: str) -> str:
        """Extract summary/objective section"""
        summary_keywords = ['summary', 'objective', 'profile', 'professional summary', 
                          'career objective', 'about me']

        summary_section = self._find_section(text, summary_keywords)

        if summary_section:
            # Clean up the summary
            summary_lines = [line.strip() for line in summary_section.split('\n') if line.strip()]
            # Remove the header line if it exists
            if summary_lines and any(keyword in summary_lines[0].lower() 
                                   for keyword in summary_keywords):
                summary_lines = summary_lines[1:]

            return ' '.join(summary_lines)

        return ""

    def _find_section(self, text: str, keywords: List[str]) -> str:
        """Find a section in the text based on keywords"""
        text_lines = text.split('\n')
        section_start = -1
        section_end = len(text_lines)

        # Find section start
        for i, line in enumerate(text_lines):
            line_lower = line.lower().strip()
            if any(keyword in line_lower for keyword in keywords):
                section_start = i
                break

        if section_start == -1:
            return ""

        # Find section end (next major section or end of document)
        common_sections = ['experience', 'education', 'skills', 'projects', 
                          'certifications', 'awards', 'references']

        for i in range(section_start + 1, len(text_lines)):
            line_lower = text_lines[i].lower().strip()
            if any(section in line_lower for section in common_sections):
                if not any(keyword in line_lower for keyword in keywords):
                    section_end = i
                    break

        return '\n'.join(text_lines[section_start:section_end])
