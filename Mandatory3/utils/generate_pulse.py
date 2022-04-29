''' IN5450 Mandatory exercise 3
Thomas Aussaguès, 05/04/2022
thomas.aussagues@imt-atlantique.net

This script contains a function to generate LFM pulses. 
'''

import numpy as np


def lfm_pulse(B: float, f_c: float,T_p: float, fs: float) -> np.array :
    
    '''This function computes and returns int(f_s*T_p) samples of a Linear Frequency Modulated (LFM).
    Note that if you want an UP LFM pulse, you need to use a positive bandwidth B. For a DOWN LFM pulse, 
    use a negative one.

    Inputs:
    - B     : float, bandwidth in Hertz (Hz)
    - f_c   : float, pulse central frequency in Hertz (Hz)
    - T_p   : float, pulse length in seconds (s)
    - f_s   : float, pulse sampling frequency in Hertz (Hz) 

    Output:
    - pulse : np.array (dtyp = 'complex'), LFM pulse
    '''
    
    '''First, we compute the chirp rate alpha (in 1/s^2) definded as the bandwidth divided by the pulse length
    alpha = B/T_p.'''
    alpha = B / T_p

    '''Then, we create a time np.array from t = 0 s to t = T_p with a time sampling interval of 1/fs which corresponds
    to a total number of points of int(Tp * fs).'''
    time = np.linspace(0, T_p, int(T_p * fs))

    '''We allocate space for the pulse array. Note that this array must be a complex array!'''
    pulse = np.zeros((int(T_p * fs) + 1), dtype= 'complex')
    
    '''Finally, we compute the pulse using the LFM pulse formula:
    pulse[k] = exp(2j * pi * ( (fc - B / 2) * t + alpha * t ** 2 / 2) )'''
    pulse = np.exp(2 * 1j * np.pi * ((f_c - B/2) * time + alpha * time ** 2 / 2))

    '''We return the pulse array.'''

    return pulse
