#!/usr/bin/python
from PIL import Image, ImageDraw
import math



class SceneObj(object):
    ##this is just a superclass of Sphere currently, but will be used to eventually house all renderable objects
    def __init__(self):
        sceneObjList.append(self)

class Light(object):
    def __init__(self, position):
        self.position=position

class Pixel(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"
class Sphere(SceneObj):
    def __init__(self,radius, center, color, ambColor = (0, 0, 0)):
        self.radius = radius
        self.center = center
        self.color = color
        self.ambient = ambColor
    def getRadius(self):
        return self.radius
    def getCenter(self):
        return self.center


class Canvas(object):
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.img = Image.new("RGB",(width,height),"white")
        self.draw = ImageDraw.Draw(self.img)
    def getHeight(self):
        return self.height
    def getWidth(self):
        return self.width
    def getImg(self):
        return self.img
    def getDraw(self):
        return self.draw

class ImagePlane(object):
    def __init__(self,position,height,width):
        self.position=position
        self.height=height
        self.width=width

class Camera(object):
    def __init__(self, position, direction):
        self.direction = direction
        self.position = position

    def setPosition(self,otherVec3):
        self.position = otherVec3

    def setDirection(self,otherVec3):
        self.direction=otherVec3


class Ray(object):
    def __init__(self,Po,rDir):
        self.Po = Po
        self.rDir = rDir
    def getOrigin(self):
        return self.Po
    def getDirection(self):
        return self.rDir
    def getPoint(self,t):
        return (self.Po + self.rDir*t)


class Vec3(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):

        return str(self.x)+","+str(self.y)+","+str(self.z)
    def __add__(self,other):

        return Vec3(self.x+other.x,self.y+other.y,self.z+other.z)
    def __sub__(self,other):

        if type(other)==Vec3:
            return Vec3(self.x-other.x,self.y-other.y,self.z-other.z)
    def __mul__(self,other):

        if type(other)==Vec3:
            return Vec3(self.x*other.x, self.y*other.y,self.y*other.z)
        else:
            return Vec3(self.x*other, self.y*other, self.z*other)
    def __div__(self,other):

        if type(other)==Vec3:
            return Vec3(self.x/other.x, self.y/other.y, self.z/other.z)
        else:
            inv = (1.0/other)
            return Vec3(self.x*inv, self.y*inv, self.z*inv)
    def getMagnitude(self):
        return math.sqrt(self.x**2+self.y**2+self.z**2)
    def normalize(self):
        mag = self.getMagnitude()
        if mag==0:
            return
        else:
            inverseMag = (1/mag) ##a little optimization, so we're multiplying by inverse instead of dividing each time
            normalVec = Vec3(self.x*inverseMag,self.y*inverseMag,self.z*inverseMag)
            return normalVec
    def dot(self,other):
        return self.x*other.x + self.y*other.y + self.z*other.z
    def cross (self, other):
        return Vec3(
            self.y*other.z - self.z * other.y,
            self.z*other.x - self.x *other.z,
            self.x*other.y - self.y * other.x
            )
    def getAngle(self,other):
        selfNorm = self.normalize()
        otherNorm = other.normalize()
        return math.degrees(math.acos(selfNorm.dot(otherNorm)))

class Matrix44(object):


    def __init__(self, r0,r1,r2,r3):
        self.r0 = r0
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.m = [self.r0, self.r1, self.r2, self.r3]
    def __mul__(self,other):
        if type(other)==Matrix44:
            print ("ees two matricies")
            prodM = Matrix44([0]*4,[0]*4,[0]*4,[0]*4)
            for row in range(4):
                for column in range(4):
                    prodM.m[row][column] = (
                        self.m[row][0]*other.m[0][column]+
                        self.m[row][1]*other.m[1][column]+
                        self.m[row][2]*other.m[2][column]+
                        self.m[row][3]*other.m[3][column])
            return prodM
        else:
            print ("no es 2 matricies")
            return
    def __str__(self):
        return str(self.m)
        
    
    
