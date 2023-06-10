Web VPython 3.2
# from vpython import *

#Constants
runRate = 200 #50 times a second
elasticity = 1 #NOT USED
level = 0 #Current Level
#Background
scene.background = vector(0,0,0) #RGB but out of 1
scene.userzoom = False # No zooming or spinning :(
scene.userspin = False
scene.background = color.white

scene.autoscale = False
scene.range = 150

# Arena Boundaries
boundaryLeft3D = box(pos=vector(-200, 0, 0), length=5, width=5, height=200, color=vector(54.5, 0, 0)) 
boundaryRight3D = box(pos=vector(200, 0, 0), length=5, width=5, height=200, color=vector(54.5, 0, 0))  
boundaryTop3D = box(pos=vector(0, 100, 0), length=405, width=5, height=5, color=vector(54.5, 0, 0))  
boundaryBottom3D = box(pos=vector(0, -100, 0), length=405, width=5, height=5, color=vector(54.5, 0, 0))  

# TODO: LIST:
# 1. Add a different background, like white or a picture
# 2. Change color of boarders, maybe red
# 3. Create various levels
# 4. Create a game winning screen
# FINAL TODO:
# ADD MAX FORCE AND ADD FRICTION


#Our PUCK CLASS :)))
class Puck:
    def __init__(self, mass, velocity, position, charge, radius, color):
        #initializing stuffssss
        self.mass = mass
        self.velocity = velocity
        self.charge = charge
        self.position = position
        self.netForce = vector(0,0,0)
        self.radius = radius
        self.color = color
        self.shape = cylinder(pos=self.position, axis=vector(0,0,1), radius = self.radius, color=self.color)
    
    # Calculate the net force of the charges on the puck
    def calcNetForce(self, forceCreators):
        distanceVector = self.position - forceCreators.position
        maxDistanceVector = abs(self.radius + 5)
        forceMag = (1 / (4 * pi* 8.85 * pow(10, -12))) * ((self.charge * forceCreators.charge) / pow(mag(distanceVector), 2))
        
        if (abs(forceMag) > abs((1 / (4 * pi* 8.85 * pow(10, -12))) * ((self.charge * forceCreators.charge) / pow(maxDistanceVector, 2)))):
            forceMag = 0
        forceVector = vector((forceMag * distanceVector.x) / mag(distanceVector), (forceMag * distanceVector.y) / mag(distanceVector), 0) 
        self.netForce = forceVector
        
    # Make sure the puck doesn't go through the boundaries
    def checkBoundary(self):
        # 5 is boundary thickness
        if (self.position.x + self.radius + self.velocity.x > (boundaryRight3D.pos.x - 5)):
            self.position.x = boundaryRight3D.pos.x - 5 - self.radius
            self.velocity.x = - self.velocity.x
        

        if (self.position.x - self.radius + self.velocity.x < (boundaryLeft3D.pos.x + 5)):
            self.position.x = boundaryLeft3D.pos.x + self.radius + 5
            self.velocity.x = - self.velocity.x

        if (self.position.y + self.radius + self.velocity.y > (boundaryTop3D.pos.y - 5)):
            self.position.y = boundaryTop3D.pos.y - self.radius - 5
            self.velocity.y = - self.velocity.y

        if (self.position.y - self.radius + self.velocity.y < (boundaryBottom3D.pos.y + 5)):
            self.position.y = boundaryBottom3D.pos.y + self.radius + 5
            self.velocity.y = - self.velocity.y
            
    # Obstacle collision, prevents puck from going through obstacles
    def checkObstacles(self, obstacle):
        if (self.touchingObstacleLeftBounds(obstacle) and self.position.y < obstacle.topBox.pos.y and self.position.y > obstacle.bottomBox.pos.y):
            self.position.x = obstacle.leftBox.pos.x - self.radius - 5
            self.velocity.x = - self.velocity.x
        if (self.touchingObstacleRightBounds(obstacle) and self.position.y < obstacle.topBox.pos.y and self.position.y > obstacle.bottomBox.pos.y):
            self.position.x = obstacle.leftBox.pos.x + self.radius + 5
            self.velocity.x = - self.velocity.x
        if (self.touchingObstacleBottomBounds(obstacle) and self.position.x < obstacle.rightBox.pos.x and self.position.x > obstacle.leftBox.pos.x):
            self.position.y = obstacle.bottomBox.pos.y - self.radius - 5
            self.velocity.y = - self.velocity.y
        if (self.touchingObstacleTopBounds(obstacle) and self.position.x < obstacle.rightBox.pos.x and self.position.x > obstacle.leftBox.pos.x):
            self.position.y = obstacle.topBox.pos.y + self.radius + 5
            self.velocity.y = - self.velocity.y
    def touchingGoal(self, obstacle):
        if (self.touchingObstacleLeftBounds(obstacle) and self.position.y < obstacle.topBox.pos.y and self.position.y > obstacle.bottomBox.pos.y):
            self.position.x = obstacle.leftBox.pos.x - self.radius - 5
            self.velocity.x = - self.velocity.x
        if (self.touchingObstacleRightBounds(obstacle) and self.position.y < obstacle.topBox.pos.y and self.position.y > obstacle.bottomBox.pos.y):
            self.position.x = obstacle.leftBox.pos.x + self.radius + 5
            self.velocity.x = - self.velocity.x
        if (self.touchingObstacleBottomBounds(obstacle) and self.position.x < obstacle.rightBox.pos.x and self.position.x > obstacle.leftBox.pos.x):
            self.position.y = obstacle.bottomBox.pos.y - self.radius - 5
            self.velocity.y = - self.velocity.y
        if (self.touchingObstacleTopBounds(obstacle) and self.position.x < obstacle.rightBox.pos.x and self.position.x > obstacle.leftBox.pos.x):
            self.position.y = obstacle.topBox.pos.y + self.radius + 5
            self.velocity.y = - self.velocity.y
            
    # Make sure the puck doesn't go through the charges
    def checkCharges(self, charges):
        if (mag(self.position - charges.position + self.velocity) < 10):
            self.velocity.x = - self.velocity.x
            self.velocity.y = - self.velocity.y
            
    # Check if puck is touching obstacle left
    def touchingObstacleLeftBounds(self, obstacle): 
        if (abs(((self.position.x + self.radius + self.velocity.x) - (obstacle.leftBox.pos.x))) < 2.5):
            return True
        else:
            return False
        
    # Check if puck is touching obstacle right
    def touchingObstacleRightBounds(self, obstacle):
        return (abs(((self.position.x - self.radius + self.velocity.x) - (obstacle.rightBox.pos.x))) < 2.5)
        
        
    # Check if puck is touching obstacle top
    def touchingObstacleTopBounds(self, obstacle):
        return (abs(((self.position.y - self.radius + self.velocity.y) - (obstacle.topBox.pos.y))) < 2.5)

    # Check if puck is touching obstacle bottom
    def touchingObstacleBottomBounds(self, obstacle):
        return (abs(((self.position.y + self.radius + self.velocity.y) - (obstacle.bottomBox.pos.y))) < 2.5)

    # Update the position of the puck
    def update(self, forcer, obstacleList, chargeList, goal):
        self.calcNetForce(forcer)
        self.checkBoundary()
        for o in chargeList: 
            self.checkCharges(o)
        for o in obstacleList:
            self.checkObstacles(o)
        for o in goal.shape:
            self.touchingGoal(o)
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
        
    # Calculate the electric field at a point
    def calculateElectricField(self, point):
        distanceVector = point - self.position
        forceMag = (1 / (4 * pi* 8.85 * pow(10, -12))) * (self.charge / pow(mag(distanceVector), 2))
        forceVector = vector((forceMag * distanceVector.x) / mag(distanceVector), (forceMag * distanceVector.y) / mag(distanceVector), 0) 
        return forceVector
            
