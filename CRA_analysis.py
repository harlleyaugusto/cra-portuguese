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


def central_words(index):
    #index = nx.betweenness_centrality(G)
    sorted_index = sorted(index.items(), key=lambda x: x[1], reverse=True)

    # Top 10 noun phrases by betweenness centrality:
    for word, centr in sorted_index[:20]:
        print (word + " " + str(centr))

def simple_resonance(index_a, index_b):
    sorted_a = sorted(index_a, key=lambda x:x[1], reverse=True)
    sorted_b = sorted(index_b, key=lambda x:x[1], reverse=True)
    scores = [a[1]*b[1] for a, b in zip(sorted_a, sorted_b) if a[0] == b[0]]
    return sum(scores)

def standardized_sr(index_a, index_b):
    sum_a_squared = sum([centr**2 for word, centr in index_a])
    sum_b_squared = sum([centr**2 for word, centr in index_b])
    norm = math.sqrt((sum_a_squared * sum_b_squared))
    standardized = simple_resonance(index_a, index_b) / norm
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
    G = nx.read_gexf("data/facebook_network.gexf")

    finance_index = nx.get_node_attributes(G, 'betweenness').items()
    food_index = nx.get_node_attributes(G, 'betweenness').items()

    print (simple_resonance(finance_index, food_index))
    print (standardized_sr(finance_index, food_index))

    finance_iscore = nx.get_edge_attributes(G, 'pair_i')
    food_iscore = nx.get_edge_attributes(G, 'pair_i')

    print(pair_resonance(finance_iscore, food_iscore))

    print(standardized_pr(finance_iscore, food_iscore))

