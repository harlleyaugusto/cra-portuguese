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
import configparser

from stop_words import get_stop_words
import networkx as nx
import math

import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.distributions.empirical_distribution import ECDF


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
    standardized = simple_resonance(network_a, network_b) / norm

    return standardized

def pair_influence(graph, betweenness='betweenness',
                   frequency='frequency', name='pair_i'):
    for u, v in graph.edges():
        index_u = graph.nodes[u][betweenness]
        index_v = graph.nodes[v][betweenness]
        score = index_u * index_v * graph[u][v][frequency]
        graph[u][v][name] = score

def pair_resonance(network_a, network_b):
    if(not nx.get_edge_attributes(network_a, 'pair_i')):
        pair_influence(network_a)
        index_a = nx.get_edge_attributes(network_a, 'pair_i')
    else:
        index_a = nx.get_edge_attributes(network_a, 'pair_i')

    if (not nx.get_edge_attributes(network_b, 'pair_i')):
        pair_influence(network_b)
        index_b = nx.get_edge_attributes(network_b, 'pair_i')
    else:
        index_b = nx.get_edge_attributes(network_b, 'pair_i')

    edges = set(index_a.keys()) & set(index_b.keys())
    pr_score = sum([index_a[edge] * index_b[edge] for edge in edges])
    return pr_score

def standardized_pr(network_a, network_b):
    if(not nx.get_edge_attributes(network_a, 'pair_i')):
        pair_influence(network_a)
        index_a = nx.get_edge_attributes(network_a, 'pair_i')
    else:
        index_a = nx.get_edge_attributes(network_a, 'pair_i')

    if (not nx.get_edge_attributes(network_b, 'pair_i')):
        pair_influence(network_b)
        index_b = nx.get_edge_attributes(network_b, 'pair_i')
    else:
        index_b = nx.get_edge_attributes(network_b, 'pair_i')

    a_sqrt = math.sqrt(sum([index_a[edge]**2 for edge in index_a]))
    b_sqrt = math.sqrt(sum([index_b[edge]**2 for edge in index_b]))
    standardized = pair_resonance(network_a, network_b) / (a_sqrt * b_sqrt)
    return standardized


if __name__ == '__main__':
    # level = [4, 5]
    # G = nx.read_gexf("data/facebook_network_level_" + str(level).replace(" ", "") + ".gexf")
    # betweenneess = [y['betweenness'] for x, y in G.nodes(data=True)]
    # freq = [z['frequency'] for x, y, z in G.edges.data()]
    #
    # #nodes with betweenness == 0.0
    # H = G.copy()
    # #nodes = [x for x, y in H.nodes(data=True) if y['betweenness'] == 0.0]
    # #H.remove_nodes_from(nodes)
    # remov_edge = [(x, y) for x, y, z in G.edges.data() if z['frequency'] < 50]
    # H.remove_edges_from(remov_edge)
    # H.remove_nodes_from(list(nx.isolates(H)))
    # nx.write_gexf(H, 'data/freq_greater_than_5_facebook_network_level_[4,5].gexf')
    # nx.write_gexf(G, 'data/facebook_network_level_[4,5].gexf')

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

    exp_config = configparser.ConfigParser()
    exp_config.read("experiments/visualizacao_post_exclusivo.ini")
    experiment_name = exp_config['EXPERIMENT']['name']
    networks = eval(exp_config['EXPERIMENT']['networks'])
    folder = exp_config['EXPERIMENT']['folder']
    networks_keys = list(networks.keys())
    for i in range(networks_keys.__len__()):
        net_1 = nx.read_gexf(folder + experiment_name + "/" + experiment_name + "_" + str(networks_keys[i]) + ".gexf")
        for j in range(i + 1, networks_keys.__len__()):
            net_2 = nx.read_gexf(
                folder + experiment_name + "/" + experiment_name + "_" + str(networks_keys[j]) + ".gexf")
            print(simple_resonance(net_1, net_2))
