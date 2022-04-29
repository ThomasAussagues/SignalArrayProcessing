# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

# This script contains the configurations dictionaries


import numpy as np

# General parameters

config = dict()
config['DOA_array'] = np.arange(-50,50,0.01)

# Questions 1->7: incoherent sources

config1 = dict()
# Incoherent sources
config1['coherent'] = False
# Number of time samples
config1['N'] = 100
# number of sensors
config1['M'] = 10
# Source 1 SNR (in dB)
config1['SNR1'] = 0
# Source 2 SNR (in dB)
config1['SNR2'] = 0
# Source 1 direction of arrival (degrees)
config1['theta1'] = 0
# Source 2 direction of arrival (degrees)
config1['theta2'] = -10
# Phase shift between the the two sources (degrees)
config1['gamma'] = 45
# Array element spacing 
config1['d'] = 0.5
# Normalized wavenumber
config1['k'] = 2*np.pi
# Time sampling interval
config1['T'] = 0.5
# Source 1 normalized frequency/pulsation
config1['omega1'] = 2*np.pi
# Here, we want to make the two sources incoherent. Therefore, we make source 2 frequency slightly different from source 1 frequency
config1['omega2'] = config1['omega1']#*(1-3/config1['N'])
# We fix the numpy seed to ensure that all sources are subject to the same noise
config1['seed'] = 0
# We generate a complex AWGN (spatially white) with variance (1 or 2)
config1['variance'] = 1   

# Question 8: coherent sources

config2 = dict()
# Coherent sources
config2['coherent'] = True
# Number of time samples
config2['N'] = 100
# number of sensors
config2['M'] = 10
# Source 1 SNR (in dB)
config2['SNR1'] = 0
# Source 2 SNR (in dB)
config2['SNR2'] = 0
# Source 1 direction of arrival (degrees)
config2['theta1'] = 0
# Source 2 direction of arrival (degrees)
config2['theta2'] = 10
# Phase shift between the the two sources (degrees)
config2['gamma'] = 45
# Array element spacing 
config2['d'] = 0.5
# Normalized wavenumber
config2['k'] = 2*np.pi
# Time sampling interval
config2['T'] = 0.5
# Source 1 normalized frequency/pulsation
config2['omega1'] = 2*np.pi
# Here, we want to make the two sources coherent. 
config2['omega2'] = 2*np.pi
# We fix the numpy seed to ensure that all sources are subject to the same noise
config2['seed'] = 0
# We generate a complex AWGN (spatially white) with variance (1 or 2)
config2['variance'] = 1
# Diagonal loading: delta value
config2['delta'] = -15
# Spatial smoothing: number of sensors per subarray
config2['L'] = 5

def get_general_config():
    return config

def get_config_1()->dict:
    return config1

def get_config_2()->dict:
    return config2

def get_config_SNR_analysis(snr:float)->dict:
    config2['SNR1'] = snr
    config2['SNR2'] = snr
    return config2