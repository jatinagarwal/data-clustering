import csv, json, sys, types, itertools, math
import statistics as stat
from collections import defaultdict

columns = defaultdict(list) # each value in each column is appended to a list
attributeUniqueCount = {}
attributeUniqueTuples = {}
sdOfAttributes = []
indexCountSd = []
filteredTuples = []
levelOneClusters = []
levelTwoClusters = []
leastSds = []

#Function below extracts all columns of csv file and stores it in columns
def extractAttributesFromTable():
	global totalCount
	totalCount = sum(1 for row in csv.reader(open(sys.argv[1]))) - 1
	with open(sys.argv[1]) as f:# opening a file as an object
	    reader = csv.DictReader(f) # read rows into a dictionary format
	    for row in reader: # read a row as {column1: value1, column2: value2,...}
		for (k,v) in row.items(): # go over each column name and value 
		    columns[k].append(v) # append the value into the appropriate list
		                         # based on column name k



# Function below computes count of unique values in each attribute and standard deviation for each attribute
# It also computes a list of tuple with (index, count, sd, attributeName)
def extractCountAndSdForEachAttribute():
	i = 0 			# for tracking index of attributes
	for column in columns:  # iterating over attributes of a table
		attributeUniqueTuples[column] = [(g[0], len(list(g[1]))) for g in itertools.groupby(sorted(columns[column]))]; 
		# grouping based on unqiue values 
		uniqueList = []
		for tup in attributeUniqueTuples[column]:
			uniqueList.append(tup[1]) # Appending of count of uniques values to list
		sd = 0	 
		# Computing standard deviation for each attribute
		if(len(uniqueList) == 1):
			sdOfAttributes.append(sd)
		else:
			sd = stat.stdev(uniqueList) 
			sdOfAttributes.append(sd)
		attributeUniqueCount[column] = len(attributeUniqueTuples[column]);
		# computing with index, count of uniques valuess on each attribute,  standard deviation and name of the attribute 
		indexCountSd.append((i,attributeUniqueCount[column],sd,column));
		i = i + 1


#Extract tuples in selected range, sorts tuples on standard deviation and returns tuple with least standard deviation
def findAttributeWithLeastSd(sdRange):		
	sortedTuplesOnSd = sorted(indexCountSd, key=lambda tup: tup[1]) # sorting tuples based on count
	#print x
	selectedRange = sdRange;
	countRange = (math.ceil(selectedRange*totalCount),math.floor(totalCount*(1-selectedRange)))
	for tup in sortedTuplesOnSd:
		if tup[1] > countRange[0] and tup[1]<countRange[1]:
			filteredTuples.append(tup)  # filtering out the tuple not in countRange
	leastSds = sorted(filteredTuples, key=lambda tup: tup[2]) #sorting filtred tuples based on standard deviation
	return leastSds

def levelOneClustering(indexOfLeastSd):
	with open(sys.argv[1], 'rb') as f:
	    reader = csv.reader(f)
	    your_list = list(reader)
	 
	sorted_by_sd = sorted(your_list, key=lambda tup: tup[indexOfLeastSd])
	print 'We do level one clustering for on ', leastSds[0][3]
	levelOneClusters = [(g[0], list(g[1]	)) for g in itertools.groupby(sorted_by_sd,lambda attribute: attribute[indexOfLeastSd])]
	del levelOneClusters[0]
	return levelOneClusters
	

def levelTwoClustering(levelOneCluster,indexOfLeastSd):
	print 'We do level two clustering for on ', leastSds[1][3]
	for cluster in levelOneCluster:
		sorted_by_sd = sorted(cluster[1], key=lambda tup: tup[indexOfLeastSd])
		secondCluster = [(g[0], list(g[1])) for g in itertools.groupby(sorted_by_sd,lambda attribute: attribute[indexOfLeastSd])]
		#print cluster
		levelTwoClusters.append((cluster[0],secondCluster));

if __name__ == "__main__":
	extractAttributesFromTable() # Extracting attributes from the table
	extractCountAndSdForEachAttribute() # Computing count of unique values on each attribute and standard deviation of each attribute
	for row in indexCountSd:
		print row
	sdRange = 0.1 # Range of standard deviation
	leastSds = findAttributeWithLeastSd(sdRange) 
	print '************************************************************************************************'
	indexOfLeastSd = leastSds[0][0]; # index of attribute with least standard deviation
	levelOneClusters =  levelOneClustering(indexOfLeastSd)
	indexOfLeastSd = leastSds[1][0];
	levelTwoClustering(levelOneClusters,indexOfLeastSd)
	#code for printing clusters
	for levelTwo in levelTwoClusters:
		print levelTwo[0]
		for cluster in levelTwo[1]:
			print '\t', cluster[0]
			for tup in cluster[1]:
				print '\t', tup
				print '*******************************************************************************************************'
			print '\n'	
		print '\n', '\n', '\n'	

	




