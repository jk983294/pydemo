add_library( pydemo SHARED "Py11Demo.cpp" )
set_property(TARGET pydemo PROPERTY POSITION_INDEPENDENT_CODE ON)
SET_TARGET_PROPERTIES(pydemo PROPERTIES PREFIX "")
target_link_libraries( pydemo mathdummystatic mathdummydyn)