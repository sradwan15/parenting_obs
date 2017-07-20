from __future__ import print_function

import collections
import os
import sys
import string
import csv
import re

def main(speech_dir,rel_file):
    abso_file = speech_dir+rel_file
    with open(abso_file) as f:
        flines = f.readlines()
        n_lines = len(flines)
        words = []
        for line in flines:
            line = re.sub('\t+','\t',line) #condenses multiple tabs into one
            splitline = line.strip().split('\t') #splits lines based on tabs
            #print(splitline[0], len(splitline))
            if len(splitline)!=2: 
                continue
            speaker = splitline[0].strip()
            if (speaker!='*MOT:' and speaker!='*FAT:'):
                continue
            #print(speaker!='*MOT:' and speaker!='*FAT:',splitline[1])
            new_words = splitline[1].split()
            words += [word.lower() for word in new_words]

    n_words = len(words)
    #print(words)

    # remove all punctuations
    for i in range(n_words):
        for c in string.punctuation:
            words[i] = words[i].replace(c,'')

    # remove empty words
    words = list(filter(None, words))
    n_words = len(words)

    # count each word
    word_count = collections.Counter(words)

    # get the sorted list of unique words
    unique_words = list(word_count.keys())
    unique_words.sort()

    n_unique = len(unique_words)
    ttr = len(word_count)/float(len(words))

    """
    out_fname = '{}_out.txt'.format(os.path.splitext(speech_sample)[0])

    out_lines = []
    out_lines.append('Type-Token Ratio (U/T):           {:0.4f}\n'.format(ttr))
    out_lines.append('Number of Utterances:             {}\n'.format(n_lines))
    out_lines.append('Total Number of Words (T):        {}\n'.format(n_words))
    out_lines.append('Total Number of Unique Words (U): {}\n'.format(n_unique))

    out_lines.append('\nUnique Words (frequency):\n')
    for word, count in word_count.most_common():
        out_lines.append('{}\t{}\n'.format(count, word))

    out_lines.append('\nUnique Words (alphabetical):\n')
    for word in unique_words:
        out_lines.append('{}\t{}\n'.format(word_count[word], word))
    """

    # lines.append('\n\n{}\n'.format(str(word_count)))
    # out_file.write('\n\n' + str(word_count)+'\n')

    #with open(out_fname, 'w') as out_file:
    #    for line in out_lines:
    #        out_file.write(line)

    #out_lines = ['output saved to: \n{}\n\n'.format(out_fname)] + out_lines

    return([str(rel_file), str(n_unique), str(n_words), str(ttr)])


    #out_lines.append('='*80)
    #output = ''.join(out_lines)

    return output

if __name__ == '__main__':
    d = sys.argv[1] #directory name
    filelist = os.listdir(d)
    c = csv.writer(open("lexdiv_data.csv", "wb"))
    c.writerow(["SID", "Type count","Token count","Lexical diversity"])

    for rf in filelist:
        if os.path.splitext(rf)[-1]!='.txt':
            print('Skipping file:', rf)
            continue
        print("Analyzing file:", rf)
        output = main(d,rf)
        c.writerow(output)
