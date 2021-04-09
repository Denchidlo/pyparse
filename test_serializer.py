from lib import Serializer
from tests.sample_objects import *
import math

ser = Serializer.Serializer()


class TestPrimesJson:
    def test_tuple(self):
        ser.change_form('json')
        ser.string = '{".list": [1, 2, 3], ".collection_type": "tuple"}'
        ser.loads()
        assert ser.data == sample_tuple

    def test_int(self):
        ser.change_form('json')
        ser.string = '123445'
        ser.loads()
        assert ser.data == sample_int

    def test_float(self):
        ser.change_form('json')
        ser.string = '0.42'
        ser.loads()
        assert math.isclose(ser.data, sample_float)

    def test_bool(self):
        ser.change_form('json')
        ser.string = 'true'
        ser.loads()
        assert ser.data == sample_bool

    def test_string(self):
        ser.change_form('json')
        ser.string = '"abacaba"'
        ser.loads()
        assert ser.data == sample_string

    def test_datetime(self):
        ser.change_form('json')
        ser.string = '{".time": "2021-04-10T00:00:00"}'
        ser.loads()
        assert ser.data == sample_datetime

    def test_None(self):
        ser.change_form('json')
        ser.string = 'null'
        ser.loads()
        assert ser.data == sample_None

    def test_dict(self):
        ser.change_form('json')
        ser.string = '{"123445": true, "abacaba": {".list": [1, 2, 3], ".collection_type": "tuple"}}'
        ser.loads()
        assert isinstance(ser.data, dict)
        assert ser.data["123445"] == sample_bool
        assert ser.data[sample_string] == sample_tuple

    def test_list(self):
        ser.change_form('json')
        ser.string = '["12, ", null, false, {".list": [1, 2, 3], ".collection_type": "tuple"}]'
        ser.loads()
        assert ser.data == sample_list

    def test_set(self):
        ser.change_form('json')
        ser.string = '{".list": [1, 2, "abacaba", 12, 123445], ".collection_type": "set"}'
        ser.loads()
        assert isinstance(ser.data, set)
        assert len(ser.data) == 5
        for i in sample_set:
            assert i in ser.data

    def test_frozenset(self):
        ser.change_form('json')
        ser.string = '{".list": ["c", "a", "b"], ".collection_type": "frozenset"}'
        ser.loads()
        assert isinstance(ser.data, frozenset)
        assert len(ser.data) == 3
        for i in sample_frozenset:
            assert i in ser.data


