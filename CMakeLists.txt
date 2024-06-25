cmake_minimum_required(VERSION 3.10)

# Set the OpenCV_DIR to the directory containing OpenCVConfig.cmake
set(OpenCV_DIR /Users/kxiong1505525/git/color_space_vector_quantization/build_opencv)

# Find OpenCV package
find_package(OpenCV REQUIRED)

project(OpenCVTest)

# Include OpenCV headers
include_directories(${OpenCV_INCLUDE_DIRS})

# Define files to be included in executable
set(SOURCES
    main.cpp
    functions.cpp
)

# Define your executable
add_executable(OpenCVTest ${SOURCES})

# Link OpenCV libraries
target_link_libraries(OpenCVTest ${OpenCV_LIBS})

# Set RPATH
set_target_properties(OpenCVTest PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "${OpenCV_DIR}/lib"
    INSTALL_RPATH_USE_LINK_PATH TRUE
)
