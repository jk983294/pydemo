pybind11_add_module(pydemo "Py11Demo.cpp")
target_link_libraries( pydemo PRIVATE mathdummystatic mathdummydyn ${CMAKE_THREAD_LIBS_INIT})