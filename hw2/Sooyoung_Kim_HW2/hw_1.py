import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

L = 256
gamma1 = 0.4
gamma2 = 2.5

ROWS = 480
COLUMNS = 640

def power_law_transform(gray_level, gamma, L=256):
    tf = int(((gray_level / (L - 1)) ** gamma) * (L - 1))
    return np.clip(np.floor(tf + 0.5), 0, L-1).astype(np.uint8)

def generate_lookup_table(gamma, L=256):
    lookup_table = np.array([power_law_transform(i, gamma, L) for i in range(L)])
    return lookup_table

def apply_lookup_table(image_array, lookup_table):
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

    if plot is True:
        plt.figure(figsize=(5, 5))

        plt.plot(input_levels, lut_gamma04, label=rf'$\gamma = {gamma1}$')
        plt.xlabel('Input Gray Level (r)')
        plt.ylabel('Output Gray Level (s)')
        plt.legend(loc='upper left')

        plt.plot(input_levels, lut_gamma25, label=rf'$\gamma = {gamma2}$')
        plt.xlabel('Input Gray Level (r)')
        plt.ylabel('Output Gray Level (s)')
        plt.legend(loc='upper left')

        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return lut_gamma04, lut_gamma25

def draw_cat_GLT(transform_1, transform_2, plot=False):

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

    transformed_image_gamma04 = apply_lookup_table(original_image, transform_1)
    transformed_image_gamma25 = apply_lookup_table(original_image, transform_2)

    if plot is True:
        plt.figure(figsize=(15, 5))

        plt.subplot(1, 3, 1)
        plt.imshow(original_image, cmap='gray', vmin=0, vmax=255)
        plt.title('Original Image')

        plt.subplot(1, 3, 2)
        plt.imshow(transformed_image_gamma04, cmap='gray', vmin=0, vmax=255)
        plt.title(f'Transformed Image ($\gamma = {gamma1}$)')

        plt.subplot(1, 3, 3)
        plt.imshow(transformed_image_gamma25, cmap='gray', vmin=0, vmax=255)
        plt.title(f'Transformed Image ($\gamma = {gamma2}$)')

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    lut_gamma04, lut_gamma25 = draw_lookup_table(True)
    draw_cat_GLT(lut_gamma04, lut_gamma25, True)
