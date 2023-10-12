import requests
import PyPDF2
from io import BytesIO
import re

text_data = """
STATE OF NEW YORK                          2 0 2 3   F I N A L   A S S E S S M E N T   R O L L                           PAGE      1
COUNTY  - Ulster                                  T A X A B L E  SECTION OF THE ROLL - 1                 VALUATION DATE-JUL 01, 2022
CITY    - KINGSTON                                      TAX MAP NUMBER SEQUENCE                     TAXABLE STATUS DATE-MAR 01, 2023
SWIS    - 510800                                 UNIFORM PERCENT OF VALUE IS 061.00
TAX MAP PARCEL NUMBER          PROPERTY LOCATION & CLASS  ASSESSMENT  EXEMPTION CODE------------------COUNTY--------CITY------SCHOOL
CURRENT OWNERS NAME            SCHOOL DISTRICT               LAND      TAX DESCRIPTION            TAXABLE VALUE
CURRENT OWNERS ADDRESS         PARCEL SIZE/GRID COORD       TOTAL      SPECIAL DISTRICTS                                 ACCOUNT NO.
******************************************************************************************************* 48.16-5-2 ******************
                           495 First Ave                  HOMESTEAD PARCEL                                               068464.000
48.16-5-2                      210 1 Family Res                        COUNTY  TAXABLE VALUE            192,000
Westermann Casey J             KINGSTON CONSOL 510800-99      49,000   CITY    TAXABLE VALUE            192,000
Sass Andrea L                  487-495                       192,000   SCHOOL  TAXABLE VALUE            192,000
495 First Avenue               ACRES    0.75 BANK0180330               LB008 Kingston library            192,000 TO
Kingston, NY 12401             EAST-0634168 NRTH-1133007               LB009 Kingston Libry Debt         192,000 TO
                               DEED BOOK 5908   PG-220
                               FULL MARKET VALUE             314,754
******************************************************************************************************* 48.16-5-3 ******************
                       497-509 First Ave                  HOMESTEAD PARCEL
48.16-5-3                      311 Res vac land                        COUNTY  TAXABLE VALUE             63,000
Westermann Casey J             KINGSTON CONSOL 510800-99      63,000   CITY    TAXABLE VALUE             63,000
Sass Andrea L                  ACRES    1.20 BANK0180330      63,000   SCHOOL  TAXABLE VALUE             63,000
495 First Avenue               EAST-0634233 NRTH-1133127               LB008 Kingston library             63,000 TO
Kingston, NY 12401             DEED BOOK 5908   PG-220                 LB009 Kingston Libry Debt          63,000 TO
                               FULL MARKET VALUE             103,279
******************************************************************************************************* 48.16-5-4 ******************
                           500 First Ave                  HOMESTEAD PARCEL                                               068508.000
48.16-5-4                      210 1 Family Res                        COUNTY  TAXABLE VALUE            333,000
Weiss Ian                      KINGSTON CONSOL 510800-99      72,000   CITY    TAXABLE VALUE            333,000
Medaglia Matthew               511-539                       333,000   SCHOOL  TAXABLE VALUE            333,000
2457 Frederick Douglas BlvdApt ACRES    2.60                           LB008 Kingston library            333,000 TO
New York, NY 10027             EAST-0634350 NRTH-1133307               LB009 Kingston Libry Debt         333,000 TO
                               DEED BOOK 7125   PG-70
                               FULL MARKET VALUE             545,902
******************************************************************************************************* 48.16-5-5 ******************
                       543-575 First Ave                  NON-HOMESTEAD PARCEL                                           068530.000
48.16-5-5                      330 Vacant comm                         COUNTY  TAXABLE VALUE             48,000
Bryant Joseph                  KINGSTON CONSOL 510800-99      48,000   CITY    TAXABLE VALUE             48,000
PO Box 2227                    ACRES    4.20                  48,000   SCHOOL  TAXABLE VALUE             48,000
Kingston, NY 12402             EAST-0634615 NRTH-1133633               LB008 Kingston library             48,000 TO
                               DEED BOOK 4218   PG-326                 LB009 Kingston Libry Debt          48,000 TO
                               FULL MARKET VALUE              78,689
******************************************************************************************************* 48.16-5-9 ******************
                           544 First Ave                  HOMESTEAD PARCEL                                               069674.000
48.16-5-9                      210 1 Family Res                        COUNTY  TAXABLE VALUE            152,000
Ryu Byuong Cory                KINGSTON CONSOL 510800-99      66,000   CITY    TAXABLE VALUE            152,000
544 First Ave                  PARATIAL ASSMT. 2010          152,000   SCHOOL  TAXABLE VALUE            152,000
Kingston, NY 12401             530-544                                 LB008 Kingston library            152,000 TO
                               ACRES    1.60                           LB009 Kingston Libry Debt         152,000 TO
                               EAST-0634764 NRTH-1133283               RT002 Unpaid water                 359.85 MT
                               DEED BOOK 4663   PG-284                 RT040 Unpaid sewer                  21.61 MT
                               FULL MARKET VALUE             249,180
************************************************************************************************************************************
"""

def get_groups(text):

    property_groups = []
    current_group = []
    property_details = {
        'owner_name': '',
        'owner_address': '',
        'property_address': '',
        'property_type': '',
        'full_market_value': '',
        'acres': '',
        'feet': '',
        'east': '',
        'north': ''
    }


    full_market_value = 'FULL MARKET VALUE'
    # acres = 'ACRES'
    feet = 'FRNT'

    east_pattern = r'EAST-(\d{7})'
    north_pattern = r'NRTH-(\d{7})'
    acres = r'ACRES(\s+\d+\.\d+)'
    # front_in_feet = r'FRNT (\d+\.\d+)'
    # depth_in_feet = r''

    # Split the text into lines
    lines = text.split('\n')

    for line in lines:
    # Check if the last item on the line starts with stars
        if line.strip().endswith('****'):
            # If we have collected lines in the current_group, add it to property_groups
            if current_group:
                property_details['property_address'] = current_group[1][0:50].strip()
                property_details['property_type'] = current_group[2][30:50].strip()
            

                property_groups.append(property_details)
                current_group = []
                property_details = {}
    
        # Ulster county acres = [36:45]
        if re.search(acres, line) is not None:
            match = re.search(acres, line)
            property_details['acres'] = match.group(1)

        # front_match = re.search(front_in_feet, line)
        # if  front_match is not None:
        #     property_details['feet'] = front_match

        if full_market_value in line:
            property_details['full_market_value'] = line[50:70].strip()

        if re.search(east_pattern, line) is not None:
            match = re.search(east_pattern, line)
            property_details['east'] = match.group(1)

        if re.search(north_pattern, line) is not None:
            match = re.search(north_pattern, line)
            property_details['north'] = match.group(1)
        
        if feet in line:
            property_details['feet'] = line[25:60].strip()

        # Append the line to the current_group
        current_group.append(line)

    # Add the last property group
    # if current_group:
    #     property_groups.append('\n'.join(current_group))

    # Filter out empty groups
    if property_groups and property_groups[0]:
        property_groups.remove(property_groups[0])
    else:
        pass
    
    # property_groups = [group.strip() for group in property_groups if group.strip()]

    # Print each property group
    for group in property_groups:
        print(f"\n{group}")

# get_groups(text_data)