# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 17:49:46 2020

@author: Dawid
"""

import os
import tables
import numpy as np

hdf5_file_path = os.path.abspath("brats_data.h5")

data_index = 1
data_file = tables.open_file(hdf5_file_path, "r")

subject = data_file.root.subject_ids[data_index].decode('utf-8')
affine = data_file.root.affine[data_index]
test_data = np.asarray([data_file.root.data[data_index]])


# print()

# import h5py
# import numpy as np
# import tables

# filename = "brats_data.h5"



# with h5py.File(filename, "r") as h5file:
#     # List all groups
#     print("Keys: %s" % h5file.keys())
#     file_keys = list(h5file.keys())
#     d = list(h5file.items())
#     print(d)
    
#     print(h5file['affine'].attrs.items())
    
#     n1 = np.array(h5file['affine'])
#     print(n1)
    
    
#     # print(affineData2[0])

#     # Get the data
#     # data = list(f[a_group_key])