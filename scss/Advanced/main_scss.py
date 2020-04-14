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
# Sample-based Caching Selection System (SCSS)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class scss:
    def set_scss(self, file_name, df_fifo, df_lfu, cs, az, da, a,  del_max, s):
        self.file_name = file_name
        self.df_fifo = df_fifo
        self.df_lfu = df_lfu        
        self.cache_size = cs
        self.alpha_zero = az
        self.delta_alpha = da
        self.alpha = a
        self.del_max = del_max        
        self.seed = s
    
    def read_file(self, file_name):
        header = ['exp_ind', 'seed', 'cache_type', 'alpha_zero', 'delta_alpha',  'alpha', 'da_amp', 'cache_size', 'n', 'comp_time', 'decomp_time', 'total_time', 'comp_ratio', 'ds_size', 'ds_name', 'cached', 'win_size', 'nb_win', 'win_ind']
        search = "ref"
        results = pd.DataFrame([])
        os.chdir(file_name+'/')
        for counter, file in enumerate(glob.glob("["+str(search)+"]*.csv")):
            namedf = pd.read_csv(file, skiprows=0, usecols=header)
            results = results.append(namedf)
        return results
        
    def scss_main(self):
        print ("----------------------------------\n")
        print ("|Taking sample from data frames: |")
        print ("----------------------------------\n")
        header = ['exp_ind', 'seed', 'cache_type', 'alpha_zero', 'delta_alpha',  'alpha', 'da_amp', 'cache_size', 'n', 'comp_time', 'decomp_time', 'total_time', 'comp_ratio', 'ds_size', 'ds_name', 'cached', 'win_size', 'nb_win', 'win_ind']
                
        df_fifo = self.df_fifo
        df_lfu = self.df_lfu
        
        if df_fifo.empty == False:
            df_fifo.columns = header
        if df_lfu.empty == False:
            df_lfu.columns = header       
        
        # See how many is 1% for the experiment
        opq_fifo = len(df_fifo)/100
        opq_lfu = len(df_lfu)/100
        
        if opq_fifo < 1:
            opq_fifo = round(opq_fifo, 1) + 1
        if opq_lfu < 1:
            opq_lfu = round(opq_lfu, 1) + 1
                
        # Select the names of the datasets for operation
        df_fifo_que = df_fifo.filter(['ds_name'])
        df_lfu_que = df_lfu.filter(['ds_name'])
                        
        # Only 1% results selected
        selected_fifo_queries = df_fifo_que[:int(opq_fifo)]
        selected_lfu_queries = df_lfu_que[:int(opq_lfu)]
                
        # Results converted to list
        df_fifo_list = selected_fifo_queries.values.tolist()
        df_lfu_list = selected_lfu_queries.values.tolist()
                        
        # Merged the results 
        if df_fifo_list and df_lfu_list:
            data_names = list(df_fifo_list + df_lfu_list)
        if not df_fifo_list:
            data_names = list(df_lfu_list)
        if not df_lfu_list:
            data_names = list(df_fifo_list)
        
        # Receive the full paths of the selected datasets and push them into a list
        data = []
        path = p.datasets_location
        os.chdir(path)
        for dirpath, dirs, files in os.walk(path): 
            for d in np.ravel(data_names):     
                if d in files:  
                    data.append(os.path.join(dirpath, str(d)))
        
        # Requires variables to run the experiment
        s = self.seed
        n = len(data)    
        cache_size = self.cache_size
        alpha_zero = self.alpha_zero
        delta_alpha = self.delta_alpha        
        alpha = self.alpha
        del_max = self.del_max
        type_cache_list = ["fifo", "lfu"]                
        avg_fifo_time = ''
        avg_lfu_time = ''
        avg_winner_time = ''        
        cac_obj_lfu = ''
        cac_obj_fifo = ''        
        df_fifo_results = pd.DataFrame()        
        df_lfu_results = pd.DataFrame()
               
        cac_obj_lfu = cache_lfu.cache_lfu()
        cac_obj_fifo = cache_fifo.cache_fifo()
       
        exp_folder_name = 'scss_s'+str(s)+'_q'+str(n)+' _cs'+str(cache_size)+'_a'+str(round(alpha, 1))         
        exp_ind = 'scss_s'+str(s)+'_q'+str(n)+' _cs'+str(cache_size)+'_az.'+str(round(alpha_zero, 1))        
        result_location = p.results_save_path+exp_folder_name+'/'
        fname = 'agg_result_'+exp_folder_name # File name for results for one type of cache        
        for type_cache in type_cache_list:           
            result = cd.comp_decomp(exp_ind+'_'+type_cache, round(float(alpha_zero), 1), round(float(delta_alpha), 1), round(float(alpha), 1), del_max, int(cache_size), type_cache, s, n, result_location, '',  cac_obj_lfu, cac_obj_fifo, data, '', '', 'scss')     

            if type_cache == "fifo":
                df_fifo_results = df_fifo_results.append(result)
            if type_cache == "lfu":
                df_lfu_results = df_lfu_results.append(result)        
      
        del cac_obj_lfu
        del cac_obj_fifo
        
        df_fifo_results.columns = header
        df_lfu_results.columns = header
        
        # Now calculating the times
        df_fifo_avg = df_fifo_results["total_time"].mean()
        df_lfu_avg = df_lfu_results["total_time"].mean()
        
        print ("Avg FIFO time" + str(df_fifo_avg))
        print ("Avg LFU time" + str(df_lfu_avg))
               
        if df_fifo_avg >= df_lfu_avg:
            print ("+++++++++++++++++++++++++++++++++++++++++++++")
            print ("LFU is selected for next window")
            print ("+++++++++++++++++++++++++++++++++++++++++++++")
            return "lfu"
            print (df_lfu_avg)
        elif df_fifo_avg <= df_lfu_avg:
            print ("+++++++++++++++++++++++++++++++++++++++++++++")
            print ("Fifo is selected for next window")
            print ("+++++++++++++++++++++++++++++++++++++++++++++")
            print (df_fifo_avg)
            return "fifo"            