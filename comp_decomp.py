import lz4.frame
import os
import numpy as np
import time
import pandas as pd
from collections import Counter
import utils as ul
import paths_all as p
import csv_writer as cw
import verbo as v
import sys
import cache_lfu as cache_lfu
import cache_fifo as cache_fifo
import cache_check as cdc
import cache_check_real_data as cdcrd

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Compress and Decompress the data
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def comp_decomp(exp_ind, alpha_zero, delta_alpha, alpha, del_max, cache_size, type_cache, seed, n, result_location, window_size, cache_obj_lfu, cache_obj_fifo, dat, no_of_win, win_ind, mark):    
    if v.args.verbose >= 1: # Parsing data
        print ('value of alpha is set to: ' + str(alpha))
   
    header = ['exp_ind', 'seed', 'cache_type', 'alpha_zero', 'delta_alpha',  'alpha', 'da_amp', 'cache_size', 'n', 'comp_time', 'decomp_time', 'total_time', 'comp_ratio', 'ds_size', 'ds_name', 'cached', 'win_size', 'nb_win', 'win_ind']
    results_csv = []
    query_csv = []
    cache_type = []    
    result_location = result_location
    window_size = window_size
    no_of_win = no_of_win
    exp_ind = exp_ind
    del_max = del_max
    mark = mark
    data = []
    
    # print ("Before data")
    # print (dat)
    # input ("enter to continue")
    
    if mark == 'normal':        
        data = ul.get_data(alpha_zero, delta_alpha, alpha, seed, n, cache_size, type_cache, window_size, dat, no_of_win, win_ind)
    elif mark == 'scss' or mark == 'rd':        
        for d in dat:
            if mark == 'scss':
                data.append([d])
            elif mark == 'rd':
                data.append(d)
    # print ("After data")
    # print (data)
    # input ("enter to continue")
    if(type_cache == "lfu"):
        if v.args.verbose >=3:
            print ('Cache type is LFU')
            print ('Creating LFU object')
        
        if v.args.cm is True:
            cache_obj = cache_obj_lfu
        elif v.args.cm is False:
            cache_obj = cache_lfu.cache_lfu()
        
        cache_obj.set_cache_size(cache_size)
        ctype = 'ctlfu' # File name of the result
        cache_type = type_cache
        result_location = result_location+'/lfu/'
    if(type_cache == "fifo"):
        if v.args.verbose >=3:
            print ('Cache type is FIFO')
            print ('Creating FIFO object')
        
        if v.args.cm is True:
            cache_obj = cache_obj_fifo
        elif v.args.cm is False:
            cache_obj = cache_fifo.cache_fifo()
        
        cache_obj.set_cache_size(cache_size)
        ctype = 'ctfifo' # File name of the result
        cache_type = type_cache
        result_location = result_location+'/fifo/'
    
    
    if v.args.n is None:
        if v.args.rd == False:
            n = len(data)
        elif v.args.rd == True:
            n = n
    else:
        n = n
    
    
    cdc_obj = cdc.comp_decomp() # Object of comp_decomp class    
    cdc_obj.set_seed_alpha(exp_ind, seed, alpha_zero, delta_alpha, alpha, del_max, cache_type, cache_size, n, window_size, no_of_win, win_ind)
    
    cdcrd_obj = cdcrd.comp_decomp() # Object of comp_decomp class    
    cdcrd_obj.set_seed_alpha(exp_ind, cache_type, cache_size, n, window_size, no_of_win, win_ind)
    
    if v.args.rd == True:
        header = ['exp_ind', 'cache_type', 'cache_size', 'n', 'comp_time', 'decomp_time', 'total_time', 'comp_ratio', 'ds_size', 'ds_name', 'cached', 'win_size', 'nb_win', 'win_ind']
        # print ("Data found is ")
        # print (data)
        # print ("N is ")
        # print (n)
        # print ("Length of data")
        # print (len(data))
        for i in range(0, n): # name me n pls
            fname = data[i] # Reading the names of datasets with full path
            query_csv.append([fname]) # query_csv is a list of all the datasets after randomization
            if cache_obj.if_in_cache(str(fname)) == True: # check if dataset is in the cache or not                
                cache_results = cdcrd_obj.in_cache(fname); # Increment dataset frequency of occurance in cache
                results_csv.append(cache_results)            
                cache_obj.increment_cache(str(fname))
            if cache_obj.if_in_cache(str(fname)) == False: 
                cache_obj.push_cache(str(fname)) # Compress and Decompress dataset and set frequency of occurance of dataset in cache       
                results = cdcrd_obj.not_in_cache(fname)
                results_csv.append(results)
            if v.args.verbose >= 3:  
                print ('Cache view for iteration no: ' + str(i))
                cache_df = pd.DataFrame.from_dict(cache_obj.cache, orient='index', columns=['Frequency']) # TODO call object passed cache
                print (cache_df)
                print ('---------------------------------------------------------------')
            cache_obj.check_size()
            #i += 1            
        
        c = cw.csv_writer('results_', '', '', '', 'cs'+str(cache_size), '_'+str(ctype), '', result_location, results_csv, 'w', header, '_n'+str(n), '', '_w'+str(window_size), '_nbw'+str(no_of_win), '', '', '', '_wi'+str(win_ind)) # writing results in the csv file
        c.csv_writer_result()
    
    
    if v.args.rd == False:     
        header = ['exp_ind', 'seed', 'cache_type', 'alpha_zero', 'delta_alpha',  'alpha', 'da_amp', 'cache_size', 'n', 'comp_time', 'decomp_time', 'total_time', 'comp_ratio', 'ds_size', 'ds_name', 'cached', 'win_size', 'nb_win', 'win_ind']
        for i in range(0, n): # name me n pls
            fname = ', '.join(data[i]) # Reading the names of datasets with full path
            dataset_name = os.path.basename(fname) # dataset_name has only name of the datasets without full path
            query_csv.append([dataset_name] + [fname]) # query_csv is a list of all the datasets after randomization
            if cache_obj.if_in_cache(str(dataset_name)) == True: # check if dataset is in the cache or not                
                cache_results = cdc_obj.in_cache(fname); # Increment dataset frequency of occurance in cache
                results_csv.append(cache_results)            
                cache_obj.increment_cache(str(dataset_name))
            if cache_obj.if_in_cache(str(dataset_name)) == False: 
                cache_obj.push_cache(str(dataset_name)) # Compress and Decompress dataset and set frequency of occurance of dataset in cache       
                results = cdc_obj.not_in_cache(fname)
                results_csv.append(results)
            if v.args.verbose >= 3:  
                print ('Cache view for iteration no: ' + str(i))
                cache_df = pd.DataFrame.from_dict(cache_obj.cache, orient='index', columns=['Frequency']) # TODO call object passed cache
                print (cache_df)
                print ('---------------------------------------------------------------')
            cache_obj.check_size()
            #i += 1            
        
        c = cw.csv_writer('results_', 'az.'+str(alpha_zero), '_da.'+str(delta_alpha), '_a.'+str(alpha), '_cs'+str(cache_size), '_'+str(ctype), '_s'+str(seed), result_location, results_csv, 'w', header, '_n'+str(n), '', '_w'+str(window_size), '_nbw'+str(no_of_win), '', '_damp'+str(del_max), '', '_wi'+str(win_ind)) # writing results in the csv file
        c.csv_writer_result()
    
    
    if v.args.verbose >= 2: 
        cache_df = pd.DataFrame.from_dict(cache_obj.cache, orient='index', columns=['Frequency'])
        print (cache_df)
        print ('\n')
        print (pd.DataFrame.from_dict(results_csv))
        print ('Minimum value in cache: '  + min(cache_obj.cache, key = cache_obj.cache.get))
        print ('Maximum value in cache: ' + max(cache_obj.cache, key = cache_obj.cache.get))
    if v.args.verbose >= 3:  
        random_query_save_path = ''
        if v.args.alpha is not None:
            random_query_save_path = p.random_query_save_path + 'perf_eval_input_queries_a.' + str(v.args.alpha) + '_without_full_path/'
        elif v.args.alpha is None:
            random_query_save_path = p.random_query_save_path + 'perf_eval_input_queries_a.' + str(v.args.astart)+'-'+str(v.args.astop) + '_without_full_path/'
        
        if v.args.rd == False:
            queries = cw.csv_writer('results_', 'az.'+str(alpha_zero), '_da.'+str(delta_alpha), '_a.'+str(alpha), '_cs'+str(cache_size), '_'+str(ctype), '_s'+str(seed), random_query_save_path , query_csv, 'w', ['dataset_name', 'path'], '_n'+str(n), '', '_w'+str(window_size), '_nbw'+str(no_of_win), '', '_damp'+str(del_max), '', '_wi'+str(win_ind))
            queries.csv_writer_result()        
        if v.args.rd == True:
            queries = cw.csv_writer('results_', '', '', '', 'cs'+str(cache_size), '_'+str(ctype), '', random_query_save_path , query_csv, 'w', ['dataset_name', 'path'], '_n'+str(n), '', '_w'+str(window_size), '_nbw'+str(no_of_win), '', '', '', '_wi'+str(win_ind))
            queries.csv_writer_result()        
    return results_csv