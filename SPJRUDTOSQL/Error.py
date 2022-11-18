class CustomError(Exception):
	def __init__(self, error, desc, position):
		if(position != None):
			message = f"{error} : {desc} at {position}"
		elif(desc != None):
			message = f"{error} : {desc}"
		else:
			message = error

		super().__init__(message)


# Erreur générique, lancée quand une erreur de syntaxe est détectée
class BadSyntaxError(CustomError):
	def __init__(self, desc=None, position=None):
		super().__init__("Bad syntax", desc, position)

# Est lancée quand le nom d'une table est invalide
class BadNameError(CustomError):
	def __init__(self, desc=None, position=None):
		super().__init__("Bad name", desc, position)

# Est lancée quand le nom d'une commande n'existe pas
class UnknowCommand(CustomError):
	def __init__(self, desc=None, position=None):
		super().__init__("Unknow command", desc, position)

# Est lmancée quand la condition est incorrecte
class WrongConditionSyntax(CustomError):
	def __init__(self, desc=None, position=None):
		super().__init__("Bad condition", desc, position)

# Est lmancée quand la condition est incorrecte
class MissingExprError(CustomError):
	def __init__(self, desc=None, position=None):
		super().__init__("Missing expression", desc, position)
class NotSameAttribute(CustomError):
	def __init__(self,desc=None,position=None):
		super().__init__("Not same attribute for",desc,position)
class WrongDatabaseFileName(CustomError):
	def __init__(self,desc="Database must be in the same file and must be a file.db",position=None):
		super().__init__("WrongFileName for the Database ", desc, position)
class NoDatabaseException(CustomError):
	def __init__(self,desc=None,position=None):
		super().__init__("No Database found, add it with @use database_name",desc,position)