# Web VPython 3.2
from vpython import *
#Constants
runRate = 50 #50 times a second
elasticity = 1
gameMode = ""
#Background
scene.background = vector(0,0,0) #RGB but out of 1

#3D shapes
boundaryLeft3D = box(pos=vector(-100, 0, 0), length=5, width=5, height=100) 
boundaryRight3D = box(pos=vector(100, 0, 0), length=5, width=5, height=100)  
boundaryTop3D = box(pos=vector(0, 50, 0), length=205, width=5, height=5)  
boundaryBottom3D = box(pos=vector(0, -50, 0), length=205, width=5, height=5)  

class Puck:
    def __init__(self, mass, velocity, position, charge, radius):
        #mass is scalar, velocity is vector, position is vector
        self.mass = mass
        self.velocity = velocity
        self.charge = charge
        self.position = position
        self.netForce = vector(0,0,0)
        self.radius = radius
        self.shape = cylinder(pos=self.position, axis=vector(0,0,1), radius = 5)
    
    def calcNetForce(self, forceCreators):
        #TODO: CHECK MATH        
           
        distanceVector = self.position - forceCreators.position
        forceMag = (1 / (4 * pi* 8.85 * pow(10, -12))) * ((self.charge * forceCreators.charge) / pow(mag(distanceVector), 2))
        forceVector = vector((forceMag * distanceVector.x) / mag(distanceVector), (forceMag * distanceVector.y) / mag(distanceVector), 0) 
        self.netForce = self.netForce + forceVector
            
    def update(self, forcer):
        self.calcNetForce(forcer)
        addVelo = False
        if (self.position.x + self.radius + self.velocity.x > (boundaryRight3D.pos.x - 5)):
            self.position.x = boundaryRight3D.pos.x - 5 - self.radius
            self.velocity.x = - self.velocity.x
            addVelo = True
        

        if (self.position.x + self.radius + self.velocity.x < (boundaryLeft3D.pos.x + 5)):
            self.position.x = boundaryLeft3D.pos.x + self.radius + 5
            self.velocity.x = - self.velocity.x
            addVelo = True

        if (self.position.y + self.radius + self.velocity.y > (boundaryTop3D.pos.y - 5)):
            self.position.y = boundaryTop3D.pos.y - self.radius - 5
            self.velocity.y = - self.velocity.y
            addVelo = True

        if (self.position.y + self.radius + self.velocity.y < (boundaryBottom3D.pos.y + 5)):
            self.position.y = boundaryBottom3D.pos.y + self.radius + 5
            self.velocity.y = - self.velocity.y
            addVelo = True
        
        if (addVelo == False):
            self.velocity = self.velocity + (self.netForce / self.mass) * (1 / runRate)
        self.position = self.position + self.velocity
        self.shape.pos = self.position
        print(self.velocity)

#FOR AIR HOCKEY STRETCH GOAL
class ForceCreator:
    def __init__(self, position, charge):
        self.position = position
        self.charge = charge
        self.shape = cylinder(pos=self.position, axis=vector(0,0,1), radius=5)
    def update(self):
        self.position = scene.mouse.pos
        self.shape.pos = self.position

class Charges:
    def __init__(self, position, charge):
        self.position = position
        self.charge = charge
        self.shape = cylinder(pos=self.position, axis=vector(0,0,1), radius=5)
    def createElectricField(self):
        return 0  

        

def ray_tracing_method(x,y,poly):
    print(poly)
    n = 8
    inside = False
    xints = None
    p1x = poly[0].x
    p1y = poly[0].y
    
    print("error here")

    for i in range(n+1):
        p2x = poly[i % n].x
        p2y = poly[i % n].y
        if (y > min(p1y,p2y)):
            if (y <= max(p1y,p2y)):
                if (x <= max(p1x,p2x)):
                    if (p1y != p2y):
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if (p1x == p2x or x <= xints):
                        inside = not inside
        p1x = p2x
        p1y = p2y

    return inside        

#Declaring our one block        
puck = Puck(1, vector(-10, 0, 0), vector(20, 20, 0), pow(10, -4), 5)
forcer = ForceCreator(vector(0, 20, 0), pow(10, -4))
        
while(True):
    rate(runRate)
    puck.update(forcer)
    forcer.update()
    #when click and drag add a new point charge to a list, then run the loop through puck and update everyone
   
    