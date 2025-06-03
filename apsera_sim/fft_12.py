import numpy as np

def fft(M,N,P,w_signal,sampling_rate,gain):
    U = np.zeros((M, N), dtype=complex)
    for m in range(M):
        for n in range(N):
            U[m, n] = w_signal[m + n * M]

    U = np.fft.fft(U, axis=1)

    m = np.arange(M).reshape(-1, 1)
    n = np.arange(N).reshape(1, -1)
    twiddles = np.exp(-2j * np.pi * m * n / P)
    U = U * twiddles

    U = np.fft.fft(U, axis=0)
    y = U.flatten()

    freqs = np.fft.fftfreq(P, d=1 / sampling_rate)

    # mag = np.abs(y) / P
    
    y_shifted = np.fft.fftshift(y)
    freqs_shifted = np.fft.fftshift(freqs)
    mag_shifted = np.abs(y_shifted) / (P*gain)
    
    return freqs_shifted,mag_shifted