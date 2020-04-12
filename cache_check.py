import paths_all as p
import time
import os
import lz4.frame
import verbo as v

class comp_decomp:
    
    def set_seed_alpha(self, exp_ind, seed, alpha_zero, delta_alpha, alpha, del_max, cache_type, cache_size, n, window_size, no_of_win, win_ind):
        self.seed = seed
        self.alpha_zero = alpha_zero
        self.delta_alpha = delta_alpha
        self.alpha = alpha
        self.cache_type = cache_type
        self.cache_size = cache_size
        self.n = n
        self.window_size = window_size
        self.no_of_win = no_of_win
        self.exp_ind = exp_ind
        self.win_ind = win_ind
        self.del_max = del_max
        
    def in_cache(self, fname):
        cache_time_start = (time.time())*1000
        cache_file = open(fname, 'r')
        cache_file.close()
        cache_time_end = (time.time())*1000
        if v.args.rd == False:
            cache_results = [str(self.exp_ind), int(self.seed), str(self.cache_type), str(self.alpha_zero), str(self.delta_alpha), str(self.alpha), str(self.del_max), self.cache_size, int(self.n), '', '', round(float(cache_time_end-cache_time_start), 4), '', float(os.path.getsize(cache_file.name)), os.path.basename(fname), '1', self.window_size, self.no_of_win, self.win_ind]
        # if v.args.rd == True:
            # cache_results = [str(self.exp_ind),'', str(self.cache_type), '', '', '', '', self.cache_size, int(self.n), '', '', round(float(cache_time_end-cache_time_start), 4), '', float(os.path.getsize(cache_file.name)), os.path.basename(fname), '1', self.window_size, self.no_of_win, self.win_ind]
        return cache_results
    
    def not_in_cache(self, fname):
        inputFile = open(fname, 'rb')
        comp_time_start = (time.time())*1000
        compressed = lz4.frame.compress(inputFile.read())
        comp_time_end = (time.time())*1000
        compression_time = comp_time_end - comp_time_start
        with open(inputFile.name + '_compressed', 'wb') as comp:
            comp.write(compressed)
            comp.flush()
            comp.close()
        original_size = float(os.path.getsize(inputFile.name))
        comp_file_size = float(os.path.getsize(comp.name))
        os.remove(inputFile.name + '_compressed')
        decomp_time_start = (time.time())*1000
        decompressed = lz4.frame.decompress(compressed)
        decomp_time_end = (time.time())*1000
        decompression_time = decomp_time_end - decomp_time_start
        ratio = (comp_file_size/original_size) * 100
        if v.args.rd == False:
            results = [str(self.exp_ind), int(self.seed), str(self.cache_type), str(self.alpha_zero), str(self.delta_alpha), str(self.alpha), str(self.del_max), self.cache_size, int(self.n),  float("{0:.4f}".format(compression_time)), float("{0:.4f}".format(decompression_time)), float("{0:.4f}".format(compression_time+decompression_time)), round(ratio, 4), float(os.path.getsize(inputFile.name)), os.path.basename(fname), '0', self.window_size, self.no_of_win, self.win_ind]
        # if v.args.rd == True:
            # results = [str(self.exp_ind), '', str(self.cache_type), '', '', '', '', self.cache_size, int(self.n),  float("{0:.4f}".format(compression_time)), float("{0:.4f}".format(decompression_time)), float("{0:.4f}".format(compression_time+decompression_time)), round(ratio, 4), float(os.path.getsize(inputFile.name)), os.path.basename(fname), '0', self.window_size, self.no_of_win, self.win_ind]
        return results