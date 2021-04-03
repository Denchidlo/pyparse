from io import FileIO
from typing import Any, IO
from yaml import dump, load
from packager import *

class Yaml:
    base_dumps = dump
    base_loads = load

    def dump(obj: object, file: object=None) -> None:
        packed_obj = Packer().pack(obj)
        if file:
            file.write(Yaml.base_dumps(packed_obj))
        else:
            raise ValueError("File transfer aborted")

    def dumps(obj: object) -> None:
        packed_obj = Packer().pack(obj)
        return Yaml.base_dumps(packed_obj)

    def load(file: object) -> Any:
        if file:
            raw_obj = Yaml.base_loads(file.read())
            unpacked_obj = Unpacker().unpack(raw_obj)
            return unpacked_obj
        else:
            raise ValueError("File transfer aborted")

    def loads(json: str) -> Any:
        raw_obj = Yaml.base_loads(json)
        unpacked_obj = Unpacker().unpack(raw_obj)
        return unpacked_obj
