# SQL project

Here I make use of SQL under the software Microsoft SQL Server Management Studio where [the query](https://github.com/AnthonyAtencioM/Colombia-Sex-Crimes/blob/main/SQL/SQL%20-%20Cleaning%20Data.sql) was made as well as the import/export of the file before doing the EDA on Python.

In this query I made some cleaning in the dataset to make it easier to work with on python. The database had some inputs that clearly were made by human error like misspellings and missing data. Some columns had redundant categories that could be reduced without risking the loss of information or clarity.



## Variables on the dataset

- DEPARTAMENTO=Department/State where crime took place.
- MUNICIPIO=City/Municipality where crime took place.
- CODIGO.DANE= City/Municipality ID in DANE(National Administrative Department of Statistics, Spanish: Departamento Administrativo Nacional de Estadística)
- ARMAS.MEDIOS= Weapon used.
- FECHA.HECHO= Date of report.
- GENERO= Gender.
- GRUPO.ETARIO= Age group.
- CANTIDAD= Amount of criminals involved.
- DELITO= Official crime category by law.

