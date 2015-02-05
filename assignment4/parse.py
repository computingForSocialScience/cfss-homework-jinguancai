
# coding: utf-8

# In[ ]:

import csv
import sys

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)




### enter your code below
def latlong ():
    n = len(readCSV("permits_hydepark.csv"))
    k = readCSV("permits_hydepark.csv")
    sum_latitude = 0
    sum_longtitude = 0
    for i in k:
    	sum_latitude += float(i[-3])
    	sum_longtitude += float(i[-2])
    avg_latitude = float(sum_latitude/n)
    avg_longitude = float(sum_longtitude/n)
    print (avg_latitude,avg_longitude)

def hist():
    import matplotlib.pyplot as plt
    import numpy as np 
    n = len(readCSV("permits_hydepark.csv"))
    k = readCSV("permits_hydepark.csv")
    zipcode = []
    z = [28,35,42,49,56,63,70]
    for i in k:
        for t in z:
            if i[t] != '':
                j = int(i[t][:5])
                zipcode.append(j)    
        
    #print zipcode    
    plt.hist(zipcode, bins=50)
    plt.savefig("histogram.jpg")

if sys.argv[1] == "latlong":
    latlong()
elif sys.argv[1] ==  "hist":
    hist()