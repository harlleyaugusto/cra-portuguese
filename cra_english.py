from nltk.corpus import reuters
from nltk.corpus import stopwords
import re
import itertools as it
import nltk
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