class ElectricField:
    def __init__(self):
        self.arrowList = []
        self.createElectricField()
                
    # Initialize the electric field
    def createElectricField(self):
        for x in range(-200, 200, 20):
            for y in range(-100, 100, 20):
                ar = arrow(pos=vector(x, y, 0), axis=vector(0,0,0), color=color.green, length = 15, opacity = 1)
                ar.visible = False
                self.arrowList.append(ar)

    # Limit the magnitude of the electric field
    def squash(x, forceCreatorsList):
        greatestMag = 0
        for x in range(-200, 200, 20):
                for y in range(-100, 100, 20):
                    forceVector = vector(0,0,0)
                    for object in forceCreatorsList:
                        forceVector = forceVector + object.calculateElectricField(vector(x, y, 0))
                    if (mag(forceVector) > greatestMag):
                        greatestMag = mag(forceVector)
        return x / greatestMag
    
    # Show the electric field
    def enableElectricField(self):
        for arrow in self.arrowList:
            arrow.visible = True
            
    # Hide the electric field
    def disableElectricField(self):
        for arrow in self.arrowList:
            arrow.visible = False
        
    # Update the electric field with the new charges
    def updateElectricField(self, forceCreatorsList):
        pos = 0
        for x in range(-200, 200, 20):
                for y in range(-100, 100, 20):
                    forceVector = vector(0,0,0)
                    for object in forceCreatorsList:
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
        self.topBox = box(pos=self.position + vector(0, self.width/2 - 1, 0), length = self.length, width = 5, height = 1, color=color.blue)
        self.bottomBox = box(pos=(self.position - vector(0, self.width/2 - 1, 0)), length = self.length, width = 5, height = 1, color=color.red)
        self.leftBox = box(pos=(self.position - vector(self.length/2 - 1, 0, 0)), length = 1, width = 5, height = self.width, color=color.green)
        self.rightBox = box(pos=self.position + vector(self.length/2 - 1, 0, 0), length = 1, width = 5, height = self.width, color=color.orange)
        self.topBox.visible = False
        self.bottomBox.visible = False
        self.leftBox.visible = False
        self.rightBox.visible = False

    # get the bounds of the box
    def getVertices(self):
        return self.shape.bounding_box()
