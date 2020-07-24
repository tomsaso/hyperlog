# hyperlog
This is proof-of-concept implementation of the hyperloglog algorithim. The algoritham aim is to overcome the memory problem when counting the distinct items in a data set. Namely, in order to check whether you have already seen an element when counting items in a data set you would have to keep a list of seen items in memory. This becomes a problem when working with Big Data. The way to solve this, although not completly and exactly, is by estimaing the number of unique elements in a data set by doing probablity calculations on the items binary represantion. The implementation is done with pandas, although that would not be relevant for big data sets, it is still onyl a proof-of-concept.

Data drive link (400MB) https://drive.google.com/open?id=1ApALDf05xIMmGZgT2EK1xwJ4Oxd0CvBb
