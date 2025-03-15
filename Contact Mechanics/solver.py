import numpy as np

def solve_fem(nodes, elements, material_properties, fixed_dofs, contact_forces, solver_params):
    """
    Solves the FEM system for the given stiffness matrix, boundary conditions, and forces.

    Parameters:
        nodes (numpy.ndarray): Array of node coordinates [x, y].
        elements (numpy.ndarray): Array of element connectivity [n1, n2, n3].
        material_properties (numpy.ndarray): Array of material properties at each node.
        fixed_dofs (list): List of constrained degrees of freedom.
        contact_forces (numpy.ndarray): Global force vector (N).
        solver_params (dict): Solver parameters.

    Returns:
        tuple: (displacements, stresses)
            - displacements: Array of nodal displacements [u_x, u_y].
            - stresses: Array of element stresses [sigma_xx, sigma_yy, tau_xy].
    """
    num_nodes = len(nodes)
    num_dofs = 2 * num_nodes  # Two degrees of freedom (u_x, u_y) per node

    # Initialize global stiffness matrix and force vector
    K = np.zeros((num_dofs, num_dofs))  # Global stiffness matrix
    F = contact_forces.copy()           # Force vector (already includes contact forces)

    # Assemble global stiffness matrix
    for element in elements:
        element_nodes = nodes[element]  # Coordinates of element nodes
        element_material = material_properties[element]  # Extract material properties [E, nu] for element nodes
        K_element = element_stiffness_matrix(element_nodes, element_material)

        # Skip degenerate elements
        if np.allclose(K_element, 0):
            print(f"Skipping degenerate element with nodes: {element_nodes}")
            continue

        # Global DOF indices for triangular elements
        global_dof_indices = np.array([2 * n for n in element] + [2 * n + 1 for n in element], dtype=int)

        # Assemble into the global stiffness matrix
        for i in range(6):  # 6 DOFs for triangular elements
            for j in range(6):
                K[global_dof_indices[i], global_dof_indices[j]] += K_element[i, j]

    print(f"Non-zero elements in global K after assembly: {np.count_nonzero(K)}")
    print(f"Force Vector Size: {F.shape}")
    print(f"Stiffness Matrix Shape: {K.shape}")
    print(f"First row of K (sample): {K[0, :10]}")  # Display part of the stiffness matrix

    # Before applying boundary conditions
    print(f"Initial Force Vector (F): Non-zero entries: {np.nonzero(F)[0]}")
    print(f"Force Magnitudes: {F[np.nonzero(F)]}")

    # Apply boundary conditions
    for dof in fixed_dofs:
        K[dof, :] = 0
        K[:, dof] = 0
        K[dof, dof] = 1
        F[dof] = 0

    # After applying boundary conditions
    F_bc = F.copy()  # Copy of F after applying boundary conditions
    print(f"Force Vector after BCs: Non-zero entries: {np.nonzero(F_bc)[0]}")
    print(f"Force Magnitudes after BCs: {F_bc[np.nonzero(F_bc)]}")

    # Check equilibrium
    net_force = np.sum(F_bc)
    print(f"Net Force in the system after applying BCs: {net_force}")

    # Solve the system of equations
    try:
        print("Solving system of equations...")
        displacements = np.linalg.solve(K, F)
    except np.linalg.LinAlgError:
        print("Error: Stiffness matrix is singular. Check boundary conditions or mesh connectivity.")
        return np.zeros(num_dofs), np.zeros((len(elements), 3))  # Return zero displacements and stresses

    print(f"Maximum Displacement: {np.max(displacements):.2e}")
    print(f"Non-zero forces in F: {np.nonzero(F)}")
    print(f"Force values: {F[np.nonzero(F)]}")


    # Compute stresses for each element
    stresses = []
    for element in elements:
        element_nodes = nodes[element]
        element_material = material_properties[element]
        element_displacements = displacements[[2 * n for n in element] + [2 * n + 1 for n in element]]
        stress = compute_element_stress(element_nodes, element_material, element_displacements)
        stresses.append(stress)

    return displacements, np.array(stresses)



