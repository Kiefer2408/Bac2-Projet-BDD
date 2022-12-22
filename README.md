# Bac2-Projet-BDD

Le projet de base de donnée de l'année 2022-2023 consiste à la création d'un outils de compilation (traduction) de requête SPJRUD vers des requêtes SQL.

## Usage

Les commandes SPJRUD doivent être précédée du préfixe `@` (ex. @join, @select,...). 
Sans parenthèses, le traitement des commandes est left-associative (c'est-à-dire `A @join B @join C` équivaut à `(A @join B) @join c` et non `A @join (B @join c)`)
```
SPJRUD >> @select{A=1} A
[select: [condition: A=1] [table: A]]
 A | B 
———|———
 1 | 2 
 1 | 3 
SPJRUD >> Table1 @join Table2
[join: [table: Table1] [table: Table2]]
 A1 | B12 | A2
————|—————|————
 1  | 2   | 7
 4  | 3   | 9
```
## Example
### Select
````
SPJRUD >> @select{SALARY>20000} COMPANY 
(SELECT * from COMPANY where "SALARY">20000)
```` 
### Project
````
SPJRUD >> @project{ID,NAME,AGE} COMPANY
(SELECT DISTINCT ID,NAME,AGE from COMPANY table4)
````
### Join
````
SPJRUD >> COMPANY @join EMPLOYEE
(SELECT * FROM COMPANY table2 NATURAL JOIN EMPLOYEE table3)
````
### Rename
````
SPJRUD >> @rename{SALARY:SAL}COMPANY)
(SELECT ID,NAME,AGE,ADDRESS,SALARY AS SAL FROM COMPANY table1)
````
### Union 
````
SPJRUD >> COMPANY @union EMPLOYEE

````
### Difference
````
SPJRUD >> @project{salary}COMPANY) @minus (@project{salary}(@select{salary>20000}COMPANY)
(SELECT * FROM (SELECT DISTINCT salary from COMPANY table1)) MINUS (SELECT * FROM (SELECT DISTINCT salary from (SELECT * from COMPANY where "salary">20000) table2))
````
## Choix d'implémentation

La traduction de la requête SPJRUD commence d'abord par l'analyse syntaxique de celle-ci. Pour cela, le programme extrait une liste de [lexèmes](https://fr.wikipedia.org/wiki/Lex%C3%A8me) dans la chaîne de caractères de la requêtes, puis crée un arbre de syntaxe abstraite en parcourant récursivement la liste des lexèmes.

Soit $$A = \{modify , link , ( , ) , table\}, V_n = \{E, F\}, \text{l'axiome est E}$$
Les règles sont :

[insérer ici l'image]


## Difficulté et solution
Une difficulté a été de faire les 

## Fonctionnalité supplémentaire
Notre projet présente quelque fonctionnalité supplémentaires :

Choix de base de données : l'utilisateur peut, à tout moment pendant que le programme est lancé, modifier la base de donnée que celui-ci utilise.
```bash
@use [db-name]
Database Found

@use [incorrect-db-name]
Database Not Found


```
-
