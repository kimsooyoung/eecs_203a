import numpy as np 
from scipy import ndimage
import matplotlib.pyplot as plt

L = 256
ROWS = 256
COLUMNS = 256

# def arithmetic_mean_filter(image, size):
#     kernel = np.ones((size, size), dtype=np.float32) / (size * size)
#     return convolve2d(image, kernel, mode='same', boundary='symm')

def arithmetic_mean_filter(image: np.ndarray, size: int):
    kernel = np.ones((size, size), dtype=np.float32) / (size * size)
    return ndimage.convolve(image, kernel, mode='nearest')

if __name__ == "__main__":

    image_name = "stripes" 

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

    # Apply arithmetic mean filters
    filtered_3x3 = arithmetic_mean_filter(original_image, 3)
    filtered_7x7 = arithmetic_mean_filter(original_image, 7)
    filtered_9x9 = arithmetic_mean_filter(original_image, 9)

    # Show images
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.imshow(original_image, cmap="gray", vmin=0, vmax=255)
    plt.title("Original Image") 
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.imshow(filtered_3x3, cmap="gray", vmin=0, vmax=255)
    plt.title("3x3 Arithmetic Mean Filter")
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(filtered_7x7, cmap="gray", vmin=0, vmax=255)
    plt.title("7x7 Arithmetic Mean Filter")
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.imshow(filtered_9x9, cmap="gray", vmin=0, vmax=255)
    plt.title("9x9 Arithmetic Mean Filter")
    plt.axis('off')

    plt.tight_layout()
    plt.show()