def element_stiffness_matrix(nodes, material_properties):
    """
    Computes the stiffness matrix for a 2D triangular element using isoparametric formulation.

    Parameters:
        nodes (numpy.ndarray): Coordinates of the element nodes, shape (3, 2).
        material_properties (numpy.ndarray): Material properties for the element nodes [E, nu].

    Returns:
        numpy.ndarray: Element stiffness matrix, shape (6, 6).
    """
    # Extract node coordinates
    x1, y1 = nodes[0]
    x2, y2 = nodes[1]
    x3, y3 = nodes[2]

    # Compute the area of the triangle
    A = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if A < 1e-6:  # Skip degenerate elements
        print(f"Degenerate triangular element detected: Nodes = {nodes}")
        return np.zeros((6, 6))

    # Compute averaged material properties for the element
    E_avg = np.mean(material_properties[:, 0])  # Average Young's modulus
    nu_avg = np.mean(material_properties[:, 1])  # Average Poisson's ratio

    # Compute D matrix
    D = (E_avg / (1 - nu_avg**2)) * np.array([
        [1, nu_avg, 0],
        [nu_avg, 1, 0],
        [0, 0, (1 - nu_avg) / 2]
    ])

    # Compute the B matrix
    b1 = y2 - y3
    b2 = y3 - y1
    b3 = y1 - y2
    c1 = x3 - x2
    c2 = x1 - x3
    c3 = x2 - x1
    B = (1 / (2 * A)) * np.array([
        [b1,  0, b2,  0, b3,  0],
        [0, c1,  0, c2,  0, c3],
        [c1, b1, c2, b2, c3, b3]
    ])

    # Compute the element stiffness matrix
    K = A * (B.T @ D @ B)

    return K


def compute_element_stress(nodes, material_properties, displacements):
    """
    Computes the stresses for a single triangular element.

    Parameters:
        nodes (numpy.ndarray): Coordinates of the element nodes, shape (3, 2).
        material_properties (numpy.ndarray): Material properties for the element nodes [E, nu].
        displacements (numpy.ndarray): Element nodal displacement vector, shape (6,).

    Returns:
        numpy.ndarray: Stress vector [sigma_xx, sigma_yy, tau_xy].
    """
    # Extract node coordinates
    x1, y1 = nodes[0]
    x2, y2 = nodes[1]
    x3, y3 = nodes[2]

    # Compute the area of the triangle
    A = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if A < 1e-6:  # Adjust tolerance as needed
        print(f"Skipping degenerate triangular element: Nodes = {nodes}")
        return np.zeros(3)  # Skip this element and return zero stress

    # Compute averaged material properties for the element
    E_avg = np.mean(material_properties[:, 0])  # Average Young's modulus
    nu_avg = np.mean(material_properties[:, 1])  # Average Poisson's ratio

    # Material matrix D
    D = (E_avg / (1 - nu_avg**2)) * np.array([
        [1, nu_avg, 0],
        [nu_avg, 1, 0],
        [0, 0, (1 - nu_avg) / 2]
    ])

    # Compute the B matrix
    b1 = y2 - y3
    b2 = y3 - y1
    b3 = y1 - y2
    c1 = x3 - x2
    c2 = x1 - x3
    c3 = x2 - x1
    B = (1 / (2 * A)) * np.array([
        [b1,  0, b2,  0, b3,  0],
        [0, c1,  0, c2,  0, c3],
        [c1, b1, c2, b2, c3, b3]
    ])

    # Compute strain
    strain = B @ displacements  # [epsilon_xx, epsilon_yy, gamma_xy]

    # Compute stress
    stress = D @ strain  # [sigma_xx, sigma_yy, tau_xy]

    return stress





if __name__ == "__main__":
    # Example usage for testing
    from parameters import params
    from mesh_generation import generate_mesh_gmsh
    from material_properties import apply_material_gradient
    from boundary_conditions import apply_boundary_conditions

    # Generate a mesh
    nodes, elements = generate_mesh_gmsh(
        params["geometry"],
        params["mesh"]["num_elements_x"],
        params["mesh"]["num_elements_y_FGM"] + params["mesh"]["num_elements_y_substrate"],
        visualize=False,
    )

    # Apply material properties
    material_properties = apply_material_gradient(nodes, params["material"], params["geometry"])

    # Apply boundary conditions
    fixed_dofs, contact_forces = apply_boundary_conditions(nodes, elements, params["geometry"], params["contact"])

    # Solve FEM system
    displacements, stresses = solve_fem(nodes, elements, material_properties, fixed_dofs, contact_forces,
                                        params["solver"])

    print(f"Displacements: {displacements[:10]}...")  # Display first 10 displacements
    print(f"Stresses: {stresses[:3]}...")  # Display first 3 element stresses

