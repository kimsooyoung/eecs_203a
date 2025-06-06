import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

L = 256
ROWS = 480
COLUMNS = 640

def histogram_equalization(image_array):
    # 1. Calculate the histogram of the input image
    histogram, bins = np.histogram(image_array.flatten(), bins=L, range=(0, L))

    # 2. Calculate the cumulative distribution function (CDF)
    cdf = histogram.cumsum()

    # 3. Normalize the CDF to the range [0, L-1]
    cdf_normalized = (cdf - cdf.min()) * (L - 1) / (cdf.max() - cdf.min())
    cdf_normalized = cdf_normalized.astype(np.uint8)

    # 4. Create the mapping function (lookup table)
    mapping = cdf_normalized

    # 5. Apply the mapping to the original image
    equalized_image = mapping[image_array]

    return equalized_image, mapping

def draw_mapping_plot(mapping_function):
    input_levels = np.arange(L)

    plt.figure(figsize=(8, 6))
    plt.plot(input_levels, mapping_function)
    plt.title('Histogram Equalization Mapping')
    plt.xlabel('Input Gray Level')
    plt.ylabel('Output Gray Level')
    
    plt.grid(True)
    plt.show()

def draw_cat_imgs(original_image, equalized_image):

    # Display the original and histogram equalized images
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(original_image, cmap='gray', vmin=0, vmax=255)
    plt.title('Original Image')

    plt.subplot(1, 2, 2)
    plt.imshow(equalized_image, cmap='gray', vmin=0, vmax=255)
    plt.title('Histogram Equalized Image')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    try:
        with open("cat.raw", "rb") as f:
            data = np.fromfile(f, dtype=np.uint8)
            original_image = data.reshape((ROWS, COLUMNS))
    except FileNotFoundError:
        print("Error: 'cat.raw' not found.")
        exit()
    except Exception as e:
        print(f"Error loading 'cat.raw': {e}")
        exit()

    # Apply histogram equalization
    equalized_image, mapping_function = histogram_equalization(original_image)

    draw_mapping_plot(mapping_function)
    draw_cat_imgs(original_image, equalized_image)
