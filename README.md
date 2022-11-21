# Bac2-Projet-BDD

## Organisation

Pour ce projet de BDD, nous avons décidé de se diviser la tâche en 2 : Adrien s'est occupé de la conversion de la chaîne de caractères en AST (Abstract Syntax Tree) tandis que Kiefer s'est occupé de la traduction de cet arbre en commande SQL compatible avec SQLite3

## Implémentation

La conversion de la chaîne de caractère en ast se fait en 2 étapes : 
Tout d'abord une itération sur la chaîne est executée pour la découper en Lexeme et se débarrasser des caractères inutile et/ou redondants (ex. les espaces). Ces lexemes sont divisé entre plusieurs types :
	`str` : représente une chaîne de caractère
	`condition` : représente la condition d'une commande
	`link` : représente les commandes qui prennent en paramètre 2 expression
	`modify` : représente les commandes qui prennent en paramètre qu'une expression et possède une condition
	`(` et `)` : délimite une sous expression

Ensuite une fois la liste de Lexeme crée, une itération récursive s'occupe de créer les noeuds de l'AST tout en restant left-associative (1 + 1 + 1 devient (1 + 1) + 1). Les noeuds sont représenter par la classe Terme, qui possède une nature :
	`select`, `project`, `rename` sont des commandes qui prennent comme attribut une condition et une sous-expression/table
	`join`, `union`, `minus` sont des commandes prennent comme attribut 2 sous-expression/table
	`condition` a pour unique attribut une condition
	`table` a pour unique attribut le nom d'une table

La conversion de l'AST en commande SQL se fait via une récursive qui part de l'axiome de l'arbre 

## Fonctionnalité

## Difficulté rencontrée


## Usage

```bash
SPJRUD >> @select{Name = "John"} Table
SELECT 
SPJRUD >> Table1 @join Table2
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)