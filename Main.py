import os
import traceback
from Input import *
from SQL import *
from Convert import to_sql, createTable

debug = True

if __name__ == "__main__":
	isrunning = True

	inp = Input()
	Sql = SQL()
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
						ast = Sql.convert_to_ast(x)
						print(ast)
						sql = to_sql(ast)
						print(sql)
						createTable(sql)
					except Exception as e:
						if(debug):
							print(traceback.format_exc())
						print("\033[93m" + str(e) + "\033[0m")

		# Quitte l'interpréteur SPJRUD lorsqu'une EOFError est capturée
		except (EOFError, KeyboardInterrupt):
			print("\nGoodbye !")
			exit(0)