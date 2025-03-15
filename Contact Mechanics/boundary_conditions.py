import numpy as np
import matplotlib.pyplot as plt


def apply_boundary_conditions(nodes, elements, geometry_params, contact_params, visualize=False):
    """
    Defines and applies boundary and contact conditions for the FEM system.

    Parameters:
        nodes (numpy.ndarray): Array of node coordinates [x, y].
        elements (numpy.ndarray): Array of element connectivity [n1, n2, n3].
        geometry_params (dict): Geometry parameters.
        contact_params (dict): Contact parameters.
        visualize (bool): If True, visualizes boundary and contact nodes.

    Returns:
        tuple: (fixed_dofs, contact_forces)
            - fixed_dofs: List of constrained degrees of freedom.
            - contact_forces: List of external forces applied at contact nodes.
    """
    W_FGM = geometry_params["W_FGM"]
    H_substrate = geometry_params["H_substrate"]
    H_FGM = geometry_params["H_FGM"]
    normal_force = contact_params["normal_force"]
    contact_region = contact_params["contact_region"]
    tolerance = 1e-6  # Tolerance for identifying nodes

    # Identify nodes on boundaries
    fixed_dofs = []  # List of constrained degrees of freedom
    contact_nodes = []  # Nodes in contact with the indenter

    for i, (x, y) in enumerate(nodes):
        # Fully fix bottom edge (y = 0)
        if np.isclose(y, 0, atol=tolerance):
            fixed_dofs.append(2 * i)  # Fix u_x
            fixed_dofs.append(2 * i + 1)  # Fix u_y

        # Fix left edge (x = 0) in u_x direction only
        elif np.isclose(x, 0, atol=tolerance):
            fixed_dofs.append(2 * i)  # Fix u_x

        # Fix right edge (x = W_FGM) in u_x direction only
        elif np.isclose(x, W_FGM, atol=tolerance):
            fixed_dofs.append(2 * i)  # Fix u_x

        # Identify contact nodes on the top surface
        if (contact_region[0] - tolerance <= x <= contact_region[1] + tolerance) and np.isclose(y, H_substrate + H_FGM,
                                                                                                atol=tolerance):
            contact_nodes.append(i)

    # Debugging: Check contact region and nodes
    print(f"Contact Region: {contact_region}")
    print(f"Identified Contact Nodes: {[nodes[i] for i in contact_nodes]}")

    # Apply contact forces (evenly distributed among contact nodes)
    contact_forces = np.zeros(2 * len(nodes))  # Initialize global force vector
    if len(contact_nodes) > 0:
        contact_force_per_node = normal_force / len(contact_nodes)  # Evenly distribute the force
        for node in contact_nodes:
            contact_forces[2 * node + 1] = -contact_force_per_node  # Apply normal force in -y direction
    else:
        print("Warning: No contact nodes detected in the contact region.")

    # Debugging: Applied forces
    for node in contact_nodes:
        print(f"Contact Node {node}: {nodes[node]}, Force: {contact_forces[2 * node + 1]}")

    # Fix reference node (e.g., bottom-left corner)
    fixed_dofs.append(0)  # Fix u_x of node 0
    fixed_dofs.append(1)  # Fix u_y of node 0

    # Remove duplicates and sort fixed DOFs
    fixed_dofs = sorted(set(fixed_dofs))

    # Debugging outputs
    print(f"Total Fixed DOFs: {len(fixed_dofs)}")
    print(f"Total Contact Nodes: {len(contact_nodes)}")

    # Optional visualization
    if visualize:
        plt.figure(figsize=(8, 6))
        plt.scatter(nodes[:, 0], nodes[:, 1], c="gray", label="All Nodes")
        plt.scatter(nodes[contact_nodes, 0], nodes[contact_nodes, 1], c="red", label="Contact Nodes")
        for dof in fixed_dofs[::2]:
            plt.scatter(nodes[dof // 2, 0], nodes[dof // 2, 1], c="blue", label="Fixed DOFs (x)" if dof == 0 else "")

        # Plot applied force vectors
        # for node in contact_nodes:
        #     force_x, force_y = contact_forces[2 * node], contact_forces[2 * node + 1]
        #     plt.arrow(nodes[node, 0], nodes[node, 1], 0, force_y / 1000, color="green", head_width=0.002,
        #               length_includes_head=False)

        plt.title("Boundary and Contact Nodes with Applied Forces")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.axis("equal")
        plt.legend()
        plt.show()

    return fixed_dofs, contact_forces

if __name__ == "__main__":
    # Example usage for testing
    from parameters import params
    from mesh_generation import generate_mesh_gmsh

    # Generate a mesh for testing
    nodes, elements = generate_mesh_gmsh(
        params["geometry"],
        params["mesh"]["num_elements_x"],
        params["mesh"]["num_elements_y_FGM"] + params["mesh"]["num_elements_y_substrate"],
        visualize=False,
    )

    # Apply boundary and contact conditions
    fixed_dofs, contact_forces = apply_boundary_conditions(
        nodes, elements, params["geometry"], params["contact"], visualize=True
    )

    # Print results for verification
    print(f"Fixed DOFs: {fixed_dofs[:10]}...")  # Show first 10 constraints
    print(f"Non-zero contact forces: {np.nonzero(contact_forces)[0][:10]}...")
    print(f"Total Fixed DOFs: {len(fixed_dofs)}")
