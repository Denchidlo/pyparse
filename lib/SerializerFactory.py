from JsonParser import JsonParser
from TomlParser import TomlParser
from YamlParser import YamlParser
from PickleParser import PickleParser


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

factory.create_serializer('JSON', JsonParser.Json)
factory.create_serializer('Pickle', TomlParser.Toml)
factory.create_serializer('Yaml', YamlParser.Yaml)
factory.create_serializer('Toml', PickleParser.Pickle)
