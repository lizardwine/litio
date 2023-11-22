def addOne(n):
    print(n + 1)
def addOneWR(n):
    return n + 1
def concatenate_lists(a, b):
    print(a)
    a.extend(b)
    return a
def pow(base, exponent):
    if exponent == 0:
        return 1
    elif exponent < 0:
        return 1 / pow(base, -exponent)
    elif exponent % 2 == 0:
        half_pow = pow(base, exponent // 2)
        return half_pow * half_pow
    else:
        return base * pow(base, exponent - 1)

class Hello:
    def __init__(self,name):
        self.__name = name
    def sum_lists(self, a, b):
        a.extend(b)
        return a
    @classmethod
    def print_hello(self,name):
        prt = f"hello {name}"
        return prt

class World:
    def __init__(self,name):
        pass

def generate_world(name):
    return World(name)