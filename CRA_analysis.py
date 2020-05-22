import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import os
import subprocess
import collections
import sys
import nltk

import stanza
import itertools as it
import re
import matplotlib.pyplot as plt
from matplotlib import pylab

from stop_words import get_stop_words
import networkx as nx
import math

import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.distributions.empirical_distribution import ECDF


def graph_plot(G):
    #%pylab inline
    #%config InlineBackend.figure_format = 'png'
    H = G.copy()
    plt.rc('figure', figsize=(12, 7))
    nodes = [x for x, y in H.nodes(data=True) if y['betweenness'] == 0.0]
    H.remove_nodes_from(nodes)
    node_size = [y['betweenness'] * 10000 for x, y in H.nodes(data=True)]
    pos = nx.spring_layout(H)
    nx.draw_networkx(H, pos, node_size=node_size, edge_color='y', alpha=.004, linewidths=0.00001)
    plt.savefig("graph.pdf")

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


def central_words(index):
    #index = nx.betweenness_centrality(G)
    sorted_index = sorted(index.items(), key=lambda x: x[1], reverse=True)

    # Top 10 noun phrases by betweenness centrality:
    for word, centr in sorted_index[:20]:
        print (word + " " + str(centr))

def simple_resonance(network_a, network_b):
    index_a = nx.get_node_attributes(network_a, 'betweenness').items()
    index_b = nx.get_node_attributes(network_b, 'betweenness').items()

    sorted_a = sorted(index_a, key=lambda x:x[1], reverse=True)
    sorted_b = sorted(index_b, key=lambda x:x[1], reverse=True)

    scores = [a[1]*b[1] for a, b in zip(sorted_a, sorted_b) if a[0] == b[0]]
    return sum(scores)

def standardized_sr(network_a, network_b):
    index_a = nx.get_node_attributes(network_a, 'betweenness').items()
    index_b = nx.get_node_attributes(network_b, 'betweenness').items()

    sum_a_squared = sum([centr**2 for word, centr in index_a])
    sum_b_squared = sum([centr**2 for word, centr in index_b])

    norm = math.sqrt((sum_a_squared * sum_b_squared))
    standardized = simple_resonance(network_a, network_a) / norm

    return standardized

def pair_influence(graph, betweenness='betweenness',
                   frequency='frequency', name='pair_i'):
    for u, v in graph.edges():
        index_u = graph.node[u][betweenness]
        index_v = graph.node[v][betweenness]
        score = index_u * index_v * graph[u][v][frequency]
        graph[u][v][name] = score

def pair_resonance(index_a, index_b):
    edges = set(index_a.keys()) & set(index_b.keys())
    pr_score = sum([index_a[edge] * index_b[edge] for edge in edges])
    return pr_score

def standardized_pr(index_a, index_b):
    a_sqrt = math.sqrt(sum([index_a[edge]**2 for edge in index_a]))
    b_sqrt = math.sqrt(sum([index_b[edge]**2 for edge in index_b]))
    standardized = pair_resonance(index_a, index_b) / (a_sqrt * b_sqrt)
    return standardized


if __name__ == '__main__':
    level = [4, 5]
    G = nx.read_gexf("data/facebook_network_level_" + str(level).replace(" ", "") + ".gexf")
    betweenneess = [y['betweenness'] for x, y in G.nodes(data=True)]
    freq = [z['frequency'] for x, y, z in G.edges.data()]

    #nodes with betweenness == 0.0
    H = G.copy()
    #nodes = [x for x, y in H.nodes(data=True) if y['betweenness'] == 0.0]
    #H.remove_nodes_from(nodes)
    remov_edge = [(x, y) for x, y, z in G.edges.data() if z['frequency'] < 50]
    H.remove_edges_from(remov_edge)
    H.remove_nodes_from(list(nx.isolates(H)))
    nx.write_gexf(H, 'data/freq_greater_than_5_facebook_network_level_[4,5].gexf')
    nx.write_gexf(G, 'data/facebook_network_level_[4,5].gexf')

    # finance_index = nx.get_node_attributes(G, 'betweenness').items()
    # food_index = nx.get_node_attributes(G, 'betweenness').items()
    #
    # print (simple_resonance(finance_index, food_index))
    # print (standardized_sr(finance_index, food_index))
    #
    # finance_iscore = nx.get_edge_attributes(G, 'pair_i')
    # food_iscore = nx.get_edge_attributes(G, 'pair_i')
    #
    # print(pair_resonance(finance_iscore, food_iscore))
    #
    # print(standardized_pr(finance_iscore, food_iscore))

