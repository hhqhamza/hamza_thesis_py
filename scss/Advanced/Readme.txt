### Author 
Hamza

### Description
This is the experimental setup I used. It uses command line parameters to configure it. It uses synthetic and real workload.

input folder has the data set that can be used to generate synthetic data


### Paths
paths_all.py can be configured for input data and results
datasets_location: The location of the input folder.
datasets_found_save_path: Location to save the list of all the found datasets in input folder in a csv file.
random_query_save_path: The location where the list queries with respect to skewness are going to be saved.
results_save_path: location for results of LFU and FIFO in a seperate csv file with respect to each alpha value.
agg_sep_results: location for combinedLFU results and combined FIFO resutls in seperated csv files.
agg_results: location for combined LFU and FIFO results in a single csv.
real_dataset_path: path for the real dataset
real_dataset_save_path: location of the resutls
real_dataset_log_path: location for the logs

### Parameters
-s define the seed
-sstart, -sstop, -sstep define the start, stop and step for the seed range function
-n deifnes the iterations
-nstart, -nstop, -nstep define the start, stop and step for the n range function
-a defines run experiment without random alpha without window size
-astart, -astop, -astep define the start, stop and step for the alpha range function and it must be gives as values of alpha are chosen at randon from a range of alphas
-ws defines a single window size. if used with multiple windows it supercedes the multiples windows and only single window size is used.
-wsstart, -wsstop, -wsstep define the start, stop and step for the window size range function
-csize defines the cache size
-fifo and -lfu define the types of cache
-cm does cache management if used same cache is used
-cm Defines true or false for cache maintain state. If it is used same cache never renews, if not used new cache will be made for every experiment.
-m will merge all results in single file in the end of all the experiments. Without -m will merge results after each experiment
-v defines level of verbosity. There are three level v=1, v=2 and v=3
if -s is given than -sstart, -sstop, -sstep are ignored
if -n is given than -nstart, -nstop, -nstep are ignored
if -w is given than -wsstart, -wsstop, -wsstep are ignored

### Default parameter values
Default vlaues can be modified in constants.py
Default cache size is 3
Default seed is 30
Default no of queries is 100
Default window size is 5
Default range of window size is start = 5 stop = 10 step = 5
Default range of alpha is start = 0.1 stop = 1.0 step = 0.1
Default range of delta alpha is start = -0.5 stop = +0.5 step = 0.1

### Example commands
For synthetic data:
python3 main.py -csize=3 -fifo -lfu -sstart=10 -sstop=1000 -sstep=10 -ws=500 -n=25000 -astart=0.1 -astop=1.0 -astep=0.1 -cm -m -scss
For real data:
python3 main.py -csize=3 -fifo -lfu -wsstart=50 -wsstop=500 -wsstep=20 -cm -m -scss -rd