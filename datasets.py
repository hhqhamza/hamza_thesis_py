import sys
import os
import paths_all as p
import csv_writer as cw

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Get list of datasets
# Change path to give the location of the datasets
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def datasets():
    path = p.datasets_location
    datasets = []
    datasets_found = []
    for dirpath, dirs, files in os.walk(path): 
          for filename in files:
              fname = os.path.join(dirpath,filename)
              dataset_name = [os.path.basename(fname)]
              datasets.append(fname)
              datasets_found.append(dataset_name)
    found_datasets = cw.csv_writer('datasets_found','', '', '', '', '','', p.datasets_found_save_path, datasets_found, 'w', ['Datasets'], '', '', '', '', '', '', '', '')
    found_datasets.csv_writer_result()
    return datasets
   