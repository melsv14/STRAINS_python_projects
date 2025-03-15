import numpy as np
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation

def plot_mesh_with_refinement(nodes, elements, contact_region, refined_region=None):
    """
    Plots the mesh, highlighting refined regions and contact nodes.
    """
    plt.figure(figsize=(8, 6))

    # Plot all elements
    for element in elements:
        polygon = nodes[element]
        plt.fill(*polygon.T, edgecolor="gray", fill=False, linewidth=0.5)

    # Highlight elements in the refined region
    if refined_region:
        for element in elements:
            element_nodes = nodes[element]
            x_min, x_max = element_nodes[:, 0].min(), element_nodes[:, 0].max()
            if refined_region[0] <= x_min <= refined_region[1] or refined_region[0] <= x_max <= refined_region[1]:
                plt.fill(*element_nodes.T, edgecolor="blue", fill=False, linewidth=1.0, alpha=0.6)

    # Highlight the contact region
    plt.axvspan(contact_region[0], contact_region[1], color="red", alpha=0.3, label="Contact Region")

    plt.title("Mesh with Refined Region and Contact Region Highlighted")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis("equal")
    plt.legend()
    plt.show()


def plot_deformation_with_annotations(nodes, elements, displacements, scale=1.0, contact_region=None):
    """
    Plots the deformed mesh and overlays it with the original mesh for comparison.
    """
    plt.figure(figsize=(8, 6))

    # Compute deformed coordinates
    deformed_nodes = nodes + scale * displacements.reshape(-1, 2)

    # Plot original mesh
    for element in elements:
        original = nodes[element]
        plt.fill(*original.T, edgecolor="gray", fill=False, linewidth=0.5)

    # Plot deformed mesh
    for element in elements:
        deformed = deformed_nodes[element]
        plt.fill(*deformed.T, edgecolor="blue", fill=False, linewidth=0.5)

    # Highlight contact region
    if contact_region:
        plt.axvspan(contact_region[0], contact_region[1], color="red", alpha=0.3, label="Contact Region")

    plt.title("Deformed Mesh with Displacements")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis("equal")
    plt.legend()
    plt.show()


def plot_stresses_with_contact(nodes, elements, stresses, stress_component, contact_region):
    """
    Plots the stress distribution across the material, ensuring proper mapping of stress values.

    Parameters:
        nodes (numpy.ndarray): Array of node coordinates [x, y].
        elements (numpy.ndarray): Array of element connectivity [n1, n2, n3].
        stresses (numpy.ndarray): Array of element stresses [sigma_xx, sigma_yy, tau_xy].
        stress_component (int): Index of the stress component to plot.
        contact_region (tuple): x-coordinates of the contact region.
    """
    plt.figure(figsize=(8, 6))

    # Extract stress values for the chosen component
    stress_values = stresses[:, stress_component]

    # Debugging: Print sizes for validation
    print(f"Number of stress values: {len(stress_values)}")
    print(f"Number of elements: {len(elements)}")
    print(f"Number of nodes: {len(nodes)}")

    # Ensure stress values align with the nodes for plotting
    if len(stress_values) == len(elements):
        # Map stress values from elements to nodes
        stress_per_node = np.zeros(len(nodes))
        count_per_node = np.zeros(len(nodes))
        for element, stress in zip(elements, stress_values):
            for node in element:
                stress_per_node[node] += stress
                count_per_node[node] += 1
        # Avoid division by zero
        count_per_node[count_per_node == 0] = 1
        stress_values = stress_per_node / count_per_node
    elif len(stress_values) != len(nodes):
        raise ValueError("Mismatch between stress values and nodes/elements.")

    # Create a triangulation object for plotting
    triangulation = Triangulation(nodes[:, 0], nodes[:, 1], elements)

    # Plot the stress distribution
    levels = np.linspace(stress_values.min(), stress_values.max(), 20)
    contour = plt.tricontourf(triangulation, stress_values, levels=levels, cmap="viridis")
    plt.colorbar(contour, label=f"Stress Component {stress_component} (Pa)")

    # Highlight contact region
    plt.axvspan(contact_region[0], contact_region[1], color="red", alpha=0.3, label="Contact Region")

    plt.title(f"Stress Distribution (Component {stress_component})")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis("equal")
    plt.legend()
    plt.show()


def plot_forces(nodes, contact_forces, scale=1.0):
    """
    Plots the applied forces on the nodes.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(nodes[:, 0], nodes[:, 1], c="gray", label="Nodes")

    for i, (x, y) in enumerate(nodes):
        fx, fy = contact_forces[2 * i], contact_forces[2 * i + 1]
        if fx != 0 or fy != 0:
            plt.quiver(x, y, scale * fx, scale * fy, angles="xy", scale_units="xy", color="red", label="Forces" if i == 0 else "")

    plt.title("Applied Forces")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis("equal")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    from main import main
    from parameters import params

    # Run the main function to retrieve results
    nodes, elements, displacements, stresses, contact_forces = main()

    # Define regions for plotting
    contact_region = params["contact"]["contact_region"]
    refined_region = [
        contact_region[0] - 0.1,  # Slightly extend refined region for visualization
        contact_region[1] + 0.1,
    ]

    # Plotting
    plot_mesh_with_refinement(nodes, elements, contact_region, refined_region=refined_region)
    plot_deformation_with_annotations(nodes, elements, displacements, scale=1e4, contact_region=contact_region)
    plot_forces(nodes, contact_forces, scale=0.1)

    for i, stress_label in enumerate(["σ_xx", "σ_yy", "τ_xy"]):
        plot_stresses_with_contact(
            nodes,
            elements,
            stresses,
            stress_component=i,
            contact_region=contact_region,
        )
