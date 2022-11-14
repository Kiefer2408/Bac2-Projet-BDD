import sqlite3
#SPJRUD
'''
conn = sqlite3.connect('test.db')


cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
for row in cursor:
   print ("ID = ", row[0])
   print ("NAME = ", row[1])
   print ("ADDRESS = ", row[2])
   print ("SALARY = ", row[3], "\n")
conn.close()
'''

#Convertisseur pour l'opérateur SELECT
def sConvert(condition,dbName):
    return "SELECT * from "+dbName+" where "+formatCondition(condition)

#Formatte une condition pour la rendre "acceptaple en sql" : Rajoute des ' autour des string
def formatCondition(condition):
    condition=condition.replace(" ","")
    allowedCondition=[">=","<=",">","<","="]
    for operator in allowedCondition:
        if operator in condition:
            left=condition[:condition.index(operator)]
            right=condition[condition.index(operator)+1:]
            op=operator
            break;
    if left.isalpha():
        left="'"+left+"'"
    if right.isalpha():
        right="'"+right+"'"
    newCondition=left+op+right
    return newCondition

#Convertisseur pour l'opérateur PROJECT
def pConvert(argument,dbName):

    sqlStr = "SELECT DISTINCT "

    sqlStr += ",".join(argument)

    sqlStr+=" from "
    sqlStr+=dbName

    return sqlStr
#Convertisseur pour l'opérateur JOIN
def jconvert(dbName1,dbName2,dbFileName1,dbFileName2):
    sqlStr="SELECT * FROM "
    sqlStr+=dbName1
    sqlStr+=" NATURAL JOIN "
    sqlStr+=dbName2
    return sqlStr

#Convertisseur pour l'opérateur RENAME
def rConvert(oldName,newName,dbFileName,dbName):


    sqlStr="SELECT "
    sqlStr+=",".join(getDbKeys(dbFileName,dbName))
    sqlStr = sqlStr.replace(oldName,newName)
    sqlStr += " FROM "+dbName.upper()
    return sqlStr

#Convertisseur pour l'opérateur UNION
def uConvert(dbName1,dbName2,dbFileName1,dbFileName2):
    if checkSameAtribute(dbName1,dbName2,dbFileName1,dbFileName2):
        sqlStr="SELECT * FROM "+dbName1
        sqlStr+=" UNION "
        sqlStr+= "SELECT * FROM "+dbName2
        return sqlStr
    else:
        pass
        #Erreur à envoyer
#Convertisseur pour l'opérateur DIFFERENCE
def dConvert(dbName1,dbName2,dbFileName1,dbFileName2):
    if checkSameAtribute(dbName1,dbName2,dbFileName1,dbFileName2):
        sqlStr="SELECT * FROM "+dbName1
        sqlStr+=" MINUS "
        sqlStr+= "SELECT * FROM "+dbName2
        return sqlStr
    else:
        pass
        #Erreur à envoyer

#Récupère toutes les attributs/Clés d'une table
def getDbKeys(dbFileName,dbName):
    con=sqlite3.connect(dbFileName)
    con.row_factory = sqlite3.Row
    attributeName=con.execute("SELECT * FROM "+dbName.upper())
    line = attributeName.fetchone()
    attributes=line.keys()
    con.close()
    return attributes

#Verifie si tous les attribus sont les mêmes dans 2 tables
def checkSameAtribute(dbName1,dbName2,dbFileName1,dbFileName2):
    keys1=getDbKeys(dbFileName1,dbName1)
    keys2=getDbKeys(dbFileName2,dbName2)

    validity=True
    for attr in keys1:
        if attr not in keys2:
            validity=False
    for attr in keys2:
        if attr not in keys1:
            validity=False
    return validity

def getUserInput():
    userInput=input("Entrez votre commande SJRUD : \n")

    #Check la validité


    #Traitement de l'input



def operatorValidity(string):

    operatorList=["SELECT",
                  "PROJECT",
                  "JOIN",
                  "RENAME",
                  "UNION",
                  "DIFFERENCE"]
    for op in operatorList:
        if op in string:
            return True
    return False

def treatInput(string):
    if not operatorValidity(string):
        pass

print(getDbKeys("test.db","COMPANY"))
