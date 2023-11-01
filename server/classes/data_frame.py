import pandas as pd

class CreateFrame:
    def __init__(self, property_data):
        self.property_data = property_data
        self.file_path = 'property_data.csv'
        
        # Check if the CSV file already exists, and load it if it does
        try:
            self.data = pd.read_csv(self.file_path)
        except FileNotFoundError:
            # Create an empty DataFrame if the file doesn't exist
            columns=['town', 'parcel_number', 'property_address', 'market_value',
                        'owner_one', 'owner_two', 'owners_address_one', 'owners_address_two',
                        'front_in_feet', 'east', 'north', 'acres', 'property_type', 
                        'property_desc', 'creation_date']
            self.data = pd.DataFrame(columns=columns)

        # Add the current property data to the DataFrame
        self.add_property_data()

        # Save the DataFrame to the CSV file
        self.save_to_csv()

    def add_property_data(self):
        # Add a row of property data to the DataFrame
        self.data = self.data._append(self.property_data, ignore_index=True)

    def save_to_csv(self):
        # Save the DataFrame to a CSV file
        self.data.to_csv(self.file_path, index=False)







#         print(f"town: {self.property_data['town']}, "
#                 f"parcel_number: {self.property_data['parcel_number']}, "
#                 f"property_address: {self.property_data['property_address']}, "
#                 f"market value: {self.property_data['market_value']}, "
#                 f"owner_one: {self.property_data['owner_one']}, "
#                 f"owner_two: {self.property_data['owner_two']}, "
#                 f"owner_address: {self.property_data['owners_address_one']}, "
#                 f"owner_address2: {self.property_data['owners_address_two']}, "
#                 f"front: {self.property_data['front_in_feet']}, "
#                 f"east: {self.property_data['east']}, "
#                 f"north: {self.property_data['north']}, "
#                 f"acres: {self.property_data['acres']}, "
#                 f"property_type: {self.property_data['property_type']}, "
#                 f"creation_date: {self.property_data['creation_date']} \n"
#                )