import sys
import os

def count(outFile):
	fp = open(outFile, 'w')
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
					
					
		fp.write(fileName + "," + str(counter) + '\n')
	

	fp.close()


#to use count, python conversationCounter.py [output_file]
count(sys.argv[1])
