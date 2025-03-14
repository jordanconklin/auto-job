from openai import OpenAI
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader

class CoverLetterGenerator:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found in .env file. Please add OPENAI_API_KEY to your .env file.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"
    
    def handle_api_error(self, e):
        """Handle common OpenAI API errors with clear messages"""
        error_msg = str(e)
        if "insufficient_quota" in error_msg:
            print("\nError: OpenAI API quota exceeded.")
            print("Please visit https://platform.openai.com/account/billing to:")
            print("1. Set up billing if you haven't already")
            print("2. Add credits to your account")
            print("3. Check your usage and limits")
        elif "invalid_api_key" in error_msg:
            print("\nError: Invalid OpenAI API key.")
            print("Please check your OPENAI_API_KEY environment variable.")
        else:
            print(f"\nOpenAI API Error: {e}")
    
    def parse_job_description(self, job_description):
        """Extract key information from job description"""
        prompt = f"""
        Please analyze this job description and extract:
        1. Key technical requirements
        2. Main responsibilities
        3. Company values/mission
        4. Team/culture aspects

        Job Description:
        {job_description}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,  # Using the default model
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error parsing job description: {e}")
            return None

    def generate_cover_letter(self, company_name, position, job_description, resume_data):
        try:
            print("Connecting to OpenAI...")
            
            # Read the template content to use as example
            with open("Aurora-cover-letter.pdf", 'rb') as template:
                template_text = PdfReader(template).pages[0].extract_text()
            
            prompt = f"""
            Create a cover letter following the EXACT format of this template, keep it concise and only replacing the company-specific content while keeping the same paragraph structure, length, and flow:

            {template_text}

            Generate a version for {company_name} for the {position} position, using this job description:
            {job_description}

            Important guidelines:
            1. Keep EXACTLY the same paragraph structure as the template
            2. Maintain the same sentence patterns and flow
            3. Only change the company name, position, and technical details
            4. Keep the same length for each paragraph
            5. Use the same greeting and closing format
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
            
        except Exception as e:
            self.handle_api_error(e)
            return None