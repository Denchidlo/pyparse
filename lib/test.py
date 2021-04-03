import Serializer

serializer = Serializer.Serializer()
serializer.change_form('pickle')

ar = [serializer, {"12": 45}]
serializer.data = ar

serializer.dumps()

print(serializer.string)

