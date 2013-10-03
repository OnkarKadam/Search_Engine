#!/usr/bin python
import urllib, re, math
from collections import OrderedDict
#to read file with 25 queries
f=open('queries-3.txt')
querylines=[]
#Storing the file as a list of its lines.
for line in f:
    querylines.append(line)

f.close() #close the file
eachline=0
temp=[]
querydict={}

#Splitting each line and making a dictionary of Internal Id as the key and the external as the value
while (eachline<len(querylines)):
	temp=querylines[eachline].split(' ')
	queryno=temp[0]
	wordsinquery=temp[1:]
	wordsinquery[-1] = wordsinquery[-1][:-1]
	query="http://fiji4.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?d=1&g=p"
	avglen = 493 #the average document length of the database d3
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
	
	querytf=tfwords.values() 
	

	#We automate the process of creating a query to call the lemur database.
	eachword = 0
	for eachword in tfwords.keys():
		query = query + "&v=" + eachword
	


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
	
	#print query
	
	#Parsing the Lemur file
	text = urllib.urlopen(query).read()
	data = re.compile(r'.*?<BODY>(.*?)<HR>', re.DOTALL).match(text).group(1)
	numbers = re.compile(r'(\d+)',re.DOTALL).findall(data)
	bm25=OrderedDict()
	word=1
	i = 2
	wcount=0
	k2=500
	k1=1.2
	b=1.0
	numdocs=84678
	while word < len(numbers):
		#calculate q
		df = float (numbers[word])
		while i < word + int(numbers[word])*3 :   
			k=k1 * ((1-b)+b*(float(numbers[i+1])/avglen))
			if numbers[i] in bm25:
				bm25[numbers[i]] = bm25[numbers[i]] + math.log((numdocs- df+0.5)/(df+0.5))*(((k1+1)*float(numbers[i+2]))/(k+float(numbers[i+2])))*((k2+1)*querytf[wcount]/(k2+querytf[wcount]))
			else:
				bm25[numbers[i]] = math.log((numdocs- df + 0.5)/(df+0.5))*(((k1+1)*float(numbers[i+2]))/(k+float(numbers[i+2])))*((k2+1)*querytf[wcount]/(k2+querytf[wcount]))
	    
			i = i + 3  
	
		word = word + int(numbers[word])*3 + 2
		wcount=wcount+1
	
		i = word + 1
	
	
	
	f = open('resultbm25new.txt', 'a') 


	rank=1

	for w in sorted(bm25, key=bm25.get, reverse=True):
    
		f.write(str(queryno)+' Q0 '+str(dict[w])+' '+str(rank)+' '+str(bm25[w])+' EXP \n')
		if rank == 1000:
			break
		rank=rank+1
		
	eachline=eachline+1