# Food class

class Food:

	def __init__(self, id, x, y):
		self.id = id
		self.x = x
		self.y = y
	def __getitem__(self, key):
		if key == 0:
			return (self.x,self.y)
		else:
			return self.id