import sys
import requests
import csv
import grequests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import sys
from io import open
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo


def writeArtistsTable(artist_info_list):
    """Given a list of dictionries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    f = open("artists.csv",'w',encoding='utf-8')
    f.write('"%s", "%s","%s","%s"\n' % (u'ARTIST_ID',u'ARTIST_NAME',u'ARTIST_FOLLOWERS',u'ARTIST_POPULARITY'))
    #print len(artist_info_list),artist_info_list
    if type(artist_info_list) != list:
        f.write('"' +artist_info_list['id']+ '"' +","+'"' +artist_info_list['name']+ '"' +","+ '"' +unicode(artist_info_list['followers'])+ '"' +","+ '"' +unicode(artist_info_list['popularity'])+ '"' +"\n")
    else:
        #print artist_info_list
        for i in artist_info_list:
            #print i
            ID = i[u'id']
            name = i[u'name']
            followers = unicode(i[u'followers'])
            popularity = unicode(i[u'popularity'])
            print ID, name, followers, popularity
            print type(ID), type(name), type(followers), type(popularity) 

            f.write('"'+ ID + '"' + ','+ '"' + name + '"' + ','+ '"' + followers + '"' + ','+ '"' + popularity + '"' +'\n')
    f.close()

      
def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    f = open("albums.csv",'w',encoding='utf-8')
    f.write('"%s","%s","%s","%s","%s" \n' % (u'ARTIST_ID',u'ALBUM_ID',u'ALBUM_NAME',u'ALBUM_YEAR',u'ALBUM_POPULARITY'))
    #print album_info_list
    if type(album_info_list) != list:
        f.write('"' + album_info_list['artist_id']+ '"' +","+'"' + album_info_list['album_id']+ '"' +","+ '"' + album_info_list['name']+ '"' +","+'"' + unicode(album_info_list['year'])+ '"' +","+'"' + unicode(album_info_list['popularity']) + '"' +"\n")
    else:
        for i in album_info_list:
            #print i
            artistid = i['artist_id']
            albumid = str(i['album_id'])
            #print albumid
            name = i['name']
            year = i['year']
            popularity = i['popularity']
            f.write('"' + artistid+ '"' +','+'"' + albumid+ '"' +','+'"' + name+ '"' +','+'"' + unicode(year)+ '"' +','+'"' + unicode(popularity)+ '"' +'\n')
    f.close()

#writeArtistsTable([fetchArtistId('Amy Winehouse'),fetchArtistId('Ariana Grande')])
#writeAlbumsTable(fetchAlbumIds(fetchArtistId('Amy Winehouse'))+fetchAlbumIds(fetchArtistId('Ariana Grande')))
#writeArtistsTable(fetchArtistId('Amy Winehouse'))
#writeAlbumsTable(fetchAlbumIds(fetchArtistId('Amy Winehouse')))