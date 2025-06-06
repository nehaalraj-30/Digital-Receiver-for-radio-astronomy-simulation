import numpy as np

def sine_curve(f,sampling_rate,duration,v_ref):
    n_samples = int(duration*sampling_rate)
    t = np.linspace(0,duration,n_samples, endpoint= False)
    scaling_1dBm = 0.3546
    sine_sig = scaling_1dBm*((np.sin(2*np.pi*(f)*t)))+scaling_1dBm # offset and scaling to fit adc range 
    
    return t,sine_sig

