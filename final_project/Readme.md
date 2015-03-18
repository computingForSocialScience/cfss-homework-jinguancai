This final project is part of my thesis. It takes the NYSE Trade and Quote consolidated trading quotes data from wharton's research database as input and it analyze the change of the trading volumes for each market maker with a distinct "market maker ID". Then, it cleans the data and calculates the cumulative trading volume for each Market Maker. Using the cumulative trading volume data, it then performs a cluster analysis to find quotes patterns among market makers and lastly it assigns each market maker a pattern and generates a graph. 

For the clustering analysis, I use both KMeans and MeanShift. The Kmeans works for all the sample that I randomly choose but the MeanShift does not for some reason. However, both Kmeans and MeanShift work for the OFR data in 20060922 Offer quotes if one needs to see a full demo.



