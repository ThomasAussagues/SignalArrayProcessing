from utils.plots import plot_DAS_image
import numpy as np
import scipy.io
# If we want to use the non parallel algorithms
# from utils.DAS_imaging import DAS_imaging_TDMA, DAS_imaging_CDMA
from utils.parallel_DAS_imaging import parallel_DAS_imaging_TDMA
import time
from utils.performance import eval_perf
def run_question_3():

    '''First, we import the matlab data using scipy's loadmat function.'''

    matlab_data = scipy.io.loadmat('data/mimo_project.mat')

    '''Then, we get all parameters of the matlab data.'''

    '''Bandwidth in Hertz (Hz)'''
    B = float(matlab_data['B'])
    '''Number of receivers'''
    N_rx = int(matlab_data['N_rx'])
    '''Number of time samples'''
    N_t = int(matlab_data['N_t'])
    '''Number of transmitters'''
    N_tx = int(matlab_data['N_tx'])
    '''Time series length in seconds (s)'''
    T_p = float(matlab_data['T_p'])
    '''Wave celerity (in m/s)'''
    c = float(matlab_data['c'])
    '''cdma_data'''
    cdma_data = matlab_data['cdma_data']
    '''Central frequency in Hertz (Hz)'''
    fc = float(matlab_data['fc'])
    '''Sampling frequency in Hertz (Hz)'''
    fs = float(matlab_data['fs'])
    '''Transmitters positions (in m)'''
    tx_positions = matlab_data['tx_pos'][0]
    '''Receivers positions (in m)'''
    rx_positions = matlab_data['rx_pos'][0]
    '''tdma_data'''
    tdma_data = matlab_data['tdma_data']

    '''We create a dict containing all the necessary information about the imaging grid.'''
    grid_config = dict()
    '''Minimum value for the x-axis'''
    grid_config['x_min'] = - 5
    '''Maximum value for the x-axis'''
    grid_config['x_max'] = + 5
    '''Step-size for the x-axis'''
    grid_config['x_step'] =  0.01# 0.1 for debuging
    '''Minimum value for the y-axis'''
    grid_config['y_min'] = 0
    '''Maximum value for the y-axis'''
    grid_config['y_max'] = + 5
    '''Step-size for the y-axis'''
    grid_config['y_step'] = 0.005# 0.1 for debuging

    print('\033[01m\033[31m\n\nSection 3: Delay-And-Sum\n\n\033[0m' + '*' * 80)

    print('''In this section, we plots three images using DAS beamforming:
- one using all transmits, TDMA data
- one using only one transmit, TDMA data
- one using all transmits, CDMA data''')


    '''TDMA images---------------------------------------------------------------------------------------------------------
    
    We make two images:
    - one using all transmits,
    - one using only one transmit.
    
    With all transmits'''

    '''Test: we add some noise to the data'''
    #tdma_data = tdma_data + np.random.normal(0,0.1,tdma_data.shape)

    tic = time.time()

    print('\n\033[01m\033[34mTDMA data, all transmits\033[0m\n')
    x_values, y_values, image = parallel_DAS_imaging_TDMA(
        grid_config = grid_config,
        rx_positions = rx_positions, 
        tx_positions = tx_positions, 
        tdma_data = tdma_data, 
        B = B, 
        fc = fc, 
        c = c,
        T_p = T_p, 
        N_t = N_t, 
        fs = fs,
        data_type = 'TDMA',
        hamming = False
    )
    
    toc = time.time()
    print(toc-tic,'s')
    
    eval_perf(image = image, x_values = x_values, y_values = y_values)

    
    plot_DAS_image(
        x_values = x_values,
        y_values = y_values,
        image = image,
        title = 'DAS beamforming image, TDMA data',
        path = 'images/question3/TDMA_DAS_image.pdf'
    )

    '''With only one transmit'''

    '''selected_tx: int, denotes the selected transmitter'''
    '''selected_rx: int, denotes the selected receiver'''
    selected_tx = 0
    selected_rx = 0

    print('\n\033[01m\033[34mTDMA data, one transmit\033[0m\n')
    x_values, y_values, image = parallel_DAS_imaging_TDMA(
        grid_config = grid_config,
        rx_positions = rx_positions,
        tx_positions = tx_positions[selected_tx][np.newaxis, np.newaxis], 
        tdma_data = tdma_data, 
        B = B, 
        fc = fc, 
        c = c,
        T_p = T_p, 
        N_t = N_t, 
        fs = fs,
        data_type = 'TDMA'
    )

    plot_DAS_image(
        x_values = x_values,
        y_values = y_values,
        image = image,
        title = f'''DAS beamforming image, TDMA data''',
        path = f'images/question3/TDMA_DAS_image_one_transmit_{selected_rx}_{selected_tx}.pdf'
    )


    '''CDMA images---------------------------------------------------------------------------------------------------------
    
    We make one image using CDMA data.'''

    print('\n\033[01m\033[34mCDMA data, all transmits\033[0m\n')
    x_values, y_values, image = parallel_DAS_imaging_TDMA(
        grid_config = grid_config,
        rx_positions = rx_positions, 
        tx_positions = tx_positions, 
        tdma_data = cdma_data, 
        B = B, 
        fc = fc, 
        c = c,
        T_p = T_p, 
        N_t = N_t, 
        fs = fs,
        data_type = 'CDMA',
    )

    plot_DAS_image(
        x_values = x_values,
        y_values = y_values,
        image = image,
        title = 'DAS beamforming image, CDMA data',
        path = 'images/question3/CDMA_DAS_image.pdf'
    )

    eval_perf(image = image, x_values = x_values, y_values = y_values)
    
   

    
    
    
                    











    
