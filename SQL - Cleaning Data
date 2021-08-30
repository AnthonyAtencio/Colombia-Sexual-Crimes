-- ## Cleaning data in SQL for database [Delitos_sexuales_policia_nacional]


select top(5)*
from Cleaning_Project..Delitos_sexuales_policia_nacional

-- +--------------+---------------+-------------+---------------------+-------------------------+-----------+--------------+----------+----------------------------------------------------------+
-- | DEPARTAMENTO |   MUNICIPIO   | CODIGO DANE |    ARMAS MEDIOS     |       FECHA HECHO       |  GENERO   | GRUPO ETARIO | CANTIDAD |                          DELITO                          |
-- +--------------+---------------+-------------+---------------------+-------------------------+-----------+--------------+----------+----------------------------------------------------------+
-- | ANTIOQUIA    | SONSON        |     5756000 | SIN EMPLEO DE ARMAS | 2016-05-19 00:00:00.000 | FEMENINO  | MENORES      |        1 | ARTÍCULO 209. ACTOS SEXUALES CON MENOR DE 14 AÑOS        |
-- | META         | PUERTO GAITÁN |    50568000 | SIN EMPLEO DE ARMAS | 2016-05-19 00:00:00.000 | FEMENINO  | MENORES      |        1 | ARTÍCULO 209. ACTOS SEXUALES CON MENOR DE 14 AÑOS        |
-- | VALLE        | BUENAVENTURA  |    76109000 | SIN EMPLEO DE ARMAS | 2016-05-19 00:00:00.000 | FEMENINO  | MENORES      |        1 | ARTÍCULO 208. ACCESO CARNAL ABUSIVO CON MENOR DE 14 AÑOS |
-- | CESAR        | BOSCONIA      |    20060000 | SIN EMPLEO DE ARMAS | 2016-05-19 00:00:00.000 | FEMENINO  | MENORES      |        1 | ARTÍCULO 205. ACCESO CARNAL VIOLENTO                     |
-- | CAUCA        | POPAYÁN (CT)  |    19001000 | SIN EMPLEO DE ARMAS | 2016-05-19 00:00:00.000 | MASCULINO | ADULTOS      |        1 | ARTÍCULO 210 A. ACOSO SEXUAL                             |
-- +--------------+---------------+-------------+---------------------+-------------------------+-----------+--------------+----------+----------------------------------------------------------+


-- # GENERO  
-- this column contains some dirty data outside of the three values: MASCULINO | FEMENINO | NO REPORTA 

select	distinct(GENERO), count(GENERO)
from	Cleaning_Project..Delitos_sexuales_policia_nacional
group by GENERO

--+============+==================+
--| GENERO     | (No column name) |
--+============+==================+
--| FEMENINO   | 202459           |
--+------------+------------------+
--|            | 308              |
--+------------+------------------+
--| -          | 2                |
--+------------+------------------+
--| MASCULINO  | 33072            |
--+------------+------------------+
--| NO REPORTA | 631              |
--+============+==================+


-- Creating a temp_table to check the changes before replacing the '' and '-' values from GENERO to 'NO REPORTA'
with TEMP_TABLE_1 as(
select	replace(
				coalesce(nullif(GENERO,''), 'NO REPORTA') -- Replaces '' empty strings
				,'-','NO REPORTA') -- Replaces '-' 
				as	GENERO_CLEANED
from	Cleaning_Project..Delitos_sexuales_policia_nacional
)
select	distinct(GENERO_CLEANED), count(GENERO_CLEANED)
from	TEMP_TABLE_1
group by GENERO_CLEANED

--+----------------+------------------+
--| GENERO_CLEANED | (No column name) |
--+----------------+------------------+
--| FEMENINO       | 202459           |
--+----------------+------------------+
--| MASCULINO      | 33072            |
--+----------------+------------------+
--| NO REPORTA     | 941              |
--+----------------+------------------+



-- Updating GENERO
update Cleaning_Project..Delitos_sexuales_policia_nacional
set GENERO=replace(
				coalesce(nullif(GENERO,''), 'NO REPORTA') -- Replaces '' empty strings
				,'-','NO REPORTA') -- Replaces '-' 
				)



-- # ARMAS MEDIOS
-- this column contains duplicates or redundant catergories. These are going to be merged into one.

select	distinct([ARMAS MEDIOS]), count([ARMAS MEDIOS]) as COUNT
from	Cleaning_Project..Delitos_sexuales_policia_nacional
group by [ARMAS MEDIOS]