class chargeObstacle():
    def __init__(self, position, charge, radius, color):
        self.position = position
        self.charge = charge
        self.radius = radius
        self.shape = cylinder(pos=self.position, axis=vector(0,0,1), radius = radius, color=color)

class Goal:
    def __init__(self, position, length, width):
        self.position = position
        self.length = length
        self.width=width
        self.goalLine = box(pos=self.position+vector(-8, 20, 0), length = 2, width =1, height = width, opacity = 0.5, color = color.black)
        self.shape = [BoxObstacle(self.position, 0, self.length, 5), BoxObstacle((self.position + vector(10, 20, 0)),0, 5, self.width), BoxObstacle((self.position + vector(0, 40, 0)),0, self.length, 5)]
    
    # Check if the puck is in the goal
    def inGoal(self, puck):
        return puck.position.x + 5 > self.position.x - 10 and puck.position.x + 5 < self.position.x + 15 and puck.position.y + 5 < self.position.y + 45 and puck.position.y > self.position.y + 5
            
class ChargeHolder():
    def __init__(self, position, charge):
        self.position = position
        self.charge = charge
        self.shape = box(pos=self.position, length = 20, width = 1, height = 20, color = color.cyan)
        self.text = text(text=str("+" if self.charge > 0 else "-"), pos=self.position - vector(7, 7, 0), height=15, color=color.black)
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
    
    # Update the start menu
    def update(self):
        if (self.currPick == "PLAY"):
            self.play.opacity = 1
            
class GoalAnimation():
    def __init__(self):
        self.timer = 0
        self.bg = box(texture='https://i.imgur.com/hPqjcEJ.png', pos=vector(0, 0, 0), length = 500, height=300, width=5)
        self.goal = box(texture='https://i.imgur.com/1Xp9ych.png', pos=vector(0, 0, 0), length = 100, height=50, width=5)
        self.bg.visible = False
        self.goal.visible = False
        
    # Update the goal animation
    def update(self):
        if (mouse.gameMode == "GOAL"):
            self.timer = self.timer + 1
            self.bg.visible = True
            self.goal.visible = True
            if (self.timer > 100):
                self.timer = 0
                self.bg.visible = False
                self.goal.visible = False
                mouse.gameMode = "Simulation"
        else:
            self.timer = 0

class Arena():
    def __init__(self):
        self.bg = box(pos=vector(0,0,-10), length=410, height=200, width=5, color=vector(0.34, 0.33, 0.33), opacity=0.4)
        self.midline = box(pos=vector(0,0,-10), length=20, opacity = 0.4, height = 200, width = 5, color=vector(0.6, 0, 0))
        
