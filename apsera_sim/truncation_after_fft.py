
import matplotlib.pyplot as plt
import numpy as np
from sine_input import sine_curve
from adc import sample,adc
from window import window_bits,window_precision
from fft_return_complex import fft_complex
from truncating import truncate,truncate_after_fft

M = 16
N = 1024
P = M*N
alpha = 1
n_bits = [8,10,12,14,16,18,20,22,24]
truncate_bit = 12
adc_bits = 12
w_bit = 18
v_ref = 0.7962 # to keep output power that is adc at 2dBm of input 
f = 5e8
sampling_rate = 1e12 # for producing sine wave
adc_sampling_rate = 4e9
fft_points = 2**14

# duration such that when sampled we get appropriate no. of points
duration = fft_points/adc_sampling_rate 

time,vin_values = sine_curve(f,sampling_rate,duration,v_ref)

# sample and hold
adc_time,adc_signal = sample(time,adc_sampling_rate,vin_values) 

#passing adc
digital_values = [adc(vin,adc_bits,v_ref) for vin in adc_signal] 

# removing dc offset
digital_values_no_offset = np.array(digital_values) - (2**(adc_bits-1))
digital_values_no_offset = (digital_values_no_offset).astype(int)
 
w_signal,gain_bits = window_bits(adc_time,w_bit)

windowed_30 = digital_values_no_offset * w_signal # windowing signal
eps = 1e-12 # to avoid log(0)

# truncate to 12 bit
windowed_truncate = truncate(truncate_bit,windowed_30)
freq,re_part,im_part = fft_complex(M,N,P,windowed_truncate,adc_sampling_rate,gain_bits)

re_part_int = (np.round(re_part)).astype(np.int64)
im_part_int = (np.round(im_part)).astype(np.int64)

index_signal = np.array(im_part_int).argmax()
print("max re (signed 32-bit):", format((re_part_int[index_signal]) & 0xFFFFFFFF, '#034b'))
print("max im (signed 32-bit):", format((im_part_int[index_signal]) & 0xFFFFFFFF, '#034b'))

# from observed values truncating to 24 bits seems to retain fft properties
# also rounding to 18 bits 
re_part_trunc,im_part_trunc = truncate_after_fft(re_part_int,im_part_int,fft_points)

sq_real = np.square(re_part_trunc)
sq_im = np.square(im_part_trunc)
power_spectrum = (np.array(sq_real)+np.array(sq_im))

plt.figure(figsize=(10,4))
plt.plot(freq,power_spectrum)
plt.xlim(0,4000e6)
plt.title("power_spectrum of FFT Output Signal")
plt.xlabel("freq")
plt.ylabel("Power")
plt.grid(True)
plt.show()

power_spectrum_accu = [0]*len(power_spectrum)

for i in range(0,4095):
    power_spectrum_accu = power_spectrum + power_spectrum_accu
 
plt.figure(figsize=(10,4))
plt.plot(freq,power_spectrum_accu)
plt.xlim(0,2000e6)
plt.title("power_spectrum and accumalation of FFT Output Signal")
plt.xlabel("freq")
plt.ylabel("power_spectrum_accu")
plt.grid(True)
plt.show()    
       