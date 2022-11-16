import sqlite3
import SQL
#SPJRUD
#Formatte une condition pour la rendre "acceptaple en sql" : Rajoute des ' autour des string, Prend en paramètre un element de [">=","<=","<",">","="]
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

#Convertisseur pour l'opérateur SELECT
def sConvert(condition,RName):
    return "SELECT * from "+RName+" where "+formatCondition(condition)

#Convertisseur pour l'opérateur PROJECT
def pConvert(argument,RName):
    print(argument,RName)
    sqlStr = "SELECT DISTINCT "

    #sqlStr += ",".join(argument)
    sqlStr += argument
    sqlStr +=" from "
    sqlStr += RName

    return sqlStr
#Convertisseur pour l'opérateur JOIN
def jconvert(RName1,RName2):
    sqlStr="SELECT * FROM "
    sqlStr+=RName1
    sqlStr+=" NATURAL JOIN "
    sqlStr+=RName2
    return sqlStr

#Convertisseur pour l'opérateur RENAME
def rConvert(oldName,newName,dbFileName,RName):


    sqlStr="SELECT "
    sqlStr+=",".join(getDbKeys(dbFileName,RName))
    sqlStr = sqlStr.replace(oldName,newName)
    sqlStr += " FROM "+RName.upper()
    return sqlStr

#Convertisseur pour l'opérateur UNION
def uConvert(RName1,RName2,dbFileName1):
    if checkSameAtribute(RName1,RName2,dbFileName1):
        sqlStr="SELECT * FROM "+RName1
        sqlStr+=" UNION "
        sqlStr+= "SELECT * FROM "+RName2
        return sqlStr
    else:
        pass
        #Erreur à envoyer
#Convertisseur pour l'opérateur DIFFERENCE
def dConvert(RName1,RName2,dbFileName1):
    if checkSameAtribute(RName1,RName2,dbFileName1):
        sqlStr="SELECT * FROM "+RName1
        sqlStr+=" MINUS "
        sqlStr+= "SELECT * FROM "+RName2
        return sqlStr
    else:
        pass
        #Erreur à envoyer

#Récupère toutes les attributs/Clés d'une table
def getDbKeys(dbFileName,RName):
    con=sqlite3.connect(dbFileName)
    con.row_factory = sqlite3.Row
    attributeName=con.execute("SELECT * FROM "+RName.upper())
    line = attributeName.fetchone()
    attributes=line.keys()
    con.close()
    return attributes

#Verifie si tous les attribus sont les mêmes dans 2 tables
def checkSameAtribute(RName1,RName2,dbFileName1):
    keys1=getDbKeys(dbFileName1,RName1)
    keys2=getDbKeys(dbFileName1,RName2)

    validity=True
    for attr in keys1:
        if attr not in keys2:
            validity=False
    for attr in keys2:
        if attr not in keys1:
            validity=False
    return validity

def termeTraductor(terme):
    if(terme.a2.nature=="table" and terme.a1.nature in ["select","project","join","rename","union","minus"]):
        return termeToSJPRUD(terme)
    #elif(terme.a2.nature=="table" and terme.a1.nature not in ["select","project","join","rename","union","minus"]):
    else:
        return termeToSJPRUD(termeTraductor(terme.a2))

def termeToSJPRUD(terme):
    value=None
    match terme.nature:
        case "select":
            value=sConvert(terme.a1,terme.a2)
        case "project":
            value=pConvert(terme.a1.a1, terme.a2.a1)
        case "join":
            value=jconvert(terme.a1.a1,terme.a2.a1)
        case "rename":
            value=rConvert(terme.a1.a1,terme.a2.a1)
        case "union":
            value=uConvert(terme.a1.a1,terme.a2.a1)
        case "minus":
            value=dConvert(terme.a1.a1,terme.a2.a1)
    return value

if __name__ == "__main__":
    #print(getDbKeys("test.db","COMPANY"))
    sql=SQL.SQL()
    #print(sql.convert_to_ast("@project{Population}A"))
    print((sql.convert_to_ast("@project{Population} ( Land @join Cities)")))