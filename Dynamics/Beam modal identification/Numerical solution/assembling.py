import numpy as np
from parametrizing import *

# Initialize the global stiffness and mass matrices
K_global = np.zeros((discretization_params["dof"], discretization_params["dof"]))
M_global = np.zeros((discretization_params["dof"], discretization_params["dof"]))

# Calculate the length of each element
element_length = geometric_params["length"] / discretization_params["n_elements"]

# Define the local stiffness matrix for a beam element
def local_stiffness(E, I, element_length):
    return (material_params["E"] * geometric_params["I"] / element_length**3) * np.array([
        [ 12,  6*element_length, -12,  6*element_length],
        [ 6*element_length,  4*element_length**2, -6*element_length,  2*element_length**2],
        [-12, -6*element_length,  12, -6*element_length],
        [ 6*element_length,  2*element_length**2, -6*element_length,  4*element_length**2]
    ])

# Define the consistent mass matrix for a beam element
def local_mass(rho, A, element_length):
    return (rho * A * element_length / 420) * np.array([
        [156,  22*element_length,  54, -13*element_length],
        [22*element_length, 4*element_length**2, 13*element_length, -3*element_length**2],
        [ 54,  13*element_length, 156, -22*element_length],
        [-13*element_length, -3*element_length**2, -22*element_length, 4*element_length**2]
    ])

# Assemble the global stiffness and mass matrices
for i in range(discretization_params["n_elements"]):
    # Local matrices
    k_local = local_stiffness(material_params["E"], geometric_params["I"], element_length)
    m_local = local_mass(material_params["rho"], geometric_params["area"], element_length)

    # Assemble the global stiffness and mass matrices
for element in range(discretization_params["n_elements"]):
    # Define the starting index for the degrees of freedom for the current element
    start_dof = element * discretization_params["n_dof"]

    # Define the global DOF indices for the current element
    # Each element has 2 nodes, and each node has 2 DOFs (displacement and rotation)
    global_dof_indices = np.arange(start_dof, start_dof + discretization_params["n_dof"] * 2)

    # Add local contributions to global matrices
    for i_local, global_i in enumerate(global_dof_indices):
        for j_local, global_j in enumerate(global_dof_indices):
            K_global[global_i, global_j] += k_local[i_local, j_local]
            M_global[global_i, global_j] += m_local[i_local, j_local]

# Apply boundary conditions (clamped end at node 0)
K_reduced = K_global[2:, 2:]  # Remove the first two rows and columns
M_reduced = M_global[2:, 2:]  # Remove the first two rows and columns

# Now, K_reduced and M_reduced are ready to be used for the eigenvalue problem to find the eigenfrequencies and eigenmodes.
