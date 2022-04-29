# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

# This script contains functions to generate all the data and to compute the steering vector

import sys
import os
sys.path.append(os.getcwd()+'/utils')
import numpy as np
import scipy.io 
from generate_data import generate_data
from configuration import get_config_1,get_config_2,get_config_SNR_analysis



def get_steering_vector(DOA:float,kd:float,M:int)->np.array:

    # This function computes the steering vector for a ULA
    # Inputs
    # DOA : direction of arrival in degrees
    # M : number of sensors 
    # Output: np.array, steering vector
    
    # Phi = phase shift between two consecutive sensors (for the given array geometry)
    phi = -kd*np.sin(DOA*np.pi/180)
    # We return the steering vector: here np.newaxis is used to obtain a resulting vector with shape (M,1) and not (M,)

    return np.power(np.exp(-1j*phi),np.arange(0,M)[:,np.newaxis])

def from_matlab_to_python(matlab_file_name:str,numpy_file_name:str)->None:

    # This function takes MATLAB signals vectors and saves it as a numpy object
    # The MATLAB file (.mat) must be in the folder data/matlab 
    # Moreover, the signals vector must be called 'x' in matlab

    # Inputs:
    # matlab_file_name: str, name of the matlab file
    # numpy_file_name: str, name of the python file (should data_incoherent or data_coherent)
    # Output:
    # None

    # We load the matlab signals vector
    x = scipy.io.loadmat('data/matlab/' + matlab_file_name)['x']
    # We save it as a numpy object
    np.save('data/matlab/' + numpy_file_name,x)

    return None

def generate_all_data()->None:

    # This functions generate all data for all experiences

    # Input: None
    # Output: None

    # Question 1->7: incoherent sources
    generate_data(name='data_incoherent',config=get_config_1())
    # Question 8: coherent sources
    generate_data(name='data_coherent',config=get_config_2())
    # SNR analysis

    snr_values = np.arange(-10,10+1,1)
    for snr in snr_values:
        generate_data(name='data_coherent_{}'.format(snr),config=get_config_SNR_analysis(snr))

    return None
