import numpy as np
import matplotlib.pyplot as plt

# Material properties
material_params = {
    "E": 69*1e9,  # Young's modulus in Pa
    "rho": 2770,  # Density in kg/m^3
}

# Geometric properties
geometric_params = {
    "width": 0.010,  # Section width in meters
    "height": 0.020,  # Section height in meters
    "length": 0.400,  # Length of the beam in meters
}

geometric_params["area"] = geometric_params["width"] * geometric_params["height"]  # Cross-sectional area in m^2
geometric_params["I"] = (geometric_params["width"] * geometric_params["height"]**3) / 12  # Moment of inertia in m^4


# Discretization (Define the number of elements)
discretization_params = {
"n_elements": 10,  # Number of elements
"n_dof": 2, # Degrees of freedom per node
}

discretization_params["n_nodes"] = discretization_params["n_elements"] + 1 # Number of nodes
discretization_params["dof"] = discretization_params["n_nodes"] * discretization_params["n_dof"] # Total degrees of freedom

node_coords = np.linspace(0, geometric_params["length"], discretization_params["n_nodes"])  # Node coordinates array

# Boundary conditions
fixed_node = 0  # Node at x=0 is clamped

# For visualization, let's plot the layout of the beam
plt.plot(node_coords, np.zeros_like(node_coords), 'bo-')  # Plot the nodes as blue dots and the beam as a line
plt.title('1D Beam Layout')
plt.xlabel('Length (m)')
plt.ylabel('Position of Nodes')
plt.grid(True)
plt.show()