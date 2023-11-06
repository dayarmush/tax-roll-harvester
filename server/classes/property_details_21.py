from property_details import ExtractPropertyDetails

class ExtractPropertyDetailsFrom21:
    def __init__(self, unfiltered_details, creation_date, town):
        self.unfiltered_details = unfiltered_details
        self.creation_date = creation_date
        self.property_group = []
        self.town = town

        results = [i for i in self.unfiltered_details if i]
        joined_property = ''.join(results)

        self.property_group.append(joined_property[:133])
        self.property_group.append(joined_property[133:264])
        self.property_group.append(joined_property[264:396])
        self.property_group.append(joined_property[396:528])
        self.property_group.append(joined_property[528:660])
        self.property_group.append(joined_property[660:792])
        self.property_group.append(joined_property[792:847])
        self.property_group.append(joined_property[847:917])
        self.property_group.append(joined_property[916:])

        ExtractPropertyDetails(self.property_group, self.creation_date, self.town)
