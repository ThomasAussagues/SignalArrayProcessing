from utils.generate_pulse import lfm_pulse
from utils.fourier_analysis import sfft as custom_stft
from utils.plots import plot_chirp_stft, plot_after_before_pulse_compression, plot_all_compressed_pulses, plot_cross_corr, plot_pulse_compressed_series_resolution
from utils.pulse_compression import run_pulse_compression
import matplotlib.pyplot as plt
import numpy as np
import scipy.io

def run_question_1():


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
    tx_positions = matlab_data['tx_pos']
    '''Receivers positions (in m)'''
    rx_positions = matlab_data['rx_pos']
    '''tdma_data'''
    tdma_data = matlab_data['tdma_data']

    print('\033[01m\033[31m\n\nSection 1: Pulse compression\n\n\033[0m' + '*' * 80)
    print(fc)
    print('\033[01m\033[31m\nPlots \033[0m' + '*' * 80)

    print('''\nIn this section, we make the following plots:
- Cross-correlation between the UP and DOWN chirps
- LFM UP chirp STFT;
- LFM DOWN chirp STFT;
- After/before pulse compression for CDMA data and LFM UP chirp;
- After/before pulse compression for CDMA data and LFM DOWN chirp;
- All compressed pulses as a 2D images for CDMA data;
- After/before pulse compression for TDMA data and LFM UP chirp;
- All compressed pulses as a 2D images for TDMA data;
- A plot to investigate time resolution.''')


    '''Then, we can generate both UP and DOWN LFM pulses using the previously described
    parameters.'''
    
    '''UP'''

    up_pulse = lfm_pulse(B = B, f_c = fc, T_p = T_p, fs = fs)

    '''DOWN'''
    down_pulse = lfm_pulse(B = - B, f_c = fc, T_p = T_p, fs = fs)
    
    '''We plot the cross-correlation between the two chirps. We want to check that they are orthogonal.'''

    plot_cross_corr(
        up_chirp = up_pulse, 
        down_chirp = down_pulse, 
        T_p = T_p,
        fs = fs,
        title = 'Normalized cross-correlation',
        path = 'images/question1/cross_corr_plot.pdf')
    
    '''Here, for both pulses, we compute and plot the Short Time Fourier Transform to check that everything is 
    working. The STFT is computed using the following parameters:
    - Segment length L = 256
    - Overlap D = 32
    '''

    '''UP'''

    time_up, freq_up, up_pulse_stft = custom_stft(data = up_pulse.T , L = 512, D = 32, fs = fs, zero_padding_factor = 4)


    plot_chirp_stft(
        time_up * 1e3,
        freq_up / 1e3, 
        10*np.log10(up_pulse_stft/np.max(up_pulse_stft)), 
        '''LFM upchirp STFT''', 
        'images/question1/lfm_up_stft.pdf')

    '''DOWN'''

    time_down, freq_down, down_pulse_stft = custom_stft(data = down_pulse.T , L = 512, D = 32, fs = fs, zero_padding_factor = 4)

    plot_chirp_stft(
        time_down * 1e3,
        freq_down / 1e3, 
        10*np.log10(down_pulse_stft/np.max(down_pulse_stft)), 
        '''LFM downchirp STFT''', 
        'images/question1/lfm_down_stft.pdf'
        )

    '''
    
    CDMA DATA ----------------------------------------------------------------------------------------------------

    Here, we choose to run pulse compression on the 4-th channel. The leftmost transmitter uses a 
    LFM donwchirp whereas the rightmost uses LFM upchirp.'''

    '''Receiver index (true index - 1)'''
    rx_channel = 3
    '''Transmitter index (true index - 1)'''
    tx_channel = 0

    pulse_compressed_signal_cdma_down = run_pulse_compression(ping = down_pulse, echo = cdma_data[:, rx_channel])
    pulse_compressed_signal_cdma_up = run_pulse_compression(ping = up_pulse, echo = cdma_data[:, rx_channel])

    plot_after_before_pulse_compression(
        echo = cdma_data[:, rx_channel], 
        pulse_compressed_signal = pulse_compressed_signal_cdma_down, 
        fs = fs,
        title = f'''Pulse before and after match filtering, 
        CDMA data, channel {rx_channel + 1}, LFM donwchirp''',
        path = 'images/question1/plot_after_before_pulse_compression_cdma_channel_{}_downchirp.pdf'.format(rx_channel + 1)
        )

    plot_after_before_pulse_compression(
        echo = cdma_data[:, 3], 
        pulse_compressed_signal = pulse_compressed_signal_cdma_up, 
        fs = fs,
        title = f'''Pulse before and after match filtering, 
        CDMA data, channel {rx_channel + 1}, LFM upchirp''',
        path = 'images/question1/plot_after_before_pulse_compression_cdma_channel_{}_upchirp.pdf'.format(rx_channel + 1)
        )

    '''We make a plot of all compressed pulses to see whether the DOA is null or not. To do so,
    we run the match filter on all the N_rx = 32 recevided echos. '''

    '''We create a list all_compressed_pulses which will store all the compressed pulses.'''
    all_compressed_pulses = list()
    
    for i in range(N_rx):
        '''We run the match filter on the i-th received echo.'''
        pulse_compressed_series = run_pulse_compression(ping = up_pulse, echo = cdma_data[:,i])
        + run_pulse_compression(ping = down_pulse, echo = cdma_data[:,i])
        '''We append the computed time series in the list all_compressed_pulses.'''
        all_compressed_pulses.append(pulse_compressed_series)
    
    '''We transform the list all_compressed_pulses into an np.array.'''
    all_compressed_pulses = np.array(all_compressed_pulses)

    plot_all_compressed_pulses(
        all_pulses = all_compressed_pulses,
        fs = fs,
        title = '''Compressed pulses along the 
        $N_{Rx} = 32$ receivers, LFM upchirp''',
        path = 'images/question1/cdma_all_compressed_pulses.pdf'
        )

    '''TDMA DATA ----------------------------------------------------------------------------------------------------'''

    '''Here, we choose to run pulse compression on the 4-th channel for the signal transmitted by the left
    transducer (index N_{tx} = 0). Both left and rigth transmitters use a 
    LFM upchrirp. '''

    pulse_compressed_signal_channel_4_tdma_up = run_pulse_compression(ping = up_pulse, echo = tdma_data[:, rx_channel, tx_channel])
    
    plot_after_before_pulse_compression(
        echo = tdma_data[:, rx_channel, tx_channel], 
        pulse_compressed_signal = pulse_compressed_signal_channel_4_tdma_up, 
        fs = fs,
        title = f'''Pulse compression, TDMA data''',
        path = 'images/question1/plot_after_before_pulse_compression_tdma_channel_{}_{}_upchirp.pdf'.format(rx_channel + 1, tx_channel + 1)
        )

    '''We make a plot of all compressed pulses to see whether the DOA is null or not. To do so,
    we run the match filter on all the N_rx = 32 recevided echos. We run the experiment two times:
    one for the LFM upchirp and one for the LFM downchirp.'''

    '''We create a list all_compressed_pulses which will store all the compressed pulses.'''
    all_compressed_pulses = list()
    
    for i in range(N_rx):
        '''We run the match filter on the i-th received echo.'''
        pulse_compressed_series = run_pulse_compression(ping = up_pulse, echo = tdma_data[:, i, 0])
        '''We append the computed time series in the list all_compressed_pulses.'''
        all_compressed_pulses.append(pulse_compressed_series)
    
    '''We transform the list all_compressed_pulses into an np.array.'''
    all_compressed_pulses = np.array(all_compressed_pulses)

    plot_all_compressed_pulses(
        all_pulses = all_compressed_pulses,
        fs = fs,
        title = '''All compressed pulse, TDMA''',
        path = 'images/question1/tdma_all_compressed_pulses_upchirp_{}.pdf'.format(tx_channel + 1),
        )

    '''Time resolution of the pulse compressed series.-------------------------------------------------------------------'''
    fig, axs = plt.subplots(1, 2, sharey = True)
    ax1, ax2 = axs.flat

    max_index = np.argmax(np.abs(pulse_compressed_signal_channel_4_tdma_up))
    max_value = np.abs(pulse_compressed_signal_channel_4_tdma_up)[max_index]
    left_3dB_ML_width_index = max_index
    while np.abs(pulse_compressed_signal_channel_4_tdma_up)[left_3dB_ML_width_index] > max_value / 2:
        left_3dB_ML_width_index -= 1

    right_3dB_ML_width_index = max_index
    while np.abs(pulse_compressed_signal_channel_4_tdma_up)[right_3dB_ML_width_index] > max_value / 2:
        right_3dB_ML_width_index += 1
    
    left_3dB_ML_width = left_3dB_ML_width_index / fs
    right_3dB_ML_width = right_3dB_ML_width_index / fs
    

    plot_pulse_compressed_series_resolution(
        pulse_compressed_signal_channel_4_tdma_up=pulse_compressed_signal_channel_4_tdma_up,
        max_index = max_index,
        fs = fs,
        left_3dB_ML_width = left_3dB_ML_width,
        right_3dB_ML_width = right_3dB_ML_width,
        title = f'''Pulse compressed time series pratical resolution
        $N_{{tx}} = {tx_channel + 1}$, $N_{{rx}} = {rx_channel + 1}$, TDMA data''',
        path = 'images/question1/pulse_compressed_time_resolution_{}_{}.pdf'.format(tx_channel + 1,rx_channel + 1)
    )
   ###### TOTAL WIDTH compressed pulse = 2 * signal length (non null)

    print('\033[01m\033[31m\nResolution \033[0m' + '*' * 80)

    print('''\nThe theoretical time resolution is given by 1/B where B is the bandwidth. Therefore,
\033[01m\033[31mthe theoretical time resolution is {:.2f} ms\033[0m'''.format(1 / B * 1e3))
    print('''\nWe assume that the pratical time resolution can be approximated by the pulse compressed time 
series main lobe width (at 3 dB). Hence, \033[01m\033[31mthe pratical time resolution is: {:.2f} ms\033[0m'''.format((right_3dB_ML_width - left_3dB_ML_width) * 1e3))



    
   
