import collections
from collections import Counter
import verbo as v
import pandas as pd

class cache_lfu:
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
            top_values = Counter(self.cache)
            high = top_values.most_common(self.cache_size)
            self.cache.clear()
            self.cache = dict(high)
            if v.args.verbose >= 3:
                print ('Maximum size of cache reached')
                print ('Current Cache: ')
                current_df = pd.DataFrame.from_dict(self.cache, orient='index', columns=['Frequency'])
                print (current_df)
                print ('\n')
                print ('Item with least frequency will be deleted.\n')
                # print (self.cache)
                # least_value = next(reversed(self.cache.items()))
                # least_value = min(self.cache.keys(), key=(lambda k: self.cache[k]))
                # print (str(least_value)+' is deleted \n')

            if v.args.verbose >= 3:
                print ('New cache:')
                new_df = pd.DataFrame.from_dict(self.cache, orient='index', columns=['Frequency'])
                print (new_df)
                print ('---------------------------------------------------------------')