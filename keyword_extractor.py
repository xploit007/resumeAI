
import openai
import re
import spacy
import nltk
from collections import Counter
from typing import Dict, List, Any, Tuple
import streamlit as st

# Download required NLTK data (if not already downloaded)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class KeywordExtractor:
    """Extracts keywords and analyzes job descriptions"""

    def __init__(self):
        self.spacy_model = None
        self.load_nlp_models()

    def load_nlp_models(self):
        """Load spaCy model if available"""
        try:
            self.spacy_model = spacy.load("en_core_web_sm")
        except OSError:
            st.warning("spaCy model 'en_core_web_sm' not found. Some features may be limited. "
                      "Install with: python -m spacy download en_core_web_sm")

    def analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """Comprehensive analysis of job description"""

        analysis = {
            'raw_text': job_description,
            'company_info': self._extract_company_info(job_description),
            'role_requirements': self._extract_role_requirements(job_description),
            'technical_skills': self._extract_technical_skills(job_description),
            'soft_skills': self._extract_soft_skills(job_description),
            'experience_requirements': self._extract_experience_requirements(job_description),
            'education_requirements': self._extract_education_requirements(job_description),
            'keywords': self._extract_keywords_comprehensive(job_description),
            'job_level': self._determine_job_level(job_description),
            'industry': self._determine_industry(job_description),
            'key_phrases': self._extract_key_phrases(job_description)
        }

        return analysis

    def _extract_company_info(self, text: str) -> Dict[str, str]:
        """Extract company-related information"""
        company_info = {
            'name': '',
            'industry': '',
            'size': '',
            'location': ''
        }

        # Company name is often in the first few lines
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            # Look for company indicators
            if any(indicator in line.lower() for indicator in ['company', 'corporation', 'inc', 'llc', 'ltd']):
                company_info['name'] = line
                break

        # Industry keywords
        industry_patterns = {
            'technology': ['software', 'tech', 'ai', 'machine learning', 'cloud', 'saas'],
            'healthcare': ['healthcare', 'medical', 'hospital', 'clinic', 'pharmaceutical'],
            'finance': ['financial', 'banking', 'investment', 'fintech', 'trading'],
            'consulting': ['consulting', 'advisory', 'strategy', 'management consulting'],
            'retail': ['retail', 'e-commerce', 'consumer', 'marketplace'],
            'manufacturing': ['manufacturing', 'automotive', 'industrial', 'production'],
        }

        text_lower = text.lower()
        for industry, keywords in industry_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                company_info['industry'] = industry
                break

        return company_info

    def _extract_role_requirements(self, text: str) -> Dict[str, List[str]]:
        """Extract role requirements and responsibilities"""
        requirements = {
            'responsibilities': [],
            'qualifications': [],
            'preferred_qualifications': []
        }

        # Common section headers
        responsibility_patterns = [
            r'responsibilities?:?(.*?)(?=requirements?|qualifications?|\n\n|$)',
            r'duties:?(.*?)(?=requirements?|qualifications?|\n\n|$)',
            r'you will:?(.*?)(?=requirements?|qualifications?|\n\n|$)'
        ]

        qualification_patterns = [
            r'requirements?:?(.*?)(?=preferred|nice.to.have|\n\n|$)',
            r'qualifications?:?(.*?)(?=preferred|nice.to.have|\n\n|$)',
            r'must.have:?(.*?)(?=preferred|nice.to.have|\n\n|$)'
        ]

        preferred_patterns = [
            r'preferred:?(.*?)(?=\n\n|$)',
            r'nice.to.have:?(.*?)(?=\n\n|$)',
            r'bonus:?(.*?)(?=\n\n|$)'
        ]

        text_lower = text.lower()

        # Extract responsibilities
        for pattern in responsibility_patterns:
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            if match:
                resp_text = match.group(1).strip()
                requirements['responsibilities'] = self._extract_bullet_points(resp_text)
                break

        # Extract qualifications
        for pattern in qualification_patterns:
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            if match:
                qual_text = match.group(1).strip()
                requirements['qualifications'] = self._extract_bullet_points(qual_text)
                break

        # Extract preferred qualifications
        for pattern in preferred_patterns:
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            if match:
                pref_text = match.group(1).strip()
                requirements['preferred_qualifications'] = self._extract_bullet_points(pref_text)
                break

        return requirements

    def _extract_bullet_points(self, text: str) -> List[str]:
        """Extract bullet points from text"""
        # Split by common bullet indicators
        bullet_patterns = ['•', '-', '*', '◦', '‣']

        points = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line starts with bullet
            for bullet in bullet_patterns:
                if line.startswith(bullet):
                    points.append(line[1:].strip())
                    break
            else:
                # If no bullet, check if it's a numbered item
                if re.match(r'^\d+\.', line):
                    points.append(re.sub(r'^\d+\.\s*', '', line))
                elif len(line) > 20:  # Assume it's a requirement if long enough
                    points.append(line)

        return points

    def _extract_technical_skills(self, text: str) -> List[str]:
        """Extract technical skills from job description"""

        # Common technical skills patterns
        tech_skills = {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
                'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql'
            ],
            'frameworks': [
                'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express',
                'nodejs', 'laravel', 'rails', 'asp.net', 'tensorflow', 'pytorch',
                'scikit-learn', 'pandas', 'numpy'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'elasticsearch',
                'oracle', 'sqlite', 'dynamodb', 'neo4j'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'kubernetes', 'docker',
                'terraform', 'ansible', 'jenkins'
            ],
            'tools': [
                'git', 'jira', 'confluence', 'tableau', 'power bi', 'looker',
                'jupyter', 'linux', 'unix', 'bash', 'powershell'
            ]
        }

        found_skills = set()
        text_lower = text.lower()

        # Extract skills from all categories
        for category, skills in tech_skills.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills.add(skill)

        # Also look for skills mentioned with specific patterns
        skill_patterns = [
            r'experience with ([a-zA-Z+#.\s]+?)(?:,|\.|;|\n)',
            r'proficient in ([a-zA-Z+#.\s]+?)(?:,|\.|;|\n)',
            r'knowledge of ([a-zA-Z+#.\s]+?)(?:,|\.|;|\n)',
            r'familiar with ([a-zA-Z+#.\s]+?)(?:,|\.|;|\n)',
        ]

        for pattern in skill_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                skill = match.group(1).strip()
                if len(skill) < 30:  # Reasonable skill name length
                    found_skills.add(skill)

        return list(found_skills)

    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills from job description"""

        soft_skills_keywords = [
            'communication', 'leadership', 'teamwork', 'collaboration', 'problem solving',
            'analytical', 'critical thinking', 'creativity', 'adaptability', 'flexibility',
            'time management', 'organization', 'detail oriented', 'multitasking',
            'interpersonal', 'presentation', 'negotiation', 'customer service',
            'project management', 'strategic thinking', 'innovation', 'mentoring'
        ]

        found_soft_skills = []
        text_lower = text.lower()

        for skill in soft_skills_keywords:
            if skill in text_lower:
                found_soft_skills.append(skill)

        return found_soft_skills

    def _extract_experience_requirements(self, text: str) -> Dict[str, Any]:
        """Extract experience requirements"""

        experience_info = {
            'years_required': None,
            'level': '',
            'specific_experience': []
        }

        # Extract years of experience
        years_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'minimum\s*(\d+)\s*years?',
            r'at\s*least\s*(\d+)\s*years?',
            r'(\d+)\+\s*years?'
        ]

        text_lower = text.lower()
        for pattern in years_patterns:
            match = re.search(pattern, text_lower)
            if match:
                experience_info['years_required'] = int(match.group(1))
                break

        # Determine level based on keywords
        if any(keyword in text_lower for keyword in ['senior', 'lead', 'principal', 'architect']):
            experience_info['level'] = 'Senior'
        elif any(keyword in text_lower for keyword in ['junior', 'entry', 'associate']):
            experience_info['level'] = 'Junior'
        else:
            experience_info['level'] = 'Mid-level'

        return experience_info

    def _extract_education_requirements(self, text: str) -> List[str]:
        """Extract education requirements"""

        education_requirements = []
        text_lower = text.lower()

        degree_patterns = [
            r"bachelor'?s?\s*(?:degree)?\s*(?:in\s*)?([a-zA-Z\s]+)",
            r"master'?s?\s*(?:degree)?\s*(?:in\s*)?([a-zA-Z\s]+)",
            r"phd\s*(?:in\s*)?([a-zA-Z\s]+)",
            r"doctorate\s*(?:in\s*)?([a-zA-Z\s]+)"
        ]

        for pattern in degree_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                education_requirements.append(match.group(0))

        return education_requirements

    def _extract_keywords_comprehensive(self, text: str) -> List[str]:
        """Extract comprehensive keywords using multiple methods"""

        keywords = set()

        # Method 1: spaCy-based extraction
        if self.spacy_model:
            keywords.update(self._extract_keywords_spacy(text))

        # Method 2: NLTK-based extraction
        keywords.update(self._extract_keywords_nltk(text))

        # Method 3: Domain-specific patterns
        keywords.update(self._extract_domain_keywords(text))

        return list(keywords)

    def _extract_keywords_spacy(self, text: str) -> List[str]:
        """Extract keywords using spaCy"""

        if not self.spacy_model:
            return []

        doc = self.spacy_model(text)
        keywords = set()

        # Extract named entities
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'TECH', 'SKILL']:
                keywords.add(ent.text.lower())

        # Extract nouns and proper nouns
        for token in doc:
            if (token.pos_ in ['NOUN', 'PROPN'] and 
                not token.is_stop and 
                not token.is_punct and 
                len(token.text) > 2):
                keywords.add(token.lemma_.lower())

        return list(keywords)

    def _extract_keywords_nltk(self, text: str) -> List[str]:
        """Extract keywords using NLTK"""

        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        from nltk.tag import pos_tag

        try:
            stop_words = set(stopwords.words('english'))
        except:
            stop_words = set()

        # Tokenize and get POS tags
        tokens = word_tokenize(text.lower())
        pos_tags = pos_tag(tokens)

        keywords = set()

        # Extract nouns, proper nouns, and adjectives
        for word, pos in pos_tags:
            if (pos in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ'] and
                word not in stop_words and
                word.isalpha() and
                len(word) > 2):
                keywords.add(word)

        return list(keywords)

    def _extract_domain_keywords(self, text: str) -> List[str]:
        """Extract domain-specific keywords"""

        # Industry-specific keyword patterns
        domain_patterns = {
            'data_science': ['machine learning', 'deep learning', 'neural networks', 'data mining',
                           'statistical analysis', 'predictive modeling', 'data visualization'],
            'software_engineering': ['software development', 'code review', 'version control',
                                   'agile', 'scrum', 'ci/cd', 'microservices'],
            'project_management': ['project management', 'stakeholder management', 'risk management',
                                 'budget management', 'timeline management'],
            'business_analysis': ['business analysis', 'requirements gathering', 'process improvement',
                                'stakeholder analysis', 'gap analysis']
        }

        found_keywords = set()
        text_lower = text.lower()

        for domain, keywords in domain_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_keywords.add(keyword)

        return list(found_keywords)

    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract important key phrases"""

        # Common important phrases in job descriptions
        key_phrase_patterns = [
            r'responsible for ([^.\n]+)',
            r'experience (?:in|with) ([^.\n]+)',
            r'ability to ([^.\n]+)',
            r'skilled in ([^.\n]+)',
            r'proficiency in ([^.\n]+)',
            r'knowledge of ([^.\n]+)',
            r'expertise in ([^.\n]+)'
        ]

        phrases = set()
        text_lower = text.lower()

        for pattern in key_phrase_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                phrase = match.group(1).strip()
                if len(phrase) < 100:  # Reasonable phrase length
                    phrases.add(phrase)

        return list(phrases)

    def _determine_job_level(self, text: str) -> str:
        """Determine the job level from the description"""

        text_lower = text.lower()

        senior_indicators = ['senior', 'lead', 'principal', 'architect', 'director', 'manager', 'head of']
        junior_indicators = ['junior', 'entry', 'associate', 'intern', 'graduate', 'trainee']

        if any(indicator in text_lower for indicator in senior_indicators):
            return 'Senior'
        elif any(indicator in text_lower for indicator in junior_indicators):
            return 'Junior'
        else:
            return 'Mid-level'

    def _determine_industry(self, text: str) -> str:
        """Determine the industry from the job description"""

        industry_keywords = {
            'Technology': ['software', 'tech', 'ai', 'machine learning', 'cloud', 'saas', 'fintech'],
            'Healthcare': ['healthcare', 'medical', 'hospital', 'clinic', 'pharmaceutical', 'biotech'],
            'Finance': ['financial', 'banking', 'investment', 'trading', 'insurance', 'fintech'],
            'Consulting': ['consulting', 'advisory', 'strategy', 'management consulting'],
            'Education': ['education', 'university', 'school', 'academic', 'learning'],
            'Retail': ['retail', 'e-commerce', 'consumer', 'marketplace', 'fashion'],
            'Manufacturing': ['manufacturing', 'automotive', 'industrial', 'production', 'supply chain']
        }

        text_lower = text.lower()

        for industry, keywords in industry_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return industry

        return 'General'

    def generate_keyword_suggestions(self, job_analysis: Dict[str, Any], 
                                   resume_keywords: List[str]) -> List[str]:
        """Generate keyword suggestions for resume optimization"""

        job_keywords = set()

        # Collect all keywords from job analysis
        if 'technical_skills' in job_analysis:
            job_keywords.update(job_analysis['technical_skills'])
        if 'soft_skills' in job_analysis:
            job_keywords.update(job_analysis['soft_skills'])
        if 'keywords' in job_analysis:
            job_keywords.update(job_analysis['keywords'])

        # Find missing keywords
        resume_keywords_lower = [kw.lower() for kw in resume_keywords]
        missing_keywords = []

        for keyword in job_keywords:
            if keyword.lower() not in resume_keywords_lower:
                missing_keywords.append(keyword)

        # Sort by importance (you could implement a scoring system here)
        return missing_keywords[:20]  # Return top 20 suggestions
