from bs4 import BeautifulSoup
import requests
import re

class ScrapeSite():

    def __init__(self, url, links=[]):
        self.url = url
        self.links = links

    # Method to grab the HTML of the website
    def get_request(self):
        # Send the request
        site = requests.get(self.url)
        if site.status_code == 200:
            # Check if get back a successful status code pass HTML to bs4
            soup = BeautifulSoup(site.text, 'html.parser')
            # Calling the grab_links function and passing it all of the HTML
            self.grab_links(soup)
        else:
            print("Failed to retrieve page")

    # Method to grab all .pdf from the site
    def grab_links(self, soup):
        # Loop through all the a tags
        for link in soup.find_all('a'):
            # Check if its not a blank a tag
            if link.has_attr('href'):
                href = link.get('href')
                # Check tags href/link if its a pdf
                if href.endswith('.pdf'):
                    # Add it to the links list
                    self.links.append(href)
        return self.links

# 'https://ulstercountyny.gov/real-property/assessment-rolls'