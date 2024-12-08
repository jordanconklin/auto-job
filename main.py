from browser_automation.browser_controller import BrowserController
from browser_automation.page_parser import PageParser
from data.user_profile import UserProfile
from data.response_templates import ResponseTemplates
from application_handler.form_filler import FormFiller
from application_handler.application_tracker import ApplicationTracker

def main():
    # Initialize components
    print("\n=== Initializing Job Application Assistant ===")
    user_profile = UserProfile('config/user_info.json')
    response_templates = ResponseTemplates('config/response_bank.json')
    form_filler = FormFiller(user_profile, response_templates)
    tracker = ApplicationTracker()
    browser = BrowserController()

    try:
        # Get job URL from user
        job_url = input("\nEnter job application URL: ")
        
        # Start browser and navigate to page
        print("\n🌐 Opening browser...")
        browser.start_browser()
        page = browser.navigate_to(job_url)
        
        if not page:
            raise Exception("Failed to load page")

        # Wait for manual login
        print("\n👋 Please log in manually in the browser window")
        input("Press Enter once you've logged in and are on the application page...")
        
        # Parse page and fill forms
        print("\n🔍 Analyzing application form...")
        parser = PageParser(page)
        
        print("\n📝 Filling common fields (name, email, phone)...")
        form_filler.fill_common_fields(page)
        print("✅ Basic information filled")

        # Handle free response questions
        print("\n📋 Looking for free response questions...")
        free_responses = parser.detect_free_response_questions()
        
        if free_responses:
            print(f"Found {len(free_responses)} free response questions")
            for question in free_responses:
                print(f"\n❓ Question found: {question['question']}")
                default_response = response_templates.get_response(
                    question['question'].lower().replace(' ', '_'))
                
                print(f"📎 Default response available: {default_response[:50]}...")
                use_default = input("Use default response? (y/n): ").lower() == 'y'
                
                response = default_response if use_default else input("Enter your response: ")
                if form_filler.fill_free_response(question['element'], response):
                    print("✅ Response filled successfully")
                else:
                    print("⚠️ Failed to fill response")
        else:
            print("No free response questions found")

        # Track application
        print("\n📊 Tracking application...")
        company = input("Enter company name: ")
        position = input("Enter position title: ")
        tracker.add_application(job_url, company, position)
        print("✅ Application tracked successfully")

        print("\n⚠️ Please review the application before submitting!")
        submit = input("Should I submit the application? (y/n): ").lower() == 'y'
        
        if submit:
            print("\n🚀 Looking for submit button...")
            # Add submit button logic here
            print("Please click the submit button manually for now")
        
        input("\nPress Enter to close the browser...")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
    finally:
        print("\n👋 Closing browser...")
        browser.close()
        print("Done! Check applications.json for your application history")

if __name__ == "__main__":
    main()