
import json
from pathlib import Path

class UserProfile:
    def __init__(self, profile_path):
        self.profile_path = Path(profile_path)
        self.profile = self.load_profile()

    def load_profile(self):
        try:
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading profile: {e}")
            return {}

    def get_field(self, category, field=None):
        if field:
            return self.profile.get(category, {}).get(field)
        return self.profile.get(category)

    def update_field(self, category, field, value):
        if category not in self.profile:
            self.profile[category] = {}
        self.profile[category][field] = value
        self._save_profile()

    def _save_profile(self):
        with open(self.profile_path, 'w') as f:
            json.dump(self.profile, f, indent=4)