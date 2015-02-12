import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    # YOUR CODE HERE
    artistinfolist = [fetchArtistInfo(fetchArtistId(i)) for i in artist_names]
    albuminfolist = []
    for i in artistinfolist:
    	#print i['id']
    	for albumid in fetchAlbumIds(i['id']):
    		albuminfolist.append(fetchAlbumInfo(albumid))
    writeArtistsTable(artistinfolist)
    writeAlbumsTable(albuminfolist)
    plotBarChart()