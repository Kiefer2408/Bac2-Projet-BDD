import readline

class Input:

	DEFAULT_DISP = "SPJRUD >> "

	def read(self, content = DEFAULT_DISP):
		while True:
			x = input(content)
			if(len(x) > 0):
				return x

	# affiche une erreur dans la console
	def print_warning(self, name, desc = None):
		if(not desc):
			print(f"\033[93m{name}\033[0m")
		else:
			print(f"\033[93m{name}\n{desc}\033[0m")

	def print_success(self, msg):
		print(f"\033[92m{msg}\033[0m")