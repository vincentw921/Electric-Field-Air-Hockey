# Web VPython 3.2
from vpython import *
#Constants
runRate = 50 #50 times a second
elasticity = 1
gameMode = "Simulation"
#Background
scene.background = vector(0,0,0) #RGB but out of 1

#Boundaries
boundaryLeft3D = box(pos=vector(-200, 0, 0), length=5, width=5, height=200) 
boundaryRight3D = box(pos=vector(200, 0, 0), length=5, width=5, height=200)  
boundaryTop3D = box(pos=vector(0, 100, 0), length=405, width=5, height=5)  
boundaryBottom3D = box(pos=vector(0, -100, 0), length=405, width=5, height=5)  

# TODO: LIST:
#   1. BOUNDARY MATH FOR PUCK and GOAL IS NOT RIGHT!

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
        self.shape = cylinder(pos=self.position, axis=vector(0,0,1), radius=5, color=color.red)
    def createElectricField(self):
        return 0  

class Obstacles:
    def __init__(self, position, charge):
        self.position = position
        self.charge = charge

#INHERITENCE DONT WORKKK
class BoxObstacle(Obstacles):
    def __init__(self, position, charge, length, width):
        self.shape = box(pos=self.position, length = self.length, width=self.width, height=5)
    def getVertices(self):
        return self.shape.bounding_box()
    
class Goal:
    def __init__(self, position):
        self.position = position
        self.shape = [box(pos=self.position, length=20, width=1, height=5), box(pos=self.position + vector(10, 20, 0), length = 5, width = 1, height = 44), box(pos=self.position + vector(0, 40, 0), length = 20, width = 1, height = 5)]
    def inGoal(self, puck):
        
        if (puck.position.x + 5 > self.position.x - 10 and puck.position.x + 5 < self.position.x + 10 and puck.position.y + 5 < self.position.y + 40 and puck.position.y > self.position.y):
            print("GOALLLLL")
            
class ChargeHolder():
    def __init__(self, position, charge):
        self.position = position
        self.charge = charge
        self.shape = box(pos=self.position, length = 20, width = 1, height = 20, color = color.cyan)
    
class StupidMouse():
    def __init__(self):
        self.picked = False
        

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


def mouseDownEventHandler():
    #if mouse is in the charge box and mousedown is pressed
    if (scene.mouse.pos.x < positiveChargeHolder.position.x + 10 and scene.mouse.pos.x > positiveChargeHolder.position.x - 10 and scene.mouse.pos.y < positiveChargeHolder.position.y + 10 and scene.mouse.pos.y > positiveChargeHolder.position.y - 10):
        mouse.picked = True
        print("dong")
def mouseUpEventHandler():
    if (mouse.picked):
        forceCreatorsList.append(Charges(vector(scene.mouse.pos.x, scene.mouse.pos.y, 0), 1))
        mouse.picked = False

#Declarations
puck = Puck(1, vector(-10, 0, 0), vector(20, 20, 0), pow(10, -4), 5)
forcer = ForceCreator(vector(0, 20, 0), pow(10, -4))
goal = Goal(vector(150, 0, 0))
positiveChargeHolder = ChargeHolder(vector(100, 130, 0), 1)
mouse = StupidMouse()

forceCreatorsList = []

scene.bind("mousedown", mouseDownEventHandler)
scene.bind("mouseup", mouseUpEventHandler)

while(True):
    if (gameMode == "Simulation"):
        rate(runRate)
        for object in forceCreatorsList:
            puck.update(object)
        
        forcer.update()
        goal.inGoal(forcer)
    #when click and drag add a new point charge to a list, then run the loop through puck and update everyone
   
    