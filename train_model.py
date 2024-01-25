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

def order_and_flatten_nodes(node_features):
    # Order nodes by y-coordinate, then by x-coordinate
    ordered_nodes = node_features.sort_values(by=['longitude', 'latitude'])

    # Flatten the sequence of coordinates
    Cseq = ordered_nodes.values.flatten()
    # print(Cseq[:10])
    # print(Cseq[-10:])
    return Cseq

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

    return quantized_node_features
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

def train_model(X, A):
    # Code to train the model using node feature matrix X and adjacency matrix A
    pass

def generate_synthetic_network(model):
    # Code to generate synthetic street networks using the trained model
    pass

# Directory containing the CSV files
directory = 'files/'

# Iterate over each CSV file
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        
        # Create graph from linestrings
        G = create_graph_from_linestrings(df)
        #print(f"Number of nodes in the graph: {G.number_of_nodes()}")

        # Create node feature matrix
        X = create_node_feature_matrix(df)
        #print(X.head())
        Cseq = order_and_flatten_nodes(X)
        X_centered = center_coordinates(X)
        #print("X_centered head \n", X_centered.head())
        X_normalized = normalize_coordinates(X_centered)
        #print("X_normalised head \n", X_normalized.head())
        X_quantized = quantize_coordinates(X_normalized)
        print(X_quantized.head())
        # Create adjacency matrix
        # A = create_adjacency_matrix(G)
        # print(A)
        # Train the model
        # model = train_model(X, A)

        # Generate synthetic network
        # synthetic_network = generate_synthetic_network(model)

        # Analysis and evaluation of the synthetic network goes here
