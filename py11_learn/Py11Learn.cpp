#include <pybind11/pybind11.h>
#include <cstdio>

namespace py = pybind11;

int add(int i = 1, int j = 2) {
    return i + j;
}

struct Pet {
    enum Kind {
        Dog = 0,
        Cat
    };
    struct Attributes {
        float a = 0;
    };

    Pet(const std::string &name) : name(name) { }
    Pet(const std::string &name, Kind type) : name(name), type(type) { }
    virtual ~Pet() = default;
    void setName(const std::string &name_) { name = name_; }
    const std::string &getName() const { return name; }

    void set(int age_) { age = age_; }
    void set(const std::string &name_) { name = name_; }

    void overload_func(int a) { printf("a=%d\n", a); }
    void overload_func(int a) const { printf("a=%d\n", a); }

    std::string name;
    int age;
    Kind type;
    Attributes attr;
};

struct Dog : Pet {
    Dog(const std::string &name) : Pet(name) { }
    std::string bark() const { return "woof!"; }
};

PYBIND11_MODULE(pylearn, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("add", &add, "A function that adds two numbers");
    m.def("arg_add", &add, "A function which adds two numbers",
          py::arg("i"), py::arg("j"));
    m.def("default_add", &add, "A function which adds two numbers",
          py::arg("i") = 1, py::arg("j") = 2);

    py::class_<Pet> pet(m, "Pet", py::dynamic_attr());
    pet.def(py::init<const std::string &>())
        .def(py::init<const std::string &, Pet::Kind>())
        .def_readwrite("name", &Pet::name)
        .def_readwrite("age", &Pet::age)
        .def_readwrite("type", &Pet::type)
        .def_readwrite("attr", &Pet::attr)
        .def("set", py::overload_cast<int>(&Pet::set), "Set the pet's age")
        .def("set", py::overload_cast<const std::string &>(&Pet::set), "Set the pet's name")
        .def("overload_func_mutable", py::overload_cast<int>(&Pet::overload_func))
        .def("overload_func_const",   py::overload_cast<int>(&Pet::overload_func, py::const_))
        .def("setName", &Pet::setName)
        .def("getName", &Pet::getName)
        .def("__repr__",
             [](const Pet &a) {
                 return "<example.Pet named '" + a.name + "'>";
             });

    py::enum_<Pet::Kind>(pet, "Kind")
        .value("Dog", Pet::Kind::Dog)
        .value("Cat", Pet::Kind::Cat)
        .export_values();

    py::class_<Pet::Attributes>(pet, "Attributes")
        .def(py::init<>())
        .def_readwrite("a", &Pet::Attributes::a);

    py::class_<Dog, Pet>(m, "Dog")
        .def(py::init<const std::string &>())
        .def("bark", &Dog::bark);

    m.def("pet_store", []() { return std::unique_ptr<Pet>(new Dog("PolymorphicDog")); });
}