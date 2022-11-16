from Error import WrongConditionSyntax

class Relation:
	pass

class SPR(Relation):
	def __init__(self, condition, expr):
		self.condition = condition;
		self.expr = expr

class JRU(Relation):
	def __init__(self, expr1, expr2):
		self.expr1 = expr1
		self.expr2 = expr2


class Select(SPR):
	def __init__(self, condition, expr):
		if(not re.search("[A-Za-z0-9]+ *(=|<=|>=|<|>){1} *(\"[A-Za-z0-9]+\"|[0-9]+){1}", condition)):
			raise WrongConditionSyntax()
		super().__init__(condition, expr)


class Project(SPR):
	def __init__(self, condition, expr):
		if(not re.search("[A-Za-z0-9]+(, *[A-Za-z0-9]+)*", condition)):
			raise WrongConditionSyntax()
		super().__init__(condition, expr)


class Rename(SPR):
	def __init__(self, condition, expr):
		if(not re.search("[A-Za-z0-9]:[A-Za-z0-9]", condition)):
			raise WrongConditionSyntax()
		super().__init__(condition, expr)


class Join(JRU):
	def __init__(self):
		pass


class Minus(JRU):
	def __init__(self):
		pass


class Union(JRU):
	def __init__(self):
		pass