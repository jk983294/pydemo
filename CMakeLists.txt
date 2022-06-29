cmake_minimum_required(VERSION 3.5)

project(dummy)

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

set(PYTHON_LIBRARY_DIR /opt/anaconda3/lib/python3.8/site-packages)
set(PYTHON_EXECUTABLE /opt/anaconda3/bin/python)

#include_directories(/usr/include/python3.6)
#include_directories(/usr/include/python3.8)
include_directories(/opt/anaconda3/include/python3.8)

#find_library(PYLIB NAMES python3.6m PATHS /usr/lib/python3.6/ )
#find_library(PYLIB NAMES python3.8 PATHS /usr/lib/python3.8/ )
message ("SYSTEM_ENVIRONMENT_PATH: " ${SYSTEM_ENVIRONMENT_PATH})
find_library(PYLIB NAMES python3.8 PATHS /opt/anaconda3/lib/
        NO_CACHE NO_DEFAULT_PATH)
message ("PYLIB: " ${PYLIB})

# Source code
include_directories(include)

#add_subdirectory(example)
#add_subdirectory(test)
add_subdirectory(src)
#add_subdirectory(py11)
add_subdirectory(py11_learn)
