from numpy import *
from PIL import Image

enc = Image.open(r"enc.png")
img = array(enc)

key = [41, 37, 23]

a, b, c = img.shape

for x in range (0, a):
    for y in range (0, b):
        pixel = img[x, y]
        for i in range(0,3):
            pixel[i] = pixel[i] * key[i] % 251
        img[x][y] = pixel

flag = Image.fromarray(img)
flag.save('flag.png')
