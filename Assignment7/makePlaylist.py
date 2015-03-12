import sys
import requests
import csv
import grequests
from io import open
import pandas as pd
import numpy as np
import networkx as nx
from artistNetworks import getRelatedArtists,getDepthEdges,getEdgeList,writeEdgeList
from analyzeNetworks import readEdgeList,degree,combineEdgeLists,pandasToNetworkX,randomCentralNode
from fetchAlbums import fetchAlbumIds,fetchAlbumInfo
from fetchArtist import fetchArtistId,fetchArtistInfo

def fetchTrackIds(album_id): #input is a single id not a list
    url = "https://api.spotify.com/v1/albums/" + str(album_id) + '/tracks'
    req = grequests.get(url)
    result_list = grequests.map([req])
    if not result_list[0].ok:
        print "Error in request"
    """else:
        print "Result OK"""
    info = result_list[0].json()
    data = []
    for i in info['items']:
        data.append(i['id'])
    return (data)

def fetchTrackInfo(track_id):  
    url = "https://api.spotify.com/v1/tracks/" + track_id
    req = grequests.get(url)
    result_list = grequests.map([req])
    if not result_list[0].ok:
        print "Error in request"
    """else:
        print "Result OK"""
    if result_list[0] == None:
        Continue
    info = result_list[0].json()
    data = {}
    data['name'] = info['name']
    return (data)

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    #generate the network
    old_edgelist = None
    artistidlist = [fetchArtistId(i) for i in artist_names]
    
    for i in artistidlist:
    	edgelist = getEdgeList(i,2)
    	new_edgelist = combineEdgeLists(edgelist,old_edgelist)
    	old_edgelist = new_edgelist
	
	#pick tracks
	k = 0
	artist_list = []
	while k != 30:
		artist_dict = {}
		artist_dict['artist_name'] = fetchArtistInfo(randomCentralNode(pandasToNetworkX(old_edgelist)))['name']
		#print artist_dict['artist_name']
		album_id = np.random.choice(fetchAlbumIds(fetchArtistId(artist_dict['artist_name'])))
		#print album_id
		artist_dict['album_name'] = fetchAlbumInfo(album_id)['name']
		#print artist_dict['album_name']
		track_id = np.random.choice(fetchTrackIds(album_id))
		#print track_id
		artist_dict['track_name'] = fetchTrackInfo(track_id)['name']
		#print artist_dict['track_name']
		artist_list.append(artist_dict)
		k += 1

	#write to csv
	f = open("playlist.csv",'w',encoding= 'utf-8')
    f.write('"%s", "%s","%s"\n' % (u'artist_name',u'album_name',u'track_name'))
    for i in artist_list:
    	#print i
    	artist_name = i['artist_name']
    	album_name = i['album_name']
    	track_name = i['track_name']
    	f.write('"%s", "%s","%s"\n' % (artist_name,album_name,track_name))
    	#f.write('"'+ artist_name + '"' + ','+ '"' + album_name + '"' + ','+ '"' + track_name + '"' +'\n')
    f.close()

    ### My makelist.py hit the unicodeerror whenever I test it but the problem only occures in Windows system.##