from browser_automation.browser_controller import BrowserController
from browser_automation.page_parser import PageParser
from data.user_profile import UserProfile
from data.response_templates import ResponseTemplates
from application_handler.form_filler import FormFiller
from application_handler.application_tracker import ApplicationTracker
from data.resume_parser import ResumeParser
from ai_services.openai_client import CoverLetterGenerator
import sys

def handle_resume_upload(page):
    print("\n📄 Looking for resume upload field...")
    upload_button = page.query_selector('input[type="file"]')
    if upload_button:
        try:
            upload_button.set_input_files('Jordan-Conklin-Software-Engineer-Resume.pdf')
            print("✅ Resume uploaded successfully")
            return True
        except Exception as e:
            print(f"⚠️ Failed to upload resume: {e}")
            return False
    else:
        print("⚠️ Could not find resume upload field")
        return False

def handle_greenhouse_application(page, form_filler, resume_parser):
    print("\nReady to fill application form")
    proceed = input("\nWould you like to proceed with filling the application? (y/n): ").lower()
    
    if proceed != 'y':
        print("Application process cancelled")
        return
    
    print("\nStarting application form fill...")
    
    # Fill basic information
    form_filler.fill_common_fields(page)
    
    # Handle dropdowns
    form_filler.handle_greenhouse_dropdowns(page)
    
    # Handle resume upload
    print("\nUploading resume...")
    upload_button = page.query_selector('#resume')
    if upload_button:
        try:
            upload_button.set_input_files('Jordan-Conklin-Software-Engineer-Resume.pdf')
            print("Resume uploaded successfully")
            # Wait for resume to be processed
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"Failed to upload resume: {e}")
    
    # After filling everything, wait for user confirmation
    print("\n=== Application Review ===")
    print("Please review all filled information before proceeding.")
    print("NOTE: The application will NOT be submitted automatically.")
    
    final_proceed = input("\nWould you like to keep these changes? (y/n): ").lower()
    if final_proceed != 'y':
        print("\nCancelling application - no changes will be submitted")
        return
    
    print("\nApplication filled successfully!")
    print("You can now review and submit the application manually when ready.")

def handle_cover_letter_generation(job_description, company_name, position, resume_parser):
    try:
        generator = CoverLetterGenerator()
        
        # Get resume data
        resume_data = {
            "work_experience": resume_parser.get_work_experience(),
            "skills": resume_parser.get_skills(),
            "education": resume_parser.get_education()
        }
        
        # Generate cover letter
        cover_letter = generator.generate_cover_letter(
            company_name,
            position,
            job_description,
            resume_data
        )
        
        print("\n=== Generated Cover Letter ===")
        print(cover_letter)
        print("="*50)
        
        return cover_letter
        
    except Exception as e:
        print(f"Failed to generate cover letter: {e}")
        return None

def extract_job_description(page):
    """Extract job description from Greenhouse.io page"""
    try:
        # Try different selectors for job description
        description_selectors = [
            'div#content',
            'div[data-test="description"]',
            'div.job-description',
            'div#job_description',
            'div.opening-desc'
        ]
        
        for selector in description_selectors:
            description_element = page.query_selector(selector)
            if description_element:
                description = description_element.text_content().strip()
                if description:
                    return description
        
        # Fallback: try to get all text content from the page
        content = page.query_selector('body').text_content()
        return content
    except Exception as e:
        print(f"Error extracting job description: {e}")
        return None

def main():
    browser = None
    try:
        print("\n=== Job Application Assistant ===")
        
        # Initialize components silently
        user_profile = UserProfile()
        response_templates = ResponseTemplates('config/response_bank.json')
        form_filler = FormFiller(user_profile, response_templates)
        tracker = ApplicationTracker()
        browser = BrowserController()
        resume_parser = ResumeParser()

        # Get job URL
        job_url = input("\nEnter job URL: ")
        
        # Navigate and extract info
        print("\nProcessing job posting...")
        page = browser.new_page()
        page.goto(job_url)
        page.wait_for_load_state('networkidle')
        
        # Extract job details
        company_name = page.query_selector('a.company-name, .company-info h1')
        position = page.query_selector('h1.app-title, .job-title')
        
        company_name = company_name.text_content().strip() if company_name else input("Company name not found. Please enter: ")
        position = position.text_content().strip() if position else input("Position title not found. Please enter: ")
        
        print(f"\nCompany: {company_name}")
        print(f"Position: {position}")
        
        # Extract and verify job description
        job_description = extract_job_description(page)
        if job_description:
            print("\n=== Job Description ===")
            print(job_description)
            print("="*50)
            
            proceed = input("\nIs this the correct job description? (y/n): ").lower()
            if proceed != 'y':
                print("\nPlease paste the correct job description (press Enter twice when done):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                job_description = "\n".join(lines)

        # Generate cover letter
        print("\nGenerating cover letter...")
        cover_letter = handle_cover_letter_generation(
            job_description,
            company_name,
            position,
            resume_parser
        )

        if not cover_letter:
            print("\nUnable to generate cover letter. Options:")
            print("1. Continue without cover letter")
            print("2. Exit application")
            choice = input("Choose option (1-2): ")
            
            if choice != "1":
                print("\nExiting application process")
                return

        elif cover_letter:
            print("\nCover letter options:")
            print("1. Save as PDF")
            print("2. Save as text file")
            print("3. Copy to clipboard")
            print("4. Continue without saving")
            choice = input("Choose option (1-4): ")
            
            if choice == "1":
                from document_generator.pdf_generator import CoverLetterPDF
                pdf_gen = CoverLetterPDF()
                filename = pdf_gen.generate(cover_letter, company_name)
                print(f"Saved as PDF: {filename}")
                
                # Ask if they want to upload the PDF
                upload = input("\nWould you like to upload this cover letter to the application? (y/n): ").lower()
                if upload == 'y':
                    cover_letter_button = page.query_selector('#cover_letter')
                    if cover_letter_button:
                        try:
                            cover_letter_button.set_input_files(filename)
                            print("Cover letter uploaded successfully")
                        except Exception as e:
                            print(f"Failed to upload cover letter: {e}")
            elif choice == "2":
                filename = f"cover_letter_{company_name.lower().replace(' ', '_')}.txt"
                with open(filename, 'w') as f:
                    f.write(cover_letter)
                print(f"Saved as: {filename}")
            elif choice == "3":
                import pyperclip
                pyperclip.copy(cover_letter)
                print("Copied to clipboard")

        # Ask before proceeding with application
        proceed_to_apply = input("\nWould you like to proceed with filling out the application? (y/n): ").lower()
        if proceed_to_apply == 'y':
            print("\nProceeding with application form...")
            handle_greenhouse_application(page, form_filler, resume_parser)
        else:
            print("\nStopping before application form")

    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if browser:
            print("\nClosing browser...")
            browser.close()
            print("Application process complete")
            print("\nReminder: If you proceeded with the application, you'll need to submit it manually.")

if __name__ == "__main__":
    main()