#!/usr/bin/python

from __future__ import print_function
import collections #has counter function
import sys
import string
import csv

def checkline(): #define a function that counts words in a line
    global l
    global wordcount
    global words

    w = l.split()     #flines[1].split()   # this splits the string at all the white space and makes an array of the words
    w = [x.lower() for x in w]   # convert everything to lowercase
    wordcount += len(w)
    if 'words' in globals():     # combine all the lines into one list
        words += w
    else:
        words = w

#need to cycle through all files in a folder here instead of just grabbing the file in the argument.

wordcount = 0              # initialize the variable
SID = "SID" # need to set this to file name
f = open(sys.argv[1])      # open the file
flines = f.readlines()     # read in the lines of the file
#linecount = len(flines)    # count the lines
for l in flines:           # for each line 


#need to add qualification here *MOT


     checkline()            # combine the lines and split into words

# remove all punctuations #
for place, item in enumerate(words):
    for c in string.punctuation:
        words[place] = words[place].replace(c,'')

repeated_words = collections.Counter(words)
uniqueWords = list(set(words))

c = csv.writer(open("data.csv", "wb"))
c.writerow(["SID", "Word count","Token count","Lexical diversity"])
c.writerow([str(SID), str(wordcount), str(len(repeated_words)), str(len(repeated_words)/float(len(words)))])
