''' IN5450 Mandatory exercise 3
Thomas Aussaguès, 05/04/2022
thomas.aussagues@imt-atlantique.net

This script contains a function to do pulse compression.'''

import numpy as np

def run_pulse_compression(ping : np.array, echo : np.array) -> np.array:

    '''This function returns a pulse compressed version of the input ping echo 
    using 'ping' as reference.
    
    Inputs:
    - ping: np.array (dtype = 'complex'), array of the transmitted signal
    - echo: np.array (dtype = 'complex'), array of the received echo
    
    Output:
    - pulse_compressed_signal: np.array (dtype = 'complex'), array of the pulse compressed singal'''

    '''We run the match filter in the time domain using numpy's correlate function.'''
    pulse_compressed_signal = np.correlate(echo, ping, mode = 'same')
    '''Normalization step: we normalize the cross-correlation by the product of the ping and the echo norms.'''
    pulse_compressed_signal /= (np.linalg.norm(ping) * np.linalg.norm(echo))
    
    '''We return the normalized cross-correlation'''

    return pulse_compressed_signal