import matplotlib.pyplot as plt
import numpy as np
from sine_input import sine_curve
from adc import adc
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
sampling_rate = 4e9 # for producing sine wave
adc_sampling_rate = 4e9
fft_points = 2**14
acc = 64
x = 0
y = fft_points

# duration such that when sampled we get appropriate no. of points
duration = fft_points/adc_sampling_rate 
t_static = np.linspace(0, duration, fft_points, endpoint=False)

#generating window once
w_signal_1,gain_bits = window_bits(t_static,w_bit)
w_signal_2 = w_signal_1

power_spectrum_accu_1 = [0]*(P)
power_spectrum_accu_2 = [0]*(P)

cross_corr_combined_acc = np.zeros(P, dtype=complex)

for i in range(0,acc):
    
    # taking ith 16k chunk at 4Ghz
    time_1,sine_1 = sine_curve(f1,sampling_rate,duration,0,i)
    time_2,sine_2 = sine_curve(f2,sampling_rate,duration,90,i)
    
    adc_time_1 = time_1
    adc_time_2 = time_2
    adc_signal_1 = sine_1
    adc_signal_2 = sine_2

    #passing adc
    digital_values_1 = [adc(vin,adc_bits,v_ref) for vin in adc_signal_1] 
    digital_values_2 = [adc(vin,adc_bits,v_ref) for vin in adc_signal_2] 

    # removing dc offset
    digital_values_no_offset_1 = np.array(digital_values_1) - (2**(adc_bits-1))
    digital_values_no_offset_1 = (digital_values_no_offset_1).astype(int)
    digital_values_no_offset_2 = np.array(digital_values_2) - (2**(adc_bits-1))
    digital_values_no_offset_2 = (digital_values_no_offset_2).astype(int)

    # windowing signal
    windowed_30_1 = digital_values_no_offset_1 * w_signal_1
    windowed_30_2 = digital_values_no_offset_2 * w_signal_2
    eps = 1e-12 # to avoid log(0)

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

    # from observed values truncating to 24 bits seems to retain fft properties therefore shaving from MSB till 24 bits
    # also rounding to 18 bits to keep withing DSP 48 slice
    re_part_trunc_1,im_part_trunc_1 = truncate_after_fft(re_part_int_1,im_part_int_1,fft_points)
    re_part_trunc_2,im_part_trunc_2 = truncate_after_fft(re_part_int_2,im_part_int_2,fft_points)

    # getting power spectrum through auto correlation for signal 1
    sq_real_1 = np.square(re_part_trunc_1)
    sq_im_1 = np.square(im_part_trunc_1)
    power_spectrum_1 = (np.array(sq_real_1)+np.array(sq_im_1))

    # getting power spectrum through auto correlation for signal 2
    sq_real_2 = np.square(re_part_trunc_2)
    sq_im_2 = np.square(im_part_trunc_2)
    power_spectrum_2 = (np.array(sq_real_2)+np.array(sq_im_2))

    # accumalation
    power_spectrum_accu_1 += power_spectrum_1 
    power_spectrum_accu_2 += power_spectrum_2 
    
    cross_corr_re = []
    cross_corr_im = []
    
    #convert to ordered list
    for a, b, x, y in zip(re_part_trunc_1, im_part_trunc_1, re_part_trunc_2, im_part_trunc_2): 
        # (a + ib)(x - iy) = (ax + by) + i(bx - ay)
        cross_corr_re.append(a*x + b*y)
        cross_corr_im.append(b*x - a*y)
    
    #make complex list    
    cross_corr_combined = (np.array(cross_corr_re) + 1j*(np.array(cross_corr_im)))
    
    #accumalate
    cross_corr_combined_acc += cross_corr_combined 
    
    #shifting chunk
    x = y
    y = y+fft_points

cross_corr_mag = np.abs(cross_corr_combined_acc)
cross_corr_phase = np.angle(cross_corr_combined_acc,deg=False)
    
plt.figure(figsize=(10,4))
plt.plot(freq_1,cross_corr_mag)
plt.xlim(0,2000e6)
plt.title("power_spectrum_mag and  cross accumalation of FFT Output Signal")
plt.xlabel("freq")
plt.ylabel("cross_corr_power_acc")
plt.grid(True)
plt.show()     

plt.figure(figsize=(10,4))
plt.plot(freq_1,cross_corr_phase)
plt.xlim(0,2000e6)
plt.title("power_spectrum_phase and  cross accumalation of FFT Output Signal")
plt.xlabel("freq")
plt.ylabel("cross_corr_phase_degrees")
plt.grid(True)
plt.show()  

plt.figure(figsize=(10,4))
plt.plot(freq_1,power_spectrum_accu_1)
plt.xlim(0,2000e6)
plt.title("power_spectrum_1 and accumalation of FFT Output Signal")
plt.xlabel("freq")
plt.ylabel("power_spectrum_accu_1")
plt.grid(True)
plt.show()  

plt.figure(figsize=(10,4))
plt.plot(freq_2,power_spectrum_accu_2)
plt.xlim(0,2000e6)
plt.title("power_spectrum_2 and accumalation of FFT Output Signal")
plt.xlabel("freq")
plt.ylabel("power_spectrum_accu_2")
plt.grid(True)
plt.show()     

# phase graph has some lines at non tone bin due to quantization error