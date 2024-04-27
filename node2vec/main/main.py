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
    parser.add_argument('--input-dir', nargs='?', default='../../data/graph/',
                        help='Input directory path containing .edgelist files')
    parser.add_argument('--output-dir', nargs='?', default='../../data/emb/',
                        help='Output directory path for embeddings')
    parser.add_argument('--dimensions', type=int, default=128,
                        help='Number of dimensions. Default is 128.')
    parser.add_argument('--walk-length', type=int, default=50,
                        help='Length of walk per source. Default is 80.')
    parser.add_argument('--num-walks', type=int, default=50,
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

if __name__ == "__main__":
    args = parse_args()
    main(args)
