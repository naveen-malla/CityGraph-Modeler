import argparse
import os
import networkx as nx
import node2vec
from gensim.models import Word2Vec

def parse_args():
    '''
    Parses the node2vec arguments.
    '''
    parser = argparse.ArgumentParser(description="Run node2vec.")
    parser.add_argument('--input-root-dir', nargs='?', default='Test_dataset_Edgelist/',
                        help='Input root directory path containing country folders with .edgelist files')
    parser.add_argument('--output-root-dir', nargs='?', default='Test_dataset_Emb/',
                        help='Output root directory path for country folders with embeddings')
    parser.add_argument('--dimensions', type=int, default=128,
                        help='Number of dimensions. Default is 128.')
    parser.add_argument('--walk-length', type=int, default=50,
                        help='Length of walk per source. Default is 80.')
    parser.add_argument('--num-walks', type=int, default=20,
                        help='Number of walks per source. Default is 10.')
    parser.add_argument('--window-size', type=int, default=5,
                        help='Context size for optimization. Default is 10.')
    parser.add_argument('--iter', default=100, type=int,
                        help='Number of epochs in SGD')
    parser.add_argument('--workers', type=int, default=8,
                        help='Number of parallel workers. Default is 8.')
    parser.add_argument('--p', type=float, default=20,
                        help='Return hyperparameter. Default is 1.')
    parser.add_argument('--q', type=float, default=20,
                        help='Inout hyperparameter. Default is 1.')
    parser.add_argument('--weighted', action='store_true',
                        help='Boolean specifying (un)weighted. Default is unweighted.')
    parser.add_argument('--directed', action='store_true',
                        help='Graph is (un)directed. Default is undirected.')
    return parser.parse_args()

def process_graph(input_file, output_file, args):
    '''
    Pipeline for representational learning for all nodes in a graph given input and output file paths.
    '''
    if args.weighted:
        G = nx.read_edgelist(input_file, nodetype=int, data=(('weight', float),), create_using=nx.DiGraph())
    else:
        G = nx.read_edgelist(input_file, nodetype=int, create_using=nx.DiGraph())
        for edge in G.edges():
            G[edge[0]][edge[1]]['weight'] = 1

    if not args.directed:
        G = G.to_undirected()

    g2v = node2vec.Graph(G, args.directed, args.p, args.q)
    g2v.preprocess_transition_probs()
    walks = g2v.simulate_walks(args.num_walks, args.walk_length)
    learn_embeddings(walks, output_file, args)

def learn_embeddings(walks, output_file, args):
    '''
    Learn embeddings by optimizing the Skipgram objective using SGD and save to output file.
    '''
    walks = [list(map(str, walk)) for walk in walks]
    model = Word2Vec(walks, vector_size=args.dimensions, window=args.window_size, min_count=0, sg=1, workers=args.workers, epochs=args.iter)
    model.wv.save_word2vec_format(output_file)
    return

def main(args):
    '''
    Iterate through all .edgelist files in the input directory and process each graph.
    '''
    for filename in os.listdir(args.input_dir):
        if filename.endswith(".edgelist"):
            input_file = os.path.join(args.input_dir, filename)
            output_file = os.path.join(args.output_dir, filename.replace('.edgelist', '.emb'))
            print(f'Processing {input_file}...')
            process_graph(input_file, output_file, args)
            print(f'Embeddings saved to {output_file}')


def main(args):
    '''
    Iterate through all country folders and .edgelist files within each folder, and process each graph.
    '''
    # Create the output root directory if it doesn't exist
    if not os.path.exists(args.output_root_dir):
        os.makedirs(args.output_root_dir)

    # Iterate over each country directory in the input root directory
    for country_dir in os.listdir(args.input_root_dir):
        country_input_path = os.path.join(args.input_root_dir, country_dir)
        country_output_path = os.path.join(args.output_root_dir, country_dir + '_Emb')

        # Create the country's output directory if it doesn't exist
        if not os.path.exists(country_output_path):
            os.makedirs(country_output_path)

        # Iterate over each .edgelist file in the country's input directory
        if os.path.isdir(country_input_path):
            for filename in os.listdir(country_input_path):
                if filename.endswith(".edgelist"):
                    try:
                        input_file = os.path.join(country_input_path, filename)
                        output_file = os.path.join(country_output_path, filename.replace('.edgelist', '.emb'))
                        print(f'Processing {input_file}...')
                        process_graph(input_file, output_file, args)
                        print(f'Embeddings saved to {output_file}')
                    except Exception as e:
                        print(f"Error processing {filename}: {e}. Skipping this file.")

if __name__ == "__main__":
    args = parse_args()
    main(args)


if __name__ == "__main__":
    args = parse_args()
    main(args)