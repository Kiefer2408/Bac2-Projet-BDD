string = input()
stack = 0
for i in range(len(string)):
	x = string[i]
	if(x == "("):
		stack+=1
	elif(x == ")"):
		stack-=1
	if(stack < 0):
		# lance une erreur : parenthèse fermante sans ouvrante
		pass
	elif(stack == 0):
		print(string[1:i])
		break
if(stack > 0):
	#lance une erreur : parenthèse fermante manquante