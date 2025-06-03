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
    max_int = 2**n_bits - 1
    w_scaled = w/np.max(w)
    w_bits = np.round(w_scaled * max_int).astype(int)
    gain = np.sum(w)/length
    
    w_float_quantized = w_bits/max_int #fft takes float so convert to float
    
    return w_float_quantized,gain