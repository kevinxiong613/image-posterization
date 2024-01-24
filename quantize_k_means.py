import random
from PIL import Image

img = Image.open("puppy.jpg") # Just put the local filename in quotes.
# img.show() # Send the image to your OS to be displayed as a temporary file (the before picture)
WIDTH, HEIGHT = img.size
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.
K = 27
"""
Chooses the initial K pixels to begin K-means clustering
Input: N/A
Output: List of the K pixels
"""
def choose_initial_pixels():

    colors = set() # Make a set of the colors because we don't want duplicates
    for i in range(K):
        new_color = pix[random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)]
        while new_color in colors:
            new_color = pix[random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)]
        colors.add(new_color) # Generate k distinct colors in the picture
    means = list()
    result_list = list()
    for color in colors:
        means.append(color) # Keep a list of all the initial "means"
        result_list.append(set()) # Instantiate an empty list of lists to keep track of which rgb values go to which mean based on associated index
    
    # First pass, count up all the colors
    count = dict()
    for h in range(HEIGHT): # Do the first iteration of of associating colors with a mean
        for w in range(WIDTH):
            rgb = pix[w,h]
            count[rgb] = count.get(rgb, 0) + 1
    
    rgb_list = list()
    for color in count:
        rgb = color  # Find the mean with the lowest squared error for this rgb value
        smallest_error = 100000000000 # Initialize to some random large arbitrary value
        smallest_mean = -1
        for i in range(len(means)): 
            error = squared_error(means[i], rgb)
            if error < smallest_error: # Get the index of the mean with the smallest error
                smallest_error = error
                smallest_mean = i
        result_list[smallest_mean].append((color, count[color])) # Add this rgb value to the same index that the smallest_mean was at as a tuple with how many of this color there are too
        rgb_list.append((color, count[color])) # Keep an entire list seperately too for us to iterate through, this way we can iterate through this list instead of result_list so we can make changes to result_list as we go
    return means, result_list

"""
Calculate squared error between two RGB values by doing summation (v1-v2)^2
"""
def squared_error(rgb1, rgb2):
    return (rgb1[0]-rgb2[0]) ** 2 + (rgb1[1]-rgb2[1]) ** 2 + (rgb1[2]-rgb2[2]) ** 2

def calc_averages(means, result_list):
    for i in range(len(result_list)):
        avg_r = 0
        avg_g = 0
        avg_b = 0
        count = 0
        for j in range(len(result_list[i])): # Iterate through all the rgb values for this mean
            curr_rgb = result_list[i][j][0]
            rgb_occurences = result_list[i][j][1] # Get the occurences because they DO play a factor
            avg_r += curr_rgb[0] * rgb_occurences
            avg_g += curr_rgb[1] * rgb_occurences
            avg_b += curr_rgb[2] * rgb_occurences
            count += rgb_occurences # Count the number of occurences for this mean is so that we can average it
        new_avg = (avg_r/count, avg_g/count, avg_b/count)
        means[i] = new_avg # Change this to be the newly calculated mean
    return means

def k_means():
    means, result_list = choose_initial_pixels()

    means = calc_averages(means, result_list) # Recalculate the means based on what we added in the first batch
    print(means)
    old_means = [means[i] for i in range(len(means))] # Get the old means
    changed = 1000
    while changed > 0:
        to_move = list() # Keep track of 1. the index of the mean the rgb is currently at 2. the index of the mean we will move it to 3. The tuple representing the rgb itself and it's count to remove it
        for i in range(len(result_list)): # Iterate through every rgb value and see if we need to move it
            for j in range(len(result_list[i])): # Go through all the rgb values associated with this particular mean
                curr_rgb = result_list[i][j][0]
                smallest_error = 1000000
                smallest_mean = -1
                for mean_index in range(len(means)): # Find the index of the mean that works best for this rgb
                    error = squared_error(means[mean_index], curr_rgb)
                    if error < smallest_error:
                        smallest_error = error
                        smallest_mean = mean_index
                if smallest_mean != i: # If the smallest error mean isn't at the mean this is currently at
                    to_move.append((i, smallest_mean, result_list[i][j]))


        # Now we will iterate through the to_move list and move all the values as needed
        t = 0
        for value in to_move:
            start_index, end_index, rgb_info = value
            result_list[start_index].remove(rgb_info) # Remove it from the original place
            result_list[end_index].append(rgb_info) # Add it to the new mean that works best for it

        means = calc_averages(means, result_list) # Recalculate the means based on where we moved everything


        new_means = [means[i] for i in range(len(means))]
        changed = 0
        for i in range(len(new_means)):
            if new_means[i] != old_means[i]:
                changed += 1
            old_means[i] = new_means[i]
    return means, result_list

def process_results(means, result_list):
    color_map = dict()
    for i in range(len(result_list)):
        for j in range(len(result_list[i])):
            color_map[result_list[i][j][0]] = means[i] # Map all the colors to the mean it will be associated with

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