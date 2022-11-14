# Select,Project,Join,Rename,Union,Difference
import copy
import sqlite3

def select(database,element1=0,operator=0,element2=0):
    if (element1==0 and operator==0 and element2==0):
        return database
    else:


def project(database,element):
    if (len(database) == 0):
        raise IndexError
    newDatabase = [[" " for i in range(len(element))] for j in range(len(database))]
    index2 = 0
    for col in range(len(database[0])):
        if database[0][col] in element:
            index = 0
            for row in range(len(database)):
                newDatabase[index][index2] = database[row][col]
                index += 1
            index2 += 1
    return newDatabase


def rename(database,oldName, newName):
    newDatabase = copy.deepcopy(database)
    for i in range(len(database[0])):
        if newDatabase[0][i] == oldName:
            newDatabase[0][i] = newName
    return newDatabase


A = [["vins", "cru", "Milesime"],
     ["Chabli", "Rosé", "1990"],
     ["Vendome", "rouge", "1970"]]
b = ["vins", "Année"]
A = rename("Milesime", "Année", A)

for i in range(len(A)):
    print(project(b, A)[i])
