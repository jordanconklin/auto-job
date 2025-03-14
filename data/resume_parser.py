from .resume_data import RESUME_DATA

class ResumeParser:
    def __init__(self, file_path=None):
        # We'll ignore file_path since we're using static data
        self.work_experience = RESUME_DATA["work_experience"]
        self.personal = RESUME_DATA["personal"]
        self.education = RESUME_DATA["education"]
        self.skills = RESUME_DATA["skills"]
        self.projects = RESUME_DATA["projects"]

    def parse_resume(self):
        # No need to parse anything
        pass

    def get_work_experience(self):
        return self.work_experience

    def get_most_recent_job(self):
        return self.work_experience[0] if self.work_experience else None

    def get_skills(self):
        return {
            "full_stack": ", ".join(self.skills["full_stack"]),
            "ai_ml": ", ".join(self.skills["ai_ml"])
        }

    def get_education(self):
        return self.education

    def get_personal_info(self):
        return self.personal

    def get_projects(self):
        return self.projects

    def _normalize_date(self, date_str):
        # Add common date format handling
        date_str = date_str.lower().strip()
        date_str = date_str.replace('present', 'Present')
        return date_str

    def _clean_bullet_point(self, text):
        # Clean up bullet points for better formatting
        text = text.strip()
        if text.startswith('•'):
            text = text[1:].strip()
        return text