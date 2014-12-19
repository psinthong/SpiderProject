#--------- Environment with several food sources on right half of the screen only---------#

import numpy as np
import random
import sys
sys.path.append("..")
from matplotlib import pyplot as plt
from matplotlib import animation
from pylab import *
from Animat import Animat
from Environment.Environment import Environment

# Initialize an Animat

xMax = 20
yMax = 20
env = Environment(xMax, yMax, 10, 10)
animat = Animat(10, 10, xMax, yMax,env)
env.initializeWeb()
env.generateFood(15, 10,4,16,16)
foodList =[]

for e in env.foodList:
	foodList.append((e.x,e.y))
#print 'Food list : {}'.format(foodList)
foodList = zip(*foodList)
#print 'Modified : {}'.format(foodList)


# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, xMax), ylim=(0, yMax))

#------------Initial Web Structure already built------------#
data = [(4,4),(0,20),(6,6),(4,16),(8,8),(4,16),(10,10),(4,16),(12,12),(4,16),(14,14),(4,16),(16,16),(0,20),(0,20),(4,4),(4,16),(6,6),(4,16),(8,8),(4,16),(10,10),(4,16),(12,12),(4,16),(14,14),(0,20),(16,16)]

plt.plot(*data,color='k', linestyle='--')

#-------------Energy Level -------------#
ax.text(11, 1.3, 'Energy', fontsize=12)
ax.text(11, 0.3, 'Hunger', fontsize=12)
barh(0.5,animat.hunger/100, color='green', align='center', edgecolor="none")
barh(1.5,animat.energy/100, color='red', align='center', edgecolor="none")
#----------------------------------------#


ims = []
agent, = ax.plot([], [], 'rD')
blue, = ax.plot(foodList[0],foodList[1], 'bo')

# initialization function: plot the background of each frame
def init():
	
	agent.set_data([], [])

	return agent

# animation function.  This is called sequentially
def animate(i):
	#plt.close(1)
	
	if(i % 50 == 0 and i != 0):
		#print "timestep : ",i
		#print "timestep: ",i
		env.generateFood(15,10,0,16,20)
		foodList =[]
		for e in env.foodList:
			foodList.append((e.x,e.y))
		#print 'Food list : {}'.format(foodList)
		foodList = zip(*foodList)
		#print 'Modified : {}'.format(foodList)
		timestep = 0
		#animat.brain.printQ()
		#animat.brain.printV()
	

	
	oldLocation = [(animat.x,animat.y)] #Old Animat's location before calling animate()
	animat.animate()
	#-------------Energy Level -------------#
	barh(arange(2)+.5,30+rand(2), color='white', align='center', edgecolor="none")
	barh(0.5,animat.hunger/100, color='green', align='center', edgecolor="none")
	barh(1.5,animat.energy/100, color='red', align='center', edgecolor="none")
	#----------------------------------------#
	
	foodList =[]
	#---------Update Foodlist--------#
	if (env.foodList):
		for e in env.foodList:
			foodList.append((e.x,e.y))
		#print 'Food list : {}'.format(foodList)
		foodList = zip(*foodList)
		blue.set_data(foodList[0],foodList[1])
	#----------lay web---------#
	if (animat.layWeb):
		
		env.web[oldLocation[0][0]][oldLocation[0][1]] = 1
		web = [(oldLocation[0][0], animat.x),(oldLocation[0][1], animat.y)]
		env.web[animat.x][animat.y] = 1
		plt.plot(*web,color='#FE9A2E', linestyle='-')	

	agent.set_data(animat.x, animat.y)
	#print("Animat coordinate : {},{}".format(animat.x,animat.y))
	return agent


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, interval=100, blit=False)

plt.show()
