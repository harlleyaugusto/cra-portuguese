import pandas as pd
import stanza
import itertools as it
import re
from data_process import link_list_freq
from CRA import cra_centered_graph
import networkx as nx
import configparser
from CRA_analysis import simple_resonance, standardized_sr, pair_resonance, standardized_pr
import os
import csv

def word_level(exp_config):
    experiment_name = exp_config['EXPERIMENT']['name']
    networks = eval(exp_config['EXPERIMENT']['networks'])
    folder = exp_config['EXPERIMENT']['folder']
    for network in networks.keys():
        G = nx.read_gexf(folder + experiment_name + "/" + experiment_name + "_" + str(network) + ".gexf")
        with open(folder + experiment_name + "/" + "csv/" + network + ".csv", mode='w') as network_file:
            network_writer = csv.writer(network_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for node in list(G.nodes(data = True)):
                network_writer.writerow([node[0], node[1]['betweenness'], G.degre[node[0]]])

def report_resonace(res, exp_config):
    experiment_name = exp_config['EXPERIMENT']['name']
    networks = eval(exp_config['EXPERIMENT']['networks'])
    folder = exp_config['EXPERIMENT']['folder']

    for metric in res.keys():
        f = open(folder + experiment_name + "/" + metric + ".txt", "w")
        for net1 in res[metric]:
            for net2 in res[metric][net1]:
                f.write(net1 + " " + net2 + ": " +str(res[metric][net1][net2]) + "\n")

if __name__ == '__main__':
    exp_config = configparser.ConfigParser()
    exp_config.read("experiments/experiment1.ini")

    res = {}
    res['pair_1']= {}
    res['pair_1']['net1'] = {}
    res['pair_1']['net1']['net2'] = 1.2
    res['pair_1']['net1']['net3'] = 1.3

    res['pair_1']['net2'] = {}
    res['pair_1']['net2']['net3'] = 2.3

    res['pair_2'] = {}
    res['pair_2']['net1'] = {}
    res['pair_2']['net1']['net2'] = 1.2
    res['pair_2']['net1']['net3'] = 1.3

    res['pair_2']['net2'] = {}
    res['pair_2']['net2']['net3'] = 2.3

    report_resonace(res, exp_config)
