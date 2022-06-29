import os
import sys
from pathlib import Path
_current_root = str(Path(__file__).resolve().parents[1])
sys.path.append(_current_root + '/cmake-build-debug/lib')
sys.path.append(_current_root + '/install/lib')
sys.path.append(_current_root + '/lib')
import pylearn


if __name__ == '__main__':
    print(pylearn.add(1, 2))
    print(pylearn.arg_add(i=1, j=2))
    print(pylearn.default_add())

    # class
    p = pylearn.Pet("Molly")
    print(p)
    print(p.getName())
    p.setName("Charly")
    print(p.getName())
    p.name = "Charly1"
    print(p.name)
    p.my_attr = 2  # OK, dynamically add a new attribute
    print(p.__dict__)
    p.set(3)
    print(p.age)
    p.set("3")
    print(p.name)

    p = pylearn.Pet("Lucy", pylearn.Pet.Cat)
    print(p.type)
    print(int(p.type))
    print(pylearn.Pet.Kind.__members__)
    pet_type = p.type
    print(pet_type)  # Kind.Cat
    print(pet_type.name)  # Cat

    # sub class
    p = pylearn.Dog("Molly")
    print(p.name)
    print(p.bark())
    p = pylearn.pet_store()
    print(type(p))
    print(p.bark())