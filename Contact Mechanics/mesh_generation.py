import gmsh
import numpy as np

def generate_mesh_gmsh(geometry_params, num_elements_x, num_elements_y_total, visualize=False):
    """
    Generates a refined triangular mesh for a rectangular domain with an FGM layer and a homogeneous substrate.

    Parameters:
        geometry_params (dict): Contains the geometry parameters.
        num_elements_x (int): Number of elements along the width.
        num_elements_y_total (int): Total number of elements along the height.
        visualize (bool): If True, visualizes the mesh in the Gmsh GUI.

    Returns:
        tuple: (nodes, elements)
            - nodes: Array of node coordinates [x, y].
            - elements: Array of element connectivity [n1, n2, n3].
    """
    gmsh.initialize()
    gmsh.model.add("Mesh Generation")

    # Unpack geometry parameters
    W = geometry_params["W_FGM"]
    H_FGM = geometry_params["H_FGM"]
    H_substrate = geometry_params["H_substrate"]
    indenter_width = geometry_params["indenter_width"]

    # Create points
    p1 = gmsh.model.geo.addPoint(0, 0, 0)
    p2 = gmsh.model.geo.addPoint(W, 0, 0)
    p3 = gmsh.model.geo.addPoint(W, H_substrate, 0)
    p4 = gmsh.model.geo.addPoint(0, H_substrate, 0)
    p5 = gmsh.model.geo.addPoint(0, H_substrate + H_FGM, 0)
    p6 = gmsh.model.geo.addPoint(W, H_substrate + H_FGM, 0)

    # Create lines
    l1 = gmsh.model.geo.addLine(p1, p2)
    l2 = gmsh.model.geo.addLine(p2, p3)
    l3 = gmsh.model.geo.addLine(p3, p4)
    l4 = gmsh.model.geo.addLine(p4, p1)
    l5 = gmsh.model.geo.addLine(p4, p5)
    l6 = gmsh.model.geo.addLine(p5, p6)
    l7 = gmsh.model.geo.addLine(p6, p3)

    # Define surfaces
    substrate_loop = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
    substrate_surface = gmsh.model.geo.addPlaneSurface([substrate_loop])

    FGM_loop = gmsh.model.geo.addCurveLoop([l5, l6, l7, l3])
    FGM_surface = gmsh.model.geo.addPlaneSurface([FGM_loop])

    # Synchronize geometry
    gmsh.model.geo.synchronize()

    # Define refinement field near the indenter
    contact_x_start = W / 2 - indenter_width / 2
    contact_x_end = W / 2 + indenter_width / 2
    refinement_margin = 0.1  # Additional margin for the refinement field

    box_field = gmsh.model.mesh.field.add("Box")
    gmsh.model.mesh.field.setNumber(box_field, "VIn", 0.005)  # Minimum element size (refined)
    gmsh.model.mesh.field.setNumber(box_field, "VOut", 0.05)  # Maximum element size (coarse)
    gmsh.model.mesh.field.setNumber(box_field, "XMin", contact_x_start - refinement_margin)
    gmsh.model.mesh.field.setNumber(box_field, "XMax", contact_x_end + refinement_margin)
    gmsh.model.mesh.field.setNumber(box_field, "YMin", H_substrate)
    gmsh.model.mesh.field.setNumber(box_field, "YMax", H_substrate + H_FGM)

    # Set the field as background
    gmsh.model.mesh.field.setAsBackgroundMesh(box_field)

    # Generate mesh
    gmsh.model.mesh.generate(2)

    # Extract nodes and elements
    node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
    nodes = np.array(node_coords).reshape(-1, 3)[:, :2]
    element_types, _, element_node_tags = gmsh.model.mesh.getElements()

    # Process triangular elements
    elements = []
    for i, elem_type in enumerate(element_types):
        if elem_type == 2:  # Triangular elements
            triangular_elements = np.array(element_node_tags[i], dtype=int).reshape(-1, 3) - 1
            elements.extend(triangular_elements)
        else:
            print(f"Unsupported element type {elem_type}")

    elements = np.array(elements)

    if visualize:
        gmsh.fltk.run()

    gmsh.finalize()

    return nodes, elements


if __name__ == "__main__":
    # Example usage for testing
    from parameters import params

    nodes, elements = generate_mesh_gmsh(
        params["geometry"],
        params["mesh"]["num_elements_x"],
        params["mesh"]["num_elements_y_FGM"] + params["mesh"]["num_elements_y_substrate"],
        visualize=True,
    )
    print(f"Generated {len(nodes)} nodes and {len(elements)} elements.")
