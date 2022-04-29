import numpy as np

def get_virtual_array_positions(tx_positions : np.array, rx_positions : np.array):

    '''This function computes and returns the virtual array elements positions given the
    transmitters and receivers positions. NOTE that this function is designed to work with
    transmitters and receivers located along the x-axis (ie. y = 0).
    
    Inputs:
    - tx_positions: np.array, transmitters positions (m)
    - rx_positions: np.array, transmitters positions (m)
    
    Output:
    - virtual_array_positions: np.array, virtual array elements positions (m)'''

    '''First, we instanciate a list containing the virtual array elements positions.'''
    virtual_array_positions = list()

    '''If there is only one transmitter, then tx_positions is an array with shape (,). Hence, we convert it
    to an np.array with shape (1,1).'''
    if tx_positions.shape == ():
        tx_positions = tx_positions[np.newaxis, np.newaxis]

    '''For each receiver,'''    
    for rx_position in rx_positions:
        '''For each transmitter,'''
        for tx_position in tx_positions:
            '''We compute the virtual array element position as the middle of the segment between the
            transmitter and the receiver.'''
            virtual_array_positions.append((tx_position + rx_position) / 2)

    '''We return the virtual array elements positions.'''
    
    return virtual_array_positions