import os, glob, h5py
# Basic extraction draft
def parse_mat(path):
    with h5py.File(path, 'r') as f:
        return f['cjdata']
