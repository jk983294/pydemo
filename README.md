# pydemo
pydemo

# add pybind11
```sh
git submodule add -b master -f https://github.com/pybind/pybind11.git
python3 setup.py bdist_wheel
python3 -m pip install --force-reinstall dist/pylearn-0.0.1-cp38-cp38-linux_x86_64.whl
```
