import osmnx as ox
import pandas as pd
import os

def get_city_center(city, country_code):
    """Get the center coordinates of a city."""
    location_query = f"{city}, {country_code}"
    try:
        return ox.geocode(location_query)
    except Exception as e:
        print(f"Could not geocode {city}, {country_code}: {e}")
        return None

def get_street_network(city, country_code, country_name, base_folder_path):
    
    # If there's a slash in the city name, take only the first part
    city = city.split('/')[0].strip()

    city_center = get_city_center(city, country_code)
    if city_center is None:
        return

    # Define the distance in meters for approximately 1 square km area
    distance = 500  # 500 meters radius approximates 1 square km area

   # Folder path for the country using its name and code
    country_folder = os.path.join(base_folder_path, f"{country_name}_{country_code}")
    os.makedirs(country_folder, exist_ok=True)
    
    # File name for saving the street network
    file_name = os.path.join(country_folder, f"{city.replace(' ', '_')}_street_network.csv")

    # Check if the street network file already exists
    if os.path.exists(file_name):
        print(f"Street network for {city}, {country_code} already downloaded.")
        return

    # Get the network graph around the city center
    try:
        graph = ox.graph_from_point(city_center, dist=distance, network_type="drive")
        edges_df = ox.graph_to_gdfs(graph, nodes=False)
        
        # Save to CSV
        edges_df.to_csv(file_name, index=False)
        #print(f"Street network for {city}, {country_code} saved to {file_name}.")
    except Exception as e:
        print(f"Error fetching data for {city}, {country_code}: {e}")

# Base folder path where the country folders and CSV files will be saved
base_folder_path = '/Users/naveenmalla/Desktop/RCS/Code/Data/'  # Replace with your desired base folder path
cities_folder_path = 'cities'  # Replace with the actual path

# Iterate through the city files in the cities folder
for city_file in os.listdir(cities_folder_path):
    if city_file.endswith('.txt'):
        # Extract country code and country name from the file name
        country_code = city_file[-6:-4]
        country_name = city_file[:-11].replace('_', ' ')

        # Open city file and process each city
        with open(os.path.join(cities_folder_path, city_file), 'r') as file:
            cities = file.read().splitlines()

        for city in cities:
            if city.strip():  # Ensure the city name is not empty
                get_street_network(city, country_code, country_name, base_folder_path)

print("Processing complete. All available city street networks have been downloaded.")
