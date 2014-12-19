import random
import numpy
from Environment.Environment import Environment
from pybrain.tools.shortcuts import buildNetwork
from QLearn import QLearn

class Animat:
	PossibleActions = [0,1,2,3,4,5,6]
	def __init__(self, x, y, mapX, mapY,env):

		self.x = x
		self.y = y
		self.webX = mapX-4
		self.webY = mapY-4
		self.energy = 1000
		self.hunger = 1000
		self.location = (self.x, self.y)
		self.layWeb = False
		self.env = env
		self.lastState = None
		self.lastAction = 0
		
		self.brain = QLearn(Animat.PossibleActions) #-----Initialize animat's brain----#


	def animate(self):
		
		#--------Get current State--------#
		curState = self.getState()
		actionChosen = self.brain.chooseAction(curState)
		#--------Update Animat's energy levels------#
		if self.energy > 0:
			self.energy -= 0.5
		if self.hunger < 1000:
			self.hunger += 0.1
		#--------Calculate rewards from the selected action--------#
		selectedAction = actionChosen
		self.performAction(selectedAction)
		reward = self.getReward(curState,selectedAction)
		nextState = self.getState()
		#print "curState :",curState," Action:",selectedAction," reward:",reward," next:",nextState," web:",self.layWeb
		self.brain.learn(curState, selectedAction, reward, nextState)



	def performAction(self, selectedAction):
		self.layWeb = 0
		if selectedAction == 0:
			self.explore(0)
		elif selectedAction == 1:
			self.explore(1)
		elif selectedAction == 2:
			self.explore(2)
		elif selectedAction == 3:
			self.explore(3)
		elif selectedAction == 4:
			self.eat()
			#print "Eat"
		elif selectedAction == 5:
			self.layWeb = 1
			if (self.findFood() < 4):
				direct = self.findFood()
			else:
				direct = random.randrange(0,4)
			self.explore(direct)
		elif selectedAction ==6:
			pass
		else:
			pass



	def explore(self,direction):
		#direction = random.randrange(0,5)
		direction = direction
		if direction == 0:
			if (self.y+1 < self.webY+1 and self.env.canWalk(self.x,self.y+1)):
				self.y += 1
			else: pass
		if direction == 1:
			if (self.x+1 < self.webX+1 and self.env.canWalk(self.x+1,self.y)):
				self.x += 1
			else: pass
		if direction == 2:
			if (self.x-1 > 3 and self.env.canWalk(self.x-1,self.y)):
				self.x -= 1
			else: pass
		if direction == 3:
			if (self.y-1 > 3 and self.env.canWalk(self.x,self.y-1)):
				self.y -= 1
			else: pass

	def eat(self):
		if (self.env.returnFoodID(self.x,self.y) != -1):
			if self.energy < 960:
				self.energy += 40
			if self.hunger > 0:
				self.hunger -= 20
			self.env.removeFood(self.env.returnFoodID(self.x,self.y))			
		else:
			pass

	def findFood(self):
		direction = 0
		# self.env.getFoodgradient(self.x,self.y)
		if (self.env.foodList):
			self.env.getFoodgradient(self.x,self.y)
			for i in range(0, len(self.env.foodList)):
				if (self.env.canWalk(self.env.foodList[i].x,self.env.foodList[i].y)):
					foodTarget = self.env.foodList[i]
					if (self.x != foodTarget.x):
						if(self.x < foodTarget.x):
							direction = 1
							if(self.x > foodTarget.x-2 and self.x < foodTarget.x+2 and self.y > foodTarget.y-2 and self.y < foodTarget.y+2):
								direction += 6
								#print "close to food:",self.x,",",self.y,"f:",foodTarget.x,",",foodTarget.y
							#print "east"
							return direction
						elif(self.x > foodTarget.x):

							direction = 2
							if(self.x > foodTarget.x-2 and self.x < foodTarget.x+2 and self.y > foodTarget.y-2 and self.y < foodTarget.y+2):
								direction += 6
							return direction
					elif (self.y != foodTarget.y):
						if(self.y < foodTarget.y):
							direction = 0
							if(self.y > foodTarget.y-2 and self.y < foodTarget.y+2 and self.x > foodTarget.x-2 and self.x < foodTarget.x+2):
								direction += 6
							return direction
						elif(self.y > foodTarget.y):

							direction += 3
							if(self.y > foodTarget.y-2 and self.y < foodTarget.y+2 and self.x > foodTarget.x-2 and self.x < foodTarget.x+2):
								direction += 6

							return direction
					else:
						if(self.hunger > 0):
							direction = 4

						else:
							direction = 10
						return direction
		
		direction = 5
		return direction

	def getState(self):
		state = self.findFood()
		
		return state 

	def getReward(self, state, action):
		reward = -1
		state = state
		action = action
		if(action < 4 and action == state): #----- follow food gradient----#
			reward += 10
		elif(state == 4):
			if(action == 4):
				reward += 50
			else:
				reward = -30
		elif(state == 10): #------On top of food b/ not hungry----#
			if(action == 5):
				reward += 50
			elif(action == 4):
				reward =-1

		elif(state == 5):	#------No food -----#	
			if(action == 6):
				reward += 10
			elif(action != 4 and action != 5):
				reward += 5
			else:
				reward -= 10
		if(state > 5 and state == action+6): #----- close to food source---#
			reward += 10
		if(state > 5 and action == 5):
			reward += 50
		return reward 
    

