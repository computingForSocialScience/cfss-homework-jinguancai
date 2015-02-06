# coding=utf-8

import unittest
import nose
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import getBarChartData

def testFetchArtistId():
    assert fetchArtistId('Missy Elliott') == u'2wIVse2owClT7go1WT98tk'
    assert fetchArtistId('Robyn') == u'6UE7nl9mha6s8z0wFQFIZ2'

def testFetchArtistInfo():
    assert fetchArtistInfo('6UE7nl9mha6s8z0wFQFIZ2')['genres'] == [u'europop']

def testFetchAlbums():
    assert len(fetchAlbumIds('57anmI1X2hXWPrNagFdzZr')) == 10

def testFetchAlbumInfo():
    albumInfo = fetchAlbumInfo('24geHauG3JIbpyf9CRiuvf')
    assert albumInfo['album_id'] == '24geHauG3JIbpyf9CRiuvf'
    assert albumInfo['popularity'] == 44

def testWriteArtistsInfo():
    artistId1 = fetchArtistId('earth wind fire')
    artistId2 = fetchArtistId('patsy cline')
    artistId3 = fetchArtistId('五月天')
   
    assert artistId1=='4QQgXkCYTt3BlENzhyNETg'
    assert artistId2=='7dNsHhGeGU5MV01r06O8gK'
    assert artistId3=='16s0YTFcyjP4kgFwt7ktrY'
 
    albumIds1 = fetchAlbumIds(artistId1)
    albumIds2 = fetchAlbumIds(artistId2)
    albumIds3 = fetchAlbumIds(artistId3)

    print "albumIds1=",len(albumIds1)
    print "albumIds2=",len(albumIds2)
    print "albumIds3=",len(albumIds3)

    assert len(albumIds1) == 20
    assert len(albumIds2) == 20
    assert len(albumIds3) == 17

    artistInfo1 = fetchArtistInfo(artistId1)
    artistInfo2 = fetchArtistInfo(artistId2)
    artistInfo3 = fetchArtistInfo(artistId3)
    
    albumInfoList = []
    for albumId in albumIds1:
        albumInfoList.append(fetchAlbumInfo(albumId))
    for albumId in albumIds2:
        albumInfoList.append(fetchAlbumInfo(albumId))
    for albumId in albumIds3:
        albumInfoList.append(fetchAlbumInfo(albumId))
    
    writeArtistsTable([artistInfo1, artistInfo2, artistInfo3])
    writeAlbumsTable(albumInfoList)

    bcd =getBarChartData()

    # asset that there were 11 albums in the 80s and 21 in the 00s
    assert(bcd[1][8] == 11)
    assert(bcd[1][10] == 21)


if __name__ == '__main__':
    nose.main()
