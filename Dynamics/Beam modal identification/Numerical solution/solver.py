import numpy as np
from scipy.linalg import eigh
from assembling import *

# Check the conditioning of the matrices
print("Condition number of the global stiffness matrix:", np.linalg.cond(K_global))
print("Condition number of the global mass matrix:", np.linalg.cond(M_global))

# Solve the eigenvalue problem
# The function 'eigh' is used because it is for symmetric (Hermitian) matrices, which our K and M are
eigenvalues, eigenvectors = eigh(K_reduced, M_reduced)# Visualization of the mode shapes with displacements

# Sort the eigenvalues and eigenvectors
sorted_indices = np.argsort(eigenvalues)
eigenvalues = eigenvalues[sorted_indices]
eigenvectors = eigenvectors[:, sorted_indices]

# Extract the first 3 eigenfrequencies (square root of eigenvalues gives natural frequencies)
omega = np.sqrt(eigenvalues)
frequencies = omega / (2 * np.pi)  # Convert from rad/s to Hz
first_3_frequencies = frequencies[:3]

print("The first 3 eigenfrequencies (in Hz) are:", first_3_frequencies)

# Plotting mode shapes
for i in range(3):
    mode_shape = eigenvectors[:, i]
    mode_shape_normalized = mode_shape / np.max(np.abs(mode_shape))

    # Only take the displacement DOFs for plotting (every other DOF starting from the first)
    mode_shape_displacements = mode_shape_normalized[::2]

    plt.figure()
    plt.plot(node_coords[1:], mode_shape_displacements, 'o-', label=f'Mode {i+1}')
    plt.title(f'Mode Shape {i+1}')
    plt.xlabel('Position along the beam (m)')
    plt.ylabel('Normalized Displacement')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plotting all three mode shapes in one graph
plt.figure()
for i in range(3):
    mode_shape = eigenvectors[:, i]
    mode_shape_normalized = mode_shape / np.max(np.abs(mode_shape))

    # Only take the displacement DOFs for plotting (every other DOF starting from the first)
    mode_shape_displacements = mode_shape_normalized[::2]

    # Plot each mode shape on the same figure
    plt.plot(node_coords[1:], mode_shape_displacements, 'o-', label=f'Mode {i+1}')

plt.title('First 3 Mode Shapes')
plt.xlabel('Position along the beam (m)')
plt.ylabel('Normalized Displacement')
plt.legend()
plt.grid(True)
plt.show()
