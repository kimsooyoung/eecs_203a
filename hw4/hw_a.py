import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

L = 256
ROWS = 480
COLUMNS = 640

def apply_laplacian_filter(image):
    print(f"minumum value from Image: {np.min(image)}")

    # Define 3x3 Laplacian filter with -8 in the center
    kernel = np.array([[1, 1, 1],
                       [1, -8, 1],
                       [1, 1, 1]], dtype=np.int32)
    
    image = image.astype(np.float32)

    filtered = convolve2d(image, kernel, mode='valid')

    filtered -= filtered.min()
    if filtered.max() > 0:
        filtered *= (255.0 / filtered.max())

    return filtered.astype(np.uint8)

def apply_sharpening_filter(image):
    # Define 3x3 Laplacian filter with -8 in the center
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]], dtype=np.int32)
    
    image = image.astype(np.float32)

    filtered = convolve2d(image, kernel, mode='valid')

    filtered -= filtered.min()
    if filtered.max() > 0:
        filtered *= (255.0 / filtered.max())

    return filtered.astype(np.uint8)

if __name__ == "__main__":

    # image_name = "cat" 
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

    # Apply Laplacian filter using convolve2d
    laplacian_image = apply_laplacian_filter(original_image)

    # Apply sharpening filter
    sharpened_image = apply_sharpening_filter(original_image)

    # Show images
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(laplacian_image, cmap='gray')
    plt.title(f"Laplacian Image {image_name}")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(sharpened_image, cmap='gray')
    plt.title(f"Sharpened Image {image_name}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()