class TestFunctionsJson:
    def test_func(self):
        ser.change_form('json')
        ser.string = '{".META": {"139665363508960": {".code": {"co_argcount": 1, "co_posonlyargcount": 0, "co_kwonlyargcount": 0, "co_nlocals": 1, "co_stacksize": 2, "co_flags": 67, "co_code": [116, 0, 124, 0, 20, 0, 83, 0], "co_consts": {".list": [null], ".collection_type": "tuple"}, "co_names": {".list": ["sample_float"], ".collection_type": "tuple"}, "co_varnames": {".list": ["n"], ".collection_type": "tuple"}, "co_freevars": {".list": [], ".collection_type": "tuple"}, "co_cellvars": {".list": [], ".collection_type": "tuple"}, "co_filename": "/home/slava/Public/Testing/tests/sample_objects.py", "co_name": "sample_func", "co_firstlineno": 20, "co_lnotab": [0, 1]}, ".metatype": "func", ".name": "sample_func", ".module": "tests.sample_objects", ".refs": {".list": [{}, {"sample_float": 0.42}, {}, {".list": [], ".collection_type": "set"}], ".collection_type": "tuple"}, ".defaults": null}}, ".OBJ": {".metaid": "139665363508960"}}'
        ser.loads()
        assert math.isclose(ser.data(2.4), 1.008)

    def test_fibonacci(self):
        ser.change_form('json')
        ser.string = '{".META": {"140292067798896": {".code": {"co_argcount": 1, "co_posonlyargcount": 0, "co_kwonlyargcount": 0, "co_nlocals": 1, "co_stacksize": 4, "co_flags": 67, "co_code": [124, 0, 100, 1, 107, 2, 115, 16, 124, 0, 100, 2, 107, 2, 114, 20, 100, 1, 83, 0, 116, 0, 124, 0, 100, 1, 24, 0, 131, 1, 116, 0, 124, 0, 100, 3, 24, 0, 131, 1, 23, 0, 83, 0, 100, 0, 83, 0], "co_consts": {".list": [null, 1, 0, 2], ".collection_type": "tuple"}, "co_names": {".list": ["sample_fibonacci"], ".collection_type": "tuple"}, "co_varnames": {".list": ["n"], ".collection_type": "tuple"}, "co_freevars": {".list": [], ".collection_type": "tuple"}, "co_cellvars": {".list": [], ".collection_type": "tuple"}, "co_filename": "/home/slava/Public/Testing/tests/sample_objects.py", "co_name": "sample_fibonacci", "co_firstlineno": 24, "co_lnotab": [0, 1, 16, 1, 4, 2]}, ".metatype": "func", ".name": "sample_fibonacci", ".module": "tests.sample_objects", ".refs": {".list": [{}, {"sample_fibonacci": {".metaid": "140292067798896"}}, {}, {".list": [], ".collection_type": "set"}], ".collection_type": "tuple"}, ".defaults": null}}, ".OBJ": {".metaid": "140292067798896"}}'
        ser.loads()
        assert ser.data(7) == 21

    def test_lambda(self):
        ser.change_form('json')
        ser.string = '{".META": {"140224654409936": {".code": {"co_argcount": 1, "co_posonlyargcount": 0, "co_kwonlyargcount": 0, "co_nlocals": 1, "co_stacksize": 2, "co_flags": 67, "co_code": [124, 0, 100, 1, 19, 0, 83, 0], "co_consts": {".list": [null, 3], ".collection_type": "tuple"}, "co_names": {".list": [], ".collection_type": "tuple"}, "co_varnames": {".list": ["x"], ".collection_type": "tuple"}, "co_freevars": {".list": [], ".collection_type": "tuple"}, "co_cellvars": {".list": [], ".collection_type": "tuple"}, "co_filename": "/home/slava/Public/Testing/sample_objects.py", "co_name": "<lambda>", "co_firstlineno": 40, "co_lnotab": []}, ".metatype": "func", ".name": "<lambda>", ".module": "sample_objects", ".refs": {".list": [{}, {}, {}, {".list": [], ".collection_type": "set"}], ".collection_type": "tuple"}, ".defaults": null}}, ".OBJ": {".metaid": "140224654409936"}}'
        ser.loads()
        assert math.isclose(ser.data(1.6), 4.096)

    def test_inner_func(self):
        ser.change_form('json')
        ser.string = '{".META": {"140335234293824": {".code": {"co_argcount": 1, "co_posonlyargcount": 0, "co_kwonlyargcount": 0, "co_nlocals": 2, "co_stacksize": 3, "co_flags": 67, "co_code": [100, 1, 100, 2, 132, 0, 125, 1, 124, 1, 124, 1, 124, 0, 131, 1, 124, 0, 23, 0, 131, 1, 83, 0], "co_consts": {".list": [null, null, "sample_inner_func.<locals>.inner"], ".collection_type": "tuple"}, "co_names": {".list": [], ".collection_type": "tuple"}, "co_varnames": {".list": ["n", "inner"], ".collection_type": "tuple"}, "co_freevars": {".list": [], ".collection_type": "tuple"}, "co_cellvars": {".list": [], ".collection_type": "tuple"}, "co_filename": "/home/slava/Public/Testing/tests/sample_objects.py", "co_name": "sample_inner_func", "co_firstlineno": 31, "co_lnotab": [0, 1, 8, 3]}, ".metatype": "func", ".name": "sample_inner_func", ".module": "tests.sample_objects", ".refs": {".list": [{}, {}, {}, {".list": [], ".collection_type": "set"}], ".collection_type": "tuple"}, ".defaults": null}}, ".OBJ": {".metaid": "140335234293824"}}'
        ser.loads()
        assert math.isclose(ser.data(1.99), 37643.98251178124)


class TestClassesJson:
    def test_class_A(self):
        ser.change_form('json')
        ser.load('tests/classA.json')
        instance = ser.data()
        assert ser.data.__name__ == 'A'
        assert type(ser.data) == type
        assert instance.x == 12

    def test_class_B(self):
        ser.change_form('json')
        ser.load('tests/classB.json')
        instance = ser.data()
        assert ser.data.__name__ == 'B'
        assert type(ser.data) == type
        assert instance.non_static() == "hey from self method"
        assert ser.data.static() == "hello from static method"

    def test_class_C(self):
        ser.change_form('json')
        ser.load('tests/classC.json')
        instance = ser.data(lambda x: x + x)
        assert ser.data.__name__ == 'C'
        assert ser.data.__base__.__name__ == 'A'
        assert type(ser.data) == type
        assert instance.x == 12
        assert instance.prop("42") == "4242"

    def test_class_Foo(self):
        ser.change_form('json')
        ser.load('tests/classFoo.json')
        assert not hasattr(ser.data, 'bar')
        assert hasattr(ser.data, 'BAR')
        f = ser.data()
        assert f.BAR == "bip"


