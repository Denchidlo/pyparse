from io import FileIO
from typing import Any, IO
from toml import dumps, loads
from packager import *

class Toml:
    base_dumps = dumps
    base_loads = loads

    def dump(obj: object, file: object=None) -> None:
        packed_obj = Packer().pack(obj)
        if file:
            file.write(Toml.base_dumps(packed_obj))
        else:
            raise ValueError("File transfer aborted")

    def dumps(obj: object) -> None:
        packed_obj = Packer().pack(obj)
        return Toml.base_dumps(packed_obj)

    def load(file: object) -> Any:
        if file:
            raw_obj = Toml.base_loads(file.read())
            unpacked_obj = Unpacker().unpack(raw_obj)
            return unpacked_obj
        else:
            raise ValueError("File transfer aborted")

    def loads(json: str) -> Any:
        raw_obj = Toml.base_loads(json)
        unpacked_obj = Unpacker().unpack(raw_obj)
        return unpacked_obj
