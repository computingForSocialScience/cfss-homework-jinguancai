import sys
import requests
import csv
import grequests
from io import open
import pandas as pd
import numpy as np
import networkx as nx

def getRelatedArtists(artistid): 
    url = "https://api.spotify.com/v1/artists/" + str(artistid) +"/related-artists"  
    #print artist_id
    #print url
    req = grequests.get(url)
    result_list = grequests.map([req])
    if not result_list[0].ok:
        print "Error in request"
    """else:
        print "Result OK"""
    info = result_list[0].json()
    #print info
    data = []
    for i in info['artists']:
        #print i
        data.append(i['id'])
        #print i['id']
    
    #print data
    return (data)
#getRelatedArtists('43ZHCT0cAZBISjO8DG9PnE')
#getRelatedArtists('0JDkhL4rjiPNEp92jAgJnS')

def getDepthEdges(artistID, depth=1):
	edgelist = []
	list1 = [artistID]
	list2 = []
	while depth != 0:
		for i in list1:
			list2 = getRelatedArtists(i)
			for j in list2:
				artist_tuple = (i,j)
				edgelist.append(artist_tuple)
		depth -= 1
		if depth == 0:
			break
		list1 = list2 
		#print list1[-1]
	#print edgelist

	#check the duplicate ones
	edgelist2 = []
	for i in edgelist:
		if i not in edgelist2:
			edgelist2.append(i)
	#print edgelist2
	return edgelist2
#getDepthEdges('43ZHCT0cAZBISjO8DG9PnE',3)
#getDepthEdges('0JDkhL4rjiPNEp92jAgJnS',3)

def getEdgeList(artistID, depth):
	edgelist_df = pd.DataFrame(getDepthEdges(artistID,depth))
	return edgelist_df

def writeEdgeList(artistID,depth,filename):
	getEdgeList(artistID, depth).to_csv(path_or_buf = filename, index = False, header = ['artist1','artist2'])
	return ()
#writeEdgeList('43ZHCT0cAZBISjO8DG9PnE',3,'result.csv')
#writeEdgeList('0JDkhL4rjiPNEp92jAgJnS',3,'result2.csv')

def readEdgeList(filename):
	edgelist_df = pd.read_csv(filename)
	#print edgelist_df.columns
	if len(edgelist_df.columns) != 2:
		print "Warning: Not 2 columns"
	new_edgelist_df = edgelist_df[edgelist_df.columns[:2]]
	#print new_edgelist_df
	return new_edgelist_df
#readEdgeList('result.csv')
#readEdgeList('result2.csv')

def degree(edgeList, in_or_out):
	readEdgeList(edgeList)
	if in_or_out is 'in':
		#print type(readEdgeList(edgeList)[['artist2']])
		#print readEdgeList(edgeList)['artist2'].value_counts(sort=True)
		return readEdgeList(edgeList)['artist2'].value_counts(sort=True)
	if in_or_out is 'out':
		#print type(readEdgeList(edgeList)[['artist2']])
		#print readEdgeList(edgeList)['artist1'].value_counts(sort=True)
		return readEdgeList(edgeList)['artist1'].value_counts(sort=True)
	else:
		print "need to put in or out"

#degree('result.csv','in')
#degree('result2.csv','in')

def combineEdgelists(edgeList1,edgeList2):
	#print type(edgeList1)
	#print edgeList1
	#print edgeList2
	concatenated = pd.merge(edgeList1,edgeList2)
	#print concatenated.drop_duplicates()
	return concatenated.drop_duplicates()

#combineEdgelists(readEdgeList('result.csv'),readEdgeList('result2.csv'))

def pandasToNetworkX(edgeList):
	g = nx.DiGraph()
	for sender,receiver in edgeList.to_records(index=False):
		g.add_edge(sender,receiver)
	#print g.nodes()
	return g

#pandasToNetworkX(combineEdgelists(readEdgeList('result.csv'),readEdgeList('result2.csv')))

def randomCentralNode(inputDigraph):
	freqdict = nx.eigenvector_centrality(inputDigraph)
	#Normalization
	#print freqdict
	total = 0
	for i in freqdict:
		total += freqdict[i]
	new_freq_dict = {}
	for i in freqdict:
		new_freq_dict[i] = freqdict[i]/total
	#Check Normality
	'''new_total = 0
	for i in new_freq_dict:
		new_total += new_freq_dict[i]
	print new_total'''
	result = np.random.choice(new_freq_dict.keys(), p=new_freq_dict.values())
	print result
	return  result





randomCentralNode(pandasToNetworkX(combineEdgelists(readEdgeList('result.csv'),readEdgeList('result2.csv'))))