class MouseFollower():
    def __init__(self, charge):
        self.circle = sphere(pos=scene.mouse.pos, radius=5, color= (color.red if charge > 0 else color.blue))
        self.velocity = arrow(pos=self.circle.pos, axis=vector(0,0,0), color=color.green)
        self.velocity.visible = False
        self.circle.visible = False
    
    def update(self, puckPos):
        self.circle.pos = scene.mouse.pos
        self.updateForceDirection(puckPos)
        
    def calculateForceDirection(self, puckPos):
        direction = puckPos - self.circle.pos
        direction = direction / mag(direction)
        return direction
    
    def updateForceDirection(self, puckPos):
        self.velocity.pos = self.circle.pos
        self.velocity.axis = self.calculateForceDirection(puckPos)
        
    def hide(self):
        self.circle.visible = False
        self.velocity.visible = False

def mouseDownEventHandler():
    #if mouse is in the charge box and mousedown is pressed
    if (mouse.gameMode == "Simulation"):
        if (scene.mouse.pos.x < positiveChargeHolder.position.x + 10 and scene.mouse.pos.x > positiveChargeHolder.position.x - 10 and scene.mouse.pos.y < positiveChargeHolder.position.y + 10 and scene.mouse.pos.y > positiveChargeHolder.position.y - 10):
            mouse.picked = True
            mouseFollower = MouseFollower(1)
            mouseFollower.circle.visible = True
            mouse.currCharge = "Positive"
        if (scene.mouse.pos.x < negativeChargeHolder.position.x + 10 and scene.mouse.pos.x > negativeChargeHolder.position.x - 10 and scene.mouse.pos.y < negativeChargeHolder.position.y + 10 and scene.mouse.pos.y > negativeChargeHolder.position.y - 10):
            mouse.picked = True
            mouseFollower = MouseFollower(-1)
            mouseFollower.circle.visible = True
            mouse.currCharge = "Negative"
        
def mouseUpEventHandler():
    if (mouse.gameMode == "Simulation"):
        if (mouse.picked and mouse.currCharge == "Positive"):
            levels[level].forceCreatorsList.append(Charges(vector(scene.mouse.pos.x, scene.mouse.pos.y, 0), 1 * pow(10, -3), color.red, True))
            levels[level].updateElectricField()
            levels[level].chargeList.append(chargeObstacle(vector(scene.mouse.pos.x, scene.mouse.pos.y, 0), 0, 5, color.red))
            mouseFollower.circle.visible = False
            mouse.picked = False
        elif (mouse.picked and mouse.currCharge == "Negative"):
            levels[level].forceCreatorsList.append(Charges(vector(scene.mouse.pos.x, scene.mouse.pos.y, 0), -1 * pow(10, -3), color.blue, True))
            levels[level].updateElectricField()
            levels[level].chargeList.append(chargeObstacle(vector(scene.mouse.pos.x, scene.mouse.pos.y, 0), 0, 5, color.blue))
            mouseFollower.circle.visible = False
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
        
def ForceDirectionToggler(checkbox):
    if (checkbox.checked and mouse.gameMode == "Simulation" and mouse.picked == True):
        mouseFollower.velocity.visible = True
    else:
        mouseFollower.velocity.visible = False
        
class Level():
    def __init__(self, name, obst, goalStartLocation, puckStartLocation, forceCreators):
        self.name = name
        self.obstacles = obst
        self.forceCreatorsList = forceCreators
        self.puckStartLocation = puckStartLocation
        self.goalStartLocation = goalStartLocation
        self.puck = Puck(5, vector(0, 0, 0), puckStartLocation, pow(10, -3), 5, color.black)
        self.goal = Goal(goalStartLocation, 20, 45)
        self.electricField = ElectricField(self.forceCreatorsList)
        self.chargeList = []
        
    def startLevel(self, gameMode):
        if (level == int(self.name) and gameMode == "Simulation"):
            for obstacle in self.obstacles:
                obstacle.shape.visible = True
            for obstacle in self.chargeList:
                obstacle.shape.visible = True
            for charge in self.forceCreatorsList:
                charge.shape.visible = True
            self.puck.shape.visible = True
            self.goal.shape.visible = True
        else:
            for obstacle in self.obstacles:
                obstacle.shape.visible = False
            for obstacle in self.chargeList:
                obstacle.shape.visible = False
            for charge in self.forceCreatorsList:
                charge.shape.visible = False
            self.puck.shape.visible = False
            self.goal.shape.visible = False
            
    def updateElectricField(self):
        self.electricField.updateElectricField(self.forceCreatorsList)
        
