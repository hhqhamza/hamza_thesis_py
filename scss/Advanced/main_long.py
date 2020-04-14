import time
import comp_decomp as cd
from constants import DFT_CACHE_SIZE, DFT_SEED, DFT_A_START, DFT_A_STOP, DFT_A_STEP, DFT_W, DFT_SAMPLE, DFT_WS_START, DFT_WS_STOP, DFT_WS_STEP, DFT_MIN_DELTA_ALPHA, DFT_MAX_DELTA_ALPHA, DFT_STEP_DELTA_ALPHA
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
import main_scss as scss

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Parameters
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# -s define the seed
# -sstart, -sstop, -sstep define the start, stop and step for the seed range function 
# -n deifnes the iterations
# -nstart, -nstop, -nstep define the start, stop and step for the n range function 
# -a defines run experiment without random alpha without window size 
# -astart, -astop, -astep define the start, stop and step for the alpha range function and it must be gives as values of alpha are chosen at randon from a    range of alphas
# -w Defines the window size
# -wsstart, -wsstop, -wsstep define the start, stop and step for the window size range function 
# -csize defines the cache size
# -fifo and -lfu define the types of cache
# -cm Defines true or false for cache maintain state. If it is used same cache never renews, if not used new cache       will be made for every experiment.
# if -s is given than -sstart, -sstop, -sstep are ignored
# if -n is given than -nstart, -nstop, -nstep are ignored
# if -w is given than -wsstart, -wsstop, -wsstep are ignored
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Main function
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main(exp_ind, seed, itr, data, cs, az, da, a,  del_max, window_size, cache_obj_lfu, cache_obj_fifo, no_of_win, exp_folder_name, win_ind):

    cache_size = cs
    seed = seed
    alpha_zero = az
    delta_alpha = da
    alpha = a
    type_cache = 'undefined'
    data = data
    n = itr
    window_size = window_size
    no_of_win = no_of_win
    exp_ind = exp_ind
    exp_folder_name = exp_folder_name    
    win_ind = win_ind
    del_max = del_max
    result_fifo = []
    result_lfu = []
    
    if v.args.lfu == False and v.args.fifo == False:
        print ('\nCache type missing. Cache is undefined.') 
        print ('Use -lfu for LFU cache')
        print ('Use -fifo for FIFO cache. \n')
        sys.exit()
        
    if v.args.lfu or v.args.fifo:
        print ('Value of alpha is: ' + str(a))
        print ('Cache size is set to: ' + str(cache_size))
        print ('Seed for random value is set to: ' + str(seed))
        print ('No of iterations is set to: ' + str(n) + '\n')
        if v.args.alpha == True:
            print ('window_size size not used.')
        if v.args.alpha == False:
            print ('window_size size: ' + str(window_size))
            
    result_location = p.results_save_path+exp_folder_name+'/'
    fname = 'agg_result_'+exp_folder_name # File name for results for one type of cache

    if v.args.verbose >=3:
        print ('Result location')
        print (result_location)
    
    if v.args.lfu is True:            
        type_cache = 'LFU'
        print ('Running experiment using cache', type_cache)
        print ('---------------------------------------------')
        type_cache = 'lfu' 
        result_lfu = cd.comp_decomp(exp_ind+'_'+type_cache, alpha_zero, delta_alpha, alpha, del_max, int(cache_size), type_cache, seed, n, result_location, window_size, cache_obj_lfu, '', data, no_of_win, win_ind)
        cm = cw.csv_writer(fname, '', '', '', '', '', '', result_location, '', '','','', 'lfu', '', '', '','','', win_ind)
        cm.csv_merge()       
            
    if v.args.fifo is True:    
        type_cache = 'FIFO'
        print ('---------------------------------------------')
        print ('Running experiment using cache', type_cache)
        print ('---------------------------------------------')
        type_cache = 'fifo'
        result_fifo = cd.comp_decomp(exp_ind+'_'+type_cache, alpha_zero, delta_alpha, alpha, del_max, int(cache_size), type_cache, seed, n, result_location, window_size, '', cache_obj_fifo, data, no_of_win, win_ind)
        cm = cw.csv_writer(fname, '', '', '', '', '', '', result_location, '', '','','', 'fifo', '', '', '','','', win_ind)
        cm.csv_merge()

    # File name for combined results LFU and FIFO
    if v.args.lfu != False and v.args.fifo != False:
        cmer = cw.csv_writer('comb_agg_results_'+exp_folder_name, '', '', '', '', '', '', result_location, '', '','','', 'result', '', '', '', '', '', '')
        cmer.csv_merge()
    
    return result_fifo, result_lfu
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Main
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print ('| Series of experiment started |')
print ('--------------------------------\n')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Variables
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
time_start = time.time()

