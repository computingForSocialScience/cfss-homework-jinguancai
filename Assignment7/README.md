# Assignment 7: Databases and Websites

## Part 0: Background and setup

In this assignment, you will expand on the Spotify interface you worked on in assignments 5 and 6, adding a database to keep track of playlists and songs as you create them and a web interface to create and view those playlists and songs.

To get started you will need to have a MySQL server running on your computer. MySQL is a separate program that allows you to both run a database (server) and to access that server (client). If you have not installed MySQL, follow the [instructions on Piazza](https://piazza.com/class/i4k3cl3eddt1vl?cid=196) posted last week. If you are using Mac OS X, you may need to type `mysql.server start` at the command line to make sure your server is running (if you are using Microsoft Windows, your server is probably already running). If your server is running, the database connection code at the top of the `app.py` file included with the assignment should work without any errors. If you set a root password when you were setting up MySQL, make sure you change the definition of `passwd` to be your password instead of an empty string.

You will also need to create a new database for the assignment called `playlists`. You can do this at the MySQL command prompt with the statement `CREATE DATABASE playlists;` (remember to include the semicolon). (You can start to the MySQL command prompt using a command like `mysql -u root -p` at the Unix command line).

Your database should have two tables, one that represents playlists and another that represents songs. These will look something like this:

#### `playlists` table

<table>
<tr><th>id</th><th>rootArtist</th></tr>
<tr><td>1</td><td>Loretta Lynn</td></tr>
<tr><td>2</td><td>Patti Smith</td></tr>
<tr><td colspan=2 style='text-align:center;vertical-align:middle'>...</td></tr>
</table>

#### `songs` table

<table>
<tr>
    <th>playlistId</th>
    <th>songOrder</th>
    <th>artistName</th>
    <th>albumName</th>
    <th>trackName</th>
</tr>
<tr>
    <td>1</td>
    <td>1</td>
    <td>Johnny Paycheck</td>
    <td>I'm Not Looking Back Anymore</td>
    <td>Greater Love Have No Man 2</td>
</tr>
<tr>
    <td>1</td>
    <td>2</td>
    <td>Tammy Wynette</td>
    <td>The Definitive Tammy Wynette Collection</td>
    <td>Making Love (Live)</td>
</tr>
<tr>
    <td>1</td>
    <td>3</td>
    <td>Dwight Yoakam</td>
    <td>3 Pears</td>
    <td>Long Way To Go - Reprise</td>
</tr>
<tr><td colspan=5 style='text-align:center;vertical-align:middle'>...</td></tr>
<tr>
    <td>2</td>
    <td>1</td>
    <td>Iggy Pop</td>
    <td>Blah-Blah-Blah</td>
    <td>Blah-Blah-Blah</td>
</tr>
<tr>
    <td>2</td>
    <td>2</td>
    <td>Lou Reed</td>
    <td>Between Thought And Expression</td>
    <td>Kill Your Sons</td>
</tr>
<tr>
    <td>2</td>
    <td>3</td>
    <td>T. Rex</td>
    <td>The Slider</td>
    <td>Mystic Lady</td>
</tr>
<tr><td colspan=5 style='text-align:center;vertical-align:middle'>...</td></tr>
</table>

In the table `songs`, the first column (`playlistId`) indicates which playlist the song is associated with, while the second column (`songOrder`) specifies the order of the songs in that playlist. This way you can use the `WHERE` clause in an SQL `SELECT` query to get only the songs associated with a particular playlist ID, and the `ORDER BY` clause in that same query to make sure the songs are returned in the right order.

## Part I: Populating tables

The first step is to make a function that creates playlists and adds the appropriate rows to the tables in the database.

In the file `app.py`, create a function called `createNewPlaylist` that takes a single artist's name as its only argument and adds a 30-song playlist to your database. This function should mimic the behavior of the script `makePlaylist.py` from assignment 6, except that it will take its argument as a string in python instead of as a command-line argument, and it will put its output into the MySQL database instead of a CSV file. It also only needs to be able to handle one artist at a time, so there is no need to create and combine multiple edgelists. For instance, calling `createNewPlaylist("Patti Smith")` should fetch the related-artist network for Patti Smith to a depth of two, create random a playlist with thirty songs in it based on the centrality of the artists in that network, and add the information about this playlist to your MySQL database. For details, see the instructions from assignment 6.
(Feel free to copy any necessary files, like `fetchArtist.py`,  `fetchAlbums.py`, and `artistNetworks.py` from the previous assignments into this directory — just remember to use `git add` to add them to the repository so that we will have them for grading.)

`createNewPlaylist` should do the following things:

* Create the two tables in the database if they are not already there. You can do this by adding "`IF NOT EXISTS`" to an SQL create-table statement (e.g. `CREATE TABLE IF NOT EXISTS playlists (...)`). Look in the lecture slides (or [this part of the MySQL Tutorial](http://dev.mysql.com/doc/refman/5.7/en/creating-tables.html), as well as the somewhat obtuse [MySQL "CREATE TABLE Syntax" documentation](https://dev.mysql.com/doc/refman/5.1/en/create-table.html)) for help constructing your create-table statements.
* Add the artist's name to the `playlists` table and get the playlist ID associated with the new row (this will probably involve an `INSERT` statement to add the row to the table, followed by a `SELECT` statement to get the ID).
* Add the songs to the `songs` table, with the appropriate playlist ID in the `playlistId` column of the new rows and the appropriate order in the `songOrder` column.

The easiest way to see if your function is working is to use the MySQL command-line client to query the database. Connect to it using a command like `mysql -u root -p` at the command line. You can see an entire table with `SELECT * FROM playlists;`, or just the first five rows with `SELECT * from playlists limit 5;`. At any point you can delete everything you have added to the tables by dropping them from the database using `DROP TABLE playlists;` and `DROP TABLE songs;`. The next time you run your function it should create the empty tables again. (Remember that MySQL won't execute your commands if you don't end them with a semicolon ";")

Before you move on to part II, make sure your database has at least two playlists in it so that you will have something to experiment with.

**This is probably a good time to use `git add [your filenames]` and `git commit -m "[your message]"` to save your work so far.**


## Part II: List the playlists

Next you will use [Flask](http://flask.pocoo.org/) to create a web page that lists all of the playlists in your database. The `app.py` file you were given has a template function called `make_playlists_resp` (the `@app.route('/playlists/')` above this function is a "decorator" which tells Flask to run this function whenever someone goes to an address like `http://127.0.0.1:5000/playlists/`). You were also given an empty template `templates/playlists.html` ('playlists' plural) that you should use here.

* Add to the `make_playlists_resp` function so that it fetches all of the playlists and playlist IDs from your database and stores them in a variable called `playlists`. The call to the `render_template` function specifies that you will make this variable available to the `playlists.html` template.
* Fill out a Jinja2 template `playlists.html` (see the lecture slides for details) so that it will create a web page with links to each playlist. The playlist links should look like `/playlist/{playlistId}` (e.g. `<a href="/playlist/2">2. Patti Smith</a>`).

Test your function by running the app (`python app.py`) and visiting the address [http://127.0.0.1:5000/playlists/](http://127.0.0.1:5000/playlists/) in your web browser. You can use control-C at the command line to stop the app and server.

**This is probably a good time to use `git add [your filenames]` and `git commit -m "[your message]"` to save your work so far.**


## Part III: List the songs in the playlists

Now you will fill out the function `make_playlist_resp` in `app.py` so that it lists the songs in any playlist in your database. The Flask route `@app.route('/playlist/<playlistId>')` directly above the function tells Flask to call this function any time someone visits an address like `http://127.0.0.1:5000/playlist/14`. The `<playlistId>` part of the route tells Flask to use whatever is in that part of the address as the argument to the function. So when someone goes to `http://127.0.0.1:5000/playlist/14`, Flask will invoke the function like so: `make_playlist_resp(playlistId=14)`. You were also given an empty template `templates/playlist.html` ('playlist' singular) that you should use here.

* Add to the `make_playlist_resp` so that it fetches the `songOrder`, `artistName`, `albumName`, and `trackName` of each song in the playlist in order, and stores them in a variable called `songs` (notice that `render_template` passes the `songs` variable along to the template). Make sure that you only get songs with the right value of `playlistId`, and that they are in the right order.
* Fill out the template `playlist.html` so that it creates an HTML table where each row is a song in the playlist. The table should list the number, artist, album, and title for each track (4 columns).

If your app is running, you can test this by either going straight to a playlist address that you know exists (e.g. [http://127.0.0.1:5000/playlist/1](http://127.0.0.1:5000/playlist/1)) or by going to the playlist index that you wrote in part II ([http://127.0.0.1:5000/playlists/](http://127.0.0.1:5000/playlists/)) and clicking any of the links.

**This is probably a good time to use `git add [your filenames]` and `git commit -m "[your message]"` to save your work so far.**




## Part IV: Adding new playlists from the browser

Now you will make a simple interface so that new playlists can be added to the database directly. The function `add_playlist` is a basic template for how to do this. (We will talk a little bit in class about how web forms with user input work)

* The first block of code (under "`if request.method == 'GET':`") is the code that will be run when a person visits the page `http://127.0.0.1:5000/addPlaylist/`. We created a static template for you in `templates/addPlaylist.html` which you should not need to change. Do examine it though. It contains an HTML form that allows a user to enter an artist's name in a text field (named `artistName`) and click a button that sends that data to your app. This is a very simple form, so make sure you understand how it works. (The forms in your final projects will probably be more complex than this.)
* The second block of code, under "`elif request.method == 'POST':`", is the code that will be run once someone clicks the button to submit a new artist and create a new playlist. The line `artistName = request.form['artistName']` retrieves the value of `artistName` from the form and saves it as a python variable. the line `return(redirect("/playlists/"))` will then send the browser to the playlist index page you made in part II. Between these two (where it says `# YOUR CODE HERE`), add code that uses the function you wrote in part I to create a new playlist and add it to the database (this should be a one-liner).


## Turn it in

This assignment is **due Thurday, March 12 by 1:30pm, and there will be no extensions**.

Use `git add`, `git commit` and `git push origin master` to turn your code in. Note that this will only submit in your code, not the contents of your MySQL database. To grade this, we will be using our own, local database test the functionality.
