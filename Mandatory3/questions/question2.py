import matplotlib.pyplot as plt
import numpy as np
import scipy.io
from utils.plots import plot_rx_and_tx, plot_virtual_array
from utils.virtual_array import get_virtual_array_positions

# DeltaBeta = D / 2 / R
# DeltaX = D / 2
# DeltaY = c / (2 * B) 


def run_question_2():

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

    print('\033[01m\033[31m\n\nSection 2: Virtual array\n\n\033[0m' + '*' * 80)



    
    '''Physical and virtual arrays ------------------------------------------------------------------------------------'''
    print('\033[01m\033[31m\nArrays plots\033[0m ' + '*' * 80)
    print('''\nWe plot:
- the physical array, 
- the virtual array with all receivers and ONLY the leftmost transmitter,
- the virtual array with all receivers and ONLY the rightmost transmitter,
- the virtual array with all receivers and all transmitters.

See the plots in images/question2!''')
    '''We plot the physical array elements positions.'''
    plot_rx_and_tx(rx=rx_positions, tx=tx_positions)
    print(abs(rx_positions[-1]-rx_positions[0]))
    print(c / (B - fc/2) / 4 * 1e3)
    

    '''We plot the virtual array elements positions with all receivers and ONLY the leftmost transmitter.'''

    virtual_array_positions_left_tx = get_virtual_array_positions(tx_positions=tx_positions[0], rx_positions=rx_positions)
    
    plot_virtual_array(
        virtual_array_position = virtual_array_positions_left_tx, 
        title = '''Virtual array: left Tx and all Rx''',
        path = 'images/question2/virtual_array_left_tx.pdf')

    '''We plot the virtual array elements positions with all receivers and ONLY the rightmost transmitter.'''

    virtual_array_positions_right_tx = get_virtual_array_positions(tx_positions=tx_positions[1], rx_positions=rx_positions)

    print(f'''Virtual array with one transmitter and all receivers:
- NYQUIST criterion d <= lambda / 4 where lambda should be the minimum wavelength
- lambda = {c / (B - fc/2) * 1e3 :2f} mm 
- element spacing d = {abs(virtual_array_positions_right_tx[1]-virtual_array_positions_right_tx[0])[0] *1e3 :2f} mm
- The NYQUIST criterion is not fulfilled ! d = lambda / 4 = {c / (B - fc/2) / 4 * 1e3 :2f} mm
''')

    plot_virtual_array(
        virtual_array_position = virtual_array_positions_right_tx, 
        title = '''Virtual array: right Tx and all Rx''',
        path = 'images/question2/virtual_array_right_tx.pdf')

    '''We plot the virtual array elements positions with all receivers and all transmitters.'''

    virtual_array_positions_all_tx = np.sort(get_virtual_array_positions(tx_positions=tx_positions, rx_positions=rx_positions))
   
    print(f'''Virtual array with two transmitters and all receivers:
- NYQUIST criterion d < lambda / 4 where lambda should be the minimum wavelength
- lambda = {c / (B - fc/2) * 1e3:2f} mm 
- element spacing d = {abs(virtual_array_positions_all_tx[-2]-virtual_array_positions_all_tx[-1]) *1e3:2f} mm
- The NYQUIST criterion is fulfilled ! d < lambda / 4 = {c / (B - fc/2) / 4 * 1e3:2f} mm
''')

    plot_virtual_array(
        virtual_array_position = virtual_array_positions_all_tx, 
        title = '''Virtual array: all Tx and all Rx''',
        path = 'images/question2/virtual_array_all_tx.pdf')

    '''Resolutions -----------------------------------------------------------------------------------------------------'''
    print('\033[01m\033[31m\nResolutions\033[0m ' + '*' * 80)

    print('\n\033[01m\033[34mTheoretical lateral resolution deltaBeta\033[0m')
    print(f'''\nThe theoretical lateral resolution is given by the wavelength divided by the aperture length: 
deltaBeta = lambda / L.

Since we use a synthethic aperture, the length becomes 2 * L_{{sa}} where L_{{sa}} is the synthetic aperture length given
by the number of receivers multiplied by the element distance. 

Assuming that the element distance is equal to lambda / 4, we have : deltaBeta = lambda / (2 * lambda / 4 * N_t).
Therefore:

deltaBeta = 2 / N_t

    
Which frequency should we use? We take the minimum available frequency (fc - B / 2) such that we obtain the worst
possible lateral resolution. \033[01m\033[31mTherefore: f = {(fc - B/2) / 1e3 :.2f} kHz and the theoretical lateral resolution is:
    
                                deltaBeta = {c / (fc - B / 2) * (- np.min(rx_positions) + np.max(rx_positions)):.2f} rad\033[0m''')

    print('\n\033[01m\033[34mTheoretical lateral resolution (cross-track resolution) deltaX at a range of 4 m\033[0m')
    print(f'''\nThe theoretical lateral resolution in meter at a range R is given by deltaBeta * R. \033[01m\033[31mHence, in the worst case,
the theoretical lateral resolution is:

                                deltaX = {c / (fc - B / 2) * (- np.min(rx_positions) + np.max(rx_positions)) * 4 :.2f} m\033[0m''')

    print('\n\033[01m\033[34mTheoretical axial resolution (along-track resolution) deltaR\033[0m')
    print(f'''\nThe theoretical axial resolution in meter is given by c / (2 * B) where c is 
the sound speed and B the bandwitdth. \033[01m\033[31mTherefore, we the along track resolution is:

                                deltaR = {c / (2 * B) :.2f} m\033[0m''')



    


    



