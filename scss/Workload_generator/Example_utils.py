import utils as ul
import pandas as pd

################################ Test for utils.py #################################


################################ Tunning parameters ################################
seed = [20]
iter = [40]

astart = 0.1
astop = 2.0
astep = 0.1

del_min = -1.5
del_max = +1.5
del_step = 0.1


##################################### Dataset ######################################
list_of_datasets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 


############################### Generate list of Alphas ############################
# Get a list of alphas e.g. [0.1, 0.2, 0.3, 0.4, ....]
# alphas =[]
# alpha_zero = 0.1
# delta_alpha = 0.5
# for alpha in ul.range_positve(astart, astop, astep):
	# alphas.append(alpha)
# print ("Alphas")
# print (alphas)


########################## Generate random list of Alphas ##########################
# Un comment following to get a random list of alphas and comment the section above i.e. Get a list of alphas
# Get a random list of alphas e.g. [0.6, 0.3, 0.3, 0.4, ....]
# Gives a random list of alpha from a range of (alpha_start, alpha_stop, alpha_step)
# If the range has 10 number of alphas, then 10 random alphas will be returned
#===================================================================================
rand_alpha_list = ul.get_rand_alpha(astart, astop, astep, seed, del_min, del_max, del_step)

alpha_zero = []
for al_zero in rand_alpha_list:
    alpha_zero.append(round(float(al_zero[0]), 1))
    
delta_alpha = []
for delta_al in rand_alpha_list:
    delta_alpha.append(round(float(delta_al[1]), 1))
    
alphas = []
for al_rand in rand_alpha_list:
    alphas.append(round(float(al_rand[2]), 1))


#################################### Store Results #################################
rand_df = pd.DataFrame()


######################################## Main ######################################
for alpha in alphas:	
    for s in seed:
        for n in iter:           
            data_df = ul.get_skewed_data(alpha_zero, delta_alpha, alpha, s, n, list_of_datasets)		
            # rand_df['alpha-'+str(alpha)+'_seed-'+str(s)+'_n-'+str(n)] = data_df
            rand_df['alpha-'+str(alpha)] = data_df

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)	
print (rand_df)
rand_df.to_csv('random_data.csv')
