import numpy as np

def SINAD(freq,mag_power_acc,start,stop):

    mags_power = mag_power_acc

    zipped_list = list(zip(freq, mags_power))  # Convert to list for slicing

    signal_part = [pair for pair in zipped_list if start <= pair[0] <= stop] #slice for freq b/w start and stop
    noise_part  = [pair for pair in zipped_list if not (start < pair[0] < stop)] #slice for restS

    mags_power_signal = list(zip(*signal_part))[1] #taking mag of signal
    mags_power_noise = list(zip(*noise_part))[1]   # taking mag of noise

    mean_power_signal = np.sum(mags_power_signal)
    mean_power_noise = np.sum(mags_power_noise)

    SINAD = 10*np.log10(mean_power_signal/mean_power_noise)

    return SINAD,mean_power_noise,mags_power_noise