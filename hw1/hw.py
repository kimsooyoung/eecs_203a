import rawpy
import imageio
import numpy as np
from PIL import Image

ROWS = 480
COLUMNS = 640

# Load the RAW image
source_path = "/home/kimsooyoung/Documents/Study/eecs_203a/hw1/triangle.raw"

def to_grayscale(image):
    """Convert a color image to grayscale using a simple average."""
    if image.ndim == 3:
        return np.mean(image, axis=2)
    return image  # Already grayscale

def subsample(image, factor):
    """Subsample image by selecting every nth row and column"""
    return image[::factor, ::factor]

def nearest_neighbor_interpolation(image, target_shape):
    """Upscale using nearest neighbor interpolation"""

    row, col = image.shape
    target_row, target_col = target_shape
    row_scale = target_row / row
    col_scale = target_col / col

    output_img = np.empty(target_shape, dtype=image.dtype)

    for i in range(target_row):
        for j in range(target_col):
            original_row = int(i / row_scale)
            original_col = int(j / col_scale)
            output_img[i, j] = image[original_row, original_col]

    return output_img

def save_image(image, filename):
    """Save image to PNG using PIL"""
    Image.fromarray(image.astype(np.uint8)).save(filename)

def main(img_name):
    try:
        with rawpy.imread(f'{img_name}.raw') as raw:
            color_image  = raw.postprocess()
            grayscale_image = to_grayscale(color_image)

            # 1. Subsample the image (4 level)
            subsample_4 = subsample(grayscale_image, 4)
            # 2. Subsample the image (16 level)
            subsample_16 = subsample(grayscale_image, 16)  # 32 x 32

            # 3. Interpolate back using nearest neighbor (4 level)
            interp_4 = nearest_neighbor_interpolation(
                subsample_4, (ROWS, COLUMNS)
            )
            # 4. Interpolate back using nearest neighbor (16 level)
            interp_16 = nearest_neighbor_interpolation(
                subsample_16, (ROWS, COLUMNS)
            )

            save_image(grayscale_image, "default.png")

            # 5. Save images
            if img_name == "triangle":
                save_image(subsample_4, "triangles4.png")
                save_image(subsample_16, "triangles16.png")
                save_image(interp_4, "trianglei4.png")
                save_image(interp_16, "trianglei16.png")
            elif img_name == "cat":
                save_image(subsample_4, "cats4.png")
                save_image(subsample_16, "cats16.png")
                save_image(interp_4, "cati4.png")
                save_image(interp_16, "cati16.png")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    img_name = "triangle"
    main(img_name)