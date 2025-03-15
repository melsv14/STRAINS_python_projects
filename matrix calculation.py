import sympy as sp

# Define symbols
E, I, L, U, theta = sp.symbols('E I L U theta')

# Define stiffness matrix k
k = sp.Matrix([
    [12*E*I/L**3,  6*E*I/L**2, -12*E*I/L**3,  6*E*I/L**2],
    [ 6*E*I/L**2,  4*E*I/L,    -6*E*I/L**2,   2*E*I/L   ],
    [-12*E*I/L**3, -6*E*I/L**2, 12*E*I/L**3, -6*E*I/L**2],
    [ 6*E*I/L**2,  2*E*I/L,    -6*E*I/L**2,   4*E*I/L   ]
])

# Define displacement vector u
u = sp.Matrix([U, theta, 0, 0])

# Compute k * u
ku = k * u
print("k * u =", ku)

# Compute elastic energy U = (1/2) * u^T * k * u
elastic_energy = (1/2) * u.T * k * u
print("Elastic Energy U =", sp.simplify(elastic_energy[0]))
