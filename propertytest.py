class Foo:
    def __init__(self):
        self._x = None

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x



q = Foo()

q.x = 3
print(q.x)
q.x = 3
