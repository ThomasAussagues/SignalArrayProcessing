# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

from distutils.command.config import config
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
from utils.standard_DAS import DAS_power_estimate, estimate_classical_spectrum
from utils.eigenvector import estimate_eigenvector_spectrum
from utils.music import estimate_music_spectrum
from utils.min_variance import estimate_minimum_variance_spectrum
from utils.correlation_matrix_estimation import get_forward_backward_correlation_matrix,get_standard_correlation_matrix_estimation,get_forward_backward_smoothed_spatial_correlation_matrix,get_smoothed_forward_backward_spatial_correlation_matrix,get_smoothed_spatial_correlation_matrix
from utils.configuration import get_config_2,get_general_config
from utils.properties import estimate_DOA
plt.rcParams.update({
  "text.usetex": True,
  'font.size': 14
})


# Normalized wavenumber * d
kd = get_config_2()['k']*get_config_2()['d']
# Number of elements M
M = get_config_2()['M']
L = get_config_2()['L']


# Question 1
# Estimate the spatial correlation matrix and plot its absolute value.

def assess_music_performances(data:str)->None:

    # Input:
    # data:str, we specify which data we want to use with the string 'data'

    # We get the array output signal X
    Y = np.load('data/' + data + '/data_coherent.npy')

    # Standard R estimate
    standard_correlation_matrix = get_standard_correlation_matrix_estimation(Y=Y)
    perf_standard_correlation_matrix = get_perf(standard_correlation_matrix)

    # Smoothed R estimate
    smoothed_spatial_correlation_matrix = get_smoothed_spatial_correlation_matrix(Y=Y,L=5)
    perf_smoothed_spatial_correlation_matrix = get_perf(smoothed_spatial_correlation_matrix)

    # Forward-backward R estimate
    forward_backward_spatial_correlation_matrix = get_forward_backward_correlation_matrix(Y=Y)
    perf_forward_backward_spatial_correlation_matrix = get_perf(forward_backward_spatial_correlation_matrix)

    # Smoothed forward-backward R estimate
    smoothed_forward_backward_spatial_correlation_matrix = get_smoothed_forward_backward_spatial_correlation_matrix(Y=Y,L=L)
    perf_smoothed_forward_backward_spatial_correlation_matrix = get_perf(smoothed_forward_backward_spatial_correlation_matrix)

    # Forward-backward smoothed R estimate
    forward_backward_smoothed_spatial_correlation_matrix = get_forward_backward_smoothed_spatial_correlation_matrix(Y=Y,L=L)
    perf_forward_backward_smoothed_spatial_correlation_matrix = get_perf(forward_backward_smoothed_spatial_correlation_matrix)



    string1 = '''Standard&{:.3f}&{:.3f}&{:.3f}&{:.3f}&{:.3f}\\'''.format(perf_standard_correlation_matrix['estimated_DOA'][0],perf_standard_correlation_matrix['ML_3dB_width'][0],perf_standard_correlation_matrix['estimated_DOA'][1],perf_standard_correlation_matrix['ML_3dB_width'][1],perf_standard_correlation_matrix['min_level'])
    string2 = '''Smoothed&{:.3f}&{:.3f}&{:.3f}&{:.3f}&{:.3f}\\'''.format(perf_smoothed_spatial_correlation_matrix['estimated_DOA'][0],perf_smoothed_spatial_correlation_matrix['ML_3dB_width'][0],perf_smoothed_spatial_correlation_matrix['estimated_DOA'][1],perf_smoothed_spatial_correlation_matrix['ML_3dB_width'][1],perf_smoothed_spatial_correlation_matrix['min_level'])
    string3 = '''FB&{:.3f}&{:.3f}&{:.3f}&{:.3f}&{:.3f}\\'''.format(perf_forward_backward_spatial_correlation_matrix['estimated_DOA'][0],perf_forward_backward_spatial_correlation_matrix['ML_3dB_width'][0],perf_forward_backward_spatial_correlation_matrix['estimated_DOA'][1],perf_forward_backward_spatial_correlation_matrix['ML_3dB_width'][1],perf_forward_backward_spatial_correlation_matrix['min_level'])
    string4 = '''FB + smoothed&{:.3f}&{:.3f}&{:.3f}&{:.3f}&{:.3f}\\'''.format(perf_smoothed_forward_backward_spatial_correlation_matrix['estimated_DOA'][0],perf_smoothed_forward_backward_spatial_correlation_matrix['ML_3dB_width'][0],perf_smoothed_forward_backward_spatial_correlation_matrix['estimated_DOA'][1],perf_smoothed_forward_backward_spatial_correlation_matrix['ML_3dB_width'][1],perf_smoothed_forward_backward_spatial_correlation_matrix['min_level'])
    string5 = '''Smoothed + FB&{:.3f}&{:.3f}&{:.3f}&{:.3f}&{:.3f}\\'''.format(perf_forward_backward_smoothed_spatial_correlation_matrix['estimated_DOA'][0],perf_forward_backward_smoothed_spatial_correlation_matrix['ML_3dB_width'][0],perf_forward_backward_smoothed_spatial_correlation_matrix['estimated_DOA'][1],perf_forward_backward_smoothed_spatial_correlation_matrix['ML_3dB_width'][1],perf_forward_backward_smoothed_spatial_correlation_matrix['min_level'])


    print(string1)
    print(string2)
    print(string3)
    print(string4)
    print(string5)

    string6 = '''Standard&{:.3f}&{:.3f}\\'''.format(np.mean(np.abs(np.array(perf_standard_correlation_matrix['estimated_DOA'])-np.array([get_config_2()['theta1'],get_config_2()['theta2']]))),
    np.mean(np.array(perf_standard_correlation_matrix['ML_3dB_width'])))
    string7 = '''Smoothed&{:.3f}&{:.3f}\\'''.format(np.mean(np.abs(np.array(perf_smoothed_spatial_correlation_matrix['estimated_DOA'])-np.array([get_config_2()['theta1'],get_config_2()['theta2']]))),
    np.mean(np.array(perf_smoothed_spatial_correlation_matrix['ML_3dB_width'])))
    string8 = '''FB&{:.3f}&{:.3f}\\'''.format(np.mean(np.abs(np.array(perf_forward_backward_spatial_correlation_matrix['estimated_DOA'])-np.array([get_config_2()['theta1'],get_config_2()['theta2']]))),
    np.mean(np.array(perf_forward_backward_spatial_correlation_matrix['ML_3dB_width'])))
    string9 = '''FB + smoothed&{:.3f}&{:.3f}\\'''.format(np.mean(np.abs(np.array(perf_smoothed_forward_backward_spatial_correlation_matrix['estimated_DOA'])-np.array([get_config_2()['theta1'],get_config_2()['theta2']]))),
    np.mean(np.array(perf_smoothed_forward_backward_spatial_correlation_matrix['ML_3dB_width'])))
    string10 = '''Smoothed + FB&{:.3f}&{:.3f}\\''' .format(np.mean(np.abs(np.array(perf_forward_backward_smoothed_spatial_correlation_matrix['estimated_DOA'])-np.array([get_config_2()['theta1'],get_config_2()['theta2']]))),
    np.mean(np.array(perf_forward_backward_smoothed_spatial_correlation_matrix['ML_3dB_width'])))  
    
    print('\n')
    print(string6)
    print(string7)
    print(string8)
    print(string9)
    print(string10)
    
    
   



    

   
   
    



    

  

def get_perf(correlation_matrix)->None:

    # We construct the DOA vector: from -50° to +50°, step 0.25°
    DOA = get_general_config()['DOA_array']

    # We get the power spectrum estimate
    music_spectrum_estimate = estimate_music_spectrum(R=correlation_matrix,kd=kd,M=M,Ns=2)
    
    return estimate_DOA(DOA_array=DOA,power_estimate=10*np.log10(music_spectrum_estimate/np.max(music_spectrum_estimate)),Ns=2)
    