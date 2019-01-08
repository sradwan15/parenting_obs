import os
import string
import pandas as pd
from lexical_diversity import mtld, hdd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import tokenize
from statistics import mean
lemmatizer = WordNetLemmatizer()

# a function to clean texts in brackets
def clean(string):
    ret = ''
    skip1c = 0
    for i in string:
        if i == '[':
            skip1c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif skip1c == 0:
            ret += i
    return ret


# formatted mother utterances (each utterance should be in the same one paragraph) by hand
# "Female speaker" "*Other Child" "*OTH" "*BOTH" "*ADF,ADM" are what used to refer to other speakers than parent or child
# should replace all "CHI 2:" with "CHI:"
# get conditions.csv from google sheet instead of by hand

# creat a dataframe for calculation results
col_names = ['sid', 'MTLD', 'HDD', 'types', 'tokens', 'TTR', 'len_sentence']
results = pd.DataFrame(columns = col_names)

files = os.listdir("trans_out_txt/")
files.remove('.DS_Store')
all_dat = {}
# print (files)
for fname in files:
    folder = "trans_out_txt/"
    name =  fname
    path = "".join((folder,name))
    fr = open(path, 'r')
    print (fr)
    lines = []
    for line in fr:
        spm = line.split('*MOT:')
        spm_1 = line.split('MOT:')
        spd = line.split('*FAT:')
        spd_1 = line.split('FAT:')
        if len(spm)>1:
            lines.append(spm[1]) # found mother speech, grab it
        elif len(spd)>1:
            lines.append(spd[1]) # found father speech, grab it
        elif len(spd_1)>1:
                lines.append(spd_1[1])
        elif len(spm_1)>1:
            lines.append(spm_1[1])
    lines_str = " ".join(lines)
    lines_str = lines_str.replace ('\n', '')
    lines_str = lines_str.replace ('\t', '')
    text_ready = clean(lines_str)
#   print (repr(text_ready))
    all_dat[fname] = text_ready

# call MTLD and HDD functions and calculate
    id = fname[6:14]
    print (len(str.split(text_ready)))
    if (len(str.split(text_ready)))>50:
        mtld_value = mtld(text_ready.split())
        hdd_value = hdd(text_ready.split())
    else:
        mtld_value = 'NA'
        hdd_value = 'NA' # mtld only takes text more than 50 words


# Calculate Type, Token, TTR and average sentence length
# sentence length
    sent = tokenize.sent_tokenize(text_ready)
    l_sent = []
    for s in sent:
        s= ''.join(s)
        l_sent.append(len((str.split(s))))
    len_sent_value = mean (l_sent)

# remove all punctuations
    text_ready = list(text_ready)
    n_words = len(text_ready)
    for i in range(n_words):
        for c in string.punctuation:
            text_ready[i] = text_ready[i].replace(c,'')
# remove empty words
    text_ready = list(filter(None, text_ready))

    text_ready = ''.join(text_ready)
    token_value = len(str.split(text_ready))
    word_list = nltk.word_tokenize(text_ready)
    lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
    print(lemmatized_output)
    type_value = len(set(str.split(lemmatized_output)))
    ttr_value = type_value/token_value
    results = results.append({'sid': id, 'MTLD': mtld_value, 'HDD': hdd_value, 'tokens': token_value, 'types': type_value, 'TTR': ttr_value, 'len_sentence': len_sent_value}, ignore_index = True)
    fr.close()
#print (all_dat)
print (results)
results.to_csv('MTLD_HDD.csv', sep=',', encoding='utf-8')

# all_dat should be a dictionary full of mother/father speech for each file ID
