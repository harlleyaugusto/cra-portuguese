import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import os
import subprocess
import collections
import sys
import spacy

from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree

def extract_phrase(tree_str, label):
    phrases = []
    trees = Tree.fromstring(tree_str)
    for tree in trees:
        for subtree in tree.subtrees():
            if subtree.label() == label:
                t = subtree
                t = ' '.join(t.leaves())
                phrases.append(t)

    return phrases

if __name__ == '__main__':
    #data = pd.read_csv("facebook_processed.csv", engine = 'python')
    #nlp = spacy.load("pt_core_news_sm")
    #nlp = spacy.load("en_core_web_sm")

    #doc = nlp("My name is Harlley")

    #for chunk in doc.noun_chunks:
    #    print(chunk.text)

    sentence = "(ROOT(S(S(VP(V É)(A necessário)) (NP(NP(REL que)) (NP(PRS você)))) (S(CONJ se)(S(VP(V apresente) (NP(N' (N ao) (N serviço) (N amanhã.))))))))"

    nps = extract_phrase(sentence, "NP")

    sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
    raw_text = machado.raw('romance/marm05.txt')
    sentences = sent_tokenizer.tokenize(raw_text)
    #for sent in sentences[1000:1005]: