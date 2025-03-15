import numpy as np

# Geometry Parameters
geometry_params = {
    "W_FGM": 2.0,  # Width of the FGM layer (m)
    "H_FGM": 0.1,  # Thickness of the FGM layer (m)
    "H_substrate": 0.5,  # Thickness of the homogeneous substrate (m)
    "indenter_width": 0.2,  # Width of the flat indenter (m)
}

# Add a domain scaling factor for semi-infinite behavior
domain_scaling_factor = 1.0  # Ensures the domain is significantly larger than the indenter

# Update the width of the domain based on the scaling factor
geometry_params["W_FGM"] = max(domain_scaling_factor * geometry_params["indenter_width"], geometry_params["W_FGM"])

# Material Properties
material_params = {
    "shear_modulus_surface": 80e9,  # Shear modulus at the surface (Pa) [default: 100e9]
    "shear_modulus_substrate": 15e9,  # Shear modulus at the substrate (Pa)
    "poisson_ratio": 0.3,  # Poisson's ratio (assumed constant across the domain)
}

# Compute the inhomogeneity constant 'c' for the exponential material gradient
material_params["inhomogeneity_constant"] = -np.log(
    material_params["shear_modulus_surface"] / material_params["shear_modulus_substrate"]
) / geometry_params["H_FGM"]

# Contact and Loading Parameters
contact_params = {
    "normal_force": 1e6,  # Applied normal force on the indenter (N)
    "friction_coefficient": 0.3,  # Coefficient of Coulomb friction
    "contact_region": [
        geometry_params["W_FGM"] / 2 - geometry_params["indenter_width"] / 2,
        geometry_params["W_FGM"] / 2 + geometry_params["indenter_width"] / 2,
    ],  # x-coordinates of contact region (m)
}

# Mesh Parameters
mesh_params = {
    "num_elements_x": 100,  # Number of elements along the width [default: 50]
    "num_elements_y_FGM": 10,  # Number of elements along the FGM height [default: 10]
    "num_elements_y_substrate": 50,  # Number of elements along the substrate height [default: 40]
    "element_order": 2,  # Polynomial order of finite elements (e.g., linear/quadratic)
}

# Solver Parameters
solver_params = {
    "tolerance": 1e-6,  # Convergence tolerance for iterative solvers
    "max_iterations": 500,  # Maximum number of iterations
    "penalty_coefficient": 1e9,  # Penalty method coefficient for enforcing contact
}

# Post-Processing Parameters
post_processing_params = {
    "plot_stress_distribution": True,  # Whether to plot stress distribution
    "plot_material_gradient": True,  # Whether to visualize material property distribution
    "output_directory": "./output/",  # Directory to store result files
}

# Combine all parameters into a single dictionary for easy access
params = {
    "geometry": geometry_params,
    "material": material_params,
    "contact": contact_params,
    "mesh": mesh_params,
    "solver": solver_params,
    "post_processing": post_processing_params,
    "domain_scaling_factor": domain_scaling_factor,  # Pass the scaling factor to mesh generation
}

# Utility function to display parameters (optional for debugging)
def print_parameters():
    for category, category_params in params.items():
        print(f"=== {category.upper()} PARAMETERS ===")
        for key, value in category_params.items():
            print(f"{key}: {value}")
        print()

if __name__ == "__main__":
    # Example: Print parameters when running this file
    print_parameters()
