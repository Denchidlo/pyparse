import builtins
import os
from .pool import *
from datetime import datetime
import inspect
from types import FunctionType
from sys import builtin_module_names, modules
from packager.objectinspector import *
from packager.creator import *
from packager.pool import *

class Packer:
    def pack(self, obj: object, __globals__=globals()):
        self.metainfo = {}
        self.proceeded = []
        dump = self.dump(obj)
        if len(self.metainfo) == 0:
            return dump
        else:
            return {".META":self.metainfo, ".OBJ":dump}
    
    def funcdump(self, obj, isstatic= False):
        obj_id = id(obj)
        
        if isinstance(obj, staticmethod):
            return self.funcdump(obj.__func__, True)
        
        function_module = getattr(obj, "__module__", None)
        
        if function_module != None and function_module in builtin_module_names:
            self.metainfo.update({str(obj_id): {".metatype": "builtin func", ".name": obj.__name__, ".module": obj.__module__}})
        else:
            deconstructed = deconstruct_func(obj)
            codedump = deconstructed[".code"]
            refs = deconstructed[".references"]

            nonlocals_ = refs[0]
            globals_ = refs[1]
            builtins_ = refs[2]
            unbounds_ = refs[3]

            deconstructed_refs = {
                "nonlocals": {},
                "globals": {},
                "builtins": {},
                "unbound": {}
            }
                
            for key in nonlocals_:
                new_id = id(nonlocals_[key])
                el = self.dump(nonlocals_[key])
                deconstructed_refs["nonlocals"][key] = el

            for key in globals_:
                new_id = id(globals_[key])
                el = self.dump(globals_[key])
                deconstructed_refs["globals"][key] = el

            for key in builtins_:
                new_id = id(builtins_[key])
                el = self.dump(builtins_[key])
                deconstructed_refs["builtins"][key] = el

            for key in unbounds_:
                if key in dir(obj.__module__):
                    try:
                        exec(f"from {obj.__module__} import dump__{key}")
                        new_id = id(builtins_[key])
                        el = eval(f"dump__{key}")
                        deconstructed_refs["unbounds"][key] = str(new_id)
                    except Exception:
                        continue
            
            if self.metainfo.get(str(obj_id)) == None:
                self.metainfo.update({str(obj_id): {".code": get_code(obj), ".metatype": "func", ".name": obj.__name__, ".module": getattr(obj, "__module__", None), ".refs": deconstructed_refs}})\

            return {".metaid": str(obj_id)}            
        
    def dump(self, obj: object):
        obj_id = id(obj)       
        
        if is_none(obj):
            return None
        
        if is_primitive(obj):
            return obj
        
        if type(obj) in [list, set, tuple, dict]:
            if isinstance(obj, dict):
                result = {key:self.dump(obj[key]) for key in obj}
            elif type(obj) in [set, tuple]:
                result = {".list":[self.dump(el) for el in obj], ".collection_type":f"{obj.__class__.__name__}"}
            else:
                result = [self.dump(el) for el in obj]
            return result
        
        if isinstance(obj, datetime):
            return {".time":str(obj.isoformat())}
        
        if obj_id in self.proceeded:
            return {".metaid": str(obj_id)}
        elif not getattr(obj, "__name__", None) in dir(builtins) :
            self.proceeded.append(obj_id)


        if inspect.ismodule(obj):
            try:
                if self.metainfo.get(str(obj_id)) == None:
                    if obj.__name__ in builtin_module_names:
                        self.metainfo.update({str(obj_id):{".metatype" : "module", ".name": obj.__name__}})
                    else:
                        self.metainfo.update({str(obj_id):{".code": get_code(obj), ".metatype" : "module", ".name": obj.__name__}})
            except Exception:
                self.metainfo.update({str(obj_id):{".metatype" : "module", ".name": obj.__name__}})
            return {".metaid": str(obj_id)}
        
        if getattr(obj, "__name__", None) and not is_basetype(obj):
            if obj.__name__ in dir(builtins):
                try:
                    self.proceeded.remove(str(obj_id))
                except Exception:
                    pass
                return {".metatype" : "builtin", ".builtin": obj.__name__}
            
            if inspect.ismethod(obj) or inspect.isfunction(obj) or isinstance(obj, staticmethod):
                return self.funcdump(obj)
            
            if inspect.isbuiltin(obj):
                self.metainfo.update({str(obj_id):{".metatype": "builtin-func", ".module": obj.__module__, ".name": obj.__name__}})
                return {".metaid": str(obj_id)}
            
            if is_instance(obj):
                type_, fields = deconstruct_instance(obj)
                type_id = id(type_)
                self.dump(type_)
                    
                data = {key: self.dump(fields[key]) for key in fields}
                return { ".metaid": str(type_id), ".fields": data}
            
            if inspect.isclass(obj):
                    
                mro = fetch_typereferences(obj)
                attrs = deconstruct_class(obj)
                mro = [self.dump(el) for el in mro]
                attrs = [self.dump((el[0], self.dump(el[1]), el[2])) for el in attrs]
                    
                if self.metainfo.get(str(obj_id)) == None:
                    self.metainfo.update({str(obj_id): {".metatype": "class", ".name": obj.__name__, ".module": getattr(obj, "__module__", None), ".class": {"mro":mro, "attrs":attrs}}})
                        
                return { ".metaid": str(obj_id)}
        else:
            if inspect.ismethod(obj) or inspect.isfunction(obj) or isinstance(obj, staticmethod):
                return self.funcdump(obj)
            
            if is_instance(obj):
                type_, fields = deconstruct_instance(obj)
                type_id = id(type_)
                self.dump(type_)
                    
                data = {key: self.dump(fields[key]) for key in fields}
                return { ".metaid": str(type_id), ".fields": data}
         
        
