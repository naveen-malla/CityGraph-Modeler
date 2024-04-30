import pandas as pd
import numpy as np
import networkx as nx
import os
import re
import logging

logging.basicConfig(level=logging.INFO)

def parse_linestring(linestring):
    # Extract coordinates from LINESTRING
    coordinates = re.findall(r'LINESTRING \((.*?)\)', linestring)
    if coordinates:
        return [tuple(map(float, coord.split())) for coord in coordinates[0].split(', ')]
    else:
        return []  # Return an empty list if no match is found

def create_graph_from_linestrings(df):
    G = nx.Graph()
    for linestring in df['geometry']:
        # Extract coordinates from LINESTRING
        linestring = re.findall(r'LINESTRING \((.*?)\)', linestring)[0]
        coordinates = [tuple(map(float, coord.split())) for coord in linestring.split(', ')]
        # Add nodes and edges to the graph
        for i in range(len(coordinates) - 1):
            G.add_edge(coordinates[i], coordinates[i + 1])
    return G

def create_node_feature_matrix(df):
    # Initialize an empty list to store node features
    node_features_list = []

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        # Parse the LINESTRING to get coordinates
        coordinates = parse_linestring(row['geometry'])
        for coord in coordinates:
            # Append each coordinate as a dictionary to the list
            node_features_list.append({'latitude': coord[0], 'longitude': coord[1]})

    # Convert the list of dictionaries to a DataFrame
    node_features = pd.DataFrame(node_features_list)

    # Drop duplicate rows to ensure each node is unique
    node_features = node_features.drop_duplicates().reset_index(drop=True)
    return node_features


def center_coordinates(node_features):
    # Calculate the geometric center
    center_x = node_features['latitude'].mean()
    center_y = node_features['longitude'].mean()

    # Shift the coordinates to center them
    node_features['centered_latitude'] = node_features['latitude'] - center_x
    node_features['centered_longitude'] = node_features['longitude'] - center_y

    #logging.info(f"Center of nodes shifted to: ({center_x}, {center_y})")
    return node_features

def normalize_coordinates(centered_node_features):
    max_x = centered_node_features['centered_latitude'].max()
    min_x = centered_node_features['centered_latitude'].min()
    max_y = centered_node_features['centered_longitude'].max()
    min_y = centered_node_features['centered_longitude'].min()

    diagonal_length = ((max_x - min_x)**2 + (max_y - min_y)**2)**0.5

    centered_node_features['normalized_latitude'] = centered_node_features['centered_latitude'] / diagonal_length
    centered_node_features['normalized_longitude'] = centered_node_features['centered_longitude'] / diagonal_length

    return centered_node_features

def quantize_coordinates(normalized_node_features):
    quantized_node_features = normalized_node_features.copy()
    quantized_node_features['quantized_latitude'] = ((normalized_node_features['normalized_latitude'] * 127.5) + 127.5).astype(int)
    quantized_node_features['quantized_longitude'] = ((normalized_node_features['normalized_longitude'] * 127.5) + 127.5).astype(int)

    return quantized_node_features

def order_and_flatten_nodes(node_features, cseq_file):
    # Select only the quantized latitude and longitude
    quantized_coords = node_features[['quantized_latitude', 'quantized_longitude']]
    
    # Order nodes by y-coordinate, then by x-coordinate
    ordered_coords = quantized_coords.sort_values(by=['quantized_longitude', 'quantized_latitude'])

    # Flatten the sequence of coordinates
    Cseq = ordered_coords.values.flatten()
    print("Totoal Cseq: ", Cseq)

    with open(cseq_file, 'w') as file:
        file.write(' '.join(map(str, Cseq)) + '\n')
    return Cseq

def create_adjacency_matrix(G):
    # Initialize the adjacency matrix with zeros
    adjacency_matrix = np.zeros((len(G.nodes), len(G.nodes)))

    # Populate the matrix
    for node1, node2 in G.edges():
        index1 = list(G.nodes).index(node1)
        index2 = list(G.nodes).index(node2)
        adjacency_matrix[index1][index2] = 1
        adjacency_matrix[index2][index1] = 1  # For undirected graph

    return adjacency_matrix

# New base directory for Cseq data
cseq_base_directory = 'Cseq_Data_Master/'
os.makedirs(cseq_base_directory, exist_ok=True)  # Create base directory if it doesn't exist

# Base directory containing the country folders with city CSVs
base_directory = 'Street_Network_Data_Raw/'  

# Iterate over each country folder
for country_folder_name in os.listdir(base_directory):
    country_folder_path = os.path.join(base_directory, country_folder_name)
    
    # Skip if it's not a directory
    if not os.path.isdir(country_folder_path):
        continue

    # Extract country name and code from folder name
    country_name, country_code = country_folder_name.rsplit('_', 1)

    # Create a new directory for Cseq data corresponding to this country
    country_cseq_directory = os.path.join(cseq_base_directory, country_folder_name)
    os.makedirs(country_cseq_directory, exist_ok=True)

    # Iterate over each CSV file in the country folder
    for filename in os.listdir(country_folder_path):
        if filename.endswith(".csv"):
            print(f"Processing file: {filename}")
            filepath = os.path.join(country_folder_path, filename)
            df = pd.read_csv(filepath)
            # Create graph from linestrings
            G = create_graph_from_linestrings(df)
            print(f"Number of nodes in the graph: {G.number_of_nodes()}")

            # Create node feature matrix
            X = create_node_feature_matrix(df)
            #print(X.head())
    
            X_centered = center_coordinates(X)
            #print("X_centered head \n", X_centered.head())
            X_normalized = normalize_coordinates(X_centered)
            #print("X_normalised head \n", X_normalized.head())
            X_quantized = quantize_coordinates(X_normalized)
            #print("X_quantized head \n", X_quantized.head())

            # File path for saving the Cseq
            city_name = filename.replace('_street_network.csv', '')
            cseq_file = os.path.join(country_cseq_directory, f"{city_name}_cseq.txt")

            # Call order_and_flatten_nodes and pass cseq_file instead of using a global variable
            Cseq = order_and_flatten_nodes(X_quantized, cseq_file)            
            print("Length of Cseq of " + filename + ": ", len(Cseq))
            print("Cseq first 100: \n", Cseq[:100])
            # Create adjacency matrix
            A = create_adjacency_matrix(G)
            
