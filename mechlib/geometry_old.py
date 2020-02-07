from mpl_toolkits.mplot3d import Axes3D #Enables 3D functionality
import numpy

class Rotation:
    @staticmethod
    def getRotation(axis, angle=0):
        axis = axis.lower()
        
        if axis == 'x':
            matrix = (1,0,0,0,numpy.cos(angle), -numpy.sin(angle), 0, numpy.sin(angle), numpy.cos(angle))
        elif axis == 'y':
            matrix = (numpy.cos(angle), 0, numpy.sin(angle), 0, 1, 0, -numpy.sin(angle), 0, numpy.cos(angle))
        elif axis == 'z':
            matrix = (numpy.cos(angle), -numpy.sin(angle), 0, numpy.sin(angle), numpy.cos(angle), 0, 0, 0, 1)
        else:
            raise ValueError("Invalid axis '{}'; please pass one of ['x','y','z'].".format(axis))
        return numpy.reshape(matrix, (3,3))
    @staticmethod
    def rotateVector(vector3, axis, angle):
        return Vector3(name = vector3.name).setPosition(numpy.dot(Rotation.getRotation(axis, angle), vector3.getPosition()))
            
class Graphable():
    def draw(self, ax):
        raise AttributeError("Draw function not defined!")
    def rotate(self, axis, angle=0):
        raise AttributeError("Rotate function not defined!")

#A wrapper of lines and points
class Compound(Graphable):
    def __init__(self, lines = [], vectors = []):
        self.lines, self.vectors = lines, vectors
    def draw(self, ax):
        #if type(ax) is not Axes3D:
            #raise TypeError("Invalid Axes3D object passed to draw method!")
        for p in self.vectors:
            p.draw(ax)
        for l in self.lines:
            l.draw(ax)
    def add(self, o):
        if type(o) is Vector3:
            self.points.append(o)
        elif type(o) is Line:
            self.lines.append(o)
        else:
            raise TypeError("Attempted to register object of unknown type to compound graphable object")
    def rotate(self, axis, angle=0):
        print("Rotating compound object {} degrees around {}-axis.".format(axis, angle))
        for p in self.vectors:
            p.rotate(axis, angle)
        for l in self.lines:
            l.rotate(axis, angle)
    def __str__(self):
        return "Compound Graphable Object ({} Lines, {} Points)".format(len(self.lines), len(self.vectors))

#ONLY A WRAPPER FOR X, Y, Z
#pass
class Vector3(Graphable):
    def __init__(self, x=0, y=0, z=0, ox = 0, oy = 0, oz = 0, name = "Vector"):
        self.x, self.y, self.z, self.ox, self.oy, self.oz,  = x, y, z, ox, oy, oz
        self.name = name
    def __add__(self, other):
        if type(other) is Vector3:
            self.x += other.x
            self.y += other.y
            self.z += other.z
        return self
    def __str__(self):
        return "{} ({}, {}, {})".format(self.name, self.x, self.y, self.z)
    def draw(self, ax):
        ax.scatter3D([self.x], [self.y], [self.z])
    def getPosition(self):
        return (self.x, self.y, self.z)
    def setPosition(self, pos):
        self.x, self.y, self.z = pos[:3]

#Collection of 2 Points
class Line(Graphable):
    def __init__(self, p1, p2, name = "Line", draw_endpoints = True):
        if type(p1) is not Vector3:
            raise TypeError("Point 1 arg passed to line {} is not a Point!".format(name))
        if type(p2) is not Vector3:
            raise TypeError("Point 2 arg passed to line {} is not a Point!".format(name))
        self.points = (p1, p2)
        self.name = name
        self.draw_endpoints = draw_endpoints
    def draw(self, ax):
        ax.plot([self.points[0].x, self.points[1].x], [self.points[0].y, self.points[1].y], [self.points[0].z, self.points[1].z])
        if(self.draw_endpoints):
            for p in self.points:
                p.draw(ax)
    def rotate(self, axis, angle=0):
        for p in self.points:
            
            p.rotate(axis, angle)
        
    def __str__(self):
        s = "Line "
        if self.name is not "Line": 
            s += "'{}' ".format(self.name)
        return s+"[{}, {}]".format(self.points[0], self.points[1])

class Origin(Compound):
    def __init__(self, radius = 1, origin = Vector3(0,0,0, "Origin"), name = "Origin"):
        self.name = str(name)
        if type(origin) is not Vector3:
            raise TypeError("Origin passed to origin object '{}' is not a Point!".format(name))
        #if type(radius) is not float or not int:
            #raise TypeError("Radius passed to origin object '{}' is not a number!".format(name))
        p = [origin,
             Vector3(radius, 0, 0, "X-Arm Point")+origin,
             Vector3(0, radius, 0, "Y-Arm Point")+origin,
             Vector3(0, 0, radius, "Z-Arm Point")+origin]
        l = [Line(p[0], p[1]),
             Line(p[0], p[2]),
             Line(p[0], p[3])]
        super().__init__(l)
        