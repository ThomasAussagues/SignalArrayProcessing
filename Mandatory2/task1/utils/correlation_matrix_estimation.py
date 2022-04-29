# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

# This script contains functions to compute/estimate the spatial correlation matrix


import numpy as np

def get_forward_backward_smoothed_spatial_correlation_matrix(Y:np.array,L:int)->np.array:

    # This function computes and returns the forward-backward smoothed spatial correlation matrix
    # Inputs:
    # Y: np.array, signal matrix
    # L: int, number of element in the subarrays
    # Output: 
    # forward_backward_smoothed_covariance_matrix:np.array, forward-backward smoothed spatial correlation matrix

    # We get the smoothed spatial correlation matrix
    smoothed_spatial_correlation_matrix = get_smoothed_spatial_correlation_matrix(Y=Y,L=L)
    # We compute the exchange matrix J
    J = np.fliplr(np.identity(n=smoothed_spatial_correlation_matrix.shape[0]))
    # We return the forward-backward correlation matrix

    return 1/2*(smoothed_spatial_correlation_matrix+J@smoothed_spatial_correlation_matrix.conj()@J)

def get_smoothed_forward_backward_spatial_correlation_matrix(Y:np.array,L:int)->np.array:

    # This function computes and returns the forward-backward smoothed spatial correlation matrix
    # Inputs:
    # Y: np.array, signal matrix
    # L: int, number of element in the subarrays
    # Output: 
    # forward_backward_smoothed_covariance_matrix:np.array, forward-backward smoothed spatial correlation matrix

    # We get the forward-backward spatial correlation matrix
    forward_backward_correlation_matrix = get_forward_backward_correlation_matrix(Y=Y)
    M = forward_backward_correlation_matrix.shape[0]
    # We return the forward-backward correlation matrix

    smoothed_forward_backward_spatial_correlation_matrix = np.zeros((L,L),dtype='complex')
    for k in range(M-L):
        smoothed_forward_backward_spatial_correlation_matrix += forward_backward_correlation_matrix[k:k+L,k:k+L]

    return 1/(M-L+1)*smoothed_forward_backward_spatial_correlation_matrix


def get_forward_backward_correlation_matrix(Y:np.array)->np.array:

    # This function computes and returns the forward-backward correlation matrix
    # Inputs:
    # Y: np.array, signal vector
    # Output:
    # np.array, spatial correlation matrix

    R = get_standard_correlation_matrix_estimation(Y=Y)
    # We compute the exchange matrix J
    J = np.fliplr(np.identity(n=R.shape[0]))
    # We return the forward-backward correlation matrix
    
    return 1/2*(R+J@R.conj()@J)

def get_smoothed_spatial_correlation_matrix(Y:np.array,L:int)->np.array:

    # This function computes and returns the smoothed spatial correlation matrix
    # Inputs:
    # Y: np.array, signal matrix
    # L: int, number of element in the subarrays
    # Output: 
    # smoothed_covariance_matrix:np.array, smoothed spatial correlation matrix

    # We get the standard correlation matrix estimate
    R = get_standard_correlation_matrix_estimation(Y=Y)
    # We get the shape of M
    M = R.shape[0]
    # We compute the standard correlation matrix
    R = get_standard_correlation_matrix_estimation(Y)
    smoothed_covariance_matrix = np.zeros((L,L),dtype='complex')
    for k in range(M-L):
        smoothed_covariance_matrix += R[k:k+L,k:k+L]

    return 1/(M-L+1)*smoothed_covariance_matrix

def get_standard_correlation_matrix_estimation(Y:np.array)->np.array:

    # This function computes and returns the standard correlation matrix estimate
    # Inputs:
    # Y: np.array, signal matrix
    # Output:
    # R: np.array, spatial correlation matrix

    # We compute the spatial auto correlation matrix R
    R = Y@Y.conj().T/Y.shape[1]
    # We return it

    return R


def get_rotary_averaged_spatial_correlation_matrix(Y:np.array)->np.array:

    # This function computes and returns the rotary averaged spatial correlation matrix estimate
    # Inputs:
    # Y: np.array, signal matrix
    # Output:
    # R_ra: np.array, rotary averaged spatial correlation matrix

    # We compute the spatial auto correlation matrix R
    R = Y@Y.conj().T/Y.shape[1]
    # We compute the exchange matrix J
    J = np.fliplr(np.identity(n=R.shape[0]))
    # We compute the rotary averaged spatial correlation matrix
    R_ra = 1/4 * (R+J@R.T+J@R@J+R@J)
    # We return it

    return R_ra

def diagonal_loading(R:np.array,delta:float):

    # This function computes and returns the diagonaly reduced spatial correlation matrix
    # Inputs:
    # R: np.array, spatial correlation matrix
    # Output:
    # R -delta*I_M: np.array, the diagonaly reduced spatial correlation matrix
    return R - delta * np.identity(R.shape[0])



