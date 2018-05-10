import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

base = 'https://www.nytimes.com'
time_pattern = re.compile('\d+ year')

def get_years(det_page):
    """
    Given a detainee page return the number of years detained
    """
    div = det_page.find('div', 
                        class_='nytint-detainee-fullcol')
    matches = time_pattern.findall(div.text)
    return int(matches[0].rstrip(' year'))

def get_detainee_page(detainee_link):
    """
    Given a detainee link get a BeautifulSoup page
    """
    detainee_response = requests.get(
            base + detainee_link.attrs['href'])
    
    return BeautifulSoup(detainee_response.text, 
                         'html.parser')


# Get the main detainees page
path = '/interactive/projects/guantanamo/detainees/current'
response = requests.get(base + path)
page = BeautifulSoup(response.text, 'html.parser')

# Get the detainee links
detainee_links = page.find_all('a', href=re.compile('detainees/\d'))

# Initialize lists for results
names = []
countries = []
years = []

for a in detainee_links:
    print(a.text) # Print name to watch progress
    names.append(a.text)
    countries.append(a.find_next('a').text)

    detainee_page = get_detainee_page(a)
    years.append(get_years(detainee_page))

    time.sleep(2) # Sleep for 2 seconds between requests

# Put results in a dataframe for writing to CSV
detainees = pd.DataFrame({'name': names,
                          'country': countries,
                          'years': years})

detainees.to_csv('guantanamo.csv', index=False)
