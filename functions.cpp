#include <iostream>
#include "functions.h"


/*
Uses the results from k_means clustering to edit the image and save it
Input:
means - a list of the randomly selected, distinct pixels' rgb values to begin k_means clustering
resultList - a list of rgb values representing pixels with that rgb value in the picture. The set they are
put in depends on which mean gives the least squared error. They will be put into the set in resultList with the samd index as that mean in the means list
Output: void
*/
void process_results(const std::vector<double>& means, const std::vector<double>& resultList) {
    // std::unordered_map<std::string, int> colorMap;
    for (std::size_t i = 0; i < resultList.size(); i++) { 
        std::cout << means[i] << " ";
        std::cout << resultList[i] << std::endl; 
    }
}
