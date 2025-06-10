import numpy as np
import matplotlib.pyplot as plt
from window import window_bits,window_precision,window_bits_normalised

M = 16
N = 1024
P = M*N
n_bits = [14,16,18]
fft_points = 16*2**10
sampling_rate_input = 1e12
adc_sampling_rate = 4e9
duration = fft_points/adc_sampling_rate 
n_samples = int(duration * sampling_rate_input)
t = np.linspace(0,duration,n_samples,endpoint = False)
dt = t[1]-t[0] # d=sampling interval in seconds

plt.figure(figsize=(12, 6))

full_precision,gain = window_precision(t)
#giving number of points greater than 16k but lesser than 32k for better graph and keep within computational power
fft_len = 2**int(np.ceil(np.log2(len(full_precision)))+1)  
freq_full_precision = np.fft.fft(full_precision,fft_len) 
freq_full_precision_shift = np.fft.fftshift(freq_full_precision) # o/p shift to center
freqs_precision = np.fft.fftshift(np.fft.fftfreq(fft_len,d=dt))  #bin-shift to center

eps = 1e-12 # to avoid dividing by 0
#dividing each point by its max 
freq_full_precision_shift_db = 20 * np.log10(np.abs(freq_full_precision_shift) / np.max(np.abs(freq_full_precision_shift))+eps)
plt.plot(freqs_precision, freq_full_precision_shift_db, label='Full-Precision Window')

for bit in n_bits:
    n_bits_window,gain = window_bits(t,bit)
    freq_n_bits = np.fft.fft(n_bits_window,fft_len)  # Zero-padding 
    freq_n_bits_shift = np.fft.fftshift(freq_n_bits) # o/p shift
    freqs_bits = np.fft.fftshift(np.fft.fftfreq(fft_len,d=dt))  #bin-shift 
    freq_n_bits_shift_db = 20 * np.log10(np.abs(freq_n_bits_shift) / np.max(np.abs(freq_n_bits_shift))+eps)
    plt.plot(freqs_bits, freq_n_bits_shift_db, label=f'{bit}-bit Truncated Window')
    
bits_18_window,gain = window_bits_normalised(t,18)
freq_n_bits_18 = np.fft.fft(bits_18_window,fft_len)  # Zero-padding 
freq_n_bits_shift_18 = np.fft.fftshift(freq_n_bits_18) # o/p shift
freqs_bits = np.fft.fftshift(np.fft.fftfreq(fft_len,d=dt))  #bin-shift 
diff_18 = freq_full_precision_shift-freq_n_bits_shift_18
freq_error_db_18 = 20 * np.log10(np.mean(np.abs(diff_18)+eps))


bits_25_window,gain = window_bits_normalised(t,25)
freq_n_bits = np.fft.fft(bits_25_window,fft_len)  # Zero-padding 
freq_n_bits_shift_25 = np.fft.fftshift(freq_n_bits) # o/p shift
freqs_bits = np.fft.fftshift(np.fft.fftfreq(fft_len,d=dt))  #bin-shift 
diff_25 = freq_full_precision_shift-freq_n_bits_shift_25
freq_error_db_25 = 20 * np.log10(np.mean(np.abs(diff_25)+eps))

print(f"error in 18 bit window with respect to full precision in dbfs = {freq_error_db_18}")
print(f"error in 25 bit window with respect to full precision in dbfs = {freq_error_db_25}")


plt.title(f"Magnitude Spectrum db")
plt.xlabel("Frequency (Hz)")
plt.ylabel("|X(f)|")
plt.xlim(-adc_sampling_rate / 2, adc_sampling_rate / 2)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("fft_main_superimposed_2.png")
plt.show()

# error very less for 18 bits from graph
