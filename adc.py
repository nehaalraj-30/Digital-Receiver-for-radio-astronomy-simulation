import numpy as np

def sample(time,adc_sampling_rate,signal):
    step = int(len(time) / (adc_sampling_rate*(time[-1]-time[0]))) 
    return time[::step],signal[::step]

def adc(vin, n_bits, v_ref):
    vin_clipped = np.clip(vin,0,v_ref)
    return (np.floor((vin_clipped/v_ref)*(2**n_bits))).astype(int)




    
