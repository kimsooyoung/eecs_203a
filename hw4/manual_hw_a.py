import cv2
import numpy as np
import matplotlib.pyplot as plt

L = 256
ROWS = 480
COLUMNS = 640

def apply_laplacian_filter(image):
    print(f"minimum value from Image: {np.min(image)}")

    # Define 3x3 Laplacian filter with -8 in the center
    kernel = np.array([[1, 1, 1],
                       [1, -8, 1],
                       [1, 1, 1]])

    # kernel output can be negative; make a copy of image considering negative values
    image_int16 = image.astype(np.int16)

    # Apply convolution (ignoring border)
    laplacian = cv2.filter2D(image_int16, ddepth=-1, kernel=kernel, borderType=cv2.BORDER_CONSTANT)

    # Add a constant to the image so that the smallest value becomes zero
    min_val = np.min(laplacian)
    laplacian_shifted = laplacian - min_val  # This makes the smallest value zero

    # Scale to 0–255 and convert to uint8
    max_val = np.max(laplacian_shifted)
    laplacian_scaled = (laplacian_shifted / max_val) * 255
    laplacian_uint8 = laplacian_scaled.astype(np.uint8)

    return laplacian_uint8

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