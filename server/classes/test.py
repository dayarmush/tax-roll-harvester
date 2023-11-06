import pandas as pd

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

import requests
import PyPDF2
from io import BytesIO
from property_details_21 import ExtractPropertyDetailsFrom21


pdfs = ['https://www.dutchessny.gov/TaxRollsPDF/countytown/2022/rhinebeck23.pdf',
        'https://www.dutchessny.gov/TaxRollsPDF/countytown/2022/redhook23.pdf',
        'https://www.dutchessny.gov/TaxRollsPDF/countytown/2022/milan23.pdf']

pdfs2020 = [
    'https://www.dutchessny.gov/TaxRollsPDF/countytown/2020/rhinebeck21.pdf',
    # 'https://www.dutchessny.gov/TaxRollsPDF/countytown/2020/milan21.pdf'
    # 'https://www.dutchessny.gov/TaxRollsPDF/countytown/2020/redhook21.pdf'
]

# Extractor 
class TestPdfDataExtractor():

    def __init__(self, pdf_links):
        self.pdf_links = pdf_links

        for link in self.pdf_links:
            response = requests.get(link)
            try:
                response.raise_for_status()
                pdf_file = BytesIO(response.content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                creation_date = str(pdf_reader.metadata.creation_date)[:10]
                print(pdf_reader.metadata)
                # town = re.search(r'\d{4} (?:Town(?:\sand\sVillage)? of )?(.+?) Tax Roll', pdf_reader.metadata.subject).group(1)
                town = pdf_reader.metadata.title.split(' ')


                # Get a page
                page = pdf_reader.pages[325]
                # Extract text from the page
                text = page.extract_text()
                # Send pdf page down to Extract the property groups 
                TestExtractPropertyGroups(text, creation_date, town[1])

            except requests.exceptions.HTTPError as e:
                print(f"Error: {str(e)}")


class TestExtractPropertyGroups():

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

        print(self.property_group)


TestPdfDataExtractor(pdfs2020)