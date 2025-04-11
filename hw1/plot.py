import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the bilinear function
def b(x, y):
    return 2 + 2*x + 3*y + x*y

# Create the range of x and y values
x = np.linspace(1.0, 2.0, 100)
y = np.linspace(1.0, 2.0, 100)

# Create a meshgrid of x and y values
X, Y = np.meshgrid(x, y)

# Calculate the corresponding z values
Z = b(X, Y)

# Create the 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', antialiased=True)

# Set the axis labels
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('b(x, y)')

# Set the axis limits to match the specified domain
ax.set_xlim(1.0, 2.0)
ax.set_ylim(1.0, 2.0)

# Add a color bar for better understanding of the z values
fig.colorbar(surf, shrink=0.5, aspect=5)

# Set the title of the plot
plt.title('Surface plot of b(x, y) = 2 + 2x + 3y + xy over 1.0 <= x <= 2.0, 1.0 <= y <= 2.0')

# Show the plot
plt.show()