from JsonParser import JsonParser
from YamlParser import YamlParser


class SerializerFactory:
    def __init__(self):
        self._creators = {}

    def create_serializer(self, format, creator):
        self._creators[format.lower()] = creator

    def get_serializer(self, format):
        creator = self._creators.get(format.lower())
        if not creator:
            raise ValueError(format)
        return creator()


factory = SerializerFactory()

factory.create_serializer('JSON', JsonParser.JsonParser)
factory.create_serializer('Yaml', YamlParser.YamlParser)
