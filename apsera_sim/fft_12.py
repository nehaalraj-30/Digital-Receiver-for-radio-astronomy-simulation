import numpy as np

#fft divided into N points(rows) and M coloumns
def fft(M,N,P,w_signal,sampling_rate,gain):
    U = np.zeros((M, N), dtype=complex)
    for m in range(M):
        for n in range(N):
            U[m, n] = w_signal[m + n * M] #formula for formatting x[n] , n controls positon within block
            # m controls which block 

    U = np.fft.fft(U, axis=1) # fft on one block
    
    # arrange a row of M , (1,-1)-> -1 fill row automatically, 1 -> arrange in row
    n = np.arange(N).reshape(1, -1)
    
    # arrange a row of M, (-1,1) -1 -> fill coloumn automatically 1 -> arrange in row
    m = np.arange(M).reshape(-1, 1) 
    
    twiddles = np.exp(-2j * np.pi * m * n / P) 
    U = U * twiddles ## corrects phase

    U = np.fft.fft(U, axis=0) #fft along coloumn
    y = U.flatten() #2d -> 1d

    freqs = np.fft.fftfreq(P, d=1/sampling_rate) #freq bins for fft lenght of P, d = sample spacing
    
    y_shifted = np.fft.fftshift(y) # shifts 0 freq to centre
    freqs_shifted = np.fft.fftshift(freqs)
    mag_shifted = np.abs(y_shifted) / (P*gain) #normalize
    
    return freqs_shifted,mag_shifted