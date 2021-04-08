from io import FileIO
from typing import Any, IO
from yaml import dump, load
from packager import *

class YamlParser:
    base_dumps = dump
    base_loads = load

    def dump(self, obj: object, file: object=None):
        packed_obj = Packer().pack(obj)
        if file:
            with open(file, 'w+') as file:
                file.write(YamlParser.base_dumps(packed_obj))
        else:
            raise ValueError("File transfer aborted")

    def dumps(self, obj: object):
        packed_obj = Packer().pack(obj)
        return YamlParser.base_dumps(packed_obj)

    def load(self, file: object):
        if file:
            with open(file, 'w+') as file:
                raw_obj = YamlParser.base_loads(file.read())
            unpacked_obj = Unpacker().unpack(raw_obj)
            return unpacked_obj
        else:
            raise ValueError("File transfer aborted")

    def loads(self, json: str):
        raw_obj = YamlParser.base_loads(json)
        unpacked_obj = Unpacker().unpack(raw_obj)
        return unpacked_obj
