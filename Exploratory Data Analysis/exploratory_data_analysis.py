# =============================================================================
# **DATASET DESCRIPTION**
# In this dataset you can find information on sexual crimes from January 01,
# 2010 to May 31, 2021.
# #Source: DIJIN - National Police. Data extracted on June 14, 2021 at 18:00
# hours. 18:00 hours.
# URL:  https://www.datos.gov.co/Seguridad-y-Defensa/Reporte-Delitos-sexuales-Polic-a-Nacional/fpe5-yrmw
#
# **Variables**
# DEPARTAMENTO=Department/State where crime took place.
# MUNICIPIO=City/Municipality where crime took place.
# CODIGO.DANE= City/Municipality ID in DANE(National Administrative Department of Statistics, Spanish: Departamento Administrativo Nacional de Estadística)
# ARMAS.MEDIOS= Weapon used.
# FECHA.HECHO= Date of report.
# GENERO= Gender.
# GRUPO.ETARIO= Age group.
# CANTIDAD= Amount of criminals involved.
# DELITO= Official crime category by law.
# =============================================================================
#%%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns


crime_data = pd.read_csv('database.csv')  # importing the database

#%%

# =============================================================================
# A look up into the dataset, there are 11 columns containing the information
# of the place where the crime took place and basic info about the victim that
# would help to explore de data and what it has to say about the crime rate
# en each geographical division within the country as well as the gender/age
# group that it's the most affected.
# =============================================================================

crime_data.head()
crime_data.describe()
crime_data.describe(include=object)

# Some columns' type will be changed to 'category', 'int' and 'datetime' as
# seen convenient
crime_data.info()

#%%
# =============================================================================
# DATA PREPARATION
# =============================================================================

crime_data.rename(columns={"FECHA HECHO": "FECHA",
                  "ARMAS MEDIOS": "ARMA"}, inplace=True)  # simplifying names
crime_data.isnull().sum()  # There are 2 missing values
# The number is low so both rows with missing values will be dropped
crime_data.dropna(inplace=True)

# All Colombia's departments names are in the dataset without any misspelled duplicate.
set(crime_data["DEPARTAMENTO"])

# Changing columns to category type

columns = ["DEPARTAMENTO", "MUNICIPIO", "GENERO", "GRUPO ETARIO",
           "DELITO", "ARMA", "CANTIDAD", "ARTICULO - DELITO", "MUNICIPIO-CODIGO DANE"]
for i in columns:
    crime_data[i] = crime_data[i].astype("category")

#CODIGO.DANE should be a factor as it is an ID assigned for each city/municipality.
#before hand it will be converted to INT so remove its decimals
crime_data["CODIGO DANE"] = crime_data["CODIGO DANE"].astype(
    int).astype("category")

#FECHA is changed from factor to date class
crime_data["FECHA"] = pd.to_datetime(crime_data["FECHA"])

#GENERO with translated categories

dict={'NO REPORTA':'NOT REPORTED','MASCULINO':'MALE','FEMENINO':'FEMALE'}
crime_data['GENERO'].replace(dict,inplace=True)
# ARMA with translated categories

dict={'SIN EMPLEO DE ARMAS':'NO USE OF WEAPONS','NOT REPORTEDDO':'NOT REPORTED',
     'CONTUNDENTES':'BLUNT','ARMA BLANCA / CORTOPUNZANTE':'SHARP WEAPON',
     'ESCOPOLAMINA':'SCOPOLAMINE','ARMA DE FUEGO':'FIREARM',
     'LICOR ADULTERADO':'ADULTERATED LIQUOR','CINTAS/CINTURON':'BELTS',
     'ESPOSAS':'HANDCUFFS'}
crime_data['ARMA'].replace(dict,inplace=True)

#GRUPO ETARIO with trasnlated categories
dict={'ADOLESCENTES':'ADOLESCENTS','ADULTOS':'ADULTS','MENORES':'MINORS','NO REPORTA':'NOT REPORTED'}
crime_data['GRUPO ETARIO'].replace(dict,inplace=True)



