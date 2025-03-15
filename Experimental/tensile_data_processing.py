import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

### Loading the experimental data
data_path = 'E:\Documents\Personal development\Master\Courses\Experimental mechanics\Labwork\Metal tests\STRAINS_M1_G_C'
data = np.loadtxt(data_path+'\E24_steel_30mmUL.csv', delimiter =',', skiprows = 2)

### Processing the data
width = 10.0 # in mm
thickness =  1.0 # in mm
l_original = 50.0 # in mm
section = width*thickness # in mm^2

force= data[:,1]
stretch_y = data[:,0]
strain_y = stretch_y/l_original

# Plot force vs strain in the longitudinal direction from the raw data
plt.figure()
plt.plot(strain_y, force, color = 'k')
plt.grid()
plt.title("Force-Strain plot (raw data)")
plt.xlabel("Strain_y")
plt.ylabel("Force (N)")

stress = force/section  #in MPa (F/mm^2)
stretch_y = 1 + strain_y

#Plot raw stress and stretch
plt.figure()
plt.plot(stretch_y, stress, color = '#043062', label = 'Raw data')

# Removing the buckling phase from the data
beg = np.argmin(stretch_y)

stress_update = stress[beg:] - stress[beg]
stretch_y_update = stretch_y[beg:]/stretch_y[beg]

plt.plot(stretch_y_update, stress_update, color = '#F9AD52', label = 'Updated data')
plt.grid()
plt.title("Stress-Stretch plot")
plt.xlabel('Stretch')
plt.ylabel('Stress (MPa)')
plt.legend()

### Modeling - determination of mechanical parameters
def Hookeslaw(x, a):
    return a*(x-1)

def Yeoh(x, a, b):
    return 2*(x-1/x**2)*(a + b*(x**2 + 2/x-3))

hooke_param, var = curve_fit(Hookeslaw, stretch_y_update, stress_update)

# Determine UTS, Yield Strength, and Elongation at Fracture
UTS_index = np.argmax(stress_update)
Yield_index = np.argmin(np.abs(stress_update - (stress_update[0] + stress_update[-1]) / 2))

# Added line for UTS
UTS = stress_update[UTS_index]
print('Ultimate Tensile Strength (UTS) = %s MPa' % UTS)

offset_strain = 0.002  # 0.2% strain offset

# Identify the linear elastic region (e.g., by visual inspection or using an algorithm)
# Draw a tangent line to the steepest part of the linear elastic region
tangent_slope = (stress_update[3] - stress_update[0]) / (stretch_y_update[3] - stretch_y_update[0])
tangent_intercept = stress_update[0] - tangent_slope * stretch_y_update[0]

# Offset the tangent line
offset_line = tangent_slope * (stretch_y_update - offset_strain) + tangent_intercept

# Find the intersection point (yield strength)
yield_index_offset = np.argmin(np.abs(stress_update - offset_line))

# Retrieve the yield strength using the offset method
yield_strength_offset = stress_update[yield_index_offset]
print('Yield Strength (Offset Method) = %s MPa' % yield_strength_offset)

# Added lines for Elongation at Fracture
elongation_at_fracture = stretch_y_update[-1] - 1
print('Elongation at Fracture = %s' % elongation_at_fracture)

print('Young modulus = %s' %hooke_param[0])
# Plotting figures & models
plt.figure()
plt.plot(stretch_y_update, stress_update, color = '#F9AD52', label = 'Stress-Stretch curve')
plt.plot(stretch_y_update, Hookeslaw(stretch_y_update, *hooke_param), color = '#074EA1', label = 'Hooke law modeling')

plt.grid()
plt.xlabel('Stretch')
plt.ylabel('Stress (MPa)')
plt.legend()
plt.show()


