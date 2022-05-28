add_library(mathdummystatic STATIC dummy_demo.cpp)
install(TARGETS mathdummystatic ARCHIVE DESTINATION lib)

add_library(mathdummydyn SHARED math_dummy2.cpp)
install(TARGETS mathdummydyn LIBRARY DESTINATION lib)
