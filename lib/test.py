import Serializer

ar = [12, 32]

serializer = Serializer.Serializer()
serializer.change_form('json')
#serializer.data = ar

serializer.load('/home/slava/Public/python_lib/custom_json.json')

print(serializer.data)
