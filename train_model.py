import pandas as pd
import numpy as np
import networkx as nx
import os
import re

def parse_linestring(linestring):
    # Extract coordinates from LINESTRING
    coordinates = re.findall(r'\\((.*?)\\)', linestring)
    return [tuple(map(float, coord.split())) for coord in coordinates[0].split(', ')]

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

        # Create adjacency matrix
        A = create_adjacency_matrix(G)
        print(A)
        # Train the model
        # model = train_model(X, A)

        # Generate synthetic network
        # synthetic_network = generate_synthetic_network(model)

        # Analysis and evaluation of the synthetic network goes here
