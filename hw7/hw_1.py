import cv2
import numpy as np
import matplotlib.pyplot as plt

L = 256
ROWS = 480
COLUMNS = 640

# Parameters
size = 31
half_size = size // 2
sigma = 7.0
A = 1 / 291.66706483023165

# Gaussian filter from HW6
def gaussian_filter(size, sigma):
    g = np.zeros((size, size), dtype=np.float64)
    for i in range(-half_size, half_size + 1):
        for j in range(-half_size, half_size + 1):
            g[i + half_size, j + half_size] = A * np.exp(-(i**2 + j**2) / (2 * sigma**2))
    print(f"{np.sum(g)=}")
    g /= np.sum(g)
    return g

if __name__ == "__main__":

    image_name = "triangle"

    try:
        with open(f"{image_name}.raw", "rb") as f:
            data = np.fromfile(f, dtype=np.uint8)
            original_image = data.reshape((ROWS, COLUMNS))
    except FileNotFoundError:
        print(f"Error: '{image_name}.raw' not found.")
        exit()
    except Exception as e:
        print(f"Error loading '{image_name}.raw': {e}")
        exit()

    # Create RGB channels
    R = original_image.astype(np.float32)
    G = 0.5 * original_image
    B = 0.2 * original_image

    # Clip and convert to uint8
    R = np.clip(np.round(R), 0, 255).astype(np.uint8)
    G = np.clip(np.round(G), 0, 255).astype(np.uint8)
    B = np.clip(np.round(B), 0, 255).astype(np.uint8)

    # Stack to get input color image
    input_color_image = np.stack((R, G, B), axis=-1)

    # Create Gaussian filter
    g_filter = gaussian_filter(size, sigma)

    # Filter each channel
    R_filtered = cv2.filter2D(R.astype(np.float32), -1, g_filter)
    G_filtered = cv2.filter2D(G.astype(np.float32), -1, g_filter)
    B_filtered = cv2.filter2D(B.astype(np.float32), -1, g_filter)

    # Clip and convert to uint8
    R_filtered = np.clip(np.round(R_filtered), 0, 255).astype(np.uint8)
    G_filtered = np.clip(np.round(G_filtered), 0, 255).astype(np.uint8)
    B_filtered = np.clip(np.round(B_filtered), 0, 255).astype(np.uint8)

    # Stack to get filtered color image
    filtered_color_image = np.stack((R_filtered, G_filtered, B_filtered), axis=-1)

    # Show images
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.title("Input Color Image")
    plt.imshow(input_color_image)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Filtered Color Image")
    plt.imshow(filtered_color_image)
    plt.axis("off")

    plt.tight_layout()
    plt.show()
