import random
from PIL import Image
from time import perf_counter

img = Image.open("eagle.png") # Just put the local filename in quotes.
img.show() # Send the image to your OS to be displayed as a temporary file (the before picture)
WIDTH, HEIGHT = img.size[0], img.size[1]
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.
K = 8

"""
Chooses the initial K pixels to begin K-means clustering randomly
Input: Nothing
Output:
means (list of tuples) - a list of the randomly selected, distinct pixels' rgb values to begin k_means clustering
result_list (list of sets) - a list of sets of where later rgb values will be added, representing pixels with that rgb value in the picture.
"""
def choose_means_random():
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
    return means, result_list
"""
Chooses the initial K pixels to begin K-means clustering by sorting the total rgb values of each pixel, and dividing them into K equal segments
Input: Nothing
Output:
means (list of tuples) - a list of the randomly selected, distinct pixels' rgb values to begin k_means clustering
result_list (list of sets) - a list of sets of where later rgb values will be added, representing pixels with that rgb value in the picture.
"""
def better_selection():
    res = list()
    for h in range(HEIGHT):
        for w in range(WIDTH):
            new_color = pix[w, h]
            total = new_color[0] + new_color[1] + new_color[2]
            res.append((total, (new_color[0], new_color[1], new_color[2])))
    res = sorted(res)
    colors = set()
    for i in range(0, len(res), len(res)//(K)):
        temp = i
        while res[temp][1] in colors: # Prevent duplicates
            temp += 1
        colors.add(res[i][1])
    if len(colors) > K: # Remove a random element if this is the case
        colors.pop()
    means = list()
    result_list = list()
    for color in colors:
        means.append(color) # Keep a list of all the initial "means"
        result_list.append(set()) # Instantiate an empty list of sets to keep track of which rgb values go to which mean based on associated index
    return means, result_list
"""
Chooses the initial K pixels to begin K-means clustering and sets up necessary data structures
Input: Nothing
Output:
means (list of tuples) - a list of the randomly selected, distinct pixels' rgb values to begin k_means clustering
result_list (list of sets) - a list of sets of rgb values representing pixels with that rgb value in the picture. The set they are put in depends on which mean gives the least squared error. They will be put into the set in result_list with the same index as that mean in the means list
"""
def initialize():
    means, result_list = better_selection()
    
    # First pass, count up all the colors, we don't want to do REPEATED WORK with different pixels that have the same RGB value
    count = dict()
    for h in range(HEIGHT):
        for w in range(WIDTH):
            rgb = pix[w,h] # This will return the rgb values as a tuple for the image
            rgb = (pix[w,h][0], pix[w,h][1], pix[w,h][2]) # For some reason some images have a 4th value 255
            count[rgb] = count.get(rgb, 0) + 1
    # print(count)
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
    means, result_list = initialize()

    means = calc_averages(means, result_list) # Recalculate the means based on what we added in the first batch

    changed = True # Use this variable to keep track of if any means changed
    while changed:
        to_move = list()
        lengths = list() # Count the number of rgb values per a mean to make our life easier later with recalculating the averages as we move things from one mean to another
        for i in range(len(result_list)): # Iterate through every mean cluster
            length = 0
            """ Another performance optimization: if you compute the squared distance from a given mean to every other mean, then take the min of those, if an arbitrary point's squared distance to the given mean is less than 1/4 of the aforementioned min, then it is guaranteed not to hop"""
            smallest_mean_distance = 1000000
            curr_mean = means[i]
            for temp in range(len(means)):
                error = squared_error(curr_mean, means[temp])
                if error < smallest_mean_distance and temp != i: # Check if it's smaller AND isn't the same mean, which would result in 0 distance
                    smallest_mean_distance = error
            
            for rgb_tuple in result_list[i]: # Go through all the rgb values associated with this particular mean cluster
                curr_rgb = rgb_tuple[0] # The goal is to see if there is a different mean that has less squared error with this rgb value
                if squared_error(curr_mean, curr_rgb) > 0.25 * smallest_mean_distance: # GUARANTEED not to move otherwise
                    smallest_error = 1000000
                    smallest_mean = -1
                    for mean_index in range(len(means)): # Find the index of the mean that works best for this rgb
                        rgb1, rgb2 = means[mean_index], curr_rgb
                        error = (rgb1[0]-rgb2[0]) ** 2 + (rgb1[1]-rgb2[1]) ** 2 + (rgb1[2]-rgb2[2]) ** 2 # Calculate squared error
                        if error < smallest_error:
                            smallest_error = error
                            smallest_mean = mean_index
                    if smallest_mean != i: # If the index of the mean with the least squared error isn't the one it already is in, queue it up for moving (can't move now since we are iterating through the object)
                        # print(rgb_tuple)
                        to_move.append((i, smallest_mean, rgb_tuple)) # Keep track of 1. the index of the mean the rgb is currently at 2. the index of the mean we will move it to 3. The tuple representing the rgb itself and it's count to remove it
                length += rgb_tuple[1] #  Increment the number of occurences for this
            lengths.append(length) # Append it to the lengths array

        changed = False
        # Now we will iterate through the to_move list and move all the values as needed
        for value in to_move:
            changed = True # If we have to move anything then the clusters aren't finalized so we continue the algorithm
            start_index, end_index, rgb_info = value # Grab the values from to_move that we stored

            """
            Before I would recall the "calc_averages" method which would have to iterate through all the rgb values in the result_list, now it's just O(1) operation to just updated the means based on what moves
            1. Recalculate the mean for the start_index assuming we are going to remove that value and all its occurences
            2. Recalculate the mean for the end_index assuming we are going to add that value and all its occurences
            """
            r, g, b = rgb_info[0] # Get the rgb values of what we are moving
            occurences = rgb_info[1] # Get how many times it occured

            old_r, old_g, old_b = means[start_index] # Grab the old avg rgb values for the starting index
            l = lengths[start_index] # This is where the lengths array comes in handy
            total_r, total_g, total_b = old_r * l, old_g * l, old_b * l # Recalculate the mean by first getting the value before dividing by the number of occurences then subtracting the new r g bs
            total_r = (total_r - (r * occurences)) / (l-occurences) # Continue the calculation by redividing the mean as if the one we are moving wasn't there
            total_g = (total_g - (g * occurences)) / (l-occurences)
            total_b = (total_b - (b * occurences)) / (l-occurences)
            means[start_index] = (total_r, total_g, total_b)


            new_r, new_g, new_b = means[end_index] # Grab the old avg rgb values for the starting index
            l = lengths[end_index]
            total_r, total_g, total_b = new_r * l, new_g * l, new_b * l # Recalculate the mean by first getting the value before dividing
            total_r = (total_r + (r * occurences)) / (l+occurences) # Continue the calculation by redividing the mean as if the one we are moving was added
            total_g = (total_g + (g * occurences)) / (l+occurences)
            total_b = (total_b + (b * occurences)) / (l+occurences)
            means[end_index] = (total_r, total_g, total_b)

            result_list[start_index].remove(rgb_info) # Remove it from the original place
            result_list[end_index].add(rgb_info) # Add it to the new mean that works best for it
            # Using a set is helpful here since each of these are O(1) operations with a set

        """
        Keeping this here in case I want to performance test later down the line
        """
        # means = calc_averages(means, result_list) # Recalculate the means based on where we moved everything
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
            r,g,b = color_map[(pix[w,h][0], pix[w,h][1], pix[w,h][2])]
            pix[w,h] = (int(r), int(g), int(b))
    img.show()
    img.save("eagle-8-means.png")
    

def main():
    start = perf_counter()
    means, result_list = k_means()
    process_results(means, result_list)
    end = perf_counter()
    print("time", end-start)
if __name__ == "__main__":
    main()