''' IN5450 Mandatory exercise 3
Thomas Aussaguès, 05/04/2022
thomas.aussagues@imt-atlantique.net

This script contains functions to do FOURIER analysis and especially to compute:
- the periodogram,
- the modified periodogram
- the Short Time Fourier Transform STFT. 
'''

import numpy as np
import scipy.signal


def periodogram(data : np.array, zero_padding_factor = 1) -> np.array :

    '''This function computes and returns the standard periodogram of a given np.array.
    The standard zero padding factor is equal to 1.
    
    Inputs:
    - data: np.array, time series for which we want to compute the periodogram
    - zero_padding_factor: int, optional, zero padding factor (default value: 1)
    
    Output:
    - (periodogram), np.array, periodogram of the data np.array'''
    
    ''' We get the length of the input sequence.'''
    N = len(data)

    ''' We compute the FOURIER transform using python's FFT implementation
    Then, we re-arrange the computed sequence such that negative frequency are on the left,
    and positive ones on the right. '''
    fft = np.fft.fftshift(np.fft.fft(a = data, n = N * zero_padding_factor))

    '''We divide the estimate by the the length of the input sequence and we return it.'''

    return 1 / N * np.abs(fft) ** 2


def modified_periodogram(data : np.array, zero_padding_factor = 1):

    '''This function computes and returns the modified periodogram of a given np.array using 
    a KAISER window with beta = 4. The standard zero padding factor is equal to 1.
    
    Inputs:
    - data: np.array, time series for which we want to compute the modified periodogram
    - zero_padding_factor: int, optional, zero padding factor (default value: 1)
    
    Output:
    - (modified periodogram), np.array, modified periodogram of the data np.array'''
    
    ''' We get the length of the input sequence.'''
    N = len(data)

    '''Here, we use a KAISER window (beta=4).'''
    window = scipy.signal.windows.kaiser(N, beta = 4, sym = True)

    '''We apply the window to the input sequence by mulypling.'''
    new_data = window * data

    '''We compute the L2 norm of the window.'''
    U = 1 / N * np.sum(np.abs(window) ** 2)

    '''We divide the estimate by U and we return the modified periodogram.'''

    return 1/U*periodogram(new_data, zero_padding_factor)

def sfft(data : np.array, L : int, D : int, fs : float, zero_padding_factor = 1):

    '''This function computes and returns the modified periodogram of a given np.array using 
    a KAISER window with beta = 4. The standard zero padding factor is equal to 1.
    
    Inputs:
    - data: np.array, time series for which we want to compute the modified periodogram
    - L: int, segment length
    - D: int, overlap
    - fs: float, sampling frequency
    - zero_padding_factor: int, optional, zero padding factor (default value: 1)
    
    Output:
    - time: np.array, time vector (from t = 0 to t = N/fs where fs is the sampling frequency 
    and N the number of point in data)
    - frequency: np.array, frequency array 
    - modified_periodograms, np.array, contains the periodogram for each time interval <=> contains the 
    STFT'''
    
    '''We get the length of the input sequence.'''
    N = len(data)

    '''We compute the number of segments of length L with an overlap of D.'''
    K = int((N - L) / D + 1)

    '''We divide the input sequence into K segements of length L with an overlap of D.'''
    segments = np.array([data[k*D : k*D+L] for k in range(K)])

    '''We compute the modified periodogram of each segment which have previously zero-padded.'''
    modified_periodograms = np.array([modified_periodogram(data = segment, zero_padding_factor = zero_padding_factor) for segment in segments])
    
    '''We get the obtained matrix shape.'''
    N_t, N_f = modified_periodograms.shape
    '''We generate the time vector'''
    time = np.linspace(0, N / fs, K)
 
    '''We generate the frequency vector. We need to apply the fftshift function because data is complex.'''
    freq = np.fft.fftshift(np.fft.fftfreq(N_f, 1 / fs))
    
    '''We return the time and frequency vectors and the transposed matrix 
    (time on the x-axis and frequency on the y-axis).'''
    
    return time, freq, modified_periodograms.T