import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve, median_filter, maximum_filter, minimum_filter

L = 256
ROWS = 256
COLUMNS = 256

class Filter:

    @staticmethod
    def mean(image: np.ndarray, size: int):
        kernel = np.ones((size, size), dtype=np.float32) / (size * size)
        return convolve(image, kernel, mode='reflect')

    @staticmethod
    def geo_mean(image: np.ndarray, size: int, eps: float = 1e-9):
        img_f = image.astype(np.float32) + eps
        logs = np.log(img_f)
        sum_logs = convolve(logs, np.ones((size, size), dtype=np.float32), mode='reflect')
        g = np.exp(sum_logs / (size * size))
        if np.issubdtype(image.dtype, np.integer):
            g = np.clip(g, 0, 255)
            return g.astype(image.dtype)
        return g

    @staticmethod
    def harmonic(image: np.ndarray, size: int, eps: float = 1e-6):
        if size < 1 or size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer")
        img_f = image.astype(np.float32) + eps
        reciprocals = 1.0 / img_f
        sum_rec = convolve(reciprocals, np.ones((size, size), dtype=np.float32), mode='reflect')
        h = (size * size) / sum_rec
        return np.clip(h, 0, 255).astype(image.dtype)

    @staticmethod
    def contraharmonic(image: np.ndarray, size: int, Q: float, eps: float = 1e-6):
        if size < 1 or size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer")
        img_f = image.astype(np.float32) + eps
        num = convolve(img_f ** (Q + 1), np.ones((size, size), dtype=np.float32), mode='reflect')
        den = convolve(img_f ** Q, np.ones((size, size), dtype=np.float32), mode='reflect')
        ch = num / den
        pad = size // 2
        ch_valid = ch[pad:-pad, pad:-pad]
        return np.clip(ch_valid, 0, 255).astype(image.dtype)

    @staticmethod
    def median(image: np.ndarray, size: int):
        if size < 1 or size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer")
        return median_filter(image, size=size, mode='reflect')

    @staticmethod
    def max(image: np.ndarray, size: int):
        if size < 1 or size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer")
        return maximum_filter(image, size=size, mode='reflect')

    @staticmethod
    def min(image: np.ndarray, size: int):
        if size < 1 or size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer")
        return minimum_filter(image, size=size, mode='reflect')

    @staticmethod
    def midpoint(image: np.ndarray, size: int):
        max_img = Filter.max(image, size)
        min_img = Filter.min(image, size)
        mid = (max_img.astype(np.float32) + min_img.astype(np.float32)) / 2
        return np.clip(mid, 0, 255).astype(image.dtype)

def plot_filters(original: np.ndarray,
                 filtered: dict[int, np.ndarray],
                 title_prefix: str = "Image"):
    ncols = 1 + len(filtered)
    fig, axs = plt.subplots(1, ncols, figsize=(4*ncols, 4))
    
    axs[0].imshow(original, cmap="gray")
    axs[0].set_title(f"{title_prefix} – original")
    axs[0].axis("off")
    
    for ax, (k, img_filt) in zip(axs[1:], sorted(filtered.items())):
        ax.imshow(img_filt, cmap="gray", vmin=0, vmax=255)
        ax.set_title(f"{title_prefix} – {k}×{k}")
        ax.axis("off")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":

    image_name = "stripes"

    try:
        with open(f"{image_name}.raw", "rb") as f:
            data = np.frombuffer(f.read(), dtype=np.uint8)
            original_image = data.reshape((ROWS, COLUMNS))
    except FileNotFoundError:
        print(f"Error: '{image_name}.raw' not found.")
        exit()
    except Exception as e:
        print(f"Error loading '{image_name}.raw': {e}")
        exit()

    filter_name = "harmonic"  # Change this to any of: arithmetic, geometric, harmonic, contraharmonic_pos, contraharmonic_neg, median, max, min, midpoint

    # Apply filters
    kernels = [3, 7, 9]
    # plot_filters(original_image, filtered, title_prefix="Harmonic Filter")

    # Select filter set to display
    filter_name = "geometric"  # Change this to any of: arithmetic, geometric, harmonic, contraharmonic_pos, contraharmonic_neg, median, max, min, midpoint

    if filter_name == "geometric":
        filtered = {k: Filter.geo_mean(original_image, k) for k in kernels}
    elif filter_name == "harmonic":
        filtered = {k: Filter.harmonic(original_image, k) for k in kernels}
    elif filter_name == "contraharmonic_pos":
        filtered = {k: Filter.contraharmonic(original_image, k, Q = 1) for k in kernels}
    elif filter_name == "contraharmonic_neg":
        filtered = {k: Filter.contraharmonic(original_image, k, Q = -1) for k in kernels}
    elif filter_name == "median":
        filtered_3x3 = median_filtered_3x3
        filtered_7x7 = median_filtered_7x7
        filtered_9x9 = median_filtered_9x9
    elif filter_name == "max":
        filtered_3x3 = max_filtered_3x3
        filtered_7x7 = max_filtered_7x7
        filtered_9x9 = max_filtered_9x9
    elif filter_name == "min":
        filtered_3x3 = min_filtered_3x3
        filtered_7x7 = min_filtered_7x7
        filtered_9x9 = min_filtered_9x9
    elif filter_name == "midpoint":
        filtered_3x3 = midpoint_filtered_3x3
        filtered_7x7 = midpoint_filtered_7x7
        filtered_9x9 = midpoint_filtered_9x9
    else:
        print("Invalid filter name")
        exit()

    # Show images
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.imshow(original_image, cmap="gray", vmin=0, vmax=255)
    plt.title("Original Image")
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.imshow(filtered[3], cmap="gray", vmin=0, vmax=255)
    plt.title("3x3 " + filter_name.capitalize() + " Filter")
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(filtered[7], cmap="gray", vmin=0, vmax=255)
    plt.title("7x7 " + filter_name.capitalize() + " Filter")
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.imshow(filtered[9], cmap="gray", vmin=0, vmax=255)
    plt.title("9x9 " + filter_name.capitalize() + " Filter")
    plt.axis('off')

    plt.tight_layout()
    plt.show()
