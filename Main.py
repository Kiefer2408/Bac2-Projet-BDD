import os
from Input import *
from SQL import *




if __name__ == "__main__":
	isrunning = True

	inp = Input()
	sql = SQL()
	os.system('clear')
	while isrunning:
		try:
			x = inp.read()
			match x:
				case "@exit":
					isrunning = False
				case "@clear":
					os.system('clear')
				case _:
					try:
						ast = sql.convert_to_ast(x)
						print(ast)
					except Exception as e:
						print("\033[93m" + str(e) + "\033[0m")

		# Quitte l'interpréteur SPJRUD lorsqu'une EOFError est capturée
		except (EOFError, KeyboardInterrupt):
			print("\nGoodbye !")
			exit(0)
		
	
