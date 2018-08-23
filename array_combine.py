# array_combine — 创建一个数组，用一个数组的值作为其键名，另一个数组的值作为其值


class array_dict(dict):
    def array_combine(self, array1, array2):
        print('array1 = ', array1, 'array2 = ', array2)
        index = 0
        for i in array2:
            index += 1
        _index = 0
        for i in array1:
            if 0 == index:
                self[i] = ""
            elif index > _index:
                self[i] = array2[_index]
            else:
                self[i] = ""
            _index += 1
        print(self)


if __name__ == "__main__":
    a_array_dict = array_dict()
    a_array = ['a', 'b', 'c', 'd']
    b_array = [1, 2, 3]
    a_array_dict.array_combine(a_array, b_array)
