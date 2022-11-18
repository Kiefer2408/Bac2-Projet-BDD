import os
import traceback
from Input import *
from SQL import *
from Formatter import *
debug = True

HISTORY_FILE = os.path.expanduser('~/.history')
if os.path.exists(HISTORY_FILE):
    readline.read_history_file(HISTORY_FILE)

if __name__ == "__main__":
	isrunning = True

	inp = Input()
	formatter = Formatter()
	sql=SQL()
	os.system('clear')
	while isrunning:
		try:
			x = inp.read()
			spt = x.split(" ", 2)
			match spt[0]:
				case "@exit":
					isrunning = False
				case "@clear":
					os.system('clear')
				case "@use":
					dbName = spt[1]
					sql = SQL(dbName)
					if os.path.exists(f'{dbName}.db'):
						print("\033[92mDatabase Found\x1b[0m")
					else:
						print("\033[31mDatabase not found\x1b[0m")
				case "@create":
					tableName = spt[1]
					sql_request = spt[2]
					sql.createTable(tableName, sql_request)
				case _:
					try:
						ast = formatter.convert_to_ast(x)
						print(ast)
						sql_request = sql.to_sql(ast)
						print(sql_request)
					except Exception as e:
						if(debug):
							print(traceback.format_exc())
						print("\033[93m" + str(e) + "\033[0m")

		# Quitte l'interpréteur SPJRUD lorsqu'une EOFError est capturée
		except (EOFError, KeyboardInterrupt):
			print("\nGoodbye !")
			exit(0)