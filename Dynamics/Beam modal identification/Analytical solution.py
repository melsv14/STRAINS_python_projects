import numpy as np

# Material properties
E = 69*1e9  # Young's modulus in Pa
rho = 2770  # Density in kg/m^3

# Geometric properties
width = 0.010  # Section width in meters
height = 0.020  # Section height in meters
length = 0.400  # Length of the beam in meters
area = width * height  # Cross-sectional area in m^2
I = (width * height**3) / 12  # Moment of inertia in m^4

# Cantilever beam roots
beta = [1.8751, 4.6941, 7.8548]

# Calculating first three eigenfrequencies
frequencies = []
for n in beta:
    f_n = (n**2) * ((E * I)/(rho * area * length**4))**0.5 / (2 * np.pi)
    frequencies.append(f_n)

frequencies[:3]  # First three eigenfrequencies

print(frequencies)