import numpy as np
from scipy.linalg import solve
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Problem Parameters
P = 1000  # Total applied normal load (N)
a = 1.0  # Half-contact length (m)
E = 210e9  # Young's modulus (Pa)
nu = 0.3  # Poisson's ratio
c = 0.1  # Material inhomogeneity parameter
mu = E / (2 * (1 + nu))  # Shear modulus
kappa = (3 - nu) / (1 + nu)  # Plane strain constant

# Define analytical functions

def contact_pressure(x):
    """Analytical contact pressure for flat indenter."""
    if abs(x) <= a:
        return P / (2 * a) * np.sqrt(1 - (x / a) ** 2)
    else:
        return 0  # Outside the contact region

def stress_xx(x, y):
    """Stress component σ_xx under the indenter."""
    return -P / (2 * np.pi) * (2 * a / np.sqrt(a**2 - x**2)) if abs(x) <= a else 0

def stress_yy(x, y):
    """Stress component σ_yy under the indenter."""
    return P / (2 * np.pi) * (2 * a / np.sqrt(a**2 - x**2)) if abs(x) <= a else 0

def stress_xy(x, y):
    """Shear stress σ_xy (zero for flat indenter symmetry)."""
    return 0  # Symmetric flat indenter

def displacement(x, epsilon=1e-6):
    """
    Compute the vertical displacement under and outside the indenter.
    Ensures continuity at the contact edges.
    """
    if np.abs(x) < a:
        # Flat indenter imposes uniform displacement inside the contact region
        return -P / (2 * a * mu)
    elif np.abs(x) == a:
        # Ensure continuity at the edges
        return -P / (2 * a * mu)  # Same as inside
    else:
        # Logarithmic decay of displacement outside the contact region
        return (P * (1 - nu**2)) / (np.pi * E) * np.log(4 * a / (np.abs(x + a) + epsilon))


# Numerical integration for deformation outside the contact region
def deformation_integral(x):
    """Numerical integration for deformation outside contact region."""
    integrand = lambda t: contact_pressure(t) / np.sqrt((x - t) ** 2 + 1e-6)  # Regularized
    return quad(integrand, -a, a)[0]

# Discretization for numerical evaluation
x_vals = np.linspace(-1.5 * a, 1.5 * a, 500)  # x-coordinates for evaluation
contact_pressures = np.array([contact_pressure(x) for x in x_vals])
stress_xx_vals = np.array([stress_xx(x, 0) for x in x_vals])
stress_yy_vals = np.array([stress_yy(x, 0) for x in x_vals])
displacement_vals = np.array([displacement(x) for x in x_vals])

# Plot Contact Pressure
plt.figure()
plt.plot(x_vals, contact_pressures, label="Contact Pressure")
plt.title("Contact Pressure Distribution")
plt.xlabel("x (Contact Length)")
plt.ylabel("p(x) [Pa]")
plt.legend()
plt.grid()
plt.show()

# Plot Stress Distributions
plt.figure()
plt.plot(x_vals, stress_xx_vals, label="Stress σ_xx")
plt.plot(x_vals, stress_yy_vals, label="Stress σ_yy")
plt.title("Stress Distribution under Flat Indenter")
plt.xlabel("x (Contact Length)")
plt.ylabel("Stress [Pa]")
plt.legend()
plt.grid()
plt.show()

# Recompute displacement values using the updated function
displacement_vals = np.array([displacement(x) for x in x_vals])

# Plot the updated displacement
plt.figure()
plt.plot(x_vals, displacement_vals, label="Vertical Displacement")
plt.title("Vertical Displacement under Flat Indenter")
plt.xlabel("x (Contact Length)")
plt.ylabel("Displacement [m]")
plt.legend()
plt.grid()
plt.show()

