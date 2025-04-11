import sys
import rawpy
import numpy as np

ROWS = 480
COLUMNS = 640

def main():
    
    path = 'triangle.raw'

    try:
        with rawpy.imread(path) as raw:
            image = raw.postprocess()
            print(f"{image.size=}")
            if image.size != ROWS * COLUMNS:
                raise ValueError("Not enough data in input file")
            image = image.reshape((ROWS, COLUMNS))
            # TODO: Show image
            # TODO: subsamples the image by 4 to 128 * 128 img
            # TODO: subsamples the image by 16 to 32 * 32 img
            # TODO: use nearest neighbor interpolation to transform 4 subsampled image to a 512 * 512 image
            # TODO: use nearest neighbor interpolation to transform 16 subsampled image to a 512 * 512 image
    except Exception as e:
        print(f"Error: couldn't open or read from {path}: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        # TODO: Save each images 
        # 1 - 4 subsampled
        # 2 - 16 subsampled
        # 3 - 4 interpolated 
        # 4 - 16 interpolated 
        with open(ofile, 'wb') as f:
            image.tofile(f)
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main()
