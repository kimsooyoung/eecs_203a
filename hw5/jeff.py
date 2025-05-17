import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

L = 256
ROWS = 256
COLUMNS = 256

class Filter:

    def mean(image: np.ndarray, size: int):
        # build uniform kernel
        kernel = np.ones((size, size), dtype=np.float32) / (size*size)
        return cv2.filter2D(image, ddepth=-1, kernel=kernel)

    def geo_mean(image:np.ndarray, size: int, eps: float = 1e-9):
        img_f = image.astype(np.float32) + eps
        logs = np.log(img_f)
        # sum logs with a box filter
        sum_logs = cv2.filter2D(
            logs,
            ddepth=-1,
            kernel=np.ones((size, size), dtype=np.float32),
            borderType=cv2.BORDER_REPLICATE
        )

        # exponentiate average log
        g = np.exp(sum_logs / (size*size))
        
        # clip & cast back
        if np.issubdtype(image.dtype, np.integer):
            g = np.clip(g, 0, 255)
            return g.astype(image.dtype)
        return g

    def harmonic(image: np.ndarray, size: int, eps: float = 1e-6):

        if size < 1 or size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer")
        
        img_f = image.astype(np.float32) + eps
        reciprocals = 1.0 / img_f
        # sum reciprocals in box
        sum_rec = cv2.filter2D(
            reciprocals,
            ddepth=-1,
            kernel=np.ones((size, size), dtype=np.float32),
            borderType=cv2.BORDER_REPLICATE
        )
        # harmonic mean
        h = (size * size) / sum_rec
        return np.clip(h, 0, 255).astype(image.dtype)

    def contraharmonic(image: np.ndarray,
        size: int,
        Q: float,
        eps: float = 1e-6) -> np.ndarray:

        if size < 1 or size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer")
        img_f = image.astype(np.float32) + eps
        kernel = np.ones((size, size), dtype=np.float32)

        # numerator: sum of I^(Q+1)
        num = cv2.filter2D(img_f**(Q + 1), ddepth=-1, kernel=kernel)

        # denominator: sum of I^Q
        den = cv2.filter2D(img_f**Q, ddepth=-1, kernel=kernel)

        # contraharmonic ratio
        ch_full = num / den

        # crop off borders
        pad = size // 2
        ch_valid = ch_full[pad:-pad, pad:-pad]

        return np.clip(ch_valid, 0, 255).astype(image.dtype)

    def median(image: np.ndarray, size: int):

        if size < 1 or size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer")
        # OpenCV’s medianBlur expects a single-channel uint8 image
        return cv2.medianBlur(image, size)

    def max(image: np.ndarray, size: int) -> np.ndarray:
        if size < 1 or size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer")
        kernel = np.ones((size, size), dtype=np.uint8)
        return cv2.dilate(image, kernel)    

    def min(image: np.ndarray, size: int) -> np.ndarray:
        if size < 1 or size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer")
        kernel = np.ones((size, size), dtype=np.uint8)
        return cv2.erode(image, kernel)

    def midpoint(image: np.ndarray, size: int) -> np.ndarray:
        # compute max and min
        max_img = Filter.max(image, size)
        min_img = Filter.min(image, size)
        # average them
        mid = (max_img.astype(np.float32) + min_img.astype(np.float32)) / 2
        return np.clip(mid, 0, 255).astype(image.dtype)

def plot_filters(original: np.ndarray,
                 filtered: dict[int, np.ndarray],
                 title_prefix: str = "Image"):
    ncols = 1 + len(filtered)
    fig, axs = plt.subplots(1, ncols, figsize=(4*ncols, 4))
    
    # plot original
    axs[0].imshow(original, cmap="gray")
    axs[0].set_title(f"{title_prefix} – original")
    axs[0].axis("off")
    
    # plot each filtered
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
            # data = np.fromfile(f, dtype=np.uint8)
            data = np.frombuffer(f.read(), dtype=np.uint8)
            original_image = data.reshape((ROWS, COLUMNS))
    except FileNotFoundError:
        print(f"Error: '{image_name}.raw' not found.")
        exit()
    except Exception as e:
        print(f"Error loading '{image_name}.raw': {e}")
        exit()

    kernels = [3, 7, 9]

    filtered = {k: Filter.harmonic(original_image, k) for k in kernels}
    plot_filters(original_image, filtered, title_prefix="Filter")

