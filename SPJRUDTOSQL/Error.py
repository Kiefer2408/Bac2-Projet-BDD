class CustomError(Exception):
	def __init__(self, expr, error, desc, position):
		if(position != None):
			test = f"{' '*position}^"
			message = f"{expr}\n{test}\n{error} at {position} : {desc}"
		elif(desc != None):
			message = f"{error} : {desc}"
		else:
			message = error

		super().__init__(message)


# Erreur générique, lancée quand une erreur de syntaxe est détectée
class BadSyntaxError(CustomError):
	def __init__(self, expr, desc=None, position=None):

# Est lancée quand le nom d'une table est invalide
class InvalidNameError(CustomError):
	def __init__(self, expr, desc=None, position=None):
		super().__init__(expr, "Invalid name", desc, position)

# Est lancée quand le nom d'une commande n'existe pas
class UnknowCommand(CustomError):
	def __init__(self, expr, desc=None, position=None):
		super().__init__(expr, "Unknow command", desc, position)

# Est lmancée quand la condition est incorrecte
class WrongConditionSyntax(CustomError):
	def __init__(self, expr, desc=None, position=None):
		super().__init__(expr, "Invalid condition", desc, position)

# Est lmancée quand la condition est incorrecte
class MissingExprError(CustomError):
	def __init__(self, expr, desc=None, position=None):
		super().__init__(expr, "Missing expression", desc, position)

class NotSameAttribute(CustomError):
	def __init__(self, expr, desc=None, position=None):
		super().__init__(expr, "Not same attribute for", desc, position)

class WrongDatabaseFileName(CustomError):
	def __init__(self, expr, desc="Database must be in the same file and must be a file.db",position=None):
		super().__init__(expr, "WrongFileName for the Database ", desc, position)

class NoDatabaseException(CustomError):
	def __init__(self,desc=None,position=None):
		super().__init__(None, "No Database found, add it with @use database_name",desc,position)
		
class WrongNameException(CustomError):
	def __init__(self,desc=None,position=None):
		super().__init__(None, "This name of key doesn't exist",desc,position)
class PrintErrorException(CustomError):
	def __init__(self,desc=None,position=None):
		super().__init__(None, "Error During Print",desc,position)
