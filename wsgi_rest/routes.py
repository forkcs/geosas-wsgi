from collections import namedtuple


class Route(namedtuple('Route', ('path', 'method', 'handler'))):

    def __eq__(self, other):
        if self.path == other.path and self.method == other.method:
            return True
        return False
