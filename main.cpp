// g++ -pedantic-errors -ggdb -Wall -Weffc++ -Wextra -Wconversion -Wsign-conversion -Werror -std=c++20 -o programName programName.cpp

#include <iostream>
#include "functions.hpp"
#include <opencv2/opencv.hpp>

int main() {
    cv::Mat image = cv::imread("rocket-27-means.png");

    std::vector<double> means({"0.2", "0.3"});
    std::vector<double> t2({"0.2", "0.3"});
    process_results(means, t2);
    return 0;
}
