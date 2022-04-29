# IN5450 Mandatory 2 
# Thomas Aussaguès, 14/03/2022
# thomas.aussagues@imt-atlantique.net

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
from cmcrameri import cm
from utils.correlation_matrix_estimation import get_standard_correlation_matrix_estimation

plt.rcParams.update({
  "text.usetex": True,
  'font.size': 14
})

# Question 1
# Estimate the spatial correlation matrix and plot its absolute value.

def run_question1(data:str)->None:

    # Input:
    # data:str, we specify which data we want to use with the string 'data'
    
    # We get the array output signal Y
    Y = np.load('data/' + data + '/data_incoherent.npy')
    # We compute the spatial auto correlation matrix R
    R = get_standard_correlation_matrix_estimation(Y=Y)
    # We save the auto correlation matrix R
    np.save('data/' + data + '/spatial_correlation_matrix_incoherent',R)

    # Plots 

    # We plot R absolute value in dB
    plt.figure()
    plt.imshow(20*np.log10(np.abs(R)/np.max(np.abs(R))),cmap=cm.lajolla,alpha=0.85,vmin=20*np.log10(np.min(np.abs(R))/np.max(np.abs(R))),vmax=20*np.log10(np.max(np.abs(R))/np.max(np.abs(R))))
    plt.xlabel('Sensor')
    plt.xticks(np.arange(0,10),np.arange(1,11))
    plt.yticks(np.arange(0,10),np.arange(1,11))
    plt.ylabel('Sensor')
    c = plt.colorbar()
    c.set_label('Amplitude $20\log|r_{ij}|$ (dB)')
    plt.title('Spatial correlation matrix estimate amplitude (dB)',y=1.05)
    plt.savefig('images/question1/part_A_question_1_autocorrelation_matrix_amplitude.pdf',dpi=300)
    #plt.show()
    plt.close()

    # We plot R phase
    plt.figure()
    plt.imshow(np.angle(R)*180/np.pi,cmap=cm.oslo,alpha=0.85,vmin=-180,vmax=180)
    plt.xlabel('Sensor')
    plt.xticks(np.arange(0,10),np.arange(1,11))
    plt.yticks(np.arange(0,10),np.arange(1,11))
    plt.ylabel('Sensor')
    c = plt.colorbar()
    c.set_label('Phase $\\arg r_{ij}$ (in degrees)')
    plt.title('Spatial correlation matrix estimate phase',y=1.05)
    plt.savefig('images/question1/part_A_question_1_autocorrelation_matrix_phase.pdf',dpi=300)
    #plt.show()
    plt.close()

    # We assume the random process to be W.S.S and ergodic. We can check these properties using a 2D plot of the process
    
    fig,axs = plt.subplots(2,1,sharex=True,sharey=True)
    ax1,ax2 = axs.flat
    im1 = ax1.imshow(20*np.log10(np.abs(Y)/np.max(np.abs(Y))),cmap=cm.lajolla,alpha=0.85,vmin=20*np.log10(np.min(np.abs(Y))/np.max(np.abs(Y))),vmax=20*np.log10(np.max(np.abs(Y))/np.max(np.abs(Y))))
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes('top', size=0.25, pad=0.35)
    cbar = fig.colorbar(im1, cax=cax, orientation='horizontal') 
    cbar.ax.set_title('Amplitude $20\log| y_{it}|$ (dB)') 
    im2 = ax2.imshow(np.angle(Y)*180/np.pi,cmap=cm.oslo,alpha=0.85)
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes('top', size=0.25, pad=0.35)
    cbar = fig.colorbar(im2, cax=cax, orientation='horizontal')
    cbar.ax.set_title('Phase $\\arg y_{it}$ (in degrees)')
    fig.supxlabel('Time $t$')
    fig.supylabel('Sensor $i$')
    fig.suptitle('$\mathbf{Y}$ amplitude and phase as 2D images')
    plt.savefig('images/question1/part_A_question_1_WSS_ergodicity.pdf',dpi=300)
    #plt.show()
    plt.close()