data = ds.datasets() 
cache_size = DFT_CACHE_SIZE

seed = []
sstart = ''
stop = ''
sstep = ''

itr = []

alpha = []
astart = DFT_A_START
astop = DFT_A_STOP
astep = DFT_A_STEP   

window_size = [] 
wsstart = ''
wsstop = ''
wsstep = ''

cache_obj_lfu = ''
cache_obj_fifo = ''
new_n = ''

del_min = DFT_MIN_DELTA_ALPHA
del_max = DFT_MAX_DELTA_ALPHA
del_step = DFT_STEP_DELTA_ALPHA



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Conditions for parameters
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if v.args.cm is True:    
    cache_obj_lfu = cache_lfu.cache_lfu()
    cache_obj_fifo = cache_fifo.cache_fifo()

if v.args.csize is None: 
    print ('Cache size missing. using default cache size: ' + str(cache_size))
else:
    cache_size= v.args.csize
    
if v.args.seed is None:
    if v.args.sstart is None or v.args.sstop is None or v.args.sstep is None:
        print ('Missing the some value for the seed range function.')
        seed.append(DFT_SEED)
        print ('Using default value for seed: ' + str(seed))
        
    else:        
        sstart = v.args.sstart
        sstop = v.args.sstop    
        sstep = v.args.sstep            
        for s in range(sstart, sstop, sstep):            
            seed.append(s)

elif v.args.seed is not None:
    seed.append(v.args.seed)
    
if v.args.alpha == True:
    if v.args.astart is None or v.args.astop is None or v.args.astep is None:
        print ('Missing the some value for the alpha range function.')
        print ('Using default value for alpha: ' + str(alpha))
        for a in ul.range_positve(astart, astop, astep):            
            alpha.append(round(al + 0.1 if a == 0.0 else a, 1))
        
    else:        
        astart = v.args.astart
        astop = v.args.astop    
        astep = v.args.astep            
        for a in ul.range_positve(astart, astop, astep):            
            alpha.append(round(a, 1))

elif v.args.alpha == False:
    if v.args.astart is None or v.args.astop is None or v.args.astep is None:
        print ('Missing the some value for the alpha range function.')
        print ('Using default value for alpha: ' + str(alpha))
        for a in ul.range_positve(astart, astop, astep):            
            alpha.append(round(a, 1))
        
    else:        
        astart = v.args.astart
        astop = v.args.astop    
        astep = v.args.astep            
        for a in ul.range_positve(astart, astop, astep):            
            alpha.append(round(a, 1))
    
if v.args.n is None:
    if v.args.nstart is None or v.args.nstop is None or v.args.nstep is None:
        print ('Missing the some value for the n range function.')
        itr.append(len(data))
        print ('Using default value for n = ' +str(itr)+ ' i.e. no of datasets found.')
        
    else:        
        nstart = v.args.nstart
        nstop = v.args.nstop    
        nstep = v.args.nstep            
        for iter in range(nstart, nstop, nstep):            
            itr.append(iter)

elif v.args.n is not None:
    itr.append(v.args.n)

if v.args.window_size is None:
    if v.args.wsstart is None or v.args.wsstop is None or v.args.wsstep is None:
        print ('Missing the some value for the window size range function.')
        window_size.append(DFT_W)
        print ('Using default value for window size: ' + str(window_size))
        
    else:        
        wsstart = v.args.wsstart
        wsstop = v.args.wsstop    
        wsstep = v.args.wsstep            
        for ws in range(wsstart, wsstop, wsstep):            
            window_size.append(ws)

