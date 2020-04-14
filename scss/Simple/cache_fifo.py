import collections
from collections import Counter
import pandas as pd
from collections import deque

class cache_fifo:
    def __init__(self):        
        self.fname = ''
        self.cache_counter = 1
        self.cache = collections.OrderedDict()
    
    def set_cache_size(self, cache_size):
        self.cache_size = cache_size
                
    def if_in_cache(self, fname):
        if fname in self.cache.keys():
            return True
        if fname not in self.cache.keys():
            return False

    def increment_cache(self, fname):
        self.cache[fname] += 1
    
    def push_cache(self, fname):
        self.cache[fname] = self.cache_counter

    def check_size(self):
        if len(self.cache) > self.cache_size:
            poped = self.cache.popitem(last=False)
            print ("++++++++++++++++++++++++++++++++++++++++++++")
            print ('Maximum size of FIFO cache has reached')
            print ("++++++++++++++++++++++++++++++++++++++++++++")         