import os
import requests
from bs4 import BeautifulSoup

# URL of the TLC Trip Record Data page
url = 'https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page'

# Directory to save downloaded files
download_dir = 'nyc_taxi_data'

# Make sure the download directory exists
os.makedirs(download_dir, exist_ok=True)

# Send a GET request to the webpage
response = requests.get(url)
response.raise_for_status()  # Check for request errors

# Parse the webpage content
soup = BeautifulSoup(response.text, 'html.parser')

# Define the years of interest
years_of_interest = ['2019', '2020', '2023']

# Find all anchor tags with href attributes that contain the data URLs
for link in soup.find_all('a', href=True):
    href = link['href']
    # Check if the link is for Yellow Taxi Trip Records and for the years of interest
    if 'yellow' in href and any(year in href for year in years_of_interest):
        file_url = href if href.startswith('http') else f'https://www.nyc.gov{href}'
        file_name = file_url.split('/')[-1]
        file_path = os.path.join(download_dir, file_name)

        # Download the file and save it
        print(f'Downloading {file_name}...')
        file_response = requests.get(file_url)
        try:
            file_response.raise_for_status()
            with open(file_path, 'wb') as file:
                file.write(file_response.content)
            print(f'Saved to {file_path}')
        except:
            print('No se pudo')
            


