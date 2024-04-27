import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Read node_list.csv to get node coordinates and connections
node_list_file = "../../data/emb/Dresden_cseq.csv"
node_df = pd.read_csv(node_list_file)

# Step 2: Read the trier_net.csv file to get the adjacency matrix
trier_net_file = "../../data/emb/Dresden_street_network.csv"
adj_matrix = np.loadtxt(trier_net_file, delimiter=',')

# Step 3: Create a graph and add nodes and edges
G = nx.Graph()
for index, row in node_df.iterrows():
    node_id = int(row['nodeId'])
    G.add_node(node_id, pos=(row['Y'], row['X']))

# Add edges based on the adjacency matrix
for i in range(len(adj_matrix)):
    for j in range(len(adj_matrix[i])):
        if adj_matrix[i][j] == 1:
            G.add_edge(i, j)

# Step 4: Plot the graph with node coordinates
plt.figure(figsize=(10, 10))
pos = nx.get_node_attributes(G, 'pos')

# Debugging: Check for nodes with missing positions
missing_positions = [node_id for node_id in G.nodes() if node_id not in pos]
if missing_positions:
    print(f"Nodes with missing positions: {missing_positions}")
    # Assign default position to nodes with missing positions
    default_position = (0, 0)  # You can adjust this to your preference
    for node_id in missing_positions:
        pos[node_id] = default_position

nx.draw(G, pos, node_color='b', node_size=10, edge_color='k', with_labels=False)
plt.title("Map of Trier")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
