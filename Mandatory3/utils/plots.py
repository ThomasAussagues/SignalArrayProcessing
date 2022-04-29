''' IN5450 Mandatory exercise 3
Thomas Aussaguès, 05/04/2022
thomas.aussagues@imt-atlantique.net

This script contains functions to plot the results.'''



import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
from cmcrameri import cm
import numpy as np


cmap = cm.lajolla_r


def plot_cross_corr(up_chirp, down_chirp, T_p, fs, title, path):

    cross_corr = np.correlate(
        up_chirp / np.linalg.norm(up_chirp), 
        down_chirp / np.linalg.norm(down_chirp), 
        mode = 'full') 

    cross_corr = np.abs(cross_corr)
    max_value = np.max(cross_corr)
    
    

    plt.style.use(['science'])
    fig, ax = plt.subplots(1)
    time = np.linspace(-T_p, T_p, 2 * int(T_p * fs) - 1) * 1e3
    ax.plot(time,cross_corr, label = 'Cross-correlation')
    ax.plot(time, [max_value] * len(time), linestyle = 'dashed', label = f'$PCRR\\approx {max_value:.2f}$')
    ax.set_xlabel('Delay $\\tau$ (ms)')
    ax.set_ylabel('''$C_{xy}(\\tau)$''')
    ax.set_ylim([0,1])
    ax.legend(loc = 'best')
    ax.set_title(title)
    fig.savefig(path, dpi = 300)



def plot_chirp_stft(time, freq, stft, title, path):

    plt.style.use(['science'])

    fig, ax = plt.subplots(1)
    a = ax.imshow(stft, 
            vmin = - 60, 
            vmax = 0,
            cmap = cmap,
            extent = [0, len(time),0, len(freq)],
            origin = 'lower',
            aspect = 'auto')
    ax.set_xlabel('Time $t$ (ms)')
    ax.set_ylabel('Frequency $f$ (KHz)')
    
    x_labels = np.around(np.arange(np.min(time), np.max(time) + 2, 2),0)
    x_ticks = np.linspace(0, len(time), len(x_labels))
    y_labels = np.around(np.arange(np.min(freq), np.max(freq) + 5, 5),0)
    y_ticks = np.linspace(0, len(freq), len(y_labels))
    ax.set_xticks(x_ticks,x_labels)
    ax.set_yticks(y_ticks,y_labels)
    ax.set_ylim(int(len(freq) * (1 / 2)), int(len(freq) * (1 / 2 + 1 / 10)))
    c = fig.colorbar(a, orientation='vertical')
    c.set_label('Magnitude (dB)')
    ax.set_title(title)
    fig.savefig(path, dpi=300)
    plt.close()

def plot_after_before_pulse_compression(echo, pulse_compressed_signal,fs, title, path):

    plt.style.use(['science'])

    fig, axs = plt.subplots(2)
    ax1, ax2 = axs.flat

    normalized_pulse_compressed_signal = np.abs(pulse_compressed_signal)/np.max(np.abs(pulse_compressed_signal))
    normalized_echo = np.abs(echo)/np.max(np.abs(echo))

    ax1.plot(np.linspace(0, len(echo) / fs, len(echo)) * 1e3, normalized_echo ** 2)
    ax1.set_ylabel('''Echo 
    magnitude''')
    ax2.plot(np.linspace(0, len(echo) / fs, len(echo)) * 1e3, normalized_pulse_compressed_signal ** 2)
    ax2.set_ylabel('''Pulse compressed 
    signal magnitude''')
    ax2.set_xlabel('(1) Time $t$ (ms) (2) Delay $\\tau$ (ms)')
    fig.suptitle(title)
    fig.savefig(path, dpi=300)
    plt.close()

def plot_all_compressed_pulses(all_pulses, fs, title, path):

    
    fig, ax = plt.subplots(1)
    plt.style.use(['science'])

    epsilon = 1e-6
    normalized_compressed_pulses = np.abs(all_pulses)/np.max(np.abs(all_pulses))
    normalized_compressed_pulses[normalized_compressed_pulses < 1e-2] = epsilon
    a = ax.imshow(20*np.log10(normalized_compressed_pulses), cmap = cmap, alpha = 1, aspect = 'auto', vmin = -60, vmax = 0, interpolation = 'bicubic')
    ax.set_xticks(np.linspace(0, normalized_compressed_pulses.shape[1], 6))
    ax.set_xticklabels(np.linspace(0, normalized_compressed_pulses.shape[1] / fs, 6) * 1e3)
    c = fig.colorbar(a, orientation='vertical')
    c.set_label('Magnitude (dB)')
    ax.set_xlabel('Time $t$ (ms)')
    ax.set_ylabel('Receiver Rx')
    ax.set_title(title)
    fig.savefig(path, dpi=300)
    plt.close()

