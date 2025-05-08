import numpy as np
import matplotlib.pyplot as plt

L = 256
ROWS = 480
COLUMNS = 640

def compute_dft_magnitude(image):
    # Compute 2D Fourier Transform
    f = np.fft.fft2(image)
    f_shifted = np.fft.fftshift(f)  # Shift DC to center
    magnitude = np.abs(f_shifted)
    
    # Use logarithmic scaling for visibility
    magnitude_log = np.log1p(magnitude)  # log(1 + |F(u,v)|)
    
    # Normalize to 0–255
    magnitude_normalized = (magnitude_log / magnitude_log.max()) * 255
    return magnitude_normalized.astype(np.uint8)

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

    # Compute DFT magnitudes
    dft_image = compute_dft_magnitude(original_image)

    # show_images
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(original_image, cmap='gray')
    plt.title(f"Original Image {image_name}")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(dft_image, cmap='gray')
    plt.title(f"DFT Magnitude {image_name}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()