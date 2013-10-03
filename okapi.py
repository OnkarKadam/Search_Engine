#!/usr/bin python
import urllib, re
from urllib2 import urlopen
from collections import OrderedDict

###############################################################################
# Storing the internal and external ids as a key-value hash
f = open('doclist.txt', 'r')
lines=[]
for line in f:
	lines.append(line)

f.close()
temp=[]
iter = 0
dict=OrderedDict()
while iter<len(lines) :
	temp=lines[iter].split('   ')
	dict[temp[0]] = temp[1][:-1] 
	iter = iter + 1
###############################################################################
# Read all the queries
queryfile = open('queries.txt', 'r')
queries=[]
for query in queryfile:
	queries.append(query)

queryfile.close()
avglen = 288
docs= 84678
unique = 166054	
###############################################################################
output = open('okapi_result.txt',"w")
querynum = 0
while querynum < len(queries):
	query= queries[querynum].split(' ')
	qid = query[0]

	# relevant query items
	keywords = query[1:]
	print keywords
	keywords[-1] = keywords[-1][:-1]

	# dictionary for knowing repeated query terms
	keydict =OrderedDict()
	count = 0

	# Calculating repeated query terms
	while count < len(keywords):
		if keywords[count] in keydict:
			keydict[keywords[count]] = keydict[keywords[count]] + 1
		else:
			keydict[keywords[count]] = 1
		count = count + 1

	# Making a query for lemur
	query="http://fiji4.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?d=3&g=p"
	for k in keydict.keys():
		query = query + "&v=" + k

	print query
	otf = []

	for w in keydict:
		otf.append(keydict[w] / (keydict[w] + 0.5 + 1.5* (len(keywords)/avglen)))

	print keydict
	text = urllib.urlopen(query).read()
	data = re.compile(r'.*?<BODY>(.*?)<HR>', re.DOTALL).match(text).group(1)
	numbers = re.compile(r'(\d+)',re.DOTALL).findall(data)

	okapitf=OrderedDict()
	
	queryword = 0
	word=1
	i = 2
	while word < len(numbers):
		while i < word + int(numbers[word])*3 :   
			if numbers[i] in okapitf:
				okapitf[numbers[i]] = okapitf[numbers[i]] + otf[queryword] *(float(numbers[i+2])/ (float(numbers[i+2]) + 0.5 + (1.5 * float(numbers[i+1])/avglen)))
			else:
				okapitf[numbers[i]] = otf[queryword] *(float(numbers[i+2])/ (float(numbers[i+2]) + 0.5 + (1.5 * float(numbers[i+1])/avglen)))
			i = i + 3  
		word = word + int(numbers[word])*3 + 2
		i = word + 1
		queryword = queryword + 1

	
	c = 1
	for w in sorted(okapitf, key=okapitf.get, reverse=True):
		output.write(str(qid) + ' Q0 ' + dict[w] + ' ' + str(c) + ' ' + str(okapitf[w]) + ' Exp\n')
		if c == 1000:
			break
		c = c+ 1 
	
	querynum = querynum + 1
	
output.close()