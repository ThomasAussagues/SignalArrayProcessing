# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
from cmcrameri import cm
from utils.eigenvector import estimate_eigenvector_spectrum
from utils.music import estimate_music_spectrum
from utils.configuration import get_config_1,get_general_config

plt.rcParams.update({
  "text.usetex": True,
  'font.size': 14
})

# Question 6

# Estimate the spatial spectrum by the eigenvector method (see the lecture notes for definition). 
# Plot the response both in linear and dB scale. Discuss the differences from the MUSIC beamformer.

# Parameters

# Normalized wavenumber * d
kd = get_config_1()['k']*get_config_1()['d']
# Number of elements M
M = get_config_1()['M']

def run_question6(data:str)->None:

    # Input:
    # data:str, we specify which data we want to use with the string 'data'

    # We load the estimated spatial covariance matrix
    R = np.load('data/' + data + '/spatial_correlation_matrix_incoherent.npy')




    # We get the MUSIC power spectrum estimate
    music_spectrum_estimate = estimate_music_spectrum(R=R,kd=kd,M=M,Ns=2)
    # We normalized it and convert it into dB 
    music_spectrum_estimate = 10*np.log10(music_spectrum_estimate/np.max(music_spectrum_estimate))

    # We get the EV power spectrum estimate
    eigenvector_spectrum_estimate = estimate_eigenvector_spectrum(R=R,kd=kd,M=M,Ns=2)
    # We normalized it and convert it into dB 
    eigenvector_spectrum_estimate = 10*np.log10(eigenvector_spectrum_estimate/np.max(eigenvector_spectrum_estimate))


    # We plot the minimum variance spectrum estimate vs. the DOA
    fig,ax = plt.subplots(1)
    DOA = get_general_config()['DOA_array']
    ax.plot(DOA,eigenvector_spectrum_estimate,color='k',label='$P_{EV}(a(\\theta))$',linestyle=(0, (3, 1, 1, 1, 1, 1)))
    ax.plot(DOA,music_spectrum_estimate,color='r',label='$P_{MUSIC}(a(\\theta))$',linestyle=(0, (3, 1, 1, 1)))
    ax.set_xlabel('DOA $\\theta$ (in degrees)')
    ax.set_ylabel('Normalized power estimate $P_{EV}(a(\\theta))$ (dB)')
    ax.plot([get_config_1()['theta1'],get_config_1()['theta1']],[np.min(music_spectrum_estimate),3],linestyle='--',color='darkorange',label='$\\theta_1=${}°'.format(get_config_1()['theta1']))
    ax.plot([get_config_1()['theta2'],get_config_1()['theta2']],[np.min(music_spectrum_estimate),3],linestyle='--',color='magenta',label='$\\theta_2=${}°'.format(get_config_1()['theta2']))
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,shadow=True)
    ax.xaxis.set_tick_params(which='major', size=10, width=1, direction='in', top='on')
    ax.xaxis.set_tick_params(which='minor', size=7, width=1, direction='in', top='on')
    ax.yaxis.set_tick_params(which='major', size=10, width=1, direction='in', right='on')
    ax.yaxis.set_tick_params(which='minor', size=7, width=1, direction='in', right='on') 
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1)) 
    ax.set_title('Eigenvector power estimate vs. the DOA')
    plt.savefig('images/question6/part_A_question_6_eigenvector_spectrum_estimate.pdf',dpi=300,bbox_inches='tight')
    #plt.show()
    plt.close()