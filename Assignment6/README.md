# Assignment 6: Network Analysis of Spotify Artists

In this assignment, you will be using the Spotify API's [related-artists](https://api.spotify.com/v1/artists/43ZHCT0cAZBISjO8DG9PnE/related-artists) method to generate related-artist networks for individual musicians.
You will then combine two or more of these networks to map out the space of artists defined by their joint similarity to the root artists.
Finally, you will write a function that creates a Spotify- (or Pandora-) like playlist of tracks related to the root artists.

You will find it useful to incorporate some of the functions you wrote last week. 

## Part I. Get related-artist networks
Put all the functions you define in questions I.1 through I.4 in a file called `artistNetworks.py`.

### 1. Fetch Related Artists
Write a function called `getRelatedArtists(artistID)` that takes an artist ID as its only argument and returns a list of related artists IDs.
Spotify's [related-artists method documentation](https://developer.spotify.com/web-api/get-related-artists/) will be useful to see the URI formatting and the structure of the returned JSON data.
The method returns a maximum of twenty related artists.

For example, `getRelatedArtists('2mAFHYBasVVtMekMUkRO9g')` should return a list like `['4UEhWRcA8NyjX0xaGjYf19', '1X1aYKdWWVdWnduDyBSpdu']` (except probably much longer).

### 2. Depth Searching 
Next write a function called `getDepthEdges(artistID, depth)` that takes two arguments, an artist ID and an integer `depth`, and returns a list of tuples representing the (directed) pairs of related artists.
This function should search `depth` iterations 'deep' into the network.
So `getDepthEdges(artistId,1)` will find the root artist and all of their related artists, while `getDepthEdges(artistId,2)` will find the root artists, all of their related artists, and *then* the related artists of each of the first batch of related artists.

To illustrate, imagine that `getRelatedArtists('A')` returns two related artists `['B','C']`, and that each of those two artists themselves had two related artists: `getRelatedArtists('B') == ['D','E']` and `getRelatedArtists('C') == ['F','G']`.
Then `getDepthEdges('A',1)` would return the list `[('A','B'), ('A','C')]`,
and `getDepthEdges('A',2)` would return the list `[('A','B'), ('A','C'), ('B','D'), ('B','E'), ('C','F'), ('C','G')]` (and so-on for depths 3, 4, ...).

One thing to consider when writing this function is that your search may turn up the same edge twice: if artist A is related to artist B and artist B is related to artist A, you may end up finding the edge (A,B) more than once.
Make sure your list of edges only lists each edge once, with no duplicates.

*NOTE: you should take care to realize that with each added layer of depth, you will be making 20x more calls to Spotify. This means that if you get 20 related artists and 20 related artists per related artist (depth=2), that's 420 (20 + (20 * 20)) calls. A depth of 3 will mean over 8000 calls!*

### 3. Edge lists as Pandas DataFrames
Create a wrapper function called `getEdgeList(artistID, depth)` that takes the exact same arguments as `getDepthEdges()`, but returns the result as a Pandas DataFrame with one row for each edge.
If `getDepthEdges()` returns a list of 305 tuples, `getEdgeList()` should return a data frame with 305 rows and two columns.
This should be a simple function that just calls `getDepthEdges()` and then loads the results into a data frame.

### 4. Write to CSV
Write one final function in this file called `writeEdgeList(artistID, depth, filename)` that takes three arguments: an artist ID, a depth value, and a filename for output.
This function should generate an edge list based on the parameters `artistId` and `depth`, and write that to a CSV file specified by the `filename` parameter.
You will probably want to use the `getEdgeList()` function along with the Pandas DataFrame method `.to_csv` to accomplish this. (Note: use the parameter `index=False` to the `to_csv` method to avoid writing out the row number as a separate column, which Pandas does by default.)

If this all works, consider committing your progress so far and pushing to the github repository by typing these commands at the command line:

 * `git add artistNetworks.py`
 * `git commit -m "Finished Part I"`
 * `git push origin master`


## Part II. Simple network analysis
Put the functions defined in questions II.1 through II.5 in a file called `analyzeNetworks.py`

### 1. Read edge lists from CSV
Write a function called `readEdgeList(filename)` that takes one argument (a filename) and reads an edge list from a CSV with that filename, using the `read_csv()` function of Pandas.
It should return a Pandas DataFrame with one row for each edge.
The function should also make sure that the CSV it reads contains only two columns.
If it contains more than two columns, print a warning and return a data frame that contains only the first two columns.

### 2. In-degree and out-degree
In network terminology, a node's 'degree' is simply the number of edges that are attached to that node.
Degree is often used as a simple measure of centrality — nodes with high degree are assumed to be more central to the network.
For directed networks, the degree can be broken up into "in-degree", or the number of edges pointing from other nodes to the node in question, and "out-degree", or the number of edges pointing out from that node.
In the case of our related-artists network, edges point from the artist in question to the that artist's related artists (those returned your `getRelatedArtists` function).

