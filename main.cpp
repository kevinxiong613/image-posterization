// g++ -pedantic-errors -ggdb -Wall -Weffc++ -Wextra -Wconversion -Wsign-conversion -Werror -std=c++20 -o programName programName.cpp

#include <iostream>
#include "functions.hpp"
#include <opencv2/opencv.hpp>

int main() {
    cv::Mat image = cv::imread("../rocket.png", cv::IMREAD_COLOR);
    if (image.empty()) {
        std::cerr << "Could not open or find the image!" << std::endl;
        return -1;
    } 

    std::vector<std::vector<uchar>> pixels = select_pixels(image, 4); // Call initialize function

    for (const auto& row : pixels) {
        for (const auto& pixel : row) {
            std::cout << static_cast<int>(pixel) << " "; // Assuming uchar is printed as integer
        }
        std::cout << std::endl; // New line for each row
    }


    // Save the modified image
    cv::imwrite("../modified_image.jpg", image);

    std::vector<double> means({"0.2", "0.3"});
    std::vector<double> t2({"0.2", "0.3"});
    process_results(means, t2);

    return 0;
}
