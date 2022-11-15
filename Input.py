class Input:

	DEFAULT_DISP = "SPJRUD >> "

	def read(self, content = self.DEFAULT_DISP):
		while True:
			x = input(message)
			if(not x.isspace):
				return x

	# affiche un message dans la console
	def print(self, string):
		print(content)

	# affiche une erreur dans la console
	def print_error(self, name, desc = None):
		if(not desc)
			print(f"\033[93m{name}\033[0m")
		else:
			print(f"\033[93m{name}\n{desc}\033[0m")

	def print_table():
		