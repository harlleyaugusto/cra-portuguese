import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import pylab
import networkx as nx



def graph_plot(G, index):
    #index = nx.betweenness_centrality(G)
    #%pylab inline
    #%config InlineBackend.figure_format = 'png'
    H = G
    plt.rc('figure', figsize=(12, 7))
    H.remove_nodes_from([n for n in index if index[n] == .0])
    node_size = [index[n] * 10000 for n in H]
    pos = nx.spring_layout(H)
    nx.draw_networkx(H, pos, node_size=node_size, edge_color='y', alpha=.4, linewidths=0)

def save_graph(G, index):
    #index = nx.betweenness_centrality(G)

    G.remove_nodes_from([n for n in index if index[n] == .0])
    node_size = [index[n] * 10000 for n in G]
    pos = nx.spring_layout(G)

    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    nx.draw_networkx_nodes(G,pos, node_size=2.6)
    nx.draw_networkx_edges(G,pos, width = 0.3)

   # cut = 1.00
   # xmax = cut * max(xx for xx, yy in pos.values())
   # ymax = cut * max(yy for xx, yy in pos.values())
   # plt.xlim(0, xmax)
   # plt.ylim(0, ymax)

    plt.savefig("rede",bbox_inches="tight")
    pylab.close()

def eval_func(str):
    if str is not None:
        return eval(str)
    else:
        return None

def cra_network(edgelist):
    graph = nx.Graph(edgelist)
    return graph

def update_freq(G ,edgelist, freq_edges):
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
            freq = freq + freq_edges[str((edge[1], edge[0]))]

        G.edges[edge]['frequency'] = freq

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

        graph.add_edge(*edge, frequency=freq)#edgelist.count(edge))

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

def pair_influence(graph, betweenness='betweenness',
                   frequency='frequency', name='pair_i'):

    i = 0
    for u, v in graph.edges():
        i = i +1
        print("Setting pair_influence: " + str(i) + "/" + str(graph.number_of_edges()))
        index_u = graph.nodes[u][betweenness]
        index_v = graph.nodes[v][betweenness]
        score = index_u * index_v * graph[u][v][frequency]
        graph[u][v][name] = score

if __name__ == '__main__':
    data = pd.read_csv("data/posts_facebook_processed.csv")
    data = data[data.link.isnull() != True]
    data.link = data.link.apply(eval_func)
    data = data[data.link.apply(len) != 0]

    print("Starting edgelist...")
    edgelist = data.link.sum()
    print("Done!")

    freq_edges = pd.read_csv("data/freq_edges.csv", index_col = 0).to_dict()["0"]

    G = cra_centered_graph(edgelist, freq_edges)

    pair_influence(G)

    ## To store the data:
    nx.write_gexf(G, 'data/facebook_network.gexf')