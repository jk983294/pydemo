import os
import re
import subprocess
import sys
from setuptools import Extension, setup, find_packages
from setuptools.command.build_ext import build_ext
from setuptools.command import install_lib


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, CURRENT_DIR)
BUILD_TEMP_DIR = None


# Convert distutils Windows platform specifiers to CMake -A arguments
PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}


# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        # required for auto-detection & inclusion of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        debug = int(os.environ.get("DEBUG", 0)) if self.debug is None else self.debug
        cfg = "Debug" if debug else "Release"

        # CMake lets you override the generator - we need to check this.
        # Can be set with Conda-Build, for example.
        cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

        # Set Python_EXECUTABLE instead if you use PYBIND11_FINDPYTHON
        # EXAMPLE_VERSION_INFO shows you how to pass a value into the C++ code
        # from Python.
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",  # not used on MSVC, but no harm
        ]
        build_args = []
        # Adding CMake arguments set as environment variable
        # (needed e.g. to build for ARM OSx on conda-forge)
        if "CMAKE_ARGS" in os.environ:
            cmake_args += [item for item in os.environ["CMAKE_ARGS"].split(" ") if item]

        if self.compiler.compiler_type != "msvc":
            # Using Ninja-build since it a) is available as a wheel and b)
            # multithreads automatically. MSVC would require all variables be
            # exported for Ninja to pick it up, which is a little tricky to do.
            # Users can override the generator with CMAKE_GENERATOR in CMake
            # 3.15+.
            if not cmake_generator or cmake_generator == "Ninja":
                try:
                    import ninja  # noqa: F401

                    ninja_executable_path = os.path.join(ninja.BIN_DIR, "ninja")
                    cmake_args += [
                        "-GNinja",
                        f"-DCMAKE_MAKE_PROGRAM:FILEPATH={ninja_executable_path}",
                    ]
                except ImportError:
                    pass

        else:

            # Single config generators are handled "normally"
            single_config = any(x in cmake_generator for x in {"NMake", "Ninja"})

            # CMake allows an arch-in-generator style for backward compatibility
            contains_arch = any(x in cmake_generator for x in {"ARM", "Win64"})

            # Specify the arch if using MSVC generator, but only if it doesn't
            # contain a backward-compatibility arch spec already in the
            # generator name.
            if not single_config and not contains_arch:
                cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name]]

            # Multi-config generators have a different way to specify configs
            if not single_config:
                cmake_args += [
                    f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}"
                ]
                build_args += ["--config", cfg]

        if sys.platform.startswith("darwin"):
            # Cross-compile support for macOS - respect ARCHFLAGS if set
            archs = re.findall(r"-arch (\S+)", os.environ.get("ARCHFLAGS", ""))
            if archs:
                cmake_args += ["-DCMAKE_OSX_ARCHITECTURES={}".format(";".join(archs))]

        # Set CMAKE_BUILD_PARALLEL_LEVEL to control the parallel build level
        # across all generators.
        if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
            # self.parallel is a Python 3 only way to set parallel jobs by hand
            # using -j in the build_ext call, not supported by pip or PyPA-build.
            if hasattr(self, "parallel") and self.parallel:
                # CMake 3.12+ only.
                build_args += [f"-j{self.parallel}"]

        build_temp = os.path.join(self.build_temp, ext.name)

        global BUILD_TEMP_DIR  # pylint: disable=global-statement
        BUILD_TEMP_DIR = build_temp

        if not os.path.exists(build_temp):
            os.makedirs(build_temp)

        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=build_temp)
        subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=build_temp)


class InstallLib(install_lib.install_lib):
    def install(self):
        outfiles = super().install()
        if outfiles is None:
            outfiles = []
        lib_dir = self.install_dir
        if not os.path.exists(lib_dir):
            os.makedirs(lib_dir)

        global BUILD_TEMP_DIR
        lib_ = 'pylearn.cpython-38-x86_64-linux-gnu.so'

        dft_lib_dir = os.path.join(CURRENT_DIR, 'install/lib')

        dst = os.path.join(self.install_dir, lib_)
        if os.path.exists(os.path.join(dft_lib_dir, lib_)):
            # The library is built by CMake directly
            src = os.path.join(dft_lib_dir, lib_)
        else:
            # The library is built by setup.py
            src = os.path.join(BUILD_TEMP_DIR, 'lib', lib_)
        print('Installing shared library: %s -> %s' % (src, dst))
        dst, _ = self.copy_file(src, dst)
        print('dst:', dst)
        outfiles.append(dst)
        return outfiles


setup(
    name="pylearn",
    version="0.0.1",
    author="kun",
    author_email="kun@gmail.com",
    description="pylearn",
    long_description="pylearn",
    ext_modules=[CMakeExtension("pylearn")],
    cmdclass={"build_ext": CMakeBuild, 'install_lib': InstallLib},
    zip_safe=False,
    extras_require={"test": ["pytest>=6.0"]},
    python_requires=">=3.6",
)

# class InstallLib1(install_lib.install_lib):
#     def install(self):
#         outfiles = super().install()
#         if outfiles is None:
#             outfiles = []
#         lib_dir = self.install_dir
#         if not os.path.exists(lib_dir):
#             os.makedirs(lib_dir)

#         global BUILD_TEMP_DIR   # pylint: disable=global-statement
#         libs = ['libmathdummydyn.so', 'pydemo.cpython-38-x86_64-linux-gnu.so']

#         dft_lib_dir = os.path.join(CURRENT_DIR, 'install/lib')

#         for lib_ in libs:
#             dst = os.path.join(self.install_dir, lib_)
#             if os.path.exists(os.path.join(dft_lib_dir, lib_)):
#                 # The library is built by CMake directly
#                 src = os.path.join(dft_lib_dir, lib_)
#             else:
#                 # The library is built by setup.py
#                 src = os.path.join(BUILD_TEMP_DIR, 'lib', lib_)
#             print('Installing shared library: %s -> %s' % (src, dst))
#             dst1, _ = self.copy_file(src, dst)
#             outfiles.append(dst1)

#         # change rpath. DO IT MANUALLY!!!
#         # os.system("patchelf --remove-rpath %s" % dst)
#         # os.system("patchelf --add-rpath './' %s" % dst)
#         # os.system("patchelf --add-rpath '\$ORIGIN' %s" % dst)
#         # os.system("patchelf --remove-needed libmathdummydyn.so %s" % dst)
#         # os.system("patchelf --add-needed libmathdummydyn.so %s" % dst)
#         return outfiles


# setup(
#     name="pydemo",
#     version="0.0.1",
#     author="kun",
#     author_email="kun@gmail.com",
#     description="pydemo",
#     long_description="pydemo",
#     ext_modules=[CMakeExtension("pydemo")],
#     cmdclass={"build_ext": CMakeBuild, 'install_lib': InstallLib1},
#     packages=find_packages(),
#     package_data={
#         "": ["*.so",],
#     },
#     include_package_data=True,
#     zip_safe=False,
#     extras_require={"test": ["pytest>=6.0"]},
#     python_requires=">=3.6",
# )