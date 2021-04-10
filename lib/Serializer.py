from lib.Factory import SerializerFactory


class Serializer:
    def __init__(self, default_form="json"):
        self.string = None
        self.data = None
        self.form = default_form

    def change_form(self, new_form):
        if self.form == new_form:
            return False
        else:
            self.string = None
            self.data = None
            self.form = new_form
            return True

    def load(self, fp, unpack=True):
        serializer = SerializerFactory.factory.get_serializer(self.form)
        self.data = serializer.load(fp, unpack)

    def loads(self):
        serializer = SerializerFactory.factory.get_serializer(self.form)
        self.data = serializer.loads(self.string)

    def dump(self, fp, unpacked=True):
        serializer = SerializerFactory.factory.get_serializer(self.form)
        serializer.dump(self.data, fp, unpacked)

    def dumps(self):
        serializer = SerializerFactory.factory.get_serializer(self.form)
        self.string = serializer.dumps(self.data)
