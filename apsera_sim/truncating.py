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
    max_int = 2**(n_bits-1) - 1
    # bring b/w 0 and 1
    windowed_scale = windowed_sig/np.max(windowed_sig)  
    # assign appropriate integers depending upon bits
    windowed_truncated = np.round(windowed_scale * max_int)
    
    # windowed_truncated_final = windowed_truncated/max_int
    
    return windowed_truncated

def truncate_after_fft(re_part_int,im_part_int,fft_points):

    for i in range(fft_points):
        if re_part_int[i]>=0:
            re_part_int[i] = (re_part_int[i]%(2**25))//2**7 
        if re_part_int[i]<0:
            re_part_int[i] = -((-(re_part_int[i])%(2**25))//2**7)
        if im_part_int[i]>=0:
            im_part_int[i] = (im_part_int[i]%(2**25))//2**7       
        if im_part_int[i]<0:
            im_part_int[i] = -((-(im_part_int[i])%(2**25))//2**7)
    
    return re_part_int,im_part_int
