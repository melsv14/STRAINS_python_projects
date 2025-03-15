import numpy as np

def apply_material_gradient(nodes, material_params, geometry_params):
    """
    Applies a continuous material gradient for the substrate and FGM layer.

    Parameters:
        nodes (numpy.ndarray): Array of node coordinates [x, y].
        material_params (dict): Material properties including:
            - "shear_modulus_surface": Shear modulus at the FGM top surface.
            - "shear_modulus_substrate": Shear modulus at the substrate.
            - "poisson_ratio": Poisson's ratio (assumed constant across all layers).
            - "inhomogeneity_constant": Exponential gradient constant.
        geometry_params (dict): Geometry properties including:
            - "H_FGM": Thickness of the FGM layer.
            - "H_substrate": Thickness of the substrate.

    Returns:
        numpy.ndarray: Array of material properties at each node.
            Each row contains [E, nu] for the corresponding node.
    """
    # Extract parameters
    H_FGM = geometry_params["H_FGM"]
    H_substrate = geometry_params["H_substrate"]
    shear_modulus_surface = material_params["shear_modulus_surface"]
    poisson_ratio = material_params["poisson_ratio"]
    inhomogeneity_constant = material_params["inhomogeneity_constant"]

    # Compute material properties
    y_coords = nodes[:, 1]  # Extract y-coordinates
    substrate_mask = y_coords < H_substrate  # Nodes in the substrate
    FGM_mask = ~substrate_mask  # Nodes in the FGM layer

    # Initialize material properties (E and nu for each node)
    material_properties = np.zeros((len(nodes), 2))

    # Assign substrate shear modulus and compute E using the relation E = 2G(1+nu)
    G_substrate = material_params["shear_modulus_substrate"]
    E_substrate = 2 * G_substrate * (1 + poisson_ratio)
    material_properties[substrate_mask, 0] = E_substrate  # E for substrate
    material_properties[substrate_mask, 1] = poisson_ratio  # nu for substrate

    # Assign FGM shear modulus and compute E using the exponential gradient
    distance_from_top = y_coords[FGM_mask] - (H_substrate + H_FGM)  # Reference from the top of FGM
    G_FGM = shear_modulus_surface * np.exp(inhomogeneity_constant * distance_from_top)
    E_FGM = 2 * G_FGM * (1 + poisson_ratio)
    material_properties[FGM_mask, 0] = E_FGM  # E for FGM
    material_properties[FGM_mask, 1] = poisson_ratio  # nu for FGM

    return material_properties


def compute_inhomogeneity_constant(material_params, geometry_params):
    """
    Computes the inhomogeneity constant for the FGM material gradient.

    Parameters:
        material_params (dict): Material properties including:
            - "shear_modulus_surface": Shear modulus at the FGM top surface.
            - "shear_modulus_substrate": Shear modulus at the substrate.
        geometry_params (dict): Geometry properties including:
            - "H_FGM": Thickness of the FGM layer.

    Returns:
        float: Inhomogeneity constant.
    """
    gamma = material_params["shear_modulus_substrate"] / material_params["shear_modulus_surface"]
    inhomogeneity_constant = -np.log(gamma) / geometry_params["H_FGM"]
    return inhomogeneity_constant


if __name__ == "__main__":
    # Example usage for testing
    from parameters import params
    from mesh_generation import generate_mesh_gmsh

    # Update inhomogeneity constant in the parameters
    params["material"]["inhomogeneity_constant"] = compute_inhomogeneity_constant(
        params["material"], params["geometry"]
    )

    # Generate a mesh for testing
    nodes, _ = generate_mesh_gmsh(
        params["geometry"],
        params["mesh"]["num_elements_x"],
        params["mesh"]["num_elements_y_FGM"] + params["mesh"]["num_elements_y_substrate"],
        visualize=False,
    )

    # Apply material gradient
    material_properties = apply_material_gradient(nodes, params["material"], params["geometry"])

    # Select 10 nodes in the FGM region for testing
    FGM_nodes = nodes[nodes[:, 1] >= params["geometry"]["H_substrate"]]
    sampled_FGM_nodes = FGM_nodes[np.linspace(0, len(FGM_nodes) - 1, 10, dtype=int)]

    # Print material properties at sampled FGM nodes
    print("Material Properties at 10 Sampled FGM Nodes:")
    for i, node in enumerate(sampled_FGM_nodes):
        y = node[1]
        G = params["material"]["shear_modulus_surface"] * np.exp(
            params["material"]["inhomogeneity_constant"] * (y - (params["geometry"]["H_substrate"] + params["geometry"]["H_FGM"]))
        )
        E = 2 * G * (1 + params["material"]["poisson_ratio"])
        print(f"Node {i}: y = {y:.2f}, G = {G:.2e}, E = {E:.2e}")
