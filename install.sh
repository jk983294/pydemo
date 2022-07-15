git submodule add -b master -f https://github.com/pybind/pybind11.git
python3 -m pip install --upgrade build
cd python
python3 -m build --wheel
python3 -m pip install --force-reinstall python/dist/pydemo_package_kun-0.0.1-py3-none-any.whl

python setup.py bdist_wheel
python3 -m pip install --force-reinstall dist/pylearn-0.0.1-cp38-cp38-linux_x86_64.whl
