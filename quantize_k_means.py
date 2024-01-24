import random
from PIL import Image

img = Image.open("puppy.jpg") # Just put the local filename in quotes.
img.show() # Send the image to your OS to be displayed as a temporary file (the before picture)
WIDTH, HEIGHT = img.size
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.
K = 8

"""
Chooses the initial K pixels to begin K-means clustering
Input: Nothing
Output:
means (list of tuples) - a list of the randomly selected, distinct pixels' rgb values to begin k_means clustering
result_list (list of sets) - a list of sets of rgb values representing pixels with that rgb value in the picture. The set they are put in depends on which mean gives the least squared error. They will be put into the set in result_list with the same index as that mean in the means list
"""
def choose_initial_pixels():

    colors = set() # Make a set of the colors because we don't want duplicates
    for i in range(K):
        new_color = pix[random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)]
        while new_color in colors: # Keep generating new colors until we get a distinct one from the image
            new_color = pix[random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)]
        colors.add(new_color) 
    means = list()
    result_list = list()
    for color in colors:
        means.append(color) # Keep a list of all the initial "means"
        result_list.append(set()) # Instantiate an empty list of sets to keep track of which rgb values go to which mean based on associated index
    
    # First pass, count up all the colors, we don't want to do REPEATED WORK with different pixels that have the same RGB value
    count = dict()
    for h in range(HEIGHT):
        for w in range(WIDTH):
            rgb = pix[w,h] # This will return the rgb values as a tuple for the image
            count[rgb] = count.get(rgb, 0) + 1
    
    for color in count:
        rgb = color  # Find the mean with the lowest squared error for this rgb value
        smallest_error = 100000000000 # Initialize to some random large arbitrary value
        smallest_mean = -1
        for i in range(len(means)): 
            error = squared_error(means[i], rgb)
            if error < smallest_error: # Get the index of the mean with the smallest error
                smallest_error = error
                smallest_mean = i
        result_list[smallest_mean].add((color, count[color])) # Add this rgb value to the same index that the smallest_mean was at as a tuple with how many of this color there are too

    return means, result_list

"""
Calculate squared error between two RGB values by doing summation (v1-v2)^2
Input:
rgb1 (tuple) - The first rgb value in consideration
rgb2 (tuple) - The second rgb value in consideration
Output:
The squared error (float) between the two rgb values
"""
def squared_error(rgb1, rgb2):
    return (rgb1[0]-rgb2[0]) ** 2 + (rgb1[1]-rgb2[1]) ** 2 + (rgb1[2]-rgb2[2]) ** 2

"""
Recalculates the averages for the means list depending on the contents of the result_List
Input:
means (list of tuples) - a list of the randomly selected, distinct pixels' rgb values to begin k_means clustering
result_list (list of sets) - a list of rgb values representing pixels with that rgb value in the picture. The set they are put in depends on which mean gives the least squared error. They will be put into the set in result_list with the same index as that mean in the means list
Output:
means (list of tuples) - the updated list of mean rgbs
"""
def calc_averages(means, result_list):
    for i in range(len(result_list)):
        avg_r = 0
        avg_g = 0
        avg_b = 0
        count = 0
        for rgb_tuple in result_list[i]: # Iterate through all the rgb values for this mean
            curr_rgb = rgb_tuple[0]
            rgb_occurences = rgb_tuple[1] # Get the occurences because they DO play a factor
            avg_r += curr_rgb[0] * rgb_occurences
            avg_g += curr_rgb[1] * rgb_occurences
            avg_b += curr_rgb[2] * rgb_occurences
            count += rgb_occurences # Count the number of occurences for this mean is so that we can average it
        new_avg = (avg_r/count, avg_g/count, avg_b/count)
        means[i] = new_avg # Change this to be the newly calculated mean
    return means
"""
Runs the k_means clustering algorithm using the helper methods above until the mean rgbs no longer change, meaning the clusters have been finalized
Input:
N/A
Output:
means (list of tuples) - a list of the randomly selected, distinct pixels' rgb values to begin k_means clustering
result_list (list of sets) - a list of rgb values representing pixels with that rgb value in the picture. The set they are put in depends on which mean gives the least squared error. They will be put into the set in result_list with the same index as that mean in the means list
"""
def k_means():
    means, result_list = choose_initial_pixels()

    means = calc_averages(means, result_list) # Recalculate the means based on what we added in the first batch

    changed = True # Use this variable to keep track of if any means changed
    while changed:
        to_move = list()

        for i in range(len(result_list)): # Iterate through every mean cluster
            for rgb_tuple in result_list[i]: # Go through all the rgb values associated with this particular mean cluster
                curr_rgb = rgb_tuple[0] # The goal is to see if there is a different mean that has less squared error with this rgb value
                smallest_error = 1000000
                smallest_mean = -1
                for mean_index in range(len(means)): # Find the index of the mean that works best for this rgb
                    rgb1, rgb2 = means[mean_index], curr_rgb
                    error = (rgb1[0]-rgb2[0]) ** 2 + (rgb1[1]-rgb2[1]) ** 2 + (rgb1[2]-rgb2[2]) ** 2 # Calculate squared error
                    if error < smallest_error:
                        smallest_error = error
                        smallest_mean = mean_index
                if smallest_mean != i: # If the index of the mean with the least squared error isn't the one it already is in, queue it up for moving (can't move now since we are iterating through the object)
                    to_move.append((i, smallest_mean, rgb_tuple)) # Keep track of 1. the index of the mean the rgb is currently at 2. the index of the mean we will move it to 3. The tuple representing the rgb itself and it's count to remove it

        changed = False
        # Now we will iterate through the to_move list and move all the values as needed
        for value in to_move:
            changed = True # If we have to move anything then the clusters aren't finalized so we continue the algorithm
            start_index, end_index, rgb_info = value
            result_list[start_index].remove(rgb_info) # Remove it from the original place
            result_list[end_index].add(rgb_info) # Add it to the new mean that works best for it
            # Using a set is helpful here since each of these are O(1) operations with a set

        means = calc_averages(means, result_list) # Recalculate the means based on where we moved everything
        
    return means, result_list
"""
Uses the results from k_means clustering to edit the image and save it
Input:
means (list of tuples) - a list of the randomly selected, distinct pixels' rgb values to begin k_means clustering
result_list (list of sets) - a list of rgb values representing pixels with that rgb value in the picture. The set they are put in depends on which mean gives the least squared error. They will be put into the set in result_list with the same index as that mean in the means list
Output: N/A
"""
def process_results(means, result_list):
    color_map = dict()
    for i in range(len(result_list)):
        for rgb_tuple in result_list[i]:
            color_map[rgb_tuple[0]] = means[i] # Map all the colors to the mean it will be associated with
    for h in range(HEIGHT):
        for w in range(WIDTH):
            r,g,b = color_map[pix[w,h]]
            pix[w,h] = (int(r), int(g), int(b))
    img.show()
    img.save("my_image.png")
    

def main():
    means, result_list = k_means()
    process_results(means, result_list)
if __name__ == "__main__":
    main()