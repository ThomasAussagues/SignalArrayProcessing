# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
from cmcrameri import cm
from utils.standard_DAS import estimate_classical_spectrum
from utils.configuration import get_config_1

plt.rcParams.update({
  "text.usetex": True,
  'font.size': 14
})
# Parameter

# Number of sensors
M = get_config_1()['M']


def run_question3(data:str)->None:

    # Input:
    # data:str, we specify which data we want to use with the string 'data'

    # We load the estimated spatial covariance matrix
    R = np.load('data/' + data + '/spatial_correlation_matrix_incoherent.npy')

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
    ax.text(x=0.8,y=12,s='''Signal
      +
    noise
    subspace''')
    ax.text(x=3.25,y=14,s='Signal + noise subspace')
    #plt.fill([0,2.5,2.5,0,0],[np.min(eigenvalues),np.min(eigenvalues),np.max(eigenvalues),np.max(eigenvalues),np.min(eigenvalues)],color='blue',alpha=0.5)
    #plt.fill([2.5,10.5,10.5,2.5,2.5],[np.min(eigenvalues),np.min(eigenvalues),np.max(eigenvalues),np.max(eigenvalues),np.min(eigenvalues)],color='red',alpha=0.5)
    ax.scatter(np.arange(1,M+1)[:2],eigenvalues[:2],label='$\lambda_s$, signal + noise subspace',marker='d',color='blue')
    ax.scatter(np.arange(1,M+1)[2:],eigenvalues[2:],label='$\lambda_n$, noise only subspace',marker='d',color='red')
    ax.set_xlabel('Index $i$')
    ax.set_ylabel('Eigenvalue $\lambda_i$')
    ax.plot([2.5,2.5],[np.min(eigenvalues),np.max(eigenvalues)],color='k',linestyle='--')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,shadow=True)
    ax.xaxis.set_tick_params(which='major', size=10, width=1, direction='in', top='on')
    #ax.xaxis.set_tick_params(which='minor', size=7, width=1, direction='in', top='on')
    ax.yaxis.set_tick_params(which='major', size=10, width=1, direction='in', right='on')
    ax.yaxis.set_tick_params(which='minor', size=7, width=1, direction='in', right='on') 
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
    #ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    ax.set_title('Eigenvalues distribution')
    plt.savefig('images/question4/part_A_question_4_eigenvalues_distribution.pdf',dpi=300,bbox_inches='tight')
    #plt.show()
    plt.close()


