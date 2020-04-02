import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import os
import subprocess
import collections
import sys
import nltk

def file_creator(path, id, text):
    f = open(path + str(id) + ".txt", "w+", encoding = sys.stdout.encoding)
    f.write(text)
    f.close()


def parser(io, out):
    output = {}

    script_line = "java -Xmx3000m -cp Parser/stanford-parser-2010-11-30/stanford-parser.jar " \
                  "edu.stanford.nlp.parser.lexparser.LexicalizedParser -tokenized -sentences newline -outputFormat oneline " \
                  "-uwModel edu.stanford.nlp.parser.lexparser.BaseUnknownWordModel " \
                  "-MAX_ITEMS 500000 Parser/cintil.ser.gz "

    for f in os.listdir(io):
        #token = subprocess.check_output(script_line + io + f + " > " + out + "parsed_" + f.split("_")[0] + ".txt", shell=True, encoding=sys.stdout.encoding).lstrip()
        token = subprocess.check_output(script_line + io + f, shell=True, encoding=sys.stdout.encoding).lstrip().rstrip("\n")

        file_creator(out, f.split("_tokenized")[0] + "_parsed", token)
        index = int(f.split("_tokenized")[0])
        output[index] = token

    return list(collections.OrderedDict(sorted(output.items())).values())

def tokeinizer(io, out):
    output = {}
    for f in os.listdir(io):
        token = subprocess.check_output("cat " + io + f + " | Tokenizer/Tokenizer/run-Tokenizer.sh", shell = True, encoding = sys.stdout.encoding).lstrip().rstrip("\n")
        file_creator(out, f.split(".")[0] + "_tokenized", token)
        output[int(f.split(".")[0])] = token

    return list(collections.OrderedDict(sorted(output.items())).values())


def pos_tag(io, out):
    output = {}
    for f in os.listdir(io):
        token = subprocess.check_output("cat " + io + f + " | Tokenizer/run-Tokenizer.sh ", shell = True, encoding = sys.stdout.encoding).lstrip().rstrip("\n")
        file_creator(out, f.split(".")[0] + "_postag", token)
        output[int(f.split(".")[0])] = token

    return list(collections.OrderedDict(sorted(output.items())).values())

def sentence_tokeinizer(sent, sent_tokenizer):
    return sent_tokenizer.tokenize(sent)

def sentence_to_file(id, path, sent):
    f = open(path + str(id) + ".txt", "w", encoding='iso-8859-1')
    for s in sent:
        f.write(s + '\n')
    f.close()

if __name__ == '__main__':
    data = pd.read_csv("posts_facebook_latin.csv", engine = 'python', encoding = 'iso-8859-1', sep = ';')
    #np.savetxt("posts_text.txt", data.Texto, fmt='%s')

    data['id'] = data.index

    data['Texto'] = data['Texto'].apply(str.lstrip)

    sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')

    data['sentence'] = data['Texto'].apply(lambda x: sentence_tokeinizer(x, sent_tokenizer))

    data.apply(lambda x: sentence_to_file(x['id'], 'files_text/', x['sentence']), axis=1)

   # sentences = sent_tokenizer.tokenize(data.iloc[0].Texto)

    #data.apply(lambda x: file_creator('files_text/', x['id'], x['Texto']), axis=1)

    data['tokenized'] = tokeinizer("files_text/", "files_tokenized/")
    data['parser'] = parser('files_tokenized/', 'files_parsed/')

    #data['pos_tag'] = pos_tag("files_text/", "files_postag/")

    data.to_csv("facebook_processed.csv", index=False)

    #java -Xmx3000m -cp Parser/stanford-parser-2010-11-30/stanford-parser.jar edu.stanford.nlp.parser.lexparser.LexicalizedParser -tokenized -sentences newline -outputFormat oneline -uwModel edu.stanford.nlp.parser.lexparser.BaseUnknownWordModel -MAX_ITEMS 500000 Parser/cintil.ser.gz 0_tokenized.txt


   # p = subprocess.call(["cat", "posts_text.txt",  "|", "Tokenizer/Tokenizer/run-Tokenizer.sh"]) #| Tokenizer/Tokenizer/run-Tokenizer.sh > tokenizer_file.txt"], stdout=subprocess.PIPE)

    #stopd_sents = [[token.lower() for token in sent if token.lower() not in stopwords] for sent in first_doc]
    #noun_phrases = [[token for token, tag in sent if re.match(r'NN*|JJ*', tag)] for sent in tagged_sents]