import pandas as pd
import stanza
import itertools as it
import re
from data_process import link_list_freq
from CRA import cra_centered_graph
import networkx as nx
import configparser
from CRA_analysis import simple_resonance, standardized_sr

def save_network(G, experiment_name, filter, folder = "data/experiments/"):
    nx.write_gexf(G, folder + experiment_name + "_" + filter +'.gexf')

def filter_post(data, filter):
    for f in filter:
        data = data[data[f].apply(lambda s: set(filter.get(f)).issubset(s))]
    return data

def create_network(data, network_filters, experiment_name):
    #filtering
    for k in network_filters:
        print("------------ Experiment:filter: " + str(k) + "---------------" )
        network = filter_post(data, network_filters.get(k))
        print(network[['Subsistema', 'TemaN1']])

        # Creating edges and its frequency
        freq_edges = {}
        network['link'] = network['np'].apply(lambda x: link_list_freq(x, freq_edges))

        # Concatenate post's edges into a single list of edges
        print("Starting edgelist...")
        edgelist = network.link.sum()
        print("Done!")
        print(edgelist)

        # Return a graph with node's betweenness and edges's frequency
        G = cra_centered_graph(edgelist, freq_edges)
        save_network(G, experiment_name, str(k))

        print("------------ Experiment " + experiment_name + ": DONE!---------------")

#def similarity_betw_network(similarity_measures, network_filters, experiment_name, folder = "data/experiments/"):


def run_experiment(data, exp_config):
    experiment_name = exp_config['EXPERIMENT']['name']
    network_filters = eval(exp_config['EXPERIMENT']['network_filters'])
    similarity_measures = eval(exp_config['EXPERIMENT']['similarity_measures'])

    create_network(data, network_filters, experiment_name)
    #run the comparison between two networks give a metric

if __name__ == '__main__':
    data = pd.read_csv("data/all_posts_facebook_cleaned.csv", engine='python')
    data.Subsistema = data['Subsistema'].apply(eval)
    data.TemaN1 = data['TemaN1'].apply(eval)
    data.TemaN2 = data['TemaN2'].apply(eval)
    data.np = data['np'].apply(eval)

    #dropnull
    #data = data[data.Post.isnull() != True]
    #data = data[data.np.isnull() != True]

    #experiment = {1: {'Subsistema': ['INDIVÍDUO', 'MICROSSISTEMA'], 'TemaN1': ['PRAZER']}, 2: {'Subsistema' :['MICROSSISTEMA']}}
    exp_config = configparser.ConfigParser()
    exp_config.read("experiments/experiment1.ini")

    run_experiment(data, exp_config)
