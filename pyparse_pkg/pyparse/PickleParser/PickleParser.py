from io import FileIO
from typing import Any, IO
from pickle import dumps, loads
from pyparse.packager import *

class Pickle:
    base_dumps = dumps
    base_loads = loads

    def dump(obj: object, file: object=None) -> None:
        packed_obj = Packer().pack(obj)
        if file:
            file.write(Pickle.base_dumps(packed_obj))
        else:
            raise ValueError("File transfer aborted")

    def dumps(obj: object) -> None:
        packed_obj = Packer().pack(obj)
        return Pickle.base_dumps(packed_obj)

    def load(file: object) -> Any:
        if file:
            raw_obj = Pickle.base_loads(file.read())
            unpacked_obj = Unpacker().unpack(raw_obj)
            return unpacked_obj
        else:
            raise ValueError("File transfer aborted")

    def loads(json: str) -> Any:
        raw_obj = Pickle.base_loads(json)
        unpacked_obj = Unpacker().unpack(raw_obj)
        return unpacked_obj