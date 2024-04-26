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
    return Cseq

def center_coordinates(node_features):
    # Calculate the geometric center
    center_x = node_features['latitude'].mean()
    center_y = node_features['longitude'].mean()

    # Shift the coordinates to center them
    node_features['centered_latitude'] = node_features['latitude'] - center_x
    node_features['centered_longitude'] = node_features['longitude'] - center_y

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

def create_c_sequence(X_quantized, node_mapping):
    c_sequence = X_quantized[['quantized_latitude', 'quantized_longitude']].copy()
    c_sequence.columns = ['latitude', 'longitude']  # Rename columns
    c_sequence.insert(0, 'node_id', range(len(c_sequence)))  # Insert node_id column as the first column
    return c_sequence

def create_edgelist(G, node_mapping):
    edgelist = [(node_mapping[edge[0]], node_mapping[edge[1]]) for edge in G.edges()]
    return edgelist

# Directory containing the CSV files
directory = '/Users/0s/Downloads/RCS/Code/CityGraph-Modeler/extractdata/input/'
directory1 = '/Users/0s/Downloads/RCS/Code/CityGraph-Modeler/extractdata/output/'

# Iterate over each CSV file
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        
        # Create graph from linestrings
        G = create_graph_from_linestrings(df)

        # Create node feature matrix
        X = create_node_feature_matrix(df)
        Cseq = order_and_flatten_nodes(X)
        X_centered = center_coordinates(X)
        X_normalized = normalize_coordinates(X_centered)
        X_quantized = quantize_coordinates(X_normalized)

        # Create a mapping from quantized coordinates to node IDs
        node_mapping = {(row['latitude'], row['longitude']): node_id for node_id, (_, row) in enumerate(X_quantized.iterrows())}

        # Create c_sequence DataFrame
        c_sequence_df = create_c_sequence(X_quantized, node_mapping)

        # Save c_sequence DataFrame to a CSV file
        c_sequence_filename = os.path.join(directory1, f'{filename[:-4]}_c_sequence.csv')
        c_sequence_df.to_csv(c_sequence_filename, index=False)

        print(f"c_sequence.csv file saved successfully for {filename}.")

        # Create edgelist
        edgelist = create_edgelist(G, node_mapping)

        # Save edgelist to a file
        edgelist_filename = os.path.join(directory1, f'{filename[:-4]}.edgelist')
        with open(edgelist_filename, 'w') as f:
            for edge in edgelist:
                f.write(f"{edge[0]} {edge[1]}\n")

        print(f"{filename[:-4]}.edgelist file saved successfully.")