#CANTIDAD
crime_data["CANTIDAD"].value_counts()
#The outlier of 86 has to be removed as it's likely a mistype.
crime_data=crime_data[crime_data["CANTIDAD"]!=86]

#%%
# =============================================================================
# EDA - EXPLORATORY DATA ANALYSIS
# =============================================================================


#DEPARTAMENTO

crime_by_department=crime_data.groupby(['DEPARTAMENTO','GENERO'])['GENERO'].count().unstack()
crime_by_department=crime_by_department.fillna(0)

#Now create a new column with the total of reports by each department
crime_by_department['TOTAL']=crime_by_department['FEMALE']+crime_by_department['MALE']+crime_by_department['NOT REPORTED']
crime_by_department=crime_by_department.sort_values('TOTAL',ascending=False) # Sort TOTAL in decreasing order

# Horizontal bar graph showing the distribution of crimes by department and gender
sns.set_theme(style="ticks")
fig,ax = plt.subplots(figsize=(7,7),dpi=100)
sns.set_color_codes("muted")
sns.barplot(x="NOT REPORTED",y=crime_by_department.index.values,
            data=crime_by_department,color='y',label='NOT REPORTED',
            order=crime_by_department.index.values)
sns.barplot(x="MALE",y=crime_by_department.index.values,
            data=crime_by_department,color='b',
            left=crime_by_department['NOT REPORTED'],label='MALE',
            order=crime_by_department.index.values)
sns.set_color_codes("pastel")
sns.barplot(x="FEMALE",y=crime_by_department.index.values,
            data=crime_by_department,color='r',
            left=crime_by_department['MALE'],label='FEMALE',
            order=crime_by_department.index.values)
ax.legend(loc='lower right')
ax.set_xlabel("# of reported crimes")
ax.set_title("Crime reports distribution by department and gender")



#%%
# =============================================================================
# Now a new graph is made to see the crime reports per 1000 inhabitants but
# first the data of each Department is neededInhabitants by department, Census
# year 2018.
# Source: https://sitios.dane.gov.co/cnpv/#!/
# =============================================================================

aux_department=["CUNDINAMARCA","ANTIOQUIA","VALLE","SANTANDER","ATLÁNTICO",
                "HUILA","TOLIMA","RISARALDA","BOLÍVAR","META",
                "NORTE DE SANTANDER","BOYACÁ","CALDAS","NARIÑO","MAGDALENA",
                "CÓRDOBA","SUCRE","CAUCA","CESAR","QUINDÍO","CAQUETÁ",
                "GUAJIRA","CASANARE","ARAUCA","PUTUMAYO","CHOCÓ","GUAVIARE",
                "AMAZONAS","SAN ANDRÉS","VICHADA","VAUPÉS","GUAINÍA"]
aux_inhabitant=[9974346,5974788,3789874,2008841,2342265,1009548,1228763,839597,
                1909460,919129,1346806,1135698,923472,1335521,1263788,1555596,
                864036,1243503,1098577,509640,359602,825364,379892,239503,
                283197,457412,73081,66056,48299,76642,37690,44431]
aux_male_rate=[48.2,48.3,47.5,49,48.7,49.9,49.6,47.9,49.6,50.6,49.3,49.2,48.5,
               49,50,49.8,50.3,49.5,49.5,48.2,50.7,49,50.5,50.5,50.5,49.4,53.5,
               52.1,48.3,53.1,52.5,52.3]
aux_female_rate=[51.8,51.7,52.5,51,51.3,50.1,50.4,52.1,50.4,49.4,50.7,50.8,
                 51.5,51,50,50.2,49.7,50.5,50.5,51.8,49.3,51,49.5,49.5,49.5,
                 50.6,46.5,47.9,51.7,46.9,47.5,47.8]
