import numpy as np
import matplotlib.pyplot as plt

M, N = 256, 256
u = np.arange(M)
v = np.arange(N)
U, V = np.meshgrid(u, v)

problem_num = 2

if problem_num is 1:
    H = 0.5 * (np.cos(2 * np.pi * U / M) + np.cos(2 * np.pi * V / N))
    H_mag = np.abs(H)
elif problem_num is 2:
    H = 2 * np.cos(2 * np.pi * U / M) + 2 * np.cos(2 * np.pi * V / N) - 4
    H_mag = np.abs(H)

# Plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Surface plot with adjusted limits and angle
surf = ax.plot_surface(U, V, H_mag, cmap='plasma', edgecolor='none')
ax.set_zlim(0, np.max(H_mag))       # z-axis to show only positive magnitudes
ax.view_init(elev=30, azim=45)      # Set good viewing angle
ax.set_title("|H(u, v)|", fontsize=14)
ax.set_xlabel("u (Frequency in x)")
ax.set_ylabel("v (Frequency in y)")
ax.set_zlabel("|H(u, v)| Magnitude")
fig.colorbar(surf, shrink=0.5, aspect=10)
plt.tight_layout()
plt.show()
