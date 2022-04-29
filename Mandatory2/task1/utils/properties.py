# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

# This script contains functions to compute/estimate the power estimate properties (resolution, min power level)

import numpy as np
import scipy.signal

def estimate_DOA(DOA_array:np.array,power_estimate:np.array,Ns:int)->np.array:

    # This function computes the ML 3dB widths and the min power level
    # Inputs:
    # DOA_array: np.array, array containing the angles for which we estimated the power
    # power_estimate: np.array, power estimate
    # Ns: int, number of sources
    # Output:
    # props: dict

    # We create a dict props containing the power estimate properties
    props = dict()
    # If there are multiple targets, then we have multiple 3dB widths
    props['ML_3dB_width'] = list()
    # We get the power estimate maximums
    peaks,_ = scipy.signal.find_peaks(power_estimate)
    # We sort the peaks index (descending order) and we keep only the first Ns maximums
    peaks = np.flip(peaks[np.argsort(power_estimate[peaks])])[:Ns]
    # We get the angles corresponding to these first NS maximums
    props['estimated_DOA'] = np.sort(DOA_array[peaks])
    
    # For each source (=each peak), we compute the ML_3dB width
    for peak_index in peaks:

        # We get the ML position
        estimated_DOA = DOA_array[peak_index]
        # And its value
        peak_value = power_estimate[peak_index]
        # We initialize both the left and right -3dB DOA
        ML_3dB_width_right = None
        ML_3dB_width_left = None

        index = peak_index
        # We compute the left -3dB width
        while power_estimate[index] > peak_value - 3:
            index += 1
            ML_3dB_width_right = DOA_array[index]

        index = peak_index
        # We compute the right -3dB width
        while power_estimate[index] > peak_value - 3:
            index -= 1
            ML_3dB_width_left = DOA_array[index]
        # We add the mean of these two values to the dict
        props['ML_3dB_width'].append((np.abs(ML_3dB_width_left-estimated_DOA)+np.abs(ML_3dB_width_right-estimated_DOA))/2)

        
    # We get the min level
    props['min_level'] = np.min(power_estimate)
    # We return the props dict
    
    return props