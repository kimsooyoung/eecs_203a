import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

L = 256
gamma1 = 0.4
gamma2 = 2.5

ROWS = 480
COLUMNS = 640

def power_law_transform(gray_level, gamma, L=256):
    """Applies the power-law (gamma) transformation to a gray level.

    Args:
        gray_level (int): The input gray level (0 to L-1).
        gamma (float): The gamma value for the power-law transform.
        L (int): The total number of gray levels (default is 256).

    Returns:
        int: The output gray level after the transformation.
    """
    return int(((gray_level / (L - 1)) ** gamma) * (L - 1))

def generate_lookup_table(gamma, L=256):
    """Generates a lookup table for the power-law transformation.

    Args:
        gamma (float): The gamma value for the power-law transform.
        L (int): The total number of gray levels (default is 256).

    Returns:
        numpy.ndarray: A lookup table (1D array) mapping input to output gray levels.
    """
    lookup_table = np.array([power_law_transform(i, gamma, L) for i in range(L)])
    return lookup_table

def apply_lookup_table(image_array, lookup_table):
    """Applies a lookup table to an image array.

    Args:
        image_array (numpy.ndarray): The input image as a NumPy array.
        lookup_table (numpy.ndarray): The lookup table to apply.

    Returns:
        numpy.ndarray: The transformed image as a NumPy array.
    """
    return lookup_table[image_array]

def main(img_name):
    try:
        with open(f'{img_name}.raw', 'rb') as raw:
            data = np.frombuffer(raw.read(), dtype=np.uint8)
            grayscale_image = data.reshape((ROWS, COLUMNS))
    except Exception as e:
        print(f"Error: {e}")

def draw_lookup_table(plot=False):
    # Generate lookup tables
    lut_gamma04 = generate_lookup_table(gamma1, L)
    lut_gamma25 = generate_lookup_table(gamma2, L)

    # Plot the transformation curves
    input_levels = np.arange(L)
    output_gamma04 = lut_gamma04
    output_gamma25 = lut_gamma25

    if plot is True:
        plt.figure(figsize=(5, 5))

        plt.plot(input_levels, output_gamma04, label=rf'$\gamma = {gamma1}$')
        plt.xlabel('Input Gray Level (r)')
        plt.ylabel('Output Gray Level (s)')
        plt.legend(loc='upper left')

        plt.plot(input_levels, output_gamma25, label=rf'$\gamma = {gamma2}$')
        plt.xlabel('Input Gray Level (r)')
        plt.ylabel('Output Gray Level (s)')
        plt.legend(loc='upper left')

        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return lut_gamma04, lut_gamma25

def draw_cat_GLT(plot=False):

    try:
        with open("cat.raw", "rb") as f:
            data = np.frombuffer(f.read(), dtype=np.uint8)
            original_image = data.reshape((ROWS, COLUMNS))
    except FileNotFoundError:
        print("Error: 'cat.raw' not found.")
        exit()
    except Exception as e:
        print(f"Error loading 'cat.raw': {e}")
        exit()

    transformed_image_gamma04 = apply_lookup_table(original_image, lut_gamma04)
    transformed_image_gamma25 = apply_lookup_table(original_image, lut_gamma25)

    if plot is True:
        plt.figure(figsize=(15, 5))

        plt.subplot(1, 3, 1)
        plt.imshow(original_image, cmap='gray')
        plt.title('Original Image')

        plt.subplot(1, 3, 2)
        plt.imshow(transformed_image_gamma04, cmap='gray')
        plt.title(f'Transformed Image ($\gamma = {gamma1}$)')

        plt.subplot(1, 3, 3)
        plt.imshow(transformed_image_gamma25, cmap='gray')
        plt.title(f'Transformed Image ($\gamma = {gamma2}$)')

        plt.tight_layout()
        plt.show()

        print("\nDescription of the transformed images:")
        print(f"Image with gamma = {gamma1} (0.4): This transformation with a gamma value less than 1 stretches the intensity values in the darker regions of the original image and compresses the values in the brighter regions. As a result, the transformed image will appear brighter overall, with increased contrast in the darker areas, making details in those regions more visible. The brighter areas might appear somewhat washed out.")
        print(f"Image with gamma = {gamma2} (2.5): This transformation with a gamma value greater than 1 compresses the intensity values in the darker regions and stretches the values in the brighter regions. The transformed image will appear darker overall, with reduced contrast in the darker areas and increased contrast in the brighter areas. Details in the brighter regions will be enhanced, while darker areas might lose some visibility.")


if __name__ == "__main__":
    lut_gamma04, lut_gamma25 = draw_lookup_table(True)
    draw_cat_GLT(True)