data=list(zip(aux_department,aux_inhabitant,aux_male_rate,aux_female_rate))
inhabitants_by_department=pd.DataFrame(data,
                                       columns=['DEPARTMENT','INHABITANTS',
                                                'MALE RATE','FEMALE RATE'],
                                       index=aux_department)

# Crime rate by 1.000 inhabitants

total_crime_per1000= pd.DataFrame(crime_by_department['TOTAL']/(inhabitants_by_department['INHABITANTS'])*1000,columns=['TOTAL']).sort_values('TOTAL',ascending=False)
sns.set_theme(style="ticks")
fig,ax = plt.subplots(figsize=(7,7),dpi=150)
sns.barplot(x="TOTAL",y=total_crime_per1000.index.values,data=total_crime_per1000,color='b')
ax.set_xlabel("# of reported crimes per 1000 inhabitants")
ax.set_title("Crime reports distribution by department per 1000 inhabitants")

#%%

#MUNICIPIO
# Making a distribution of the top 10 municipalities with the highest amount of
# crime rate.

# CODIGO DANE  is used instead of MUNICIPIO as there are places with the same
# name but with different CODIGO DANE number.

crime_by_municipality=crime_data.groupby(['CODIGO DANE','GENERO'])['GENERO'].count().unstack()
crime_by_municipality['TOTAL']=crime_data.groupby(['CODIGO DANE'])['GENERO'].count().values
crime_by_municipality=crime_by_municipality.nlargest(10,'TOTAL').reset_index()


# Making a dict to replace each CODIGO DANE for its equivalent in MUNICIPIO name
aux=crime_data[['CODIGO DANE','MUNICIPIO']]
aux_dict=aux.drop_duplicates().set_index('CODIGO DANE').to_dict()['MUNICIPIO']
crime_by_municipality.replace({'CODIGO DANE':aux_dict},inplace=True)
crime_by_municipality.rename(columns={'CODIGO DANE':'MUNICIPIO'},inplace=True)

#Creating plot
fig,ax=plt.subplots(dpi=150)
sns.set_theme(style="whitegrid")
sns.barplot(x='TOTAL',y='MUNICIPIO',data=crime_by_municipality,color='b',order=crime_by_municipality.sort_values('TOTAL',ascending=False)['MUNICIPIO'])
ax.set_ylabel("")
ax.set_xlabel("# of reported crimes")
ax.set_title("Top #10 of municipalities with highest crime reports")


#%%
# ARMA
# Making a plot of the most used weapons

weapons_total=crime_data.groupby('ARMA')['ARMA'].count()
weapons_total.sort_values(inplace=True,ascending=False)
weapons_total.rename(index=dict,inplace=True)
fig, ax=plt.subplots(dpi=150)
sns.set_theme(style="whitegrid")
sns.barplot(x=weapons_total,y=weapons_total.index.astype(str))
ax.set_ylabel('')
ax.set_xlabel('# of reported crimes associated with the weapon')
ax.set_title('Weapon usage in crimes')


#%% Making plot to check if the no use of weapon is related to the age group of the victim

weapon_by_age_group=crime_data.groupby(['GRUPO ETARIO','ARMA'])['ARMA'].count().rename('VALUE').reset_index()
weapon_by_age_group=weapon_by_age_group.query('`ARMA`=="NO USE OF WEAPONS"')

fig, ax=plt.subplots(dpi=150)
sns.set_theme(style="whitegrid")
sns.barplot(data=weapon_by_age_group,
            x=weapon_by_age_group.VALUE,y=weapon_by_age_group["GRUPO ETARIO"],ci=None,
            order=weapon_by_age_group.sort_values('VALUE',ascending=False)['GRUPO ETARIO'])
ax.set_ylabel('')
ax.set_xlabel('# of reported crimes associated')
ax.set_title('Crime reports by age group where no weapon was used')

