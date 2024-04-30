

# Data gathering

# Flow to run
** collect_cities.py: Collects the data from OpenStreetMap API and stores it in the cities folder
** data_1sqkm_from_centre: Extracts data from the centroid of the city with a radius of 1sqkm

# 0node 
** 0node.py: processes the street data, creates the graph and the master cseq file

# node2vec in Python
The node2vec part in this repository implements node2vec by Grover, Aditya and Leskovec, Jure. For details of the model, refer to their original [implementation](https://github.com/aditya-grover/node2vec/tree/master) and [their paper](https://arxiv.org/pdf/1607.00653).

# How to run
* Specify your arguments in `args.py`: you can change dataset and other arguments there

# Flow to run
* node2vec/Preprocessing:
** Create .edgelist with node2vec/Preprocessing/edgelist.py as input for node2vec model
** Create real adjacency matrix node2vec/Preprocessing/realadjmatrix.py for creating real map after
* node2vec/main:
** Take .edgelist created above as input, run it in node2vec/main/main.py to create node embedidng .emb
** Create reconstructed adjacency matrix with node2vec/main/admatrix.py from input .emb 
* node2vec/plotncalculation:
** With node2vec/plotncalculation/plotmap.py: take the Cseq_predicted and reconstructed adjacency matrix to create synthetic street network
** node2vec/plotncalculation/calculation.py: input (Cseq_test, real adjacency matrix) to calculate feature on real map, input (Cseq_predicted, reconstructed adjacency matrix) to calculate feature on synthetic map

# Notes
* Per-epoch training time is a bit slower than the original implementation.
* In Real_admatrix data folder, it contains real adjacency matrix in format .csv.
* In Test_dataset_Emb data folder, it contains node embedding in format .emb.
* In Reconstructed_admatrix data folder, it contains reconstructed adjacency matrix in format .csv.
* Feel free to report some inefficiencies in the code! (It's just initial version so may have much room for adjustment)
