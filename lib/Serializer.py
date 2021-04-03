from Factory import SerializerFactory


class Serializer:
    def __init__(self):
        self.string = None
        self.data = None
        self.form = None

    def change_form(self, new_form):
        if self.form == new_form:
            return False
        else:
            self.string = None
            self.data = None
            self.form = new_form
            return True

    def load(self, fp):
        serializer = SerializerFactory.factory.get_serializer(self.form)
        self.data = serializer.load(fp)

    def loads(self):
        serializer = SerializerFactory.factory.get_serializer(self.form)
        self.data = serializer.loads(self.string)

    def dump(self, fp):
        serializer = SerializerFactory.factory.get_serializer(self.form)
        serializer.dump(self.data, fp)

    def dumps(self):
        serializer = SerializerFactory.factory.get_serializer(self.form)
        self.string = serializer.dumps(self.data)
