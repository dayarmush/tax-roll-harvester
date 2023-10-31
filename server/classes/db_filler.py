# from config import db
# from models.property import Property

class FillDbRows:

    def __init__(self, property_data):
        self.property_data = property_data

        print(f"town: {self.property_data['town']}, "
                f"parcel_number: {self.property_data['parcel_number']}, "
                f"property_address: {self.property_data['property_address']}, "
                f"market value: {self.property_data['market_value']}, "
                f"owner_one: {self.property_data['owner_one']}, "
                f"owner_two: {self.property_data['owner_two']}, "
                f"owner_address: {self.property_data['owners_address_one']}, "
                f"owner_address2: {self.property_data['owners_address_two']}, "
                f"front: {self.property_data['front_in_feet']}, "
                f"east: {self.property_data['east']}, "
                f"north: {self.property_data['north']}, "
                f"acres: {self.property_data['acres']}, "
                f"property_type: {self.property_data['property_type']}, "
                f"creation_date: {self.property_data['creation_date']} \n"
               )