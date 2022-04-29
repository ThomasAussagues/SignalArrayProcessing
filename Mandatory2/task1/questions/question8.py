# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'

from utils.correlation_matrix_estimation import diagonal_loading, get_forward_backward_correlation_matrix, get_rotary_averaged_spatial_correlation_matrix,get_standard_correlation_matrix_estimation,get_forward_backward_smoothed_spatial_correlation_matrix,get_smoothed_forward_backward_spatial_correlation_matrix,get_smoothed_spatial_correlation_matrix
from utils.configuration import get_config_2
from utils.plots import plot_matrix_amplitude,plot_matrix_phase,plot_power_estimates
plt.rcParams.update({
  "text.usetex": True,
  'font.size': 14
})


# Normalized wavenumber * d
kd = get_config_2()['k']*get_config_2()['d']
# Number of elements M
M = get_config_2()['M']
# Number of sensors per subarray L
L = get_config_2()['L']



# Question 8
# What if sources are correlated

def run_question8(data:str)->None:

    # Input:
    # data:str, we specify which data we want to use with the string 'data'

    # We get the array output signal Y
    Y = np.load('data/' + data + '/data_coherent.npy')
    # We compute the spatial auto correlation matrix R
    R = get_standard_correlation_matrix_estimation(Y=Y)


    # We compute the mateix rank. Since we have coherent sources and 10 sensors, the rank should be 9.
    # Therfore, the matrix is not invertible!
    #print('RANK = ', np.linalg.matrix_rank(R))

    # Plot the distribution of the eigenvalues of the correlation matrix and explain it on the basis of the signal and noise model.

    # First, we make an eigendecomposition of the spatial correlation matrix R.

    eigenvalues,eigenvectors = np.linalg.eig(R)

    # Again, the eigenvalues which should real (according to the spectral theorem) contain a small (e-17) imaginiary part.
    # We drop this part by selecting the real part.

    eigenvalues = np.real(eigenvalues)

    # We sort the eigenvectors according to their asscoiated eigenvalues.
    # np.sort sorts the array in ascending order. We use np.flip to reverse the order.
    eigenvectors = eigenvectors[np.flip(np.argsort(eigenvalues))]
    eigenvalues = np.flip(np.sort(eigenvalues))

    # We plot the distribution of the eigenvalues of the correlation matrix
    fig,ax = plt.subplots(1)
    ax.text(x=0.8,y=15,s='''Signal
        +
    noise
    subspace''')
    ax.plot([2,2],[20,80],color='k',linestyle='--')
    ax.text(x=5.25,y=17,s='Signal + noise subspace')
    #plt.fill([0,2.5,2.5,0,0],[np.min(eigenvalues),np.min(eigenvalues),np.max(eigenvalues),np.max(eigenvalues),np.min(eigenvalues)],color='blue',alpha=0.5)
    #plt.fill([2.5,10.5,10.5,2.5,2.5],[np.min(eigenvalues),np.min(eigenvalues),np.max(eigenvalues),np.max(eigenvalues),np.min(eigenvalues)],color='red',alpha=0.5)
    ax.scatter(np.arange(1,M+1)[:1],eigenvalues[:1],label='$\lambda_s$, signal + noise subspace',marker='d',color='blue')
    ax.scatter(np.arange(1,M+1)[1:],eigenvalues[1:],label='$\lambda_n$, noise only subspace',marker='d',color='red')
    ax.set_xlabel('Index $i$')
    ax.set_ylabel('Eigenvalue $\lambda_i$')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,shadow=True)
    ax.xaxis.set_tick_params(which='major', size=10, width=1, direction='in', top='on')
    ax.xaxis.set_tick_params(which='minor', size=7, width=1, direction='in', top='on')
    ax.yaxis.set_tick_params(which='major', size=10, width=1, direction='in', right='on')
    ax.yaxis.set_tick_params(which='minor', size=7, width=1, direction='in', right='on') 
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    ax.set_title('Eigenvalues distribution')
    ax.set_ylim([0,np.max(eigenvalues)+3])
    plt.savefig('images/question8/part_A_question_8_eigenvalues_distribution.pdf',dpi=300)
    #plt.show()

    

    

    # Here, we plot all the power estimates for different covariance matrices. We also plot the matrices

    # Standard covariance matrix ##########################################################################################    

    plot_matrix_amplitude(matrix=get_standard_correlation_matrix_estimation(Y=Y),
        path='images/question8/matrices/spatial_correlation_matrix_amplitude.pdf',
        title='Spatial correlation matrix amplitude\n')

    plot_matrix_phase(matrix=get_standard_correlation_matrix_estimation(Y=Y),
        path='images/question8/matrices/spatial_correlation_matrix_phase.pdf',
        title='Spatial correlation matrix phase\n')

    plot_power_estimates(spatial_correlation_matrix=get_standard_correlation_matrix_estimation(Y=Y),
        path='images/question8/spectrums/part_A_question_8_all_spectrums_standard_correlation_matrix.pdf',
        title='DAS, MV, MUSIC and EV spectrums for coherent sources\n standard correlation matrix')

    # Smoothed covariance matrix ###########################################################################################

    plot_matrix_amplitude(matrix=get_smoothed_spatial_correlation_matrix(Y=Y,L=L),
        path='images/question8/matrices/smoothed_spatial_correlation_matrix_amplitude.pdf',
        title='Smoothed spatial correlation matrix amplitude\n')

    plot_matrix_phase(matrix=get_smoothed_spatial_correlation_matrix(Y=Y,L=L),
        path='images/question8/matrices/smoothed_spatial_correlation_matrix_phase.pdf',
        title='Smoothed spatial correlation matrix phase\n')

    plot_power_estimates(spatial_correlation_matrix=get_smoothed_spatial_correlation_matrix(Y=Y,L=L),
        path='images/question8/spectrums/part_A_question_8_all_spectrums_smoothed_correlation_matrix.pdf',
        title='DAS, MV, MUSIC and EV spectrums for coherent sources\n smoothed correlation matrix')

    # Forward-backward covariance matrix ###################################################################################

    plot_matrix_amplitude(matrix=get_forward_backward_correlation_matrix(Y=Y),
        path='images/question8/matrices/forward_backward_spatial_correlation_matrix_amplitude.pdf',
        title='Forward-backward spatial correlation\nmatrix amplitude')

    plot_matrix_phase(matrix=get_forward_backward_correlation_matrix(Y=Y),
        path='images/question8/matrices/forward_backward_spatial_correlation_matrix_phase.pdf',
        title='Forward-backward spatial correlation matrix phase\n')


    plot_power_estimates(spatial_correlation_matrix=get_forward_backward_correlation_matrix(Y=Y),
        path='images/question8/spectrums/part_A_question_8_all_spectrums_forward_backward_correlation_matrix.pdf',
        title='DAS, MV, MUSIC and EV spectrums for coherent sources\n forward-backward correlation matrix')
   
    # Smoothed forward-backward covariance matrix ###########################################################################

    plot_matrix_amplitude(matrix=get_smoothed_forward_backward_spatial_correlation_matrix(Y=Y,L=L),
        path='images/question8/matrices/smoothed_forward_backward_spatial_correlation_matrix_amplitude.pdf',
        title='Smoothed forward-backward spatial\ncorrelation matrix amplitude')

    plot_matrix_phase(matrix=get_smoothed_forward_backward_spatial_correlation_matrix(Y=Y,L=L),
        path='images/question8/matrices/smoothed_forward_backward_spatial_correlation_matrix_phase.pdf',
        title='Smoothed forward-backward spatial\ncorrelation matrix phase')
    
    plot_power_estimates(spatial_correlation_matrix=get_smoothed_forward_backward_spatial_correlation_matrix(Y=Y,L=L),
        path='images/question8/spectrums/part_A_question_8_all_spectrums_smoothed_forward_backward_spatial_correlation_matrix.pdf',
        title='DAS, MV, MUSIC and EV spectrums for coherent sources\n smoothed forward-backward spatial correlation_matrix')

    # Forward-backward smoothed covariance matrix ###########################################################################

    plot_matrix_amplitude(matrix=get_forward_backward_smoothed_spatial_correlation_matrix(Y=Y,L=L),
        path='images/question8/matrices/forward_backward_smoothed_spatial_correlation_matrix_amplitude.pdf',
        title='Forward-backward smoothed spatial\ncorrelation matrix amplitude')

    plot_matrix_phase(matrix=get_forward_backward_smoothed_spatial_correlation_matrix(Y=Y,L=L),
        path='images/question8/matrices/forward_backward_smoothed_spatial_correlation_matrix_phase.pdf',
        title='Forward-backward smoothed spatial\ncorrelation matrix phase')


    plot_power_estimates(spatial_correlation_matrix=get_forward_backward_smoothed_spatial_correlation_matrix(Y=Y,L=L),
        path='images/question8/spectrums/part_A_question_8_all_spectrums_forward_backward_smoothed_spatial_correlation_matrix.pdf',
        title='DAS, MV, MUSIC and EV spectrums for coherent sources\n forward-backward smoothed spatial correlation_matrix')


    # Diagonaly loaded covariance matrix ###########################################################################


    plot_matrix_amplitude(matrix=diagonal_loading(R=get_standard_correlation_matrix_estimation(Y=Y),delta=get_config_2()['delta']),
        path='images/question8/matrices/diagonaly_loaded_spatial_correlation_matrix_amplitude.pdf',
        title='Diagonaly loaded spatial\ncorrelation matrix amplitude')

    plot_matrix_phase(matrix=diagonal_loading(R=get_standard_correlation_matrix_estimation(Y=Y),delta=get_config_2()['delta']),
        path='images/question8/matrices/diagonaly_loaded_spatial_correlation_matrix_phase.pdf',
        title='Diagonaly loaded spatial\ncorrelation matrix phase')

    plot_power_estimates(spatial_correlation_matrix=diagonal_loading(R=get_standard_correlation_matrix_estimation(Y=Y),delta=get_config_2()['delta']),
        path='images/question8/spectrums/part_A_question_8_all_spectrums_diagonaly_loaded.pdf',
        title='DAS, MV, MUSIC and EV spectrums for coherent sources\n diagonaly loaded correlation_matrix')

    # Rotary averaged covariance matrix ###########################################################################


    plot_matrix_amplitude(matrix=get_rotary_averaged_spatial_correlation_matrix(Y=Y),
        path='images/question8/matrices/rotary_averaged_spatial_correlation_matrix_amplitude.pdf',
        title='Rotary averaged spatial\ncorrelation matrix amplitude')

    plot_matrix_phase(matrix=get_rotary_averaged_spatial_correlation_matrix(Y=Y),
        path='images/question8/matrices/rotary_averaged_spatial_correlation_matrix_phase.pdf',
        title='Rotary averaged spatial\ncorrelation matrix phase')

    plot_power_estimates(spatial_correlation_matrix=get_rotary_averaged_spatial_correlation_matrix(Y=Y),
        path='images/question8/spectrums/part_A_question_8_all_spectrums_rotary_averaged.pdf',
        title='DAS, MV, MUSIC and EV spectrums for coherent sources\n rotary averaged correlation_matrix')

 
    
  
    

   
    
    

    


    

   

    