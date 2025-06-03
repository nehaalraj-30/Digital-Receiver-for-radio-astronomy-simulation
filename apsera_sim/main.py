import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
from sine_input import sine_curve
from adc import sample,adc
from window import window_bits
from fft_12 import fft

M = 16
N = 1024
P = M*N
alpha = 1
n_bits = 14
v_ref = 3.3
f = 5e8
sampling_rate = 1e12 # for producing sine wave
adc_sampling_rate = 4e9
fft_points = 16*2**10

duration = fft_points/adc_sampling_rate # duration such that when sampled we get appropriate no. of points

time,vin_values = sine_curve(f,sampling_rate,duration,v_ref)

adc_time,adc_signal = sample(time,adc_sampling_rate,vin_values) # sample and hold

digital_values = [adc(vin,n_bits,v_ref) for vin in adc_signal] 

digital_values_no_offset = digital_values - np.mean(digital_values) # removing dc offset 

digital_values_no_offset = np.array((digital_values_no_offset)*2)/2**(n_bits) # normalising signal to regular sine wave

w_signal,gain = window_bits(digital_values_no_offset,n_bits)
windowed = digital_values_no_offset * w_signal # windowing signal

freq,mag = fft(M,N,P,windowed,adc_sampling_rate,gain)

plt.plot(adc_time, adc_signal,linestyle = 'dashed')
plt.xlabel('t(us)')
plt.ylabel('amplitude')
plt.title('signal')
plt.grid(True)
plt.savefig("input_main.png")
plt.show()
plt.close()

plt.step(adc_time*1e6, digital_values, where ='post')
plt.xlabel('time(us)')
plt.ylabel('Digital Output (Decimal)')
plt.title(f'{n_bits}-bit ADC Conversion')
plt.grid(True)
# plt.xlim(1,1.05)
plt.show()
plt.savefig("adc_main.png")

plt.step(adc_time*1e6,windowed,where = 'post')
plt.xlabel('t(us)')
plt.ylabel('amplitude')
plt.title('windowed_signal')
plt.grid(True)
# plt.xlim(1,1.05) 
plt.savefig("windowed_main.png")
plt.show()
plt.close()

plt.figure(figsize=(12, 6))
plt.plot(freq, mag, label='Row-Column FFT')
plt.title("Magnitude Spectrum (Row-Column FFT, M=16, N=1024)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("|X(f)|")
plt.xlim(-4000e6, 4000e6)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
plt.savefig("fft_main.png")


