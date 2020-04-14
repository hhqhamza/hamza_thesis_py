import comp_decomp as cd
import pandas as pd
import sys
import random
import numpy as np
import window as win
import cache_lfu as cache_lfu
import cache_fifo as cache_fifo
# import main_scss_real_data as scss_rd

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Sample-based Caching Selection System (SCSS)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class scss:
    def __init__(self, cs, data, header):
        self.cache_size = cs        
        self.data = data
        self.header = header
        
    def cache_decision(self):
        print ("|Taking sample from data frames: |")
        print ("----------------------------------\n")
        
        # See how many is 1% for the experiment
        opq_data = int(len(self.data) / 100)
        print ("1 % of data")
        print ("opq_data")
        
        if opq_data < 1:
            opq_data = opq_data + 1
                    
        # Select the names of the datasets for operation
        sel_data = self.data[0:opq_data]
        print ("Select the requests are:")
        print ("sel_data")
        
        type_cache_list = ["fifo", "lfu"]
        df_fifo_results = pd.DataFrame()        
        df_lfu_results = pd.DataFrame()
        
        scss_obj_lfu = cache_lfu.cache_lfu() # Create LFU cache
        scss_obj_lfu.set_cache_size(self.cache_size)
        scss_obj_fifo = cache_fifo.cache_fifo() # Create FIFO cache
        scss_obj_fifo.set_cache_size(self.cache_size)
        
        for type_cache in type_cache_list: 
            if type_cache == "lfu":
                cd_obj = cd.comp_decomp(type_cache, sel_data, scss_obj_lfu) 
                result_lfu = cd_obj.comp_decomp()
                df_lfu_results = df_lfu_results.append(result_lfu)
            if type_cache == "fifo":
                cd_obj = cd.comp_decomp(type_cache, sel_data, scss_obj_fifo) 
                results_fifo = cd_obj.comp_decomp()
                df_fifo_results = df_fifo_results.append(results_fifo)
        
        print ("Data received after processing for time without headers")
        print ("df_fifo_results")
        print (df_fifo_results)
        print ("df_lfu_results")
        print (df_lfu_results)
        del scss_obj_lfu
        del scss_obj_fifo
        df_fifo_results.columns = self.header
        df_lfu_results.columns = self.header
        
        print ("Data received after processing for time with headers")
        print ("df_fifo_results")
        print (df_fifo_results)
        print ("df_lfu_results")
        print (df_lfu_results)
        
        # Now calculating the times
        # print ("now time will be calculated")
        # input ("Calculating time")
        df_fifo_avg = df_fifo_results["total_time"].mean()
        df_lfu_avg = df_lfu_results["total_time"].mean()
        # input ("Done calculating time")
        print ("Times of different cache types")
        print ("df_fifo_avg")
        print (df_fifo_avg)
        print ("df_lfu_avg")
        print (df_lfu_avg)
        if df_lfu_avg <= df_fifo_avg:
            print ("+++++++++++++++++++++++++++++++++++++++++++++")
            print ("LFU is selected for next window")
            print ("+++++++++++++++++++++++++++++++++++++++++++++")
            print (df_lfu_avg)
            return "LFU"            
        elif df_fifo_avg <= df_lfu_avg:
            print ("+++++++++++++++++++++++++++++++++++++++++++++")
            print ("Fifo is selected for next window")
            print ("+++++++++++++++++++++++++++++++++++++++++++++")
            print (df_fifo_avg)
            return "FIFO"
        