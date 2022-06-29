from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "pylearn",
        sorted(glob("src/*.cpp")),
    ),
]

setup(
    name="pylearn-package-kun",
    version="0.0.1",
    author="kun",
    author_email="kun@gmail.com",
    description="A test project using pybind11",
    long_description="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'build_ext': ext_modules
    },
    ext_modules=ext_modules,
    python_requires=">=3.6",
)