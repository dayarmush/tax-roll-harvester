import requests
import PyPDF2
import re
import os
from io import BytesIO

pdfs = ["https://ulstercountyny.gov/sites/default/files/documents/KingstonCity-Final-Roll-2023.pdf"]

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
                # send to another method that calls groups
                for page_num in range(len(pdf_reader.pages)):
                    
                    # Get a page
                    if page_num < 11:
                        page = pdf_reader.pages[page_num]
                        # Extract text from the page
                        text = page.extract_text()
                        # Send pdf page down to Extract the property groups 
                        # should only go to the next page once the current page finishes processing
                        ExtractPropertyGroups(text)
                        print(page_num)
            except requests.exceptions.HTTPError as e:
                print(f"Error: {str(e)}")

# Class to extract property groups from given text
class ExtractPropertyGroups():

    def __init__(self, pdf_page):
        self.pdf_page = pdf_page

        current_group = ''

        # Split the text into lines
        lines = pdf_page.split('\n')

        for line in lines:
        # Check if the last item on the line starts with stars
        # Send to another class property data processor
            if line.strip().endswith('****'):
                    # print(current_group + "\n")
                    ExtractPropertyDetails(current_group)
                    current_group = ''
            # Append the line to the current_group
            current_group = current_group + line + ' '

# Extract property details from given groups
class ExtractPropertyDetails():

    extracted_data = {}

    def __init__(self, property_group) -> None:
        self.property_group = property_group

        # print(self.get_market_value(self.property_group))
        # print(self.get_depth_in_feet(self.property_group))
        # print(self.get_front_in_feet(self.property_group))
        # print(self.get_east_coordinates(self.property_group))
        # print(self.get_north_Coordinates(self.property_group))
        # print(self.get_acres(self.property_group))

    def get_id(self, group):
        pass

    def get_property_address(self, group):
        pass

    def get_owners_name(self, group):
        pass

    def get_owners_address(self, group):
        pass

    def get_property_type(self, group):
        pass

    def get_depth_in_feet(self, group):
        depth_match = re.search(r'DPTH(\s+\d+\.\d+)', group)
        if depth_match is not None:
            return depth_match.group(1).strip()

    def get_front_in_feet(self, group):
        front_match = re.search(r'FRNT(\s+\d+\.\d+)', group)
        if front_match is not None:
           return front_match.group(1).strip()

    def get_east_coordinates(self, group):
        east_match = re.search(r'EAST-(\d{7})', group)
        if east_match is not None:
            return east_match.group(1)

    def get_north_Coordinates(self, group):
        north_match = re.search(r'NRTH-(\d{7})', group)
        if north_match is not None:
            return north_match.group(1)

    def get_acres(self, group):
        acre_match = re.search(r'ACRES(\s+\d+\.\d+)', group)
        if acre_match is not None:
            return acre_match.group(1).strip()

    def get_market_value(self, group):
        market_value_match = re.search(r'FULL\s*MARKET\s+VALUE\s+(\d+\,\d+)', group)
        if market_value_match is not None:
           return market_value_match.group(1).strip()


    





# extract property details 
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

    property_address_pattern = r'\n\s*([^ \n]+)\s+'

    # Split the text into lines
    lines = text.split('\n')

    for line in lines:
        # print(line)
    # Check if the last item on the line starts with stars
    # Send to another class property data processor
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

PdfDataExtractor(pdfs)
