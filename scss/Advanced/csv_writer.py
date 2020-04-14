import paths_all as p
import csv
import pandas as pd
import numpy as np
import os
import verbo as v
import glob

class csv_writer:

    def __init__(self, file_name, alpha_zero, delta_alpha, alpha, cache_size, cache_type, seed, save_path, result, write_append, header, n, marker, window_size, no_of_win, del_min, del_max, del_step, win_ind):
        self.file_name = file_name
        self.alpha_zero = alpha_zero
        self.delta_alpha = delta_alpha
        self.alpha = alpha
        self.cache_size = cache_size
        self.cache_type =cache_type
        self.seed = seed
        self.save_path = save_path
        self.result = result
        self.write_append = write_append
        self.header = header
        self.n = n
        self.marker = marker
        self.window_size = window_size
        self.no_of_win = no_of_win
        self.del_min = del_min
        self.del_max = del_max #delta amp
        self.del_step = del_step
        self.win_ind = win_ind        

    def csv_writer_result(self):
        save_path_results = self.save_path
        if not os.path.isdir(save_path_results):
            os.makedirs(save_path_results)
        result_to_write = save_path_results+str(self.file_name)+str(self.alpha_zero)+str(self.delta_alpha)+str(self.alpha)+str(self.del_max)+str(self.cache_size)+str(self.cache_type)+str(self.seed)+str(self.n)+str(self.window_size)+str(self.no_of_win)+str(self.win_ind)+'.csv'
        results = pd.DataFrame([])
        if os.path.exists(result_to_write):
            self.write_append = "a"
            self.header = ''
        with open(result_to_write, self.write_append) as results: # For linux. Also works for window_sizes but adds an extra empty row
        # with open(result_to_write, self.write_append, newline='') as results: # For window_sizes. Only works in window_sizes, gives error if ran in linux
            writer = csv.writer(results, delimiter=',')
            if self.header != '':
                writer.writerow(self.header)
                writer.writerows(self.result)
            if self.header == '':
                writer.writerows(self.result)
            results.close()

    def create_result(self, marker, save_path_results, search):
        if v.args.rd == False:
            header = ['exp_ind', 'seed', 'cache_type', 'alpha_zero', 'delta_alpha', 'alpha', 'da_amp','cache_size', 'n', 'comp_time', 'decomp_time', 'total_time', 'comp_ratio', 'ds_size', 'ds_name', 'cached', 'win_size', 'nb_win', 'win_ind']
        elif v.args.rd == True:
            header = ['exp_ind', 'cache_type', 'cache_size', 'n', 'comp_time', 'decomp_time', 'total_time', 'comp_ratio', 'ds_size', 'ds_name', 'cached', 'win_size', 'nb_win', 'win_ind']
        results = pd.DataFrame([])
        for counter, file in enumerate(glob.glob("["+str(search)+"]*.csv")):
            if marker == 'merge':
                print ('Merging file ' + str(file))
            namedf = pd.read_csv(file, skiprows=0, usecols=header)
            results = results.append(namedf)
        if not os.path.isdir(save_path_results):
            os.makedirs(save_path_results)
        results.to_csv(save_path_results+self.file_name+'_'+marker+'.csv', index=None)
        print ('Results saved in agg_results')

    def csv_merge(self):
        
        save_path_results = self.save_path
        marker = self.marker

        if marker == 'lfu':
            loc = save_path_results
            if  v.args.verbose >= 2:
                print ('Saving aggregate results for experiment_'+str(save_path_results)+marker)
                print ("Save directory")
                print (loc)         
            os.chdir(loc+marker+'/')
            self.create_result(marker, loc, "r")
            if  v.args.verbose >= 2:
                print ('Results saved in agg_sep_results\n\n')
        
        if marker == 'fifo':
            loc = save_path_results
            if  v.args.verbose >= 2:
                print ('Saving aggregate results for experiment_'+str(save_path_results)+marker)
                print ("Save directory")
                print (loc)         
            os.chdir(loc+marker+'/')
            self.create_result(marker, loc, "r")
            if  v.args.verbose >= 2:
                print ('Results saved in agg_sep_results\n\n')
            
        if marker == 'result':
            marker = 'lfu_fifo'
            loc = save_path_results
            if  v.args.verbose >= 2:
                print ('Saving aggregate results for experiment_'+str(save_path_results)+marker)
                print ("Save directory")
                print (loc)         
            os.chdir(loc+'/')
            print ('Marker')
            print (marker)
            print ('Loc')
            print (loc)
            self.create_result(marker, loc, "agg")
            if  v.args.verbose >= 2:
                print ('Results saved in agg_sep_results\n\n')

        if marker == 'merge':
            if v.args.rd == False:
                header = ['exp_ind', 'seed', 'cache_type', 'alpha_zero', 'delta_alpha', 'alpha', 'da_amp','cache_size', 'n', 'comp_time', 'decomp_time', 'total_time', 'comp_ratio', 'ds_size', 'ds_name', 'cached', 'win_size', 'nb_win', 'win_ind']
                save_loc = p.agg_results
            elif v.args.rd == True:
                header = ['exp_ind', 'cache_type', 'cache_size', 'n', 'comp_time', 'decomp_time', 'total_time', 'comp_ratio', 'ds_size', 'ds_name', 'cached', 'win_size', 'nb_win', 'win_ind']
                save_loc = p.real_dataset_save_path
                
            results = pd.DataFrame([])
            
            loc = save_path_results
            
            search = ''
            scss_search = ('_fifo.csv', '_lfu.csv')
            if v.args.lfu == False:
                search = '_fifo.csv'
            if v.args.fifo == False:
                search = '_lfu.csv'
            if v.args.fifo == True and v.args.lfu == True:    
                search = '_lfu_fifo.csv'
            
            for dirpath, dirs, files in os.walk(loc): 
                for filename in files:
                    if filename.endswith(search if v.args.scss == False else scss_search):
                        fname = os.path.join(dirpath,filename)
                        # dataset_name = [os.path.basename(fname)]
                        print (fname)                        
                        namedf = pd.read_csv(fname, skiprows=0, usecols=header)
                        # print (namedf)
                        results = results.append(namedf)
            if v.args.verbose >=2:
                print ('Saving results for all experiments in a single CSV')
                print ("Save directory")
            if not os.path.isdir(save_loc):
                os.makedirs(save_loc)
            results = results.dropna(how='all', axis='columns')
            results.to_csv(save_loc+self.file_name+'_'+marker+'.csv', index=None)
            if v.args.verbose >=2:
                print ('Results saved in agg_sep_results\n\n')
    
    def log_write(self, exp_des):
        log_location = self.save_path
        if not os.path.isdir(log_location):
                os.makedirs(log_location)
        log = open(log_location+"desc_"+self.file_name+".txt","a")# write mode 
        log.write(exp_des+"\n") 
        log.write("Index: "+str(self.file_name)+"\n") 
        log.write("Window index: "+str(self.win_ind)+"\n") 
        log.write("Cache management: "+str("True" if v.args.cm == True else "False")+"\n")
        log.write("Seed: "+str(self.seed)+"\n") 
        log.write("No of queries: "+str(self.n)+"\n") 
        log.write("Alpha zero: "+str(self.alpha_zero)+"\n") 
        log.write("Delta alpha: "+str(self.delta_alpha)+"\n") 
        log.write("Alpha: "+str(self.alpha)+"\n") 
        log.write("Delta alpha min: "+str(self.del_min)+"\n") 
        log.write("Delta alpha max: "+str(self.del_max)+"\n") 
        log.write("Delta alpha step: "+str(self.del_step)+"\n") 
        log.write("Cache size: "+str(self.cache_size)+"\n") 
        log.write("Cache type: "+str(self.cache_type)+"\n") 
        log.write("Window size: "+str(self.window_size)+"\n") 
        log.write("Number of windows: "+str(self.no_of_win)+"\n") 
        log.close() 
