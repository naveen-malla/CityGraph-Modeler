import os
import requests
import pandas as pd

# Load the country codes and names from the CSV file
df_countries = pd.read_csv('Countries.csv')

# Define the base URL for the Overpass API
overpass_url = "http://overpass-api.de/api/interpreter"

# Make sure the 'cities' folder exists
os.makedirs('cities', exist_ok=True)

for index, row in df_countries.iterrows():
    country_code = row['alpha-2']
    country_name = row['name'].replace(' ', '_')  # Replace spaces with underscores for file naming

    # Modify the Overpass QL to filter by the current country's code
    overpass_query = f"""
    [out:json];
    area["ISO3166-1"="{country_code}"][admin_level=2];
    (node["place"~"city|town"](area);
     way["place"~"city|town"](area);
     rel["place"~"city|town"](area);
    );
    out center;
    """
    
    # Attempt to send the request to the Overpass API
    try:
        response = requests.get(overpass_url, params={'data': overpass_query})
        data = response.json()

        cities = []

        for element in data['elements']:
            if 'tags' in element:
                name = element['tags'].get('name', 'Unknown')
                population = element['tags'].get('population', 0)
                try:
                    population = int(population)
                except ValueError:
                    population = 0
                
                if population > 1000:
                    cities.append(f"{name}\n")

        # Save to a text file within the 'cities' folder
        with open(f'cities/{country_name}_cities_{country_code}.txt', 'w') as file:
            file.writelines(cities)
            
        print(f"Finished processing {country_name}")

    except Exception as e:
        print(f"Failed to process {country_name}: {e}")

print("All countries processed. Check the 'cities' folder for the results.")
