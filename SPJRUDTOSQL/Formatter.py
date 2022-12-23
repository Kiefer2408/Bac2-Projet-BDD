import re
from SPJRUDTOSQL import Error

# Représente une unité de langage
class Lexeme:
	# les différentes natures valables sont str, modify, link, (, ) et condition
	# Une valeur est nécessaire pour toutes les natures sauf les ()
	# La position est utilisé par les erreurs pour indiquer la source de l'erreur
	# à l'utilisateurs
	def __init__(self, nature, value=None, position=-1):
		self.nature = nature
		self.value = value
		self.position = position

	def __repr__(self):
		return str(self)

	def __str__(self):
		if(self.value):
			return f"{self.nature}:{self.value}"
		else:
			return self.nature


# représente les noeuds de l'arbre de syntaxe abstrait
class Terme:
	# différentes nature qui ont différents attributs:
	# 	table : a1 = table
	#	condition : a = condition
	# 	select : a1 = condition, a2 = table
	# 	project : a1 = " ", a2 = " "
	# 	rename : a1 = " ", a2 = " "
	# 	join : a1 = table précédente, a2 = table suivante
	# 	minus : " "
	# 	union : " "
	def __init__(self, nature, a, b=None):
		self.nature = nature
		self.a = a
		self.b = b

	def __str__(self):
		if(self.b):
			return f"[{self.nature}: {self.a} {self.b}]"
		else:
			return f"[{self.nature}: {self.a}]"


