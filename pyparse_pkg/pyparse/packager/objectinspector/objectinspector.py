import builtins
import re
from datetime import datetime
import inspect
from sys import builtin_module_names, modules

primitives = set(
    [
        int,
        float,
        bool,
        str
    ])

# Utils
def is_primitive(obj: object) -> bool:
    return type(obj) in primitives

def is_basetype(obj: object) -> bool:
    for el in primitives:
        if el.__name__ == obj.__name__:
            return True
    if el in [dict, list, tuple, set]:
        if el.__name__ == obj.__name__:
            return True
    return False

def is_instance(obj):
    if not hasattr(obj, '__dict__'):
        return False
    if inspect.isroutine(obj): 
        return False
    if inspect.isclass(obj):
        return False
    else:
        return True

def is_none(obj: object) -> bool:
    return obj is None

def has_source(obj: object) -> bool:
    return callable(obj) or inspect.isclass(obj)

def is_magicmarked(s: str) -> bool:
    return re.match("^__(?:\w+)__$", s) != None

def is_collection(obj: object) -> bool:
    return getattr(obj, "__iter__", None) != None and getattr(obj, "__getitem__", None) != None

def is_kvbased(obj: object) -> bool:
    """Check if collection is based on <key> : <value> relations

        Returns:
            False - if an exception was occured during accessing value by __iter__() based key

            True - otherwise

    """
    for el in obj:
        try:
            val = obj[el]
        except Exception:
            return False
    return True

def pack_iterable(obj: object) -> dict:
    """Parse object as collection

        Supported objects:
            1)Object containing
    """
    if is_collection(obj):
        if is_kvbased(obj):
            subset = {}
            for key in obj:
                subset.update({key: pack(obj[key])})
        else:
            subset = []
            for el in obj:
                subset.append(pack(el))
        return subset
    else:
        raise ValueError(f"{obj} is not Iterable")

def pack_objstate(obj: object) -> dict:
    """Return object state as:
        
        1)Object state -> all fields and attributes except '__<attr>__' (magic) attributes
        
        2)As a primitive

        3)As a object collection if obj is iterable

    """
    result = {}
    try:
        result.update({".type":pack(type(obj)), ".state": {}})
    except Exception:
        result.update({".type":pack(type(obj)), ".state": {}})
    state = [el for el in inspect.getmembers(obj, lambda el: not callable(el)) if not is_magicmarked(el[0])]
    for el in state:
        result[".state"][el[0]] = pack(el[1])
    return result

def pack(obj: object):
    if is_primitive(obj):
        return obj
    if isinstance(obj, datetime):
        return {".time":str(obj.isoformat())}
    if inspect.ismodule(obj):
        try:
            return {".code": inspect.getsource(obj), ".bigmodule" : f"{obj.__name__}"}
        except Exception:
            return {".bigmodule": f"{obj.__name__}"}
    if getattr(obj, "__name__", None):
        if obj.__name__ in dir(builtins) and not is_basetype(obj):
            return {".builtin": obj.__name__}
        if  getattr(obj, "__module__", None):
            if has_source(obj):
                try:
                    return {".code": inspect.getsource(obj), ".module" : f"{obj.__module__}", ".name": obj.__name__}
                except Exception:
                    return {".name": obj.__name__, ".module": f"{obj.__module__}"}
    elif is_collection(obj):
        return pack_iterable(obj)
    else:
        return pack_objstate(obj)
    
def fetch_typereferences(cls):
    if inspect.isclass(cls):
        mro = inspect.getmro(cls)
        metamro = inspect.getmro(type(cls))
        metamro = tuple(cls for cls in metamro if cls not in (type, object))
        class_bases = mro
        if not type in mro and len(metamro) != 0:
            return class_bases[1:-1], metamro[0]
        else:
            return class_bases[1:-1], None
            
def fetch_funcreferences(func: object):
    if inspect.ismethod(func):
        func = func.__func__

    if not inspect.isfunction(func):
        raise TypeError("{!r} is not a Python function".format(func))

    code = func.__code__
    if func.__closure__ is None:
        nonlocal_vars = {}
    else:
        nonlocal_vars = {
            var : cell.cell_contents
            for var, cell in zip(code.co_freevars, func.__closure__)
       }

    global_ns = func.__globals__
    builtin_ns = global_ns.get("__builtins__", builtins.__dict__)
    if inspect.ismodule(builtin_ns):
        builtin_ns = builtin_ns.__dict__
    global_vars = {}
    builtin_vars = {}
    unbound_names = set()
    for name in code.co_names:
        if name in ("None", "True", "False"):
            continue
        try:
            global_vars[name] = global_ns[name]
        except KeyError:
            try:
                builtin_vars[name] = builtin_ns[name]
            except KeyError:
                unbound_names.add(name)

    return (nonlocal_vars, global_vars,
                       builtin_vars, unbound_names)
            
def deconstruct_class(cls):
    attributes = inspect.classify_class_attrs(cls)
    deconstructed = []
    for attr in attributes:
        if attr.defining_class == object or attr.defining_class == type:
            continue
        else:
            deconstructed.append((
                attr.name,
                attr.object,
                attr.kind
            ))
    return deconstructed

def deconstruct_func(func):
    references = fetch_funcreferences(func)
    func_code = inspect.getsource(func)
    return {
        ".name": func.__name__,
        ".code": func_code,
        ".references": references
    }

def getfields(obj):
    """Try to get as much attributes as possible"""
    members = inspect.getmembers(obj)
    
    cls = type(obj)
    type_attrnames = [el.name for el in inspect.classify_class_attrs(cls)]
    
    result = {}
    
    for member in members:
        if not member[0] in type_attrnames:
            result[member[0]] = member[1]
            
    return result

def deconstruct_instance(obj):
    type_ = type(obj)
    fields = getfields(obj)
    return (type_, fields)