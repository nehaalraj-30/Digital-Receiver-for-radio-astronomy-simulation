import matplotlib.pyplot as plt
from sine_input import sine_curve
from fft_12 import fft
from adc import sample,adc
import numpy as np

M = 16
N = 1024
P = M*N
gain=1
n_bits = 12
v_ref = 3.3
f = 5e8
adc_sampling_rate = 4e9
fft_points = 16*2**10
sampling_rate=1e12
n_bit=12
n_bits = [8, 10, 12, 14, 16, 18]
duration = fft_points/adc_sampling_rate

t,sine_sig=sine_curve(f,sampling_rate,duration,v_ref)

time_sine,sine_signal = sample(t,adc_sampling_rate,sine_sig)
sine_signal_scaled = ((sine_signal)*2)/v_ref
sine_signal_scaled = np.array(sine_signal_scaled)*(2**(n_bit-1))
sine_signal_fft = sine_signal_scaled - np.mean(sine_signal_scaled)
sine_og = (sine_signal - np.mean(sine_signal))  
sine_og = sine_og *(2/v_ref)

plt.plot(time_sine, sine_og ,linestyle = 'dashed',marker='o')
plt.xlabel('t(us)')
plt.ylabel('amplitude') 
plt.title('signal')
plt.grid(True)
plt.savefig("fp_signal.png")
plt.show()

sine_signal_fft=sine_signal_fft/(2**(n_bit-1))

y=np.fft.fft(sine_signal_fft,n=fft_points)
mags_fp= np.abs(y)[:fft_points]
freqs_fp = np.fft.fftfreq(fft_points, d=1/adc_sampling_rate)[:fft_points]
mags_fp = mags_fp / fft_points

freqs_fp=np.fft.fftshift(freqs_fp)
mags_fp=np.fft.fftshift(mags_fp)
plt.figure(figsize=(12, 6))
plt.plot(freqs_fp, mags_fp, label='Full-Precision Signal FFT')
plt.title("FFT of Full-Precision Signal (Row-Column FFT)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("|X(f)|")
plt.grid(True)
plt.savefig("fp_fft.png")
plt.show()
plt.close()

time,vin_values = sine_curve(f,sampling_rate,duration,v_ref)

adc_time,adc_signal = sample(time,adc_sampling_rate,vin_values)

plt.figure(figsize=(12, 6))
for bit in n_bits:
    digital_values = [adc(vin, bit, v_ref) for vin in adc_signal]
    no_offset_dig = digital_values - np.mean(digital_values)
    no_offset_dig = no_offset_dig / 2**(bit - 1)

    sine_signal_scaled_loop = ((sine_signal) * 2) / v_ref
    sine_signal_scaled_loop = np.array(sine_signal_scaled_loop) * (2**(bit - 1))

    freqs_n_bits,mags_n_bits = fft(M,N,P,no_offset_dig,adc_sampling_rate,gain)
    plt.plot(freqs_n_bits, mags_n_bits, label=f'{bit}-bit')

plt.title("FFT of Digital Signals (All Bit Widths)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("|X(f)|")
plt.grid(True)
plt.legend()
plt.savefig("Dig_fft_combined.png")
plt.show()
plt.close()

target_min = -1.46e9
target_max = -1.36e9
epsilon = 1e-12

mean_errors = []

for bit in n_bits:
    digital_values = [adc(vin, bit, v_ref) for vin in adc_signal]
    no_offset_dig = digital_values - np.mean(digital_values)
    no_offset_dig = no_offset_dig / (2 ** (bit - 1))

    freqs_n_bits,mags_n_bits = fft(M,N,P,no_offset_dig,adc_sampling_rate,gain)
    diff_mag = mags_fp - mags_n_bits
    diff_mag_db = 20 * np.log10(np.abs(diff_mag) + epsilon)

    mask = (freqs_n_bits >= target_min) & (freqs_n_bits <= target_max)
    error_in_range = diff_mag_db[mask]
    mean_error = np.mean(error_in_range)

    mean_errors.append(mean_error)



# Plot mean error vs n_bits
plt.figure(figsize=(10, 6))
plt.plot(n_bits, mean_errors, marker='o', linestyle='-', color='b')
plt.title("Mean FFT Error (dB) vs Bit Width in Range -1.46 GHz to -1.36 GHz")
plt.xlabel("Bit Width (n_bits)")
plt.ylabel("Mean Magnitude Error (dB)")
plt.grid(True)
plt.savefig("fft_mean_error_vs_nbits.png")
plt.show()
plt.close()


full_errors = []

for bit in n_bits:
    digital_values = [adc(vin, bit, v_ref) for vin in adc_signal]
    no_offset_dig = digital_values - np.mean(digital_values)
    no_offset_dig = no_offset_dig / (2 ** (bit - 1))

    freqs_n_bits,mags_n_bits = fft(M,N,P,no_offset_dig,adc_sampling_rate,gain)
    diff_mag = mags_fp - mags_n_bits
    diff_mag_db = 20 * np.log10(np.abs(diff_mag) + epsilon)

    
    error_in_range = diff_mag_db
    mean_error = np.mean(error_in_range)

    full_errors.append(mean_error)

plt.figure(figsize=(10, 6))
plt.plot(n_bits, full_errors, marker='o', linestyle='-', color='b')
plt.title("full Mean FFT Error (dB) ")
plt.xlabel("Bit Width (n_bits)")
plt.ylabel("Mean Magnitude Error (dB)")
plt.grid(True)
plt.savefig("fft_mean_error_vs_nbits.png")
plt.show()
plt.close()

