# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

# This script contains function to estimate the spectrum using the minimum variance MV method

import numpy as np
from utils.general_functions import get_steering_vector
from configuration import get_general_config

def capon_beamformer(R:np.array,a:np.array)->float:

    # This function computes the minimum variance power estimate 1/(a^H@R^-1@a)
    # Inputs:
    # R: np.array, spatial correlation matrix
    # a: np.array, steering vector
    # Output:
    # float, power estimate

    # If we do spatial smoothing, the smoothed spatial correlation matrix will be (M-L+1)x(M-L+1) where L is the 
    # subarrays size and M the full array size. To be able to perform the matrix product, we get rid of the L-1 last
    # elements of the steering vector
    if R.shape[0] != a.shape[0]:
        #print('Shapes do not match... We drop the last elements of the steering vector such that shapes fit')
        a = a[:R.shape[0]]
        #print(a.shape)

    return float(np.real(1/(a.conj().T@np.linalg.inv(R)@a)))


def estimate_minimum_variance_spectrum(R:np.array,kd:float,M:int)->np.array:

    
    # This function estimates the spectrum using the Capon's method
    # Inputs:
    # R: np.array, spatial correlation matrix
    # kd: float, product of the wavenumber k with the element distance d
    # M: int, number of sensors
    # Output:
    # np.array, angular spectrum


    # minimum_variance_spectrum : list storing the power estimates for different DOA values
    minimum_variance_spectrum = list()
    # For each value of the DOA, we compute the steering vector and the associated power estimate.
    # And we add it to the list minimum_variance_spectrum
    for DOA in get_general_config()['DOA_array']:
        # We compute the steering vector
        a = get_steering_vector(DOA=DOA,kd=kd,M=M)
        # We compute the power estimate and we add it to the list minimum_variance_spectrum
        minimum_variance_spectrum.append(capon_beamformer(R=R,a=a))

    # We return the minimum_variance_spectrum list as an numpy array

    return np.array(minimum_variance_spectrum)
