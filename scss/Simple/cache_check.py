import time
import os
import lz4.frame


class check_cache:
    
    def __init__(self, fname, cache_type):
        self.fname = fname
        self.cache_type = cache_type
                
    def in_cache(self):
        cache_time_start = time.time() * 1000
        cache_file = os.urandom(len(self.fname))
        cache_time_end = time.time() * 1000
        cache_results = str(self.cache_type), '', '', cache_time_end-cache_time_start,'', self.fname, '1'
        return cache_results
    
    def not_in_cache(self):
        inputFile = os.urandom(len(self.fname)+10000000)
        comp_time_start = time.time() * 1000
        compressed = lz4.frame.compress(inputFile)
        comp_time_end = time.time() * 1000
        compression_time = comp_time_end - comp_time_start
        original_size = len(inputFile)
        comp_file_size = len(compressed)
        decomp_time_start = (time.time()) * 1000
        decompressed = lz4.frame.decompress(compressed)
        decomp_time_end = (time.time()) * 1000
        decompression_time = decomp_time_end - decomp_time_start
        ratio = (comp_file_size/original_size) * 100       
        results = str(self.cache_type),  compression_time, decompression_time, compression_time+decompression_time, round(ratio, 4), self.fname, '0'
        return results