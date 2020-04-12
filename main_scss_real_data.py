import time
import comp_decomp as cd
from constants import DFT_CACHE_SIZE, DFT_SEED, DFT_A_START, DFT_A_STOP, DFT_A_STEP, DFT_W, DFT_SAMPLE, DFT_WS_START, DFT_WS_STOP, DFT_WS_STEP, DFT_MIN_DELTA_ALPHA, DFT_MAX_DELTA_ALPHA, DFT_STEP_DELTA_ALPHA, DFT_N, RD_SCSS_CACHE_SIZE
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
# Sample-based Caching Selection System (SCSS)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class scss_rd:
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
    
    def scss_main_real_data(self):
        print ("|Taking sample from data frames: |")
        print ("----------------------------------\n")
        header = ['objectid', 'time', 'method', 'type', 'status', 'region', 'server']
        print ("Reading dataset " + self.real_data)
        # real_dataset = self.read_real_data(self.real_data, header)
        real_dataset = self.read_real_data(self.real_data, header)
        real_dataset.columns = header
        # ret_data_set = real_dataset['objectid']
        return real_dataset
        
    
    def get_real_path(self, dat): # Receive the full paths of the selected datasets and push them into a list        
        data = []
        path = p.datasets_location
        os.chdir(path)
        for dirpath, dirs, files in os.walk(path): 
            for d in np.ravel(dat):     
                if d in files:  
                    data.append([os.path.join(dirpath, str(d))])        
        return data      
        
    def cache_decision(self, df_fifo, df_lfu):
        print ("|Taking sample from data frames: |")
        print ("----------------------------------\n")
        header = ['exp_ind', 'cache_type', 'cache_size', 'n', 'comp_time', 'decomp_time', 'total_time', 'comp_ratio', 'ds_size', 'ds_name', 'cached', 'win_size', 'nb_win', 'win_ind']
               
        df_fifo_result = df_fifo
        df_lfu_result = df_lfu
        # print ("Data in main without header")
        # print ("df_fifo_result")
        # print (df_fifo_result)
        # print ("df_lfu_result")
        # print (df_lfu_result)
        if df_fifo_result.empty == False:
            df_fifo_result.columns = header
        if df_lfu_result.empty == False:
            df_lfu_result.columns = header   
        # print ("Data in main with header")
        # print ("df_fifo_result")
        # print (df_fifo_result)
        # print ("df_lfu_result")
        # print (df_lfu_result)    
        # See how many is 1% for the experiment
        opq_fifo = len(df_fifo)/100
        opq_lfu = len(df_lfu)/100
        # print ("1 % of data")
        # print ("opq_fifo")
        # print (opq_fifo)
        # print ("opq_lfu")
        # print (opq_lfu)
        if opq_fifo < 1:
            opq_fifo = round(opq_fifo, 1) + 1
        if opq_lfu < 1:
            opq_lfu = round(opq_lfu, 1) + 1
        
        # Select the names of the datasets for operation
        df_fifo_que = df_fifo.filter(['ds_name'])
        df_lfu_que = df_lfu.filter(['ds_name'])
        # print ("Select the names of the datasets for operation")
        # print ("df_fifo_que")
        # print (df_fifo_que)
        # print ("df_lfu_que")
        # print (df_lfu_que)
        # Only 1% results selected
        selected_fifo_queries = df_fifo_que[:int(opq_fifo)]
        selected_lfu_queries = df_lfu_que[:int(opq_lfu)]
        # print ("Only 1% results selected")
        # print ("selected_fifo_queries")
        # print (selected_fifo_queries)
        # print ("selected_lfu_queries")
        # print (selected_lfu_queries)
        # Results converted to list
        df_fifo_list = selected_fifo_queries.values.tolist()
        df_lfu_list = selected_lfu_queries.values.tolist()
        # print ("Results converted to list")
        # print ("df_fifo_list")
        # print (df_fifo_list)
        # print ("df_lfu_list")
        # print (df_lfu_list)
        # Merged the results 
        if df_fifo_list and df_lfu_list:
            data_names = list(df_fifo_list + df_lfu_list)
        if not df_fifo_list:
            data_names = list(df_lfu_list)
        if not df_lfu_list:
            data_names = list(df_fifo_list)
        # print (" Merged the results ")
        # print ("data_names")
        # print (data_names)
        
        # data = self.get_real_path(data_names)
        data = data_names
        # print (" Data ")       
        # print (data_names)
        type_cache_list = ["fifo", "lfu"]
        df_fifo_results = pd.DataFrame()        
        df_lfu_results = pd.DataFrame()
        
        cac_obj_lfu = cache_lfu.cache_lfu()
        cac_obj_fifo = cache_fifo.cache_fifo()
        
        # print ("Data in real data main for cache decision")
        # print (data)
        rd_scss_cache_size = RD_SCSS_CACHE_SIZE # Cache size for the RD_SCSS is small as it only takes a sample from the data and sample is only one percent of the queries
        exp_folder_name = 'scss_real_data'+'_q'+str(len(data))+' _cs'+str(rd_scss_cache_size)         
        exp_ind = 'scss_real_data'+'_q'+str(len(data))+' _cs'+str(rd_scss_cache_size)     
        result_location = p.real_dataset_log_path+exp_folder_name+'/'
        fname = 'agg_result_'+exp_folder_name # File name for results for one type of cache        
        for type_cache in type_cache_list:           
            result = cd.comp_decomp(exp_ind+'_'+type_cache, '', '', '', '', rd_scss_cache_size, type_cache, '', len(data), result_location, '',  cac_obj_lfu, cac_obj_fifo, data, '', '', 'rd')            
            if type_cache == "fifo":
                df_fifo_results = df_fifo_results.append(result)
            if type_cache == "lfu":
                df_lfu_results = df_lfu_results.append(result)        
        
        # print ("Data received after processing for time without headers")
        # print ("df_fifo_results")
        # print (df_fifo_results)
        # print ("df_lfu_results")
        # print (df_lfu_results)
        del cac_obj_lfu
        del cac_obj_fifo
        df_fifo_results.columns = header
        df_lfu_results.columns = header
        
        # print ("Data received after processing for time with headers")
        # print ("df_fifo_results")
        # print (df_fifo_results)
        # print ("df_lfu_results")
        # print (df_lfu_results)
        
        # Now calculating the times
        # print ("now time will be calculated")
        # input ("Calculating time")
        df_fifo_avg = df_fifo_results["total_time"].mean()
        df_lfu_avg = df_lfu_results["total_time"].mean()
        # input ("Done calculating time")
        # print ("Times of different cache types")
        # print ("df_fifo_avg")
        # print (df_fifo_avg)
        # print ("df_lfu_avg")
        # print (df_lfu_avg)
        if df_lfu_avg <= df_fifo_avg:
            print ("+++++++++++++++++++++++++++++++++++++++++++++")
            print ("LFU is selected for next window")
            print ("+++++++++++++++++++++++++++++++++++++++++++++")
            print (df_lfu_avg)
            return "lfu"            
        elif df_fifo_avg <= df_lfu_avg:
            print ("+++++++++++++++++++++++++++++++++++++++++++++")
            print ("Fifo is selected for next window")
            print ("+++++++++++++++++++++++++++++++++++++++++++++")
            print (df_fifo_avg)
            return "fifo"