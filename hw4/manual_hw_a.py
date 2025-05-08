import cv2
import numpy as np
import matplotlib.pyplot as plt

L = 256
ROWS = 480
COLUMNS = 640

def manual_convolve(image, kernel):
    k_h, k_w = kernel.shape
    i_h, i_w = image.shape

    # Output dimensions: only "valid" region
    out_h = i_h - k_h + 1
    out_w = i_w - k_w + 1
    output = np.zeros((out_h, out_w), dtype=np.float32)

    # Convolution operation
    for i in range(out_h):
        for j in range(out_w):
            region = image[i:i + k_h, j:j + k_w]
            output[i, j] = np.sum(region * kernel)

    return output

def normalize_to_255(image):
    min_val = image.min()
    if min_val < 0:
        image = image - min_val
    max_val = image.max()
    if max_val > 0:
        image = (image / max_val) * 255
    return image.astype(np.uint8)

def apply_laplacian_filter(image):
    # Define 3x3 Laplacian filter with -8 in the center
    kernel = np.array([[1, 1, 1],
                       [1, -8, 1],
                       [1, 1, 1]])
    
    # Apply convolution (ignoring border)
    filtered = manual_convolve(image, kernel)
    
    # return both scaled and raw
    return normalize_to_255(filtered), filtered

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
    laplacian_image, _ = apply_laplacian_filter(original_image)

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