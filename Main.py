from Input import *
from SQL import *


if __name__ == "__main__":
	isrunning = True

	inp = Input()
	sql = SQL()
	while isrunning:
		x = inp.read()
		match x:
			case "@exit":
				isrunning = False
			case _:
				try:
					ast = sql.convert_to_ast(x)
					print(ast)
				except Exception as e:
					print("\033[93m" + str(e) + "\033[0m")
	
