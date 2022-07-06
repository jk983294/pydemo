#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <dummy_demo.h>

namespace py = pybind11;

std::vector<double> data_func1(const std::vector<double>& data, const std::vector<double>& data1) {
    std::vector<double> ret;
    ret.resize(data.size(), 0);
    for (size_t i = 0; i < data.size(); ++i) {
        ret[i] = dummy::func1(data[i], data1[i]);
    }
    return ret;
}

std::vector<double> data_func2(const std::vector<double>& data, const std::vector<double>& data1) {
    std::vector<double> ret;
    ret.resize(data.size(), 0);
    for (size_t i = 0; i < data.size(); ++i) {
        ret[i] = dummy::func2(data[i], data1[i]);
    }
    return ret;
}

PYBIND11_MODULE(pydemo, m) {
    m.def("data_func1", &data_func1, "data_func1");
    m.def("data_func2", &data_func2, "data_func2");
}
