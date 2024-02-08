# distutils: language=c++


from libcpp.vector cimport vector

def say_hello_to(name):
    print("Hello %s!" % name)


cpdef double f(double x):
    return x ** 2 - x


def integrate_f(double a, double b, int N):
    cdef int i
    cdef double s
    cdef double dx
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx


def cpp_primes(unsigned int nb_primes):
    cdef int n, i
    cdef vector[int] p
    p.reserve(nb_primes)  # allocate memory for 'nb_primes' elements.

    n = 2
    while p.size() < nb_primes:  # size() for vectors is similar to len()
        for i in p:
            if n % i == 0:
                break
        else:
            p.push_back(n)  # push_back is similar to append()
        n += 1

    # If possible, C values and C++ objects are automatically
    # converted to Python objects at need.
    return p  # so here, the vector will be copied into a Python list.