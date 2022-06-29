include_directories(/home/aaron/github/pybind11/include/)

add_library( pylearn SHARED "Py11Learn.cpp" )
set_property(TARGET pylearn PROPERTY POSITION_INDEPENDENT_CODE ON)
SET_TARGET_PROPERTIES(pylearn PROPERTIES PREFIX "")
target_link_libraries( pylearn ${PYLIB} pthread rt dl)

