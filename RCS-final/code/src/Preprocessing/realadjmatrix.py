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

# Directory containing CSV files
directory = '../../data/Germany_DE'
directory1 = '../../data/realadjmatrix/'

# Create the output directory if it doesn't exist
if not os.path.exists(directory1):
    os.makedirs(directory1)

# Loop through files in the directory
for filename in os.listdir(directory):
    if filename.endswith("_street_network.csv"):
        # Read the CSV file into a DataFrame
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)

        # Extract nodes and edges from the DataFrame
        nodes = set()
        edges = []
        for index, row in df.iterrows():
            if 'osmid' in row:  # Check if the column exists
                nodes.add(row['osmid'])  # Add 'osmid' to the set of nodes
            if 'geometry' in row:  # Check if the column exists
                geometry = row['geometry']
                # Assuming geometry is in the format "LINESTRING (x1 y1, x2 y2, ...)"
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
        output_filename = os.path.join(directory1, f"{os.path.splitext(filename)[0]}_admatrix.csv")
        adjacency_df.to_csv(output_filename, index=False, header=False)
        print(f"Saved adjacency matrix to {output_filename}")
