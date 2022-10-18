#!/usr/bin/env python
# coding: utf-8

# In[389]:


import pandas as pd


# In[390]:


import seaborn as sns
import matplotlib.pyplot as plt


# # Etude de santé Publique

# In[391]:


sousNutitionFile = pd.read_csv('DAN-P4-FAO/sous_nutrition.csv')


# In[392]:


sousNutitionFile.head()


# # Extraction des donnees 2017 du fichier de sous nutrition

# In[393]:


data_2017_sous_nutrition = sousNutitionFile.loc[sousNutitionFile['Année'] == '2016-2018']


# In[394]:


data_2017_sous_nutrition.head()


# In[395]:


data_2017_sous_nutrition.describe(include='all')


# Conversion de la valeur de la sous nutrition et Remplacement des valeurs NAN

# In[396]:


data_2017_sous_nutrition['Valeur'] = pd.to_numeric(data_2017_sous_nutrition['Valeur'], errors='coerce')
data_2017_sous_nutrition.fillna(0, inplace=True)


# Conversion de la population

# In[397]:


data_2017_sous_nutrition['Valeur']= data_2017_sous_nutrition['Valeur']*1000000
data_2017_sous_nutrition.head()


# Lecture du fichier de la population

# In[398]:


data_population = pd.read_csv('DAN-P4-FAO/population.csv')


# In[399]:


data_population.head()


# Extraction des données 2017 de la data Population

# In[400]:


data_population_2017 = data_population.loc[data_population["Année"] == 2017]


# In[401]:


data_population_2017.head()


# In[402]:


data_population_2017['Valeur'] = data_population_2017['Valeur']*1000


# Copie des données de sous nutrition de 2017

# In[403]:


data_2017_copy = data_2017_sous_nutrition.copy()


# In[404]:


data_population_2017_copy = data_population_2017.copy()


# # Jointure entre la table Sous nutrition et population

# In[405]:


df_final_sousnutrition_population = pd.merge(data_2017_copy,data_population_2017_copy, on='Zone',how='left')
df_final_sousnutrition_population.head()


# La proportion de personnes en état de sous-nutrition ;

# In[406]:


Proportion = df_final_sousnutrition_population['Valeur_x'].sum()*100/df_final_sousnutrition_population['Valeur_y'].sum()


# In[407]:


print('La proportion des personnes en état de sous nutrition est', Proportion)


# In[472]:


dispo_alimentairefile = pd.read_csv('DAN-P4-FAO/dispo_alimentaire.csv')
dispo_alimentairefile.head()


# Traitement des données NAN en les remplaçant par 0

# In[473]:


dispo_alimentairefile.fillna(0, inplace= True)


# Convertion de la disponibilite Alimentaire en Année et en kg

# In[474]:


var_dispo_modif = ['Disponibilité de matière grasse en quantité (g/personne/jour)','Disponibilité de protéines en quantité (g/personne/jour)']
for var in var_dispo_modif:
        dispo_alimentairefile[var] = dispo_alimentairefile[var]*365*0.001
    
    


# Renommage des colonnes

# In[475]:


dispo_alimentairefile.rename(columns={"Disponibilité de matière grasse en quantité (g/personne/jour)": "Disponibilité de matière grasse en quantité (kg/personne/an)",'Disponibilité de protéines en quantité (g/personne/jour)': 'Disponibilité de protéines en quantité (kg/personne/an)'}, inplace=True)


# Conversion des moyens d'acquisition et d'utilisation de la disponibilite alimentaire en kg

# In[476]:


var_modif = ['Aliments pour animaux','Autres Utilisations','Disponibilité intérieure','Exportations - Quantité','Importations - Quantité','Nourriture','Pertes','Production','Semences','Traitement','Variation de stock']
for var in var_modif:
    dispo_alimentairefile[var] = dispo_alimentairefile[var]*1000000
    


# In[477]:


dispo_alimentairefile.head(10)


# In[478]:


dispo_alimentairefile_copy = dispo_alimentairefile.copy()


