import   numpy as np

def SNR(freq,mag_power_acc,start,stop):

    mags_power = mag_power_acc

    zipped_list = list(zip(freq, mags_power))  # Convert to list for slicing

    signal_part = [pair for pair in zipped_list if start <= pair[0] <= stop] #slice for freq b/w start and stop
    noise_part  = [pair for pair in zipped_list if not (start < pair[0] < stop)] #slice for restS

    signal_max_and_freq = max(zipped_list, key=lambda x: x[1]) # lambda creates a throwaway function to take the second element of a tuple, find max of it 
    freq_max = signal_max_and_freq[0]

    tolerance = 0.005e6
    harmonics = []
    for i in range(2,6):
        harmonic_freqs = i*freq_max
        harmonics.append(harmonic_freqs) # collecting harmonic frequency
    
    #having a zipped list whitout harmonics with magnitude , tolerance of 0.05e6 for the harmonics
    noise_without_THD = [pair for pair in noise_part if not (any(np.abs(pair[0] - h)< tolerance for h in harmonics))] 
    mags_power_noise_THD= list(zip(*noise_without_THD))[1]
    mags_power_signal = list(zip(*signal_part))[1]

    mean_power_signal = np.sum(mags_power_signal)
    mean_power_noise_THD = np.sum(mags_power_noise_THD)

    SNR = 10*np.log10(mean_power_signal/mean_power_noise_THD)

    return SNR 