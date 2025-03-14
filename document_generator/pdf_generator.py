from PyPDF2 import PdfReader, PdfWriter
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

class CoverLetterPDF:
    def __init__(self):
        self.template_path = "Aurora-cover-letter.pdf"
        
    def generate(self, cover_letter_text, company_name):
        try:
            # Create new filename based on company
            new_filename = f"cover_letter_{company_name.lower().replace(' ', '_')}.pdf"
            
            # Read the template PDF
            reader = PdfReader(self.template_path)
            writer = PdfWriter()
            
            # Get the first page
            page = reader.pages[0]
            
            # Create a new PDF with the text content
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            
            # Split the cover letter into components
            parts = cover_letter_text.split('\n')
            
            # Set font and sizes to match template
            can.setFont("Times-Roman", 12)
            
            # Add text at the same positions as template
            y_position = 650  # Starting Y position (adjust based on template)
            
            for part in parts:
                if part.strip():
                    if part.startswith('Dear'):
                        y_position = 650  # Position for greeting
                    elif 'Best regards' in part:
                        y_position = 300  # Position for signature
                    elif 'Jordan Conklin' in part:
                        y_position = 270  # Position for name
                    else:
                        # Regular paragraph text
                        words = part.split()
                        line = ''
                        for word in words:
                            if len(line + ' ' + word) < 80:  # Character limit per line
                                line = line + ' ' + word if line else word
                            else:
                                can.drawString(72, y_position, line)
                                y_position -= 15
                                line = word
                        if line:
                            can.drawString(72, y_position, line)
                            y_position -= 30  # Space between paragraphs
            
            can.save()
            
            # Move to the beginning of the StringIO buffer
            packet.seek(0)
            new_pdf = PdfReader(packet)
            
            # Merge the template with new content
            page.merge_page(new_pdf.pages[0])
            writer.add_page(page)
            
            # Save the new PDF
            with open(new_filename, 'wb') as output_file:
                writer.write(output_file)
            
            return new_filename
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None 