# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
test1 = np.array([[1,-3],[1, 2],[3, 4]])
test2 = np.array([[1, -3],[1, 2],[3, 4], [2,5], [3,2]])

def return_n_nearest_stores(n, lat_and_longitude):
    square = lat_and_longitude**2
    squaresums = square.sum(axis=1)
    squaresums = squaresums.reshape(len(squaresums),1)
    finalarray = np.append(lat_and_longitude, squaresums, axis=1)
    finalarray.dtype = [('lat','int32'),('long','int32'), ('sums','int32')]
    finalarray = np.sort(finalarray, axis =0, order=['sums'])
    finalarray = finalarray[['lat','long']]
    return finalarray[:n]

print(return_n_nearest_stores(1, test1))
print(return_n_nearest_stores(3, test2))

