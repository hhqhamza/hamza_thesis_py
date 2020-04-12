# flexRL
flexible Reinforcement Learning Framework, usable for RL from straightforward to state of the art

# Parameters
<ul>
<li>-s define the seed
<li>-sstart, -sstop, -sstep define the start, stop and step for the seed range function </li>
<li>-n deifnes the iterations</li>
<li>-nstart, -nstop, -nstep define the start, stop and step for the n range function </li>
<li>-a defines run experiment without random alpha without window size </li>
<li>-astart, -astop, -astep define the start, stop and step for the alpha range function and it must be gives as values of alpha are chosen at randon from a    range of alphas</li>
<li>-ws defines a single window size. if used with multiple windows it supercedes the multiples windows and only single window size is used.</li>
<li>-wsstart, -wsstop, -wsstep define the start, stop and step for the window size range function </li>
<li>-csize defines the cache size</li>
<li>-fifo and -lfu define the types of cache</li>
<li>-cm does cache management if used same cache is used </li>
<li>-cm Defines true or false for cache maintain state. If it is used same cache never renews, if not used new cache will be made for every experiment.</li>
<li>-m will merge all results in single file in the end of all the experiments. Without -m will merge results after each experiment</li>
<li>-v defines level of verbosity. There are three level v=1, v=2 and v=3</li>
<li>if -s is given than -sstart, -sstop, -sstep are ignored</li>
<li>if -n is given than -nstart, -nstop, -nstep are ignored</li>
<li>if -w is given than -wsstart, -wsstop, -wsstep are ignored</li>
</ul>
