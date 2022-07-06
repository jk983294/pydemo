pybind11_add_module(pylearn "Py11Learn.cpp")
target_link_libraries( pylearn PRIVATE ${CMAKE_THREAD_LIBS_INIT})

