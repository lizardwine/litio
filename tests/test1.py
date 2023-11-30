def addOne(n):
    return n + 1
def addOneWR(n):
    return n + 1
def concatenate_lists(a, b):
    return a + b
def concatenate_dicts(a,b):
    a.update(b)
    return a
def pow(base, exponent):
    return base**exponent
  
class Hello:
    def __init__(self,name):
        self.name = name
    def sum_lists(self, a, b):
        a.extend(b)
        return a
    @classmethod
    def print_hello(self,name):
        prt = f"hello {name}"
        return prt

class World:
    def __init__(self,name):
        self.name = Hello(name)
        self.__world_id = 1243
    def hello(self):
        return Hello.print_hello(self.name)
    
def generate_world(name):
    return World(name)