class Formatter:

	# Préfixe des commandes
	prefix = "@"

	# List des commandes disponibles (SPJRUD)
	command = ["select", "rename", "project", "join", "union", "minus"]

	# Regex vérifiant la syntaxe des conditions des commandes select, rename et 
	# project
	regex = {
		"select": "[A-Za-z0-9]+ *(=|<=|>=|<|>){1} *(\"[A-Za-z0-9]+\"|[0-9]+){1}",
		"project": "[A-Za-z0-9]+(, *[A-Za-z0-9]+)*",
		"rename": "[A-Za-z0-9]:[A-Za-z0-9]"
	}
		

	# Convertis une chaîne de caractère en Arbre de Syntaxe Abstrait (AST)
	def convert_to_ast(self, string):
		self.expr = string

		self.lexeme_list = self.to_lexeme(self.expr)
		self.current_lexeme = self.lexeme_list[0]


		self.t = self.expression()

		# Si le lexème courant n'est pas de nature EOL cela veut dire que le
		# programme n'a pas parcouru l'entièreté de l'expression
		if(self.current_lexeme.nature != "EOL"):
			raise Error.BadSyntaxError("ERROR SYNTAX")
		return(self.t)


	# Convertis une chaîne de caractère en liste de Lexeme, càd elle fragmente
	# la chaîne en unités de langage plus facile à trater
	def to_lexeme(self, expr):
		lexeme_list = list()

		# Parcours la chaîne de caractères
		i = 0
		while (i < len(expr)):
			x = expr[i]

			# ignore les espaces
			if(x.isspace()):
				i += 1
				continue

			# detecte si c'est une commande ou non
			if(x == self.prefix):
				j = i+1

				if(i == len(expr)-1):
					raise Error.UnknowCommand(expr, '', i)

				# récupère le nom de la commande : "@select{} A" -> "select"
				while(expr[j].isalpha()):
					if(j == len(expr)-1):
						j += 1
						break
					j += 1
				command = expr[i+1:j]

				if(command in ["select", "rename", "project"]):
					lexeme_list.append(Lexeme("modify", command, i))
				elif(command in ["join", "union", "minus"]):
					lexeme_list.append(Lexeme("link", command, i))
				else:
					raise Error.UnknowCommand(expr, command, i)
				i = j-1

			# detecte les chaînes de caractères (nom de table)
			if(x.isalpha()):
				j = i
				while(expr[j].isalnum()):
					if(j == len(expr)-1):
						j += 1
						break
					j += 1
				string = expr[i:j]

				# retourne une erreur si le nom de la table est le même qu'une commande
				if(string in self.command):
					raise Error.InvalidNameError(expr, string, i)

				lexeme_list.append(Lexeme("str", string, i))
				i = j-1

			#  detecte une condition
			if(x == "{"):
				j = i+1
				while(expr[j] != "}"):
					if(j == len(expr)-1):
						j += 1
						break
					j += 1
				lexeme_list.append(Lexeme("condition", expr[i+1:j], i))
				i = j

			# detecte les parentheses
			if(x in ["(", ")"]):
				lexeme_list.append(Lexeme(x, None, i))

			i += 1

		# ajoute à la fin de la liste des lexèmes EOL pour signifier la fin de 
		# la chaîne de caractères
		lexeme_list.append(Lexeme("EOL", None, i))
		return lexeme_list


	# Représente les règles de l'opération link (voir read.me)
	def expression(self):
		terme = self.facteur()
		if(self.current_lexeme.nature not in [")", "link", "EOL"]):
			raise BadSyntaxError(self.expr, "unknow error", self.current_lexeme.position)

		# accumulateur pour réaliser les opérations link en right associative
		# il consite à réaliser et passer la commande dans l'appel récursif
		while(self.current_lexeme.nature == "link"): # join, union, minus
			nature = self.current_lexeme.value
			self.next()
			right = self.facteur()
			terme = Terme(nature, terme, right)
		return terme

	# Représente les règles de l'opération modify et le reste (voir read.me)
	def facteur(self):
		match self.current_lexeme.nature:
			case "(":
				self.next()
				t = self.expression()
				if(self.current_lexeme.nature != ")"):
					raise Error.BadSyntaxError(self.expr, f"missing ')'", self.current_lexeme.position)

			case "str":
				t = Terme("table", self.current_lexeme.value)

			case "condition":
				t = Terme("condition", self.current_lexeme.value)

			case "modify": # select, rename, project
				command = self.current_lexeme.value

				self.next()
				condition = self.facteur()

				# absence de condition après une commande modify
				if(not condition or condition.nature != "condition"):
					raise Error.BadSyntaxError(self.expr, f"no condition found", self.current_lexeme.position)

				if(not re.search(self.regex.get(command), condition.a)):
					raise Error.WrongConditionSyntax(self.expr, condition.a, self.current_lexeme.position)

				table = self.facteur()
				# vérifie qu'une table possédant un nom différent que les commandes ou une expression est passée en paramètre
				if(not table 
					or table.nature not in ["table", "select", "rename", "project", "join", "union", "minus"]
					or (table.nature == "table" and table.a in ["select", "rename", "project", "join", "union", "minus"])):
					raise Error.MissingExprError(self.expr, '', self.current_lexeme.position)

				return Terme(command, condition, table)

			# EOL ne devrait jamais être catch dans les fonctions expression()
			# et facteur(), ça signifie qu'il manque des éléments
			case "EOL":
				raise Error.MissingExprError(self.expr, '', self.current_lexeme.position)

			case "link":
				raise Error.MissingExprError(self.expr, f"@{self.current_lexeme.value}", self.current_lexeme.position)

			case _:
				raise Error.BadSyntaxError(self.expr, "empty string", self.current_lexeme.position)

		# passe au lexème suivant
		self.next()
		return t

	# passe au lexeme suivant de la liste des lexèmes
	def next(self):
		if(self.lexeme_list.index(self.current_lexeme)+1 != len(self.lexeme_list)):
			self.current_lexeme = self.lexeme_list[self.lexeme_list.index(self.current_lexeme)+1]



	# SQL("select{Test=\"Adrien\"} @select{Test=\"Adrien\"} A")
	# SQL("@project{Population} ((@rename{Name:Capital} Cities) @join (@select{Country=\"Mali\"} CC))")
	# SQL("A @join B @join C")