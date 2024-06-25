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
        // Modify the pixel values
    for (int y = 0; y < image.rows; y++) {
        for (int x = 0; x < image.cols; x++) {
            cv::Vec3b &color = image.at<cv::Vec3b>(y, x);
            color[0] = 0; // Set Blue channel to 0
        }
    }

    // Save the modified image
    cv::imwrite("../modified_image.jpg", image);

    std::vector<double> means({"0.2", "0.3"});
    std::vector<double> t2({"0.2", "0.3"});
    process_results(means, t2);
    return 0;
}
