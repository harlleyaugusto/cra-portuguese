import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import pylab
import networkx as nx
import numpy as np

def eval_func(str):
    if str is not None:
        return eval(str)
    else:
        return None

def cra_network(edgelist):
    graph = nx.Graph(edgelist)
    return graph

def cra_centered_graph(edgelist, freq_edges):
    graph = nx.Graph()
    set_edgelistset = set(edgelist)
    set_size = set_edgelistset.__len__()
    i = 0
    for edge in set_edgelistset:
        i = i + 1
        print("Frequency calculation: " + str(i) + "/" + str(set_size))
        freq = 0
        if str(edge) in freq_edges:
            freq = freq_edges[str(edge)]
        if str((edge[1], edge[0])) in freq_edges:
            freq = freq +  freq_edges[str((edge[1], edge[0]))]

        graph.add_edge(*edge, frequency=freq)

    print("betweenness_centrality calculation...")
    betweenness = nx.betweenness_centrality(graph)
    print("Done!")

    print("Set betweenness_centrality...")
    i = 0
    nodes_size = graph.number_of_nodes()
    for n in graph:
        i = i + 1
        print("Setting betweenness: " + str(i) + "/" + str(nodes_size))
        graph.nodes[n]['betweenness'] = betweenness[n]

    print("Done!")
    return graph

if __name__ == '__main__':
    #Load the preprocessed data
    data = pd.read_csv("data/posts_facebook_processed_level_[4,5].csv")

    #Data cleaning
    data = data[data.link.isnull() != True]
    data.link = data.link.apply(eval_func)
    data = data[data.link.apply(len) != 0]

    #Concatenate post's edges into a single list of edges
    print("Starting edgelist...")
    edgelist = data.link.sum()
    print("Done!")

    #Reading the edge frequency for the data processed file loaded
    freq_edges = pd.read_csv("data/freq_edges_level_[4,5].csv", index_col = 0).to_dict()["0"]

    #Return a graph with node's betweenness and edges's frequency
    G = cra_centered_graph(edgelist, freq_edges)

    #Save the CRA network with betweness and frequency:
    nx.write_gexf(G, 'data/facebook_network_level_[4,5].gexf')