# Regroupage des données par zone

# In[479]:


dispo_alimentairefile_copy = dispo_alimentairefile_copy.groupby("Zone").sum()
dispo_alimentairefile_copy.head()


# Jointure entre la table population et disponibilité alimentaire

# In[480]:


df_final_dispo_alimentaire_population = pd.merge(dispo_alimentairefile_copy,data_population_2017_copy, on='Zone',how='right')
df_final_dispo_alimentaire_population.head()


# Calcul de la disponibilité alimentaire par pays

# In[482]:


df_final_dispo_alimentaire_population['dispo_Alimentaire_par_pays'] = df_final_dispo_alimentaire_population['Disponibilité alimentaire (Kcal/personne/jour)']*df_final_dispo_alimentaire_population['Valeur']*365
df_final_dispo_alimentaire_population.head()


# In[485]:


disponibilite_alimentaire_totale = df_final_dispo_alimentaire_population['dispo_Alimentaire_par_pays'].sum(axis = 0)
disponibilite_alimentaire_totale


# Le nombre théorique de personnes qui pourraient être nourries

# In[484]:


nombre_personne_nourrir = df_final_dispo_alimentaire_population['dispo_Alimentaire_par_pays'].sum()/(2600*365)
nombre_personne_nourrir


# Extraction des données d'origine vegetale

# In[486]:


dispo_alimentairefile_copy_vegetal = dispo_alimentairefile.copy()
dispo_alimentairefile_copy_vegetal.head()


# In[487]:


dispo_alimentairefile_copy_vegetal  = dispo_alimentairefile_copy_vegetal.loc[dispo_alimentairefile_copy_vegetal["Origine"] == 'vegetale']


# Regroupage de la disponiblité alimentaire par pays

# In[488]:


dispo_alimentairefile_copy_vegetal = dispo_alimentairefile_copy_vegetal.groupby("Zone").sum()
dispo_alimentairefile_copy_vegetal.head()


# Jointure entre la table population et disponibilite alimentaire des produits vegetaux

# In[489]:


Dispo_Alimentaire_produit_vegetal = pd.merge(dispo_alimentairefile_copy_vegetal,data_population_2017_copy, on='Zone',how='right') 

Dispo_Alimentaire_produit_vegetal.head()


# Le nombre théorique de personnes qui pourraient être nourries a partir des produits vegetaux

# In[490]:


nombre_personne_nourrir_vegetal = (((Dispo_Alimentaire_produit_vegetal['Disponibilité alimentaire (Kcal/personne/jour)'])*Dispo_Alimentaire_produit_vegetal['Valeur']*365).sum())/(2600*365)


# In[491]:


print('Le nombre théorique de personnes qui pourraient être nourries a partir des produits vegetaux:', nombre_personne_nourrir_vegetal)


# In[492]:


df_final_dispo_alimentaire_population.head()


# Repartition de la disponibilité

# In[493]:


Repartition_disponibilite = dispo_alimentairefile.copy()


# In[494]:


col = ['Aliments pour animaux' , 'Autres Utilisations','Nourriture','Pertes','Semences','Traitement']
col2 = ['Exportations - Quantité','Importations - Quantité','Production','Variation de stock']
Repartition_disponibilite['utilisation'] =Repartition_disponibilite[col].sum(axis=1)
Repartition_disponibilite['moyen_acquisition'] =Repartition_disponibilite['Importations - Quantité'] + Repartition_disponibilite['Production'] + Repartition_disponibilite['Variation de stock'] - Repartition_disponibilite['Exportations - Quantité']
Repartition_disponibilite.head()


# In[495]:


Repartition_disponibilite = Repartition_disponibilite.groupby('Zone', as_index=False).sum()


# Calcul de la proportion de la disponibilité alimentaire animal, celle qui est perdue et celle qui est concrètement utilisée pour l'alimentation humaine

# In[496]:


