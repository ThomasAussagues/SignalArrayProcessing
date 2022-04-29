# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

# This script contains functions to plot spatial correlation matrices (amplitude and phase) and multiple spectrum estimates


import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
from cmcrameri import cm
import numpy as np
from utils.standard_DAS import  estimate_classical_spectrum
from utils.eigenvector import estimate_eigenvector_spectrum
from utils.music import estimate_music_spectrum
from utils.min_variance import estimate_minimum_variance_spectrum
from utils.configuration import get_general_config,get_config_2


# Normalized wavenumber * d
kd = get_config_2()['k']*get_config_2()['d']
# Number of elements M
M = get_config_2()['M']

def plot_matrix_phase(matrix,path,title)->None:

  # This function plots the spatial correlation matrix phase
  # Inputs
  # matrix: np.array, matrix of interest
  # path: str, path for saving the figure
  # title: str, figure title
  # Ouput:
  # None

  plt.figure()
  plt.clf()
  plt.title(title,y=1.05)
  plt.xlabel('Sensor')
  plt.xticks(np.arange(0,10),np.arange(1,11))
  plt.yticks(np.arange(0,10),np.arange(1,11))
  plt.ylabel('Sensor')
  plt.imshow(np.angle(matrix)*180/np.pi,cmap=cm.oslo,alpha=0.85,vmin=-180,vmax=180)
  c = plt.colorbar()
  c.set_label('Phase $\\arg r_{ij}$ (in degrees)')
  plt.savefig(path,dpi=300,bbox_inches='tight')
  plt.close()

  return None

  


    

    

def plot_matrix_amplitude(matrix,path,title)->None:

  # This function plots the spatial correlation matrix amplitude
  # Inputs
  # matrix: np.array, matrix of interest
  # path: str, path for saving the figure
  # title: str, figure title
  # Ouput:
  # None
  
  plt.figure()
  plt.clf()
  plt.title(title,y=1.05)
  plt.xlabel('Sensor')
  plt.xticks(np.arange(0,10),np.arange(1,11))
  plt.yticks(np.arange(0,10),np.arange(1,11))
  plt.ylabel('Sensor')
  plt.imshow(20*np.log10(np.abs(matrix)/np.max(np.abs(matrix))),cmap=cm.lajolla,alpha=0.85,vmin=20*np.log10(np.min(np.abs(matrix))/np.max(np.abs(matrix))),vmax=20*np.log10(np.max(np.abs(matrix))/np.max(np.abs(matrix))))
  c = plt.colorbar()
  c.set_label('Squared magnitude $20\log|r_{ij}|$ (dB)')
  plt.savefig(path,dpi=300,bbox_inches='tight')
  plt.close()

  return None

def plot_power_estimates(spatial_correlation_matrix,path,title)->None:

    # This function plots the different power spectrum estimates (DAS, MV, EV, MUSIC) for a given 
    # spatial correlation matrix
    # Inputs
    # spatial_correlation_matrix: np.array, spatial correlation matrix
    # path: str, path for saving the figure
    # title: str, figure title
    # Ouput:
    # None

    # We construct the DOA vector: from -50° to +50°, step 0.25°
    DOA = get_general_config()['DOA_array']
    # We get the power spectrum estimate
    minimum_variance_spectrum_estimate = estimate_minimum_variance_spectrum(R=spatial_correlation_matrix,kd=kd,M=M)
    # We normalized it and convert it into dB 
    minimum_variance_spectrum_estimate = 10*np.log10(minimum_variance_spectrum_estimate/np.max(minimum_variance_spectrum_estimate))
    # We get the power spectrum estimate
    classical_spectrum_estimate = estimate_classical_spectrum(R=spatial_correlation_matrix,kd=kd,M=M)
    # We normalized it and convert it into dB 
    classical_spectrum_estimate = 10*np.log10(classical_spectrum_estimate/np.max(classical_spectrum_estimate))
    # We get the power spectrum estimate
    music_spectrum_estimate = estimate_music_spectrum(R=spatial_correlation_matrix,kd=kd,M=M,Ns=2)
    # We normalized it and convert it into dB 
    music_spectrum_estimate = 10*np.log10(music_spectrum_estimate/np.max(music_spectrum_estimate))
    # We get the power spectrum estimate
    eigenvector_spectrum_estimate = estimate_eigenvector_spectrum(R=spatial_correlation_matrix,kd=kd,M=M,Ns=2)
    # We normalized it and convert it into dB 
    eigenvector_spectrum_estimate = 10*np.log10(eigenvector_spectrum_estimate/np.max(eigenvector_spectrum_estimate))

    
    fig,ax = plt.subplots(1)
    ax.plot(DOA,classical_spectrum_estimate,color='blue',label='$P_{DAS}(a(\\theta))$',linestyle=(0, (1, 1)))
    ax.plot(DOA,minimum_variance_spectrum_estimate,color='green',label='$P_{MV}(a(\\theta))$',linestyle=(0, (5, 1)))
    ax.plot(DOA,music_spectrum_estimate,color='red',label='$P_{MUSIC}(a(\\theta))$',linestyle=(0, (3, 1, 1, 1)))
    ax.plot(DOA,eigenvector_spectrum_estimate+0.1,color='k',label='$P_{EV}(a(\\theta))$',linestyle=(0, (3, 1, 1, 1, 1, 1)))
    ax.plot([get_config_2()['theta1'],get_config_2()['theta1']],[-50,3],linestyle='--',color='darkorange',label='$\\theta_1=${}°'.format(get_config_2()['theta1']))
    ax.plot([get_config_2()['theta2'],get_config_2()['theta2']],[-50,3],linestyle='--',color='magenta',label='$\\theta_2=${}°'.format(get_config_2()['theta2']))
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,shadow=True)
    ax.set_xlabel('DOA $\\theta$ (in degrees)')
    ax.set_ylabel('Normalized power estimate (dB)')
    ax.set_ylim([-50,3])
    ax.set_title(title)
    ax.xaxis.set_tick_params(which='major', size=10, width=1, direction='in', top='on')
    ax.xaxis.set_tick_params(which='minor', size=7, width=1, direction='in', top='on')
    ax.yaxis.set_tick_params(which='major', size=10, width=1, direction='in', right='on')
    ax.yaxis.set_tick_params(which='minor', size=7, width=1, direction='in', right='on') 
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))       
    #ax.grid(color='k', linestyle='--', linewidth=0.5)
    plt.savefig(path,dpi=300,bbox_inches ='tight')
    #plt.show()
    plt.close()

    return None