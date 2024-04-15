def order_and_flatten_nodes(node_features):
    # Order nodes by y-coordinate, then by x-coordinate
    ordered_nodes = node_features.sort_values(by=['longitude', 'latitude'])

    # Flatten the sequence of coordinates
    Cseq = ordered_nodes.values.flatten()
    # print(Cseq[:10])
    # print(Cseq[-10:])
    return Cseq

# Rest of the script (like reading the node features, etc.) goes here
