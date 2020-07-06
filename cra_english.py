from nltk.corpus import reuters
from nltk.corpus import stopwords
import re
import itertools as it
import nltk
import networkx as nx
import math
def cra_centered_graph(doc, tags='NN*|JJ*'):
    tagged_doc = [nltk.pos_tag(sentence) for sentence in doc]
    noun_phrases = [[token.lower() for token, tag in sent if re.match(tags, tag)]
                    for sent in tagged_doc]
    edgelist = [edge for phrase in noun_phrases for edge in it.combinations(phrase, 2)]
    graph = nx.Graph()
    for edge in set(edgelist):
        graph.add_edge(*edge, frequency=edgelist.count(edge))

    betweenness = nx.betweenness_centrality(graph)
    for n in graph:
        graph.nodes[n]['betweenness'] = betweenness[n]

    return graph

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

if __name__ == '__main__':
    stopwords = stopwords.words() + ['.', ',', '"', "'", '-', '.-']
    first_doc = reuters.sents(reuters.fileids()[0])
    stopd_sents = [[token.lower() for token in sent if token.lower() not in stopwords]
                   for sent in first_doc]

    for token in stopd_sents[0]:
        print(token)

    tagged_sents = [nltk.pos_tag(sentence) for sentence in stopd_sents]

    for token, tag in tagged_sents[0]:
        if re.match(r'NN*|JJ*', tag):
            print(token, tag)

    noun_phrases = [[token for token, tag in sent if re.match(r'NN*|JJ*', tag)]
                    for sent in tagged_sents]

    edgelist = [edge for phrase in noun_phrases for edge in it.combinations(phrase, 2)]

    finance = ['income', 'trade', 'money-supply']
    food = ['sugar', 'wheat', 'rice', 'coffee']

    finance_docs = reuters.sents(categories=finance)
    food_docs = reuters.sents(categories=food)

    finance_stopd = [[token.lower() for token in sent if token.lower() not in stopwords]
                     for sent in finance_docs]
    food_stopd = [[token.lower() for token in sent if token.lower() not in stopwords]
                  for sent in food_docs]

    finance_net = cra_centered_graph(finance_stopd)
    food_net = cra_centered_graph(food_stopd)