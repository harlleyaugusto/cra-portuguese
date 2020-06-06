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
from report import word_level

def save_network(G, experiment_name, filter, folder = "data/experiments/"):
    nx.write_gexf(G, folder + experiment_name + "/" + experiment_name + "_" + filter +'.gexf')

def filter_post(data, filter):
    for f in filter:
        data = data[data[f].apply(lambda s: set(filter.get(f)).issubset(s))]
    return data.copy()

def create_network(data, networks, experiment_name, folder, report):
    #filtering
    for k in networks:
        print("------------ Experiment:filter: " + str(k) + "---------------" )
        network = filter_post(data, networks.get(k))

        # Creating edges and its frequency
        freq_edges = {}
        network['link'] = network['np'].apply(lambda x: link_list_freq(x, freq_edges))
        #print(freq_edges)

        # Concatenate post's edges into a single list of edges
        print("Starting edgelist...")
        edgelist = network.link.sum()
        print("Done!")

        # Return a graph with node's betweenness and edges's frequency
        G = cra_centered_graph(edgelist, freq_edges)

        save_network(G, experiment_name, str(k), folder)

        network = None

def resonance(similarity_measures, networks, experiment_name, folder = "data/experiments/"):
    comp = list(networks.keys())
    res = {}
    for i in range(comp.__len__()):
        net_1 = nx.read_gexf(folder + experiment_name + "/" + experiment_name + "_" + str(comp[i]) + ".gexf")
        for j in range(i + 1, comp.__len__()):
            net_2 = nx.read_gexf(folder + experiment_name + "/" + experiment_name + "_" + str(comp[j]) + ".gexf")
            for sm in similarity_measures:
                print("calculating...: " + sm + " " + comp[i] + " - " + comp[j])
                r = eval(sm)(net_1, net_2)
                print("Done: " + str(r))
                if sm not in res:
                    res[sm] = {}
                    if comp[i] not in res[sm]:
                        res[sm][comp[i]] = {}
                        res[sm][comp[i]][comp[j]] = r
                    else:
                        res[sm][comp[i]][comp[j]] = r
                else:
                    if comp[i] not in res[sm]:
                        res[sm][comp[i]] = {}
                        res[sm][comp[i]][comp[j]] = r
                    else:
                        res[sm][comp[i]][comp[j]] = r
    return res

def create_folder_exp(folder, experiment_name):
    if not os.path.exists(folder+experiment_name):
        os.mkdir(folder+experiment_name)
        print("Directory ", folder+experiment_name, " Created ")
    else:
        print("Directory ", folder+experiment_name, " already exists")

    if not os.path.exists(folder + experiment_name + "csv/"):
        os.mkdir(folder+experiment_name)
        print("Directory ", folder + experiment_name + "csv/", " Created ")
    else:
        print("Directory ", folder + experiment_name + "csv/", " already exists")

def run_experiment(data, exp_config):
    experiment_name = exp_config['EXPERIMENT']['name']
    networks = eval(exp_config['EXPERIMENT']['networks'])
    folder = exp_config['EXPERIMENT']['folder']
    generate_network = eval(exp_config['EXPERIMENT']['generate_network'])
    create_folder_exp(folder, experiment_name)

    if(generate_network):
        create_network(data, networks, experiment_name, folder, report)

    if (exp_config.has_section('REPORTING')):
        if (eval(exp_config['REPORTING']['word_level'])):
            word_level(exp_config)

    if(exp_config.has_section('RESONANCE')):
        similarity_measures = eval(exp_config['RESONANCE']['resonance_measures'])
        res = resonance(similarity_measures, networks, experiment_name, folder)
        report_resonace(res, exp_config)


if __name__ == '__main__':
    data = pd.read_csv("data/all_posts_facebook_cleaned.csv", engine='python')
    data.Subsistema = data['Subsistema'].apply(eval)
    data.TemaN1 = data['TemaN1'].apply(eval)
    data.TemaN2 = data['TemaN2'].apply(eval)
    data.np = data['np'].apply(eval)

    exp_config = configparser.ConfigParser()
    exp_config.read("experiments/experiment1.ini")

    #networks = eval(exp_config['EXPERIMENT']['networks'])
    #network = filter_post(data, networks.get("net2"))
    #freq_edges = {}
    #network['link'] = network['np'].apply(lambda x: link_list_freq(x, freq_edges))

    #resonance(eval(exp_config['RESONANCE']['resonance_measures']), eval(exp_config['EXPERIMENT']['networks']), exp_config['EXPERIMENT']['name'])

    run_experiment(data, exp_config)


