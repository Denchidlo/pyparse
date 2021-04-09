from io import FileIO
from typing import Any, IO
from pickle import dumps, loads

from lib.packager import *


class PickleParser:
    base_dumps = dumps
    base_loads = loads

    def dump(self, obj: object, file: object=None) -> None:
        packed_obj = Packer().pack(obj)
        if file:

            with open(file, 'w') as file:

                file.write(PickleParser.base_dumps(packed_obj))
        else:
            raise ValueError("File transfer aborted")

    def dumps(self, obj: object) -> None:
        packed_obj = Packer().pack(obj)
        return PickleParser.base_dumps(packed_obj)

    def load(self, file: object) -> Any:
        if file:

            with open(file, 'r') as file:

                raw_obj = PickleParser.base_loads(file.read())
            unpacked_obj = Unpacker().unpack(raw_obj)
            return unpacked_obj
        else:
            raise ValueError("File transfer aborted")

    def loads(self, json: str) -> Any:
        raw_obj = PickleParser.base_loads(json)
        unpacked_obj = Unpacker().unpack(raw_obj)
        return unpacked_obj
