import sqlite3
import SQL0
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
        left='"'+left+'"'
    if right.isalpha():
        right='"'+right+'"'
    newCondition=left+op+right
    return newCondition

#Convertisseur pour l'opérateur SELECT
def sConvert(condition,RName):
    return "SELECT * from "+RName+" where "+formatCondition(condition)

#Convertisseur pour l'opérateur PROJECT
def pConvert(argument,RName):
    sqlStr = "SELECT DISTINCT "
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
    if(terme.b.nature=="table"):
        return termeToSJPRUD(terme)
    else:
        t=SQL.Terme(terme.nature,terme.a,termeTraductor(terme.b))
        return termeToSJPRUD(t)

def termeToSJPRUD(terme):
    value=None
    if(type(terme.b)==str):
        b=terme.b
    else:
        b=terme.b.a

    match terme.nature:
        case "select":
            value=sConvert(terme.a.a,terme.b.a)
        case "project":
            value=pConvert(terme.a.a, b)
        case "join":
            value=jconvert(terme.a.a,terme.b.a)
        case "rename":
            value=rConvert(terme.a.a,terme.b.a)
        case "union":
            value=uConvert(terme.a.a,terme.b.a)
        case "minus":
            value=dConvert(terme.a.a,terme.b.a)
    return value

if __name__ == "__main__":
    #print(getDbKeys("test.db","COMPANY"))
    sql=SQL.SQL()

    #print(termeTraductor(sql.convert_to_ast("@project{Population} Cities")))
    #print(termeTraductor(sql.convert_to_ast("@project{Population} (@select{A=\"city\"} Cities)")))
    print(termeTraductor(sql.convert_to_ast("@project{Population} ( Cities @minus Cities)")))