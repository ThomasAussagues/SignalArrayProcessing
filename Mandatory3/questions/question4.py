from utils.plots import plot_DAS_image
import numpy as np
import scipy.io
from utils.DAS_imaging import DAS_imaging_TDMA, DAS_imaging_CDMA
from utils.parallel_DAS_imaging import parallel_DAS_imaging_TDMA
import time
from utils.performance import eval_perf
import matplotlib.pyplot as plt

def run_question_4():

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

    grid_config = dict()
    grid_config['x_min'] = - 5
    grid_config['x_max'] = + 5
    grid_config['x_step'] =  0.01
    grid_config['y_min'] = 0
    grid_config['y_max'] = + 5
    grid_config['y_step'] = 0.01

    print('\033[01m\033[31m\n\nSection 4: Delay-And-Sum\n\n\033[0m' + '*' * 80)

    print('''In this section, we plots three images using DAS beamforming:
- one using all transmits, TDMA data
- one using only one transmit, TDMA data
- one using all transmits, CDMA data''')


    '''TDMA images---------------------------------------------------------------------------------------------------------
    
    We make two images:
    - one using all transmits,
    - one using only one transmit.
    
    With all transmits'''


    print('\n\033[01m\033[34mTDMA data, all transmits + HAMMING window\033[0m\n')
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
        hamming = True
    )
    
    # print(eval_perf(image = image, x_values = x_values, y_values = y_values))

    plot_DAS_image(
        x_values = x_values,
        y_values = y_values,
        image = image,
        title = '''DAS beamforming image, TDMA data
        Hamming window''',
        path = 'images/question4/TDMA_DAS_image_HAMMING.pdf'
    )

    eval_perf(image = image, x_values = x_values, y_values = y_values)

    # '''With only one transmit'''

    '''selected_tx: int, denotes the selected transmitter'''
    '''selected_rx: int, denotes the selected receiver'''
    selected_tx = 0
    selected_rx = 0

    print('\n\033[01m\033[34mTDMA data, one transmit + HAMMING\033[0m\n')
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
        data_type = 'TDMA',
        hamming = True
    )

    plot_DAS_image(
        x_values = x_values,
        y_values = y_values,
        image = image,
        title = f'''DAS beamforming image, TDMA data''',
        path = f'images/question4/TDMA_DAS_image_one_transmit_{selected_rx}_{selected_tx}_HAMMING.pdf'
    )


    '''CDMA images---------------------------------------------------------------------------------------------------------
    
    We make one image using TDMA data and the virtual array positions.'''

    print('\n\033[01m\033[34mTDMA data + the virtual array position\033[0m\n')
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
        hamming = False,
        virtual_array = True
    )

    plot_DAS_image(
        x_values = x_values,
        y_values = y_values,
        image = image,
        title = 'DAS beamforming image, TDMA data',
        path = 'images/question4/TDMA_DAS_image_virtual_array.pdf'
    )

    eval_perf(image = image, x_values = x_values, y_values = y_values)
    
   

    
    
    
                    











    
