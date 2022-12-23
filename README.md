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
 1 | 2 | 7
 4 | 3 | 9
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

La traduction de la requête SPJRUD commence d'abord par l'analyse syntaxique de celle-ci. Pour cela, le programme convertis tout d'abord la chaîne de caractères de la requêtes en une liste de [lexèmes](https://fr.wikipedia.org/wiki/Lex%C3%A8me) grâce à une boucle itérative et la classe `Lexeme`.

La classe `Lexeme` possède obligatoirement une nature et optionnellement une valeur et une position dans la chaîne de caractère. Les différentes nature de celle-ci sont
- `modify`, qui représente les commandes ne prennant qu'une table ou sous-expression et une condition/instruction en paramètre (select, project et rename)
- `link`, qui représente les commandes prennant 2 table ou sous-expression en paramètre (join, union et minus)
- `str`, qui représente les noms des tables
- `(` et `)`, qui représente les parenthèses ouvrantes et fermantes
- `condition`, qui représente la condition/instruction d'une commande `modify`
- `EOL`, qui représente la fin de la requête

Une fois la liste de lexèmes créée sans erreur, une seconde partie du programme s'occupe de créer l'arbre de syntaxe abstraite récursivement en parcourant celle-ci.

Si aucune erreur de syntaxe n'est repérée, la méthode renvoie un objet `Terme` qui contient lui-même des d'autres `Terme` ou une chaîne de caractère représentant une commande, une condition ou le nom d'une table.

Soit $$A = \{modify , link , ( , ) , table\}, V_n = \{E, F\}, \text{l'axiome est E}$$
Les règles sont :

[insérer ici l'image]

## Difficulté et solution
- Lors de la création de la récursive servant à produire l'arbre syntaxique abstrait, les relations de type `modify` se réalisait en right-associative, c'est à dire que l'ordre des opérations se faisait de droite à gauche (`A @join B @join C` était interprété comme `A @join (B @join C`). 
Pour résourdre ce problème, il a fallu rajouter un accumulateur pour traiter directement la première opération `modify` et l'utiliser dans les suivantes. Toutefois l'ajout de cet accumulateur a forcé l'ajout d'un nouveau lexème afin d'éviter que le programme s'arrête prématurément : `EOL`. Celui-ci indique la fin de la requête (End-Of-Line), et empêche l'arrêt de la boucle avant d'atteindre ce lexème.


## Fonctionnalité supplémentaire
Notre projet présente quelque fonctionnalité supplémentaires :

Choix de base de données : l'utilisateur peut, à tout moment pendant que le programme est lancé, modifier la base de donnée que celui-ci utilise.
```bash
@use [db-name]
Database Found

@use [incorrect-db-name]
Database Not Found
```

Nettoyage du terminal,l'utilisateur peut à tout moment nettoyer le terminal en utilisant la commande suivante:
```
@clear
```
Création de table, l'utilisateur peut créer ses propres tables à partir de requêtes SPJRUD via la commande suivante
```
@create [tableName] [SPJRUDRequest]
```
Affichage, l'utilisateur peut afficher une table ou une requête SPJRUD via la commande suivante:
```
@print [tableName]
@print [SPJRUDRequest]
```
Quitter,l'utilisateur peut quitter à tout moment le programme via la commande suivante: 
```
@exit
```
