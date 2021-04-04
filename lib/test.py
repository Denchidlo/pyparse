import Serializer

serializer = Serializer.Serializer()
serializer.change_form('json')


class A():
    def __init__(self):
        self.x = 5

a = A()

def fun():
    print(a)

serializer.data = a
serializer.dumps()

print(serializer.string)

serializer.loads()

loaded = serializer.data
print(loaded.x)
