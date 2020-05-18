import pandas as pd
import stanza
import itertools as it
import re
from data_process import remove_urls, remove_tags, remove_punctuation

from stop_words import get_stop_words
import string

def data_clean(data):
    # Data cleaning
    data.Post = data.Post.apply(remove_urls)
    data.Post = data.Post.apply(remove_tags)
    data.Post = data.Post.apply(remove_punctuation)
    return data

if __name__ == '__main__':
    #Raw data loading
    data = pd.read_csv("data/post_para_CRA_subsistemas.csv", engine='python', encoding='iso-8859-1', sep=';')
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

    data = data.groupby(['PostID', 'Post']).agg({'Subsistema': list,
                         'TemaN1': list,
                         'TemaN2': list,
                         }).reset_index()

    #items missing from Ana's file: {514, 515, 642, 645, 391, 288, 419, 429, 181, 445, 583, 206, 465, 211, 474, 859,
    # 477, 861, 481, 483, 740, 485, 102, 741, 871, 367, 502, 764}
    data = data_clean(data)