Repartition_disponibilite['proportion_dispo_Aliment_Animal'] = (Repartition_disponibilite['Aliments pour animaux']*100)/Repartition_disponibilite['Disponibilité intérieure']
Repartition_disponibilite['proportion_dispo_nourriture'] = (Repartition_disponibilite['Nourriture']*100)/Repartition_disponibilite['Disponibilité intérieure']
Repartition_disponibilite['proportion_dispo_perte'] = (Repartition_disponibilite['Pertes']*100)/Repartition_disponibilite['Disponibilité intérieure']

Repartition_disponibilite.head()


# Calcul de la proportion globale pour l'alimentation animal

# In[497]:


proportion_animal = ((Repartition_disponibilite['Aliments pour animaux'].sum())*100)/Repartition_disponibilite['Disponibilité intérieure'].sum()
proportion_animal


# Calcul de la proportion globale pour l'alimentation humaine

# In[498]:


proportion_nourriture = (Repartition_disponibilite['Nourriture'].sum()*100)/Repartition_disponibilite['Disponibilité intérieure'].sum()
proportion_nourriture


# Calcul de la proportion globale pour la disponibilité alimentaire perdue

# In[499]:


proportion_perte = (Repartition_disponibilite['Pertes'].sum()*100)/Repartition_disponibilite['Disponibilité intérieure'].sum()
proportion_perte


# In[514]:


dispo_alimentaire_par_produit = dispo_alimentairefile.copy()


# Extraction de la disponibilité alimentaire par produit et tri par rapport à la disponibilité interieur

# In[524]:


dispo_alimentaire_par_produit = dispo_alimentaire_par_produit.groupby('Produit').sum().sort_values(by=['Disponibilité intérieure'],ascending = False)


# In[525]:


dispo_alimentaire_par_produit.head()


# La proportion de la disponibilité alimentaire par produit

# In[526]:


dispo_alimentaire_par_produit['proportion_dispo_Aliment_Animal'] = (dispo_alimentaire_par_produit['Aliments pour animaux']*100)/dispo_alimentaire_par_produit['Disponibilité intérieure']
dispo_alimentaire_par_produit['proportion_dispo_nourriture'] = (dispo_alimentaire_par_produit['Nourriture']*100)/dispo_alimentaire_par_produit['Disponibilité intérieure']
dispo_alimentaire_par_produit['proportion_dispo_perte'] = (dispo_alimentaire_par_produit['Pertes']*100)/dispo_alimentaire_par_produit['Disponibilité intérieure']

dispo_alimentaire_par_produit.head()


# # La repartition de la disponibilité sur les cereales

# Creation d'une liste contenant les cereales listés par la FAO et extraction des données sur ces céréales 

# In[529]:


liste_cereal =['Blé',
'Seigle',
'Orge',
'Avoine',
'Maïs',
'Riz (paddy)',
'Mélanges de céréales',
'Sarrasin',
'Sorgho',
'Mil',
'Quinoa',
'Autres céréales']

dispo_alimentaire_par_produit_cereal = dispo_alimentairefile.loc[dispo_alimentairefile['Produit'].isin(liste_cereal)]
dispo_alimentaire_par_produit_cereal.head()


# Calcul de la proportion de cereal par pays, pour l'alimentation humaine et animale, et la proportion perdue

# In[553]:


dispo_alimentaire_par_produit_cereal['proportion_animal'] = (dispo_alimentaire_par_produit_cereal['Aliments pour animaux']*100)/dispo_alimentaire_par_produit_cereal['Disponibilité intérieure']
dispo_alimentaire_par_produit_cereal['proportion_humaine'] = (dispo_alimentaire_par_produit_cereal['Nourriture']*100)/dispo_alimentaire_par_produit_cereal['Disponibilité intérieure']
dispo_alimentaire_par_produit_cereal['proportion_pertes'] = (dispo_alimentaire_par_produit_cereal['Pertes']*100)/dispo_alimentaire_par_produit_cereal['Disponibilité intérieure']

dispo_alimentaire_par_produit_cereal.head()


# In[532]:


