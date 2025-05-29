import numpy as np
import matplotlib.pyplot as plt

# --- 1. Simulate the Blue Band Data based on the problem description ---
# Assume an image size for simulation purposes (e.g., 100x100 pixels)
image_width = 10000  # Using more pixels for a smoother histogram
image_height = 10000
num_pixels = image_width * image_height

# Generate random K values for each pixel (uniformly distributed between 0 and 1)
# K is a random variable with a uniform distribution between 0 and 1
K_values = np.random.uniform(0, 1, num_pixels)

# Calculate the blue band values for each pixel: B = 200 * K
# So, the blue band intensity values will be uniformly distributed between 0 and 200
blue_band_pixels = 200 * K_values

# --- 2. Plot the Gray Level Histogram for the Blue Band ---
plt.figure(figsize=(10, 6))
plt.hist(blue_band_pixels, bins=100, range=(0, 200), edgecolor='black', alpha=0.7, color='blue')
plt.title('Gray Level Histogram for the Blue Band of Image $C_1$', fontsize=16)
plt.xlabel('Intensity Value (Blue Band: $200K$)', fontsize=14)
plt.ylabel('Number of Pixels', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', alpha=0.75)
plt.show()