class Unpacker:
    def unpack(self, src: object, __globals__=globals()):
        self._globals = __globals__
        if isinstance(src, dict): 
            if src.get(".META") != None and src.get(".OBJ") != None:
                self.metatypes ={}
                self.proceeded = []
                self.metadict = src[".META"]
                return self.load(src[".OBJ"])
            else:
                return self.load(src)
        
        if is_none(src):
            return None
        
        if is_primitive(src):
            return src
        
        if isinstance(src,list):
            return  [self.load(el) for el in src]
        
    def load(self, src, id_=None):
        if is_none(src):
            return None
        
        if is_primitive(src):
            return src
        
        elif isinstance(src,list):
            return [self.load(el) for el in src]
            
        
        elif isinstance(src, dict):
            if src.get(".metaid") != None and src.get(".metatype") == None:
                meta_id = src[".metaid"]
                obj = None
                
                if src[".metaid"] in self.proceeded:
                    obj = self.metatypes[meta_id]
                else:
                    obj = self.load(self.metadict[meta_id], meta_id)
                    self.metatypes[meta_id] = obj
                    self.proceeded.append(meta_id)
                if src.get(".fields"):
                    obj = create_instance(obj, self.load(src[".fields"]))
                return  obj
            
            elif src.get(".metatype"):
                metatype = src[".metatype"]
                
                if metatype == "func":
                    if src[".module"] != "__main__":
                        try:
                            exec(f'from {src[".module"]} import {src[".name"]}')
                            return eval(f'{src[".name"]}')
                        except Exception:
                            pass
                    exec(src[".code"])
                    func = eval(src[".name"])
                    refs = self.load(src[".refs"])
                    nonlocals = refs["nonlocals"]
                    globals_ = refs["globals"]
                    
                    for el in globals_:
                        if el in globals().keys():
                            continue
                        else:
                            globals()[el] = self.load(globals_[el])
                    
                    code = func.__code__
                    closures = tuple(cell_factory(nonlocals[el]) for el in code.co_freevars)

                    naked = [
                        func.__code__,
                        func.__globals__,
                        func.__name__,
                        func.__defaults__,
                        closures
                    ]

                    func = FunctionType(*naked)                    
                    return func
                
                if metatype == "builtin-func":
                    try:
                        exec(f'from {src[".module"]} import {src[".name"]}')
                        return eval(f'{src[".name"]}')
                    except Exception:
                        raise KeyError(f'builtin func "{src[".module"]}.{src[".name"]}" import failed')
                
                elif metatype == "class":
                    if src[".module"] != "__main__":
                        try:
                            exec(f'from {src[".module"]} import {src[".name"]}')
                            return eval(f'{src[".name"]}')
                        except Exception:
                            pass
                        
                    class_info = src[".class"]
                    mro = self.load(class_info["mro"])
                    cls = create_classbase(src[".name"], mro)

                    self.metatypes[id_] = cls
                    self.proceeded.append(id_)
                    
                    attrs = self.load(class_info["attrs"])
                    
                    
                        
                    return set_classattrs(cls, attrs)
                
                elif metatype == "module":
                    try:
                        exec(f'import {src[".name"]}')
                        result = eval(src[".name"])
                        return result
                    except Exception:
                        if ".code" in src.keys():
                            with open("{}/{}.py".format("/".join(modules["__main__"].__file__.split('/')[:-1]), src[".name"]), "w") as writer:
                                writer.write(src[".code"])
                            exec(f'import {src[".name"]}')
                            result = eval(src[".name"])
                            os.unlink("{}/{}.py".format("/".join(modules["__main__"].__file__.split('/')[:-1]), src[".name"]))
                            return result
                    raise KeyError(f'module"{src[".module"]}" import failed')
                
                elif metatype == "builtin":
                    if src.get(".builtin"):
                        return getattr(builtins, src[".builtin"])
                    else:
                        raise KeyError(f'builtin "{src[".builtin"]}" import failed')
                        
                else:
                    raise KeyError(f"Unexpected metatype: {metatype}")
            
            elif src.get(".collection_type"):
                if src[".collection_type"] == "tuple":
                    return tuple(el for el in self.load(src[".list"]))
                elif src[".collection_type"] == "set":
                    return set(el for el in self.load(src[".list"]))
                else:
                    return self.load(src[".list"])
            
            else:    
                res=  {
                    key: self.load(src[key]) for key in src
                }
                return res
            
            