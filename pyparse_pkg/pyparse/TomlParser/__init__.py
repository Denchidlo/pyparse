from io import FileIO
from typing import Any, IO
from toml import dumps, loads
from packager import *

class TomlParser:
    base_dumps = dumps
    base_loads = loads

    def dump(self, obj: object, file: object=None) -> None:
        packed_obj = Packer().pack(obj)
        if file:
            file.write(TomlParser.base_dumps(packed_obj))
        else:
            raise ValueError("File transfer aborted")

    def dumps(self, obj: object) -> None:
        packed_obj = Packer().pack(obj)
        return TomlParser.base_dumps(packed_obj)

    def load(self, file: object) -> Any:
        if file:
            raw_obj = TomlParser.base_loads(file.read())
            unpacked_obj = Unpacker().unpack(raw_obj)
            return unpacked_obj
        else:
            raise ValueError("File transfer aborted")

    def loads(self, json: str) -> Any:
        raw_obj = TomlParser.base_loads(json)
        unpacked_obj = Unpacker().unpack(raw_obj)
        return unpacked_obj