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
            # Extend the embedding with zeros if it's shorter than the maximum length
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
    emb_folder = '../../data/emb/'
    threshold = 0.876  # Update with your chosen threshold

    for file_name in os.listdir(emb_folder):
        if file_name.endswith(".emb"):
            city_name = os.path.splitext(file_name)[0]
            emb_file_path = os.path.join(emb_folder, file_name)
            adjacency_output_file = f"./emb/{city_name}_admatrix.csv"  # Adjust output file path
            adjacency_matrix, nodes = convert_embeddings_to_adjacency_matrix(emb_file_path, threshold)
            save_adjacency_matrix_to_file(adjacency_matrix, adjacency_output_file)
            print(f"Saved adjacency matrix for {city_name} to {adjacency_output_file}")

if __name__ == "__main__":
    main()