def addLevels():
    for lev in levels:
            lev.startLevel("Homescreen")
    levels.clear()
    forceCreator0 = []
    obstacle0 = []
    levels.append(Level("0", obstacle0, vector(150, -25, 0), vector(-50, 0, 0), forceCreator0) )
    forceCreator2 = []
    obstacle2 = [BoxObstacle(vector(100,0,0), 0, 50, 20), BoxObstacle(vector(100,0,0), 0, 50, -20)]
    levels.append(Level("1", obstacle2, vector(150,-25,0), vector(-75, 0, 0), forceCreator2) )
    forceCreator3 = []
    obstacle3 = [BoxObstacle(vector(100,0,0), 0, 50, 20), BoxObstacle(vector(100,0,0), 0, 50, -20), BoxObstacle(vector(100,0,0), 0, 50, 60)]
    levels.append(Level("2", obstacle3, vector(150,-25,0), vector(-75, 0, 0), forceCreator3) )
    forceCreator4 = []
    obstacle4 = [BoxObstacle(vector(25,-50,0), 0, 10, 100), BoxObstacle(vector(50,50,0), 0, 10, 100), BoxObstacle(vector(75, -50, 0), 0, 10, 100), BoxObstacle(vector(100, 0, 0), 0, 10, 100)]
    levels.append(Level("3", obstacle4, vector(150,-25,0), vector(-75, 0, 0), forceCreator4) )


def changePuckSize(slider):
    for le in levels:
        le.puck.shape.radius=slider.value

def changePuckMass(slider):
    for le in levels:
        le.puck.mass = slider.value

def levelNumber():
    return level        

def resetLevel():
    addLevels()

#Declarations: our charge holders where you can drag charges from and or mouse and startMenu classes
arena = Arena()
positiveChargeHolder = ChargeHolder(vector(160, 115, 0), 1)
negativeChargeHolder = ChargeHolder(vector(185, 115, 0), -1)
mouse = StupidMouse()
start = StartMenu()
mouseFollower = MouseFollower(-1)


# Levels (list)
levels = []
addLevels()

goalAnimation = GoalAnimation()

#binding events to keys n stuff
scene.bind("mousedown", mouseDownEventHandler)
scene.bind("mouseup", mouseUpEventHandler)
scene.bind("click", mouseClickHandler)

checkbox(bind=ElectricFieldToggler, text="Show Electric Field")
checkbox(bind=ForceDirectionToggler, text="Show Force Direction")

wtext(text="\n\nPuck Size")
slider(bind=changePuckSize, min=5, max=10, step=1, pos=scene.caption_anchor)
wtext(text="\n\nPuck Mass")
slider(bind=changePuckMass, min=1, max=10, step=1, pos=scene.caption_anchor)
button(bind=resetLevel, text="Reset Level", pos=scene.caption_anchor)
wtext(text="\n\nLevel")
levelSlider = slider(bind=levelNumber,min=0, max=len(levels), step=1, pos=scene.caption_anchor)

while(True):
    rate(runRate)
    if (mouse.gameMode == "Homescreen"):
        positiveChargeHolder.text.visible = False
        negativeChargeHolder.text.visible = False
        start.bg.visible = True
        start.play.visible = True
    if (mouse.gameMode == "Simulation"):
        levelSlider.value = level
        positiveChargeHolder.text.visible = True
        negativeChargeHolder.text.visible = True
        mouseFollower.update(levels[level].puck.position)
        for lev in levels:
            lev.startLevel(mouse.gameMode)
        for object in levels[level].forceCreatorsList:           
            levels[level].puck.update(object, levels[level].obstacles, levels[level].chargeList, levels[level].goal)
        if (levels[level].goal.inGoal(levels[level].puck)):
            mouse.gameMode = "GOAL"
            level = level + 1
            if (level >= len(levels)):
                level = -1
                for lev in levels:
                    lev.startLevel(mouse.gameMode)
                level = 0
                mouse.gameMode = "Homescreen"
                levels = []
                addLevels()
            electricField = ElectricField(levels[level].forceCreatorsList)
            
    if (mouse.gameMode == "GOAL"):
            goalAnimation.update()

    #when click and drag add a new point charge to a list, then run the loop through puck and update everyonel