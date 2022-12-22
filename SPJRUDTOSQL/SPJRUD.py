import sqlite3
import os
from SPJRUDTOSQL import Error
from SPJRUDTOSQL import Formatter
# SPJRUD
# Formatte une condition pour la rendre "acceptaple en sql" : Rajoute des ' autour des string, Prend en paramètre un element de [">=","<=","<",">","="]
class SPJRUD:

    def __init__(self, DbFileName=None):
        self.dbFileName = DbFileName
        self.alias_number = 0

    #vérifie si il y a une chaine de caractère dans la condition si oui : rajoute des guillemets autour de la chaine EMPLOYÉE>2 -> "EMPLOYE">2
    def formatCondition(self, condition):
        condition = condition.replace(" ", "")
        allowedCondition = [">=", "<=", ">", "<", "="]
        for operator in allowedCondition:
            if operator in condition:
                left, right = condition.split(operator)
                op = operator
                break;
        if left.isalpha():

            left = f'"{left}"'
        if right.isalpha():
            right = f'"{right}"'
        newCondition = f"{left}{op}{right}"

        return newCondition

    # Convertisseur pour l'opérateur SELECT
    def sConvert(self, condition, RName):
        if (RName.isalpha()):
            return f"(SELECT * from {RName} where {self.formatCondition(condition)})"
        return f"(SELECT * from {RName} {self.getAlias()} where {self.formatCondition(condition)})"

    # Convertisseur pour l'opérateur PROJECT
    def pConvert(self, argument, RName):
        sqlStr = f"(SELECT DISTINCT {argument} from {RName} {self.getAlias()})"
        return sqlStr

    # Convertisseur pour l'opérateur JOIN
    def jConvert(self, RName1, RName2):
        sqlStr = f"(SELECT * FROM {RName1} {self.getAlias()} NATURAL JOIN {RName2} {self.getAlias()})"
        return sqlStr

    # Convertisseur pour l'opérateur RENAME
    def rConvert(self, oldName, newName, RName):
        if(oldName not in self.getDbKeys(RName)):
            raise Error.WrongNameException

        columns_name = ",".join(self.getDbKeys( RName)).replace(oldName, f"{oldName} AS {newName}")
        sqlStr = f"(SELECT {columns_name} FROM {RName} {self.getAlias()})"
        return sqlStr

    # Convertisseur pour l'opérateur UNION
    def uConvert(self, RName1, RName2):
        if self.checkSameAtribute(RName1, RName2):
            sqlStr = f"(SELECT * FROM {RName1} UNION SELECT * FROM {RName2})"
            return sqlStr
        else:
            raise Error.NotSameAttribute("UNION")

    # Convertisseur pour l'opérateur DIFFERENCE
    def dConvert(self, RName1, RName2):
        if self.checkSameAtribute(RName1, RName2):
            sqlStr = f"(SELECT * FROM {RName1} MINUS SELECT * FROM {RName2})"
            return sqlStr
        else:
            raise Error.NotSameAttribute("DIFFERNCE/MINUS")

    # Récupère toutes les attributs/Clés d'une table
    def getDbKeys(self, RName):
        if(self.checkDbValidity()):
            con = sqlite3.connect(f"{self.dbFileName}.db")
            con.row_factory = sqlite3.Row
            attributeName = con.execute("SELECT * FROM " + RName.upper())
            line = attributeName.fetchone()
            attributes = line.keys()
            con.close()
            return attributes


    # Verifie si tous les attribus sont les mêmes dans 2 tables
    def checkSameAtribute(self, RName1, RName2):
        keys1 = self.getDbKeys(RName1)
        keys2 = self.getDbKeys(RName2)
        validity = True
        for attr in keys1:
            if attr not in keys2:
                validity = False
        for attr in keys2:
            if attr not in keys1:
                validity = False
        return validity

    #Affiche la relation Rname sous forme de tableau
    def printTable(self,Rname):
        self.checkDbValidity()
        try:
            conn=sqlite3.connect(f"{self.dbFileName}.db")
            cursor=conn.cursor()
            print(f"SELECT * FROM {Rname} {self.getAlias()}")
            request=cursor.execute(f"SELECT * FROM {Rname} {self.getAlias()}")
            names = list(map(lambda x: x[0], request.description))
            column_lenght = list()
            for col in names:
                longest = len(col)
                test = cursor.execute(f"SELECT {col} FROM {Rname} {self.getAlias()}")
                for val in test.fetchall():
                    lenght = len(str(val[0]))
                    if lenght > longest:
                        longest = lenght
                column_lenght.append(longest)
            table = cursor.execute(f"SELECT * FROM {Rname} {self.getAlias()}")

            line = list()
            self.printLine(names, column_lenght)
            print("|".join(["—"*(x+2) for x in column_lenght]))
            for row in table.fetchall():
                self.printLine(row, column_lenght)
            print("\n")
            cursor.close()
        except sqlite3.OperationalError:
            raise Error.NoDatabaseException()


    #Affiche une ligne row, de la relation, de longueur lenght
    def printLine(self,row, lenght):
        line = list()
        for i in range(len(row)):
            col = row[i]
            x = f"{col:<{lenght[i]}}"
            line.append(f"{x:^{lenght[i]+2}}")
        line = "|".join(line)
        print(line)

    #Crée une table à partir d'une requete sql
    def createTable(self,tableName, sqlRequest):
        self.checkDbValidity()
        con = sqlite3.connect(f"{self.dbFileName}.db")
        con.execute(f"CREATE TABLE {tableName} AS SELECT * FROM {sqlRequest} temp")
        con.close()

    #Retourne le string table en incrémentant à chaque appel : permet de creer des alias de table afin d'utiliser des sous requêtes
    def getAlias(self):
        self.alias_number += 1
        return f"table{self.alias_number}"

    #Fonction récusive traduisant un terme en sql
    def to_sql(self, terme):
        sql = None
        match terme.nature:
            case "table":
                sql = terme.a
            case "select":
                sql = self.sConvert(terme.a.a, self.to_sql(terme.b))
            case "rename":
                old, new = terme.a.a.split(":")
                sql = self.rConvert(old, new, self.to_sql(terme.b))
            case "project":
                sql = self.pConvert(terme.a.a, self.to_sql(terme.b))
            case "join":
                sql = self.jConvert(self.to_sql(terme.a), self.to_sql(terme.b))
            case "minus":
                sql = self.dConvert(self.to_sql(terme.a), self.to_sql(terme.b))
            case "union":
                sql = self.uConvert(self.to_sql(terme.a), self.to_sql(terme.b))
        return sql
    def sqlTraductor(self,string):
        formatter = Formatter.Formatter()
        return self.to_sql(formatter.convert_to_ast(string))


    #Vérifie si la base de donnée existe dans le répétoire renvoie une erreur si non
    def checkDbValidity(self):
        if(self.dbFileName==0):
            raise Error.NoDatabaseException()
        elif(os.path.exists(f'{self.dbFileName}.db')):
            return True
        else:
            raise Error.WrongDatabaseFileName()

