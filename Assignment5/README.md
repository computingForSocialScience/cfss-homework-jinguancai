# CFSS Assignment 5: Scraping Spotify

In this assignment you will use the API from [http://www.spotify.com](Spotify), the
London/Stockholm-based commercial streaming music service, to find information
about your favorite artists and their albums. Then, you'll write out that data
to separate `.csv` files just as you might if you were (ultimately) constructing
your own personal music metadata database.


## Part 1: Collecting Artist Data from Spotify


We've given you a file, `fetchArtist.py`, which has stub functions
called `fetchArtistId(name)` and `fetchArtistInfo(id)`.
(The stub functions use the `pass` keyword to tell Python that the
function body is empty and the function does nothing. You should
delete the line that says `pass` when you fill the functions in.)

The former function, given a name of an artist/band, such as
`'Chumbawamba'` or `'Beyoncé'`, will return what Spotify calls a
"Spotify ID", which is part of a "Uniform Resource Identifier" or
"URI". For example, the Spotify ID for the artist Patti Smith is
`'0vYkHhJ48Bs3jWcvZXvOrP'`. (In a perfect world, this would uniquely
identify Spotify resources related to Patti Smith for all time.  In
reality -- and much like URLs -- at some point in the future, after
Spotify goes bankrupt or is acquired by Google or whatever, this will
just return to being a meaningless string of characters.)

### 1.1 Getting a Spotify artist ID given an artist name: `fetchArtistId()`

Your first task is to implement the `fetchArtistId(name)`
function. You should consult the Spotify documentation, including the
main [Web API User
Guide](https://developer.spotify.com/web-api/user-guide/), especially the
[Endpoint
Reference](https://developer.spotify.com/web-api/endpoint-reference/).
You will be writing code similar to Assignment 3 to
connect using the `requests` library, and to grab the JSON associate
with the Spotify API website's response. (Hint: look for an API
endpoint which allows you to search for an artist by name. Then,
examine the returned JSON to find an `'id'` field. The API call
may return more than one artist, in which case your function will
need to pick just one.)

### 1.2 Getting info about an artist: `fetchArtistInfo()`

Your second task is to implement the `fetchArtistInfo(artist_id)` function,
which, given a Spotify artist ID (e.g. a string like `'0vYkHhJ48Bs3jWcvZXvOrP'` as
returned from `fetchArtistId()`), to return a dictionary which includes the following keys:

 * `'followers'` (number of Spotify followers)
 * `'genres'` (list of Spotify genres associated with the given artist)
 * `'id'` (the Spotify Artist ID)
 * `'name'` (the artist name),
 * `'popularity'` (Spotify's popularity-meter, an integer).

To do this, look in the Spotify documentation to find an API endpoint
which returns data about an artist given its Spotify ID.

## Part 2: Getting Album Data from Spotify

We now have a way to get information on an artist. Let's find out what
Spotify knows about their albums! We've given you another file,
`fetchAlbums.py`, which has stub functions called
`fetchAlbumIds(artist_id)` and `fetchAlbumInfo(album_id)`.

### 2.1 Getting Spotify album IDs given an artist: `fetchAlbumIds()`

First, write the function `fetchAlbumIds(artist_id)` which, given an
Spotify artist ID, returns the Spotify IDs associated with albums on
which that artist appears. 

**NOTE: Spotify has many duplicate entries for many albums for particular sets of
international markets, as well as compilations on which given artists appear.
We want to restrict our query to only full-length albums released directly by a
given artist (as opposed to releases of single songs, or appearances of single songs on compilations); and we also
want to restrict our query to only include the US market. This will make it
_much_ easier to examine and understand the return values from the API. _Make sure your API
query parameters include `album_type=album` and `market=US` in the URL!_**

(NOTE 2: Even once you do this, there will still be some duplicates, because of remastered versions, copies of
albums with different UPC codes, and other things that only make sense to the struggling
music distribution industry.)

### 2.2 Getting info on an album: `fetchAlbumInfo()`

Second, write the function `fetchAlbumInfo(album_id)` to get some
information about a given album ID (as returned from `fetchAlbumIds()`).
Specifically, this function should return a dictionary with the following
keys:

 * `'artist_id'`: the id of the first artist associated with a given album. (For
   most conventional LP albums, there will only be one associated
   artist.)
 * `'album_id'`: the id of the album
 * `'name'`: the album name
 * `'year'`: the year (and only the year) in which the album was released.
 You probably don't want to use the `datetime.strptime()` function (see slides from Thu 1/22/2015)
 to parse out the date, because some of the release dates just have the year. Try just
 reading the first 4 characters instead.
 * `'popularity'`: the popularity of this album (not of the artist)

## Part 3: Writing out your own CSV files

The file `csvUtils.py` has two stub functions `writeArtistTables(artist_info_list)` and
`writeAlbumsTable(album_info_list)` which you will write.

### 3.1 Writing the artist CSV file: `writeArtistsTable()`

To implement `writeArtistsTable()`: using the methods described in
the Thursday Feb 5th lecture, open a file for writing called
`artists.csv` for writing, and write out a comma-separated file
consisting of (some of) the contents of your list of artist info dictionaries
(as returned from `fetchArtistInfo()`).

The `artists.csv` file output when you execute this function should have
a header line at the top that looks like the following:

`ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY`

Unfortunately, since some of your data might have Unicode characters,
we can't recommend that you use the `csv.writer` method of the `csv`
library to write out the rows. Instead, we recommend importing the special
`open` function of the `io` library:

`from io import open`

thereby ensuring (hopefully) that all of your file writes (using the `write()` function
of the file object) can take Unicode as their input.

So specifically, to write the header, for example, you will want to write something like

`f.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')`

After this, you will loop through the list of artist dictionaries to populate the rest of the CSV file. **Because an artist's name might include a comma, make sure to format your rows with the `ARTIST_NAME` field in double quotes**. An example line from `artists.csv` should look something like this:

`6vWDO969PvNqNYHIOW5v0m,"Beyoncé",2539238,95`

Remember to close your files (using the `close()` method of file
objects).


### 3.2 Writing the albums CSV file: `writeAlbumsTable()`

To implement `writeAlbumsTable()`, you should do the
same thing as in section 3.1, but output a file called `albums.csv`,
with data from a given list of album info dictionaries (each as
returned from `fetchAlbumInfo()`).

Your header file for `albums.csv` should look like:

`ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY`

And therefore you will only need to include these parameters when populating the rest of the CSV file. Similarly to above, **an album's name might include a comma, so make sure to format your rows with the `ALBUM_NAME` field in double quotes**. An example line from `albums.csv` will look something like this:

`6vWDO969PvNqNYHIOW5v0m,6oxVabMIqCMJRYN1GqR3Vf,"Dangerously In Love",2003,74`


## Part 4: Commenting Code

We've written a script for you, `barChart.py` with two functions,
`getBarChartData()` and `plotBarChart()`. The former function, when
run in the same directory as an `artists.csv` and `albums.csv` file,
returns some data regarding the content of those files. The latter
function plots a bar chart of the count of albums released in each
decade by all the included artists.

### 4.1 Comment our Bar Chart code

First, test that this code works on the CSV files that you are generating.

Now we want you to add comments to `barChart.py` explaining what the provided code is doing,
in as much detail as you think necessary. This task is intended to give you practice in
reading undocumented code, which happens more than you'd like to think.

You'll check in the revised `barChart.py` with your added comments.


<!--Using [subplot](http://matplotlib.org/examples/pylab_examples/subplot_demo.html) in matplotlib, make a bar chart for each artist, where the x axis is the number of tracks, and the y axis is the number of albums with that many tracks. Each subplot should have the artist name in the title.  -->


## Part 5: Bringing it all together

The last part of this assignment is to take all of the code you've written and bring it together into
one standalone script which imports all of your functions, executes them given some input artist names,
and plots the bar chart.

You should be able to run this script from the command line by typing
`python main.py ArtistName1 ArtistName2 ArtistName3` (or on Cygwin,
perhaps `python -i main.py ArtistName1 ArtistName2 ArtistName3`),
where `ArtistName1` etc. correspond to the real names of musical
artists/bands. The script should work for any number of artists.

Alternatively, you can run `main.py` from *within* `ipython` by typing `%run main.py ArtistName1 ArtistName2 ArtistName3`.

If it works, you should be able to type `python main.py ArtistName1
ArtistName2 ArtistName3` as specified above, and it will run all of
the functions you've implemented so far and produce a nice graph.

### 5.1 Implementing `main.py`

Where the `main.py` script says `# YOUR CODE HERE`, you should write code using the imported functions
which:

 * Loops through the list of artist names, gets their IDs and corresponding info (using `fetchArtistId()` and `fetchArtistInfo()`).
 * Loops through the artist IDs and gets their album IDs and album info (using `fetchAlbumIds()` and `fetchAlbumInfo()`).
 * Writes out CSV files given these lists of artist info dictionaries and album info dictionaries (using `writeArtistsTable()` and `writeAlbumsTable()`.
 * Calls `plotBarChart()` to read and plot your CSV files.

## Part 6. Testing

Unit testing is today a fundamental part of code design and
development. The goal of testing is to assure yourself
that you have implemented a function in
the way you expect it to behave (or that you haven't broken anything in the last
round of changes). In this assignment, we have
distributed a test suite in `tests.py` that checks each function for
correctness. We will be using this to grade some of the assignment instead of actually
inspecting your code, so you will want to make sure to run this script and validate that it
works before your final submission!

To run the tests, simply type `python tests.py`. When you have all your code working, it should take about 30-40 seconds to fully run.

The output will look something like this if the tests all pass: 

```
.....
----------------------------------------------------------------------
Ran 5 tests in 37.583s

OK

```

If the tests do not pass, it will print out the error for the failing test(s).

Again, we will be using the test suite to grade this homework, so make sure your tests pass. 

## Part 6. Adding/Commiting and Pushing to Github

Just like in the previous assignment, you can push changed code to
github by typing `git add filename` on a given changed file,
then running `git commit -m "my message"` to log a commit message,
and `git push origin master` to push changes to the server (where you can
then see them on github.com.) We will make copies of your last update
just before class on Thursday, February 12th at 1:30pm.
