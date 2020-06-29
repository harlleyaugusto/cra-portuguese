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

def filter_post(data, filter):
    for f in filter:
        data = data[data[f].apply(lambda s: set(filter.get(f)).issubset(s))]
    return data.copy()

def create_network(data, networks, experiment_name, folder):
    #filtering
    for k in networks:
        print("------------ Experiment:filter: " + str(k) + "---------------" )
        network = filter_post(data, networks.get(k))

        # Creating edges and its frequency
        freq_edges = {}
        network['link'] = network['np'].apply(lambda x: link_list_freq(x, freq_edges))

        # Concatenate post's edges into a single list of edges
        print("Starting edgelist...")
        edgelist = network.link.sum()
        print("Done!")

        # Return a graph with node's betweenness and edges's frequency
        G = cra_centered_graph(edgelist, freq_edges)

        # Save the network as .gexf file
        save_network(G, experiment_name, str(k), folder)

        network = None

def resonance(similarity_measures, networks, experiment_name, folder = "data/experiments/"):

    networks_keys = list(networks.keys())
    res = {}
    for i in range(networks_keys.__len__()):
        net_1 = nx.read_gexf(folder + experiment_name + "/" + experiment_name + "_" + str(networks_keys[i]) + ".gexf")
        for j in range(i + 1, networks_keys.__len__()):
            net_2 = nx.read_gexf(folder + experiment_name + "/" + experiment_name + "_" + str(networks_keys[j]) + ".gexf")
            for sm in similarity_measures:
                print("calculating...: " + sm + " " + networks_keys[i] + " - " + networks_keys[j])
                r = eval(sm)(net_1, net_2)
                print("Done: " + str(r))
                if sm not in res:
                    res[sm] = {}
                    if networks_keys[i] not in res[sm]:
                        res[sm][networks_keys[i]] = {}
                        res[sm][networks_keys[i]][networks_keys[j]] = r
                    else:
                        res[sm][networks_keys[i]][networks_keys[j]] = r
                else:
                    if networks_keys[i] not in res[sm]:
                        res[sm][networks_keys[i]] = {}
                        res[sm][networks_keys[i]][networks_keys[j]] = r
                    else:
                        res[sm][networks_keys[i]][networks_keys[j]] = r
    return res



def run_experiment(data, exp_config):
    '''
    Orchestrates all the experiments (network generation, metrics and report) set-up in exp_config.

    :param data: data already processed
    :param exp_config: experiment setup
    '''

    experiment_name = exp_config['EXPERIMENT']['name']
    networks = eval(exp_config['EXPERIMENT']['networks'])
    folder = exp_config['EXPERIMENT']['folder']
    generate_network = eval(exp_config['EXPERIMENT']['generate_network'])
    create_folder_exp(folder, experiment_name)

    #Creates all the networks, if it was not created
    if(generate_network):
        create_network(data, networks, experiment_name, folder)

    #Exports network info in a week level
    if (exp_config.has_section('REPORTING')):
        if (eval(exp_config['REPORTING']['word_level'])):
            word_level(exp_config)

    #Computes all metrics for each pair of network
    if(exp_config.has_section('RESONANCE')):
        similarity_measures = eval(exp_config['RESONANCE']['resonance_measures'])
        res = resonance(similarity_measures, networks, experiment_name, folder)
        report_resonace(res, exp_config)


if __name__ == '__main__':
    #Reading the data already processed to create the networks
    data = pd.read_csv("data/all_posts_facebook_cleaned.csv", engine='python')

    #Transforming data as string into list
    data.Subsistema = data['Subsistema'].apply(eval)
    data.TemaN1 = data['TemaN1'].apply(eval)
    data.TemaN2 = data['TemaN2'].apply(eval)
    data.np = data['np'].apply(eval)

    #Reading the experiment configurantion
    exp_config = configparser.ConfigParser()
    exp_config.read("experiments/experiment1.ini")

    run_experiment(data, exp_config)


