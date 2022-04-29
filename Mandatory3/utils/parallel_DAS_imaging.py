''' IN5450 Mandatory exercise 3
Thomas Aussaguès, 05/04/2022
thomas.aussagues@imt-atlantique.net

This script contains functions to perform DAS beamforming with TDMA and CDMA data using 
parallel computing.'''


import numpy as np
from utils.pulse_compression import run_pulse_compression
from utils.generate_pulse import lfm_pulse
import concurrent.futures
from typing import Tuple
from tqdm import tqdm
from utils.virtual_array import get_virtual_array_positions

def tdma_sequence_generator(tdma_data : np.array, hamming : bool, data_type : str) -> np.array:

    '''This generator returns the TDMA time series.
    
    Input:
    
    - tdma          : np.array, an array containing the TDMA time series. Should have shape (N_t, N_rx, N_tx)
    - hamming       : boolean, if True, we apply an hamming window to the data
    - data_type     : str, 'TDMA' or 'CDMA'

    Output:

    - np.array, an array containing one TDMA time series for given transmitter and receiver'''

    '''We get the number of the time samples N_t'''
    N_t = tdma_data.shape[0]
    '''We get the number of receivers N_rx and transmitters N_tx.'''
    N_rx = tdma_data.shape[1]
    '''The third dimension only exists if we use TDMA data. For CDMA data, we set N_tx to one'''
    if data_type == 'TDMA':
        N_tx = tdma_data.shape[2]
    elif data_type == 'CDMA':
        N_tx = 1
    
    if data_type == 'TDMA':
        '''We return each TDMA time series.'''
        for n_rx in range(N_rx):
            for n_tx in range(N_tx):
                if hamming :
                    yield tdma_data[:, n_rx, n_tx]
                else :
                    yield tdma_data[:, n_rx, n_tx] * np.hamming(N_t)
    
    elif data_type == 'CDMA':
        for n_rx in range(N_rx):
            if hamming :
                yield tdma_data[:, n_rx]
            else :
                yield tdma_data[:, n_rx] * np.hamming(N_t)

def rx_tx_virtual_array_index_generator(N_rx : int, N_tx : int) -> int:

    '''This generator returns the index of the transmitter/receiver.
    
    Inputs:
    
    - N_rx: int, number of receivers
    - N_tx: int, number of transmitters

    Output:

    - int, receiver index'''

    '''We return the receiver index.'''
    for i in range(N_rx * N_tx):
        yield i



def rx_index_generator(N_rx : int, N_tx : int) -> int:

    '''This generator returns the index of the receivers in the following way:
    0 N_tx times, 1 N_tx times ... N_rx N_tx times <=> 0 0 1 1 2 2 ... 31 31
    
    Inputs:
    
    - N_rx: int, number of receivers
    - N_tx: int, number of transmitters

    Output:

    - int, receiver index'''

    '''We return the receiver index.'''
    for i in range(N_rx):
        for _ in range(N_tx):
            yield i

def tx_index_generator(N_rx : int, N_tx : int) -> int:

    '''This generator returns the index of the transmitters in the following way:
    0 N_tx times, 1 N_tx times ... N_rx N_tx times <=> 0 0 1 1 2 2 ... 31 31
    
    Inputs:
    
    - N_rx: int, number of receivers
    - N_tx: int, number of transmitters

    Output:

    - int, receiver index'''

    '''We return the transmitter index.'''
    for _ in range(N_rx):
        for i in range(N_tx):
            yield i




