Web VPython 3.2
# from vpython import *
#Constants
runRate = 100 #50 times a second
elasticity = 1
level = 0
#Background
scene.background = vector(0,0,0) #RGB but out of 1
scene.userzoom = False
scene.userspin = False

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
        self.netForce = forceVector
    def checkBoundary(self):
        if (self.position.x + self.radius + self.velocity.x > (boundaryRight3D.pos.x - 5)):
            self.position.x = boundaryRight3D.pos.x - 5 - self.radius
            self.velocity.x = - self.velocity.x
        

        if (self.position.x + self.radius + self.velocity.x < (boundaryLeft3D.pos.x + 5)):
            self.position.x = boundaryLeft3D.pos.x + self.radius + 5
            self.velocity.x = - self.velocity.x

        if (self.position.y + self.radius + self.velocity.y > (boundaryTop3D.pos.y - 5)):
            self.position.y = boundaryTop3D.pos.y - self.radius - 5
            self.velocity.y = - self.velocity.y

        if (self.position.y + self.radius + self.velocity.y < (boundaryBottom3D.pos.y + 5)):
            self.position.y = boundaryBottom3D.pos.y + self.radius + 5
            self.velocity.y = - self.velocity.y
    def checkObstacles(self, obstacle):
        if (self.touchingObstacleLeftBounds(obstacle) and self.position.y < obstacle.topBox.pos.y and self.position.y > obstacle.bottomBox.pos.y):
            self.position.x = obstacle.leftBox.pos.x - 5
            self.velocity.x = - self.velocity.x
        if (self.touchingObstacleRightBounds(obstacle) and self.position.y < obstacle.topBox.pos.y and self.position.y > obstacle.bottomBox.pos.y):
            self.position.x = obstacle.leftBox.pos.x + 5
            self.velocity.x = - self.velocity.x
        if (self.touchingObstacleBottomBounds(obstacle) and self.position.x < obstacle.rightBox.pos.x and self.position.x > obstacle.leftBox.pos.x):
            self.position.y = obstacle.bottomBox.pos.y - 5
            self.velocity.y = - self.velocity.y
        if (self.touchingObstacleTopBounds(obstacle) and self.position.x < obstacle.rightBox.pos.x and self.position.x > obstacle.leftBox.pos.x):
            self.position.y = obstacle.Top.pos.y + 5
            self.velocity.y = - self.velocity.y
    
    def touchingObstacleLeftBounds(self, obstacle): 
        if (abs(((self.position.x + self.radius + self.velocity.x) - (obstacle.leftBox.pos.x))) < 0.5):
            return True
        else:
            return False
        
    def touchingObstacleRightBounds(self, obstacle):
        return (abs(((self.position.x - self.radius + self.velocity.x) - (obstacle.rightBox.pos.x))) < 0.5)
        
    def touchingObstacleTopBounds(self, obstacle):
        return (abs(((self.position.y - self.radius + self.velocity.y) - (obstacle.topBox.pos.y))) < 0.5)

    def touchingObstacleBottomBounds(self, obstacle):
        return (abs(((self.position.y + self.radius + self.velocity.y) - (obstacle.bottomBox.pos.y))) < 0.5)

        # if (self.position.x + self.radius + self.velocity.x > (obstacle.position.x - (obstacle.length / 2)) and
        #     self.position.x + self.radius + self.velocity.x < (obstacle.position.x + (obstacle.length / 2)) and
        #     self.position.y + self.radius + self.velocity.y > (obstacle.position.y - (obstacle.width / 2)) and 
        #     self.position.y + self.radius + self.velocity.y < (obstacle.position.y + (obstacle.width / 2)) 
        #     ):
            

        

    def update(self, forcer, obstacleList):
        self.calcNetForce(forcer)
        self.checkBoundary()
        for o in obstacleList:
            self.checkObstacles(o)
        # print(self.velocity)
        self.velocity = self.velocity + (self.netForce / self.mass) * (1 / runRate)
        self.position = self.position + self.velocity
        self.shape.pos = self.position

class Charges:
    def __init__(self, position, charge, chargeColor, showField):
        self.position = position
        self.charge = charge
        self.shape = cylinder(pos=self.position, axis=vector(0,0,1), radius=5, color=chargeColor)
        self.showField = showField
    def calculateElectricField(self, point):
        distanceVector = point - self.position
        forceMag = (1 / (4 * pi* 8.85 * pow(10, -12))) * (self.charge / pow(mag(distanceVector), 2))
        forceVector = vector((forceMag * distanceVector.x) / mag(distanceVector), (forceMag * distanceVector.y) / mag(distanceVector), 0) 
        return forceVector
            
