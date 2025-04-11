import rawpy
import imageio

path = 'cat.raw'
raw = rawpy.imread(path)
rgb = raw.postprocess()
print(len(rgb), len(rgb[0]))
# imageio.imsave('default.jpg', raw)