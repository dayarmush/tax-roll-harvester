import requests
import PyPDF2
from io import BytesIO
import datetime
import re
from property_groups import ExtractPropertyGroups
pdfs = ['https://www.dutchessny.gov/TaxRollsPDF/countytown/2022/rhinebeck23.pdf']
        # 'https://www.dutchessny.gov/TaxRollsPDF/countytown/2022/redhook23.pdf'
        # 'https://www.dutchessny.gov/TaxRollsPDF/countytown/2022/milan23.pdf']

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
                creation_date = str(pdf_reader.metadata.creation_date)[:10]
                town = re.search(r'\d{4} (?:Town(?:\sand\sVillage)? of )?(.+?) Tax Roll', pdf_reader.metadata.subject).group(1)

                # Iterate through each page
                for page_num in range(len(pdf_reader.pages)):
                    
                    # Get a page
                    if page_num < 2:
                        page = pdf_reader.pages[page_num]
                        # Extract text from the page
                        text = page.extract_text()
                        # Send pdf page down to Extract the property groups 
                        ExtractPropertyGroups(text, creation_date, town)
                        print(page_num)
                    else:
                        break
            except requests.exceptions.HTTPError as e:
                print(f"Error: {str(e)}")

PdfDataExtractor(pdfs)
