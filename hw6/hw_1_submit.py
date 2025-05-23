import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.fft import fft2, ifft2, fftshift

L = 256
ROWS = 480
COLUMNS = 640

# Parameters
size = 31
half_size = size // 2
sigma = 7.0  # standard deviation, estimated from g(7,0) = A * exp(-49 / (2*sigma^2)) = A * exp(-0.5)
A = 1/291.66706483023165  # Initial guess

# Generate 31x31 Gaussian filter g(i,j)
def gaussian_filter(size, sigma):
    g = np.zeros((size, size), dtype=np.float64)
    for i in range(-half_size, half_size + 1):
        for j in range(-half_size, half_size + 1):
            g[i + half_size, j + half_size] = A * np.exp(-(i**2 + j**2) / (2 * sigma**2))
    print(f"{np.sum(g)=}")
    g /= np.sum(g)  # Normalize so the sum = 1
    return g

def inverse_filter(degraded, kernel, K_regularization=1e-3): # Added K_regularization parameter

    # Ensure inputs are float for FFT
    degraded = degraded.astype(np.float64)
    kernel = kernel.astype(np.float64)

    # 1. Prepare the kernel's DFT (Optical Transfer Function - OTF)
    img_rows, img_cols = degraded.shape
    k_rows, k_cols = kernel.shape
    
    # The input `kernel` has its conceptual (0,0) at its center (k_rows//2, k_cols//2)
    k_center_r, k_center_c = k_rows // 2, k_cols // 2

    psf_padded = np.zeros((img_rows, img_cols), dtype=np.float64)

    # Place the kernel elements into the padded PSF array such that the
    # kernel's center aligns with the (0,0) index of psf_padded (with wrap-around).
    for r_idx in range(k_rows):
        for c_idx in range(k_cols):
            # map kernel index (r_idx, c_idx) to coordinates relative to kernel's center (i, j)
            i = r_idx - k_center_r
            j = c_idx - k_center_c
            
            # map (i,j) to indices in the padded PSF array (with wrap-around for negative indices)
            # (i % img_rows) ensures that negative i wraps around to img_rows + i
            dest_r = (i + img_rows) % img_rows 
            dest_c = (j + img_cols) % img_cols
            psf_padded[dest_r, dest_c] = kernel[r_idx, c_idx]
            
    H = fft2(psf_padded) # Optical Transfer Function (OTF)

    # 2. Get DFT of the degraded image
    Degraded_DFT = fft2(degraded)

    # 3. Perform inverse filtering in frequency domain
    H_conj = np.conj(H)
    H_abs_sq = np.abs(H)**2
    
    Restored_DFT = (H_conj / (H_abs_sq + K_regularization)) * Degraded_DFT

    # 4. Get restored image by inverse DFT
    restored_spatial_complex = ifft2(Restored_DFT)
    restored_image = np.real(restored_spatial_complex)

    return restored_image

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

    # Create the Gaussian kernel
    g = gaussian_filter(size, sigma)
    print(f"{g=} / {sum(sum(g))}")

    # Degrade image by convolution
    degraded = cv2.filter2D(original_image, -1, g)

    # Apply inverse filtering
    restored = inverse_filter(degraded, g)

    # Show images
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    plt.title("Gaussian Filter g(i,j)")
    plt.imshow(g, cmap='gray')

    plt.subplot(2, 2, 2)
    plt.title("Original Image")
    plt.imshow(original_image, cmap='gray', vmin=0, vmax=255)

    plt.subplot(2, 2, 3)
    plt.title("Degraded Image")
    plt.imshow(degraded, cmap='gray', vmin=0, vmax=255)

    plt.subplot(2, 2, 4)
    plt.title("Restored Image")
    plt.imshow(restored, cmap='gray', vmin=0, vmax=255)
    plt.show()