proportion_animal_cereal = ((dispo_alimentaire_par_produit_cereal['Aliments pour animaux'].sum())*100)/dispo_alimentaire_par_produit_cereal['Disponibilité intérieure'].sum()
proportion_animal_cereal


# In[533]:


proportion_alimentaire_cereal = ((dispo_alimentaire_par_produit_cereal['Nourriture'].sum())*100)/dispo_alimentaire_par_produit_cereal['Disponibilité intérieure'].sum()
proportion_alimentaire_cereal


# Les 10 premiers pays utilisateurs du blé en alimentation animal

# In[534]:


df_ble =dispo_alimentaire_par_produit_cereal.loc[dispo_alimentaire_par_produit_cereal['Produit'] == 'Blé'].sort_values(by=['proportion_animal'], ascending=False)
df_ble.head(10)


# Les 10 premiers pays utilisateurs du blé en alimentation humaine

# In[535]:


df_ble_humaine =dispo_alimentaire_par_produit_cereal.loc[dispo_alimentaire_par_produit_cereal['Produit'] == 'Blé'].sort_values(by=['proportion_humaine'], ascending=False)
df_ble_humaine.head(10)


# Le céréal le plus utilisé dans le monde en alimentation animal

# In[536]:


cereal_up = dispo_alimentaire_par_produit_cereal.groupby('Produit',as_index=False).sum().sort_values(by='proportion_animal', ascending=False)
cereal_up.head(6)


# In[537]:


plt.pie(cereal_up["Aliments pour animaux"], labels=cereal_up["Produit"]) 
plt.show() 


# Le céréal le plus utilisé dans le monde en alimentation humaine

# In[538]:


dispo_alimentaire_par_produit_cereal.groupby('Produit',as_index=False).sum().sort_values(by='proportion_humaine', ascending=False)


# In[539]:


cereal_up_nourriture = dispo_alimentaire_par_produit_cereal.groupby('Produit',as_index=False).sum().sort_values(by='proportion_humaine', ascending=False)


# In[540]:


plt.pie(cereal_up_nourriture["Nourriture"], labels=cereal_up_nourriture["Produit"]) 
plt.show() 


# Proportion par pays

# In[541]:


df_final_sousnutrition_population.head()


# Calcul de la proportion par pays en 2017

# In[542]:


df_final_sousnutrition_population['proportion_par_pays'] = (df_final_sousnutrition_population['Valeur_x']*100)/df_final_sousnutrition_population['Valeur_y']
df_final_sousnutrition_population.head()


# In[543]:


df_final_sousnutrition_population.describe(include='all')


# Les pays pour lesquels la proportion de personnes sous-alimentées est la plus forte en 2017

# In[544]:


df_final_sousnutrition_population.sort_values(by=['proportion_par_pays'], ascending=False)


# Les pays ayant le plus de disponibilité par habitant

# In[546]:


dispo_alimentairefile_copy.sort_values(by=['Disponibilité alimentaire (Kcal/personne/jour)'],ascending = False)


# Les pays ayant le moins de disponibilité par habitant

# In[548]:


dispo_alimentairefile_copy.sort_values(by=['Disponibilité alimentaire (Kcal/personne/jour)'],ascending = True)


# ## Chargement du fichier d'aide alimentaire

# In[549]:


aide_alimentaire_file = pd.read_csv('DAN-P4-FAO/aide_alimentaire.csv')
aide_alimentaire_file.head()


# In[550]:


aide_alimentaire_2013 = aide_alimentaire_file.loc[aide_alimentaire_file['Année']==2013,['Pays bénéficiaire','Produit','Valeur']]
aide_alimentaire_2013.head()


# In[551]:


aide_alimentaire_2013.info()


# Les pays qui ont le plus bénéficié d’aide depuis 2013

# In[552]:


aide_alimentaire_2013 =aide_alimentaire_2013.groupby('Pays bénéficiaire').sum().sort_values(by='Valeur',ascending=False)
aide_alimentaire_2013.head()


# In[ ]:




