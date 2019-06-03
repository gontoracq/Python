# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:09:56 2019

@author: gtorres
"""

########################### LIMPIEZA DEL DATASET #############################
import numpy as np
import pandas as pd
import random as rnd
import time

import seaborn as sns
import matplotlib.pyplot as plt

#loading datasets
train_df = pd.read_csv('C:/Users/gtorres/Desktop/Proyectos/DATA SCIENCE TREN/Querys/Dataset_v3.csv', sep=';')
test_df = pd.read_csv('C:/Users/gtorres/Desktop/Proyectos/DATA SCIENCE TREN/Querys/Dataset_v3.csv', sep=';')

group_df = pd.read_csv('C:/Users/gtorres/Desktop/Proyectos/DATA SCIENCE TREN/Querys/PK_GRAV_D.csv', sep=';')
#Ponemos los campos de tipo string a un tipo unique especial que los convierte a una especie
#booleanos/numericos distribuidos en una nueva columna por cada posible valor y true/false

"""for elem in train_df['DE_C_NOMBRE'].unique():
    train_df[str(elem)] = train_df['DE_C_NOMBRE'] == elem
for elem in train_df['INCI_C_OBSERVACIONES'].unique():
    train_df[str(elem)] = train_df['INCI_C_OBSERVACIONES'] == elem"""
    
#Eliminamos atributos que hemos pasado a tipos aleatorios en unos nuevos
del train_df["INCI_C_OBSERVACIONES"]
#del train_df["DE_C_NOMBRE"]

#Eliminamos atributo de id inservible
del train_df["EV_I_ID_LINEA"]

#Eliminamos atributos problematicos
del train_df["EV_I_PK_INICIO"]
del train_df["EV_I_PK_FIN"]

#train_df.round(decimals=5)

train_df['SES_D_INICIO'] = pd.to_numeric(pd.to_datetime(train_df['SES_D_INICIO']))
train_df['INCI_PK_PICO'] = pd.to_numeric(train_df['INCI_PK_PICO'], downcast='float')
train_df['SES_D_INICIO'] = pd.to_datetime(pd.to_numeric(train_df['SES_D_INICIO']))
train_df=train_df.dropna()

    
import itertools
from itertools import repeat

###############################################################################
################### FIN TRATAMIENTO DATASET ###################################

def joinEV(train_df):

    listaInd = []
    df = train_df[0:1000]
    for i in range(len(df)):
        for j in range (i,len(df)):
            if(df['INCI_PK_PICO'][i] == df['INCI_PK_PICO'][j] 
                and df['SES_IA_ID'][i] == df['SES_IA_ID'][j]
                    and df['DE_C_NOMBRE'][i] != df['DE_C_NOMBRE'][j]):

                df['DE_C_NOMBRE'][i] = df['DE_C_NOMBRE'][i]+'|'+df['DE_C_NOMBRE'][j]
                listaInd.append(j)

    df = df.drop(df.index[listaInd])
    return df.to_csv('EV.csv',encoding='utf-8')

def joinEV1(train_df):

    listaInd = []
    df = train_df.copy()
    for i in range(len(df)):
        for j in range (i,len(df)):
            if(df['INCI_PK_PICO'][i] == df['INCI_PK_PICO'][j] 
                and df['SES_IA_ID'][i] == df['SES_IA_ID'][j]
                    and df['DE_C_NOMBRE'][i] != df['DE_C_NOMBRE'][j]):

                df['DE_C_NOMBRE'][i] = df['DE_C_NOMBRE'][i]+'|'+df['DE_C_NOMBRE'][j]
                listaInd.append(j)

    df = df.drop(df.index[listaInd])
    return df.to_csv('EV.csv',encoding='utf-8')

joinEV(train_df)