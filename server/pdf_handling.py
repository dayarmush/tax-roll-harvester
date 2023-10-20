import requests
import PyPDF2
import re
from io import BytesIO

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
            except requests.exceptions.HTTPError as e:
                print(f"Error: {str(e)}")

# Class to extract property groups from given text
class ExtractPropertyGroups():

    def __init__(self, pdf_page):
        self.pdf_page = pdf_page

        current_group = []

        # Split the text into lines
        lines = pdf_page.split('\n')
        # First 7 lines are not needed 
        for i in range(7, len(lines)):
        # Check if the last item on the line starts with stars
        # Send to another class property data processor
            if lines[i].strip().endswith('****'):
                    # print(current_group)
                    ExtractPropertyDetails(current_group)
                    current_group = []
            # Append the line to the current_group
            current_group.append(lines[i])

# Extract property details from given groups
class ExtractPropertyDetails():

    extracted_data = {}
    # None is coming from line one being passed down itself
    def __init__(self, property_group) -> None:
        self.property_group = property_group

        # print(self.get_market_value(self.property_group))
        # print(self.get_depth_in_feet(self.property_group))
        # print(self.get_front_in_feet(self.property_group))
        # print(self.get_east_coordinates(self.property_group))
        # print(self.get_north_Coordinates(self.property_group))
        # print(self.get_acres(self.property_group))
        # print(self.get_id(self.property_group))
        # print(self.get_property_address(self.property_group))
        # print(self.get_property_type(self.property_group))
        print(self.get_owners_name(self.property_group))

    def get_id(self, group):
        if len(group) > 0:
            id_match = re.search(r'\*{2,}([^*]+)\*{2,}', group[0])
            if id_match is not None:
                return id_match.group(1).strip()

    def get_property_address(self, group):
        if len(group) > 0:
            address_match = group[1][:50]
            if address_match is not None:
                return address_match.strip() 
    # use NLP https://unbiased-coder.com/extract-names-python-nltk/
    def get_owners_name(self, group):
        if len(group) > 0:
            search_area = group[3] + group[4]
            owners_line = re.search(r'^[A-Za-z\s]+$', search_area)
            if owners_line is not None:
                return owners_line.group()

    def get_owners_address(self, group):
        pass

    def get_property_type(self, group):
        if len(group) > 0:
            type_match = re.search(r'\s(\d{3})\s', group[2])
            if type_match is not None:
                return type_match.group().strip()
        
    def get_depth_in_feet(self, group):
        if len(group) > 0:
            search_text = group[4] + group[5]
            depth_match = re.search(r'DPTH(\s+\d+\.\d+)', search_text)
            if depth_match is not None:
                return depth_match.group(1).strip()

    def get_front_in_feet(self, group):
        if len(group) > 0:
            search_area = group[4] + group[5]
            front_match = re.search(r'FRNT(\s+\d+\.\d+)', search_area)
            if front_match is not None:
                return front_match.group(1).strip()

    def get_east_coordinates(self, group):
        if len(group) > 0:
            search_area = ' '.join(group[5:-2])
            east_match = re.search(r'EAST-(\d{7})', search_area)
            if east_match is not None:
                return east_match.group(1) 

    def get_north_Coordinates(self, group):
        if len(group) > 0:
            search_area = ' '.join(group[5:-2])
            north_match = re.search(r'NRTH-(\d{7})', search_area)
            if north_match is not None:
                return north_match.group(1)

    def get_acres(self, group):
        if len(group) > 0:
            search_area = ' '.join(group[4:-2])
            acre_match = re.search(r'ACRES(\s+\d+\.\d+)', search_area)
            if acre_match is not None:
                return acre_match.group(1).strip()

    def get_market_value(self, group): 
        if len(group) > 0:
            line = len(group)-1
            market_value_match = re.search(r'FULL\s*MARKET\s+VALUE\s+(\d+\,\d+)', group[line])
            if market_value_match is not None:
                return market_value_match.group(1).strip()


    




# def get_groups(self, text):

#     property_address_pattern = r'\n\s*([^ \n]+)\s+'
#     lines = text.split('\n')
#     for line in lines:
#         if line.strip().endswith('****'):
#             if current_group:
#                 property_details['property_address'] = current_group[1].strip()
#                 property_details['property_type'] = current_group[2][30:50].strip()

#                 if current_group[4][0].isnumeric():
#                     property_details['owner_name'] = current_group[3][0:25].strip()
#                     property_details['owner_address'] = current_group[4][0:30].strip() + ' ' + current_group[5][0:30].strip()
#                 else:
#                     property_details['owner_name'] = current_group[3][0:25].strip() + ', ' + current_group[4][0:25].strip()
#                     property_details['owner_address'] = current_group[5][0:30].strip() + ' ' + current_group[6][0:30].strip()

PdfDataExtractor(pdf)
