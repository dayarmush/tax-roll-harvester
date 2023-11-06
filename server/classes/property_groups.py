from property_details import ExtractPropertyDetails
from property_details_21 import ExtractPropertyDetailsFrom21

# Class to extract property groups from given text
class ExtractPropertyGroups():

    def __init__(self, pdf_page, creation_date, town=None):
        self.pdf_page = pdf_page

        current_group = []
        # print(self.pdf_page)
        # Split the text into lines
        lines = pdf_page.split('\n')
        # First 7 lines are not needed 
        for i in range(7, len(lines)):
        # Check if the last item on the line starts with stars
        # Send to another class property data processor
            if lines[i].strip().endswith('****'):
                    # print((current_group))
                    # ExtractPropertyDetails(current_group, creation_date, town)
                    ExtractPropertyDetailsFrom21(current_group, creation_date, town)
                    current_group = []
            # Append the line to the current_group
            current_group.append(lines[i])
