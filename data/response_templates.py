import json
from pathlib import Path

class ResponseTemplates:
    def __init__(self, template_path):
        self.template_path = Path(template_path)
        self.templates = self.load_templates()

    def load_templates(self):
        try:
            with open(self.template_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading templates: {e}")
            return {}

    def get_response(self, key):
        return self.templates.get(key, '')

    def customize_response(self, key, replacements):
        response = self.get_response(key)
        for old, new in replacements.items():
            response = response.replace(f"[{old}]", new)
        return response