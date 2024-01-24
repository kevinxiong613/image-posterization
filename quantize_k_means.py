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

    colors = set() # Make a set of the colors because we don't want duplicates

    for i in range(K):
        new_color = pix[random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        while new_color in colors:
            new_color = pix[random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        colors.add(new_color) # Generate k distinct colors in the picture
    means = dict()
    for color in colors:
        means[color] = list() # Use the dictionary to keep track of colors associated with this one

    for h in range(HEIGHT): # Do the first iteration of k-means to put the colors in
        for w in range(WIDTH):
            rgb = pix[w, h] # Find the mean with the lowest squared error for this rgb value
            smallest_error = 100000000000
            smallest_mean = None
            for mean in means:
                error = squared_error(mean, rgb)
                if error < smallest_error:
                    smallest_error = error
                    smallest_mean = mean
            means[smallest_mean].append(rgb) # Add this rgb value to that particular mean that resulted in the lowest squared error
    return means

"""
Calculate squared error between two RGB values by doing summation (v1-v2)^2
"""
def squared_error(rgb1, rgb2):
    return (rgb1[0]-rgb2[0]) ** 2 + (rgb1[1]-rgb2[1]) ** 2 + (rgb1[2]-rgb2[2]) ** 2

def calc_averages
def k_means():
    means = choose_initial_pixels()
    old_keys = set([mean for mean in means]) # Grab the means for the old keys
    changed = True
    while changed:
        for mean in means:
            avg_r = 0
            avg_g = 0
            avg_b = 0
            count = 0
            for i in range(len(means[mean])): # Iterate through all the rgb values
                curr_rgb = means[mean][i]
                avg_r += curr_rgb[0]
                avg_g += curr_rgb[1]
                avg_b += curr_rgb[2]
                count += 1
            new_avg = (avg_r//count, avg_g//count, avg_b//count)
            means[new_avg] = means.pop(mean) # Create a new key with the old key's values

        return

print(choose_initial_pixels())