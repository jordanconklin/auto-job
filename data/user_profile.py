import json
from pathlib import Path
import os
from dotenv import load_dotenv

class UserProfile:
    def __init__(self):
        load_dotenv()
        self.profile = self.load_profile_from_env()

    def load_profile_from_env(self):
        return {
            "personal": {
                "first_name": os.getenv("FIRST_NAME"),
                "last_name": os.getenv("LAST_NAME"),
                "email": os.getenv("EMAIL"),
                "phone": os.getenv("PHONE"),
                "location": os.getenv("LOCATION"),
                "linkedin": os.getenv("LINKEDIN"),
                "address": {
                    "street": os.getenv("ADDRESS_STREET"),
                    "city": os.getenv("ADDRESS_CITY"),
                    "state": os.getenv("ADDRESS_STATE"),
                    "zip": os.getenv("ADDRESS_ZIP")
                }
            }
        }

    def get_field(self, category, field=None):
        if field:
            if '.' in field:  # Handle nested fields like 'address.street'
                subcategory, subfield = field.split('.')
                return self.profile.get(category, {}).get(subcategory, {}).get(subfield)
            return self.profile.get(category, {}).get(field)
        return self.profile.get(category)