def plot_pulse_compressed_series_resolution(pulse_compressed_signal_channel_4_tdma_up, max_index, fs, left_3dB_ML_width, right_3dB_ML_width, title, path):

    
    plt.style.use(['science'])
    fig, axs = plt.subplots(1, 2, sharey = True)
    ax1, ax2 = axs.flat

    ax1.plot(np.linspace(0, len(pulse_compressed_signal_channel_4_tdma_up) / fs, len(pulse_compressed_signal_channel_4_tdma_up)) * 1e3, np.abs(pulse_compressed_signal_channel_4_tdma_up) / np.max(np.abs(pulse_compressed_signal_channel_4_tdma_up)))
    ax1.set_xlim([22.915 - 1,22.915 + 1])
    ax1.plot([max_index / fs * 1e3, max_index / fs * 1e3], [0, 1], linestyle = '--', color = 'r')
    ax1.annotate('$\\tau =$\n {:.2f}\n ms'.format(max_index / fs * 1e3),
         xy=(max_index / fs * 1e3, 1), xycoords='data',
         xytext=(+ 10, - 90), textcoords='offset points', fontsize=12,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=+.3"))

    ax2.plot(np.linspace(0, len(pulse_compressed_signal_channel_4_tdma_up) / fs, len(pulse_compressed_signal_channel_4_tdma_up)) * 1e3, np.abs(pulse_compressed_signal_channel_4_tdma_up) / np.max(np.abs(pulse_compressed_signal_channel_4_tdma_up)))
    ax2.set_xlim([22.915 - 0.25,22.915 + 0.25])
    ax2.set_ylim([0,1])
    ax2.arrow((left_3dB_ML_width + 1e-5) * 1e3, 0.5, (right_3dB_ML_width - left_3dB_ML_width - 1e-5) * 1e3, 0 ,width = 0.005, head_width = 0.01, head_length = 0.01,length_includes_head = True, ec ='r', color = 'r')
    ax2.arrow((right_3dB_ML_width - 1e-5) * 1e3, 0.5, - (right_3dB_ML_width - left_3dB_ML_width - 1e-5) * 1e3, 0 ,width = 0.005, head_width = 0.01, head_length = 0.01,length_includes_head = True, ec ='r', color = 'r')
    ax2.annotate('$\delta\\tau =$\n {:.2f}\n ms'.format((right_3dB_ML_width - left_3dB_ML_width) * 1e3),
         xy=(max_index / fs * 1e3, 0.5), xycoords='data',
         xytext=(+ 10, + 20), textcoords='offset points', fontsize=12,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-.3"))
    fig.supylabel('''Pulse compressed
    signal magnitude''', x = - 0.05)
    fig.supxlabel('Delay $\\tau$ (ms)', y = - 0.05)
    fig.suptitle(title, y = 1.05)
    plt.savefig(path, dpi = 300)
    plt.close()

def plot_rx_and_tx(tx, rx):

    plt.style.use(['science'])
    fig, ax = plt.subplots(1)
    ax.scatter(tx, [0] * len(tx), label = 'Tx positions', marker = 'd')
    ax.scatter(rx, [0] * len(rx), label = 'Rx positions', marker = '.')
    ax.set_xlabel('$x$ position (m)')
    ax.set_ylabel('$y$ position (m)')
    ax.set_title('Transmitter and receiver positions')
    ax.legend(loc = 'best')
    plt.savefig('images/question2/rx_and_tx_postions.pdf', dpi = 300)
    plt.close()

def plot_virtual_array(virtual_array_position, title, path):

    plt.style.use(['science'])
    fig, ax = plt.subplots(1)
    ax.scatter(virtual_array_position, [0] * len(virtual_array_position), label = '''Virtual elements 
    positions''', marker = '.')
    ax.set_xlabel('$x$ position (m)')
    ax.set_ylabel('$y$ position (m)')
    ax.set_title(title)
    ax.legend(loc = 'best')
    plt.savefig(path, dpi = 300)
    plt.close()

def plot_DAS_image(x_values, y_values, image, title, path):

        plt.style.use(['science'])
        fig, ax = plt.subplots(1)
        a = ax.imshow(20 * np.log10(np.abs(image)/np.max(np.abs(image)) + 1e-4), 
            vmin = - 60, 
            vmax = 0,
            cmap = cmap,
            origin = 'lower',
            extent = [0, len(x_values), 0, len(y_values)])
        # a = ax.pcolormesh(
        #     x_values, 
        #     y_values, 
        #     20 * np.log10(np.abs(image)/np.max(np.abs(image)) + 1e-4), 
        #     shading='gouraud', 
        #     vmin = - 60, 
        #     vmax = 0, 
        #     cmap = cmap,
        #     rasterized = True)
        ax.set_xlabel('$x$ position (m)')
        ax.set_ylabel('$y$ position (m)')
        ax.set_title(title)
        x_labels = np.around(np.arange(np.min(x_values), np.max(x_values) + 1, 1),0)
        x_ticks = np.linspace(0, len(x_values), len(x_labels))
        y_labels = np.around(np.arange(np.min(y_values), np.max(y_values) + 1, 1),0)
        y_ticks = np.linspace(0, len(y_values), len(y_labels))
        ax.set_xticks(x_ticks,x_labels)
        ax.set_yticks(y_ticks,y_labels)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("bottom", size="5%", pad=0.5)
        c = plt.colorbar(a, cax=cax, orientation='horizontal')
        ax.set_aspect('auto')
        #c = fig.colorbar(a, orientation='horizontal')
        c.set_label('Power (dB)')
        fig.savefig(path, dpi = 300)
        plt.close()




    