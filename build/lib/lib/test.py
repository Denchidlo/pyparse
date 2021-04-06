import Serializer
import json
import yaml

serializer = Serializer.Serializer()
serializer.change_form('json')


class A():
    def __init__(self):
        self.x = 5


a = A()
# a.b = 12

b = [12, 23, "333"]


def c():
    print(b)


def fun():
    print(a)


serializer.data = c
serializer.dump('j.json')

serializer.load('j.json', False)

loaded = serializer.data

print(loaded)

serializer2 = Serializer.Serializer()
serializer2.change_form('yaml')
serializer2.data = loaded
serializer2.dump('y.yaml', False)

serializer2.load('y.yaml')

yaml_loaded = serializer2.data
yaml_loaded()
# print(loaded)