class TestPackUnpackJson:
    def test_tuple(self):
        ser.change_form('json')
        ser.data = sample_tuple
        ser.dumps()
        ser.loads()
        assert ser.data == sample_tuple

    def test_int(self):
        ser.change_form('json')
        ser.data = sample_int
        ser.dumps()
        ser.loads()
        assert ser.data == sample_int

    def test_float(self):
        ser.change_form('json')
        ser.data = sample_float
        ser.dumps()
        ser.loads()
        assert math.isclose(ser.data, sample_float)

    def test_bool(self):
        ser.change_form('json')
        ser.data = sample_bool
        ser.dumps()
        ser.loads()
        assert ser.data == sample_bool

    def test_string(self):
        ser.change_form('json')
        ser.data = sample_string
        ser.dumps()
        ser.loads()
        assert ser.data == sample_string

    def test_datetime(self):
        ser.change_form('json')
        ser.data = sample_datetime
        ser.dumps()
        ser.loads()
        assert ser.data == sample_datetime

    def test_None(self):
        ser.change_form('json')
        ser.data = sample_None
        ser.dumps()
        ser.loads()
        assert ser.data == sample_None

    def test_dict(self):
        ser.change_form('json')
        ser.data = sample_dict
        ser.dumps()
        ser.loads()
        assert isinstance(ser.data, dict)
        assert ser.data["123445"] == sample_bool
        assert ser.data[sample_string] == sample_tuple

    def test_list(self):
        ser.change_form('json')
        ser.data = sample_list
        ser.dumps()
        ser.loads()
        assert ser.data == sample_list

    def test_set(self):
        ser.change_form('json')
        ser.data = sample_set
        ser.dumps()
        ser.loads()
        assert isinstance(ser.data, set)
        assert len(ser.data) == 5
        for i in sample_set:
            assert i in ser.data

    def test_frozenset(self):
        ser.change_form('json')
        ser.data = sample_frozenset
        ser.dumps()
        ser.loads()
        assert isinstance(ser.data, frozenset)
        assert len(ser.data) == 3
        for i in sample_frozenset:
            assert i in ser.data

    def test_func(self):
        ser.change_form('json')
        ser.data = sample_func
        ser.dumps()
        ser.loads()
        assert math.isclose(ser.data(2.4), 1.008)

    def test_fibonacci(self):
        ser.change_form('json')
        ser.data = sample_fibonacci
        ser.dumps()
        ser.loads()
        assert ser.data(7) == 21

    def test_lambda(self):
        ser.change_form('json')
        ser.data = sample_lambda
        ser.dumps()
        ser.loads()
        assert math.isclose(ser.data(1.6), 4.096)

    def test_inner_func(self):
        ser.change_form('json')
        ser.data = sample_inner_func
        ser.dumps()
        ser.loads()
        assert math.isclose(ser.data(1.99), 37643.98251178124)

    def test_class_A(self):
        ser.change_form('json')
        ser.data = A
        ser.dumps()
        ser.loads()
        instance = ser.data()
        assert ser.data.__name__ == 'A'
        assert type(ser.data) == type
        assert instance.x == 12

    def test_class_B(self):
        ser.change_form('json')
        ser.data = B
        ser.dumps()
        ser.loads()
        instance = ser.data()
        assert ser.data.__name__ == 'B'
        assert type(ser.data) == type
        assert instance.non_static() == "hey from self method"
        assert ser.data.static() == "hello from static method"

    def test_class_C(self):
        ser.change_form('json')
        ser.data = C
        ser.dumps()
        ser.loads()
        instance = ser.data(lambda x: x + x)
        assert ser.data.__name__ == 'C'
        assert ser.data.__base__.__name__ == 'A'
        assert type(ser.data) == type
        assert instance.x == 12
        assert instance.prop("42") == "4242"

    def test_class_Foo(self):
        ser.change_form('json')
        ser.data = Foo
        ser.dumps()
        ser.loads()
        assert not hasattr(ser.data, 'bar')
        assert hasattr(ser.data, 'BAR')
        f = ser.data()
        assert f.BAR == "bip"