def compute_image(
    tdma_data : np.array, 
    up_pulse : np.array, 
    tx_pos : float, 
    rx_pos : float, 
    x_values : np.array, 
    y_values : np.array,
    c : float,
    fs : float,
    hamming = False
    ) -> np.array :

    '''This function computes and return an temporary image for a given transmitter/receiver couple.
    
    Inputs:
        
    - tdma_data   : np.array, an np.array of shape N_t containing one time series corresponding to the chosen
    transmitter / receiver couple
    - up_pulse    : np.array, an array containing the UP LFM pulse used for the pulse compression
    - tx_pos      : float, the positon of the transmitter (m)
    - rx_pos      : float, the positon of the receiver (m)
    - x_values    : np.array, contains the x-postions values (m)
    - y_values    : np.array, contains the y-postions values (m)
    - B           : float, bandwidth (Hz)
    - c           : float, speed of sound (m/s)
    - fs          : float, sampling frequency (Hz)
    - hamming     : boolean, if True, we apply an hamming window to the LFM pulse
        
    Output:
    
    - tmp_image   : np.array, the generated image for the given transmitter / receiver couple'''
    
  
    '''Then, we apply the match filter (as done in section one).'''
    compressed_pulse = run_pulse_compression(ping = up_pulse * np.hamming(len(up_pulse)), echo = tdma_data)
    '''We get the number of x, n_x, and y, n_y, positions.'''
    n_x = len(x_values)
    n_y = len(y_values)
    '''Then, we instanciate a temporary image, tmp_image, to store the results for the 
    current transmitter/receiver couple. NOTE that tmp_image is a complex np.array
    of shape (n_x, n_y).'''
    tmp_image = np.zeros((n_x, n_y), dtype = 'complex')
    '''We get the length of the time series / the number of time samples N_t.'''
    N_t = tdma_data.shape[0]

    '''Then, we iterate through the pixel of the image.'''
    '''For each x-pixel. We access the x-pixel through its index.'''
    for j in range(n_x):
        '''For each y-pixel. We access the y-pixel through its index.'''
        for k in range(n_y):

            '''We get the correspoding positions in meters.'''
            pixel_x_pos = x_values[j]
            pixel_y_pos = y_values[k]
            '''
            Then, we compute two distances:
            - tx_to_pixel_distance: the distance between the transmitter and the pixel,
            - rx_to_pixel_distance: the distance between the receiver and the pixel.
            NOTE the we assume the transmitters and receivers to be along the x-axis.
            '''
            tx_to_pixel_distance = np.sqrt((pixel_x_pos - tx_pos) ** 2 + pixel_y_pos ** 2)
            rx_to_pixel_distance = np.sqrt((pixel_x_pos - rx_pos) ** 2 + pixel_y_pos ** 2)
            '''We compute the corresponding time delay using the speed of sound c.'''           
            time_delay = (tx_to_pixel_distance + rx_to_pixel_distance) / c
            '''We convert this time delay into an index using the nearest neighbour interpolation
            method.'''
            index_delay = int(time_delay * fs)
            '''We work only with delays that are inferior to the total number of time samples N_t'''
            if index_delay < N_t:
                '''We add the value from the pulsed compressed time series to the corresponding pixel.'''
                tmp_image[j, k] += compressed_pulse[index_delay]

    '''We return the temporary image.'''
    
    return tmp_image

