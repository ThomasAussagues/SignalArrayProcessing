# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
from utils.standard_DAS import estimate_classical_spectrum
from utils.configuration import get_general_config,get_config_1

plt.rcParams.update({
  "text.usetex": True,
  'font.size': 14
})

# Question 2

# Estimate the classical spatial spectrum using the conventional method (Figure 4, bottom panel) and Equation (27). 
# Plot the response both in linear and dB scale. Discuss why the sources are not separated.

# Parameters


# Normalized wavenumber * d
kd = get_config_1()['k']*get_config_1()['d']
# Number of elements M
M = get_config_1()['M']

def run_question2(data:str)->None:

    # Input:
    # data:str, we specify which data we want to use with the string 'data'

    # We load the spatial correlation matrix
    R = np.load('data/' + data + '/spatial_correlation_matrix_incoherent.npy')

    # We get the classical power spectrum estimate
    classical_spectrum_estimate = estimate_classical_spectrum(R=R,kd=kd,M=M)
    # We normalized it and convert it into dB 
    classical_spectrum_estimate = 10*np.log10(classical_spectrum_estimate/np.max(classical_spectrum_estimate))

    # We plot the classical_spectrum_estimate vs. the DOA
    fig,ax = plt.subplots(1)
    DOA = get_general_config()['DOA_array']
    ax.plot(DOA,classical_spectrum_estimate,color='blue',label='$P_{DAS}(a(\\theta))$',linestyle=(0, (1, 1)))
    ax.set_xlabel('DOA $\\theta$ (in degrees)')
    ax.set_ylabel('Normalized power estimate $P_{DAS}(a(\\theta))$ (dB)')
    ax.annotate('Side lobe',
         xy=(-29,-8.4), xycoords='data',
         xytext=(-40, +80), textcoords='offset points', fontsize=12,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-.3"))
    ax.annotate('''The two peaks can 
    not be resolved''',
         xy=(-5,0), xycoords='data',
         xytext=(+50, -100), textcoords='offset points', fontsize=12,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-.3"))
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
    ax.set_title('Classical power spectrum estimate vs. the DOA')
    plt.savefig('images/question2/part_A_question_2_classical_spectrum_estimate.pdf',dpi=300,bbox_inches='tight')
    #plt.show()
    plt.close()

    