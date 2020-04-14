import numpy as np
import pandas as pd
import cache_check as cc

class comp_decomp:
    def __init__(self, cache_type, data, cache_obj):
        self.cache_type = cache_type
        self.data = data
        self.cache_obj = cache_obj        
        self.result = []
        
    def comp_decomp(self):
        for fname in self.data:            
            print ("Requested item: " + str(fname))
            cc_obj = cc.check_cache(fname, self.cache_type)            
            if self.cache_obj.if_in_cache(str(fname)) == True:
                cache_results = cc_obj.in_cache()
                self.cache_obj.increment_cache(str(fname))
                self.result.append(cache_results)    
            if self.cache_obj.if_in_cache(str(fname)) == False:
                self.cache_obj.push_cache(str(fname))
                results = cc_obj.not_in_cache()
                self.result.append(results) 
            self.cache_obj.check_size()
            cache_df = pd.DataFrame.from_dict(self.cache_obj.cache, orient='index', columns=['Frequency']) 
            print (cache_df)
        return self.result