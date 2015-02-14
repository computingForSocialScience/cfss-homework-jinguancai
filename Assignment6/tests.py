# coding=utf-8

import unittest
import nose
from artistNetworks import *
from analyzeNetworks import *
import pandas as pd
from collections import Counter
import networkx as nx
import os
import unicodecsv
import random

def testRelatedArtists():
    rList = getRelatedArtists(u'2I1CyuXXtqhYCgX1blMfDg')
    # check that 20 artists are being returned
    assert len(rList) == 20
    # check the length of a random related Artist ID
    assert len(random.choice(rList)) == 22


def testWriteEdgeList():
    rootId = '4EF5vIcCYKMM61oYOG2Tqa'
    writeEdgeList(rootId,2,'testEdgeList.csv')

    with open('testEdgeList.csv','r') as f:
        f.next()
        edges = []
        for l in f:
            lsplit = [i.strip('"\'') for i in l.strip().split(',')]
            edges.append(tuple(lsplit))
    # make sure that at least 20 edges start from root artist
    assert Counter([i for (i,j) in edges])[rootId] == 20
    # check that a random edge looks right
    rEdge = random.choice(edges)
    assert type(rEdge) == tuple # each edge should be a tuple
    assert len(rEdge) == 2 # each edge should have exactly two items in it
    assert len(rEdge[1]) == 22 # each artistId should have 22 characters in it
    # check that there are no duplicate edges
    assert len(edges) == len(set(edges))


def testDegree():
    df = readEdgeList('testEdgeList.csv')

    # the seed artis id should have exactly 20 out-edges
    assert degree(df,'out')['4EF5vIcCYKMM61oYOG2Tqa'] == 20


def testCombineEdgeLists():
    baseDF = readEdgeList('testEdgeList.csv')
    df1 = baseDF[0:100]
    df2 = baseDF[50:150]
    df1.columns = df2.columns

    comb = combineEdgeLists(df1,df2)
    # df1 and df2 have 50 rows in common, so comb
    # should get rid of duplicates and have only 150 rows
    assert len(comb) == 150

    # check explicitly for duplicates
    assert str(comb) == str(comb.drop_duplicates())


def testPandasToNetworkX():
    df = readEdgeList('testEdgeList.csv')
    g = pandasToNetworkX(df)
    # make sure the graph looks right
    assert g.is_directed() # graph must be directed (DiGraph)
    assert len(random.choice(g.nodes()))==22 # nodes should be 22-character artisIDs
    assert '4EF5vIcCYKMM61oYOG2Tqa' in g.nodes() # the root artist should be in the graph
    assert g.out_degree()['4EF5vIcCYKMM61oYOG2Tqa']==20 # the root artist should have out-degree of 20

    # this will fail if any of the edges point to themsleves
    # e.g. ('6UY2yCOBXcmlI0BEbo2emE', '6UY2yCOBXcmlI0BEbo2emE') 
    assert len(g.selfloop_edges()) == 0


def testRandomCentralNode():
    df = readEdgeList('testEdgeList.csv')
    g = pandasToNetworkX(df)

    # make sure randomCentralNode is actually a node in the graph
    assert randomCentralNode(g) in g.nodes()

    # the following few lines sample 500 random nodes, getting
    # the most- and least-frequently chosen ones.
    # if the random sampling is being done right, then the
    # eigenvector centrality of the most-frequent node should be
    # larger than that of the least-frequent node (with high probability)
    smpl = Counter([randomCentralNode(g) for i in xrange(500)])
    top,topCount = smpl.most_common()[0]
    btm,btmCount = smpl.most_common()[-1]
    evc = nx.eigenvector_centrality_numpy(g)
    # this could fail by chance every once in a while
    # but it should be very rare
    assert evc[top] > evc[btm]


def testMakePlaylist():
    os.system('python makePlaylist.py "КОФЕ"')

    f = open('playlist.csv','r')
    reader = unicodecsv.reader(f)
    header = reader.next()
    rows = []
    for line in reader:
        rows.append(line)

    # check the number of rows
    # (We are assuming the CSV has one header row and 30 data rows)
    assert len(rows) == 30
    # check the number of columns
    # (the column count can get messed up if you don't
    # put your artist/album/track names in quotes)
    assert sum([len(r) for r in rows]) == 90
        

if __name__ == '__main__':
    nose.main()