#%% Now cheking which of the adults victims are distributed by gender and no weapon was used
noweapon_by_gender=crime_data.groupby(['GRUPO ETARIO','ARMA','GENERO'])['GENERO'].count().rename('VALUE').reset_index()
noweapon_by_gender=noweapon_by_gender.query('`ARMA`=="NO USE OF WEAPONS" & `GRUPO ETARIO`=="ADULTS"')

fig, ax=plt.subplots(dpi=150)
sns.set_theme(style="whitegrid")
sns.barplot(data=noweapon_by_gender,
            x=noweapon_by_gender.VALUE,y=noweapon_by_gender["GENERO"])
ax.set_ylabel('')
ax.set_xlabel('# of reported crimes associated')
ax.set_title('Crime reports by gender where no weapon was used against an adult')

#%% Now same as before but trying to see if in the use of weapons there is any difference

sharp_weapon_by_gender=crime_data.groupby(['GRUPO ETARIO','ARMA','GENERO'])['GENERO'].count().rename('VALUE').reset_index()
sharp_weapon_by_gender=sharp_weapon_by_gender.query('`ARMA`=="SHARP WEAPON" & `GRUPO ETARIO`=="ADULTS"')

fig, ax=plt.subplots(dpi=150)
sns.set_theme(style="whitegrid")
sns.barplot(data=noweapon_by_gender,
            x=noweapon_by_gender.VALUE,y=noweapon_by_gender["GENERO"])
ax.set_ylabel('')
ax.set_xlabel('# of reported crimes associated')
ax.set_title('Crime reports by gender where no weapon was used against an adult')

#%%

weapon_by_gender=crime_data.groupby(['GRUPO ETARIO','ARMA','GENERO'])['GENERO'].count().rename('VALUE').reset_index()
weapon_by_gender.query('`GRUPO ETARIO`=="ADULTS"')
sns.catplot(data=weapon_by_gender, x="GENERO", y="VALUE",col="ARMA", col_wrap=2,
            saturation=.5,kind="bar", ci=None)

#%%
#FECHA
# Making a distribution plot where crimes rate are displayed by month,

crime_by_year=crime_data.groupby([crime_data['FECHA'].dt.year,
                                  crime_data['FECHA'].dt.month]).size()
crime_by_year.rename('VALUE',inplace= True)
crime_by_year.index.names=['YEAR', 'MONTH']
crime_by_year=crime_by_year.reset_index()


