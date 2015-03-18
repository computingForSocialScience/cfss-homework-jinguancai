import pandas as pd
import matplotlib.pyplot as plt
import sys
import csv
import datetime
import time
import re
import sys
import numpy as np
from io import open
from sklearn.cluster import KMeans
from sklearn import datasets
from urllib import urlopen
from numpy import vstack,array
from scipy.cluster.vq import kmeans,vq,whiten
from sklearn.cluster import MeanShift
from sklearn.datasets.samples_generator import make_blobs

#set data directory
directory = '20060922.csv'

#set parameters
DATE = directory[-12:-4]
ini_time = datetime.datetime(2006,9,22,9,00,0)
stop_time = datetime.datetime(2006,9,22,19,30,0)
delta = datetime.timedelta(minutes=30)
min_volume = 100
#BIDOFR = 'BIDSIZ'
BIDOFR = 'OFRSIZ'
ini_colors = 10*['r','g','b','c','k','y','m']



"""function that readdata into dataframe"""
def readdata(directory): 
    data_df = pd.read_csv(directory,encoding='utf-8',parse_dates={'DATETIME':[1,2]},keep_date_col=True) #use second and third column as datetime
    data_df['MMID'] = data_df['MMID'].fillna('NONMM') #replace the "" in MMID with NONMM(Non market maket)
    return data_df


"""function that calculate volumes for each MMID"""
def calculate_rel_trading_vol(data,ini_time,stop_time,delta,min_volume,BID_OFR):
    mminfo = {}
    #loop remember to set time, stoptime and delta, bidsize only
    for MMID in data_df['MMID'].value_counts().index:
        if float(data_df[data_df['MMID']== MMID][BID_OFR].sum()) >= min_volume: # if no total trading volume, skip this Market Maker
            mminfo[MMID] = []
            #print MMID
            time = ini_time
            while time < stop_time: #create a list of one MMID's relative trading volume
                time2 = time + delta
                #print time2
                top = float(data_df[(data_df['MMID']== MMID)&((data_df['DATETIME']>time)&(data_df['DATETIME']<=time2))][BID_OFR].sum())
                bottom = float(data_df[data_df['MMID']== MMID][BID_OFR].sum())
                volume = top/bottom
                mminfo[MMID].append(volume)
                #print volume
                time = time2
    return mminfo

def calculate_cum_trading_vol(data,ini_time,stop_time,delta,min_volume,BID_OFR):
    mminfo = {}
    #loop remember to set time, stoptime and delta, bidsize only
    for MMID in data_df['MMID'].value_counts().index:
        if float(data_df[data_df['MMID']== MMID][BID_OFR].sum()) >= min_volume: # if no total trading volume, skip this Market Maker
            volume = 0
            volume2 = 0
            mminfo[MMID] = []
            #print MMID
            time = ini_time
            while time < stop_time: #create a list of one MMID's relative trading volume
                time2 = time + delta
                #print time2
                top = float(data_df[(data_df['MMID']== MMID)&((data_df['DATETIME']>time)&(data_df['DATETIME']<=time2))][BID_OFR].sum())
                bottom = float(data_df[data_df['MMID']== MMID][BID_OFR].sum())
                volume = top/bottom
                volume2 += volume
                if volume2 > 1: # in case we have 1.0000001
                	volume2 = 1
                mminfo[MMID].append(volume2)
                #print volume
                time = time2
    return mminfo

"""function that checks if the total trading volume adds up to 1"""
def vol_check (data):
	sum_check = {}
	for i in data:
	    #print i
	    #print mminfo_rel[i]
	    sum_check[i] = sum([j for j in mminfo_rel[i]])
	assert int(sum_check[i]) == 1 or int(sum_check[i])


"""function that creates time column names"""
def create_time_bins(ini_time,stop_time,delta):
	time_column = []
	time = ini_time
	while time < stop_time:
	    time = time + delta
	    time_column.append(time)
	return time_column

"""function that creates graph for trading lines (input is a cumulative mminfo dataframe"""
def graph_trading_lines(mminfo_cum_df,filename):
	y = mminfo_cum_df.transpose()
	y.plot()
	plt.legend(loc='lower right')
	plt.title("Trading Volume Line for %s" %(filename))
	plt.show()
	#plt.savefig('%s.jpg' % (filename))

def exportmminfodata(mminfo_cum_df,filename):
    mminfo_cum_df.to_csv('%s.csv'%(filename))

def MeanShiftClassification(data):
    ms = MeanShift()
    ms.fit(data.values)
    labels = ms.labels_
    #print labels
    cluster_centers = ms.cluster_centers_
    #print (cluster_centers)
    n_clusters_ = len(np.unique(labels))
    #print ("Number of estimated clusters:",n_clusters_)
    return {'cluster_centers':cluster_centers,'labels':labels,'n':n_clusters_}

def graph_Result(data,filename,labels,ini_colors,method):
    colors = [ini_colors[i] for i in labels ]
    #print colors
    y= data.transpose()
    y.plot(color=colors)
    plt.legend(loc='lower right')
    plt.title("Trading Volume Line for %s after %s Classification" %(filename,method))
    plt.show()
    #plt.savefig('%s.jpg' % (filename))

def Kmeansclustering(data,k):
     centriods, _ = kmeans(data.values,k)
     idx, _ = vq(data.values,centriods)
     #print idx
     #print centriods, _
     return {'centriods':centriods,'labels':idx}

def graph_patterns(cluster_centers,filename):
    pattern = {}
    j = 1
    for i in cluster_centers.tolist():
        pattern['pattern %s'%(j)]=i
        j += 1
    y = pd.DataFrame(pattern,index=time_column)
    y.plot()
    plt.legend(loc='lower right')
    plt.title("Pattern for %s" %(filename))
    plt.show()
    #plt.savefig('%s.jpg' % (filename))



data_df = readdata(directory)
mminfo_rel = calculate_rel_trading_vol(data_df,ini_time,stop_time,delta,min_volume,BIDOFR)
mminfo_cum = calculate_cum_trading_vol(data_df,ini_time,stop_time,delta,min_volume,BIDOFR)
time_column = create_time_bins(ini_time,stop_time,delta)
mminfo_cum_df = pd.DataFrame.from_dict(mminfo_cum, orient="index")
mminfo_cum_df.columns = time_column 
graph_trading_lines(mminfo_cum_df,DATE)

"""Kmeans Method"""
#k = 3 #k for k means
#labels = Kmeansclustering(mminfo_cum_df,k)['labels']
#graph_Result(mminfo_cum_df,DATE,labels,ini_colors,'KMeans')
#cluster_centers = Kmeansclustering(mminfo_cum_df,k)['centriods']
#graph_patterns(cluster_centers,'KMeans')

"Meanshift Method"
cluster_centers = MeanShiftClassification(mminfo_cum_df)['cluster_centers']
graph_Result(mminfo_cum_df,DATE,labels,ini_colors,'Meanshift')
labels = MeanShiftClassification(mminfo_cum_df)['labels']
graph_patterns(cluster_centers,'MeanShift')



#exportmminfodata(mminfo_cum_df,DATE)
#print mminfo_cum_df.values