import sys
import requests
import csv
import grequests
from io import open
import pandas as pd
import numpy as np
import networkx as nx

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

#randomCentralNode(pandasToNetworkX(combineEdgelists(readEdgeList('result.csv'),readEdgeList('result2.csv'))))
