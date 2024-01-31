import math


class Vector:
    def __init__(self, x:"float", y:"float"):
        self.x = x
        self.y = y
        self.length = math.sqrt((self.x * self.x + self.y * self.y))
        self.angle = math.atan2(y, x)

    def set_x(self, value):
        self.x = value

    def get_x(self):
        return self.x

    def set_y(self, value):
        self.y = value

    def get_y(self):
        return self.y

    def get_pos(self)->"tuple[float,float]":
        return (self.x, self.y)

    def get_length(self):
        return self.length

    def set_length(self, value):
        self.length = value
        self.cal_pos()

    def get_angle(self)->"float":
        return self.angle

    def set_angle(self, value:"float"):
        self.angle = value
        self.cal_pos()

    def cal_pos(self):
        self.x = math.cos(self.angle) * self.length
        self.y = math.sin(self.angle) * self.length

    def add(self, other: "Vector"):
        return Vector(self.x + other.get_x(), self.y + other.get_y())

    def sub(self, other: "Vector"):
        return Vector(self.x - other.get_x(), self.y - other.get_y())

    def mul(self, value):
        return Vector(self.x * value, self.y * value)

    def div(self, value):
        return Vector(self.x / value, self.y / value)


def points_distance(x1: "int", y1: "int", x2: "int", y2: "int") -> "float":
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def point_angle_to_point(x1: "int", y1: "int", x2: "int", y2: "int")->"float":
    nx = x2 - x1
    ny = y2 - y1
    return math.atan2(ny,nx)