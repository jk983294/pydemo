import hello
import pure_python as pp

print(dir(hello))
hello.say_hello_to("kun")
print(hello.f(4.2))
print(hello.integrate_f(1.0, 4.2, 100))
print(pp.primes(100))
print(hello.cpp_primes(100))