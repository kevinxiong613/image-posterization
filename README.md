## Color Space Vector Quantization

- Posterizes an inputted image to K different colors, utilizing K Means clustering to implement color space vector quantization from scratch
- Reduced run time by 20% by implementing a different approach for choosing the K initial values, where the RGBS are divided K segments in a sorted list
- Reduced run time by 30% by reducing redundant calculations throughout


Example Input:
This is a picture of an Eagle

![alt text](https://raw.githubusercontent.com/kevxemail/color_space_vector_quantization/main/eagle.png)

Example Output:
Here is the result of posterizing it with 8 different colors

![alt text](https://raw.githubusercontent.com/kevxemail/color_space_vector_quantization/main/eagle-8-means.png)


Here is the result of posterizing it with 27 different colors
![alt text](https://raw.githubusercontent.com/kevxemail/color_space_vector_quantization/main/eagle-27-means.png)

