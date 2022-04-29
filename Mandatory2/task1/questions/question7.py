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
from utils.min_variance import estimate_minimum_variance_spectrum
from utils.standard_DAS import estimate_classical_spectrum
from utils.configuration import get_config_1,get_general_config

plt.rcParams.update({
  "text.usetex": True,
  'font.size': 14
})

# Question 7

# Estimate the spatial spectrum with the MUSIC method (and eigenvector method) when the number of signals is incorrectly estimated. 
# Let the estimate of the number of signals be 0, 1, and 3. 
# Discuss the differences between the estimates for the various cases. 
# (Which spatial spectrum estimator is the eigenvector method equivalent to when 0 signals are assumed to be present?)

# Parameters

# Normalized wavenumber * d
kd = get_config_1()['k']*get_config_1()['d']
# Number of elements M
M = get_config_1()['M']

def run_question7(data:str)->None:

    # Input:
    # data:str, we specify which data we want to use with the string 'data'

    # We load the estimated spatial covariance matrix
    R = np.load('data/' + data + '/spatial_correlation_matrix_incoherent.npy')


    
    plt.tight_layout()
    DOA = get_general_config()['DOA_array']
    for i in range(4):
        Ns = [0,1,3,4][i]
        
        fig,ax = plt.subplots(1)

        # We get the EV power spectrum estimate
        eigenvector_spectrum_estimate = estimate_eigenvector_spectrum(R=R,kd=kd,M=M,Ns=Ns)
        # We normalized it and convert it into dB 
        eigenvector_spectrum_estimate = 10*np.log10(eigenvector_spectrum_estimate/np.max(eigenvector_spectrum_estimate))
        # We get the MUSIC power spectrum estimate
        music_spectrum_estimate = estimate_music_spectrum(R=R,kd=kd,M=M,Ns=Ns)
        # We normalized it and convert it into dB 
        music_spectrum_estimate = 10*np.log10(music_spectrum_estimate/np.max(music_spectrum_estimate))

        ax.plot(DOA,eigenvector_spectrum_estimate,color='k',label='$P_{EV}(a(\\theta))$',linestyle=(0, (3, 1, 1, 1, 1, 1)))
        ax.plot(DOA,music_spectrum_estimate,color='r',label='$P_{MUSIC}(a(\\theta))$',linestyle=(0, (5, 1)))

        #if i == 0:
        # We get the MV power spectrum estimate
        minimum_variance_spectrum_estimate = estimate_minimum_variance_spectrum(R=R,kd=kd,M=M)
        # We normalized it and convert it into dB 
        minimum_variance_spectrum_estimate = 10*np.log10(minimum_variance_spectrum_estimate/np.max(minimum_variance_spectrum_estimate))
        ax.plot(DOA,minimum_variance_spectrum_estimate+0.1,color='green',label='$P_{MV}(a(\\theta))$',linestyle=(0, (5, 1)))


        ax.plot([get_config_1()['theta1'],get_config_1()['theta1']],[np.min(eigenvector_spectrum_estimate),3],linestyle='--',color='darkorange',label='$\\theta_1=${}°'.format(get_config_1()['theta1']))
        ax.plot([get_config_1()['theta2'],get_config_1()['theta2']],[np.min(eigenvector_spectrum_estimate),3],linestyle='--',color='magenta',label='$\\theta_2=${}°'.format(get_config_1()['theta2']))
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,shadow=True)
        ax.xaxis.set_tick_params(which='major', size=10, width=1, direction='in', top='on')
        ax.xaxis.set_tick_params(which='minor', size=7, width=1, direction='in', top='on')
        ax.yaxis.set_tick_params(which='major', size=10, width=1, direction='in', right='on')
        ax.yaxis.set_tick_params(which='minor', size=7, width=1, direction='in', right='on') 
        ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
        ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
        ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
        ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1)) 
       

        
        #ax.legend(lns,labs,loc='upper center', bbox_to_anchor=(0.5, -0.2),
            #fancybox=True, shadow=True, ncol=3)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
        fig.supxlabel('DOA $\\theta$ (in degrees)')
        fig.supylabel('Normalized power estimate (dB)')
        fig.suptitle('MUSIC \& eigenvector power estimates for $N_s={}$'.format(Ns))
        plt.savefig('images/question7/part_A_question_7_number_of_sources_+Ns={}.pdf'.format(Ns),dpi=300,bbox_inches ='tight')
        #plt.show()
        plt.close

    fig,ax = plt.subplots(1)

    # We get the power spectrum estimate
    minimum_variance_spectrum_estimate = estimate_minimum_variance_spectrum(R=R,kd=kd,M=M)
    # We normalized it and convert it into dB 
    minimum_variance_spectrum_estimate = 10*np.log10(minimum_variance_spectrum_estimate/np.max(minimum_variance_spectrum_estimate))
    # We get the power spectrum estimate
    classical_spectrum_estimate = estimate_classical_spectrum(R=R,kd=kd,M=M)
    # We normalized it and convert it into dB 
    classical_spectrum_estimate = 10*np.log10(classical_spectrum_estimate/np.max(classical_spectrum_estimate))
    # We get the power spectrum estimate
    music_spectrum_estimate = estimate_music_spectrum(R=R,kd=kd,M=M,Ns=2)
    # We normalized it and convert it into dB 
    music_spectrum_estimate = 10*np.log10(music_spectrum_estimate/np.max(music_spectrum_estimate))
    # We get the power spectrum estimate
    eigenvector_spectrum_estimate = estimate_eigenvector_spectrum(R=R,kd=kd,M=M,Ns=2)
    # We normalized it and convert it into dB 
    eigenvector_spectrum_estimate = 10*np.log10(eigenvector_spectrum_estimate/np.max(eigenvector_spectrum_estimate))

    ax.plot(DOA,classical_spectrum_estimate,color='blue',label='$P_{DAS}(a(\\theta))$',linestyle=(0, (1, 1)))
    ax.plot(DOA,minimum_variance_spectrum_estimate,color='green',label='$P_{MV}(a(\\theta))$',linestyle=(0, (5, 1)))
    ax.plot(DOA,music_spectrum_estimate,color='red',label='$P_{MUSIC}(a(\\theta))$',linestyle=(0, (3, 1, 1, 1)))
    ax.plot(DOA,eigenvector_spectrum_estimate+0.1,color='k',label='$P_{EV}(a(\\theta))$',linestyle=(0, (3, 1, 1, 1, 1, 1)))
    ax.plot([get_config_1()['theta1'],get_config_1()['theta1']],[np.min(eigenvector_spectrum_estimate),3],linestyle='--',color='darkorange',label='$\\theta_1=${}°'.format(get_config_1()['theta1']))
    ax.plot([get_config_1()['theta2'],get_config_1()['theta2']],[np.min(eigenvector_spectrum_estimate),3],linestyle='--',color='magenta',label='$\\theta_2=${}°'.format(get_config_1()['theta2']))
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,shadow=True)
    ax.xaxis.set_tick_params(which='major', size=10, width=1, direction='in', top='on')
    ax.xaxis.set_tick_params(which='minor', size=7, width=1, direction='in', top='on')
    ax.yaxis.set_tick_params(which='major', size=10, width=1, direction='in', right='on')
    ax.yaxis.set_tick_params(which='minor', size=7, width=1, direction='in', right='on') 
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1)) 
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,shadow=True)
    ax.set_xlabel('DOA $\\theta$ (in degrees)')
    ax.set_ylabel('Normalized power estimate (dB)')
    ax.set_title('DAS, minimum-variance, MUSIC and EV \npower estimates, incoherent sources')
    plt.savefig('images/question7/part_A_question_7_all.pdf',dpi=300,bbox_inches ='tight')
    #plt.show()
    plt.close()

   






