import Error
import numpy as np

class Table:

	def __init__(self, names, values):
		if(len(names) == len(values[0])):
			self.names = names
			self.values = values
		else:
			raise Error.SizeError()


	def print(self):
		array = self.values
		array.insert(0, self.names)
		array = np.array(array)
		print(array.reshape(len(array), len(self.names)))


if __name__ == "__main__":
	t = Table(
		["Id", "Name"],
		[
			[1, "Adrien"],
			[2, "Kiefer"],
			[123, "Jean-Patrick-Hugue"]
		]
		)
	t.print()