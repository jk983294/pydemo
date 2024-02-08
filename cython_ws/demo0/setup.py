from setuptools import Extension, setup
from Cython.Build import cythonize

ext_modules = [
    Extension("hello", 
              sources=["hello.pyx", "pure_python.py"],
              libraries=["m"]  # Unix-like specific
              )
]

setup(
    name='hello module',
    ext_modules=cythonize(ext_modules,
                          annotate=True,
                          compiler_directives={'language_level' : "3"}
    )
)