class ElectricField:
    def __init__(self, forceCreators):
        self.arrowList = []
        self.forceCreators = forceCreators
        self.createElectricField()
                
    def createElectricField(self):
        for x in range(-200, 200, 20):
            for y in range(-100, 100, 20):
                ar = arrow(pos=vector(x, y, 0), axis=vector(0,0,0), color=color.green, length = 15, opacity = 1)
                # ar.visible = False
                self.arrowList.append(ar)
                
    def squash(self, x):
        greatestMag = 0
        for x in range(-200, 200, 20):
                for y in range(-100, 100, 20):
                    forceVector = vector(0,0,0)
                    for object in self.forceCreators:
                        forceVector = forceVector + object.calculateElectricField(vector(x, y, 0))
                    if (mag(forceVector) > greatestMag):
                        greatestMag = mag(forceVector)
        return x / greatestMag
                
    def enableElectricField(self):
        print("ACKLAJL:DF")
        for arrow in self.arrowList:
            arrow.visible = True
            
    def disableElectricField(self):
        for arrow in self.arrowList:
            arrow.visible = False
        
    def updateElectricField(self, forceCreatorsList):
        self.forceCreators = forceCreatorsList
        pos = 0
        for x in range(-200, 200, 20):
                for y in range(-100, 100, 20):
                    forceVector = vector(0,0,0)
                    for object in self.forceCreators:
                        forceVector = forceVector + object.calculateElectricField(vector(x, y, 0))
                    self.arrowList[pos].axis = forceVector
                    self.arrowList[pos].opacity = self.squash(mag(forceVector))
                    self.arrowList[pos].length = 15
                    pos += 1

class Obstacles:
    def __init__(self, position, charge):
        self.position = position
        self.charge = charge

#INHERITENCE DONT WORKKK
class BoxObstacle(Obstacles):
    def __init__(self, position, charge, length, width):
        self.position = position
        self.charge = charge
        self.length = length
        self.width = width
        self.shape = box(pos=self.position, length = self.length, width=5, height=self.width)
        self.topBox = box(pos=self.position + vector(0, self.width/2 - 1, 0), length = self.length - 2, width = 5, height = 1, color=color.blue)
        self.bottomBox = box(pos=(self.position - vector(0, self.width/2 - 1, 0)), length = self.length - 2, width = 5, height = 1, color=color.red)
        self.leftBox = box(pos=(self.position - vector(self.length/2 - 1, 0, 0)), length = 1, width = 5, height = self.width - 2, color=color.green)
        self.rightBox = box(pos=self.position + vector(self.length/2 - 1, 0, 0), length = 1, width = 5, height = self.width - 2, color=color.orange)

    
    def getVertices(self):
        return self.shape.bounding_box()
    
class Goal:
    def __init__(self, position):
        self.position = position
        self.shape = [box(pos=self.position, length=20, width=1, height=5), box(pos=self.position + vector(10, 20, 0), length = 5, width = 1, height = 44), box(pos=self.position + vector(0, 40, 0), length = 20, width = 1, height = 5)]
    def inGoal(self, puck):
        return puck.position.x + 5 > self.position.x - 10 and puck.position.x + 5 < self.position.x + 10 and puck.position.y + 5 < self.position.y + 40 and puck.position.y > self.position.y
            
class ChargeHolder():
    def __init__(self, position, charge):
        self.position = position
        self.charge = charge
        self.shape = box(pos=self.position, length = 20, width = 1, height = 20, color = color.cyan)
        self.color
        if (charge > 0):
            self.color = color.red
        else:
            self.color = color.blue
        self.circles = [cylinder(pos=self.position - vector(5, 5, 0), axis=vector(0,0,1), radius=2, color=self.color), cylinder(pos=self.position+vector(5, 5, 0), axis=vector(0,0,1), radius=2, color=self.color)]
class StupidMouse():
    def __init__(self):
        self.picked = False
        self.currCharge = None
        #Simulation, HomeScreen
        self.gameMode = "Homescreen"
class StartMenu():
    def __init__(self):
        self.currPick = "NONE"
        self.bg = box(texture='https://i.imgur.com/C8lDKFW.jpeg', pos=vector(0,0,0), length=500, height=300, width = 5)
        self.play = box(texture='https://i.imgur.com/JdkcbAr.jpeg', pos=vector(0, -50, 0), length = 100, height=50, width=5)
    def update(self):
        if (self.currPick == "PLAY"):
            self.play.opacity = 1
            
class GoalAnimation():
    def __init__(self):
        self.timer = 0
        self.bg = box(texture='https://i.imgur.com/hPqjcEJ.png', pos=vector(0, 0, 0), length = 500, height=300, width=5)
        self.bg.visible = False
        # self.goal.visible = False
        
    def update(self):
        if (mouse.gameMode == "GOAL"):
            self.timer = self.timer + 1
            self.bg.visible = True
            if (self.timer > 1000):
                print("timer done")
                self.bg.visible = False
                mouse.gameMode = "Simulation"
        else:
            self.timer = 0

