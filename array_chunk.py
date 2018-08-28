# array_chunk — 将一个数组分割成多个


import random


class array_list(list):
    def array_chunk1(self):
        breakpiont = random.randint(0, self.__len__())
        b = self[0:breakpiont]
        c = self[breakpiont:]
        a = (b, c)
        return a


if __name__ == "__main__":
    a = array_list((1, 2, 3, 4))
    print(a.array_chunk1())
