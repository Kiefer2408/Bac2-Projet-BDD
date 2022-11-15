import Input
import SQL


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
				ast = sql.convert_to_ast(x)
				print(ast)
	
