import osmnx as ox
import networkx as nx

def extract_street_network(city_center, distance_km):
    """
    Extracts the street network within a square of 'distance_km' kilometers
    from the 'city_center'.
    """
    # Get the network graph
    G = ox.graph_from_point(city_center, dist=distance_km*1000, network_type='drive')

    # Extract nodes and edges
    nodes, edges = ox.graph_to_gdfs(G)

    return nodes, edges

# Example usage
city_center = (49.7596, 6.6439)  # Replace with the latitude and longitude of the city center
distance_km = 1  # 1 square km from the center

nodes, edges = extract_street_network(city_center, distance_km)

# You can now work with 'nodes' and 'edges' DataFrames
print(nodes.head())
print(edges.head())
