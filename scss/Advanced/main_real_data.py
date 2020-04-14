import time
import comp_decomp as cd
from constants import DFT_CACHE_SIZE, DFT_SEED, DFT_A_START, DFT_A_STOP, DFT_A_STEP, DFT_W, DFT_SAMPLE, DFT_WS_START, DFT_WS_STOP, DFT_WS_STEP, DFT_MIN_DELTA_ALPHA, DFT_MAX_DELTA_ALPHA, DFT_STEP_DELTA_ALPHA, DFT_N
import verbo as v
import utils as ul
import pandas as pd
import csv_writer as cw
import paths_all as p
import sys
import datasets as ds
import random
import numpy as np
import cache_lfu as cache_lfu
import cache_fifo as cache_fifo
import os
import glob

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Real dataset without alpha and window
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class main_rd:
    def set_scss_rd(self, file_name, df_fifo, df_lfu, cs, real_data):
        self.file_name = file_name
        self.df_fifo = df_fifo
        self.df_lfu = df_lfu        
        self.cache_size = cs        
        self.real_data = real_data
   
    def read_real_data(self, file_name, head):
        header = head
        search = "real_data"
        results = pd.DataFrame([])
        os.chdir(file_name+'/')
        for counter, file in enumerate(glob.glob("["+str(search)+"]*.csv")):
            # namedf = pd.read_csv(file, skiprows=0, usecols = header)
            if v.args.n != '':
                namedf = pd.read_csv(file, nrows=v.args.n) # Add  nrows = 100 for reading only 100 rows from the dataset
            else:
                namedf = pd.read_csv(file)
            results = results.append(namedf)
        return results    
    
    def main_real_data(self):
        print ("|Taking sample from data frames: |")
        print ("----------------------------------\n")
        header = ['objectid', 'time', 'method', 'type', 'status', 'region', 'server']
        print ("Reading dataset " + self.real_data)
        # real_dataset = self.read_real_data(self.real_data, header)
        real_dataset = self.read_real_data(self.real_data, header)
        real_dataset.columns = header
        # ret_data_set = real_dataset['objectid']
        return real_dataset