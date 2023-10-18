import requests
import PyPDF2
import re
import os
from io import BytesIO

pdfs = [
    "https://www.columbiacountyny.com/uploads/1/0/6/8/106827239/ancram_23_fr.pdf",
    "https://greene.sdgnys.com/2023Final/1920Final.pdf",
    "https://ulstercountyny.gov/sites/default/files/documents/KingstonCity-Final-Roll-2023.pdf",
    "https://www.dutchessny.gov/TaxRollsPDF/countytown/2022/amenia23.pdf"
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
                # creation_date = pdf_reader.metadata.creation_date

                # Iterate through each page
                for page_num in range(len(pdf_reader.pages)):
                    print(page_num)
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
            # 'owner_name': '',
            # 'owner_address': '',
            # 'property_address': '',
            # 'property_type': '',
            # 'full_market_value': '',
            # 'acres': '',
            # 'feet': '',
            # 'east': '',
            # 'north': ''
        }

        east_pattern = r'EAST-(\d{7})'
        north_pattern = r'NRTH-(\d{7})'
        acres_pattern = r'ACRES(\s+\d+\.\d+)'
        front_in_feet = r'FRNT(\s+\d+\.\d+)'
        depth_in_feet = r'DPTH(\s+\d+\.\d+)'
        market_value_pattern = r'FULL\s*MARKET\s+VALUE\s+(\d+\,\d+)'
        property_address_pattern = r'\n\s*([^ \n]+)\s+'

        # Split the text into lines
        lines = text.split('\n')

        for line in lines:
            # print(line)
        # Check if the last item on the line starts with stars
            if line.strip().endswith('****'):
                # If we have collected lines in the current_group, add it to property_groups
                if current_group:
                    property_details['property_address'] = current_group[1].strip()
                    property_details['property_type'] = current_group[2][30:50].strip()

                    if current_group[4][0].isnumeric():
                        property_details['owner_name'] = current_group[3][0:25].strip()
                        property_details['owner_address'] = current_group[4][0:30].strip() + ' ' + current_group[5][0:30].strip()
                    else:
                        property_details['owner_name'] = current_group[3][0:25].strip() + ', ' + current_group[4][0:25].strip()
                        property_details['owner_address'] = current_group[5][0:30].strip() + ' ' + current_group[6][0:30].strip()
                

                    property_groups.append(property_details)
                    current_group = []
                    property_details = {}

            acre_match = re.search(acres_pattern, line)
            if acre_match is not None:
                property_details['acres'] = acre_match.group(1).strip()

            front_match = re.search(front_in_feet, line)
            if front_match is not None:
                property_details['front_feet'] = front_match.group(1).strip()
                print(front_match.group())

            depth_match = re.search(depth_in_feet, line)
            if depth_match is not None:
                property_details['depth_feet'] = depth_match.group(1).strip()

            market_value_match = re.search(market_value_pattern, line)
            if market_value_match is not None:
                property_details['full_market_value'] = market_value_match.group(1).strip()

            east_match = re.search(east_pattern, line)
            if east_match is not None:
                property_details['east'] = east_match.group(1)

            north_match = re.search(north_pattern, line)
            if north_match is not None:
                property_details['north'] = north_match.group(1)

            if len(current_group) > 1:
                property_address_match = re.search(property_address_pattern, current_group[1])
                
                if property_address_match is not None:
                    print(current_group[1])
                    property_details['property_address'] = property_address_match.group().strip()

            # Append the line to the current_group
            current_group.append(line)

        # Add the last property group
        # if current_group:
        #     property_groups.append('\n'.join(current_group))

        # Delete first group
        if property_groups and property_groups[0]:
            property_groups.remove(property_groups[0])
        else:
            pass

        # Print each property group
        for group in property_groups:
            print(f"\n{group}")

PdfFormatter(pdfs)
