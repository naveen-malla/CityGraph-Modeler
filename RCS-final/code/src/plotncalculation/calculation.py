import os
import pandas as pd
import numpy as np
import networkx as nx
from scipy.spatial import ConvexHull

def calculate_average_street_length(G):
    total_length = sum(nx.get_edge_attributes(G, 'length').values())
    num_edges = len(G.edges)
    if num_edges > 0:
        return total_length / num_edges
    else:
        return 0

def calculate_avg_edge_per_node(G):
    if len(G.nodes) > 0:
        return len(G.edges) / len(G.nodes)
    else:
        return 0

def calculate_circuity(G):
    total_network_distance = sum(nx.all_pairs_dijkstra_path_length(G).values())
    total_euclidean_distance = 0
    for u, v, data in G.edges(data=True):
        total_euclidean_distance += np.sqrt((G.nodes[u]['pos'][0] - G.nodes[v]['pos'][0])**2 + 
                                            (G.nodes[u]['pos'][1] - G.nodes[v]['pos'][1])**2)
    if total_euclidean_distance > 0:
        return total_network_distance / total_euclidean_distance
    else:
        return 0

def calculate_avg_form_factor(G):
    if len(G.nodes) == 0:
        return 0
    else:
        areas = []
        for component in nx.connected_components(G):
            node_positions = np.array([G.nodes[node]['pos'] for node in component])
            hull = ConvexHull(node_positions)
            areas.append(hull.volume)
        return sum(areas) / len(G.nodes)

def calculate_avg_block_size(G):
    if len(G.nodes) == 0:
        return 0
    else:
        return sum([nx.node_connectivity(G, node) for node in G.nodes]) / len(G.nodes)

def calculate_avg_compactness(G):
    if len(G.nodes) == 0:
        return 0
    else:
        compactness_values = []
        for component in nx.connected_components(G):
            node_positions = np.array([G.nodes[node]['pos'] for node in component])
            hull = ConvexHull(node_positions)
            compactness_values.append((hull.area**2) / (4 * np.pi * hull.volume))
        return sum(compactness_values) / len(G.nodes)

def process_files(folder_path, option):
    results = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith("_admatrix.csv"):
            city_name = file_name.split("_")[0]
            node_list_file = os.path.join(folder_path, f"{city_name}_cseq.csv")
            net_file = os.path.join(folder_path, file_name)

            try:
                # Read node list
                node_df = pd.read_csv(node_list_file)

                # Read adjacency matrix
                adj_matrix = np.loadtxt(net_file, delimiter=',')

                # Create a graph
                G = nx.Graph()

                # Add nodes with positions
                for _, row in node_df.iterrows():
                    node_id = int(row['nodeId'])
                    G.add_node(node_id, pos=(row['Y'], row['X']))

                # Add edges with lengths from adjacency matrix
                for i in range(len(adj_matrix)):
                    for j in range(len(adj_matrix[i])):
                        if adj_matrix[i][j] == 1:
                            node1 = node_df.loc[i]
                            node2 = node_df.loc[j]
                            length = np.sqrt((node1['X'] - node2['X'])**2 + (node1['Y'] - node2['Y'])**2)  # Euclidean distance
                            G.add_edge(i, j, length=length)

                # Perform chosen calculation
                if option == '1':
                    result = calculate_average_street_length(G)
                    results[city_name] = result
                elif option == '2':
                    result = calculate_avg_edge_per_node(G)
                    results[city_name] = result
                elif option == '3':
                    result = calculate_circuity(G)
                    results[city_name] = result
                elif option == '4':
                    result = calculate_avg_form_factor(G)
                    results[city_name] = result
                elif option == '5':
                    result = calculate_avg_block_size(G)
                    results[city_name] = result
                elif option == '6':
                    result = calculate_avg_compactness(G)
                    results[city_name] = result

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    return results

def main():
    folder_path = "../../data/real_map/"
    option = input("Choose an option:\n"
                   "1. Calculate average street length\n"
                   "2. Calculate average edge per node\n"
                   "3. Calculate circuity\n"
                   "4. Calculate average form factor\n"
                   "5. Calculate average block size\n"
                   "6. Calculate average compactness\n"
                   "Option: ")

    if option in ['1', '2', '3', '4', '5', '6']:
        results = process_files(folder_path, option)
        output_file = f"result_option_{option}.csv"

        if results:
            df = pd.DataFrame(list(results.items()), columns=['City', 'Value'])
            df.to_csv(output_file, index=False)
            print(f"Results saved to {output_file}")
        else:
            print("No data to process.")

    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()