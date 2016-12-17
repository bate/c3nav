import numpy as np
from django.utils.functional import cached_property

from c3nav.mapdata.utils.misc import get_dimensions


class Route:
    def __init__(self, connections, distance=None):
        self.connections = tuple(connections)
        self.distance = sum(connection.distance for connection in self.connections)
        self.from_point = connections[0].from_point
        self.to_point = connections[-1].to_point

    def __repr__(self):
        return ('<Route (\n    %s\n) distance=%f>' %
                ('\n    '.join(repr(connection) for connection in self.connections), self.distance))

    @cached_property
    def routeparts(self):
        routeparts = []
        connections = []
        level = self.connections[0].from_point.level

        for connection in self.connections:
            connections.append(connection)
            point = connection.to_point
            if point.level and point.level != level:
                routeparts.append(RoutePart(level, connections))
                level = point.level
                connections = []

        if connections:
            routeparts.append(RoutePart(level, connections))
        print(routeparts)
        return tuple(routeparts)


class RoutePart:
    def __init__(self, level, connections):
        self.level = level
        self.level_name = level.level.name
        self.connections = connections

        width, height = get_dimensions()

        points = (connections[0].from_point, ) + tuple(connection.to_point for connection in connections)
        for point in points:
            point.svg_x = point.x * 6
            point.svg_y = (height - point.y) * 6

        x, y = zip(*((point.svg_x, point.svg_y) for point in points if point.level == level))

        self.distance = sum(connection.distance for connection in connections)

        # bounds for rendering
        self.min_x = min(x) - 20
        self.max_x = max(x) + 20
        self.min_y = min(y) - 20
        self.max_y = max(y) + 20

        width = self.max_x - self.min_x
        height = self.max_y - self.min_y

        if width < 150:
            self.min_x -= (10 - width) / 2
            self.max_x += (10 - width) / 2

        if height < 150:
            self.min_y -= (10 - height) / 2
            self.max_y += (10 - height) / 2

        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y

    def __str__(self):
        return repr(self.__dict__)


class RouteLine:
    def __init__(self, from_point, to_point, distance):
        self.from_point = from_point
        self.to_point = to_point
        self.distance = distance


class NoRoute:
    distance = np.inf
