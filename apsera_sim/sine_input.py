import numpy as np

def sine_curve(f,sampling_rate,duration,phase,acc):
    n_samples = int(duration*sampling_rate)
    t = np.linspace(0+acc*duration,duration+acc*duration,n_samples, endpoint= False)
    phase_rad = np.deg2rad(phase)
    scaling_1dbm = 0.3546 
    sine_sig = scaling_1dbm*((np.sin(2*np.pi*(f)*t+phase_rad))) + scaling_1dbm
    # offset and scaling to fit adc range 
    
    return t,sine_sig

