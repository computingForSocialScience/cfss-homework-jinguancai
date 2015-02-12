import grequests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import sys
from io import open



def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    
    url = "https://api.spotify.com/v1/search?q="+ name +"&type=artist" 
    #print url 
    req = grequests.get(url)
    result_list = grequests.map([req])
    if not result_list[0].ok:
        print "Error in request"
    """else:
        print "Result OK"""
    info = result_list[0].json()
    #print url
    #info["artists"][0]['id']
    ID = info['artists']['items'][0]['id']
    #print ID
    return(ID)
#print fetchArtistId('Patti Smith')
#print fetchArtistId('Ariana Grande')
    
def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
    returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    url = "https://api.spotify.com/v1/artists/" + artist_id
    req = grequests.get(url)
    #print url
    result_list = grequests.map([req])
    if not result_list[0].ok:
        print "Error in request"
    """else:
        print "Result OK"""
    info = result_list[0].json()
    #print info
    data = {}
    data['followers'] = info['followers']['total']
    data['genres'] = info['genres']
    data['id'] = info['id']
    data['name'] = info['name']
    data['popularity'] = info['popularity']
    #print data
    return (data)
#print fetchArtistInfo(fetchArtistId('Patti Smith'))
#print fetchArtistInfo(fetchArtistId('Ariana Grande'))