elif v.args.window_size is not None:
    window_size.append(v.args.window_size)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Sample-based Caching Selection System (SCSS)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if v.args.scss == True:
    print ("| Sample-based Caching Selection System (SCSS) |")
    print ("------------------------------------------------\n")
    # sc = scss.scss()
    # sc.set_scss(p.agg_results)
    # sc.scss_main()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# New data generation strategy
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if v.args.alpha == False:
    if v.args.scss == True:
        print ("| Sample-based Caching Selection System (SCSS) is enabled |")
        print ("------------------------------------------------\n")
    # Experiment log
    nbw = []
    rand_alpha_list = []
    
    for s in seed:
         gra = ul.get_rand_alpha(astart, astop, astep, s, del_min, del_max, del_step)
         rand_alpha_list = gra
    
    # print ("Random alpha list")
    # print (rand_alpha_list)
    
    alpha_zero = []
    for al_zero in rand_alpha_list:
        alpha_zero.append(al_zero[0])
        
    delta_alpha = []
    for delta_al in rand_alpha_list:
        delta_alpha.append(delta_al[1])
        
    alphas = []
    for al_rand in rand_alpha_list:
        alphas.append(al_rand[2])
                
    for ws in window_size:
        for n in itr:
            nbw.append(n//ws)
    
    exp_des = 'Experiment with random alphas and window size'
    exp_folder_name = 'of_experiments'
    mr = cw.csv_writer(exp_folder_name, alpha_zero, delta_alpha, alphas, cache_size, str('LFU' if v.args.lfu == True else '')+" "+str('FIFO' if v.args.fifo == True else ''), seed, p.agg_results+'/', '', 'w','', itr, '', window_size, nbw, del_min, del_max, del_step, '')
    mr.log_write(exp_des)
    
    
    
    # Experiment
    print (exp_des)
    for win_size in window_size:
        i = 0    
        
        for s in seed:                
            for n in itr:
                win_ind = 0
                no_of_win = n//win_size
                new_n = win_size                
                # al_random = random.sample(rand_alpha_list,  no_of_win)               
                al_random = random.choices(rand_alpha_list,  k = no_of_win)               
                # print ("Random alphas selected: "+str(al_random))
                max_al = max(al_random[2])
                min_al = min(al_random[2])
                
                df_fifo = pd.DataFrame()
                df_lfu = pd.DataFrame()
                
                for al in al_random:                    
                    i += 1
                    win_ind += 1
                    seed_new = s+i
                    print("Window_size: "+str(win_size))
                    print("Actual seed: "+str(s))
                    print("New Seed: "+str(seed_new))
                    print("No of windows: "+str(no_of_win))
                    print("No of iterations: "+str(n))
                    print("Alpha zero: "+str(al[0]))
                    print("Delta alpha: "+str(al[1]))
                    print("Alpha: "+str(al[2]))
                    print("Window index: "+str(win_ind))
                    
                    exp_folder_name = 'e_s'+str(s)+'_q'+str(n)+' _cs'+str(cache_size)+'_ws'+str(win_size)+'_nbw'+str(no_of_win)+'_wi'+str(win_ind)+'_a'+str(round(float(al[2]), 1))
                    
                    exp_ind = 'e_s'+str(s)+'_q'+str(n)+' _cs'+str(cache_size)+'_ws'+str(win_size)+'_nbw'+str(no_of_win)+'_wi'+str(win_ind)+'_az.'+str(al[0])
                    try:
                        df_fif, df_lf = main (exp_ind, seed_new, new_n, data, cache_size, float(al[0]), float(al[1]), float(al[2]), del_max, win_size, cache_obj_lfu, cache_obj_fifo, no_of_win, exp_folder_name, win_ind)
                        print ('seed='+str(seed_new)+' no_of_queries='+str(new_n)+' data=... '+' cache_size='+str(cache_size)+' alpha_zero='+str(al[0])+' delta_alpha='+str(al[1])+' alpha='+str(al[2])+' window_size='+str(win_size)+' no_of_windows='+str(no_of_win)+' window_index='+str(win_ind))
                        
                        if df_fif:
                            df_fifo = df_fifo.append(df_fif)
                        if df_lf:
                            df_lfu = df_lfu.append(df_lf)
                           
                    except ValueError:
                        print('Division by zero error. Alpha is '+str(al[2]))
                        continue
                    print("+++++++++++++++++++++++++++++++\n")
                    
                    if v.args.m == False:
                        mr = cw.csv_writer('agg_results', '', '', '', '', p.results_save_path, '', '','','', 'merge', '', '', '', '', '', '')
                        mr.csv_merge()
                    # Create log for the experiment
                    mr = cw.csv_writer(exp_folder_name, str(al[0]), str(al[1]), str(al[2]), cache_size, str('LFU' if v.args.lfu == True else '')+" "+str('FIFO' if v.args.fifo == True else ''), s, p.results_save_path+exp_folder_name+'/', '', 'w','', n, '', win_size, no_of_win, del_min, del_max, del_step, win_ind)
                    mr.log_write(exp_des)
                    
                    
                if v.args.scss == True:
                    sc = scss.scss()
                    sc.set_scss(p.agg_results, df_fifo, df_lfu, rand_alpha_list)
                    cache_type = sc.scss_main()
                    if cache_type == "lfu":
                        v.args.fifo = False
                        v.args.lfu = True
                    elif cache_type == "fifo":
                        v.args.fifo = True
                        v.args.lfu = False
                    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Old data generation strategy
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if v.args.alpha == True and v.args.scss == False:
    # Experiment Log
    exp_des = 'Running experiment without random alphas and windows size'
    exp_folder_name = 'of_experiments'
    mr = cw.csv_writer(exp_folder_name, '', '', alpha, cache_size, str('LFU' if v.args.lfu == True else '')+" "+str('FIFO' if v.args.fifo == True else ''), seed, p.agg_results+'/', '', 'w','', itr, '', '', '', '', '', '', '')
    mr.log_write(exp_des)
    
    # Experiment    
    print (exp_des)
    for s in seed:
        for n in itr:
            max_al = max(alpha)
            min_al = min(alpha)
            for a in alpha:
                exp_folder_name = 'e_s'+str(s)+'_q'+str(n)+' _cs'+str(cache_size)+'_a'+str(min_al)+'-'+str(max_al)
                exp_ind = 'e_s'+str(s)+'_q'+str(n)+' _cs'+str(cache_size)+'_a'+str(a)
                try:
                    main(exp_ind, s, n, data, cache_size, '', '', a, '', '', cache_obj_lfu, cache_obj_fifo, '', exp_folder_name, '')
                    print ('seed='+str(s)+' no_of_queries='+str(n)+' data=... '+' cache_size='+str(cache_size)+' alpha='+str(a))
                    
                except ValueError:
                    print('Division by zero error. Alpha is '+str(a))
                    continue
                print("+++++++++++++++++++++++++++++++\n")
                
                if v.args.m == False:
                    mr = cw.csv_writer('agg_results', '', '', '', '', p.results_save_path, '', '','','', 'merge', '', '', '', '', '', '')
                    mr.csv_merge()
            # Create log for the experiment
            mr = cw.csv_writer(exp_folder_name, '', '', alpha, cache_size, str('LFU' if v.args.lfu == True else '')+" "+str('FIFO' if v.args.fifo == True else ''), s, p.results_save_path+exp_folder_name+'/', '', 'w','', n, '', '', '', '', '', '', '')
            mr.log_write(exp_des)        
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Merging all results in a single csv
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if v.args.m == True:
    print ('Merging all experiment results in a single CSV')
    mr = cw.csv_writer('agg_results', '', '', '', '', '', '', p.results_save_path, '', '','','', 'merge', '', '', '','','', '')
    mr.csv_merge()
    print ('Finished creating the file')

time_stop = time.time()
print ('Series of experiment finished')
print ('Aggregated Results location')
print (p.agg_results)
print ('Seperate Results location')
print (p.results_save_path)
print ("Time taken: ", (time_stop-time_start)*1000)