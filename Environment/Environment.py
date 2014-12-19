import numpy as np
import random
import math
from matplotlib import pyplot as plt
from matplotlib import animation
#from Animat import Animat
from Food import Food

class Environment:

    def __init__(self, sizeX, sizeY, animatX, animatY):
        self.mapX = sizeX
        self.mapY = sizeY
        self.foodCount = 0
        self.totalFood = 0
        self.foodList = []
        self.animatX = animatX
        self.animatY = animatY
        self.webX = sizeX-4
        self.webY = sizeY-4
        self.web = [[0 for x in range(20)] for x in range(20)]
        self.caught = []

    def generateFood(self, count,minX,minY,maxX,maxY):
        i = 0
        for x in range(0,count):
            self.totalFood +=1
         
            posX = np.random.choice(np.arange(minX,maxX,1))
            posY = np.random.choice(np.arange(minY,maxY,1))

            if(self.web[posX][posY] == 1):
                food = Food(self.totalFood, posX, posY)
                i += 1
              #  print ("Food in Queue :{},({},{})".format(i,posX,posY))
                self.foodList.append(food)
                self.foodCount += 1
        #print "Food caught: ",i
        self.caught.append(i)
        if(self.totalFood == count):
            food = Food(len(self.foodList),0,0)
            self.foodList.append(food)

    def getDist(self, item):
        dist = math.sqrt((self.animatX-item[0][0])**2 + (self.animatY-item[0][1])**2)
        return dist

    def getFoodgradient(self, animatX, animatY):
        self.animatX = animatX
        self.animatY = animatY
        self.foodList = sorted(self.foodList, key=self.getDist)
      #  print ("Animat's position: {},{}".format(self.animatX,self.animatY))
        
        #for x in range(0, self.foodCount):
        #    print ("New Food id :{},({},{})".format(self.foodList[x].id,self.foodList[x].x,self.foodList[x].y))



    def canWalk(self, x, y):
        if float(x).is_integer() or float(y).is_integer():
            if(x < self.webX+1 and x >3 and y < self.webY+1 and y > 3):
                return True
        return False

    def removeFood(self, foodID):
         #print("Remove food id: {}".format(foodID))
        for food in self.foodList:
            if(food.id == foodID):
                self.foodList.remove(food)
                self.foodCount -= 1
        # for f in self.foodList:
        #     print ("Food id :{},{},{}".format(f.id,f.x,f.y))

    def update(self):
        pass

    def returnFoodID(self, x,y):
        for food in self.foodList:
            if(food.x == x and food.y == y):
                return food.id
        return -1

    def initializeWeb(self):
        a = 4
        b = 4
        for x in range(0,7):
            for y in range(0,7):
                self.web[a][b] = 1
                b += 2
            a +=2
            b = 4


