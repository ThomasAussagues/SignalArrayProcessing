import numpy as np


def custom_fft2(input_):
    
    return np.fft.fftshift(np.fft.fft2(np.fft.fftshift(input_)))


def custom_ifft2(input_):
    
    return np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(input_)))