----+-----------------------------+--------+
----|        ARMAS MEDIOS         |  COUNT |
----+-----------------------------+--------+
----| SIN EMPLEO DE ARMAS         | 106030 |
----| CINTAS/CINTURON             |    100 |
----| ESPOSAS                     |     59 |
----| CORTANTES                   |     14 |
----| CORTOPUNZANTES              |    107 |
----| ESCOPOLAMINA                |   5777 |
----| -                           |      2 |
----| ARMA BLANCA / CORTOPUNZANTE |  11692 |
----| ARMAS BLANCAS               |      1 |
----| CONTUNDENTES                |  41467 |
----| ARMA DE FUEGO               |   2153 |
----| NO REPORTADO                |  68103 |
----| LICOR ADULTERADO            |    967 |
----+-----------------------------+--------+

-- Testing replacement
with TEMP_TABLE as(
select	replace(
		replace(
		replace(
		replace([ARMAS MEDIOS],'ARMAS BLANCAS','ARMA BLANCA / CORTOPUNZANTE')
				,'CORTANTES','ARMA BLANCA / CORTOPUNZANTE')
				,'CORTOPUNZANTES','ARMA BLANCA / CORTOPUNZANTE')
				,'-','NO REPORTADO') -- replaces all redundants categories and merge them into one
				as	ARMAS_CLEANED
from	Cleaning_Project..Delitos_sexuales_policia_nacional
)
select	distinct(ARMAS_CLEANED), count(ARMAS_CLEANED)
from	TEMP_TABLE
group by ARMAS_CLEANED

-- Updating ARMAS MEDIOS

update Cleaning_Project..Delitos_sexuales_policia_nacional
SET [ARMAS MEDIOS]=replace(
					replace(
					replace(
					replace([ARMAS MEDIOS],'ARMAS BLANCAS','ARMA BLANCA / CORTOPUNZANTE')
					,'CORTANTES','ARMA BLANCA / CORTOPUNZANTE')
					,'CORTOPUNZANTES','ARMA BLANCA / CORTOPUNZANTE')
					,'-','NO REPORTADO')

-- Result:
select	distinct([ARMAS MEDIOS]), count([ARMAS MEDIOS]) as COUNT
from	Cleaning_Project..Delitos_sexuales_policia_nacional
group by [ARMAS MEDIOS]


-- +-----------------------------+--------+
-- |        ARMAS MEDIOS         | COUNT  |
-- +-----------------------------+--------+
-- | SIN EMPLEO DE ARMAS         | 106030 |
-- | CINTAS/CINTURON             |    100 |
-- | ESPOSAS                     |     59 |
-- | ESCOPOLAMINA                |   5777 |
-- | ARMA BLANCA / CORTOPUNZANTE |  11814 |
-- | CONTUNDENTES                |  41467 |
-- | ARMA DE FUEGO               |   2153 |
-- | NO REPORTADO                |  68105 |
-- | LICOR ADULTERADO            |    967 |
-- +-----------------------------+--------+



-- #DELITO 
-- This column will be reduced to only the law infridgement article number instead of being followed by its description.
-- The delimited '.' will be used to separate them as every observation has it in between.

select TOP(5)[DELITO] 
from Cleaning_Project..Delitos_sexuales_policia_nacional


-- +----------------------------------------------------------+
-- |                          DELITO                          |
-- +----------------------------------------------------------+
-- | ARTÍCULO 209. ACTOS SEXUALES CON MENOR DE 14 AÑOS        |
-- | ARTÍCULO 209. ACTOS SEXUALES CON MENOR DE 14 AÑOS        |
-- | ARTÍCULO 208. ACCESO CARNAL ABUSIVO CON MENOR DE 14 AÑOS |
-- | ARTÍCULO 205. ACCESO CARNAL VIOLENTO                     |
-- | ARTÍCULO 210 A. ACOSO SEXUAL                             |
-- +----------------------------------------------------------+


select  distinct(PARSENAME([DELITO],2)) as list
from Cleaning_Project..Delitos_sexuales_policia_nacional
order by list

-- A new column will be created to store this data
alter table Cleaning_Project..Delitos_sexuales_policia_nacional
add [ARTICULO - DELITO] Nvarchar(255);

update Cleaning_Project..Delitos_sexuales_policia_nacional
set [ARTICULO - DELITO]=PARSENAME([DELITO],2) from Cleaning_Project..Delitos_sexuales_policia_nacional

select TOP(5)[ARTICULO - DELITO] 
from Cleaning_Project..Delitos_sexuales_policia_nacional


-- +-------------------+
-- | ARTICULO - DELITO |
-- +-------------------+
-- | ARTÍCULO 209      |
-- | ARTÍCULO 209      |
-- | ARTÍCULO 208      |
-- | ARTÍCULO 205      |
-- | ARTÍCULO 210 A    |
-- +-------------------+


-- # GRUPO ETARIO 
-- this column has some misspelling error which created an extra category "adoleScentes" & "adolecentes"

