// g++ -pedantic-errors -ggdb -Wall -Weffc++ -Wextra -Wconversion -Wsign-conversion -Werror -std=c++20 -o programName programName.cpp

#include <iostream>
#include "functions.h"

int main() {
    std::vector<double> t1({"0.2", "0.3"});
    std::vector<double> t2({"0.2", "0.3"});
    process_results(t1, t2);
    return 0;
}
