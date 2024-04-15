import os
import requests
import pandas as pd

# Load the country codes and names from the CSV file
df_countries = pd.read_csv('Countries.csv')

# Define the base URL for the Overpass API
overpass_url = "http://overpass-api.de/api/interpreter"

# Make sure the 'cities' folder exists
os.makedirs('cities', exist_ok=True)

# Modify the Overpass QL to filter by the current country's code
overpass_query = f"""
[out:json][timeout:25];
area["ISO3166-1"="IN"][admin_level=2];
(node["place"~"city|town"](area);
    way["place"~"city|town"](area);
    rel["place"~"city|town"](area);
);
out center;
"""


response = requests.get(overpass_url, params={'data': overpass_query})
data = response.json()
print(data)