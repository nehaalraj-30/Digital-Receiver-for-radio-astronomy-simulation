import matplotlib.pyplot as plt
import numpy as np
from sine_input import sine_curve
from adc import sample,adc
from window import window_bits,window_precision
from fft_return_complex import fft_complex
from truncating import truncate

M = 16
N = 1024
P = M*N
alpha = 1
n_bits = [8,10,12,14,16,18,20,22,24]
truncate_bit = 12
adc_bits = 12
w_bit = 18
v_ref = 0.7096 # to keep output power that is adc at 1dBm of input 
f = 5e8
sampling_rate = 1e12 # for producing sine wave
adc_sampling_rate = 4e9
fft_points = 16*2**10

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

# normalising signal to regular sine wave for right fft amplitude 
# digital_values_no_offset = np.array((digital_values_no_offset)*1)/2**(0) 

plt.step(adc_time,digital_values_no_offset)
plt.grid(True)
plt.show()

w_signal,gain_bits = window_bits(adc_time,w_bit)
windowed_30 = digital_values_no_offset * w_signal # windowing signal
eps = 1e-12 # to avoid log(0)

plt.plot(adc_time,windowed_30)
plt.show()
print(np.max(windowed_30))
# plt.plot(adc_time,w_signal)
# plt.show()
#fft for truncated signal 
windowed_truncate = truncate(truncate_bit,windowed_30)
freq,re_part,im_part = fft_complex(M,N,P,windowed_truncate,adc_sampling_rate,gain_bits)




print(np.max(windowed_truncate))
re_part_int = (np.round(re_part)).astype(np.int64)
im_part_int = (np.round(im_part)).astype(np.int64)
plt.plot(freq,im_part_int)
plt.grid(True)
plt.show()

plt.plot(freq,re_part_int)
plt.grid(True)
plt.show()
# /im_part=np.round(im_part)
# re_part=np.round(re_part)
# plt.subplot(1,2,1)
# plt.plot(freq,re_part)
# plt.subplot(1,2,2)
# plt.plot(freq,im_part)
# plt.show()
index_signal = np.array(im_part_int).argmax()
print("max re (signed 32-bit):", format((re_part_int[index_signal]) & 0xFFFFFFFF, '#034b'))
print("max im (signed 32-bit):", format((im_part_int[index_signal]) & 0xFFFFFFFF, '#034b'))

for i in range(8000,8031):
    print(format(abs(re_part_int[i]) & 0xFFFFFFFF, '#034b'))
# from observed values truncating to 14 bits seems to retain fft properties


# im_part_scaled = im_part
# im_part_scaled = np.round(im_part_scaled).astype(int)
# index_signal_im = np.array(im_part_scaled).argmax()
# print(index_signal_im,)
# binary_im_part = bin(im_part_scaled[index_signal_im] )
# print(im_part_scaled[index_signal_im])
# print(binary_im_part)

# im_partNoise_scaled = im_part
# im_partNoise_scaled = np.round(im_partNoise_scaled).astype(int)
# index_signal_imNoise = 808
# max=0
# for i in range(index_signal_imNoise,index_signal_imNoise+50):
#     if abs(im_partNoise_scaled[i])>=max:
#         max=abs(im_partNoise_scaled[i])
#     print(format(abs(im_partNoise_scaled[i]), '#029b'))
#     # print(bin(abs(im_partNoise_scaled[i])))
# print("max is", max)    
# binary_im_partNoise = bin(im_partNoise_scaled[index_signal_imNoise] )
# print(im_partNoise_scaled[index_signal_imNoise:830])
# print(binary_im_partNoise)


# re_part_scaled = re_part
# re_part_scaled = np.round(re_part_scaled).astype(int)
# index_signal = np.array(re_part_scaled).argmax()
# binary_re_part = bin(re_part_scaled[index_signal] )
# print(re_part_scaled[index_signal])
# print(binary_re_part)

