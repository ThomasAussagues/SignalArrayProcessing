''' IN5450 Mandatory exercise 3
Thomas Aussaguès, 05/04/2022
thomas.aussagues@imt-atlantique.net

This script contains functions to perform DAS beamforming with TDMA and CDMA.'''



import numpy as np
from utils.pulse_compression import run_pulse_compression
from utils.generate_pulse import lfm_pulse
from tqdm import tqdm

def DAS_imaging_TDMA(
    grid_config : dict, 
    rx_positions : np.array, 
    tx_positions : np.array, 
    tdma_data : np.array, 
    B : float, 
    fc : float,
    c : float, 
    T_p : float, 
    N_t : float, 
    fs : float
    ) -> np.array:

        '''This function computes and returns an image using DAS beamforming for TDMA data.
        
        Inputs:
        
        - grid_config : dict, a dict for the grid parameters
        - tx_positions: np.array, transmitters positions (m)
        - rx_positions: np.array, transmitters positions (m)
        - tdma_data   : np.array, array containing the TDMA data. Should have shape (N_t, N_tx, N_rx)
        - B           : float, bandwidth (Hz)
        - fc          : float, center frequency (Hz)
        - c           : float, speed of sound (m/s)
        - T_p         : float, pulse duration (s)
        - N_t         : int, number of time samples 
        - fs          : float, sampling frequency (Hz)
        
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

        '''We generate an UP LFM pulse using the given parameters (bandwidth, cetenr frequency, duration and
        sampling frequency.'''
        up_pulse = lfm_pulse(B = B, f_c = fc, T_p = T_p, fs = fs)

        '''Then, we apply the DAS beamforming algorithm.'''
        
        '''We get both the numbers of transmitters and receivers.'''
        N_rx = len(rx_positions)
        N_tx = len(tx_positions)

        '''For each receiver (note that we add tqdm to have a progress bar. We access the receiver through its index.'''
        for n_rx in tqdm(range(N_rx)):
            '''For each transmitter. We access the receiver through its index.'''
            for n_tx in range(N_tx):
            
                '''We select the echo corresponding to the current transmitter/receiver couple.'''
                echo = tdma_data[:, n_rx, n_tx]
                '''Then, we apply the match filter (as done in section one).'''
                compressed_pulse = run_pulse_compression(ping = up_pulse, echo = echo)
                '''We also instanciate a temporary image, tmp_image, to store the results for the 
                current transmitter/receiver couple. NOTE that tmp_image is a complex np.array
                of shape (n_x, n_y).'''
                tmp_image = np.zeros_like(image, dtype = 'complex')
                '''We get the positions for the current transmitter/receiver couple.'''
                tx_pos = tx_positions[n_tx]
                rx_pos = rx_positions[n_rx]

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
                '''(End of the pixel loops) Finally, we add the temporaty image to the final one.'''
                image += tmp_image
        '''(End of the transmitters and receivers loops) We return the transposed image (to have x-axis below and 
        y-axis at the left) and the x and y values.'''

        return x_values, y_values, image.T


def DAS_imaging_CDMA(
    grid_config : dict, 
    rx_positions : np.array, 
    tx_positions : np.array, 
    cdma_data : np.array, 
    B : float, 
    fc : float,
    c : float, 
    T_p : float, 
    N_t : float, 
    fs : float
    ) -> np.array:

        '''This function computes and returns an image using DAS beamforming for TDMA data.
        
        Inputs:
        
        - grid_config : dict, a dict for the grid parameters
        - tx_positions: np.array, transmitters positions (m)
        - rx_positions: np.array, transmitters positions (m)
        - cdma_data   : np.array, array containing the CDMA data. Should have shape (N_t, N_rx)
        - B           : float, bandwidth (Hz)
        - fc          : float, center frequency (Hz)
        - c           : float, speed of sound (m/s)
        - T_p         : float, pulse duration (s)
        - N_t         : int, number of time samples 
        - fs          : float, sampling frequency (Hz)
        
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

        '''We generate an UP LFM pulse using the given parameters (bandwidth, cetenr frequency, duration and
        sampling frequency.'''
        up_pulse = lfm_pulse(B = B, f_c = fc, T_p = T_p, fs = fs)
        '''We generate an DOWN LFM pulse using the given parameters (bandwidth, cetenr frequency, duration and
        sampling frequency.'''
        down_pulse = lfm_pulse(B = - B, f_c = fc, T_p = T_p, fs = fs)
        
        pulses = [down_pulse, up_pulse]
        '''Then, we apply the DAS beamforming algorithm.'''
        
        '''We get both the numbers of transmitters and receivers.'''
        N_rx = len(rx_positions)
        N_tx = len(tx_positions)

        for n_tx in range(N_tx):
            
            pulse = pulses[n_tx]
            tx_pos = tx_positions[n_tx]

            '''For each transmitter. (note that we add tqdm to have a progress bar). We access the receiver through its index.'''
            for n_rx in tqdm(range(N_rx)):
            
                '''We select the echo corresponding to the current receiver.'''
                echo = cdma_data[:, n_rx]
                '''Then, we apply the match filter (as done in section one) using the UP LFM pulse.'''
                compressed_pulse = run_pulse_compression(ping = pulse, echo = echo)
                '''We also instanciate a temporary image, tmp_image, to store the results for the 
                current transmitter/receiver couple. NOTE that tmp_image is a complex np.array
                of shape (n_x, n_y).'''
                tmp_image = np.zeros_like(image, dtype = 'complex')
                '''We get the positions for the current transmitter/receiver couple.'''
                rx_pos = rx_positions[n_rx]

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
                            '''We add the value from the pulsed compressed time series to the corresponding pixel. Since
                            the waveforms are orthogonal either the up compressed pulse is non null or the down is 
                            non null.'''
                            tmp_image[j, k] += compressed_pulse[index_delay]
                '''(End of the pixel loops) Finally, we add the temporaty image to the final one.'''
                image += tmp_image
        '''(End of the transmitters and receivers loops) We return the transposed image (to have x-axis below and 
        y-axis at the left) and the x and y values.'''

        return x_values, y_values, image.T