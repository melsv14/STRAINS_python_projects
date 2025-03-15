import gmsh

# Initialize Gmsh
gmsh.initialize()

# Create a new model
gmsh.model.add("model")

######## GEOMETRY DEFINITION
#
#    3**4                            9
#    *  *                            *
#    *  5                            8
#    *  *                            *
#    *  6****************************7
#    2*******************************1

lc1 = 0.01
lc2 = 0.02  # characteristic lengths

# Define points
gmsh.model.geo.addPoint(0.2, 0, 0, lc2, 1)
gmsh.model.geo.addPoint(0, 0, 0, lc2, 2)
gmsh.model.geo.addPoint(0, 0.08, 0, lc2, 3)
gmsh.model.geo.addPoint(0.05, 0.08, 0, lc2, 4)
gmsh.model.geo.addPoint(0.05, 0.06, 0, lc1, 5)
gmsh.model.geo.addPoint(0.05, 0.04, 0, lc1, 6)
gmsh.model.geo.addPoint(0.2, 0.04, 0, lc1, 7)
gmsh.model.geo.addPoint(0.2, 0.06, 0, lc1, 8)
gmsh.model.geo.addPoint(0.2, 0.08, 0, lc1, 9)


# Define lines:
# Lines first surface (aluminium base)
gmsh.model.geo.addLine(1, 2, 1)
gmsh.model.geo.addLine(2, 3, 2)
gmsh.model.geo.addLine(3, 4, 3)
gmsh.model.geo.addLine(4, 6, 4)
gmsh.model.geo.addLine(6, 7, 5)
gmsh.model.geo.addLine(7, 1, 6)

#Lines second surface (cells)
gmsh.model.geo.addLine(6, 7, 7)
gmsh.model.geo.addLine(7, 8, 8)
gmsh.model.geo.addLine(8, 5, 9)
gmsh.model.geo.addLine(5, 6, 10)

#Lines third surface (cover)
gmsh.model.geo.addLine(5, 8, 11)
gmsh.model.geo.addLine(8, 9, 12)
gmsh.model.geo.addLine(9, 4, 13)
gmsh.model.geo.addLine(4, 5, 14)

# Define the loop and surface for aluminium panel
gmsh.model.geo.addCurveLoop([1, 2, 3, 4, 5, 6], 1)
gmsh.model.geo.addPlaneSurface([1], 1)

# Define the loop and surface for cells
gmsh.model.geo.addCurveLoop([7, 8, 9, 10], 2)
gmsh.model.geo.addPlaneSurface([2], 2)

# Define the loop and surface for cover
gmsh.model.geo.addCurveLoop([11, 12, 13, 14], 3)
gmsh.model.geo.addPlaneSurface([3], 3)

# Synchronize the CAD kernel with the Gmsh model
gmsh.model.geo.synchronize()

# Define two physical surfaces
gmsh.model.addPhysicalGroup(2, [1], 1)
gmsh.model.setPhysicalName(2, 1, "Physical Surface 1")

gmsh.model.addPhysicalGroup(2, [2], 2)
gmsh.model.setPhysicalName(2, 2, "Physical Surface 2")

gmsh.model.addPhysicalGroup(2, [3], 3)
gmsh.model.setPhysicalName(2, 3, "Physical Surface 3")

# Generate the mesh
gmsh.model.mesh.generate(2)

# Save and close
gmsh.write("solar_panel.msh")
gmsh.finalize()

import gmsh
import numpy as np
import matplotlib.pyplot as plt

# Initialize Gmsh and load the mesh
gmsh.initialize()
gmsh.open("solar_panel.msh")

# Get all nodes
node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
node_coords = np.array(node_coords).reshape(-1, 3)

# Function to get elements of a physical group
def get_elements_of_physical_group(dim, tag):
    entity_tags = gmsh.model.getEntitiesForPhysicalGroup(dim, tag)
    all_elements = []
    for entity_tag in entity_tags:
        element_types, element_tags, node_tags = gmsh.model.mesh.getElements(dim, entity_tag)
        for i in range(len(element_types)):
            all_elements.append(np.array(node_tags[i]).reshape(-1, 3))
    return np.concatenate(all_elements) if all_elements else np.array([])

# Get elements for each physical surface
elements_surface_1 = get_elements_of_physical_group(2, 1)
elements_surface_2 = get_elements_of_physical_group(2, 2)
elements_surface_3 = get_elements_of_physical_group(2, 3)

# Plot the mesh for each physical surface separately
plt.figure(figsize=(8, 8))

# Plot for Physical Surface 1
if elements_surface_1.size > 0:
    plt.triplot(node_coords[:, 0], node_coords[:, 1], elements_surface_1 - 1, color='blue', label='Aluminium support')

# Plot for Physical Surface 2
if elements_surface_2.size > 0:
    plt.triplot(node_coords[:, 0], node_coords[:, 1], elements_surface_2 - 1, color='red', label='Cells')

# Plot for Physical Surface 3
if elements_surface_3.size > 0:
    plt.triplot(node_coords[:, 0], node_coords[:, 1], elements_surface_3 - 1, color='green', label='Glass cover')

plt.gca().set_aspect('equal')
plt.title('Solar panel mesh with three physical surfaces')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

# Finalize Gmsh
gmsh.finalize()