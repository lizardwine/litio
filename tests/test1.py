def addOne(n:int) -> None:
    print(n + 1)
def addOneWR(n:int) -> int:
    return n + 1
def concatenate_lists(a:list,b:list) -> list:
    print(a)
    a.extend(b)
    return a
def pow(base:int,exponent:int) -> int:
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
    def __init__(self,name:str):
        self.__name = name
    def sum_lists(self,a:list,b:list) -> list:
        a.extend(b)
        return a
    @classmethod
    def print_hello(self,name:str) -> str:
        prt = f"hello {name}"
        return prt

class World:
    def __init__(self,name:str):
        pass

def generate_world(name:str) -> World:
    return World(name)