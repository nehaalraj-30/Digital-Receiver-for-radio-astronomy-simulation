from scipy import signal
import numpy as np

def window_precision(t):
    length = len(t)
    w = signal.windows.hann(length)
    gain = np.sum(w)/length
    
    return w,gain

def window_bits(t,n_bits):
    length = len(t)
    w = signal.windows.hann(length)
    max_int = 2**(n_bits-1) - 1 
    w_scaled = w/np.max(w)
    # scaling so that when we multiply by max int window is stil b/w 0 -> 1
    w_bits = np.round(w_scaled* max_int).astype(int) 
    # multiplying by max possible integer for n bit representation then rounding and typecasting to int 
    gain = np.sum(w)/length
    
    #normalising back to 0->1
    # w_float_quantized = (w_bits/max_int)
    
    return w_bits,gain

def window_bits_normalised(t,n_bits):
    length = len(t)
    n_bits -= 1
    w = signal.windows.hann(length)
    max_int = 2**n_bits - 1 
    w_scaled = w/np.max(w)
    # scaling so that when we multiply by max int window is stil b/w 0 -> 1
    w_bits = np.round(w_scaled* max_int).astype(int) 
    # multiplying by max possible integer for n bit representation then rounding and typecasting to int 
    gain = np.sum(w)/length
    
    #normalising back to 0->1
    w_float_quantized = (w_bits/max_int)
    
    return w_float_quantized,gain