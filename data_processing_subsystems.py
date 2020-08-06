import pandas as pd
import stanza
import itertools as it
import re
from data_process import remove_urls, remove_tags, remove_punctuation, filter_noun_phrases, create_docs

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
    data = pd.read_csv("data/planilha_completa_4_e_5_subsistemas.csv", engine='python', encoding='iso-8859-1', sep=';')
    #For all_posts_facebook the below line is needed
    #data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

    # data = data.groupby(['PostID', 'Post']).agg({'Subsistema': list,
    #                      'TemaN1': list,
    #                      'TemaN2': list,
    #                      }).reset_index()

    # #Exclusive posts
    # data = data.groupby(['PostID', 'Post']).agg({'Subsistema': list,}).reset_index()
    #
    # #Post with more than 4 subsystems
    data = data.groupby(['PostID', 'Post']).agg({'Subsistema': list, 'num_subsistemas' : list,}).reset_index()
    #
    #PostId missing from Ana's file: {514, 515, 642, 645, 391, 288, 419, 429, 181, 445, 583, 206, 465, 211, 474, 859,
    # 477, 861, 481, 483, 740, 485, 102, 741, 871, 367, 502, 764}
    data = data_clean(data)

    # Stanza pipeline for word classification (pt-br)
    stopwords = get_stop_words('pt')
    nlp = stanza.Pipeline(lang='pt', processors='tokenize,mwt,pos,lemma')
    docs = data.Post.apply(lambda post: create_docs(post, nlp))

    # Filtering noun phrases
    data['np'] = docs.apply(lambda doc: filter_noun_phrases(doc, stopwords))

    #Drop null creted by the cleaning processing
    data = data[data.Post.isnull() != True]
    data = data[data.np.isnull() != True]

    # Save data with Subsitema, TemaN1 and TemaN2 aggreagated, and with noun-phrases for each post
    data.to_csv("data/planilha_completa_4_e_5_subsistemas_cleaned.csv", index=False)




