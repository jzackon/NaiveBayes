#Jeremy Zackon
#CS378
#hw3

import sys


def run():

	if(len(sys.argv) < 4):
		sys.exit('Missing an argument. Arguments: Training Set file, Test Set File, Output File.')

	trainingFile = str(sys.argv[1]);
	testFile = str(sys.argv[2]);
	outputFile = str(sys.argv[3]);


	f = open(trainingFile, 'r')
	rows = [line.split() for line in f]
	classDict = {}
	attDict = {}
	classAttPairDict = {}


	#classDict counts instances of class e or p
	for row in rows:
		if row[0] in classDict:
			classDict[row[0]] += 1
		else:
			classDict[row[0]] = 1

	#attDict counts instances of the other attributes in the data set
	for row in rows:
		for x in range(1, len(row)):
			tempTuple = (row[x], x)
			if tempTuple in attDict:
				attDict[tempTuple] += 1
			else:
				attDict[tempTuple] = 1

	#classAttPairDict combines the classDict and attDict to make keys of all possible combinations
	for c in classDict:
		for att in attDict:
			tempTuple = (c, att[0], att[1])
			classAttPairDict[tempTuple] = 0



	#gets counts for classAttPairDict
	for row in rows:
		for x in range(1, len(row)):
			tempTuple = (row[0], row[x], x)
			if tempTuple in classAttPairDict:
				classAttPairDict[tempTuple] += 1
			else:
				classAttPairDict[tempTuple] = 1

	#Finds the keys with 0 counts to get indexes for laplacian correction
	zeroIndexList = []
	for key in classAttPairDict:
		if classAttPairDict[key] == 0:
			if key[2] not in zeroIndexList:
				zeroIndexList.append(key[2])

	#Adds 1 to the keys that have an index that need laplacian correction
	for key in classAttPairDict:
		if key[2] in zeroIndexList:
			classAttPairDict[key] += 1

	#classProbDict converts the classDict into a dictionary of probabilities
	classProbDict = {}
	total = float(sum(x for x in classDict.values()))
	for key in classDict.keys():
		count = float(classDict[key])
		prob = count/total
		classProbDict[key] = prob

	#classAttPairProbDict converts the classAttPairDict into a dictionary of probabilities
	classAttPairProbDict = {}
	for key in classAttPairDict.keys():
		count = float(classAttPairDict[key])
		classTotal = float(classDict[key[0]])
		prob = count/classTotal
		classAttPairProbDict[key] = prob




	f = open(testFile, 'r')
	rows = [line.split() for line in f]
	tempClass = ''
	correct = 0
	totalRows = len(rows)
	f2 = open(outputFile, 'w')

	#Tests the rows of the test set and writes to the output file
	for row in rows:
		tempKey = None
		maxProb = 0.0
		for key in classProbDict.keys():
			tempTotalProb = 1.0
			for x in range(1, len(row)):
				tempKey = (key, row[x], x)
				tempTotalProb *= classAttPairProbDict[tempKey]
			tempTotalProb *= classProbDict[key]
			if tempTotalProb > maxProb:
				maxProb = tempTotalProb
				tempClass = key
		s = 'Predicted Class: ' + str(tempClass) + '	Actual Class: ' + str(row[0])
		f2.write(s + '\n')
		if tempClass is row[0]:
			correct += 1

	accuracy = (float(correct)/float(totalRows)) * 100.0
	s = 'Accuracy: ' + str(accuracy) + '%'
	f2.write(s)


run()
