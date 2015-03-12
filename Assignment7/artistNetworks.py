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
#writeEdgeList('43ZHCT0cAZBISjO8DG9PnE',2,'result.csv')
#writeEdgeList('0JDkhL4rjiPNEp92jAgJnS',2,'result2.csv')

