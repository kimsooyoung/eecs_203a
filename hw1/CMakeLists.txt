cmake_minimum_required(VERSION 3.10)
project(ImageViewer)

# Set the C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED True)

# Add the executable
add_executable(image_viewer main.c)
