import pandas as pd
import numpy as np
import networkx as nx
import os

def create_adjacency_matrix(G):
    # Initialize the adjacency matrix with zeros
    adjacency_matrix = np.zeros((len(G.nodes), len(G.nodes)), dtype=int)
    # Populate the matrix
    for node1, node2 in G.edges():
        index1 = list(G.nodes).index(node1)
        index2 = list(G.nodes).index(node2)
        adjacency_matrix[index1][index2] = 1
        adjacency_matrix[index2][index1] = 1  # For undirected graph
    return adjacency_matrix

# New function to process each CSV file and generate an adjacency matrix
def process_csv_file(file_path, output_directory):
    df = pd.read_csv(file_path)

    # Extract nodes and edges from the DataFrame
    nodes = set()
    edges = []
    for index, row in df.iterrows():
        if 'osmid' in row:
            nodes.add(row['osmid'])
        if 'geometry' in row:
            geometry = row['geometry']
            coordinates = geometry.replace('LINESTRING (', '').replace(')', '').split(', ')
            nodes.update([float(coord.split()[0]) for coord in coordinates])
            edges.extend([(float(coordinates[i].split()[0]), float(coordinates[i+1].split()[0])) for i in range(len(coordinates)-1)])
    
    # Create a graph from the nodes and edges
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    # Generate the adjacency matrix
    adjacency_matrix = create_adjacency_matrix(G)

    # Convert adjacency matrix to DataFrame
    adjacency_df = pd.DataFrame(adjacency_matrix)

    # Save DataFrame to a CSV file
    output_filename = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(file_path))[0]}_admatrix.csv")
    adjacency_df.to_csv(output_filename, index=False, header=False)
    print(f"Saved adjacency matrix to {output_filename}")

# Directory containing the Test_Dataset folder
root_directory = 'Test_dataset'
output_root_directory = 'Test_dataset_realadjmatrix/'

# Iterate over each country in the Test_Dataset directory
for country in os.listdir(root_directory):
    country_path = os.path.join(root_directory, country)
    if os.path.isdir(country_path):
        # Create a specific output directory for each country if it does not exist
        country_output_directory = os.path.join(output_root_directory, country)
        if not os.path.exists(country_output_directory):
            os.makedirs(country_output_directory)

        # Iterate over each CSV file in the country directory
        for filename in os.listdir(country_path):
            if filename.endswith("_street_network.csv"):
                file_path = os.path.join(country_path, filename)
                process_csv_file(file_path, country_output_directory)
