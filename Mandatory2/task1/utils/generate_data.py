
# Generate 2 signals in noise according to page 73 of 
# H. Krim, M. Viberg, "Two decades of array signal processing research
# - The parametric approach," IEEE Signal Processing Magazine, pp.67-94,
# July 1996.

# Note that definition of direction of arrival (DOA) is different from that
# of Krim and Viberg in that 0 degrees is normal incidence

# Written by:
# S. Holm, Department of Informatics, University of Oslo
# 31. Oct 1997 First version 
# 21. Nov 1997 Corrected for noise in imaginary part 21. November 1997
# 12. Dec 1997 Added random phase noise to signals to better ensure incoherence

import numpy as np


def generate_data(name:str,config:dict) -> None :

    # We fix the numpy seed to ensure that all sources are subject to the same noise
    np.random.seed(config['seed'])
    # Number of time samples
    N = config['N']
    # number of sensors
    M = config['M']
    # Source 1 SNR (in dB)
    SNR1 = config['SNR1']
    # Source 2 SNR (in dB)
    SNR2 = config['SNR2']
    # Source 1 direction of arrival (degrees)
    theta1 = config['theta1']
    # Source 2 direction of arrival (degrees)
    theta2 = config['theta2']
    # Phase shift between the the two sources (degrees)
    gamma  = config['gamma']
    # Array element spacing 
    d = config['d']
    # Normalized wavenumber
    k = config['k']
    # Time sampling interval
    T = config['T']
    # Source 1 normalized frequency/pulsation
    omega1 = config['omega1']
    # Source 1 normalized frequency/pulsation
    omega2 = config['omega2']
    
    # Here, we want to make the two sources coherent. Therefore, we make source 2 frequency equal to source 1 frequency
    #if config['coherent'] :
        # Source 2 normalized frequency/pulsation
        #omega2 = config['omega1']
    

    # We generate a complex AWGN (spatially white) with variance (1 or 2)
    variance = config['variance']  
    # Here, we assume that the real and imaginary parts of the noise are independent...                  
    noise = np.random.randn(M,N) + 1j*np.random.randn(M,N)
    
    # We compute both sources amplitudes...
    amp1 = np.sqrt(2)*10**(SNR1/20)   
    amp2 = np.sqrt(2)*10**(SNR2/20)
    # ...And their respective phases
    phi1 = -k*d*np.sin(theta1*np.pi/180)
    phi2 = -k*d*np.sin(theta2*np.pi/180)
    # We pack everything into a 
    a1 = np.power(np.exp(-1j*phi1),np.arange(0,M))
    a2 = np.power(np.exp(-1j*phi2),np.arange(0,M))

    A = np.stack((a1,a2),axis=-1)
    

    #phase1 = 1j*2*np.pi*np.random.normal(loc=0,scale=1,size=(N,1))
    #phase2 = 1j*2*np.pi*np.random.normal(loc=0,scale=1,size=(N,1))

    phase1 = 1j*2*np.pi*np.random.rand(N,1)
    phase2 = 1j*2*np.pi*np.random.rand(N,1)

    signal1 = amp1*np.exp(phase1)*np.power(np.exp(1j*omega1*T),np.arange(0,N)[:,np.newaxis])

    if config['coherent'] :
        phase2 = phase1

    signal2 = amp2*np.exp(1j*gamma*np.pi/180)*np.exp(phase2)*np.power(np.exp(1j*omega2*T),np.arange(0,N)[:,np.newaxis])

    s = np.concatenate((signal1,signal2),axis=1).T
    
    x = A@s + noise

    print('\n')
    print('-'*90)
    
    if config['coherent'] :
        print('\n\033[01m\033[31mSignals are coherent!\033[0m\n')
    else :
        print('\n\033[01m\033[31mSignals are not coherent!\033[0m\n')

    print('\n\033[01mSignal 1\033[0m\n')
    print('','_'*88,'')
    print('|  Amplitude | Frequency (Hz) | Direction of arrival (degrees) | Relative phase (degrees)|')
    print('|','-'*86,'|')
    print('|','   {:.2f}    |     {:.2f}       |              {:.2f}              |      0 (reference)     '.format(amp1,omega1/(2*np.pi),theta1),'|')
    print('|','_'*86,'|')

    print('\n\033[01mSignal 2\033[0m\n')
    print('','_'*88,'')
    print('|  Amplitude | Frequency (Hz) | Direction of arrival (degrees) | Relative phase (degrees)|')
    print('|','-'*86,'|')
    print('|','   {:.2f}    |     {:.2f}       |             {:.2f}             |         {:.2f}          '.format(amp2,omega2/(2*np.pi),theta2,gamma),'|')
    print('|','_'*86,'|')


    print('\n\033[01mNoise standad deviation : {}\033[0m'.format(np.sqrt(variance)))
    print('Output vector x is size {} by {} time samples\n'.format(M,N))

    # Has R full rank?
    #rank = np.linalg.matrix_rank(A,hermitian=False)
    #print('Matrix A rank is {}'.format(rank))
    #if rank == A.shape[1]:
      #print('A has full rank')
    #else :
      #print('A does not have full rank')

    print('The output signal has been save in: data/\n')
    
    
    np.save('data/python/'+name,x)

    return None

    