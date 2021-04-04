import Serializer

serializer = Serializer.Serializer()

serializer.change_form('json')


ar = [serializer, {"12": 45}]
serializer.data = ar

serializer.dumps()

print(serializer.string)


serializer.loads()

print(serializer.data)