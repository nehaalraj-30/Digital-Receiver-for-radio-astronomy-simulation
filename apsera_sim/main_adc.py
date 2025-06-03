import matplotlib.pyplot as plt
from sine_input import sine_curve
from overlap import fft
from adc import sample,adc
import numpy as np

n_bits = 12
v_ref = 3.3
f = 2e8
adc_sampling_rate = 4e9
fft_points = 16*2**10
sampling_rate=4e9


duration = fft_points/adc_sampling_rate


t,sine_sig=sine_curve(f,sampling_rate,duration,v_ref)

# time,sine_sig=sample(t,adc_sampling_rate,sine_sig)
sine_sig=((sine_sig)*2)/v_ref

sine_sig = np.array(sine_sig)*2048



plt.plot(t, sine_sig ,linestyle = 'dashed',marker='o')
plt.xlabel('t(us)')
plt.ylabel('amplitude') 
plt.title('signal')
plt.grid(True)
plt.savefig("fp_signal.png")

mags_fp,freqs_fp = fft(sine_sig)


plt.figure(figsize=(12, 6))
plt.plot(freqs_fp, mags_fp, label='Full-Precision Signal FFT')
plt.title("FFT of Full-Precision Signal (Row-Column FFT)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("|X(f)|")
plt.grid(True)
plt.savefig("fp_fft.png")

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


mags_n_bits,freqs_n_bits=fft(no_offset_dig)


plt.figure(figsize=(12, 6))
plt.plot(freqs_n_bits, mags_n_bits, label='n_bits Signal FFT')
plt.title("FFT of f'{n_bit} Signal (Row-Column FFT)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("|X(f)|")
plt.grid(True)
plt.savefig("Dig_fft.png")

diff_mag = mags_fp - mags_n_bits

plt.figure(figsize=(12, 6))
plt.plot(freqs_n_bits, diff_mag, label='n_bits Signal FFT')
plt.title("FFT of f'{n_bit} Signal (Row-Column FFT)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("|X(f)|")
plt.grid(True)
plt.savefig("fft_diff.png")

diff=[]
for x in range (0,len(no_offset_dig)):
    diff.append(digital_values[x]-sine_sig[x])

for x in range (0,5):
    print(no_offset_dig[x],sine_sig[x],no_offset_dig[x]-sine_sig[x])


plt.figure(figsize=(12, 6))
plt.plot(t, diff, label='error')
plt.title("error of f'{n_bit} Signal (Row-Column FFT)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("LSB")
plt.grid(True)
plt.savefig("sig_error.png")

