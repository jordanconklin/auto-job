from flask import Flask, render_template, request, jsonify
from browser_automation.browser_controller import BrowserController
from data.user_profile import UserProfile
from data.response_templates import ResponseTemplates
from application_handler.form_filler import FormFiller
from data.resume_parser import ResumeParser
from ai_services.openai_client import CoverLetterGenerator

app = Flask(__name__)

def process_application(job_url):
    browser = None
    try:
        # Initialize components
        user_profile = UserProfile()
        browser = BrowserController()
        resume_parser = ResumeParser()
        
        # Navigate to job page
        page = browser.new_page()
        page.goto(job_url)
        page.wait_for_load_state('networkidle')
        
        # Extract job details with better selectors
        company_selectors = [
            'a.company-name',
            '.company-info h1',
            'div.company-name',
            'div[data-test="company-name"]',
            '.posting-header h1'
        ]
        
        position_selectors = [
            'h1.app-title',
            '.job-title',
            'div.posting-headline h2',
            'div[data-test="job-title"]'
        ]
        
        # Try multiple selectors for company name
        company_name = None
        for selector in company_selectors:
            element = page.query_selector(selector)
            if element:
                company_name = element.text_content().strip()
                if company_name:
                    break
                    
        # Try multiple selectors for position
        position = None
        for selector in position_selectors:
            element = page.query_selector(selector)
            if element:
                position = element.text_content().strip()
                if position:
                    break
        
        # Extract job description with better selectors
        description_selectors = [
            'div#content',
            'div.job-description',
            'div#job_description',
            'div.description',
            'div[data-test="job-description"]'
        ]
        
        job_description = ""
        for selector in description_selectors:
            element = page.query_selector(selector)
            if element:
                job_description = element.text_content().strip()
                if job_description:
                    break
        
        if not company_name or not position or not job_description:
            print("Failed to extract some job details automatically")
            if not company_name:
                company_name = input("Company name not found. Please enter: ")
            if not position:
                position = input("Position title not found. Please enter: ")
            if not job_description:
                print("\nPlease paste the job description (press Enter twice when done):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                job_description = "\n".join(lines)
        
        # Generate cover letter
        generator = CoverLetterGenerator()
        cover_letter = generator.generate_cover_letter(
            company_name,
            position,
            job_description,
            resume_parser.get_work_experience()
        )
        
        return {
            'success': True,
            'cover_letter': cover_letter,
            'company': company_name,
            'position': position
        }
        
    except Exception as e:
        raise Exception(f"Error processing application: {str(e)}")
    finally:
        if browser:
            browser.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply', methods=['POST'])
def apply():
    job_url = request.json.get('job_url')
    if not job_url:
        return jsonify({'success': False, 'error': 'No URL provided'})
    
    try:
        result = process_application(job_url)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 