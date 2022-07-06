python3 -m pip install --upgrade build
cd python
python3 -m build --wheel
python3 -m pip install python/dist/pydemo_package_kun-0.0.1-py3-none-any.whl

python setup.py bdist_wheel
