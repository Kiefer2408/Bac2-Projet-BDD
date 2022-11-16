class CustomError(Exception):
	def __init__(self, desc, position):
		message = f"{desc} at {position}"
		super().__init__(message)


class BadSyntaxError(CustomError):
	def __init__(self, desc, position)
		super().__init__(desc, position)

# Est lancée quand le nom d'une table est invalide
class BadNameError(CustomError):
	def __init__(self, desc, position)
		super().__init__(desc, position)

# Est lancée quand le nom d'une commande n'existe pas
class UnknowCommand(CustomError):
	def __init__(self, desc, position)
		super().__init__(desc, position)

# Est lmancée quand la condition est incorrecte
class WrongConditionSyntax(CustomError):
	def __init__(self, desc, position)
		super().__init__(desc, position)