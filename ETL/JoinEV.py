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
import csv

import seaborn as sns
import matplotlib.pyplot as plt

#loading datasets
train_df = pd.read_csv('kjbe974543jbt398ht43j', sep=';')
test_df = pd.read_csv('kjbefkew8y549uj5b43985', sep=';')

group_df = pd.read_csv('ljn49584j5n3486h3o8i', sep=';')
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
train_df=train_df.dropna()

    
import itertools
from itertools import repeat

###############################################################################
################### FIN TRATAMIENTO DATASET ###################################


#### METODO PARA AGRUPAR LOS ELEMENTOS DE VÍA EN UN SOLO REGISTRO CUANDO EL PK Y LA SESIÓN SON LA MISMA ####
""" A través de dos bucles while, uno para recorrer todo el dataset, y otro para recorrer lo que nos va quedando a partir
del pk (i) actual, guardamos los elementos de vía agrupados y sin que se repitan y borramos los registros antiguos.
Esto se hace si se verifica la condición que hay en el if.
Partimos de la premisa de que el csc viene ordenado por DTR_IA_ID y INCI_PK_PICO"""

def joinEV(train_df):

    listaInd = []
    df = train_df.copy()
    tam = len(df)
    i = 0
    while i < tam:
        j = i + 1
        while j < tam:
            if(df['INCI_PK_PICO'].iloc[i] == df['INCI_PK_PICO'].iloc[j] and df['SES_IA_ID'].iloc[i] == df['SES_IA_ID'].iloc[j] and df['DE_C_NOMBRE'].iloc[i] != df['DE_C_NOMBRE'].iloc[j] and not (df['DE_C_NOMBRE'].iloc[j] in df['DE_C_NOMBRE'].iloc[i])):

                df['DE_C_NOMBRE'].iloc[i] = df['DE_C_NOMBRE'].iloc[i]+'|'+df['DE_C_NOMBRE'].iloc[j]
                listaInd.append(j)
                j = j + 1
            else:
                break # Vamos a comparar solo mientras se repitan los PKs
           
        i = i + 1
    df = df.drop(df.index[listaInd])
    return df.to_csv('EV.csv',encoding='utf-8')

def joinEV1(train_df):

    listaInd = []
    df = train_df.copy()
    tam = len(df)
    aux_str = ''
    lista_str = []
    i = 0
    while i < tam:
        j = i + 1
        while j < tam:
            aux_str = df['DE_C_NOMBRE'].iloc[i]
            aux_str.split("|")
            if aux_str not in lista_str:
                lista_str.append(aux_str)
            if(df['INCI_PK_PICO'].iloc[i] == df['INCI_PK_PICO'].iloc[j] and df['SES_IA_ID'].iloc[i] == df['SES_IA_ID'].iloc[j] and df['DE_C_NOMBRE'].iloc[i] != df['DE_C_NOMBRE'].iloc[j] and not (df['DE_C_NOMBRE'].iloc[j] in lista_str)):

                df['DE_C_NOMBRE'].iloc[i] = df['DE_C_NOMBRE'].iloc[i]+'|'+df['DE_C_NOMBRE'].iloc[j]
                listaInd.append(j)
                j = j + 1
            else:
                break # Vamos a comparar solo mientras se repitan los PKs
           
        i = i + 1
    df = df.drop(df.index[listaInd])
    return df.to_csv('EV1.csv',encoding='utf-8',index=False)


joinEV1(train_df)