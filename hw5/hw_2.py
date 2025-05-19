import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import generic_filter, median_filter as scipy_median_filter
from scipy.ndimage import maximum_filter as scipy_maximum_filter, minimum_filter as scipy_minimum_filter

L = 256
ROWS = 256
COLUMNS = 256

# TODO: for each filters, write a brief verbal description of the result. For example, “the resulting image will consist
# of vertical bars 3 pixels wide and 206 pixels high. / The mean filter smooths out the bars and as we increase the kernel size, the bars corners become soewhat visibly rounded while also becoming darker as well” Be sure to describe any deformation of the bars, such as rounded corners. You may ignore image border effects, in which the masks only
# partially contain image pixels.

# Arithmetic Mean filter
def arithmetic_mean_filter(image, size):
    kernel = np.ones((size, size), dtype=np.float32) / (size * size)
    return ndimage.convolve(image, kernel, mode='nearest')

# Geometric Mean Filter
def geometric_mean_filter(image, size):
    def geo_mean(values):
        values = np.maximum(values, 1e-5)  # avoid log(0)
        return np.exp(np.mean(np.log(values)))
    return generic_filter(image.astype(np.float64), geo_mean, size=size)

# Harmonic Mean Filter
def harmonic_mean_filter(image, size):
    def harm_mean(values):
        values = np.maximum(values, 1e-5)
        return len(values) / np.sum(1.0 / values)
    return generic_filter(image.astype(np.float64), harm_mean, size=size)

# Contraharmonic Mean Filter
def contraharmonic_mean_filter(image, size, Q):
    def contra_mean(values):
        values = values.astype(np.float64)
        numerator = np.sum(values ** (Q + 1))
        denominator = np.sum(values ** Q) + 1e-5  # avoid division by zero
        return numerator / denominator
    return generic_filter(image, contra_mean, size=size)

# Median Filter
def median_filter(image, size):
    return scipy_median_filter(image, size=size)

# Maximum Filter
def maximum_filter(image, size):
    return scipy_maximum_filter(image, size=size)

# Minimum Filter
def minimum_filter(image, size):
    return scipy_minimum_filter(image, size=size)

# Midpoint Filter
def midpoint_filter(image, size):
    def midpoint(values):
        return 0.5 * (np.max(values) + np.min(values))
    return generic_filter(image, midpoint, size=size)

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

    # Apply filters
    arith_filtered_3x3 = arithmetic_mean_filter(original_image, 3)
    arith_filtered_7x7 = arithmetic_mean_filter(original_image, 7)
    arith_filtered_9x9 = arithmetic_mean_filter(original_image, 9)

    geo_filtered_3x3 = geometric_mean_filter(original_image, 3)
    geo_filtered_7x7 = geometric_mean_filter(original_image, 7)
    geo_filtered_9x9 = geometric_mean_filter(original_image, 9)

    harm_filtered_3x3 = harmonic_mean_filter(original_image, 3)
    harm_filtered_7x7 = harmonic_mean_filter(original_image, 7)
    harm_filtered_9x9 = harmonic_mean_filter(original_image, 9)

    pos_contra_filtered_3x3 = contraharmonic_mean_filter(original_image, 3, Q=+1)
    pos_contra_filtered_7x7 = contraharmonic_mean_filter(original_image, 7, Q=+1)
    pos_contra_filtered_9x9 = contraharmonic_mean_filter(original_image, 9, Q=+1)

    neg_contra_filtered_3x3 = contraharmonic_mean_filter(original_image, 3, Q=-1)
    neg_contra_filtered_7x7 = contraharmonic_mean_filter(original_image, 7, Q=-1)
    neg_contra_filtered_9x9 = contraharmonic_mean_filter(original_image, 9, Q=-1)

    median_filtered_3x3 = median_filter(original_image, 3)
    median_filtered_7x7 = median_filter(original_image, 7)
    median_filtered_9x9 = median_filter(original_image, 9)

    max_filtered_3x3 = maximum_filter(original_image, 3)
    max_filtered_7x7 = maximum_filter(original_image, 7)
    max_filtered_9x9 = maximum_filter(original_image, 9)

    min_filtered_3x3 = minimum_filter(original_image, 3)
    min_filtered_7x7 = minimum_filter(original_image, 7)
    min_filtered_9x9 = minimum_filter(original_image, 9)

    midpoint_filtered_3x3 = midpoint_filter(original_image, 3)
    midpoint_filtered_7x7 = midpoint_filter(original_image, 7)
    midpoint_filtered_9x9 = midpoint_filter(original_image, 9)

    # Select filter set to display
    filter_name = "harmonic"  # Change this to any of: arithmetic, geometric, harmonic, contraharmonic_pos, contraharmonic_neg, median, max, min, midpoint

    if filter_name == "arithmetic":
        filtered_3x3 = arith_filtered_3x3
        filtered_7x7 = arith_filtered_7x7
        filtered_9x9 = arith_filtered_9x9
    if filter_name == "geometric":
        filtered_3x3 = geo_filtered_3x3
        filtered_7x7 = geo_filtered_7x7
        filtered_9x9 = geo_filtered_9x9
    elif filter_name == "harmonic":
        filtered_3x3 = harm_filtered_3x3
        filtered_7x7 = harm_filtered_7x7
        filtered_9x9 = harm_filtered_9x9
    elif filter_name == "contraharmonic_pos":
        filtered_3x3 = pos_contra_filtered_3x3
        filtered_7x7 = pos_contra_filtered_7x7
        filtered_9x9 = pos_contra_filtered_9x9
    elif filter_name == "contraharmonic_neg":
        filtered_3x3 = neg_contra_filtered_3x3
        filtered_7x7 = neg_contra_filtered_7x7
        filtered_9x9 = neg_contra_filtered_9x9
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
    plt.imshow(filtered_3x3, cmap="gray", vmin=0, vmax=255)
    plt.title("3x3 " + filter_name.capitalize() + " Filter")
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(filtered_7x7, cmap="gray", vmin=0, vmax=255)
    plt.title("7x7 " + filter_name.capitalize() + " Filter")
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.imshow(filtered_9x9, cmap="gray", vmin=0, vmax=255)
    plt.title("9x9 " + filter_name.capitalize() + " Filter")
    plt.axis('off')

    plt.tight_layout()
    plt.show()
