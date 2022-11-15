import Error

class Table:

	def __init__(names, value):
		if(len(value) == len(value[0])):
			pass
		else:
			raise SizeError()

