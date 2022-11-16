import re
from Error import *

# Représente une unité de langage
class Lexeme:

	# les différentes natures sont str, modify, link, (, ) et condition
	def __init__(self, nature, value=None):
		self.nature = nature
		self.value = value

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
	def __init__(self, nature, a1, a2=None):
		self.nature = nature
		self.a1 = a1
		self.a2 = a2

	def __str__(self):
		return f"[{self.nature}: {self.a1} {self.a2}]"

class SQL:

	# préfixe des commandes
	prefix = "@"

	regex = {
			"select": "[A-Za-z0-9]+ *(=|<=|>=|<|>){1} *(\"[A-Za-z0-9]+\"|[0-9]+){1}",
			"project": "[A-Za-z0-9]+(, *[A-Za-z0-9]+)*",
			"rename": "[A-Za-z0-9]:[A-Za-z0-9]"
		}
		

	def convert_to_ast(self, string):
		self.lexeme_list = self.to_lexeme(string)
		self.lc = self.lexeme_list[0]
		self.t = self.expression()
		if(self.lexeme_list.index(self.lc) != len(self.lexeme_list)-1):
			raise BadSyntaxError("ERROR SYNTAX")
		return(self.t)


	# Convertis une chaîne de caractère en Lexeme, càd elle fragmente la chaîne en unité de langage
	def to_lexeme(self, expr):
		i = 0
		lexeme_list = list()
		while (i < len(expr)):
			x = expr[i]

			if(x.isspace()):
				i += 1
				continue

			if(x == self.prefix):
				j = i+1
				if(j == len(expr)):
					raise UnknowCommand("UNKNOW COMMAND")
				while(expr[j].isalpha()):
					if(j == len(expr)-1):
						j += 1
						break
					j += 1
				command = expr[i+1:j]
				if(command in ["select", "rename", "project"]):
					lexeme_list.append(Lexeme("modify", command))
				elif(command in ["join", "union", "minus"]):
					lexeme_list.append(Lexeme("link", command))
				else:
					raise UnknowCommand(f"ERROR : UNKNOW COMMAND \"{self.lc.nature}\"")
				i = j-1

			if(x.isalpha()):
				j = i
				while(expr[j].isalpha()):
					if(j == len(expr)-1):
						j += 1
						break
					j += 1
				lexeme_list.append(Lexeme("str", expr[i:j]))
				i = j-1
			
			if(x == "{"):
				j = i+1
				while(expr[j] != "}"):
					if(j == len(expr)-1):
						j += 1
						break
					j += 1
				lexeme_list.append(Lexeme("condition", expr[i+1:j]))
				i = j

			if(x in ["(", ")"]):
				lexeme_list.append(Lexeme(x))

			i += 1
		lexeme_list.append(Lexeme("EOL"))
		return lexeme_list

	# truc compliqué à expliquer
	def expression(self):
		t = self.facteur()
		if(self.lc.nature not in [")", "link", "EOL"]):
			raise Exception("ERROR : INVALID SYNTAX")
		while(self.lc.nature == "link"): #JOIN UNION MINUS
			nature = self.lc.value
			self.next()
			r = self.facteur()

			t = Terme(nature, t, r)
		return t

	# truc compliqué à expliquer bis
	def facteur(self):
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
			case "modify": 				#select,rename,project
				nature = self.lc.value
				self.next()
				condition = self.facteur()
				if(not re.search(self.regex.get(nature), condition.a1)):
					raise BadSyntaxError(f"ERROR : WRONG CONDITION SYNTAX \"{{{condition.a1}}}\"")
				table = self.facteur()
				print(table.nature)
				if(table.nature != "table" or table.nature in ["select", "rename", "project", "join", "union", "minus"]):
					raise BadSyntaxError(f"ERROR : MISSING TABLE OR EXPRESSION")
				return Terme(nature, condition,table )
			case "EOL":
				return None
			case _:
				raise UnknowCommand(f"ERROR : UNKNOW COMMAND \"{self.lc.nature}\"")
		self.next()
		return t

	# passe au lexeme suivant
	def next(self):
		if(self.lexeme_list.index(self.lc)+1 != len(self.lexeme_list)):
			self.lc = self.lexeme_list[self.lexeme_list.index(self.lc)+1]

	def __str__(self):
		return self.sql

if __name__ == "__main__":
	sql = SQL()
	print(type(sql.convert_to_ast("@project[{Population}A")))
	print(sql.convert_to_ast("@project[{Population}A"))
	string="@project[{Population}A"
	a=sql.to_lexeme(string)
	#for i in range(len(a)):
		#print(a[i].Terme())
	while True:
		x = input("SPJRUD >>")
		if(x == "@exit"):
			break
		try:
			print(sql.convert_to_ast(x))
		except Exception as e:
			print("\033[93m" + str(e) + "\033[0m")


	# SQL("select{Test=\"Adrien\"} @select{Test=\"Adrien\"} A")
	#SQL("@project{Population} ((@rename{Name:Capital} Cities) @join (@select{Country=\"Mali\"} CC))")
	# SQL("A @join B @join C")
