import os
import traceback
from Input import *
from Formatter import *
from SQL import *
from Formatter import *
debug = True

if __name__ == "__main__":
	isrunning = True

	inp = Input()
	formatter = Formatter()
	sql=SQL()
	os.system('clear')
	while isrunning:
		try:
			x = inp.read()
			match x:
				case "@exit":
					isrunning = False
				case "@clear":
					os.system('clear')
				case "@use":
					dbName = inp.read("\033[96mUSE >>\x1b[0m")
					sql = SQL(dbName)

					if os.path.exists(f'{dbName}.db'):
						print("\033[92mDatabase Found\x1b[0m")
					else:
						print("\033[31mDatabase not found\x1b[0m")
				case _:
					try:
						print(x)
						ast = formatter.convert_to_ast(x)
						print(ast)
						sql = SQL.to_sql(ast)
						print(sql)
					except Exception as e:
						if(debug):
							print(traceback.format_exc())
						print("\033[93m" + str(e) + "\033[0m")

		# Quitte l'interpréteur SPJRUD lorsqu'une EOFError est capturée
		except (EOFError, KeyboardInterrupt):
			print("\nGoodbye !")
			exit(0)