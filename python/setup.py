import os
import setuptools
from setuptools.command import install_lib
# from setuptools import setup, find_packages, Extension

class InstallLib(install_lib.install_lib):
    def install(self):
        outfiles = super().install()
        CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
        lib_dir = os.path.join(self.install_dir, 'demo')
        if not os.path.exists(lib_dir):
            os.mkdir(lib_dir)

        print('InstallLib=', self.install_dir, lib_dir, CURRENT_DIR)

        dft_lib_dir1 = os.path.join(CURRENT_DIR, os.path.pardir, 'cmake-build-debug/lib')
        dft_lib_dir2 = os.path.join(CURRENT_DIR, os.path.pardir, 'install/lib')
        dft_lib_dir = dft_lib_dir1

        if os.path.exists(dft_lib_dir1):
            dft_lib_dir = dft_lib_dir1
        elif os.path.exists(dft_lib_dir2):
            dft_lib_dir = dft_lib_dir2
        else:
            raise Exception("lib path not found %s" % dft_lib_dir)
        # self.logger.info('Installing shared library: %s', src)
        to_copy = ['pydemo.so', 'libmathdummydyn.so']
        for toc in to_copy:
            dst = os.path.join(lib_dir, toc)
            src = os.path.join(dft_lib_dir, toc)
            print('InstallLib copy %s -> %s' % (src, dst))
            dst, _ = self.copy_file(src, dst)
            outfiles.append(dst)
        return outfiles


setuptools.setup(
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    # package_data={'': ['pydemo.so', 'libmathdummydyn.so']},
    cmdclass={
        'install_lib': InstallLib
    },
    python_requires=">=3.6",
)