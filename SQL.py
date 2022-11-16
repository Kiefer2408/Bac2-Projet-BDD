import re
from Error import *

# Représente une unité de langage
class Lexeme:
	# les différentes natures sont str, modify, link, (, ) et condition
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

# représente les arbres de syntaxe abstraites
class Terme:
	# différentes nature qui ont différents attributs:
	# 	table : a1 = table
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


class SQL:

	# préfixe des commandes
	prefix = "@"

	command = ["select", "rename", "project", "join", "union", "minus"]

	regex = {
			"select": "[A-Za-z0-9]+ *(=|<=|>=|<|>){1} *(\"[A-Za-z0-9]+\"|[0-9]+){1}",
			"project": "[A-Za-z0-9]+(, *[A-Za-z0-9]+)*",
			"rename": "[A-Za-z0-9]:[A-Za-z0-9]"
		}
		

	def convert_to_ast(self, string):
		self.lexeme_list = self.to_lexeme(string)
		print(self.lexeme_list)
		self.lc = self.lexeme_list[0]
		self.t = self.expression()
		if(self.lc.nature != "EOL"):
			raise BadSyntaxError("ERROR SYNTAX")
		return(self.t)


	# Convertis une chaîne de caractère en Lexeme, càd elle fragmente la chaîne en unité de langage
	def to_lexeme(self, expr):
		lexeme_list = list()

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
					raise UnknowCommand(self.prefix, i)

				while(expr[j].isalpha()):
					if(j == len(expr)-1):
						j += 1
						break
					j += 1

				# récupère le nom de la commande : "@select{} A" -> "select"
				command = expr[i+1:j]

				if(command in ["select", "rename", "project"]):
					lexeme_list.append(Lexeme("modify", command, i))
				elif(command in ["join", "union", "minus"]):
					lexeme_list.append(Lexeme("link", command, i))
				else:
					raise UnknowCommand(command, i)

				i = j-1

			if(x.isalpha()):
				j = i
				while(expr[j].isalpha()):
					if(j == len(expr)-1):
						j += 1
						break
					j += 1
				string = expr[i:j]
				if(string in self.command):
					raise BadNameError(string, i)
				lexeme_list.append(Lexeme("str", string, i))
				i = j-1
			
			if(x == "{"):
				j = i+1
				while(expr[j] != "}"):
					if(j == len(expr)-1):
						j += 1
						break
					j += 1
				lexeme_list.append(Lexeme("condition", expr[i+1:j], i))
				i = j

			if(x in ["(", ")"]):
				lexeme_list.append(Lexeme(x, None, i))

			i += 1
		lexeme_list.append(Lexeme("EOL", None, i))
		return lexeme_list

	# truc compliqué à expliquer
	def expression(self):
		t = self.facteur()
		if(self.lc.nature not in [")", "link", "EOL"]):
			raise Exception("ERROR : INVALID SYNTAX")
		while(self.lc.nature == "link"):
			nature = self.lc.value
			self.next()
			r = self.facteur()
			t = Terme(nature, t, r)
		return t

	# truc compliqué à expliquer bis
	def facteur(self):
		print(self.lc.nature)
		match self.lc.nature:
			case "(":
				self.next()
				t = self.expression()
				if(self.lc.nature != ")"):
					raise BadSyntaxError(f"ERROR : MISSING )")
			case "str":
				t = Terme("table", self.lc.value)
			case "condition":
				t = Terme("condition", self.lc.value)

			# (, modify, condition, table, )
			case "modify":
				nature = self.lc.value
				self.next()
				condition = self.facteur()
				if(not condition or condition.nature != "condition"):
					raise BadSyntaxError(condition)
				if(not re.search(self.regex.get(nature), condition.a)):
					raise WrongConditionSyntax(condition.a)
				table = self.facteur()
				print(table)
				if(not table or (table.nature == "table" and table.a in ["select", "rename", "project", "join", "union", "minus"])):
					raise MissingExprError(table.nature)
				return Terme(nature, condition, table)
			case "EOL":
				return None
			case _:
				raise BadSyntaxError("empty string")
		self.next()
		return t

	# passe au lexeme suivant  @project{popu} (@rename{popu:popu} A)
	def next(self):
		if(self.lexeme_list.index(self.lc)+1 != len(self.lexeme_list)):
			self.lc = self.lexeme_list[self.lexeme_list.index(self.lc)+1]

	def __str__(self):
		return self.sql

if __name__ == "__main__":
	sql = SQL()
	while True:
		x = input("SPJRUD >>")
		if(x == "@exit"):
			break
		try:
			print(sql.convert_to_ast(x))
		except Exception as e:
			print("\033[93m" + str(e) + "\033[0m")


	# SQL("select{Test=\"Adrien\"} @select{Test=\"Adrien\"} A")
	# SQL("@project{Population} ((@rename{Name:Capital} Cities) @join (@select{Country=\"Mali\"} CC))")
	# SQL("A @join B @join C")
