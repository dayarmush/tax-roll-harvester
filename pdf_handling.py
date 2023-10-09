import requests
import PyPDF2
import re
import os
from io import BytesIO
from test import get_groups

pdfs = [
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

        # Split the text into lines
        lines = text.split('\n')

        for line in lines:
        # Check if the last item on the line starts with stars
            if line.strip().endswith('****'):
                # If we have collected lines in the current_group, add it to property_groups
                if current_group:
                    property_groups.append('\n'.join(current_group))
                    current_group = []
            
            # Append the line to the current_group
            current_group.append(line)
        # Remove the first group which is non needed 
        property_groups.remove(property_groups[0])

        # Filter out empty groups may not be necessary 
        property_groups = [group.strip() for group in property_groups if group.strip()]

        # Print each property group
        for index, group in enumerate(property_groups, start=1):
            print(f"Property {index}:\n{group}\n\n\n")


PdfFormatter(pdfs)
