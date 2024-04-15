import osmnx as ox
import geopandas as gpd

# Function to retrieve and process a street network for a given town or city name
def fetch_street_network(place_name, population_threshold=1000):
    # Retrieve data on urban centers from OSM
    urban_centers = ox.geometries_from_place(place_name, tags={'place': True})
    
    # Filter by population if population data is available
    if 'population' in urban_centers.columns:
        urban_centers = urban_centers[urban_centers['population'] >= population_threshold]
    
    # Assuming that the urban_centers DataFrame has the appropriate information,
    # we proceed with just one center (you would loop over all needed centers in practice)
    if not urban_centers.empty:
        some_center = urban_centers.iloc[0]  # Pick the first center

        # Get the centroid of the urban center
        centroid = some_center.geometry.centroid

        # Retrieve the network within 1 km around the centroid
        G = ox.graph_from_point((centroid.y, centroid.x), dist=1000, network_type='drive')

        # Convert the network from lat-long to UTM (meters)
        G_projected = ox.project_graph(G)

        # Simplify the network
        G_simplified = ox.simplify_graph(G_projected)
        
        return G_simplified
    else:
        return None

# Replace 'Your City Name' with the actual place you want to query
G_simplified = fetch_street_network('Berlin')