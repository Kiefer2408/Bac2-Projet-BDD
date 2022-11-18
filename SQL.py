import sqlite3
import Formatter

alias_number = 0

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
    # TODO vérifier avec isalpha() si Rname est une table ou une sous requête pour éviter de mettre l'alias h24
    return f"(SELECT * from {RName} {getAlias()} where {formatCondition(condition)})"

#Convertisseur pour l'opérateur PROJECT
def pConvert(argument,RName):
    sqlStr = f"(SELECT DISTINCT {getAlias()} from {RName} {getAlias()})"
    return sqlStr

#Convertisseur pour l'opérateur JOIN
def jConvert(RName1,RName2):
    sqlStr = f"(SELECT * FROM {RName1} {getAlias()} NATURAL JOIN {RName2} {getAlias()})"
    return sqlStr

#Convertisseur pour l'opérateur RENAME
# (tu devrais pas utiliser ça ? https://stackoverflow.com/questions/614238/how-can-i-rename-a-single-column-in-a-table-at-select)
def rConvert(oldName,newName,dbFileName,RName):
    columns_name = ",".join(getDbKeys(dbFileName,RName)).replace(oldName, f"{oldName} AS {newName}")
    sqlStr = f"(SELECT {columns_name} FROM {RName} {getAlias()})"
    return sqlStr

#Convertisseur pour l'opérateur UNION
def uConvert(RName1,RName2,dbFileName):
    if checkSameAtribute(RName1,RName2,dbFileName):
        sqlStr="SELECT * FROM "+RName1
        sqlStr+=" UNION "
        sqlStr+= "SELECT * FROM "+RName2
        return sqlStr
    else:
        pass
        #Erreur à envoyer
#Convertisseur pour l'opérateur DIFFERENCE
def dConvert(RName1,RName2,dbFileName):
    if checkSameAtribute(RName1,RName2,dbFileName):
        sqlStr="SELECT * FROM "+RName1
        sqlStr+=" MINUS "
        sqlStr+= "SELECT * FROM "+RName2
        return sqlStr
    else:
        pass
        #Erreur à envoyer

#Récupère toutes les attributs/Clés d'une table
def getDbKeys(dbFileName, RName):
    con=sqlite3.connect(dbFileName)
    con.row_factory = sqlite3.Row
    attributeName=con.execute("SELECT * FROM "+RName.upper())
    line = attributeName.fetchone()
    attributes=line.keys()
    con.close()
    return attributes

#Verifie si tous les attribus sont les mêmes dans 2 tables
def checkSameAtribute(RName1,RName2,dbFileName):
    keys1=getDbKeys(dbFileName,RName1)
    keys2=getDbKeys(dbFileName,RName2)

    validity=True
    for attr in keys1:
        if attr not in keys2:
            validity=False
    for attr in keys2:
        if attr not in keys1:
            validity=False
    return validity

def createTable(sql, dbFileName="test.db"):
    con=sqlite3.connect(dbFileName)
    con.execute(f"CREATE TABLE new_table AS SELECT * FROM {sql} temp")
    con.close()

def getAlias():
    global alias_number
    alias_number += 1
    return f"table{alias_number}"

def to_sql(terme):
    db = "test.db"
    sql = None
    match terme.nature:
        case "table":
            sql = terme.a
        case "select":
            sql = sConvert(terme.a.a, to_sql(terme.b))
        case "rename":
            old, new = terme.a.a.split(":")
            sql = rConvert(old, new, db, to_sql(terme.b))
        case "project":
            sql = pConvert(terme.a.a, to_sql(terme.b))
        case "join":
            sql = jConvert(to_sql(terme.a), to_sql(terme.b))
        case "minus":
            sql = mConvert(to_sql(terme.a), to_sql(terme.b), db)
        case "union":
            sql = uConvert(to_sql(terme.a), to_sql(terme.b), db)
    return sql

def printTable(Rname, dbFileName="test.db"):
    con=sqlite3.connect(dbFileName)
    cursor=con.execute(f"SELECT * FROM {Rname}")
    names = list(map(lambda x: x[0], cursor.description))
    column_lenght = list()
    for col in names:
        longest = len(col)
        test = con.execute(f"SELECT {col} FROM {Rname}")
        for val in test.fetchall():
            lenght = len(str(val[0]))
            if lenght > longest:
                longest = lenght
        column_lenght.append(longest)
    table = con.execute(f"SELECT * FROM {Rname}")

    line = list()
    printLine(names, column_lenght)
    print("|".join(["—"*(x+2) for x in column_lenght]))
    for row in table.fetchall():
        printLine(row, column_lenght)

def printLine(row, lenght):
    line = list()
    for i in range(len(row)):
        col = row[i]
        x = f"{col:<{lenght[i]}}"
        line.append(f"{x:^{lenght[i]+2}}")
    line = "|".join(line)
    print(line)

if __name__ == "__main__":
    sql=SQL.SQL()
    printTable("A")
