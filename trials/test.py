import csv, json, sys, types

nodesStringKeys = []
input = open(sys.argv[1])
data = json.load(input)
input.close()

nodes = data["nodes"]
tags = u'tags'

def tagConverter():
	for row in nodes:
		if len(row[tags]) > 1:
			if row[tags][0][u'key'] == 'Type':
				row[u'tagName'] = row[tags][0][u'value']
				row[u'tagType'] = row[tags][1][u'value']
			else:
				row[u'tagName'] = row[tags][1][u'value']
				row[u'tagType'] = row[tags][0][u'value']
		elif len(row[tags]) > 0:
			if row[tags][0][u'key'] == 'Type':
				row[u'tagType'] = row[tags][0][u'value']
				row[u'tagName'] = None
			else:
				row[u'tagName'] = row[tags][0][u'value']
				row[u'tagType'] = None
		else:
			row[u'tagName'] = None
			row[u'tagType'] = None

tagConverter()

for row in nodes:
	if len(row[tags]) > 1:
			if row[tags][0][u'key'] == 'Type':
				print row[u'tagName'], row[u'tagType']	
			else:
				print row[u'tagName'], row[u'tagType']
	elif len(row[tags]) > 0:
		if row[tags][0][u'key'] == 'Type':
			print row[u'tagName'], ',', row[u'tagType']	
		else:
			print row[u'tagName'], ',', row[u'tagType']
	else:
		print row[u'tagName'], ',', row[u'tagType']

