
# Introduction

This repository contains code for the research case study conducted on building model to generate synthetic street network. The research for the project is inspired by the [paper](https://arxiv.org/abs/2211.04984) Graph representation learning for street networks 

### Note on docker files

* The docker files are provided for the following components:
    * Data gathering
    * 0node
    * node2vec
* The transformer model requires a GPU to train, so a docker file is not provided for it. Since, this disrupts the flow of execution to put all the details in one place, the docker files were seperated for the other components which also enables the user to run the components individually if necessary for testing since the data is already provided in the repository.

### Note on Time taken for execution

* The data gathering process involves extracting data from around 40000 cities around the world. This process takes anywhere from few hours to few days depending on the speed of the internet. 
* The transformer model was trained on a NVIDIA A100 GPU with 40GB memory rented from a cloud service for 40 hours.
* The node2vec model involves training the model on the data too which again might take a while depending on if it's run on a GPU or CPU.

# Data gathering

## Automate with docker:
* docker build -t rcs_data_extract -f Dockerfile.dataextract .
* docker run -v $(pwd):/app rcs_data_extract

(or)

## Flow to run
* Countries.csv contains the list of countries for which the data is to be extracted
*  python collect_cities.py: Collects the data from OpenStreetMap API and stores it in the cities folder
* python data_1sqkm_from_centre: Extracts data from the centroid of the city with a radius of 1sqkm

# 0node 

## Automate with docker:

* docker build -t rcs_0node -f Dockerfile.0node .
* docker run -v $(pwd):/app rcs_0node

(or)

## Flow to run
* python 0node.py: processes the street data, creates the graph and the master cseq file
* python split_cseq_data.py: splits the cseq data for training and testing 
* python seperate_testdata.py: seperates test data files correspoinding to the cseq test files from original street network data 


# Training transformer

* the transformer implementation was derived from the following repository: https://github.com/karpathy/nanoGPT/tree/master?tab=readme-ov-file 
* the transformer is trained on the cseq file containing the training data present in nanoGPT/data/osm/cseq.txt
* the model was trained on a NVDIA A100 GPU with 40GB memory rented from a cloud service for 40 hours for 20000 iterations and with a context length of 1024
** the loss obtained was ~0.4

## Flow to run
* install the dependecies: pip install torch numpy transformers datasets tiktoken wandb tqdm
* prepare the data: python nanoGPT/data/osm/prepare_data.py
* the configuration of the model is provided in nanoGPT/config/train_osm.py
* train the model: python nanoGPT/train.py --config nanoGPT/config/train_osm.py
* the weights are stored in nanoGPT/out-osm-1024-20000
* get the cseq predictions: python get_cseq_predictions.py

## Note
* a docker file is not provided for the transformer training as it requires a GPU to train the model and to get the predictions and we do not have access to a GPU to test.

# node2vec

The node2vec part in this repository implements node2vec by Grover, Aditya and Leskovec, Jure. For details of the model, refer to their original [implementation](https://github.com/aditya-grover/node2vec/tree/master) and [their paper](https://arxiv.org/pdf/1607.00653).

## Automate with docker:

* docker build -t rcs_node2vec -f Dockerfile.node2vec .
* docker run -v $(pwd):/app rcs_node2vec

(or)

## Flow to run

* Specify your arguments in `args.py`: you can change dataset and other arguments there
* node2vec/Preprocessing:
- Create .edgelist with node2vec/Preprocessing/edgelist.py as input for node2vec model
- Create real adjacency matrix node2vec/Preprocessing/realadjmatrix.py for creating real map after
* node2vec/main:
- Take .edgelist created above as input, run it in node2vec/main/main.py to create node embedidng .emb
- Create reconstructed adjacency matrix with node2vec/main/admatrix.py from input .emb 
* node2vec/plotncalculation:

- **plotmap.py**: Uses a file from Cseq_predicted and a file from Reconstructed_admatrix for one city to create a synthetic street network.
- **calculation.py**: Executes calculation of features from given input. Required input consists of files in two folders: `Cseq_predicted_subset` (Cseq_predicted) and `syn_admatrix_subset` (Test_dataset_synadjmatrix) to calculate for synthetic map OR `Cseq_test_subset` (Cseq_Data_Test) and `real_admatrix_subset` (Test_Dataset_realadjmatrix) for calculating features from a real map. All input files are in .csv format. Users can choose one of the following options for feature calculation:
  1. Average street length
  2. Average edges per node
  3. Average circuity
  4. Average form factor
  5. Average block size
  6. Average compactness
- **filter.py**: Given pairs of synthetic and real feature results, syncs them so that both files have the same pair of cities.
- **removespace.py**: Executes this file to create the correct format for input files to run in plotchart.py.
- **plotchart.py**: Plots the result from synthetic and real feature files.
  


# Related data files
* Real_admatrix data folder contains real adjacency matrix in format .csv.
* Test_dataset_Emb data folder contains node embedding in format .emb.
* Reconstructed_admatrix data folder contains reconstructed adjacency matrix in format .csv.

# Note
* Per-epoch training time is a bit slower than the original implementation.


* Feel free to report some inefficiencies in the code! (It's just initial version so may have much room for adjustment)
