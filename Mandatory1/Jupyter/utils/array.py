import numpy as np
import scipy
import scipy.signal


def array_pattern(positions,weights,values):

    array_pattern = np.zeros(len(values),dtype='complex')
    
    
    array_pattern = np.sum(np.exp(1j*np.matmul(positions[:,np.newaxis],values[np.newaxis,:]))*np.conj(weights[:,np.newaxis]),axis=0)

    
    #for i in range(len(values)):
        
        #array_pattern[i] = sum(weights[k]*np.exp(1j*values[i]*positions[k]) for k in range(len(positions)))
        
    return array_pattern

def get_lobes_positions(pattern,values):
    
    max_peaks = scipy.signal.find_peaks(pattern, height=None)
    min_peaks = scipy.signal.find_peaks(-pattern, height=None)
    
    # Main lobe level and main lobe position ##########################
    
    ML_center_index = np.argmax(pattern[100:len(pattern)-100])+100
    ML_position = values[ML_center_index]
    ML_level = pattern[ML_center_index]
    
    ####################################################################
    
    # Side lobes mean level and side lobes max level ###################
    SL_mean_level = 0
    SL_max_level = 0
    
    SL_levels = []
    for i in range(len(max_peaks[0])):
        
        SL_levels.append(pattern[max_peaks[0][i]])
        
    del SL_levels[len(SL_levels)//2]
    
    SL_max_level = np.max(SL_levels)
    SL_mean_level = np.mean(SL_levels)
    
    #####################################################################
    
    
    
    
    # Side lobes mean width #############################################
    
    
    SL_widths = []
    for i in range(len(min_peaks[0])-1) :
        SL_widths.append(values[min_peaks[0][i+1]]-values[min_peaks[0][i]])
    del SL_widths[len(SL_widths)//2]
   

    SL_mean_widths = np.mean(SL_widths)
    
    #######################################################################
   

            
    
    
    
    ML_level = pattern[ML_center_index]
    
    ML_3dB_index = ML_center_index
    
    
    try :

	    while pattern[ML_3dB_index] > ML_level-3 :

                ML_3dB_index += 1

    except :

        ML_3dB_index = ML_center_index

        while pattern[ML_3dB_index] > ML_level - 3:

            ML_3dB_index -= 1

    ML_3dB = pattern[ML_3dB_index]

    #####################################

    ML_6dB_index = ML_3dB_index
    
    try :

        while pattern[ML_6dB_index] > ML_level-6 :

            ML_6dB_index += 1

    except :

        ML_6dB_index = ML_3dB_index

        while pattern[ML_6dB_index] > ML_level - 6:

            ML_6dB_index -= 1


        
    ML_6dB = pattern[ML_6dB_index]
    
    params = {'ML position' : ML_position,
            'ML level' : ML_level,
            'ML 3 dB width' : 2*np.abs(values[ML_3dB_index]-ML_position),
            'ML 6 dB width' : 2*np.abs(values[ML_6dB_index]-ML_position),
            'SL max level' : SL_max_level,
            'SL mean level' : SL_mean_level,
            'SL mean widths' : SL_mean_widths}
        
        
    
    
        
    return params