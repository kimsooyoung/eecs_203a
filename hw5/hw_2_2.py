import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import generic_filter, median_filter as scipy_median_filter, maximum_filter as scipy_max_filter, minimum_filter as scipy_min_filter

L = 256
ROWS = 256
COLUMNS = 256

# TODO 1: Implement each filters
# You may ignore image border effects, in which the masks only
# partially contain image pixels.

# TODO 2: Add comments that brief verbal description of the result. 
# For example, “the resulting image will consist of vertical bars 3 pixels wide and 206 pixels high.” 
# Be sure to describe any deformation of the bars, such as rounded corners. 

# Geometric Mean Filter
def geometric_mean_filter(image, size):
    def geo_mean(values):
        product = np.prod(values + 1e-8)  # Avoid log(0)
        return product ** (1.0 / len(values))
    filtered = generic_filter(image.astype(float), geo_mean, size=(size, size))
    # Description: Smooths the image while preserving edge transitions better than arithmetic mean. Bars may appear slightly blurred but sharpness mostly retained.
    return filtered.astype(np.uint8)

# Harmonic Mean Filter
def harmonic_mean_filter(image, size):
    def harm_mean(values):
        values = values.astype(float) + 1e-8  # Prevent division by zero
        return len(values) / np.sum(1.0 / values)
    filtered = generic_filter(image.astype(float), harm_mean, size=(size, size))
    # Description: Reduces Gaussian noise while preserving edge definition. Dark regions tend to be preserved better than bright.
    return filtered.astype(np.uint8)

# Contraharmonic Mean Filter
def contraharmonic_mean_filter(image, size, Q):
    def contra_mean(values):
        values = values.astype(float)
        numerator = np.sum(values ** (Q + 1))
        denominator = np.sum(values ** Q) + 1e-8  # Avoid division by zero
        return numerator / denominator
    filtered = generic_filter(image.astype(float), contra_mean, size=(size, size))
    # Description: Q > 0 reduces pepper noise; Q < 0 reduces salt noise. Stripes may appear faded or smoothed depending on noise and Q.
    return filtered.astype(np.uint8)

# Median Filter
def median_filter(image, size):
    filtered = scipy_median_filter(image, size=size)
    # Description: Removes salt-and-pepper noise effectively. Stripes will remain mostly intact unless very thin.
    return filtered

# Maximum Filter
def maximum_filter(image, size):
    filtered = scipy_max_filter(image, size=size)
    # Description: Brightens image by enhancing light regions. Dark stripes may get reduced or disappear depending on width.
    return filtered

# Minimum Filter
def minimum_filter(image, size):
    filtered = scipy_min_filter(image, size=size)
    # Description: Darkens image by enhancing dark regions. White areas between dark stripes may shrink or disappear.
    return filtered

# Midpoint Filter
def midpoint_filter(image, size):
    def midpoint(values):
        return (np.max(values) + np.min(values)) / 2.0
    filtered = generic_filter(image.astype(float), midpoint, size=(size, size))
    # Description: Smooths image by averaging extreme values. Bars may appear rounded or blurred depending on filter size.
    return filtered.astype(np.uint8)

if __name__ == "__main__":

    image_name = "stripes"

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

    # Apply filters
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
    plt.imshow(original_image, cmap='gray')
    plt.title("Original Image")
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.imshow(filtered_3x3, cmap='gray')
    plt.title("3x3 " + filter_name.capitalize() + " Filter")
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(filtered_7x7, cmap='gray')
    plt.title("7x7 " + filter_name.capitalize() + " Filter")
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.imshow(filtered_9x9, cmap='gray')
    plt.title("9x9 " + filter_name.capitalize() + " Filter")
    plt.axis('off')

    plt.tight_layout()
    plt.show()
