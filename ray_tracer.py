#!/Users/michaelpiazza/Documents/RayTracer/
from ray_classes import *
import random
import sys
import time
##vars
objectList = []
lightList = []
##functions

def addLight (position):
    light = Light
    light.position = position
    lightList.append(light)

def addSphere(center,radius,color, ambientColor = (0, 0, 0)):
    """

    :rtype : object
    """
    sphere = Sphere(radius,center,color, ambientColor)
    objectList.append(sphere)

def solveQuadratic(pOrig,rDir,center,radius): ##I'm not implementing this with the fancy optimized function, if shit's broken look to this
    a = rDir.dot(rDir) ##this is the direction of the ray, squared
    b = rDir.dot((pOrig-center))*2.0
    c = (((pOrig-center).getMagnitude()**2.0)-radius**2.0)
    disc = (b**2)-(a*c*4.0) ##evaluate discriminant
    if disc<0:
        return False
        
    elif disc==0:
        return #(b/(2.0*a))*-1.0
    else:
        solutions = ((((b*-1.0)+math.sqrt(disc))/(a*2.0)),(((b*-1.0)-math.sqrt(disc))/(a*2.0)))
        return solutions
    
def sphereRayIntersect(sphere,ray):

    # intersections = []
    # tVal = solveQuadratic(ray.getOrigin(),ray.getDirection(),sphere.getCenter(),sphere.getRadius())
    # for each in tVal:
    #     intersections.append(ray.getPoint(each))
    solution = solveQuadratic(ray.getOrigin(),ray.getDirection(),sphere.getCenter(),sphere.getRadius())
    if solution == False:
        return False
    parametricValue = min(solution)
    #because solveQuadratic will often return two values, we want to take the minimum (closest) of these two values
    return parametricValue



#draws noise of alternating black and white across the image. for testing drawing
#functions.
def drawNoise(canvas):
    color = 0
    height = canvas.getHeight()
    width = canvas.getWidth()
    for x in range(height):
        if color == 0: #this makes it so that each line starts as a new color
            color = 1
        else:
            color = 0
        for y in range(width):
            if color == 0:
                canvas.getDraw().point((x,y), (0,0,0))
                color = 1
            else:
                canvas.getDraw().point((x,y), (255,255,255))
                color = 0
    canvas.getImg().save("noiseIMG.png","PNG")
    canvas.getImg().show()
    print("I finished drawing your noise image, Michael!")
    return

def rasterToCamera(pixel, width, height,fov):
    # Takes a pixel from the canvas in canvas dimensions, and returns that point in worldSpace
    assert(isinstance(pixel,Pixel))
    aspectRatio = float(width) / float(height)
    fovRadian = math.radians(fov)

    def rasterToNormalized(point):
        #Normalizes the coord of the canvas pixel in a plane going from (0,1)
        pixelX = (point.x + 0.5) / width
        pixelY = (point.y + 0.5) / height
        #we add 0.5 to shoot it thru the middle of the pixel
        return Pixel(pixelX,pixelY)

    def normalizedToScreen(point):
        #remaps the normalized into a range of (-1,1) multiplied by the FOV
        remappedX = (2.0 * point.x - 1.0) * math.tan(fovRadian/2.0)
        remappedY = (1.0 - (2.0 * point.y)) * math.tan(fovRadian/2.0)
        if aspectRatio != 1:
            remappedX *= aspectRatio
        return Pixel(remappedX,remappedY)

    transformedPixel = normalizedToScreen(rasterToNormalized(pixel))
    return Vec3(transformedPixel.x, transformedPixel.y, -1.0)

def render(width, height, camera, objList):
    startTime = time.clock()
    canvas = Canvas(width,height)
    #loops through all pixels in the canvas, column by column
    for x in range(width):
        print (float(x)*100.0)/float(width)
        for y in range(height):
            computedPoint = rasterToCamera(Pixel(x,y), width, height,60.0)
            #takes the point in
            canvas.getDraw().point((x,y), trace(camera.position, computedPoint, objList))
    endTime = time.clock()
    print "Total time was  " + str(endTime - startTime)
    canvas.getImg().save("tracedImg.png","PNG")
    canvas.getImg().show()

def makeScene():
    return

def trace(cameraOrigin, imagePlanePoint,objList):

    collisionList=[]
    #We get the directional vector from the camera to the img plane point, and normalize
    directionVec = (imagePlanePoint-cameraOrigin).normalize()
    #We make the ray we're gonna trace
    traceRay = Ray(cameraOrigin,directionVec)
    #We test each object to see if it hits the traceray, and store only the closest value
    for sceneObj in objList:
        intersectionPoint = sphereRayIntersect(sceneObj,traceRay)
        if intersectionPoint != False:
            if len(collisionList)==0:
                collisionList.append(sceneObj)
                collisionList.append(intersectionPoint)
            elif intersectionPoint < collisionList[1] and intersectionPoint > 0:
                # print("old val was" + str(collisionList[1]) + "new val is " + str(intersectionPoint))
                collisionList[0], collisionList[1] = sceneObj, intersectionPoint
    if len(collisionList)>0:
        return shade(collisionList[0], traceRay.getPoint(collisionList[1]))
        #call the shade function with the neareest object, and corresponding intersection point
    return "#FFFFFF"
