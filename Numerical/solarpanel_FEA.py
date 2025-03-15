import gmsh
import numpy as np

# Initialize Gmsh and load the mesh
gmsh.initialize()
gmsh.open("solar_panel.msh")

# Get all nodes
node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
node_coords = np.array(node_coords).reshape(-1, 3)

print("Nodes = ", node_coords.shape)

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

print(elements_surface_1.shape, elements_surface_2.shape, elements_surface_3.shape)

def jacobian(coord):
  # compute the jacobian value for a triangle
  # coord is a (2x3) array
  # [[x1 x2 x3]
  #   y1 y2 y3]]

  jacobian = (coord[0,0]-coord[0,2]) * (coord[1,1]-coord[1,2]) - (coord[0,1] - coord[0,2]) * (coord[1,0] - coord[1,2])
  # it's the determinant of the jacobian
  return jacobian

def compute_N_matrix(coord):
 #zeta= ((()*())-(()*()))/ (2*A)

  # Assuming coord is a (2x3) array
  N = np.zeros([3, 1])

  denominator_0 = coord[1, 0] - coord[1, 1]
  denominator_1 = coord[1, 2] - coord[1, 0]
  denominator_2 = coord[1, 1] - coord[1, 2]

  if denominator_0 != 0:
      N[0, 0] = (coord[1, 1] - coord[1, 2]) / denominator_0
      N[0, 1] = (coord[0, 0] - coord[0, 2]) / denominator_0

  if denominator_1 != 0:
      N[1, 0] = (coord[1, 2] - coord[1, 0]) / denominator_1
      N[1, 1] = (coord[0, 1] - coord[0, 0]) / denominator_1

  if denominator_2 != 0:
      N[2, 0] = (coord[1, 0] - coord[1, 1]) / denominator_2
      N[2, 1] = (coord[0, 2] - coord[0, 1]) / denominator_2
  N /= (2 * jacobian(coord) )

  return N

def compute_b_matrix(coord):
  # coord is a (2x3) array
  # [[x1 x2 x3]
  #   y1 y2 y3]]

  B = np.zeros((2,3))
  B[0,0] = coord[1,1] - coord[1,2]  #y2 - y3
  B[0,1] = coord[1,2] - coord[1,0]
  B[0,2] = coord[1,0] - coord[1,1]

  B[1,0] = coord[0,2] - coord[0,1]  #x3 - x2
  B[1,1] = coord[0,0] - coord[0,2]
  B[1,2] = coord[0,1] - coord[0,0]

  B /= (2*jacobian(coord))

  return B

def compute_q(coord):
  T= np.array([[2], [3], [4]])
  B = compute_b_matrix(coord)
  q= np.dot(B,T)
  return q

def CST(coord, conductivity):
  B = compute_b_matrix(coord)
# compute the transpose(B).B, check that size is 3x3
# use numpy.transpose and numpy.dot
# multiply by the conductivity value and by the area of the element and also by the thickness!
  s = np.dot(np.transpose(B), B)
  s *= conductivity

  p =np.zeros((3))
 # coord is a (2x3) array
 # [[x1 x2 x3]
 #   y1 y2 y3]]
  if np.any(coord == 0.2, axis=0)[1]: # check whether one node is on the top layer

    print('Found node on the top edge, coordinates are = ', coord)


  return s,p

# Here we start with the FE process
# In hands we have:
# the nodes coordinates: node_coords
# the connectivity for each material: elements_surface_1, elements_surface_2, elements_surface_3

# Remove all third coordinates (should be zero's!)
nodes = np.delete(node_coords, 2, 1)
print("Nodes = ", nodes.shape)

print("Aluminium support = ", elements_surface_1.shape)
print("Cells = ", elements_surface_2.shape)
print("Glass cover = ", elements_surface_3.shape)


# STEP 1: loop over all the elements and compute the elementary quantities using the "CST" function
# remark : we do three separate loops (one for each material)
for element in elements_surface_1:
  coord = np.transpose(np.vstack((nodes[element[0]], nodes[element[1]], nodes[element[2]])))
  s, p = CST(coord = coord, conductivity = 1.0)
  print('elementary stiffness matrix = ', s)
  break

for element in elements_surface_2:
  coord = np.transpose(np.vstack((nodes[element[0]], nodes[element[1]], nodes[element[2]])))
  s, p = CST(coord = coord, conductivity = 0.1)
  print('elementary stiffness matrix = ', s)
  break

for element in elements_surface_3:
  coord = np.transpose(np.vstack((nodes[element[0]], nodes[element[1]], nodes[element[2]])))
  s, p = CST(coord = coord, conductivity = 0.01)
  print('elementary stiffness matrix = ', s)
  print('nodal flux = ', p)
  break
