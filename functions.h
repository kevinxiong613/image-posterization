#ifndef FUNCTIONS_H // checks if a unique identifier (macro) has not been defined yet
#define FUNCTIONS_H // defines the unique identifier (macro)

// This checks if MYFUNCTIONS_H has not been defined. If it hasn't been defined, the preprocessor continues processing the file. 

void process_results(const std::vector<double> &means, const std::vector<double> &result_list);

#endif
