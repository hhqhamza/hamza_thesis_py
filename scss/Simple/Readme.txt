### cache_lfu.py
This is a class for an LFU cache
Items are inserted one by one and only frequency of each item is maintained
Item with least frequecy will be removed if cache is full

### cache_fifo.py
This is a class for an FIFO cache
Items are inserted one by one and niether frequency nor recency of any item is maintained
Item arrived first will be removed if cache is full

### cache_check.py
It simulated the transmission of requests
It has two functions
in_cache()
If the requested item is in the cache save the access time required to access the requested item and return the results.
not_in_cache()
If the requested item is not in the cache it will create an bytes object, i.e. equal to the size of the length of the requested item + 10000000 and compress it and decompress it and return the access time it took to perform the operation.

### comp_decomp.py
This is a wrapper for the main.py and main_scss.py
This uses the cache_lfu and cache_fifo classes to check if the requested item is in the cache or not.
According to the results retured from the cache_lfu and cache_fifo, it then calls the cache_check.py to calculate the access times.

### window.py
This class takes an input of data streams and return the streams in defined size windows.

### main.py
This is the example script written to define and start an experiment using windows of requests and LFU/ FIFO caches.

### main_scss.py
This is an addition to the main.py with SCSS example. After the first window of requests is run the scss.py is called.

### scss.py
This class samples items for the window and uses LFU and FIFO to assess the access times and return the cache type with least access time to be used for the next window of requests.