crime_by_month=crime_by_year.groupby('MONTH')['VALUE'].mean()
dict={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun'
      ,7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
crime_by_year.replace({'MONTH':dict},inplace=True)

sns.set_theme(style="darkgrid")
g=sns.relplot(data=crime_by_year[crime_by_year['YEAR']<2021],
              x='MONTH',y='VALUE',col='YEAR',col_wrap=3,
              hue='YEAR',kind='line',
              linewidth=5,height=3,aspect=1.5,legend=False,zorder=5)

for year, ax in g.axes_dict.items():
    #Change titles
    ax.text(0.85,0.85,year, transform=ax.transAxes, fontweight="bold",size=20)
    #Add preexisting
    sns.lineplot(
    data=crime_by_year[crime_by_year['YEAR']<2021], x="MONTH", y="VALUE", units="YEAR",
    estimator=None, color=".7", linewidth=1, ax=ax)
    ax.grid(axis='y')

ax.set_xticks(ax.get_xticks()[::2])
g.set_titles('')
g.set_axis_labels("", "Crime reports")
g.tight_layout()

#%% GENERO
# Plotting to check which gender is the most affected
crime_by_gender=crime_data.groupby('GENERO').size().reset_index(name='VALUE')
# Percentage of total reported crimes by gender
crime_by_gender['VALUE']=crime_by_gender['VALUE']/crime_by_gender['VALUE'].sum()*100


fig, ax=plt.subplots(dpi=150)

sns.set_theme(style="whitegrid")
sns.barplot(data=crime_by_gender,x='GENERO',y='VALUE')

for bar in ax.patches:

    ax.annotate(format(bar.get_height(), '.2f')+"%",
                   (bar.get_x() + bar.get_width() / 2,
                    bar.get_height()), ha='center', va='center',
                   size=10, xytext=(0, 3),
                   textcoords='offset points',fontweight="bold")

ax.set_ylim(top=100)
ax.yaxis.set_major_formatter(PercentFormatter(100))
ax.set_title('Genders distribution in crime reports')
ax.set_xlabel("")
ax.set_ylabel("")
plt.show()


#%% GRUPO.ETARIO
# Plot distribution by each age group and see which one is the most affected

crime_by_age_group=crime_data.groupby('GRUPO ETARIO').size().reset_index(name='VALUE')

crime_by_age_group['VALUE']=crime_by_age_group['VALUE']/crime_by_age_group['VALUE'].sum()*100


fig, ax=plt.subplots(dpi=150,figsize=(7,2))
sns.set_theme(style="whitegrid")
sns.barplot(data=crime_by_age_group,
            x='GRUPO ETARIO',y='VALUE',
            order=crime_by_age_group.sort_values('VALUE',ascending=False)['GRUPO ETARIO'])

sns.set_theme(style="whitegrid")
for bar in ax.patches:

    ax.annotate(format(bar.get_height(), '.2f')+"%",
                    (bar.get_x() + bar.get_width() / 2,
                    bar.get_height()), ha='center', va='center',
                    size=12, xytext=(0, 5),
                    textcoords='offset points',fontweight="bold")

ax.set_ylim(top=100)
ax.yaxis.set_major_formatter(PercentFormatter(100))
ax.set_title('Victim age group  distribution in crime reports')
ax.set_xlabel("")
ax.set_ylabel("")
ax.tick_params(axis='x')
plt.show()

#%% CANTIDAD
# This one doesn't require a plot because more than 90% of the crime reports
# were done by a single criminal
crime_by_criminal_amount=crime_data.groupby('CANTIDAD').size().reset_index(name='VALUE')
crime_by_criminal_amount['VALUE']=crime_by_criminal_amount['VALUE']/crime_by_criminal_amount['VALUE'].sum()*100
crime_by_criminal_amount['VALUE']=crime_by_criminal_amount['VALUE'].apply(lambda x: ('%1.1f'%x +'%'))
print(crime_by_criminal_amount.head(5))

#%% DELITO
# Plot to see the most common law infridgment by general and by department.


crime_by_infringement=crime_data.groupby('DELITO').size().reset_index(name='VALUE')
crime_by_infringement['VALUE']=crime_by_infringement['VALUE']/crime_by_infringement['VALUE'].sum()*100
crime_by_infringement['DELITO']=crime_by_infringement['DELITO'].str.partition(sep='.')[0] # Trimming the law description down to only the article number.

fig, ax=plt.subplots(dpi=150)
sns.set_theme(style="whitegrid")
sns.barplot(data=crime_by_infringement.iloc[0:5],
            x='DELITO',y='VALUE',
            order=crime_by_infringement.iloc[0:5].sort_values('VALUE',ascending=False)['DELITO'])
for bar in ax.patches:

  # Using Matplotlib's annotate function and
  # passing the coordinates where the annotation shall be done
  # x-coordinate: bar.get_x() + bar.get_width() / 2
  # y-coordinate: bar.get_height()
  # free space to be left to make graph pleasing: (0, 8)
  # ha and va stand for the horizontal and vertical alignment
    ax.annotate(format(bar.get_height(), '.2f')+"%",
                   (bar.get_x() + bar.get_width() / 2,
                    bar.get_height()), ha='center', va='center',
                   size=12, xytext=(0, 5),
                   textcoords='offset points',fontweight="bold")

ax.tick_params(axis='x', rotation=70)
ax.set_ylim(top=50)
ax.yaxis.set_major_formatter(PercentFormatter(100))
ax.set_title('TOP #5 law ingringment')
ax.set_xlabel("")
ax.set_ylabel("")
plt.show()

# %%


# %%

# %%

# %%

# %%

# %%
