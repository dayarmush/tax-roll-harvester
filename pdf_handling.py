import requests
import PyPDF2
import re
import os
from io import BytesIO

pdfs = [
    "https://ulstercountyny.gov/sites/default/files/documents/KingstonCity-Final-Roll-2023.pdf",
    "https://www.dutchessny.gov/TaxRollsPDF/countytown/2022/amenia23.pdf",
    "https://ulstercountyny.gov/sites/default/files/documents/Denning-Final-Roll-2023.pdf"
    ]


class PdfFormatter():

    def __init__(self, pdf_links):
        self.pdf_links = pdf_links

        for link in self.pdf_links:
            response = requests.get(link)
            try:
                response.raise_for_status()
                pdf_file = BytesIO(response.content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)

                # Iterate through each page
                for page_num in range(len(pdf_reader.pages)):
                    # Get a page
                    page = pdf_reader.pages[page_num]
                    # Extract text from the page
                    text = page.extract_text()

                    self.get_groups(text)
            except requests.exceptions.HTTPError as e:
                print(f"Error: {str(e)}")

    def get_groups(self, text):

        property_groups = []
        current_group = []
        property_details = {
            'owner_name': '',
            'owner_address': '',
            'property_address': '',
            'property_type': '',
            'full_market_value': ''
        }

        # Split the text into lines
        lines = text.split('\n')

        for line in lines:
        # Check if the last item on the line starts with stars
            if line.strip().endswith('****'):
                # If we have collected lines in the current_group, add it to property_groups
                if current_group:
                    property_details['property_address'] = current_group[1][20:50].strip()
                    property_details['property_type'] = current_group[2][32:35]

                    if len(current_group) == 10:
                        if 'U' in current_group[9][32:34]:
                            property_details['full_market_value'] = current_group[9][50:70].strip()
                    
                    elif len(current_group) == 9:
                        if 'U' in current_group[8][32:34]:
                            property_details['full_market_value'] = current_group[8][50:70].strip()

                    elif len(current_group) == 8:
                        if 'U' in current_group[7][32:34]:
                            property_details['full_market_value'] = current_group[7][50:70].strip()

                    else:
                        property_details['full_market_value'] = 'waste of space!!!!!!'

                    if current_group[4][0].isnumeric():
                        property_details['owner_name'] = current_group[3][0:30].strip()
                        property_details['owner_address'] = current_group[4][0:30].strip() + ' ' + current_group[5][0:30].strip()
                    else:
                        property_details['owner_name'] = current_group[3][0:30].strip() + ', ' + current_group[4][0:30].strip()
                        property_details['owner_address'] = current_group[5][0:30].strip() + ' ' + current_group[6][0:30].strip()

                    property_groups.append(property_details)
                    current_group = []
                    property_details = {}
            
            # Append the line to the current_group
            current_group.append(line)

        # Filter out empty groups
        if property_groups:
            property_groups.remove(property_groups[0])

        # Print each property group
        for group in property_groups:
            print(f"\n{group}")

PdfFormatter(pdfs)
