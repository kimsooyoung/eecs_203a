import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

L = 256
ROWS = 480
COLUMNS = 640

def apply_averaging_filter(image, size=11):
    pad = size // 2
    kernel = np.ones((size, size), dtype=np.float32) / (size * size)

    # Pad the image using pixel replication
    padded_image = np.pad(image, pad_width=pad, mode='edge')

    # Prepare output image
    filtered_image = np.zeros_like(image, dtype=np.float32)

    # Convolution operation
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded_image[i:i+size, j:j+size]
            filtered_value = np.sum(region * kernel)
            filtered_image[i, j] = filtered_value

    return np.clip(filtered_image, 0, 255).astype(np.uint8)

def plot_histogram(image, title):
    plt.hist(image.ravel(), bins=range(L+1), color='black')
    plt.title(title)
    plt.xlabel("Gray Level")
    plt.ylabel("Frequency")
    plt.grid(True)

if __name__ == "__main__":

    image_name = "cat" 
    # or 
    # image_name = "triangle" 

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

    # Apply 11x11 averaging filter with pixel replication
    filtered_image = apply_averaging_filter(original_image)

    # Show original and filtered images side-by-side
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(original_image, cmap='gray')
    plt.title(f"Original Image ({image_name})")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(filtered_image, cmap='gray')
    plt.title(f"Filtered Image ({image_name})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    # Plot histograms
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plot_histogram(original_image, f"Histogram of Original ({image_name})")

    plt.subplot(1, 2, 2)
    plot_histogram(filtered_image, f"Histogram of Filtered ({image_name})")
    plt.tight_layout()
    plt.show()