#take cameraOrigin, imagePlanePoint
#make a normalized direction vector from the cameraOrigin to the imagePlanePoint
#make a ray, with startpoint as origin and normalized direction vector
#for every object in the scene, loop thru the sphereIntersect function w/it and the ray
#if it hits, return the color of that sphere
#if not, return black
def shadowTest(ray):
    for object in objectList:
        #if the ray hits any object, return true: the object is in shadow. So if intersect != False, because intersect never returns true, only false, or a paremets
        intersection = sphereRayIntersect(object,ray)
        if intersection > 0:
            return True
    else:
        # print"didn't hit"
        return False


def shade(object, point):


    def tupToList(myTuple):
        return [x for x in myTuple]

    def intTuple(myTuple):
        tupList = [int(x) for x in myTuple]
        return (tupList[0], tupList[1], tupList[2])

    def lambertShade(color, ambient, angle):
        colorList = [x for x in color]
        colorList = [channel * angle for channel in colorList]
        for x in colorList:
            if x<0:
                sys.exit()
        return colorList

    def ambientAdjustment(color, ambient):
        #incorporate some scale factors 'n shit
        for i in range(len(color)):
            #first, we avoid a divide by zero error
            if color[i] == 0:
                color[i]=ambient[i]
            else:
                #if it isn't black, we find out the scale of the thing  away from the ambient color
                scaleFactor = (255.0-float(ambient[i]))/255.0
                color[i] = (color[i] * scaleFactor) + ambient[i]
        return color



    ambient = tupToList(object.ambient)

    for light in lightList:
        #this is the direction from the hit point of the ray, and the light
        directionVector = light.position - point
        #the normal off of this point in the sphere
        normalVector = point - object.getCenter()
        directionVector = directionVector.normalize()
        normalVector = normalVector.normalize()
        shadowRay = Ray(point, directionVector)
        if shadowTest(shadowRay):
            return object.ambient
        #determine the project of one normalized vector onto the other, from 0-1
        angle = normalVector.dot(directionVector)
        if angle < 0:
            angle = 0
        #convert some RGB values, scaled from 0-255
        newColor = lambertShade(object.color, object.ambient, angle)
        newColor = ambientAdjustment(newColor,ambient)
        return intTuple(newColor)
    # should return a color

def run(height,width):

    makeScene()
    camera = Camera(Vec3(0, 0, 0),Vec3(0, 0, -1.0))
    imagePlane = ImagePlane(Vec3(0, 0, -1.0), 1.0, 1.0)
    render(height,width)

def populateScene(numSpheres):
    colorList = [[(255,107,84),(90,50,50)], [(66,90,245), (45, 45, 80)], [(45,250,85), (40,70,70)],[(255, 156, 226),(128, 94, 118)],[(213, 255, 87),(122, 130, 98)]]
    for x in range(numSpheres):
        xCoor = random.randrange(-160, 160)
        yCoor = random.randrange(-100, 100)
        zCoor = random.randrange(-400, -100)
        radius = int(zCoor * -0.1 * random.uniform(1,3))
        color = random.choice(colorList)
        addSphere(Vec3(xCoor,yCoor,zCoor),radius, color[0], color[1])
addLight (Vec3(-75, 200, -100))

# addSphere(Vec3(-40, 0, -150), 75, (255,107,84), (90,50,50)) #red sphere
# addSphere(Vec3(0, 200, -400), 100, (66,90,245), (45, 45, 80)) #blue sphere
# addSphere(Vec3(-40,75,-70), 25, (45,250,85), (40,70,70)) #green sphere

populateScene(10)
def micky():
    addSphere(Vec3(0,-75.0,-600.0), 150.0, (200, 200, 200))#head
    addSphere(Vec3(-55,-60.0,-450.0), 80.0, (200, 200, 200))#muzzle
    addSphere(Vec3(-100,-25.0,-370.0), 30.0, (200, 200, 200))#nose
    addSphere(Vec3(30.0,145.0,-700.0), 140.0, (200, 200, 200)) #left ear
    addSphere(Vec3(260.0,-25,-700.0), 140.0, (200, 200, 200)) #right ear


# micky()
render(500,500,Camera(Vec3(0, 0, 0), Vec3(0, 0, -1)),objectList)


