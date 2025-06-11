
import matplotlib.pyplot as plt
import numpy as np
from sine_input import sine_curve
from adc import sample,adc
from window import window_bits
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
f1 = 5e8
f2 = 5e8
sampling_rate = 1e12 # for producing sine wave
adc_sampling_rate = 4e9
fft_points = 2**14

# duration such that when sampled we get appropriate no. of points
duration = fft_points/adc_sampling_rate 

time,vin_values = sine_curve(f1,sampling_rate,duration,0,acc=1)

adc_time,adc_signal = sample(time,adc_sampling_rate,vin_values) 

#passing adc
digital_values = [adc(vin,adc_bits,v_ref) for vin in adc_signal] 
 
# removing dc offset
digital_values_no_offset = np.array(digital_values) - (2**(adc_bits-1))
digital_values_no_offset = (digital_values_no_offset).astype(int)

w_signal,gain_bits = window_bits(adc_time,w_bit)

#windowing 
windowed_30 = digital_values_no_offset * w_signal
eps = 1e-12 # to avoid log(0)

# truncate to 12 bit
windowed_truncate = truncate(truncate_bit,windowed_30)

# fft
freq,re_part,im_part = fft_complex(M,N,P,windowed_truncate,adc_sampling_rate,gain_bits)

#converting to int
re_part_int= (np.round(re_part)).astype(np.int64)
im_part_int = (np.round(im_part)).astype(np.int64)

index_signal_1 = np.array(im_part_int).argmax()
index_signal_2 = np.array(im_part_int).argmax()
print("max real part (signed 32-bit):", format((re_part_int[index_signal_1]) & 0xFFFFFFFF, '#034b'))
print("imaginary part at tone(signed 32-bit):", format((im_part_int[index_signal_1]) & 0xFFFFFFFF, '#034b'))

re_part_trunc,im_part_trunc = truncate_after_fft(re_part_int,im_part_int,fft_points)

index_signal_trunc = np.array(im_part_trunc).argmax()
print("Max integer after truncation", max(im_part_trunc))
print("imaginary part at tone after truncation (signed 32-bit):", format((im_part_trunc[index_signal_trunc]) & 0xFFFFFFFF, '#020b'))

# from observed values truncating to 25 bits seems to retain fft properties therefore shaving from MSB till 25 bits
# also rounding to 18 bits to keep withing DSP 48 slice
