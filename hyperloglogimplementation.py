# -*- coding: utf-8 -*-
"""
This is a sample implemenation of HyperLogLog algorithm for learning and 
pratice purposes. Brief explanations are provieded each step of the code.

While HyperLogLog belongs to Big Data problems and distributed systems, here
the implemenation is to read in and count unqiue elements of a string
column of a csv file. Sample tests are done on a dataset of ip addresses.

Created by: tomsaso

"""
import os
import numpy as np
import pandas as pd
wd = os.getcwd()
FILE_NAME = wd + "\ip.csv"
def hash_string(stringToHash):
    """
    Function takes a string and retrurns fixed-lenght(64 char) string represntation
    of it's binary hashed value. Default python hash() function is used that
    returns 64-bit hash on 64bit machines. Better functions such as 128-bit md5 
    function can be used for less chance of collison. HyperLogLog recommends
    using at least 64-bit hashing function. The point of hashing is to achive
    uniformly distributed fixed-lenght pseudo-random values where 
    the same object(string) always maps to the same binary number. 
    """
    #get the hash of the string and convert to string of it's binary
    # to perform this needs to be used on 64-bit machines for the hash to be 
    #64 bit
    hashNumber = hash(stringToHash)
    hashString = bin(hashNumber)
    #check if it is negative and handle accordiling
    if hashString.startswith("-"):
        # remove sign and 0b from binary string representation
        hashString = hashString[3:]
    else:
        #remove 0b from binary string representation
        hashString = hashString[2:]
    #make the hash string fixed-lenght by adding zeroes to the left
    hashString = hashString.zfill(64)
    return(hashString)
def get_index_of_first_1(binaryString):
    """ 
    Functions retruns the index of the first 1 in a string represenation
    of a binary number 
    """
    index = binaryString.find("1")
    if index == -1:
        index = 64
        #there may be a bug here, hashing function needs to be tested
        #on diffrenet data types and values and see when it produceds 0
    return(index)

def update_buckets(elements, buckets):
  """ Function takes 2 arguments, elements which is a subset of the elements
      to count-distinct items of, and buckets which is a numpy array of lenght
      (2 to some power) minus 1. Returns updated buckets by calclating leading 
      zeroes in binary hashed string repersentation of each elment, which is
      added to appropriate bucket index"""
  binNumOfBucketsDigits = len(bin(len(buckets))[2:])
  #handle somehow bucket-array indexing(poorly, needs improvment)
  buckets = np.append(buckets,[0])
  for element in elements:
      binStr = hash_string(element)
      oneIndex = get_index_of_first_1(binStr)
      #get last binNumOfBucketDigits binary digits, convert
      #to int to use for bucket indexing
      bucketNumber = (int(binStr[-binNumOfBucketsDigits:],2))
      #update bucket index largest number of zeroes encountered thus far 
      #in that bucket
      buckets[bucketNumber] = max(oneIndex, buckets[bucketNumber])
  return(buckets[:-1])


def count_distinct(buckets):
    """ This is where all the magic happens.In any 64 bit binary sequence that
    is uniformly distributed the chance of getting a 0 or a 1 is 50%, chances 
    of finding n consecutive zeros's are 0.5**n. If k is the number of consecutive
    zeroes found in such a binary number on avarage 2**k items need to be 
    traversed before getting k conecutive zeros. While this is the expected
    value E(x) the varaince in single a case is huge. Therefore the number
    of consective zeros are stored in registers, 2047 in this case where 
    separte subsets of the mainset are beeing tracked. In the end they are
    avaraged with a harmonic mean and adjusted to get a better estimate.
    One is multiplying by the square of the number of registers and the other 
    is multplying by a constant to adjust for multiplicative bias of the 
    estimate. Imporvemnts suggested might be throwing out 30% of outliers 
    in the buckets to arriave at better avarage and estimate"""
    m = len(buckets)
    alphaConstant = 0.7213/(1+(1.079/m))
    harmoicMean = 1/sum((1/(2**buckets)))
    estimate = alphaConstant * (m**2) * harmoicMean
    return(estimate)


def read_elements(FILE_NAME, column):
    """ Function should sequentialy read subset of the main set to which
    count-distnct aproximation to be applied. It needs to return a list of
    the elements(subset) to be counted. Function should be a generator function 
    to be called for sequentially reading elements(subsets) of the main set."""
    chunksize = 10000
    for chunk in pd.read_csv(FILE_NAME, chunksize=chunksize):
        yield chunk[column].values.tolist()
def hyper_log_log_count_distinct_ips(FILE_NAME, column):
    """Function is called with the dataset filename and column name to find
    distinct values. 2047 registers are used or the right-most 11 bit sequences
    of string representation of the binary hash."""
    m = (2**11)-1
    buckets = np.zeros(m)
    generator = read_elements(FILE_NAME=FILE_NAME, column = column)
    for elements in generator:
        if elements:
            buckets = update_buckets(elements, buckets)
        else:
            next
    distinct = count_distinct(buckets)
    return(distinct)

df = pd.read_csv(FILE_NAME)
srcIpUniquesExact = df['Src IP'].nunique()
dstIpUniquesExact = df['Dst IP'].nunique()
srcIpUniquesAprox=hyper_log_log_count_distinct_ips(FILE_NAME=FILE_NAME,
                                                   column = "Src IP")
dstIpUniquesAprox=hyper_log_log_count_distinct_ips(FILE_NAME=FILE_NAME,
                                                   column = "Dst IP")
print("Testing the HyperLogLog algorithm on a data set with " +
      str(len(df.index)) + " rows. There are exactly " + str(srcIpUniquesExact)
      + " unique IP's in the Source ip column. HyperLogLog estimate is " + 
      str(round(srcIpUniquesAprox)) + " uniques, which is " + 
      str(round((abs(srcIpUniquesAprox - srcIpUniquesExact )
      /srcIpUniquesExact)*100))+ 
      " percent away of the exact number of unqiue elements. " +
    "There are exactly " + str(dstIpUniquesExact) +
      " unique IP's in the Dest ip column. HyperLogLog estimate is " + 
      str(round(dstIpUniquesAprox)) + " uniques, which is " + 
      str(round((abs(dstIpUniquesAprox - dstIpUniquesExact )
      /dstIpUniquesExact)*100))+ 
      " percent away of the exact number of unqiue elements. ")