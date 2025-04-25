import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import convolve

L = 256
ROWS = 480
COLUMNS = 640

if __name__ == "__main__":

    # image_name = "cat" 
    # or 
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

    # Apply an 11 × 11 median filter to the triangle image and the cat image. For this
    # filter, you can let all 121 coefficients be 1 and scale the result by 1/121. Use pixel replication
    # for the boundaries so that the input and output images are the same size. 
    
    # Also submit a plot of the gray level histogram for the
    # triangle and the cat image and the gray level histogram for the two filtered images

