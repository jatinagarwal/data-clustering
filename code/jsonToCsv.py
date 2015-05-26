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

a = 0 
nodesKeys = nodes[0].keys()
nodesValues = nodes[0].values()
for key in nodesKeys:
	if type(nodes[0][key]) is dict or type(nodes[0][key]) is list:
		a = a + 1
	else:
		nodesStringKeys.append(key)

	
output = csv.writer(sys.stdout)
output.writerow(nodesStringKeys)  # header row

			
for row in nodes:
	value = []
	for key in nodesStringKeys:
		value.append(row[key])
	output.writerow(value)
	





