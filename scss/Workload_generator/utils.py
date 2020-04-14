import numpy as np
import pandas as pd
import sys
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Randomise the data (Exponential Distribution)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_skewed_data(alpha_zero, delta_alpha, alpha_value, seed, n, data):
    random_query_save_path = ''
    random_query_csv = []
    data = data
    b = np.ravel(data)   
    iter = n
    i = 0
    alpha = alpha_value   # skewness parameter; the higher, the less skewed the distibution
    alpha_zero = alpha_zero
    delta_alpha = delta_alpha
    
    if alpha == 1.0:
        alpha = alpha + 0.1
    seed = seed
    
    n = len(b)
    if n == 0:
        print("No datasets found")
        sys.exit()
    f = lambda alpha,k,n: \
    (1 - alpha) / (1 - np.power(alpha,n)) * np.power(alpha,k)
    g = lambda k: f(alpha,k,n)
    k = range(0, n)
    ks = []
    for ki in k:
        ks.append(ki)
    dfks = pd.DataFrame(ks)
    dfp = dfks.apply(g)
    c = np.asanyarray(dfp)    
    np.random.seed(seed)
    
    while i < iter:
        random_choice = np.random.choice(data, p=np.ravel(c), replace=True)
        random_query_csv.append(random_choice)
        i += 1   
    return random_query_csv

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Float number range function for alpha
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def range_positve(start, stop=None, step=None):
    if stop == None:
        stop = start + 0.0
        start = 0.0
    if step == None:
        step = 1.0
    while start < stop:
        yield start
        start += step

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Get random alphas
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_rand_alpha(astart, astop, astep, seed, del_min, del_max, del_step):
    seed = seed
    np.random.seed(seed)
    # interval generation
    (min_alpha, max_alpha, step_alpha) = (astart, astop, astep)
    alphas_or = np.arange(min_alpha, max_alpha, step_alpha)

    nb_alphas = len(alphas_or)
    (min_delta_alpha, max_delta_alpha, step_delta_alpha) = (del_min, del_max, del_step)
    delta_alphas_or = np.arange(min_delta_alpha, max_delta_alpha, step_delta_alpha)
    
    # random selection
    alpha_zero = np.random.choice(list(alphas_or), 1)
    np.random.seed(seed)
    delta_alphas = np.random.choice(list(delta_alphas_or), nb_alphas)
    alphas = [alpha_zero + delta_alpha for delta_alpha in delta_alphas]
    alp = []   
    for delta_alpha in delta_alphas:
        deduced_alpha = min(max_alpha, max(min_alpha, alpha_zero + delta_alpha))        
        al = (alpha_zero, delta_alpha, deduced_alpha)
        alp.append(al)
    return (alp)
