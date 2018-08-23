# array_change_key_case — 将数组中的所有键名修改为全大写或小写


class array_dict(dict):
    def array_change_key_case1(self):
        a_list = []
        for i in self:
            i = i.upper()
            a_list.append(i)
        return tuple(a_list)

    def array_change_key_case2(self):
        a_dict = {}
        for i in self:
            a_dict[i.upper()] = self.get(i)
        self.clear()
        self.update(a_dict)


if __name__ == "__main__":
    a = array_dict(a=1, b=2, c=3)
    print(a.array_change_key_case1())
    b = array_dict(a=1, b=2, c=3)
    b.array_change_key_case2()
    print(b)

