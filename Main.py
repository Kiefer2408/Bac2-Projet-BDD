import os
import traceback
from Input import *
from SQL import *
from Formatter import *
from Error import *
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
			readline.write_history_file()
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
					sql.createTable(tableName, sql.to_sql(formatter.convert_to_ast(sql_request)))
					inp.print_success("Table succesfully created")
				case "@print":
					if(len(spt)>2):
						table=f"{spt[1]} {spt[2]}"
					else:
						table=spt[1]
					sql.printTable(sql.to_sql(formatter.convert_to_ast(table)))
				case _:
					ast = formatter.convert_to_ast(x)
					sql_request = sql.to_sql(ast)
					

		# Quitte l'interpréteur SPJRUD lorsqu'une EOFError est capturée
		except (EOFError, KeyboardInterrupt):
			print("\nGoodbye !")
			exit(0)

		except CustomError as e:
			if(debug):
				print(traceback.format_exc())
			print("\033[93m" + str(e) + "\033[0m")