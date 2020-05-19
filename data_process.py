import pandas as pd
import stanza
import itertools as it
import re

from stop_words import get_stop_words
import string

def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text = url_pattern.sub(r'', text)
    return text.strip()

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation)).strip()

def remove_tags(text):
    splits = []
    text = text.lstrip().rstrip("\n")
    print(text)
    if text.startswith("["):
        splits = list(map(str.lstrip, re.split(r"(])(\s*)([^[|\s+])", text, 1)))
        text = splits[splits.__len__()-2].lstrip() + splits[splits.__len__()-1].lstrip()
    elif(text.startswith("{")):
        splits = text.split("{")
        text = splits[splits.__len__() - 1]
        text = re.split(r"\s+", text, 1)[1]
    elif re.match(r"[^\(]*[+\)]", text) is not None:
        text = re.split(r"[^\(]*[+\)]", text, 1)[1].lstrip()

    return text.lower()

def filter_noun_phrases(doc, stopwords):
    noun_phrases = None
    if doc is not None:
        noun_phrases = [[str.lower(word.lemma) for word in sent.words if str.lower(word.lemma) not in stopwords and
                     (word.upos == 'NOUN' or word.upos == 'ADJ' or word.upos == 'PROPN')] for sent in doc.sentences]
    return noun_phrases

def link_list(noun_phrases):
    edgelist = None
    if noun_phrases is not None:
        edgelist = [edge for phrase in noun_phrases for edge in it.combinations(phrase, 2)]
    return edgelist

def link_list_freq(noun_phrases, freq_edges):
    edgelist = []
    if noun_phrases is not None:
        for phrase in noun_phrases:
            for edge in it.combinations(phrase, 2):
                edgelist.append(edge)
                if edge in freq_edges:
                    freq_edges[edge] = freq_edges[edge] + 1
                else:
                    freq_edges[edge] = 1
    return edgelist

#Apply nlp to get nlp features for each string
def create_docs(str, nlp):
    print(str)
    if(str is not None and str != ''):
        return nlp(str)
    else: return None

if __name__ == '__main__':
    #Raw data loading
    data = pd.read_csv("data/posts_facebook_latin.csv", engine='python', encoding='iso-8859-1', sep=';')
    #Post influents: levels [1...5]
    posts_influents = pd.read_csv("data/posts_mais_influentes.csv", encoding='iso-8859-1', sep=';')

    #Jois raw data with influents posts to get the level column
    data = pd.merge(data, posts_influents, left_on='Texto', right_on='POST').drop(columns=['POST']).rename(
        columns={"Qtd Níveis": "qtd_niveis"})

    #Filtering posts by level
    level = [4, 5]
    data = data[data.qtd_niveis.isin(level)]

    #Data cleaning
    data.Texto = data.Texto.apply(remove_urls)
    data.Texto = data.Texto.apply(remove_tags)
    data.Texto = data.Texto.apply(remove_punctuation)

    #Stanza pipeline for word classification (pt-br)
    stopwords = get_stop_words('pt')
    nlp = stanza.Pipeline(lang='pt', processors='tokenize,mwt,pos,lemma')
    docs = data.Texto.apply(create_docs)

    #Filtering noun phrases
    data['np'] = docs.apply(lambda doc : filter_noun_phrases(doc, stopwords))

    #Creating edges and its frequency
    freq_edges = {}
    data['link'] = data['np'].apply(lambda x: link_list_freq(x, freq_edges))

    #Save the network with posts in level[1...5]
    data.to_csv("data/posts_facebook_processed_level_" + str(level).replace(" ", "") + ".csv", index=False)

    #Save the frequency of each edges
    freq_edges = pd.DataFrame.from_dict(freq_edges, orient= "index")
    freq_edges.to_csv("data/freq_edges_level_" + str(level).replace(" ", "") + ".csv")