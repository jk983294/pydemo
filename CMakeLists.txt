cmake_minimum_required(VERSION 3.5)

project(pydemo)

SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/)

SET(CMAKE_CXX_FLAGS "-std=c++17 -O3 -s -Wall -Werror")
#SET(CMAKE_CXX_FLAGS "-std=c++17 -g -Wall -Werror")

message ("cxx Flags: " ${CMAKE_CXX_FLAGS})
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
SET(CMAKE_SHARED_LIBRARY_LINK_CXX_FLAGS)

add_subdirectory(pybind11)

# Source code
include_directories(include)

#add_subdirectory(example)
#add_subdirectory(test)
add_subdirectory(src)
add_subdirectory(py11_learn)
add_subdirectory(py11)
