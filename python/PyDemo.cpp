#include <Python.h>
#include <dummy_demo.h>
#include <boost/python.hpp>
#include <boost/python/stl_iterator.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

using namespace boost::python;

template <class T>
boost::python::list std_vector_to_pylist(const std::vector<T>& v) {
    boost::python::list l;
    for (const auto& item : v) {
        l.append(item);
    }
    return l;
}

template <class T>
boost::python::list std_vector_to_pylist(const std::vector<std::vector<T>>& v) {
    boost::python::list l;
    for (const auto& item : v) {
        l.append(std_vector_to_pylist(item));
    }
    return l;
}

template <typename T>
std::vector<T> to_std_vector(const boost::python::object& iterable) {
    return std::vector<T>(boost::python::stl_input_iterator<T>(iterable), boost::python::stl_input_iterator<T>());
}

boost::python::list data_func1(const boost::python::object& data, const boost::python::object& data1) {
    std::vector<double> ret;
    std::vector<double> data_ = to_std_vector<double>(data);
    std::vector<double> data1_ = to_std_vector<double>(data1);
    ret.resize(data_.size(), 0);
    for (size_t i = 0; i < data_.size(); ++i) {
        ret[i] = dummy::func1(data_[i], data1_[i]);
    }
    return std_vector_to_pylist(ret);
}

boost::python::list data_func2(const boost::python::object& data, const boost::python::object& data1) {
    std::vector<double> ret;
    std::vector<double> data_ = to_std_vector<double>(data);
    std::vector<double> data1_ = to_std_vector<double>(data1);
    ret.resize(data_.size(), 0);
    for (size_t i = 0; i < data_.size(); ++i) {
        ret[i] = dummy::func2(data_[i], data1_[i]);
    }
    return std_vector_to_pylist(ret);
}

BOOST_PYTHON_MODULE(pydemo) {
    def("data_func1", data_func1);
    def("data_func2", data_func2);
}
