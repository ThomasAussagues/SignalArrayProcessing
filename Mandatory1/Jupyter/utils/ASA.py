import numpy as np
import matplotlib.pyplot as plt

import numpy as np

# Defines parameters for the ASA

# Simulation grid
Nx = 1024  # No of pixels, x-direction
Ny = 1024  # No of pixels, y-direction

# Medium / problem
fc = 3e6  # Center frequency, probe (Hz)
c = 1500  # Speed of sound (m/s)
lambda_ = c / fc  # Wavelength

# Physical grid
dx = lambda_ / 2  # pixel size, x-direction, [m]
dy = lambda_ / 2  # pixel size, y-direction, [m]
Dx = Nx * dx  # Physical length, x-direction, [m]
Dy = Ny * dy  # Physical length, y-direction, [m]

# Frequency grid
u = 2 * np.arange(0, Nx, 1) / Nx - 1  # Defines as in fft
v = 2 * np.arange(0, Ny, 1) / Ny - 1  # Aliasing will occure if sampling distance too large
# Axis
ax = np.linspace(-Dx / 2, Dx / 2, Nx)
ay = np.linspace(-Dy / 2, Dy / 2, Ny)


def get_params():
    config = {'Nx': Nx, 'Ny': Ny, 'fc': fc, 'c': c, 'lambda': lambda_, 'dx': dx, 'dy': dy, 'Dx': Dx, 'Dy': Dy, 'u': u,
              'v': v, 'ax': ax, 'ay': ay}

    return config


def ASA_propagator(config, z):
    # Propogator in ASA from z_0 to z

    prop = np.zeros((config['Nx'], config['Ny']))

    uSq = np.tile(config['u'][:, np.newaxis] ** 2, (1, config['Ny']))
    vSq = np.tile(config['v'][np.newaxis, :] ** 2, (config['Nx'], 1))

    prop = np.exp(1j * 2 * np.pi * z * np.sqrt(1 - uSq - vSq) / config['lambda'])

    prop[uSq + vSq > 1] = 0

    return prop


def ASA_sources(config, type, r):
    # Function setting up the source for the ASA simulation

    # Defining a piston w/uniform pressure, radius 'r' placed in origo
    if type == 'piston':

        X, Y = np.meshgrid(config['ax'], config['ay'])
        U_0 = np.zeros((config['Nx'], config['Ny']), dtype='complex')
        U_0[X ** 2 + Y ** 2 <= r ** 2] = 1

    elif type == 'square':

        # Defining a piston w/uniform pressure, radius 'r' placed in origo

        X, Y = np.meshgrid(config['ax'], config['ay'])
        U_0 = np.zeros((config['Nx'], config['Ny']), dtype='complex')
        U_0[np.where((np.abs(X) <= r) & (np.abs(Y) <= r))] = 1

    else:
        print('Source type not defined in ASAsource.m')
        exit()

    return U_0


def ASA_focused_sources(config, type,r, focusing_distance):

    source = ASA_sources(config, type, r)

    delay = np.zeros((config['Nx'], config['Ny']), dtype='complex')

    theta = np.arctan(config['Nx']/(2*focusing_distance))

    k_x = 2*np.pi/config['lambda']*theta

    delay_1D = k_x*config['ax']

    delay = np.tile(delay_1D,(1,config['Ny']))

    return delay










