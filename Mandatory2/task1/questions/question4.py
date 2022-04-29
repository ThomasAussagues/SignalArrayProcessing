# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
from cmcrameri import cm
from utils.min_variance import estimate_minimum_variance_spectrum
from utils.standard_DAS import estimate_classical_spectrum
from utils.configuration import get_config_1,get_general_config

plt.rcParams.update({
  "text.usetex": True,
  'font.size': 14
})

# Question 4

# Estimate the spatial spectrum for the same signal using the minimum variance beamformer (Capon’s beamformer) (Figure 5). 
# Plot the response both in linear and dB scale. Discuss the differences from the conventional beamformer.


# Parameters

# Normalized wavenumber * d
kd = get_config_1()['k']*get_config_1()['d']
# Number of elements M
M = get_config_1()['M']

def run_question4(data:str)->None:

    # Input:
    # data:str, we specify which data we want to use with the string 'data'

    # We load the estimated spatial covariance matrix
    R = np.load('data/' + data + '/spatial_correlation_matrix_incoherent.npy')


    # We get the minimum variance power spectrum estimate
    minimum_variance_spectrum_estimate = estimate_minimum_variance_spectrum(R=R,kd=kd,M=M)
    # We normalized it and convert it into dB 
    minimum_variance_spectrum_estimate = 10*np.log10(minimum_variance_spectrum_estimate/np.max(minimum_variance_spectrum_estimate))

    # We get the classical power spectrum estimate
    classical_spectrum_estimate = estimate_classical_spectrum(R=R,kd=kd,M=M)
    # We normalized it and convert it into dB 
    classical_spectrum_estimate = 10*np.log10(classical_spectrum_estimate/np.max(classical_spectrum_estimate))

    # We plot the minimum variance spectrum estimate vs. the DOA
    fig,ax = plt.subplots(1)
    DOA = get_general_config()['DOA_array']
    ax.plot(DOA,minimum_variance_spectrum_estimate,color='green',label='$P_{MV}(a(\\theta))$',linestyle=(0, (5, 1)))
    ax.plot(DOA,classical_spectrum_estimate,color='blue',label='$P_{DAS}(a(\\theta))$',linestyle=(0, (1, 1)))
    ax.set_xlabel('DOA $\\theta$ (in degrees)')
    ax.set_ylabel('Normalized power estimate $P_{MV}(a(\\theta))$ (dB)')
    ax.annotate('Lower side lobe',
         xy=(-29,-8.4), xycoords='data',
         xytext=(-40, +80), textcoords='offset points', fontsize=12,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-.3"))
    ax.annotate('',
         xy=(-29,-10.4), xycoords='data',
         xytext=(2, +120), textcoords='offset points', fontsize=12,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-.3"))
    ax.annotate('''The two peaks can 
    be resolved''',
         xy=(-10,0), xycoords='data',
         xytext=(+80, -130), textcoords='offset points', fontsize=12,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-.3"))
    ax.annotate('''''',
         xy=(0,0), xycoords='data',
         xytext=(+52, -107), textcoords='offset points', fontsize=12,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-.3"))
    ax.set_title('Minimum variance power estimate vs. the DOA')
    ax.plot([get_config_1()['theta1'],get_config_1()['theta1']],[np.min(classical_spectrum_estimate),3],linestyle='--',color='darkorange',label='$\\theta_1=${}°'.format(get_config_1()['theta1']))
    ax.plot([get_config_1()['theta2'],get_config_1()['theta2']],[np.min(classical_spectrum_estimate),3],linestyle='--',color='magenta',label='$\\theta_2=${}°'.format(get_config_1()['theta2']))
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,shadow=True)
    ax.xaxis.set_tick_params(which='major', size=10, width=1, direction='in', top='on')
    ax.xaxis.set_tick_params(which='minor', size=7, width=1, direction='in', top='on')
    ax.yaxis.set_tick_params(which='major', size=10, width=1, direction='in', right='on')
    ax.yaxis.set_tick_params(which='minor', size=7, width=1, direction='in', right='on') 
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1)) 
    plt.savefig('images/question3/part_A_question_3_minimum_variance_spectrum_estimate.pdf',dpi=300,bbox_inches='tight')
    #plt.show()
    plt.close()



