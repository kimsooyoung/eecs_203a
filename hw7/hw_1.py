import cv2
import numpy as np
import matplotlib.pyplot as plt


L = 256
ROWS = 480
COLUMNS = 640


if __name__ == "__main__":

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

    # TODO
    # Create an input color image where the R(x,y), G(x,y), B(x,y) bands
    # are defined by scaling the triangle gray-level image using R(x,y) = triangle(x,y), G(x,y)=
    # 0.5*triangle(x,y), B(x,y) = 0.2*triangle(x,y). Round non-integer values to the nearest inte-
    # ger so that each band is represented by an 8-bit non-negative integer. Filter each band of
    # the input color image separately using the Gaussian lowpass filter from Homework 6 to ob-
    # tain R′(x, y), G′(x, y), B′(x, y). Create a filtered color image where the bands are defined by
    # R′(x, y), G′(x, y), B′(x, y). Submit the displayable input color image and the displayable filtered
    # color image.

    # Show images
    plt.figure(figsize=(12, 8))
    