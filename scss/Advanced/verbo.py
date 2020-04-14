import argparse

parser = argparse.ArgumentParser(description='Multiple compression experiment')

# Verbose
parser.add_argument("-v", "--verbose", type=int, default=0, help="Verbosity levels are 1, 2 and 3")

# Sample-based Caching Selection System (SCSS)
parser.add_argument("-scss", "--scss", action='store_true', help="Sample-based Caching Selection System")
parser.add_argument("-rd", "--rd", action='store_true', help="Use Real Data")

# Results merge
parser.add_argument("-m", "--m", action='store_true', help="If used files are merged after the completion of all the experiments")

# Cache type
parser.add_argument("-lfu", "--lfu", action='store_true', help="cache LFU")
parser.add_argument("-fifo", "--fifo", action='store_true', help="cache FIFO")

# Alpha
# parser.add_argument("-a", "--alpha", action='store', type=float, dest='alpha',help="Value of alpha")
parser.add_argument("-a", "--alpha", action='store_true', help="Random alpha")
parser.add_argument("-astart", "--astart", action='store', type=float, dest='astart', help="Staring value for alpha")
parser.add_argument("-astop", "--astop", action='store', type=float, dest='astop',help="Stoping value for alpha")
parser.add_argument("-astep", "--astep", action='store', type=float, dest='astep',help="Increment value for alpha")


# Seed
parser.add_argument("-s", "--seed", action='store', type=int, dest='seed',help="Seed for random function")
# Seed range
parser.add_argument("-sstart", "--sstart", action='store', type=int, dest='sstart', help="Staring value for seed")
parser.add_argument("-sstop", "--sstop", action='store', type=int, dest='sstop',help="Stoping value for seed")
parser.add_argument("-sstep", "--sstep", action='store', type=int, dest='sstep',help="Increment value for seed")

# Queries
parser.add_argument("-n", "--n", action='store', type=int, dest='n',help="Number of iterations")
# Queries range
parser.add_argument("-nstart", "--nstart", action='store', type=int, dest='nstart', help="Staring value for n")
parser.add_argument("-nstop", "--nstop", action='store', type=int, dest='nstop',help="Stoping value for n")
parser.add_argument("-nstep", "--nstep", action='store', type=int, dest='nstep',help="Increment value for n")

# Cache size
parser.add_argument("-csize", "--csize", action='store', type=int, dest='csize',help="Size of the cache")

# Mantain cache
parser.add_argument("-cm", "--cm", action='store_true', dest='cm',help="True and cache will be maintained. False and cache will be destroyed after each experiment")

# Windows_size
parser.add_argument("-ws", "--window_size", action='store', type=int, dest='window_size',help="Size of the window")
# Windows_size range
parser.add_argument("-wsstart", "--wsstart", action='store', type=int, dest='wsstart', help="Staring value for windows size")
parser.add_argument("-wsstop", "--wsstop", action='store', type=int, dest='wsstop',help="Stoping value for windows size")
parser.add_argument("-wsstep", "--wsstep", action='store', type=int, dest='wsstep',help="Increment value for windows size")

args = parser.parse_args()
# if args.verbose < 1 or args.verbose > 3:
    # prfloat("verbosity values are 1, 2 and 3")
    # prfloat 'Example command: python main.py -v  2 -lfu'
    # sys.exit()