# pyparse

## Projcet structure

* pyparse_pkg
    * pyparse
        * packager
            * creator * > base instantiator
            * objectinspector * > inspect object's metadata
        * TomlParser 
        * YamlParser
        * JsonParser
        * PickleParser
    * unitests
        *  resourses (folder)* > [.json, .pickle, .toml, .yaml] test files
        *  testobjects * > data samples
        *  test * > test itself
    * tasks
    * ideas (folder) * > folder with usefull files based on previous work
