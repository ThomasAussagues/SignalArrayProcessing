# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from utils.configuration import get_config_SNR_analysis
from utils.properties import estimate_DOA
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
from cmcrameri import cm
from utils.standard_DAS import estimate_classical_spectrum
from utils.eigenvector import estimate_eigenvector_spectrum
from utils.music import estimate_music_spectrum
from utils.min_variance import estimate_minimum_variance_spectrum
from utils.correlation_matrix_estimation import get_forward_backward_correlation_matrix,get_standard_correlation_matrix_estimation,get_forward_backward_smoothed_spatial_correlation_matrix,get_smoothed_forward_backward_spatial_correlation_matrix,get_smoothed_spatial_correlation_matrix
from utils.configuration import get_config_2,get_general_config
plt.rcParams.update({
  "text.usetex": True,
  'font.size': 14
})

def analysis(data:str):

    snr_values = np.arange(-10,10,1)
    estimated_DOA = []
    mean_error = []
    mean_resolution = []
    for snr in snr_values:
      
        spatial_correlation_matrix = get_forward_backward_correlation_matrix(Y=np.load('data/'+data+'/data_coherent_{}.npy'.format(snr)))

        config = get_config_SNR_analysis(0)
        kd = config['k']*config['d']
        M = config['M']

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
        props = estimate_DOA(DOA_array=DOA,power_estimate=eigenvector_spectrum_estimate,Ns=2)
        
        estimated_DOA.append(props['estimated_DOA'])
        mean_error.append(np.mean(np.abs(np.array(props['estimated_DOA'])-np.array([get_config_2()['theta1'],get_config_2()['theta2']]))))
        mean_resolution.append(np.mean(np.array(props['ML_3dB_width'])))
    
    
    
    estimated_DOA = np.array(estimated_DOA)
    fig,ax = plt.subplots(1)
    ax.plot(snr_values,estimated_DOA[:,0],marker='^',color='red',label='$\hat{\\theta}_1$')
    ax.plot([np.min(snr_values),np.max(snr_values)],[get_config_2()['theta1'],get_config_2()['theta1']],linestyle='--',color='red',label='$\\theta_1$')
    ax.plot(snr_values,estimated_DOA[:,1],marker='v',color='blue',label='$\hat{\\theta}_2$')
    ax.plot([np.min(snr_values),np.max(snr_values)],[get_config_2()['theta2'],get_config_2()['theta2']],linestyle='--',color='blue',label='$\\theta_2$')
    ax.set_title('Estimated DOA vs. SNR, MUSIC\n with forward-backward $\mathbf{R}$')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4,shadow=True)
    ax.set_xlabel('SNR (dB)')
    ax.set_ylabel('Estimated DOA $\\theta_i$ (degrees)')
    ax.xaxis.set_tick_params(which='major', size=10, width=1, direction='in', top='on')
    ax.xaxis.set_tick_params(which='minor', size=7, width=1, direction='in', top='on')
    ax.yaxis.set_tick_params(which='major', size=10, width=1, direction='in', right='on')
    ax.yaxis.set_tick_params(which='minor', size=7, width=1, direction='in', right='on') 
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1)) 
    plt.savefig('images/snr_analysis/DOA_estimation_vs_snr_forward_backward_correlation_matrix.pdf',dpi=300,bbox_inches='tight')
    #plt.show()
    plt.close()


    fig,ax = plt.subplots(1)
    ax.plot(snr_values,mean_error,marker='^',color='red',label='Mean error')
    ax.plot(snr_values,mean_resolution,marker='v',color='blue',label='mean ML width')
    ax.set_title('Mean error and ML width vs. SNR, MUSIC\n with forward-backward $\mathbf{R}$')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4,shadow=True)
    ax.set_xlabel('SNR (dB)')
    ax.set_ylabel('$\\theta_i-\\theta$ and $\Delta\\theta$ (degrees)')
    ax.xaxis.set_tick_params(which='major', size=10, width=1, direction='in', top='on')
    ax.xaxis.set_tick_params(which='minor', size=7, width=1, direction='in', top='on')
    ax.yaxis.set_tick_params(which='major', size=10, width=1, direction='in', right='on')
    ax.yaxis.set_tick_params(which='minor', size=7, width=1, direction='in', right='on') 
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(0.5)) 
    plt.savefig('images/snr_analysis/mean_error_and_resolution_vs_snr_forward_backward_correlation_matrix.pdf',dpi=300,bbox_inches='tight')
    #plt.show()
    plt.close()
