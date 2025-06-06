import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
from sine_input import sine_curve
from adc import sample,adc
from window import window_bits_normalised,window_precision
from fft_12 import fft
from truncating import truncate_normalised

M = 16
N = 1024
P = M*N
alpha = 1
n_bits = [8,10,12,14,16]
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
digital_values_no_offset = digital_values - np.mean(digital_values)  

# normalising signal to regular sine wave for right fft amplitude 
digital_values_no_offset = np.array((digital_values_no_offset)*2)/2**(adc_bits) 

w_signal,gain_bits = window_bits_normalised(adc_time,w_bit)
w_signal_fp,gain_fp = window_precision(adc_time)
windowed_fp = digital_values_no_offset * w_signal_fp # windowing fp
windowed_30 = digital_values_no_offset * w_signal # windowing signal

#fft of 64 bit
freq_fp = np.fft.fftfreq(fft_points, d = 1/adc_sampling_rate)[:fft_points]
freq_fp_shift = np.fft.fftshift(freq_fp)
y_fp = np.fft.fft(windowed_fp,n=fft_points)
y_fp_shift = np.fft.fftshift(y_fp)
mags_fp_shift = np.abs(y_fp_shift)/(P*gain_fp)
eps = 1e-12 # adding to avoid 0
mags_db = 20*np.log10(mags_fp_shift/(np.max(mags_fp_shift)+eps))
plt.figure(figsize=(12,6))
plt.plot(freq_fp_shift, mags_db, label='full precision fft')

#fft of 30 bit (adc_bit = 12 window_bit_precision = 18(arch of dsp_slice on red pitaya))
freq_30 = np.fft.fftfreq(fft_points, d = 1/adc_sampling_rate)[:fft_points]
freq_30_shift = np.fft.fftshift(freq_30)
y_30 = np.fft.fft(windowed_30,n=fft_points)
y_30_shift = np.fft.fftshift(y_30)
mags_30_shift = np.abs(y_30_shift)/(P*gain_bits)
mags_db_30 = 20*np.log10(mags_30_shift/(np.max(mags_30_shift)+eps))
plt.plot(freq_30_shift, mags_db_30, label='30 bit fft')

diff = {} # intialize dictionaries to graph , each diff[bit] = list for key bit
diff_mean={}

#fft for truncated signal 
for bit in n_bits:
    windowed_truncate = truncate_normalised(bit,windowed_30)
    freq_truncated,mags_truncated = fft(M,N,P,windowed_truncate,adc_sampling_rate,gain=1)
    mags_trunc_db = 20*np.log10(mags_truncated/(np.max(mags_truncated)+eps))
    diff_linear = np.abs(mags_truncated-mags_30_shift)
    diff[bit] = 20*np.log10(diff_linear+eps)
    diff_mean[bit] = 20*np.log10(np.mean(diff_linear)+eps)
    plt.plot(freq_truncated, mags_trunc_db, label=f'{bit}-bit Truncated FFT' )

plt.title("30 and n_bits fft ")
plt.xlabel("Frequency (Hz)")
plt.ylabel("|X(f)| in db")
plt.xlim(-4000e6, 4000e6)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("fft_main_8-16b.png")
plt.show()
plt.close()

plt.figure(figsize=(12,6))
for bit in n_bits:
    plt.plot(freq_truncated,diff[bit],label = f'{bit}-bit error with 30 bit')
plt.title('error in db scale_8-16b')
plt.xlabel('frequency (hz)')
plt.ylabel("error in db")   
plt.xlim(-4000e6, 4000e6)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("fft_error_8-16b.png") 
plt.show()
plt.close()

bit_vals = list(diff_mean.keys())
mean_errors_db = list(diff_mean.values())

plt.figure(figsize=(12,6))
plt.plot(bit_vals,mean_errors_db,label = f'{bit}-bit mean error with 30 bit')
plt.title('error in db scale (mean)')
plt.xlabel('bits')
plt.ylabel("error in db")   
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("fft_error_mean_8-16b.png") 
plt.show()
plt.close()

# from graph we can conclude 10 bit or 12 bit is sufficient truncation as error beyond 12 bit 
# is not reducing by much


