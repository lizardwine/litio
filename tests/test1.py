def addOne(n):
    return n + 1
def addOneWR(n):
    return n + 1
def concatenate_lists(a, b):
    return a + b
def pow(base, exponent):
    return base**exponent
  
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