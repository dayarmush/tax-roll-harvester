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
            columns = ['town', 'parcel_number', 'property_address', 'market_value',
                       'owner_one', 'owner_two', 'owners_address_one', 'owners_address_two',
                       'front_in_feet', 'east', 'north', 'acres', 'property_type', 
                       'property_desc', 'creation_date']
            self.data = pd.DataFrame(columns=columns)

        # Check if current owner is the same as the one in the existing record
        self.check_current_owner()

    def add_property_data(self):
        # Append the current property data to the DataFrame
        # Ensure self.property_data is a DataFrame with one row or a Series
        if not isinstance(self.property_data, pd.DataFrame):
            self.property_data = pd.DataFrame([self.property_data])
        self.data = pd.concat([self.data, self.property_data], ignore_index=True)

    def save_to_csv(self):
        # Save the DataFrame to a CSV file
        self.data.to_csv(self.file_path, index=False)

    def check_current_owner(self):
        # Find rows with the same 'parcel_number'
        matching_row = self.data[self.data['parcel_number'] == self.property_data['parcel_number']]

        if not matching_row.empty:
            # Check if 'owner_one' is the same in the existing record
            current_owner = matching_row.iloc[0]['owner_one']
            owner_2020 = self.property_data['owner_one']
            # print(self.property_data)
            # print(f"current: {current_owner}, 2020: {owner_2020}")
            if current_owner == owner_2020:
                print(f"Property with parcel_number {self.property_data['parcel_number']} already exists with the same owner.")
                # Add or update the 'year' column for the matching rows to 2020
                self.data.loc[self.data['parcel_number'] == self.property_data['parcel_number'], 'year'] = 2020
                self.save_to_csv()
            else:
                print(f"Property with parcel_number {self.property_data['parcel_number']} already exists but with a different owner")
                # No further action needed, proceed without adding the 'year'
        # else:
            # No existing row with the same 'parcel_number', add new property data without the 'year' column
            # self.add_property_data()
            # self.save_to_csv()




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