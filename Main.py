import os
import traceback
from Input import *
from Formatter import *
from SQL import to_sql, createTable

debug = True
HISTORY_FILE = os.path.expanduser('~/.history')
if os.path.exists(HISTORY_FILE):
    readline.read_history_file(HISTORY_FILE)

if __name__ == "__main__":
	isrunning = True

	inp = Input()
	Sql = SQL()
	os.system('clear')
	while isrunning:
		try:
			x = inp.read()
			readline.write_history_file()
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