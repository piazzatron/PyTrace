#!/Users/michaelpiazza/Documents/RayTracer/
from ray_classes import *

##functions
    
def solveQuadratic(pOrig,rDir,center,radius): ##I'm not implementing this with the fancy optimized function, if shit's broken look to this
    a=rDir.dot(rDir) ##this is the direction of the ray, squared
    b=rDir.dot((pOrig-center))*2.0
    c=(((pOrig-center).getMagnitude()**2.0)-radius**2.0)
    disc=(b**2)-(a*c*4.0) ##evaluate discriminant
    if disc<0:
        print("no hit")
        print disc
        return False
        
    elif disc==0:
        print("one hit")
        return #(b/(2.0*a))*-1.0
    else:
        print("two hits!")
        print ("discriminant is "+str(disc))
        solutions=((((b*-1.0)+math.sqrt(disc))/(a*2.0)),(((b*-1.0)-math.sqrt(disc))/(a*2.0)))
        print "solutions for t val of ray are: " + str(solutions)
        return solutions
    
def sphereRayIntersect(sphere,ray):
    intersections=[]
    tVal=solveQuadratic(ray.getOrigin(),ray.getDirection(),sphere.getCenter(),sphere.getRadius())
    for each in tVal:
        intersections.append(ray.getPoint(each))
        print "intersection point at " + str(ray.getPoint(each))
    return intersections
#draws noise of alterating black and white across the image. for testing drawing
#functions.
def drawNoise(canvas):
    color=0
    height=canvas.getHeight()
    width=canvas.getWidth()
    for x in range(height):
        if color==0: #this makes it so that each line starts as a new color
            color=1
        else:
            color=0
        for y in range(width):
            if color==0:
                canvas.getDraw().point((x,y), (0,0,0))
                color=1
            else:
                canvas.getDraw().point((x,y), (255,255,255))
                color=0
    canvas.getImg().save("noiseIMG.png","PNG")
    canvas.getImg().show()
    print("I finished drawing your noise image, Michael!")
    return
def render(height,width):
    canvas = Canvas(height,width)
    for x in width:
        for y in height:
            #make ray
            canvas.getDraw.point(x,y,trace)
def makeScene():
    return
def trace():
    return #color
def shade():
    return color
def run():
    makeScene()
    


#operations
##vec1=Vec3(2.0,4.0,6.0)
##vec2=Vec3(1.0,2.0,3.0)
##print vec1+vec2
##print vec1-vec2
##print vec1*vec2
##print vec1*5
##print vec1/4
##print vec1/vec2
##M1=Matrix44([1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4])
##M2=Matrix44([1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4])
##M3=M1*M2
##print M3
ray=Ray(Vec3(-10.0,0,0),Vec3(1.0,0.0,0.0))
sphere=Sphere(3.0,Vec3(0,0,0))
print sphereRayIntersect(sphere,ray)
ray2=Ray(Vec3(0,0,0),Vec3(0,1.0,0))
sphere2=Sphere(4.0, Vec3(0,50,0))
print sphereRayIntersect(sphere2,ray2)
##print(math.sqrt(9))
##myVec=Vec3(1,2,3)
##myVec.getMagnitude()
##
##drawNoise(Canvas(300,300))
##sphere1=Sphere(5,(0,0))
##print sceneObjList
##print sceneObjList[0].getPosition()
##vec1=Vec3(5,0,0)
##vec2=Vec3(0,5,0)
##vec3=vec1.cross(vec2)
##print vec3



##Raytracer


