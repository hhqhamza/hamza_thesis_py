# flexRL
flexible Reinforcement Learning Framework, usable for RL from straightforward to state of the art

# Parameters
  <ul>
<li>Line 1</li>
<li>Line 2</li>
</ul>
 -s define the seed  
 -sstart, -sstop, -sstep define the start, stop and step for the seed range function  
 -n deifnes the iterations  
 -nstart, -nstop, -nstep define the start, stop and step for the n range function  
 -a defines run experiment without random alpha without window size  
 -astart, -astop, -astep define the start, stop and step for the alpha range function and it must be gives as values of alpha are chosen at randon from a range of alphas  
 -wsstart, -wsstop, -wsstep define the start, stop and step for the window size range function  
 -csize defines the cache size  
 -fifo and -lfu define the types of cache  
 -cm Defines true or false for cache maintain state. If it is used same cache never renews, if not used new cache will be made for every experiment.  
 if -s is given than -sstart, -sstop, -sstep are ignored  
 if -n is given than -nstart, -nstop, -nstep are ignored  
 if -w is given than -wsstart, -wsstop, -wsstep are ignored  
 -m will merge all results in single file in the end of all the experiments. Without -m will merge results after each experiment  
 -cm does cache management if used same cache is used  
 -ws defines a single window size. if used with multiple windows it supercedes the multiples windows and only single window size is used.  
 -v defines level of verbosity. There are three level v=1, v=2 and v=3  

# Default parameter values
   Default cache size is 3  
   Default seed is 30  
   Default no of queries is 100  
   Default window size is 5  
   Default range of window size is start = 5 stop = 10 step = 5  
   Default range of alpha is start = 0.1 stop = 1.0 step = 0.1  
   Default range of delta alpha is start = -0.5 stop = +0.5 step = 0.1  
