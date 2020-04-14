import comp_decomp as cd
import pandas as pd
import sys
import random
import numpy as np
import window as win
import cache_lfu as cache_lfu
import cache_fifo as cache_fifo
# import main_scss_real_data as scss_rd

##################################### Dataset ######################################
# data = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'j', 'k', 'j', 'k', 'j', 'k', 'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 't', 'u', 't', 'u', 't', 'u', 't', 'u', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'v', 'w', 'x', 'y', 'z'] 
# data = ['a', 'b', 'o','o','o','o','o','o','o','o','o','o','o'] 

data = pd.read_csv("./data_set.csv", nrows=200)
data = data['type']
################################ Tunning parameters ################################
window_size = [5] 
seed = [20]
itr = [40]
cache_type = ['LFU', 'FIFO']
cache_size = 3
n = len(data)
nbw = []
for ws in window_size:
    nbw.append(n//ws)
header = ['cache_type', 'comp_time', 'decomp_time', 'total_time', 'comp_ratio', 'ds_name', 'cached']
results_lfu = pd.DataFrame()
results_fifo = pd.DataFrame()
win_obj = win.window(window_size, n, data)
selected_requests = win_obj.get_window()
# print ("Selected Requests for window")
cache_obj_lfu = cache_lfu.cache_lfu() # Create LFU cache
cache_obj_lfu.set_cache_size(cache_size)
cache_obj_fifo = cache_fifo.cache_fifo() # Create FIFO cache
cache_obj_fifo.set_cache_size(cache_size)
for sel_win in selected_requests:
    print ("Selected window")
    print (sel_win)
    for ct in cache_type:
        if ct == "LFU":             
            cd_obj = cd.comp_decomp(ct, sel_win, cache_obj_lfu)
            result_lfu = cd_obj.comp_decomp()
            results_lfu = results_lfu.append(result_lfu)
            print ("Results LFU")
            print (result_lfu)
            
        if ct == "FIFO":            
            cd_obj = cd.comp_decomp(ct, sel_win, cache_obj_fifo)
            result_fifo = cd_obj.comp_decomp()
            results_fifo = results_fifo.append(result_fifo)
            print ("Results FIFO")
            print (result_fifo)
            
print ("Results for the experiment")
results_lfu.columns = header     
results_fifo.columns = header     
print (results_lfu)       
print (results_fifo)       
results_lfu.to_csv('result_lfu.csv')
results_fifo.to_csv('result_fifo.csv')
        