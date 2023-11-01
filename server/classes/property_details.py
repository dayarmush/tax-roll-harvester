import re
# from models.property import Property 
# from config import db
from data_frame import CreateFrame
class ExtractPropertyDetails():

    extracted_data = {}
    # None is coming from line one being passed down itself
    def __init__(self, property_group, creation_date, town) -> None:
        self.property_group = property_group
        self.creation_date = creation_date
        self.town = town

        market_value = self.get_market_value(self.property_group)
        # depth_in_feet = self.get_depth_in_feet(self.property_group)
        front_in_feet = self.get_front_in_feet(self.property_group)
        east = self.get_east_coordinates(self.property_group)
        north = self.get_north_Coordinates(self.property_group)
        acres = self.get_acres(self.property_group)
        parcel_number = self.get_id(self.property_group)
        property_address = self.get_property_address(self.property_group)
        property_type = self.get_property_type(self.property_group)
        property_desc = self.get_property_desc(self.property_group)
        owner_one = self.get_owner_one_name(self.property_group)
        owner_two = self.get_owner_two_name(self.property_group)
        owners_address_one = self.get_owners_address_one(self.property_group)
        owners_address_two = self.get_owners_address_two(self.property_group)
        

        extracted_data = {
            'town': self.town,
            'creation_date': self.creation_date,
            'market_value': market_value,
            'property_desc': property_desc,
            'front_in_feet': front_in_feet,
            'acres': acres,
            'parcel_number': parcel_number,
            'property_address': property_address,
            'owner_one': owner_one,
            'owner_two': owner_two,
            'owners_address_one': owners_address_one,
            'owners_address_two': owners_address_two
        }

        if 'LLC' in owner_one or 'Inc' in owner_one:
            extracted_data['owned_by'] = 'Business'
        elif 'Trustee' in owner_one:
            extracted_data['owned_by'] = 'Trustee'
        else:
            extracted_data['owned_by'] = 'Personal'

        if east is not None:
            extracted_data['east'] = int(east)
        
        if north is not None:
            extracted_data['north'] = int(north)

        if property_type is not None:
            extracted_data['property_type'] = int(property_type)

        if parcel_number is not None:
            CreateFrame(extracted_data)

    def get_id(self, group):
        if len(group) > 0:
            id_match = re.search(r'\*{2,}([^*]+)\*{2,}', group[0])
            if id_match is not None:
                return id_match.group(1).strip()

    def get_property_address(self, group):
        if len(group) > 1:
            address_match = group[1][:50]
            if address_match is not None:
                return address_match.strip() 

    def get_owner_one_name(self, group):
        owner = ''
        if len(group) > 4:
                owner = group[3][:30].strip()
        return owner.strip()
    
    def get_owner_two_name(self, group):
        owner = ''
        if len(group) > 4:
            if not group[4][0].isnumeric() and group[4][:2] != 'PO':
                owner = group[4][:30].strip()
        return owner.strip()

    def get_owners_address_one(self, group):
        address_one = ''

        if len(group) > 4:
            if group[4][0].isnumeric() or group[4][:2] == 'PO':
                address_one = group[4][:30]
            else:
                address_one = group[5][:30]

        return address_one.strip()
    
    def get_owners_address_two(self, group):
        address_two = ''

        if len(group) > 4:
            if group[4][0].isnumeric() or group[4][:2] == 'PO':
                address_two = group[5][:30]
            else:
                address_two = group[6][:30]

        return address_two.strip()

    def get_property_type(self, group):
        if len(group) > 2:
            type_match = re.search(r'\s(\d{3})\s', group[2])
            if type_match is not None:
                return type_match.group().strip()
            
    def get_property_desc(self, group):
        if len(group) > 2:
            type_match = re.search(r'\s(\d{3})\s(.*?)\s{2,}', group[2])
            if type_match is not None:
                return type_match.group(2).strip()
        
    def get_depth_in_feet(self, group):
        if len(group) > 4:
            search_text = group[4] + group[5]
            depth_match = re.search(r'DPTH(\s+\d+\.\d+)', search_text)
            if depth_match is not None:
                return depth_match.group(1).strip()

    def get_front_in_feet(self, group):
        if len(group) > 4:
            search_area = group[4] + group[5]
            front_match = re.search(r'FRNT(\s+\d+\.\d+)', search_area)
            if front_match is not None:
                return front_match.group(1).strip()

    def get_east_coordinates(self, group):
        if len(group) > 0:
            search_area = ' '.join(group[5:-2])
            east_match = re.search(r'EAST-(\d{7})', search_area)
            if east_match is not None:
                return east_match.group(1).strip()

    def get_north_Coordinates(self, group):
        if len(group) > 0:
            search_area = ' '.join(group[5:-2])
            north_match = re.search(r'NRTH-(\d{7})', search_area)
            if north_match is not None:
                return north_match.group(1).strip()

    def get_acres(self, group):
        if len(group) > 0:
            search_area = ' '.join(group[4:-2])
            acre_match = re.search(r'ACRES(\s+\d+\.\d+)', search_area)
            if acre_match is not None:
                return acre_match.group(1).strip()

    def get_market_value(self, group): 
        if len(group) > 5:
            search_area = ' '.join(group[5:-2])
            market_value_match = re.search(r'FULL\s*MARKET\s+VALUE\s+(\d+\,\d+)', search_area)
            if market_value_match is not None:
                return market_value_match.group(1).strip()