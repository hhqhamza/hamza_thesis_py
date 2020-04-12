import paths_all as p
import time
import os
import lz4.frame
import verbo as v

class comp_decomp:
    
    def set_seed_alpha(self, exp_ind, cache_type, cache_size, n, window_size, no_of_win, win_ind):
        self.cache_type = cache_type
        self.cache_size = cache_size
        self.n = n
        self.window_size = window_size
        self.no_of_win = no_of_win
        self.exp_ind = exp_ind
        self.win_ind = win_ind
                
    def in_cache(self, fname):
        cache_time_start = (time.time())*1000
        cache_file = os.urandom(len(fname))
        cache_time_end = (time.time())*1000
        if v.args.rd == True:
            cache_results = [str(self.exp_ind), str(self.cache_type), self.cache_size, int(self.n), '', '', round(float(cache_time_end-cache_time_start), 4), '', len(cache_file), fname, '1', self.window_size, self.no_of_win, self.win_ind]
        return cache_results
    
    def not_in_cache(self, fname):
        inputFile = os.urandom(len(fname))
        comp_time_start = (time.time())*1000
        compressed = lz4.frame.compress(inputFile)
        comp_time_end = (time.time())*1000
        compression_time = comp_time_end - comp_time_start
        original_size = len(inputFile)
        comp_file_size = len(compressed)
        decomp_time_start = (time.time())*1000
        decompressed = lz4.frame.decompress(compressed)
        decomp_time_end = (time.time())*1000
        decompression_time = decomp_time_end - decomp_time_start
        ratio = (comp_file_size/original_size) * 100       
        if v.args.rd == True:
            results = [str(self.exp_ind), str(self.cache_type), self.cache_size, int(self.n),  float("{0:.4f}".format(compression_time)), float("{0:.4f}".format(decompression_time)), float("{0:.4f}".format(compression_time+decompression_time)), round(ratio, 4), len(inputFile), fname, '0', self.window_size, self.no_of_win, self.win_ind]
        return results