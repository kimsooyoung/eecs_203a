import cv2
import numpy as np
import matplotlib.pyplot as plt

L = 256
ROWS = 480
COLUMNS = 640

def apply_laplacian_filter(image):
    # Define 3x3 Laplacian filter with -8 in the center
    kernel = np.array([[1, 1, 1],
                       [1, -8, 1],
                       [1, 1, 1]])
    
    # Apply convolution (ignoring border)
    filtered = cv2.filter2D(image, -1, kernel, borderType=cv2.BORDER_CONSTANT)
    
    # Normalize: shift so min is 0
    min_val = np.min(filtered)
    if min_val < 0:
        filtered = filtered - min_val

    # Scale to 0–255 and convert to uint8
    filtered = (filtered / np.max(filtered)) * 255
    return filtered.astype(np.uint8)

def apply_sharpening_filter(image, laplacian):
    # Sharpened image = input - Laplacian
    sharpened = image.astype(np.int16) - laplacian.astype(np.int16)
    sharpened = np.clip(sharpened, 0, 255)
    return sharpened.astype(np.uint8)

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

    # Apply Laplacian filters
    laplacian_image = apply_laplacian_filter(original_image)

    # Apply sharpening filters
    sharpened_image = apply_sharpening_filter(original_image, laplacian_image)

    # show_images
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