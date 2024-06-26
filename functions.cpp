#include <iostream>
#include <opencv2/opencv.hpp>
#include <unordered_set>


void process_results(const std::vector<double>& means, const std::vector<double>& resultList) {
    // std::unordered_map<std::string, int> colorMap;
    for (std::size_t i = 0; i < resultList.size(); i++) { 
        std::cout << means[i] << " ";
        std::cout << resultList[i] << std::endl;
    }
}

std::vector<std::vector<uchar>> select_pixels(cv::Mat& image, int k) {
    std::vector<std::vector<uchar>> res{};
    for (int h = 0; h < image.rows; h++) {
        for (int w = 0 ; w < image.cols; w++) {
            cv::Vec3b &color = image.at<cv::Vec3b>(h, w); // for OpenCV, it's (h, w)
            uchar b = color[0]; // color's indices are of type uchar, a value 0-255
            uchar g = color[1];
            uchar r = color[2];
            uchar total = b + g + r;
            std::vector<uchar> pixel{total, b, g, r};
            res.push_back(pixel); // Add these values to the datastructure
        }
    }

    std::set<uchar> rSet{}; // Hash each rgb individually to prevent duplicates
    std::set<uchar> bSet{};
    std::set<uchar> gSet{};
    for (std::size_t i = 0; i < res.size(); i += res.size() / k) {
        size_t temp = i;
        uchar b = res[temp][0];
        uchar g = res[temp][1];
        uchar r = res[temp][2];
        while (rSet.count(r) > 0 || bSet.count(b) > 0 || gSet.count(g) > 0) {
            temp += 1;
            b = res[temp][0];
            g = res[temp][1];
            r = res[temp][2];
        };
        rSet.insert(r);
        bSet.insert(b);
        gSet.insert(g);
    }

    std::vector<std::vector<uchar>> means{};

    std::__1::set<uchar>::iterator r = rSet.begin();
    auto g = gSet.begin();
    auto b = bSet.begin();

    while (r != rSet.end() && g != gSet.end() && b != bSet.end()) {
        uchar rTemp = *r;
        uchar gTemp = *g;
        uchar bTemp = *b;
        std::vector<uchar> temp{bTemp, gTemp, rTemp};
        means.push_back(temp);
        r++;
        g++;
        b++;
    }
    if (means.size() > k){ // Some cases there will be too many depending on number of pixels
        means.pop_back();
    }
    return means;
}