def parallel_DAS_imaging_TDMA(
    grid_config : dict, 
    rx_positions : np.array, 
    tx_positions : np.array, 
    tdma_data : np.array, 
    B : float, 
    fc : float,
    c : float, 
    T_p : float, 
    N_t : float, 
    fs : float,
    data_type : str,
    virtual_array = False,
    hamming = False,
    ) -> Tuple[np.array, np.array, np.array]:

    '''This function computes and returns an image using DAS beamforming for TDMA data.
    
    Inputs:
    
    - grid_config   : dict, a dict for the grid parameters
    - tx_positions  : np.array, transmitters positions (m)
    - rx_positions  : np.array, transmitters positions (m)
    - tdma_data     : np.array, array containing the TDMA data. Should have shape (N_t, N_tx, N_rx)
    - B             : float, bandwidth (Hz)
    - fc            : float, center frequency (Hz)
    - c             : float, speed of sound (m/s)
    - T_p           : float, pulse duration (s)
    - N_t           : int, number of time samples 
    - fs            : float, sampling frequency (Hz)
    - virtual_array :  boolean, if True, we use a virtual array constructed from tx_positions and rx_positions
    - hamming       : boolean, if True, we apply an hamming window to the data
    - data_type     : str, 'TDMA' or 'CDMA'
    
    Output:

    - x_values   : np.array, contains the x-postions (m)
    - y_values   : np.array, contains the y-postions (m)
    - image      : np.array, computed image'''

    '''We create an np.array of x values using the grid_config dict.'''
    x_values = np.arange(grid_config['x_min'],  grid_config['x_max'], grid_config['x_step'])
    '''We get the number of x points.'''
    n_x = len(x_values)
    '''We create an np.array of y values using the grid_config dict.'''
    y_values = np.arange(grid_config['y_min'],  grid_config['y_max'], grid_config['y_step'])
    '''We get the number of y points.'''
    n_y = len(y_values)
    
    '''We instanciate the output image as an np.array of shape (n_x, n_y) fill with zeros.
    NOTE that image is a complex np.array.'''
    image = np.zeros((n_x, n_y), dtype = 'complex')

    '''We generate an UP/DOWN LFM pulse using the given parameters (bandwidth, cetenr frequency, duration and
    sampling frequency.'''

    up_pulse = lfm_pulse(B = B, f_c = fc, T_p = T_p, fs = fs)

    if data_type == 'CDMA':
        down_pulse = lfm_pulse(B = -B, f_c = fc, T_p = T_p, fs = fs)
        if hamming:
            down_pulse *= np.hamming(len(down_pulse))

    elif data_type == 'TDMA':
        up_pulse = lfm_pulse(B = B, f_c = fc, T_p = T_p, fs = fs)
        if hamming:
            up_pulse *= np.hamming(len(up_pulse))
        
        
    '''Then, we apply the DAS beamforming algorithm.'''
    
    '''We get both the numbers of transmitters N_tx and receivers N_rx.'''
    N_rx = len(rx_positions)
    N_tx = len(tx_positions)

    '''We compute the number of transmitter / receiver couples N'''
    N = N_rx * N_tx

    

    if virtual_array :

        virtual_array_pos = get_virtual_array_positions(tx_positions = tx_positions, rx_positions = rx_positions)
        
        N = len(virtual_array_pos)

    '''We instanciate 3 generators:
    - rx_index_generator_      : the receiver index generator
    - tx_index_generator_      : the tranmistter index generator
    - tdma_sequence_generator_ : the TDMA time series generator'''
    rx_index_generator_ = rx_index_generator(N_rx, N_tx)
    tx_index_generator_ = tx_index_generator(N_rx, N_tx)
    tdma_sequence_generator_ = tdma_sequence_generator(tdma_data=tdma_data, hamming = hamming, data_type = data_type)

    '''NOTE: PARALLELIZATION -----------------------------------------------------------------------------------------'''

    with concurrent.futures.ProcessPoolExecutor(10) as executor:

        print(f'Number of parallel threads: {executor._max_workers}')

        if hamming:
            print('** We apply an Hamming window. **')

        if data_type == 'CDMA':
            print('** We use CDMA data. **')

            '''We run the process two times: one for the leftmost transmitter with the DOWN LFM pulse
            and one  for the rightmost transmitter with the UP LFM pulse.'''

            '''Down / Leftmost'''
            results1 = list(tqdm(executor.map(
            compute_image,
            [next(tdma_sequence_generator_) for _ in range(N_rx)],
            [down_pulse] * N_rx,
            [tx_positions[0]] * N_rx,
            rx_positions,
            [x_values] * N_rx , 
            [y_values] * N_rx,
            [c] * N_rx,
            [fs] * N_rx),total = N_rx
            ))

            '''We create a new generator because we iterated through the entire previous generator.'''

            tdma_sequence_generator_ = tdma_sequence_generator(tdma_data=tdma_data, hamming = hamming, data_type = data_type)

            '''Up / Rightmost'''
            results2 = list(tqdm(executor.map(
            compute_image,
            [next(tdma_sequence_generator_) for _ in range(N_rx)],
            [up_pulse] * N_rx,
            [tx_positions[1]] * N_rx,
            rx_positions,
            [x_values] * N_rx , 
            [y_values] * N_rx,
            [c] * N_rx,
            [fs] * N_rx),total = N_rx
            ))

            results = list(results1) + list(results2)

        elif data_type == 'TDMA':

            print('** We use TDMA data. **')

            if virtual_array:
                print('** We use the virtual array. **')

                results = list(tqdm(executor.map(
                compute_image,
                [next(tdma_sequence_generator_) for _ in range(N)],
                [up_pulse] * N,
                [virtual_array_pos[i] for i in range(N)],
                [virtual_array_pos[i] for i in range(N)],
                [x_values] * N , 
                [y_values] * N,
                [c] * N,
                [fs] * N),total = N
                ))

            else :
                results = list(tqdm(executor.map(
                compute_image,
                [next(tdma_sequence_generator_) for _ in range(N)],
                [up_pulse] * N,
                [tx_positions[next(tx_index_generator_)] for _ in range(N)],
                [rx_positions[next(rx_index_generator_)] for _ in range(N)],
                [x_values] * N , 
                [y_values] * N,
                [c] * N,
                [fs] * N),total = N
                ))

    '''---------------------------------------------------------------------------------------------------------------''' 
        

    '''We sum all the computed images'''
    for result in results:
        image += result

    '''(End of the transmitters and receivers loops) We return the transposed image (to have x-axis below and 
        y-axis at the left) and the x and y values.'''

    return x_values, y_values, image.T