import json
from datetime import datetime
from pathlib import Path

class ApplicationTracker:
    def __init__(self, tracker_file="applications.json"):
        self.tracker_file = Path(tracker_file)
        self.applications = self.load_applications()

    def load_applications(self):
        if self.tracker_file.exists():
            with open(self.tracker_file, 'r') as f:
                return json.load(f)
        return []

    def add_application(self, job_url, company, position):
        application = {
            'job_url': job_url,
            'company': company,
            'position': position,
            'date_applied': datetime.now().isoformat(),
            'status': 'applied'
        }
        self.applications.append(application)
        self._save_applications()

    def update_status(self, job_url, new_status):
        for app in self.applications:
            if app['job_url'] == job_url:
                app['status'] = new_status
                app['last_updated'] = datetime.now().isoformat()
        self._save_applications()

    def _save_applications(self):
        with open(self.tracker_file, 'w') as f:
            json.dump(self.applications, f, indent=4)