import readline

class Input:

	DEFAULT_DISP = "SPJRUD[{}] >> "

	def read(self, dbName = "None"):
		while True:
			x = input(self.DEFAULT_DISP.format(dbName))
			if(len(x) > 0):
				return x

	def print_failed(self, name, desc = None):
		if(not desc):
			print(f"\033[91m{name}\033[0m")
		else:
			print(f"\033[91m{name}\n{desc}\033[0m")

	# affiche une erreur dans la console
	def print_warning(self, name, desc = None):
		if(not desc):
			print(f"\033[93m{name}\033[0m")
		else:
			print(f"\033[93m{name}\n{desc}\033[0m")

	def print_success(self, msg):
		print(f"\033[92m{msg}\033[0m")