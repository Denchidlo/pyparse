import JSONSerializer
import TomlSerializer
import YamlSerializer
import PickleSerializer


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

factory.create_serializer('JSON', JSONSerializer.JSONSerializer)
factory.create_serializer('Pickle', PickleSerializer.PickleSerializer)
factory.create_serializer('Yaml', YamlSerializer.YamlSerializer)
factory.create_serializer('Toml', TomlSerializer.TomlSerializer)
