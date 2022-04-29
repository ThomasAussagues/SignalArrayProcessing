# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

# This script contains function to estimate the spectrum using the MUSIC algorithm

import numpy as np
from utils.general_functions import get_steering_vector
from configuration import get_general_config

def DAS_power_estimate(R:np.array,a:np.array)->float:

    # This function computes the power estimate (using a full R estimate)
    # Inputs:
    # R: np.array, spatial correaltion matrix
    # a: np.array, steering vector
    # Output:
    # float, power estimate

    # @ is the matrix multiplication in numpy
    # We return a^H@R@a/M as a floar (if we do not use complex(.), the function returns a numpy.ndarray...)
    # Warning!!! Here, the we get rid of the extremly small imaginary part (e-17...) of the power estimate !

    # If we do spatial smoothing, the smoothed spatial correlation matrix will be (M-L+1)x(M-L+1) where L is the 
    # subarrays size and M the full array size. To be able to perform the matrix product, we get rid of the L-1 last
    # elements of the steering vector
    if R.shape[0] != a.shape[0]:
        #print('Shapes do not match... We drop the last elements of the steering vector such that shapes fit')
        a = a[:R.shape[0]]
        #print(a.shape)
   
    return float(np.abs(a.conj().T@R@a/a.shape[0]))

def estimate_classical_spectrum(R:np.array,kd:float,M:int)->np.array:

    # This function computes and returns the spectrum (for angles in [-40,50] degrees) using the standard DAS method
    # Inputs:
    # R: np.array, spatial correlation matrix
    # kd: float, product of the wavenumber k with the element distance d
    # M: int, number of sensors
    # Output:
    # np.array, angular spectrum

    # This function estimates the spectrum using the classical way
    # classical_spectrum : list storing the power estimates for different DOA values
    classical_spectrum = list()
    # For each value of the DOA, we compute the steering vector and the associated power estimate.
    # And we add it to the list classical_spectrum
    for DOA in get_general_config()['DOA_array']:
        # We compute the steering vector
        a = get_steering_vector(DOA=DOA,kd=kd,M=M)
        # We compute the power estimate and we add it to the list classical_spectrum
        classical_spectrum.append(DAS_power_estimate(R,a))

    # We return the classical spectrum list as an numpy array

    return np.array(classical_spectrum)