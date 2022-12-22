import traceback
from Input import *
from configparser import ConfigParser
from SPJRUDTOSQL.SPJRUD import *
from SPJRUDTOSQL.Error import *

debug = False
config = ConfigParser(allow_no_value=True)

HISTORY_FILE = os.path.expanduser('~/.history')
CONFIG_FILE = os.path.expanduser('config.ini')

if os.path.exists(HISTORY_FILE):
	readline.read_history_file(HISTORY_FILE)

if __name__ == "__main__":
	isrunning = True

	inp = Input()
	config.read(CONFIG_FILE)
	if(config.has_option("main", "dbName")):
		spjrud = SPJRUD(config.get("main", "dbName"))
	else:
		config.add_section("main")
		with open(CONFIG_FILE, 'w') as f:
			config.write(f)

		spjrud=SPJRUD()

	os.system('clear')

	while isrunning:
		try:
			x = inp.read(spjrud.dbFileName)
			readline.write_history_file()
			spt = x.split(" ", 2)

			match spt[0]:
				case "@exit":
					isrunning = False
				case "@clear":
					os.system('clear')
				case "@use":
					dbName = spt[1]
					if os.path.exists(f'{dbName}.db'):

						config.set("main", "dbname", dbName)
						with open(CONFIG_FILE, 'w') as f:
							config.write(f)

						spjrud = SPJRUD(dbName)
						print("\033[92mDatabase Found\x1b[0m")
					else:
						print("\033[31mDatabase not found\x1b[0m")
				case "@create":
					tableName = spt[1]
					sql_request = spt[2]
					spjrud.createTable(tableName, spjrud.sqlTraductor(sql_request))
					inp.print_success("Table succesfully created")
				case "@print":
					if(len(spt)>2):
						table=f"{spt[1]} {spt[2]}"
					else:
						table=spt[1]
					spjrud.printTable(spjrud.sqlTraductor(table))
				case _:
					print(spjrud.sqlTraductor(x))
					

		# Quitte l'interpréteur SPJRUD lorsqu'une EOFError est capturée
		except (EOFError, KeyboardInterrupt):
			print("\nGoodbye !")
			exit(0)

		except CustomError as e:
			if(debug):
				print(traceback.format_exc())
			inp.print_failed(str(e))