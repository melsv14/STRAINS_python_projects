import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve

# Test NumPy array creation
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])
x = solve(A, b)
print("Solution to Ax = b:", x)

# Test Matplotlib
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.title("Test Plot")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