def mouseDownEventHandler():
    #if mouse is in the charge box and mousedown is pressed
    if (mouse.gameMode == "Simulation"):
        if (scene.mouse.pos.x < positiveChargeHolder.position.x + 10 and scene.mouse.pos.x > positiveChargeHolder.position.x - 10 and scene.mouse.pos.y < positiveChargeHolder.position.y + 10 and scene.mouse.pos.y > positiveChargeHolder.position.y - 10):
            mouse.picked = True
            mouse.currCharge = "Positive"
        if (scene.mouse.pos.x < negativeChargeHolder.position.x + 10 and scene.mouse.pos.x > negativeChargeHolder.position.x - 10 and scene.mouse.pos.y < negativeChargeHolder.position.y + 10 and scene.mouse.pos.y > negativeChargeHolder.position.y - 10):
            mouse.picked = True
            mouse.currCharge = "Negative"
        
def mouseUpEventHandler():
    if (mouse.gameMode == "Simulation"):
        if (mouse.picked and mouse.currCharge == "Positive"):
            levels[level].forceCreatorsList.append(Charges(vector(scene.mouse.pos.x, scene.mouse.pos.y, 0), 1 * pow(10, -3), color.red, True))
            levels[level].electricField.updateElectricField(levels[level].forceCreatorsList)
            mouse.picked = False
        elif (mouse.picked and mouse.currCharge == "Negative"):
            levels[level].forceCreatorsList.append(Charges(vector(scene.mouse.pos.x, scene.mouse.pos.y, 0), -1 * pow(10, -3), color.blue, True))
            levels[level].electricField.updateElectricField(levels[level].forceCreatorsList)
            mouse.picked = False
        mouse.currCharge = "None"

def mouseClickHandler():
    if (mouse.gameMode == "Homescreen"):
        if (scene.mouse.pos.x < start.play.pos.x + 50 and scene.mouse.pos.x > start.play.pos.x - 50 and scene.mouse.pos.y < start.play.pos.y + 25 and scene.mouse.pos.y > start.play.pos.y - 25):
            mouse.gameMode = "Simulation"
            start.bg.visible = False
            start.play.visible = False

def ElectricFieldToggler(checkbox):
    if (checkbox.checked and len(levels[level].forceCreatorsList) > 0 and mouse.gameMode == "Simulation"):
        print("activated")
        levels[level].electricField.enableElectricField()
    else:
        levels[level].electricField.disableElectricField()
        
class Level():
    def __init__(self, name, obst, goalStartLocation, puckStartLocation, forceCreators):
        self.name = name
        self.obstacles = obst
        self.forceCreatorsList = forceCreators
        self.puck = Puck(1, vector(0, 0, 0), puckStartLocation, pow(10, -3), 5)
        self.goal = Goal(goalStartLocation)
        self.electricField = ElectricField(self.forceCreatorsList)

        
    def startLevel(self):
        if (level == int(self.name)):
            for obstacle in self.obstacles:
                obstacle.shape.visible = True
            self.puck.shape.visible = True
            self.goal.shape.visible = True
        else:
            for obstacle in self.obstacles:
                obstacle.shape.visible = False
            self.puck.shape.visible = False
            self.goal.shape.visible = False

# Levels
levels = []
forceCreator0 = [Charges(vector(-200,0,0), -1, color.blue, False)]
obstacle0 = []
levels.append(Level("0", obstacle0, vector(0, 0, 0), vector(-50, 0, 0), forceCreator0) )
forceCreator1 = [Charges(vector(0,0,0), -1, color.blue, False)]
obstacle1 = [BoxObstacle(vector(80, 0, 0), 0, 50, 20)]
levels.append(Level("1", obstacle1, vector(0, 0, 0), vector(0, 0, 0), forceCreator1) )

#Declarations
positiveChargeHolder = ChargeHolder(vector(100, 130, 0), 1)
negativeChargeHolder = ChargeHolder(vector(120, 130, 0), -1)
mouse = StupidMouse()
start = StartMenu()

goalAnimation = GoalAnimation()

scene.bind("mousedown", mouseDownEventHandler)
scene.bind("mouseup", mouseUpEventHandler)
scene.bind("click", mouseClickHandler)

checkbox(bind=ElectricFieldToggler, text="Show Electric Field")

while(True):
    rate(runRate)
    if (mouse.gameMode == "Simulation"):
        for lev in levels:
            lev.startLevel()
        for object in levels[level].forceCreatorsList:           
            levels[level].puck.update(object, levels[level].obstacles)
        if (levels[level].goal.inGoal(levels[level].puck)):
            mouse.gameMode = "GOAL"
            level = level + 1
            electricField = ElectricField(levels[level].forceCreatorsList)
            if (level > len(levels)):
                level = 0
                mouse.gameMode = "Homescreen"
            levels[level].puck.visible = False
            
    if (mouse.gameMode == "GOAL"):
            goalAnimation.update()

    #when click and drag add a new point charge to a list, then run the loop through puck and update everyone