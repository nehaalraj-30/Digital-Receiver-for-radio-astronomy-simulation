import matplotlib.pyplot as plt
from sine_input import sine_curve
from fft_12 import fft
from adc import sample,adc
import numpy as np

M = 16
N = 1024
P = M*N
n_bits = 12
v_ref = 3.3
f = 2e8
adc_sampling_rate = 4e9
fft_points = 16*2**10
sampling_rate=1e12

duration = fft_points/adc_sampling_rate

t,sine_sig=sine_curve(f,sampling_rate,duration,v_ref)

time_sine,sine_signal = sample(t,adc_sampling_rate,sine_sig)
sine_signal_scaled = ((sine_signal)*2)/v_ref
sine_signal_scaled = np.array(sine_signal_scaled)*2048
sine_signal_fft = sine_signal_scaled - np.mean(sine_signal_scaled)
sine_og = ((sine_signal - np.mean(sine_signal))*2)/v_ref

plt.plot(time_sine, sine_og ,linestyle = 'dashed',marker='o')
plt.xlabel('t(us)')
plt.ylabel('amplitude') 
plt.title('signal')
plt.grid(True)
plt.savefig("fp_signal.png")
plt.show()

freqs_fp,mags_fp = fft(M,N,P,sine_signal_fft,adc_sampling_rate,gain=1)

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

digital_values = [adc(vin,n_bits,v_ref) for vin in adc_signal]

no_offset_dig = digital_values - np.mean(digital_values)

plt.step(adc_time*1e6, no_offset_dig, where ='post',marker='o')
plt.xlabel('time(us)')
plt.ylabel('Digital Output (Decimal)')
plt.title(f'{n_bits}-bit ADC Conversion')
plt.grid(True)
plt.savefig("adc_dig.png")
plt.show()
plt.close()

freqs_n_bits,mags_n_bits = fft(M,N,P,no_offset_dig,adc_sampling_rate,gain=1)

plt.figure(figsize=(12, 6))
plt.plot(freqs_n_bits, mags_n_bits, label='n_bits Signal FFT')
plt.title("FFT of f'{n_bit} Signal (Row-Column FFT)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("|X(f)|")
plt.grid(True)
plt.savefig("Dig_fft.png")
plt.show()
plt.close()

diff_mag = mags_fp - mags_n_bits

plt.figure(figsize=(12, 6))
plt.plot(freqs_n_bits, diff_mag, label='n_bits Signal FFT')
plt.title("FFT of f'{n_bit} Signal (Row-Column FFT)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("|X(f)|")
plt.grid(True)
plt.savefig("fft_diff.png")
plt.show()
plt.close()

diff=[]
for x in range (0,len(no_offset_dig)):
    diff.append(-(digital_values[x]-sine_signal_scaled[x]))

plt.figure(figsize=(12, 6))
plt.plot(adc_time, diff, label='error')
plt.title("error of f'{n_bit} Signal (Row-Column FFT)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("LSB")
plt.grid(True)
plt.savefig("sig_error.png")
plt.show()
plt.close()

