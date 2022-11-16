from SQL import *
from Error import *

class Test:

	def __init__(self):
		self.sql = SQL()

	def run_test(self, input_string, expected_output):
		try:
			output = self.sql.convert_to_ast(input_string)
			if(str(output) == str(expected_output)):
				self.print_passed(input_string)
			else:
				self.print_failed(input_string, output, expected_output)

		except Exception as e:
			if(type(e) == type(expected_output)):
				self.print_passed(input_string)
			else:
				self.print_failed(input_string, type(e), type(expected_output))
				print(e)
		

	def print_failed(self, input_string, output, expected_output):
		print(f"\033[91m \"{input_string}\" : Test failed, got {output}, expected {expected_output} \033[0m")

	def print_passed(self, input_string):
		print(f"\033[92m \"{input_string}\" : Test passed \033[0m")


if __name__ == "__main__":
	test = Test()
	test.run_test("", None)
	test.run_test("@", UnknowCommand())
	test.run_test("@s", UnknowCommand())
	test.run_test("@select", BadSyntaxError())
	test.run_test("select", BadNameError())
	test.run_test("table", "[table: table]")
	test.run_test("@select{A=\"A\"}", MissingExprError())
	test.run_test("@select{A=\"A\"} A", "[select: [condition: A=\"A\"] [table: A]]")
	test.run_test("@select{\"A\"=\"A\"} A", WrongConditionSyntax())
	test.run_test("(", "[select: [condition: A=\"A\"] [table: A]]")
	test.run_test("()", BadSyntaxError(²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²²))
