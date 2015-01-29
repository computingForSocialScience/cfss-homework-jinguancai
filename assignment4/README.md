# Assignment 4: Cleaning City Data/Shell Scripting/Python Scripting

## Part 0. Overview
Sean Hogan's [Intro to Unix](http://csil.cs.uchicago.edu/assets/unix_i.pdf) document will be a good reference throughout this assignment.

### Accessing a *Shell*
To access a shell on OS X, run the Terminal program, accessible via the `Utilities/` subdirectory of the `/Applications` directory.

To access a shell on Windows, run the Cygwin terminal, which (if you installed Cygwin successfully) should be available from your Windows desktop. 

To access a shell with Windows/Vagrant (if you installed Vagrant), run `vagrant ssh`. 

### Basic Shell Commands
`ls`: List all directories in the current working directory. 

`pwd`: Print current working directory. 

`cd [directoryname]`: Change directory to a directory called `directoryname`.

`grep [expression] [filename(s)]`: search for a specified string or regular expression in one or mor files.


## Part 1. Setup

### 1.0: Git setup
First you will need to clone the repository of
files for this assignment from github. To do so, use the command shell
to first navigate to the directory on your computer (using `cd`) where
you want the local copy of the repository to be stored.

For example, you can create a `cfss` directory as a subdirectory of
your home directory; on OS X this would be `/Users/[username]/cfss`,
and on Windows 7 this would be `C:\Users\[username]\cfss` (Note: from
the Cygwin terminal, this directory is equivalent to
`/cygdrive/c/Users/[username]`).

Then, once you've changed to this directory at the terminal using
`cd`, type the command `git clone https://github.com/cfss/2015` to
make a local copy of the assignment repository. Switch into the newly
created `2015` directory using `cd`. (This directory is a "clone" of
the directory in the main repository.)

To confirm that this worked, type `git status`; it should say `On
branch master / Your branch is up-to-date with 'origin/master'`.

### 1.1: Download building-permit data
For this assignment we will be using data from the City of Chicago data portal consisting of data on
all of the building permits issued by the city since 2006. We will be
accessing a subset of the data as a CSV (comma-separated values) file, but it is
useful to first examine the structure of the data in your browser at 
[City of Chicago data portal Building Permits](https://data.cityofchicago.org/Buildings/Building-Permits/ydr8-5enu).

At your command line, download our curated Building Permits subset .csv file by typing the command:

`wget http://cfss.uchicago.edu/data/permits.csv`

(If you're on Windows and don't have `wget`, you can try to install it from the Cygwin `setup.exe` or just [right-click to download our csv directly](http://cfss.uchicago.edu/data/permits.csv).

Now type `git status` and you'll see that it suggests that you'll need
to add the file to git. However, because of the large size of the
file, we'd prefer if you didn't do this. (You can check the size of
the file using the command `du -h permits.csv`.) Instead, create a
`.gitignore` file by typing `touch .gitignore` and then opening it in
the text editor of your choice (e.g. SublimeText or TextWrangler).

### 1.2: `.gitignore` 
The `.gitignore` file tells git to ignore any
file in the repository whose name matches a certain pattern. Each line
of the `.gitignore` file is a separate
pattern. [Here is an example python .gitignore](https://github.com/github/gitignore/blob/master/Python.gitignore). However,
you will not need such a complicated file. Instead, simply add two
entries to your empty `.gitignore` file: The first should be
`permits.csv` and the second should be `*.pyc`. This tells git to
ignore all python-bytecode (.pyc) files.

Now add your .gitignore to your repository by typing at the command line:

1. `git add .gitignore`
2. `git commit -m "adding gitignore"`


## Part 2. Basic finding using grep, wc. 
Okay, now that we have have an environment set up to do data analysis,
write a shell script (.sh) file that does the following two things
with the permit data you downloaded above. (A shell script is simply a
set of shell commands in a text file. You can run it by typing `bash
script.sh` at the shell prompt.)

1. Print out how many rows are in the dataset. (consider using `wc -l`)
2. Find all rows with the string "Hyde Park" in them and save them into a new file called `permits_hydepark.csv`. (consider using `grep` and the `>` operator)

Add this script to git by using the commands above (`git add`/`git commit`) but with different arguments. 


## Part 3. Python scripting
Shell scripting is a remarkably powerful tool, but we've only really scratched the surface. However, often for ease-of-use/utility purposes, you will turn to Python scripting. To run a Python script, you simply type `python filename.py`. Your git repository should have a Python script called `parse.py` that contains a function to read CSV files. Edit this script, utilizing the functions provided, to do the following:

### 3.1 Latitude and Longitude
Write a Python function `get_avg_latlng()` that computes the average latitude and longitude of construction permits in Hyde Park and prints it to the console.

### 3.2 Histograms
Write another Python function `zip_code_barchart()` that plots and saves
as a `.jpg` a bar chart of contractor zip codes.

### 3.3 Combine into an executable program

The python module `sys` allows you to access command arguments. For
example, `sys.argv[0]` is a way of accessing a command line argument
that, if you print it out, will be the name of the script; `sys.argv[1]`
corresponds to the first argument, `sys.argv[2]` the second argument, etc.

Using the contents of the value `sys.argv[1]`, write a combined script
that either (1) prints the mean latitude and longitude to the console
if given the command-line argument `latlong` (i.e., `python parse.py
latlong`) or (2) creates the histogram if given the command-line
argument `hist` (i.e., `python parse.py hist`).

## Part 4. Commit and push to github

A good motto is to commit early and often. To do this, run `git pull
origin master` (to get any changes from origin/master, i.e. github)
and then `git push origin master` to send your changes back. Unless we
hear otherwise from you, **we will be grading the last version of your
assignment that was committed to github before the deadline**!
