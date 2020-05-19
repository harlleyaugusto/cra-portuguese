#Clean the data
    #Group by post_id
    #Clean each group
    #Filter noun-phrase for each group
    #Create edges for each group
    #Create columns with all sub-systems

import pandas as pd
import stanza
import itertools as it
import re
from data_process import link_list_freq
from CRA import cra_centered_graph
import networkx as nx

def filter_post(data, filter):
    for f in filter:
        data = data[data[f].apply(lambda s: set(filter.get(f)).issubset(s))]
    return data

def create_network(data, experiment):
    #filtering
    for k in experiment:
        print("------------ Experiment:filter: " + str(k) + "---------------" )
        network = filter_post(data, experiment.get(k))
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

        nx.write_gexf(G, 'data/experiment' + str(k) + '.gexf')
        print("------------ Experiment:DONE!---------------")

        #print(type(experiment))
        #edges and frequency
        #save to the gexf file

if __name__ == '__main__':
    data = pd.read_csv("data/all_posts_facebook_cleaned.csv", engine='python')
    data.Subsistema = data['Subsistema'].apply(eval)
    data.TemaN1 = data['TemaN1'].apply(eval)
    data.TemaN2 = data['TemaN2'].apply(eval)
    #dropnull
    data = data[data.Post.isnull() != True]
    data = data[data.np.isnull() != True]
    data.np = data['np'].apply(eval)

    experiment = {1: {'Subsistema': ['INDIVÍDUO', 'MICROSSISTEMA'], 'TemaN1': ['PRAZER']}, 2: {'Subsistema' :['MICROSSISTEMA']}}
    create_network(data, experiment)
    #data.link = data.link.apply(eval_func)
