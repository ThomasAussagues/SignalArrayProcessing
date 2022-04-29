# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

# This script contains function to estimate the spectrum using the MUSIC algorithm

import numpy as np
from utils.general_functions import get_steering_vector
from configuration import get_general_config

def estimate_music_power(R:np.array,a:np.array,Ns:int):

    # This function estimate the power using the MUSIC method given a correlation matrix, a steering vector and 
    # the number of sources Ns
    # Inputs:
    # R: np.array, spatial correlation matrix
    # a: np.array, steering vector
    # Ns: int, number of sources
    # Outputs:
    # float, power estimate

    # First, we make an eigendecomposition of the spatial correlation matrix R.

    eigenvalues,eigenvectors = np.linalg.eig(R)

    # Again, the eigenvalues which should real (according to the spectral theorem) contain a small (e-17) imaginiary part.
    # We drop this part by selecting the real part.

    eigenvalues = np.real(eigenvalues)
    
    # We sort the eigenvectors according to their asscoiated eigenvalues.
    # np.sort sorts the array in ascending order. We use np.flip to reverse the order.
    eigenvectors = eigenvectors[:,np.flip(np.argsort(eigenvalues))]

    # We only select the M-Ns eigenvectors associated to the smallest eigenvalues
    eigenvectors = eigenvectors [:,Ns:]
    # Warning!!! Here, the we get rid of the extremly small imaginary part (e-17...) of the power estimate !
    # We use float to return a floar type and not an np.array

    # If we do spatial smoothing, the smoothed spatial correlation matrix will be (M-L+1)x(M-L+1) where L is the 
    # subarrays size and M the full array size. To be able to perform the matrix product, we get rid of the L-1 last
    # elements of the steering vector
    if R.shape[0] != a.shape[0]:
        #print('Shapes do not match... We drop the last elements of the steering vector such that shapes fit')
        a = a[:R.shape[0]]
        #print(a.shape)


    return float(np.real(1/(a.conj().T@eigenvectors@eigenvectors.conj().T@a)))


def estimate_music_spectrum(R:np.array,kd:float,M:int,Ns:int)->np.array:

    # This function computes and returns the spectrum (for angles in [-40,50] degrees) using the MUSIC method
    # Inputs:
    # R: np.array, spatial correlation matrix
    # kd: float, product of the wavenumber k with the element distance d
    # M: int, number of sensors
    # Ns: int, number of sources
    # Output:
    # np.array, angular spectrum

    # This function estimates the spectrum using the MUSIC algorithm
    # music_spectrum : list storing the power estimates for different DOA values
    music_spectrum = list()
    # For each value of the DOA, we compute the steering vector and the associated power estimate.
    # And we add it to the list music_spectrum
    for DOA in get_general_config()['DOA_array']:
        # We compute the steering vector
        a = get_steering_vector(DOA=DOA,kd=kd,M=M)
        # We compute the power estimate and we add it to the list minimum_variance_spectrum
        music_spectrum.append(estimate_music_power(R,a,Ns))

    # We return the music_spectrum list as an numpy array

    return np.array(music_spectrum)