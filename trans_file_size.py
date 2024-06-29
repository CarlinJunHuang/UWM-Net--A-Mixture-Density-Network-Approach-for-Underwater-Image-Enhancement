# Specify the directory you want to resize images
from PIL import Image
import os
import glob

directory = 'ILSVRC2012_test_00005808.png'
size = (height := 256, width := 256)


img = Image.open("497.png")
img_resized = img.resize(size, Image.Resampling.LANCZOS)
img_resized.save("497.png")