# max_val = np.max(np.abs(im_part))  # or full FFT output
# growth_bits = np.ceil(1.5*np.log2(max_val))
# print(f"Measured bit growth: {int(growth_bits)} bits")
# re_part_trunc = {}
# imag_part_trunc = {}
# diff_real = {}
# diff_imag = {}
# diff_imag_db= {}
# diff_real_db = {}
# diff_mean={}
# im_mean={}

# plt.figure(figsize = (12,6))

# eps = 1e-12

# for bit in n_bits[::-1]:
#     imag_part_trunc[bit] = truncate_fft(bit,im_part)
#     diff_imag[bit]= imag_part_trunc[bit] - im_part
#     # print(diff_imag[bit][8000:8100])
#     im_mean[bit] = 20*np.log10(np.mean(np.abs(diff_imag[bit]))+eps) 
#     diff_imag_db[bit] = 20*np.log10(np.abs(diff_imag[bit])/np.max(np.abs(im_part))+eps)
#     plt.plot(freq,diff_imag_db[bit],label = f'{bit}-bit truncated error from initial estimated growth of 20')

# plt.title('error in fft amplitude after truncating')
# plt.xlabel('freq')
# plt.ylabel("Im_diff")   
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show() 
# plt.close()

# bit_vals = list(im_mean.keys())
# mean_errors_db = list(im_mean.values())

# plt.figure(figsize=(12,6))
# plt.plot(bit_vals,mean_errors_db,label = f'{bit}-bit mean error with 30 bit')
# plt.title('im error in db scale (mean)')
# plt.xlabel('bits')
# plt.ylabel("error in db")   
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# # plt.savefig("fft_error_mean_8-16b.png")
# plt.show() 
# plt.close()

# plt.figure(figsize = (12,6)) 
# for bit in n_bits[::-1]:
#     re_part_trunc[bit] = truncate_fft(bit,re_part)    
#     diff_real[bit] = re_part_trunc[bit] - re_part    
#     diff_real_db[bit] = 20*np.log10(np.abs(diff_real[bit])/np.max(np.abs(re_part))+eps)
#     diff_mean[bit] = 20*np.log10(np.mean(np.abs(diff_real[bit]))+eps)    
#     plt.plot(freq,diff_real_db[bit],label = f'{bit}-bit truncated error from initial estimated growth of 20')    

# # for bit in n_bits:
# #     err = np.max(np.abs(diff_imag[bit]))
# #     print(f"Max imag error at {bit} bits: {err}")

# plt.title('error in fft amplitude after truncating')
# plt.xlabel('freq')
# plt.ylabel("Re_diff")   
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show() 
# plt.close()

# bit_vals = list(diff_mean.keys())
# mean_errors_db = list(diff_mean.values())

# plt.figure(figsize=(12,6))
# plt.plot(bit_vals,mean_errors_db,label = f'{bit}-bit mean error with 30 bit')
# plt.title('re error in db scale (mean)')
# plt.xlabel('bits')
# plt.ylabel("error in db")   
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# # plt.savefig("fft_error_mean_8-16b.png")
# plt.show() 
# plt.close()

# # plt.figure(figsize=(12,6))
# # plt.plot(adc_time,digital_values_no_offset)
# # plt.title('input')
# # plt.xlabel('t')
# # plt.ylabel("dec")   
# # plt.grid(True)
# # plt.tight_layout()
# # plt.show() 
# # plt.close()

# # plt.figure(figsize=(12,6))
# # plt.plot(freq,re_part,label = "Real")
# # plt.title('RE')
# # plt.xlabel('freq')
# # plt.ylabel("RE")   
# # plt.grid(True)
# # plt.tight_layout()
# # plt.show() 
# # plt.close()

# # plt.plot(freq,im_part,label = "imaginary")
# # plt.title('Imag')
# # plt.xlabel('freq')
# # plt.ylabel("Imag")   
# # plt.grid(True)
# # plt.tight_layout()
# # plt.show() 
# # plt.close()



