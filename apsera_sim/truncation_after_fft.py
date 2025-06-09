
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

time_1,vin_values_1 = sine_curve(f1,sampling_rate,duration,0)
time_2,vin_values_2 = sine_curve(f2,sampling_rate,duration,90)

# plt.plot(time_2,vin_values_2)
# plt.show()
# sample and hold
adc_time_1,adc_signal_1 = sample(time_1,adc_sampling_rate,vin_values_1) 
adc_time_2,adc_signal_2 = sample(time_2,adc_sampling_rate,vin_values_2)

#passing adc
digital_values_1 = [adc(vin,adc_bits,v_ref) for vin in adc_signal_1] 
digital_values_2 = [adc(vin,adc_bits,v_ref) for vin in adc_signal_2] 

# removing dc offset
digital_values_no_offset_1 = np.array(digital_values_1) - (2**(adc_bits-1))
digital_values_no_offset_1 = (digital_values_no_offset_1).astype(int)
digital_values_no_offset_2 = np.array(digital_values_2) - (2**(adc_bits-1))
digital_values_no_offset_2 = (digital_values_no_offset_2).astype(int)
 
w_signal_1,gain_bits = window_bits(adc_time_1,w_bit)
w_signal_2,gain_bits = window_bits(adc_time_2,w_bit)

windowed_30_1 = digital_values_no_offset_1 * w_signal_1
windowed_30_2 = digital_values_no_offset_2 * w_signal_2 # windowing signal
eps = 1e-12 # to avoid log(0)

# plt.plot(adc_time_1,windowed_30_1)
# plt.show()

# truncate to 12 bit
windowed_truncate_1 = truncate(truncate_bit,windowed_30_1)
windowed_truncate_2 = truncate(truncate_bit,windowed_30_2)

# fft
freq_1,re_part_1,im_part_1 = fft_complex(M,N,P,windowed_truncate_1,adc_sampling_rate,gain_bits)
freq_2,re_part_2,im_part_2 = fft_complex(M,N,P,windowed_truncate_2,adc_sampling_rate,gain_bits)

#converting to int
re_part_int_1 = (np.round(re_part_1)).astype(np.int64)
im_part_int_1 = (np.round(im_part_1)).astype(np.int64)
re_part_int_2 = (np.round(re_part_2)).astype(np.int64)
im_part_int_2 = (np.round(im_part_2)).astype(np.int64)

index_signal_1 = np.array(im_part_int_1).argmax()
index_signal_2 = np.array(im_part_int_2).argmax()
print("max re (signed 32-bit):", format((re_part_int_1[index_signal_1]) & 0xFFFFFFFF, '#034b'))
print("max im (signed 32-bit):", format((im_part_int_1[index_signal_1]) & 0xFFFFFFFF, '#034b'))
print("max re (signed 32-bit):", format((re_part_int_2[index_signal_2]) & 0xFFFFFFFF, '#034b'))
print("max im (signed 32-bit):", format((im_part_int_2[index_signal_2]) & 0xFFFFFFFF, '#034b'))

# from observed values truncating to 24 bits seems to retain fft properties therefore shaving from MSB till 24 bits
# also rounding to 18 bits to keep withing DSP 48 slice
