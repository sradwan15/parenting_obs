import sys
import os
import csv

def count():
	outFile = '/Users/samaherradwan/Desktop/parenting_obs/exp2_lexical_diversity'
	fp = open(outFile + "Add.csv", 'w')
	csvLines = []
	with open(outFile + ".csv", 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
		for row in spamreader:
			csvLines.append(' '.join(row))	
	header = csvLines[0]
	csvLines = csvLines[1:]
	header = header + ",Coversational_Turns\n"
	fp.write(header)
	path = '/Users/samaherradwan/Desktop/parenting_obs/parenting_obs_e2/trans_out_txt/'
	for fileName in os.listdir(path):
		inFile = open(path + fileName, 'r')
		counter = 0
		lines = inFile.read()
		ifChild = False
		start = False
		lines = lines.strip().split(":")
		for line in lines[:len(lines) - 1]:
			if "MOT" in line:
				if ifChild:
					counter+=1
					ifChild = False
				else:
					start = True
					ifChild = False
			elif "CHI" in line:
				if ifChild == False and start:
					counter+=1
					ifChild = True
				else:
					start = True
					ifChild = True
			elif "FAT" in line:
				if ifChild:
					counter+=1
					ifChild = False
				else:
					start = True
					ifChild = False
		
		fileName = fileName.split("_")
		fileName = fileName[1] + "_" + fileName[2]
		fileName = fileName.split(".")
		fileName = fileName[0]
		for csvRow in csvLines:
			if fileName in csvRow:
				fp.write(csvRow + "," + str(counter) + "\n")
	

	fp.close()


#to use count, python conversationCounter.py
count()
