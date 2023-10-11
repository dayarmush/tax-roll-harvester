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
        'full_market_value': ''
    }

    # Split the text into lines
    lines = text.split('\n')
    # Define the regular expression pattern
    # pattern = r'FULL MARKET VALUE\s+([\d,]+)'

    for line in lines:
    # Check if the last item on the line starts with stars
        if line.strip().endswith('****'):
            # If we have collected lines in the current_group, add it to property_groups
            if current_group:
                property_details['property_address'] = current_group[1][20:50].strip()
                property_details['property_type'] = current_group[2][32:35]

                if len(current_group) == 10:
                    if 'U' in current_group[9][32:34]:
                        property_details['full_market_value'] = current_group[9][50:70].strip()
                
                elif len(current_group) == 9:
                    if 'U' in current_group[8][32:34]:
                        property_details['full_market_value'] = current_group[8][50:70].strip()

                elif len(current_group) == 8:
                    if 'U' in current_group[7][32:34]:
                        property_details['full_market_value'] = current_group[7][50:70].strip()

                else:
                    property_details['full_market_value'] = 'waste of space!!!!!!'

                if current_group[4][0].isnumeric():
                    property_details['owner_name'] = current_group[3][0:30].strip()
                    property_details['owner_address'] = current_group[4][0:30].strip() + ' ' + current_group[5][0:30].strip()
                else:
                    property_details['owner_name'] = current_group[3][0:30].strip() + ', ' + current_group[4][0:30].strip()
                    property_details['owner_address'] = current_group[5][0:30].strip() + ' ' + current_group[6][0:30].strip()

                # if line[32:3] == 'FULL':
                #     property_details['full_market_value'] = line[32:80].strip()

                property_groups.append(property_details)
                current_group = []
                property_details = {}
        
        # Append the line to the current_group
        current_group.append(line)

    # Add the last property group
    # if current_group:
    #     property_groups.append('\n'.join(current_group))

    # Filter out empty groups
    # if len(property_groups[0]) > 0:
    #     property_groups.remove(property_groups[0])
    
    # property_groups = [group.strip() for group in property_groups if group.strip()]

    # Print each property group
    for group in property_groups:
        print(f"\n{group}")


# get_groups(text_data)