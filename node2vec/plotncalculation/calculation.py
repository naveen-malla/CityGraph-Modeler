import os
import pandas as pd
import networkx as nx
import numpy as np
import csv

def calculate_average_street_length(G):
    return sum(data['length'] for u, v, data in G.edges(data=True)) / G.number_of_edges()

def calculate_avg_edge_per_node(G):
    return G.number_of_edges() / G.number_of_nodes()

def calculate_circuity(G):
    total_length = sum(data['length'] for u, v, data in G.edges(data=True))
    total_nodes = G.number_of_nodes()
    degrees = dict(G.degree())
    sum_degrees = sum(degrees.values())
    return total_length / (total_nodes * (total_nodes - 1) / 2)

def calculate_avg_form_factor(G):
    perimeters = calculate_avg_perimeter(G)
    areas = calculate_avg_area(G)
    return perimeters / areas

def calculate_avg_perimeter(G):
     return sum(data['length'] for u, v, data in G.edges(data=True))

def calculate_avg_area(G):
    perimeters = calculate_avg_perimeter(G)
    total_nodes = G.number_of_nodes()
    degrees = dict(G.degree())
    total_degree = sum(degrees.values())
    return (4 * perimeters + 2 * np.sqrt(total_degree * (total_degree - 3))) / 2

def calculate_avg_block_size(G):
    node_sizes = nx.get_node_attributes(G, 'blockSize')
    return sum(node_sizes.values()) / G.number_of_nodes()

def calculate_avg_compactness(G):
    areas = calculate_avg_area(G)
    perimeters = calculate_avg_perimeter(G)
    return areas / (perimeters**2)

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
                    G.add_node(node_id, pos=(row['X'], row['Y']))

                # Add edges with lengths from adjacency matrix
                for i in range(len(adj_matrix)):
                    for j in range(i+1, len(adj_matrix)):
                        if adj_matrix[i][j] == 1:
                            G.add_edge(i, j, length=1)
                            G.add_edge(j, i, length=1)

                if option == 1:
                    # Calculate average street length
                    average_street_length = calculate_average_street_length(G)
                    results[city_name] = average_street_length
                elif option == 2:
                    # Calculate average number of edges per node
                    avg_edge_per_node = calculate_avg_edge_per_node(G)
                    results[city_name] = avg_edge_per_node
                elif option == 3:
                    # Calculate average circuitity
                    circuitity = calculate_circuity(G)
                    results[city_name] = circuitity
                elif option == 4:
                    # Calculate average form factor
                    form_factor = calculate_avg_form_factor(G)
                    results[city_name] = form_factor
                elif option == 5:
                    # Calculate average block size
                    block_size = calculate_avg_block_size(G)
                    results[city_name] = block_size
                elif option == 6:
                    # Calculate average compactness
                    compactness = calculate_avg_compactness(G)
                    results[city_name] = compactness
                else:
                    print("Invalid option. Please try again.")
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    return results

def main():
    folder_path = "/real_map/"
    option = int(input("Enter the option you want to calculate: "))
    results = process_files(folder_path, option)

    output_file = f"results_{option}.csv"
    fieldnames = ['City', 'Result']

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for city, result in results.items():
            writer.writerow({'City': city, 'Result': result})
        print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
