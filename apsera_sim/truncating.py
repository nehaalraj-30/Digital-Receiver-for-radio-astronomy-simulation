import numpy as np

def truncate_normalised(n_bits,windowed_sig):
    max_int = 2**n_bits - 1
    # bring b/w 0 and 1
    windowed_scale = windowed_sig/np.max(windowed_sig)  
    # assign appropriate integers depending upon bits
    windowed_truncated = np.round(windowed_scale * max_int)
    
    windowed_truncated_normalised = windowed_truncated/max_int
    
    return windowed_truncated_normalised

def truncate(n_bits,windowed_sig):
    max_int = 2**n_bits - 1
    # bring b/w 0 and 1
    windowed_scale = windowed_sig/np.max(windowed_sig)  
    # assign appropriate integers depending upon bits
    windowed_truncated = np.round(windowed_scale * max_int)
    
    # windowed_truncated_final = windowed_truncated/max_int
    
    return windowed_truncated
    
