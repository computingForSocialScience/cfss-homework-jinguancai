import sys
import requests
import csv
import grequests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from io import open

def fetchAlbumIds(artist_id): #input is a single id not a list
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url = "https://api.spotify.com/v1/artists/" + str(artist_id) +"/albums?album_type=album&market=US"  
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
    for i in info['items']:
        #print i
        data.append(i['id'])
        #print i['id']
    
    #print data
    return (data)

#print fetchAlbumIds(fetchArtistId('Patti Smith'))
#print fetchAlbumIds(fetchArtistId('Ariana Grande'))


def fetchAlbumInfo(album_id):  # input is a single string but not a list
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    url = "https://api.spotify.com/v1/albums/" + str(album_id)
    #print url
    req = grequests.get(url)
    result_list = grequests.map([req])
    if not result_list[0].ok:
        print "Error in request"
    """else:
        print "Result OK"""
    if result_list[0] == None:
        Continue
    info = result_list[0].json()
    #print info
    data = {}
    data['artist_id'] = info['artists'][0]['id']
    data['album_id'] = info['id']
    data['name'] = info['name']
    data['year'] = info['release_date'][:4]
    data['popularity'] = info['popularity']
    #print data
    return (data)

#print fetchAlbumInfo(fetchAlbumIds(fetchArtistId('Patti Smith'))[0])
#print fetchAlbumInfo(fetchAlbumIds(fetchArtistId('Ariana Grande'))[0])
#print fetchAlbumInfo('4QQgXkCYTt3BlENzhyNETg')