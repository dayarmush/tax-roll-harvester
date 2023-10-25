import requests
import PyPDF2
from io import BytesIO
from classes.property_groups import ExtractPropertyGroups
pdf = ["https://ulstercountyny.gov/sites/default/files/documents/KingstonCity-Final-Roll-2023.pdf"]

# Extractor 
class PdfDataExtractor():

    def __init__(self, pdf_links):
        self.pdf_links = pdf_links

        for link in self.pdf_links:
            response = requests.get(link)
            try:
                response.raise_for_status()
                pdf_file = BytesIO(response.content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                # creation_date = pdf_reader.metadata.creation_date

                # Iterate through each page
                for page_num in range(len(pdf_reader.pages)):
                    
                    # Get a page
                    if page_num < 11:
                        page = pdf_reader.pages[page_num]
                        # Extract text from the page
                        text = page.extract_text()
                        # Send pdf page down to Extract the property groups 
                        ExtractPropertyGroups(text)
                        print(page_num)
                    else:
                        break
            except requests.exceptions.HTTPError as e:
                print(f"Error: {str(e)}")

# PdfDataExtractor(pdf)
