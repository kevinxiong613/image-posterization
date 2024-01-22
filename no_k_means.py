from PIL import Image

# Attempting vector quantization without K-means clustering

img = Image.open("RoadImage.png") # Just put the local filename in quotes.
img.show() # Send the image to your OS to be displayed as a temporary file (the before picture)
width, height = img.size
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.

def quantization27(): # Restrict to 3 values each gives 27 possible colors
    for h in range(height):
        for w in range(width):
            r, g, b = pix[w, h] # Get the current rgb values at this pixel location
            r2, g2, b2 = 127, 127, 127
            if r < (255//3):
                r2 = 0
            elif r > (255*2)//3:
                r2 = 255

            if g < (255//3):
                g2 = 0
            elif g > (255*2)//3:
                g2 = 255

            if b < (255//3):
                b2 = 0
            elif b > (255*2)//3:
                b2 = 255

            pix[w, h] = (r2, g2, b2) # Set the pixel to these new RGB values

def quantization8(): # Restrict to 2 values each gives 8 possible colors
    for h in range(height):
        for w in range(width):
            r, g, b = pix[w, h] # Get the current rgb values at this pixel location
            r2, g2, b2 = 255, 255, 255
            if r < 128:
                r2 = 0

            if g < 128:
                g2 = 0

            if b < 128:
                b2 = 0
            pix[w, h] = (r2, g2, b2) # Set the pixel to these new RGB values

quantization8()
img.show() # View the new image
img.save("my_image.png") # Save the resulting image. Alter your filename as necessary.

