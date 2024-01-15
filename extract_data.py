import osmnx as ox
import pandas as pd
import os

def get_street_network(city, folder_path):
    graph = ox.graph_from_place(city, network_type="drive")
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




'''
name: The name of the street or way.
junction: Indicates the nature of the junction, if applicable.
service: Defines the service type of a way, typically for roads (e.g., parking, driveway).
geometry: The geometrical shape of the street or way, usually in the form of a LineString.
maxspeed: The maximum speed limit on the way.
est_width: Estimated width of the street or way.
highway: Classifies the type of road or path.
lanes: The number of lanes on the street or way.
width: The physical width of the way.
length: The length of the way, calculated as the great-circle distance between nodes.
oneway: Indicates if the street is one-way.
osmid: The OpenStreetMap ID of the way.
access: Describes access restrictions for the way.
tunnel: Indicates if the way is a tunnel.
area: Specifies if the way forms an area.
bridge: Indicates if the way is a bridge.
ref: Reference codes or numbers associated with the way.
reversed: Indicates if the direction of the way is reversed in the data.
'''