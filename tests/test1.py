def addOne(n):
    print(n + 1)
def addOneWR(n):
    return n + 1
def pow(base,exponent):
    if exponent == 0:
        return 1
    elif exponent < 0:
        return 1 / pow(base, -exponent)
    elif exponent % 2 == 0:
        half_pow = pow(base, exponent // 2)
        return half_pow * half_pow
    else:
        return base * pow(base, exponent - 1)
class hello:
    def __init__(self,name):
        self.__name = name
    @classmethod
    def print_hello(self):
        print(f"hello world!!!")

