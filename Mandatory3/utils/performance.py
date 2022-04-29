import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import sys

def eval_perf(image, x_values, y_values):


    '''This function evaluates the following metric for both x and y-axis:
    - Full Width Half Maximum measurement (FWHM), AKA the 3dB resolution'''
    
    '''First, we need to locate the point scatterer in the image. NOTE that
    if there are multiple point scatterers, we only consider the closest point
    scatterer to the top of the image.
    
    max_x_index: int, index of the point scatterer x-postion
    max_y_index: int, index of the point scatterer x-postion'''

    

    image = 20 * np.log10(np.abs(image) / np.max(np.abs(image)) + 1e-5)

    (max_y_index, max_x_index) = np.unravel_index(image.argmax(), image.shape)

    '''FWHM ------------------------------------------------------------------
    
    We compute the x and y FWHM.
    
    We select a slice of the data (containing the point scatterer) along the x-axis and
    we compute the x FWHM.'''

    x_data_slice = image[max_y_index, :]
    x_data_slice = scipy.signal.resample(x_data_slice,10000) 
    x_values = np.linspace(np.min(x_values), np.max(x_values), 10000)

    x_fwhm = eval_FWHM(data = x_data_slice, values = x_values)
    
    plt.figure()
    plt.plot(x_values,x_data_slice, color = 'r')
    plt.savefig('test0.pdf')

    plt.figure()
    plt.plot(x_values,x_data_slice, color = 'r')
    plt.ylim([-5, 0])
    plt.savefig('test1.pdf')
    

    '''We select a slice of the data (containing the point scatterer) along the x-axis and
    we compute the x FWHM.'''

    y_data_slice = image[:, max_x_index]
    y_data_slice = scipy.signal.resample(y_data_slice,10000) 
    y_values = np.linspace(np.min(y_values), np.max(y_values), 10000)
    y_fwhm = eval_FWHM(data = y_data_slice, values = y_values)

    plt.figure()
    plt.plot(y_values,y_data_slice, color = 'r')

    plt.savefig('test2.pdf')

    lambda_ = 340 / 15e3
    print(f'''
----------------------------------------------------------------------------------------------------------
|        Axis / Metric    |    FWHM (3dB resolution) (in mm)     |    FWHM (3dB resolution) (in lambda)  | 
|   Along-track (x-axis)  |               {x_fwhm * 1e3:.2f}                  |                 {x_fwhm / lambda_:.2f}                  |
|   Cross-track (y-axis)  |               {y_fwhm * 1e3:.2f}                  |                 {y_fwhm / lambda_:.2f}                  |
----------------------------------------------------------------------------------------------------------''')

    return x_fwhm, y_fwhm

def eval_FWHM(data, values):

    '''This function computes the Full Width Half Maximum measurement (FWHM), AKA the 3dB resolution
    in the following way: we start at the maximum index and while the value is superior to the maximum
    value / 2, we increased (+1, right side) / decreased (-1, left side) the index by one. 
    We do this for both left and right sides.
    
    Inputs:
    
    - data: np.array, the array of the sequence that we want to compute the FWHM. Should be a real sequence
    - values: np.array, the array of the x/y or t values
    
    Ouput:
    
    -fwhm: float, FWHM'''


    '''First, we get both the index of the maximum value, max_index, and the maximum value
    max_value.'''
    max_index = np.argmax(data)
    max_value = data[max_index]

    '''First, we compute the left 3dB main lobe width index denoted as left_3dB_ML_width_index.'''
    left_3dB_ML_width_index = max_index
    while data[left_3dB_ML_width_index] > max_value - 3:
        left_3dB_ML_width_index -= 1
        
    '''Then, we compute the right 3dB main lobe width index denoted as right_3dB_ML_width_index.'''
    right_3dB_ML_width_index = max_index
    while data[right_3dB_ML_width_index] > max_value - 3:
        right_3dB_ML_width_index += 1


    '''We compute the FWHM (for x positions) as FWHM = abs(x_max - left_3dB width) + abs(x_max - right_3dB width).'''
    fwhm = (
        abs(values[max_index] - values[left_3dB_ML_width_index]) + 
        abs(values[max_index] - values[right_3dB_ML_width_index])
        )

    '''We return the FWHM.'''

    return fwhm
