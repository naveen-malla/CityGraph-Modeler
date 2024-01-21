import osmnx as ox
import pandas as pd
import os

def get_city_center(city):
    """Get the center coordinates of a city."""
    return ox.geocode(city)

def get_street_network(city, folder_path):
    city_center = get_city_center(city)
    # Define the distance in meters for approximately 1 square km area
    distance = 500  # 500 meters radius approximates 1 square km area

    # Get the network graph around the city center
    graph = ox.graph_from_point(city_center, dist=distance, network_type="drive")
    edges_df = ox.graph_to_gdfs(graph, nodes=False)
    
    # Save to CSV in the specified folder with city name as filename
    file_name = os.path.join(folder_path, f"{city.replace(' ', '_')}_street_network.csv")
    edges_df.to_csv(file_name, index=False)

    return edges_df.columns

# Folder path where the CSV files will be saved
folder_path = '/Users/0s/Downloads/RCS/Code/CityGraph-Modeler/' # Replace with your desired folder path
os.makedirs(folder_path, exist_ok=True)

# Read city names from the file
with open('cities.txt', 'r') as file:
    cities = file.read().splitlines()

# Set to collect all unique column names
all_columns = set()

# Iterate through the cities, fetch data, and collect column names
for city in cities:
    columns = get_street_network(city, folder_path)
    all_columns.update(columns)

# Convert the set of all columns to a list
all_columns_list = list(all_columns)

# Save the list of all column names to a file
columns_file_path = os.path.join(folder_path, 'all_columns.txt')
with open(columns_file_path, 'w') as file:
    for col in all_columns_list:
        file.write(col + '\n')

# Notify the paths
print(f"All city CSVs saved in: {folder_path}")
print(f"List of all unique columns saved in: {columns_file_path}")
