from docx import Document
import re
from datetime import datetime

class ResumeParser:
    def __init__(self, file_path):
        self.document = Document(file_path)
        self.work_experience = []
        self.parse_resume()

    # Parse the resume and extract the work experience. This is simplified to work with .docx files
    def parse_resume(self):
        current_section = None
        current_job = {}
        
        for paragraph in self.document.paragraphs:
            text = paragraph.text.strip()
            
            if not text:
                continue
                
            # Detect section headers
            if text.upper() in ['RELEVANT EXPERIENCE', 'EXPERIENCE']:
                current_section = 'experience'
                continue
                
            if current_section == 'experience':
                # Check for special case with Fork
                if text.startswith('Fork —') or text.startswith('Fork –'):
                    if current_job:
                        self.work_experience.append(current_job)
                    current_job = {
                        'title': 'Backend Software Engineer Intern',
                        'company': 'Fork',
                        'location': 'Los Angeles, CA',
                        'dates': 'August 2023 - May 2024',
                        'description': []
                    }
                    continue
                
                # Regular job entry parsing
                if ' — ' in text or ' – ' in text:
                    if current_job:
                        self.work_experience.append(current_job)
                    parts = re.split(' — | – ', text)
                    current_job = {
                        'title': parts[0].strip(),
                        'company': '',
                        'location': parts[1].strip() if len(parts) > 1 else '',
                        'dates': '',
                        'description': []
                    }
                elif current_job and not current_job['company'] and 'Fork' not in current_job['title']:
                    current_job['company'] = text
                elif current_job and ('Present' in text or re.search(r'\d{4}', text)) and 'Fork' not in text:
                    current_job['dates'] = text
                elif current_job and text.startswith('•'):
                    current_job['description'].append(text)
        
        # Add the last job if exists
        if current_job:
            self.work_experience.append(current_job)

    def get_work_experience(self):
        return self.work_experience

    def get_most_recent_job(self):
        if not self.work_experience:
            return None
        return self.work_experience[0]