select	distinct([GRUPO ETARIO]), count([GRUPO ETARIO]) as COUNT
from	Cleaning_Project..Delitos_sexuales_policia_nacional
group by [GRUPO ETARIO]


-- +--------------+--------+
-- | GRUPO ETARIO | COUNT  |
-- +--------------+--------+
-- | ADULTOS      |  72469 |
-- | MENORES      | 121768 |
-- | ADOLESCENTES |   2915 |
-- |              |    541 |
-- | ADOLECENTES  |  38779 |
-- +--------------+--------+

update Cleaning_Project..Delitos_sexuales_policia_nacional
set [GRUPO ETARIO]=replace(
				coalesce(nullif([GRUPO ETARIO],''), 'NO REPORTA') -- Replaces '' empty strings
				,'ADOLECENTES','ADOLESCENTES') -- Replaces misspell 
				
select	distinct([GRUPO ETARIO]), count([GRUPO ETARIO]) as COUNT
from	Cleaning_Project..Delitos_sexuales_policia_nacional
group by [GRUPO ETARIO]

-- +--------------+--------+
-- | GRUPO ETARIO | COUNT  |
-- +--------------+--------+
-- | ADULTOS      |  72469 |
-- | MENORES      | 121768 |
-- | ADOLESCENTES |  41694 |
-- | NO REPORTA   |    541 |
-- +--------------+--------+



-- # MUNICIPIO and CODIGO DANE
-- The former is the name of the city/town/place and the later is the ID under the administrative department DANE. This helps to avoid confusion when a city 
-- has the same name as another place while maintaning a unique ID. A new column will be created to store both in a single element, for future usage.

alter table Cleaning_Project..Delitos_sexuales_policia_nacional
add [MUNICIPIO-CODIGO DANE] Nvarchar(255);

update Cleaning_Project..Delitos_sexuales_policia_nacional
set [MUNICIPIO-CODIGO DANE] = concat([MUNICIPIO],'- ID[',cast([CODIGO DANE] as int),']')

----

select top(5) *
from Cleaning_Project..Delitos_sexuales_policia_nacional


-- +--------------+---------------+-------------+---------------------+-------------------------+-----------+--------------+----------+----------------------------------------------------------+-------------------+-----------------------------+
-- | DEPARTAMENTO |   MUNICIPIO   | CODIGO DANE |    ARMAS MEDIOS     |       FECHA HECHO       |  GENERO   | GRUPO ETARIO | CANTIDAD |                          DELITO                          | ARTICULO - DELITO |    MUNICIPIO-CODIGO DANE    |
-- +--------------+---------------+-------------+---------------------+-------------------------+-----------+--------------+----------+----------------------------------------------------------+-------------------+-----------------------------+
-- | ANTIOQUIA    | SONSON        |     5756000 | SIN EMPLEO DE ARMAS | 2016-05-19 00:00:00.000 | FEMENINO  | MENORES      |        1 | ARTÍCULO 209. ACTOS SEXUALES CON MENOR DE 14 AÑOS        | ARTÍCULO 209      | SONSON- ID[5756000]         |
-- | META         | PUERTO GAITÁN |    50568000 | SIN EMPLEO DE ARMAS | 2016-05-19 00:00:00.000 | FEMENINO  | MENORES      |        1 | ARTÍCULO 209. ACTOS SEXUALES CON MENOR DE 14 AÑOS        | ARTÍCULO 209      | PUERTO GAITÁN- ID[50568000] |
-- | VALLE        | BUENAVENTURA  |    76109000 | SIN EMPLEO DE ARMAS | 2016-05-19 00:00:00.000 | FEMENINO  | MENORES      |        1 | ARTÍCULO 208. ACCESO CARNAL ABUSIVO CON MENOR DE 14 AÑOS | ARTÍCULO 208      | BUENAVENTURA- ID[76109000]  |
-- | CESAR        | BOSCONIA      |    20060000 | SIN EMPLEO DE ARMAS | 2016-05-19 00:00:00.000 | FEMENINO  | MENORES      |        1 | ARTÍCULO 205. ACCESO CARNAL VIOLENTO                     | ARTÍCULO 205      | BOSCONIA- ID[20060000]      |
-- | CAUCA        | POPAYÁN (CT)  |    19001000 | SIN EMPLEO DE ARMAS | 2016-05-19 00:00:00.000 | MASCULINO | ADULTOS      |        1 | ARTÍCULO 210 A. ACOSO SEXUAL                             | ARTÍCULO 210 A    | POPAYÁN (CT)- ID[19001000]  |
-- +--------------+---------------+-------------+---------------------+-------------------------+-----------+--------------+----------+----------------------------------------------------------+-------------------+-----------------------------+

