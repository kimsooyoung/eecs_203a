import numpy as np
import matplotlib.pyplot as plt

# Define image dimensions and intensity values
ROWS = 10
COLUMNS = 10
INTENSITY_P = 255  # Intensity of the polygon
INTENSITY_O = 0    # Intensity of the background

# Equation of the polygon edge: y = 0.3x

def generate_image_pixel_center_sampling():
    """
    Generates a 10x10 image by sampling the continuous data at pixel centers.
    (Part a)
    """
    image = np.zeros((ROWS, COLUMNS), dtype=np.uint8)

    for i in range(ROWS):  # Iterate through rows (y-coordinate, from bottom to top)
        for j in range(COLUMNS): # Iterate through columns (x-coordinate, from left to right)
            # Calculate continuous coordinates of the pixel center
            # Assuming (0,0) is the bottom-left corner of the first pixel
            x_center = j + 0.5
            y_center = i + 0.5

            # Check if the pixel center is below the line y = 0.3x
            if y_center < 0.3 * x_center:
                image[ROWS - 1 - i, j] = INTENSITY_P # Assign P if below the line
            else:
                image[ROWS - 1 - i, j] = INTENSITY_O # Assign 0 if above or on the line
    return image

def generate_image_box_filter_antialiasing(subpixel_grid_size=10):
    """
    Generates a 10x10 image using an antialiasing algorithm that averages
    intensity over each pixel area (box filter).
    (Part b)
    """
    image = np.zeros((ROWS, COLUMNS), dtype=np.float32) # Use float for fractional intensities

    for i in range(ROWS):  # Iterate through rows (y-coordinate, from bottom to top)
        for j in range(COLUMNS): # Iterate through columns (x-coordinate, from left to right)
            count_P = 0 # Counter for subpixels covered by polygon
            total_subpixels = subpixel_grid_size * subpixel_grid_size

            # Iterate through subpixels within the current pixel
            for sy in range(subpixel_grid_size):
                for sx in range(subpixel_grid_size):
                    # Calculate continuous coordinates of the subpixel center
                    x_sub_center = j + (sx + 0.5) / subpixel_grid_size
                    y_sub_center = i + (sy + 0.5) / subpixel_grid_size

                    # Check if the subpixel center is below the line y = 0.3x
                    if y_sub_center < 0.3 * x_sub_center:
                        count_P += 1

            # Calculate the fraction of the pixel covered by the polygon
            fraction_P = count_P / total_subpixels
            # Assign the average intensity to the pixel
            image[ROWS - 1 - i, j] = INTENSITY_P * fraction_P + INTENSITY_O * (1 - fraction_P) # Background is 0

    return image.astype(np.uint8) # Convert back to uint8 for display

# --- Main execution ---
if __name__ == "__main__":
    # Part a: Pixel center sampling
    image_a = generate_image_pixel_center_sampling()

    # Part b: Box filter antialiasing
    image_b = generate_image_box_filter_antialiasing(subpixel_grid_size=100) # Increased subpixel_grid_size for better accuracy

    # Plotting the results
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(image_a, cmap='gray', origin='upper', extent=[0, COLUMNS, 0, ROWS])
    axes[0].set_title('Part a: Pixel Center Sampling')
    axes[0].set_xlabel('X (pixels)')
    axes[0].set_ylabel('Y (pixels)')
    axes[0].set_xticks(np.arange(0, COLUMNS + 1, 1))
    axes[0].set_yticks(np.arange(0, ROWS + 1, 1))
    axes[0].grid(True, color='red', linestyle='--', linewidth=0.5)
    # Add labels for pixel coordinates (bottom-left is 0,0)
    for r in range(ROWS):
        for c in range(COLUMNS):
            axes[0].text(c + 0.5, ROWS - 1 - r + 0.5, f'({c},{r})', color='blue', ha='center', va='center', fontsize=6)


    axes[1].imshow(image_b, cmap='gray', origin='upper', extent=[0, COLUMNS, 0, ROWS])
    axes[1].set_title('Part b: Box Filter Antialiasing')
    axes[1].set_xlabel('X (pixels)')
    axes[1].set_ylabel('Y (pixels)')
    axes[1].set_xticks(np.arange(0, COLUMNS + 1, 1))
    axes[1].set_yticks(np.arange(0, ROWS + 1, 1))
    axes[1].grid(True, color='red', linestyle='--', linewidth=0.5)
    # Add labels for pixel coordinates (bottom-left is 0,0)
    for r in range(ROWS):
        for c in range(COLUMNS):
            axes[1].text(c + 0.5, ROWS - 1 - r + 0.5, f'({c},{r})', color='blue', ha='center', va='center', fontsize=6)


    plt.tight_layout()
    plt.show()

    # Print pixel values for better inspection
    print("--- Part a: Pixel Values (Pixel Center Sampling) ---")
    print(image_a)
    print("\n--- Part b: Pixel Values (Box Filter Antialiasing) ---")
    print(image_b)