from PIL import Image

img = Image.open('breathe.jpg')
img2 = Image.open('output.png')
width, height = img.size

extracted_bin = []
byte = []
for x in range(0, width):
 for y in range(0, height):
  pixel = list(img.getpixel((x, y)))
  pix = list(img2.getpixel((x,y)))
  for n in range(0,3):
   extracted_bin.append(pixel[n]&pix[n])

data = "".join([str(x) for x in extracted_bin])
print(data)
