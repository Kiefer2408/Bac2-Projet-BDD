class Expr:

	def __init__(self, left, right):
		self.right = right
		self.left = left

	def get_left(self):
		return self.left

	def get_right(self):
		return self.right



class SQL:

	def __init__(self, str):
		if(isValid(str)):
			self.str = str


	# check validity of the spjrud string
	def isValid(self, str):
		pass

	def __str__(self)

class Select (Expr):
	def __int__(self):
		pass


class Project(Expr):
	def __init__(self,element):
		pass
	def __str__(self):
		return "project "

