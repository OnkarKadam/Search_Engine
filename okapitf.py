#!/usr/bin python
import urllib, re
from collections import OrderedDict
#to read file with 25 queries
f=open('queries-3.txt')
querylines=[]
#Storing the file as a list of its lines.
for line in f:
    querylines.append(line)


f.close() #close the file


#Splitting each line and making a dictionary of query number and query.
eachline=0
temp=[]	
while (eachline< len(querylines)):
	temp=querylines[eachline].split(' ')
	queryno=temp[0]
	wordsinquery=temp[1:]
	wordsinquery[-1] = wordsinquery[-1][:-1]
	
	query="http://fiji4.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?d=1&g=p"
	avglen = 493  #the average document length of the database d3
	#print query
    ##To calculte the tf of the query
	# dictionary for knowing repeated query terms
	tfwords =OrderedDict()
	count = 0

	while count < len(wordsinquery):
		if wordsinquery[count] in tfwords:
			tfwords[wordsinquery[count]] = tfwords[wordsinquery[count]] + 1
		else:
			tfwords[wordsinquery[count]] = 1
		count = count + 1


# we store the term frequency in the list tf
	tf=tfwords.values() 

	eachword=0
	querytf=[]
# the list querytf will have the list of okapi tf's for the query
	while (eachword < len(tf)) :
		querytf.append (float(tf[eachword])/(float(tf[eachword])+0.5+(1.5*(len(wordsinquery)/float(avglen)))))
		eachword=eachword+1

#We automate the process of creating a qury to call the lemur database.
	eachword = 0
	for eachword in tfwords.keys():
		query = query + "&v=" + eachword
	
	#print query

#Reading the file for mapping internal id's to the external ones
	f = open('C:\IR\Project 1\doclist.txt' , 'r')

	lines=[]
#Storing the file as a list of its lines.
	for line in f:
		lines.append(line)

	iter=0
	temp=[]
	dict=OrderedDict()

#Splitting each line and making a dictionary of Internal Id as the key and the external as the value
	while (iter<len(lines)):
		temp=lines[iter].split('   ')
		dict[temp[0]]=temp[1].strip('\n')
		iter=iter+1	

	f.close() #close the file



	
#Parsing the Lemur file
	text = urllib.urlopen(query).read()
	data = re.compile(r'.*?<BODY>(.*?)<HR>', re.DOTALL).match(text).group(1)
	numbers = re.compile(r'(\d+)',re.DOTALL).findall(data)



#okapilength = numbers[1] 
#print okapilength


	hash_okapi=OrderedDict()

	word=1
	i = 2
	wcount=0
	while word < len(numbers):
		#calculate q
		while i < word + int(numbers[word])*3 :   
			if numbers[i] in hash_okapi:
				hash_okapi[numbers[i]] = hash_okapi[numbers[i]] + querytf[wcount]*(float(numbers[i+2])/ (float(numbers[i+2]) + 0.5 + (1.5 * float(numbers[i+1])/avglen)))
			else:
				hash_okapi[numbers[i]] = querytf[wcount]*(float(numbers[i+2])/ (float(numbers[i+2]) + 0.5 + (1.5 * float(numbers[i+1])/avglen)))
	    
			i = i + 3  
	
		word = word + int(numbers[word])*3 + 2
		wcount=wcount+1
		i = word + 1


	f = open('resultokapi-queries-3-d1.txt', 'a') 


	rank=1

	for w in sorted(hash_okapi, key=hash_okapi.get, reverse=True):
		if w in dict:
			f.write( str(queryno)+' Q0 '+str(dict[w])+' '+str(rank)+' '+str(hash_okapi[w])+' EXP \n')
		if rank == 1000:
			break
		rank=rank+1
		
	eachline=eachline+1