# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 18:12:53 2020

@author: Dawid
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 17:49:46 2020

@author: Dawid
"""

import h5py
import numpy as np

with h5py.File("mytestfile.h5", "w") as f:
    dset = f.create_dataset("mydataset", (100,), dtype='i')
    
with h5py.File("mytestfile.h5", "r+") as h:
    # List all groups
    print("Keys: %s" % h.keys())
    file_key = list(h.keys())[0]
    
    arr = h[file_key]
    print(arr.shape)
    print(arr[7])
    
    
import pickle

with open('val.pkl', 'rb') as f:
    data = pickle.load(f)


