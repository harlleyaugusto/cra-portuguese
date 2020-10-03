import pandas as pd
import stanza
import itertools as it
import re
from data_process import link_list_freq
from CRA import cra_centered_graph
import networkx as nx
import configparser
from resonances import simple_resonance, standardized_sr, pair_resonance, standardized_pr
import os
import csv
from report import word_level, report_resonace, save_network, create_folder_exp

def network_cut_att(G,threshold, att):
    network_sorted = sorted(G.nodes(data=True), key=lambda x: x[1][att], reverse = True)
    network_greater = network_sorted[threshold:network_sorted.__len__()]
    nodes_removed = [node[0] for node in network_greater]
    G.remove_nodes_from(nodes_removed)
    return G

def remove_dumb(G, dumb_list):
    dumb_list = list(dumb_list['node'])
    G.remove_nodes_from(dumb_list)
    return G

def create_visualization(exp_config):
    visualization_path = exp_config['EXPERIMENT']['folder']
    networks = eval(exp_config['EXPERIMENT']['networks'])
    cut = int(exp_config['EXPERIMENT']['cut'])
    att_cut = exp_config['EXPERIMENT']['att_cut']
    dumb_word = eval(exp_config['EXPERIMENT']['dumb_word'])
    for network_name in networks:
        experiment_name = exp_config['EXPERIMENT']['name'] + "_" + network_name
        G = nx.read_gexf(visualization_path + experiment_name + ".gexf")
        G = network_cut_att(G, cut, att_cut)
        if(dumb_word):
            dumb_list_path = exp_config['EXPERIMENT']['dumb_list_path']
            dumb_list = pd.read_csv(dumb_list_path, engine='python', encoding='iso-8859-1')
            dumb_list = dumb_list[dumb_list['Subsistema'] == network_name].copy()
            G = remove_dumb(G, dumb_list)


        print(G.number_of_nodes())
        create_folder_exp(visualization_path, "visualization")
        nx.write_gexf(G, visualization_path + "visualization/" + experiment_name + "_" + network_name + '.gexf')

if __name__ == '__main__':
    exp_config = configparser.ConfigParser()

    exp_config.read("visualization/visualizacao_post_exclusivo.ini")
    create_visualization(exp_config)

    exp_config.read("visualization/visualizacao_individuo_vs_todos.ini")
    create_visualization(exp_config)

    exp_config.read("visualization/visualizacao_post_4_5_subsistema.ini")
    create_visualization(exp_config)

