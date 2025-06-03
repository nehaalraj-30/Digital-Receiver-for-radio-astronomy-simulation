import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

N = 1024
w = signal.windows.hann(N)
W = np.fft.fft(w, 4*N)  # Zero-padding improves frequency resolution
W = np.fft.fftshift(W) #shifts fft o/p spectrum
freqs = np.fft.fftshift(np.fft.fftfreq(4*N, d=1)) #shifts fft bins

W_db = 20 * np.log10(np.abs(W) / np.max(np.abs(W)))

plt.plot(freqs, W_db)
plt.title("FFT of Hann Window")
plt.xlabel("Normalized Frequency")
plt.ylabel("Magnitude (dB)")
plt.grid(True)
plt.ylim(-100, 0)
plt.show()
