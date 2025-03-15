from parameters import params
from mesh_generation import generate_mesh_gmsh
from material_properties import apply_material_gradient
from boundary_conditions import apply_boundary_conditions
from solver import solve_fem

def main():
    # Step 1: Generate Mesh
    print("Generating Mesh...")
    nodes, elements = generate_mesh_gmsh(
        params["geometry"],
        params["mesh"]["num_elements_x"],
        params["mesh"]["num_elements_y_FGM"] + params["mesh"]["num_elements_y_substrate"],
        visualize=False,
    )

    # Step 2: Apply Material Properties
    print("Applying Material Gradient...")
    material_properties = apply_material_gradient(nodes, params["material"], params["geometry"])

    # Step 3: Apply Boundary Conditions
    print("Applying Boundary Conditions...")
    fixed_dofs, contact_forces = apply_boundary_conditions(
        nodes, elements, params["geometry"], params["contact"]
    )

    # Step 4: Solve FEM System
    print("Solving FEM System...")
    displacements, stresses = solve_fem(
        nodes, elements, material_properties, fixed_dofs, contact_forces, params["solver"]
    )

    # Step 5: Output Results
    print(f"Displacements: {displacements[:10]}...")  # First 10 displacements
    print(f"Stresses: {stresses[:3]}...")  # First 3 stresses

    # Step 6: Pass to Post-Processing (if ready)
    return nodes, elements, displacements, stresses, contact_forces

if __name__ == "__main__":
    results = main()
