import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def convert_embeddings_to_adjacency_matrix(emb_file_path, threshold=0.8):
    # Read embeddings
    embeddings = {}
    max_length = 0  # Keep track of the maximum length of embedding vectors
    with open(emb_file_path, 'r') as emb_file:
        for line in emb_file:
            parts = line.strip().split()
            node_id = int(parts[0])
            vec = np.array([float(x) for x in parts[1:]], dtype=np.float32)
            embeddings[node_id] = vec
            max_length = max(max_length, len(vec))

    # Ensure all embeddings are of the same length
    for node in embeddings.keys():
        if len(embeddings[node]) < max_length:
            embeddings[node] = np.append(embeddings[node], [0]*(max_length - len(embeddings[node])))
    
    # Create embedding matrix
    nodes = sorted(embeddings.keys())
    embedding_matrix = np.array([embeddings[node] for node in nodes])
    
    # Compute cosine similarity and threshold
    similarity_matrix = cosine_similarity(embedding_matrix)
    adjacency_matrix = (similarity_matrix > threshold).astype(int)

    # Ensure self-connections are removed
    np.fill_diagonal(adjacency_matrix, 0)
    
    return adjacency_matrix, nodes

def save_adjacency_matrix_to_file(adjacency_matrix, output_file):
    np.savetxt(output_file, adjacency_matrix, fmt='%d', delimiter=',')

def main():
    base_folder = 'Test_dataset_Emb'
    output_base_folder = 'Test_dataset_synadjmatrix'  # Set base output folder
    threshold = 0.876  # Update with your chosen threshold

    for country_folder in os.listdir(base_folder):
        country_path = os.path.join(base_folder, country_folder)
        if os.path.isdir(country_path):  # Ensure it is a directory
            for file_name in os.listdir(country_path):
                if file_name.endswith(".emb"):
                    city_name = os.path.splitext(file_name)[0]
                    emb_file_path = os.path.join(country_path, file_name)
                    adjacency_output_file = os.path.join(output_base_folder, country_folder, f"{city_name}_admatrix.csv")
                    os.makedirs(os.path.dirname(adjacency_output_file), exist_ok=True)  # Ensure directory exists
                    adjacency_matrix, nodes = convert_embeddings_to_adjacency_matrix(emb_file_path, threshold)
                    save_adjacency_matrix_to_file(adjacency_matrix, adjacency_output_file)
                    print(f"Saved adjacency matrix for {city_name} in {country_folder} to {adjacency_output_file}")

if __name__ == "__main__":
    main()
