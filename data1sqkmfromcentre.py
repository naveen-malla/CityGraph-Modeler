import osmnx as ox
import pandas as pd

def extract_street_network(city_center, distance_km, city_name):
    """
    Extracts the street network within a square of 'distance_km' kilometers
    from the 'city_center'.
    """
    # Get the network graph
    G = ox.graph_from_point(city_center, dist=distance_km*1000, network_type='drive')

    # Extract nodes and edges
    nodes, edges = ox.graph_to_gdfs(G)

    # Save to files
    nodes.to_csv(f"{city_name}_nodes.csv")
    edges.to_csv(f"{city_name}_edges.csv")

# Read the city coordinates from the text file
with open("./city_coordinates.txt", "r") as file:
    for line in file:
        parts = line.split(":")
        city_name = parts[0].strip()
        coords = parts[1].strip().strip("()").split(",")
        latitude = float(coords[0].strip())
        longitude = float(coords[1].strip())

        # Extract and save street network for each city
        extract_street_network((latitude, longitude), 1, city_name)
