import sqlite3


# SPJRUD
# Formatte une condition pour la rendre "acceptaple en sql" : Rajoute des ' autour des string, Prend en paramètre un element de [">=","<=","<",">","="]
class SQL:

    def __init__(self, DbFileName=0):
        self.dbFileName = DbFileName
        self.alias_number = 0
    def formatCondition(self, condition):
        condition = condition.replace(" ", "")
        allowedCondition = [">=", "<=", ">", "<", "="]
        for operator in allowedCondition:
            if operator in condition:
                left = condition[:condition.index(operator)]
                right = condition[condition.index(operator) + 1:]
                op = operator
                break;
        if left.isalpha():
            left = '"' + left + '"'
        if right.isalpha():
            right = '"' + right + '"'
        newCondition = left + op + right
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
    # (tu devrais pas utiliser ça ? https://stackoverflow.com/questions/614238/how-can-i-rename-a-single-column-in-a-table-at-select)
    def rConvert(self, oldName, newName, RName):
        columns_name = ",".join(self.getDbKeys( RName)).replace(oldName, f"{oldName} AS {newName}")
        sqlStr = f"(SELECT {columns_name} FROM {RName} {self.getAlias()})"
        return sqlStr

        # sqlStr="SELECT "
        # sqlStr+=",".join(getDbKeys(dbFileName,RName))
        # sqlStr = sqlStr.replace(oldName,newName)
        # sqlStr += " FROM "+RName.upper()
        # return sqlStr

    # Convertisseur pour l'opérateur UNION
    def uConvert(self, RName1, RName2):
        if self.checkSameAtribute(RName1, RName2):
            sqlStr = f"(SELECT * FROM {RName1}) UNION  (SELECT * FROM {RName2}) "
            return sqlStr

            # Erreur à envoyer

    # Convertisseur pour l'opérateur DIFFERENCE
    def dConvert(self, RName1, RName2):
        if self.checkSameAtribute(RName1, RName2):
            sqlStr = f"(SELECT * FROM {RName1}) MINUS (SELECT * FROM {RName2})"
            return sqlStr
        else:
            pass
            # Erreur à envoyer

    # Récupère toutes les attributs/Clés d'une table
    def getDbKeys(self, RName):
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

    def printTable(self,Rname, dbFileName="test.db"):
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
        self.printLine(names, column_lenght)
        print("|".join(["—"*(x+2) for x in column_lenght]))
        for row in table.fetchall():
            self.printLine(row, column_lenght)

    def printLine(self,row, lenght):
        line = list()
        for i in range(len(row)):
            col = row[i]
            x = f"{col:<{lenght[i]}}"
            line.append(f"{x:^{lenght[i]+2}}")
        line = "|".join(line)
        print(line)

    def createTable(self,tableName, sqlRequest):
        con = sqlite3.connect(f"{self.dbFileName}.db")
        con.execute(f"CREATE TABLE {tableName} AS SELECT * FROM {sqlRequest} temp")
        con.close()

    def getAlias(self):
        self.alias_number += 1
        return f"table{self.alias_number}"

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
