import random
from PIL import Image

img = Image.open("puppy.jpg") # Just put the local filename in quotes.
img.show() # Send the image to your OS to be displayed as a temporary file (the before picture)
WIDTH, HEIGHT = img.size
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.
K = 8

"""
Chooses the initial K pixels to begin K-means clustering
Input: N/A
Output: List of the K pixels
"""
def choose_initial_pixels():

    color1 = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    colors = set([color1])

    for i in range(K):
        new_color = color1
        while new_color in colors:
            new_color = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        colors.add(new_color)
    return list(colors)

print(choose_initial_pixels())