Write a function called `degree(edgeList, in_or_out)` that takes two arguments: an edge list as returned by `readEdgeList`, and a string that is either `"in"` or `"out"`.
This function should use the `value_counts()` method of Pandas data frame columns to return the in-degree or out-degree (as specified by the second argument `in_or_out`) for all nodes in a given edge list. 
(Here we consider each directed edge to be pointed _from_ the node in the first column _towards_ the node in the second column.)

(Note that `value_counts()` is a method on the data type `Series`, which is the Pandas data type for columns in a data frame. So you can't call `value_counts()` on a data frame directly. If your data frame is called `df` and the two columns are called `artist1` and `artist2`, try `df['artist1'].value_counts()`).


### 3. Combine edge lists
As long as two networks have no nodes that are not connected to any other nodes (this type of node is called an "isolate"), then merging two networks together is as simple as combining their edge lists.
Define a function `combineEdgelists(edgeList1, edgeList2)` that takes two data frames as arguments and combines them into one long edge list.
The returned data frame should have every row that either of the two input data frames has, but it should not have any duplicate rows (the data frame returned by your function should have no duplicate rows). The DataFrame method `.drop_duplicates()` will help ensure this.

### 4. NetworkX
There is only so much network analysis that can be done using edge lists.
Make a function named `pandasToNetworkX(edgeList)` that creates a NetworkX Digraph (directed graph) from of an edge list in a pandas data frame.

Note: 
 * The Pandas DataFrame method `.to_records()` will convert a data frame into a list-like object containing a tuple for each row.
 * Here is the [networkx webpage](http://networkx.github.io/documentation/networkx-1.9.1/) and the [networkx documentation](http://networkx.github.io/documentation/networkx-1.9.1/).
 * Make sure to put the line `import networkx as nx` at the top of your script to use the `networkx` methods (e.g. `nx.DiGraph()`).
 * See the [slides from Tuesday February 12th](http://cfss.uchicago.edu/slides/w6_d2_networks.pdf) for examples of using `networkx`.
 
### 5. Picking a central node
To create a Spotify-like playlist generator, we will need a method to pick a random node from a related-artists network that is biased toward picking more central nodes over those on the network's periphery.
To this end, make a new function called `randomCentralNode(inputDiGraph)` that takes a NetworkX DiGraph as its only argument and returns a single node from that network.
The function should:

 * a) Use `the function networkx.eigenvector_centrality()` (or `nx.eigenvector_centrality()`, depending on how you imported `networkx`) to find the eigenvector centrality for each node in the network. (You can pass the entire DiGraph to this function, and it will return a dictionary mapping nodes to eigenvector centrality.)
 * b) *Normalize* the returned centrality scores so that they sum to 1. (One way to do this is to create a new dictionary similar to the one returned by `nx.eigenvector_centrality()`,
 except with each value divided by the sum of all the original values.)
 * c) Use the function `numpy.random.choice()` to randomly choose one node from a list of your nodes, using normalized centrality scores as the probabilities (i.e. the `p` argument to the `choice` function).
    * So for example, if your dictionary of nodes and normalized centrality scores is called `nc_dict`, you can type `numpy.random.choice(nc_dict.keys(), p=nc_dict.values())` to get a random
 node with a probability proportional to its centrality.
    * (Make sure you `import numpy` to use the `numpy.random.choice` function.
 * d) Return just that node (which should be an artist ID string).

And if this all works, consider committing your progress so far and pushing to the github repository by typing these commands at the command line:

 * `git add analyzeNetworks.py`
 * `git commit -m "Finished Part II"`
 * `git push origin master`


## Part III. Put it all together

### 1. Write a playlist generator
Make a script called `makePlaylist.py` that takes any number of artist names as command-line arguments and which writes a file called `playlist.csv` that lists 30 songs (as given by artist name, album name, and track name).
   * Remember that to read command-line arguments, look at the variable `sys.argv` (you must `import sys` at the top of your script).
* `makePlaylist.py` should import the functions from `artistNetworks.py`, `analyzeNetworks.py`, and possibly your scripts `fetchArtist.py` and `fetchAlbums.py` from assignment 5.
   * (This means, e.g., putting lines like `from artistNetworks import *` at the top of the script.)
* The script should fetch networks for each artist specified at the command line (to a depth of 2), combine their related-artist networks into one network, and sample 30 artists from that network using `randomCentralNode`.
(This list may have repeats of the same artist, much as in real computer-generated playlists)
* For each artist in this list, use the Spotify API (specifically, [this albums endpoint](https://developer.spotify.com/web-api/get-artists-albums/) and [this tracks endpoint](https://developer.spotify.com/web-api/get-albums-tracks/)) to pick a random album by that artist, and a random track from that album.
* The output file `playlist.csv` should have three columns: `artist_name`, `album_name`, and `track_name`.

Finally, submit this last script to github just as in Part I and Part II. We will pull down whatever code you have submitted before class on Thursday, February 19th at 1:30pm.

Similarly to assignment 5, we included a test suite to check your functions. You run it the same way (with `python tests.py` at the command shell), and the output should look something like this:
```
.......
----------------------------------------------------------------------
Ran 7 tests in 71.530s

OK
```

You can also run the tests individually, one at a time, by calling `from tests import *` from within IPython, and calling the functions inside `tests.py` yourself, interactively.
