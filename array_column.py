# array_column — 返回数组中指定的一列


class array_dict(dict):
    def array_column(self, index):
        _index = 0
        for k in self:
            if _index == index:
                return {k: self.get(k)}
            _index += 1


if __name__ == "__main__":
    a = array_dict(a=1, b=2, c=3)
    print(a.array_column(2))
