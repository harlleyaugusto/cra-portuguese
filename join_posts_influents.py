import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import pylab
import networkx as nx

if __name__ == '__main__':
    data = pd.read_csv("data/posts_facebook_latin.csv", encoding='iso-8859-1', sep=';')
    data_processed = pd.read_csv("data/posts_facebook_processed.csv")
    posts_influents = pd.read_csv("data/posts_mais_influentes.csv",  encoding='iso-8859-1', sep=';')

    data_merged = pd.merge(data, posts_influents, left_on='Texto', right_on='POST').drop(columns = ['POST']).rename(columns = {"Qtd Níveis" : "qtd_niveis"})
    data_merged = pd.merge(data_merged, posts_influents, left_on='Texto', right_on='POST')
    data_merged.drop(columns=['ID_x', 'Qtd Níveis_x', 'POST_x', 'POST_y'], inplace=True)
    data_merged.rename(columns={"ID_y": "ID", "Qtd Níveis_y": "qtd_niveis"}, inplace=True)