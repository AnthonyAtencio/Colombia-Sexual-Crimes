# Analysis on sexual crimes in Colombia 

In this project I analyze the database of sexual crimes in Colombia in the years between 2010 and 2020. This database was provided by  [DIJIN - National Police(Data extracted on June 14, 2021 at 18:00)](https://www.datos.gov.co/Seguridad-y-Defensa/Reporte-Delitos-sexuales-Polic-a-Nacional/fpe5-yrmw) 



First the data is partially cleaned and prepared in SQL([link to query script](https://github.com/AnthonyAtencioM/Colombia-Sex-Crimes/blob/main/SQL/SQL%20-%20Cleaning%20Data.sql)). The database is exported and worked on Python where libraries as pandas, matplotlib and seaborn are used to make an Exploratory Data Analysis and take a better understanding on the state of sexual crimes in the country.



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
