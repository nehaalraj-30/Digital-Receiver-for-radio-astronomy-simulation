import numpy as np

def sine_curve(f,sampling_rate,duration,v_ref):
    n_samples = int(duration*sampling_rate)
    t = np.linspace(0,duration,n_samples, endpoint= False)
    sine_sig = (np.sin(2*np.pi*(f)*t)+1)*(v_ref/2)
    
    return t,sine_sig

