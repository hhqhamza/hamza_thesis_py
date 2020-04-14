# import comp_decomp as cd
import pandas as pd
import sys
import random
import numpy as np

class window:
    def __init__(self, window_size, n, data):
        self.window_size = window_size
        self.n = n
        self.data = data

    def get_window(self):
        for win_size in self.window_size:
            win_ind = 0
            no_of_win = self.n//win_size
            new_n = win_size
            # print ("Window size: " +str(win_size))
            # print ("Total no of windows: " +str(no_of_win))
            start_win = 0
            stop_win = win_size
            for nbw in range(start_win, no_of_win):
                df_fifo_r = pd.DataFrame()
                df_lfu_r = pd.DataFrame()
                win_ind += 1
                qd = self.data[start_win:stop_win] # Selected window of requests from stream
                # print ("Window index: " + str(win_ind))
                # print ("No of windows: " + str(nbw))
                # print ("Start win: " + str(start_win))
                # print ("Stop win: " + str(stop_win))        
                # print ("Selected queries")
                # print (qd)
                # print ("Length of selected queries: " + str(len(qd)))
                start_win = stop_win
                stop_win = stop_win + win_size
                yield  qd
                