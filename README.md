## Color Space Vector Quantization

- Recreates an inputted image using only K different colors (posterizes), utilizing K Means clustering to implement color space vector quantization from scratch
- Reduced run time by 20% by implementing a different approach for choosing the K initial values, where the RGBS are divided K segments in a sorted list
- Reduced run time by 30% by reducing redundant calculations throughout


This is a picture of an eagle

![alt text](https://raw.githubusercontent.com/kevxemail/color_space_vector_quantization/main/images/eagle.png)

Here is the result of posterizing it with 8 different colors

![alt text](https://raw.githubusercontent.com/kevxemail/color_space_vector_quantization/main/images/eagle-8-means.png)


Here is the result of posterizing it with 27 different colors

![alt text](https://raw.githubusercontent.com/kevxemail/color_space_vector_quantization/main/images/eagle-27-means.png)


This is a picture of a rocket

![alt text](https://raw.githubusercontent.com/kevxemail/color_space_vector_quantization/main/images/rocket.png)


Here is the result of posterizing it with 8 different colors

![alt text](https://raw.githubusercontent.com/kevxemail/color_space_vector_quantization/main/images/rocket-8-means.png)


Here is the result of posterizing it with 27 different colors

