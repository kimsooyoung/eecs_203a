import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROWS = 512
COLUMNS = 512

def subsample(image, factor):
    """Subsample image by selecting every nth row and column"""
    return image[::factor, ::factor]

def nearest_neighbor_interpolation(image, target_shape):
    """Upscale using nearest neighbor interpolation"""
    zoom_y = target_shape[0] // image.shape[0]
    zoom_x = target_shape[1] // image.shape[1]
    return image.repeat(zoom_y, axis=0).repeat(zoom_x, axis=1)

def save_image(image, filename):
    """Save image to PNG using PIL"""
    Image.fromarray(image.astype(np.uint8)).save(filename)

def show_image(image, title='Image'):
    """Display image using matplotlib"""
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

def main():
    try:
        with open('cat.raw', 'rb') as f:
            image = np.fromfile(f, dtype=np.uint64, count=ROWS * COLUMNS)
            print(f"{image.size=}")
            # 640*480 = 307,200
            if image.size != ROWS * COLUMNS: 
                raise ValueError("Not enough data in input file")
            image = image.reshape((ROWS, COLUMNS))

            # ✅ Show original image
            show_image(image, title="Original Image")

            # ✅ Subsample the image
            subsample_4 = subsample(image, 4)  # 128 x 128
            subsample_16 = subsample(image, 16)  # 32 x 32

            # ✅ Interpolate back to 512 x 512 using nearest neighbor
            interp_4 = nearest_neighbor_interpolation(subsample_4, (ROWS, COLUMNS))
            interp_16 = nearest_neighbor_interpolation(subsample_16, (ROWS, COLUMNS))

            # ✅ Show all images
            show_image(subsample_4, title="Subsampled by 4 (128x128)")
            show_image(subsample_16, title="Subsampled by 16 (32x32)")
            show_image(interp_4, title="Interpolated from 128x128")
            show_image(interp_16, title="Interpolated from 32x32")

            # ✅ Save images
            save_image(subsample_4, "subsample_4.png")
            save_image(subsample_16, "subsample_16.png")
            save_image(interp_4, "interp_4.png")
            save_image(interp_16, "interp_16.png")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
