# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:09:56 2019

@author: gtorres
"""

########################### LIMPIEZA DEL DATASET #############################

import pandas as pd
import numpy as np
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

for elem in train_df['DE_C_NOMBRE'].unique():
    train_df[str(elem)] = train_df['DE_C_NOMBRE'] == elem
for elem in train_df['INCI_C_OBSERVACIONES'].unique():
    train_df[str(elem)] = train_df['INCI_C_OBSERVACIONES'] == elem
    
#Eliminamos atributos que hemos pasado a tipos aleatorios en unos nuevos
del train_df["INCI_C_OBSERVACIONES"]
del train_df["DE_C_NOMBRE"]

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


#########  METODOS PARA CEAR LA LISTA CON LOS PK REPETIDOS Y SUS RESPECTIVAS GRAVEDADES  Y FECHAS  ##########

def crearListaPKRepetidos():
    listaPK = []
    listaSol = []

    df = train_df.copy()
    
    for i in range (len(df)):
        listaPK.append(df['INCI_PK_PICO'][i])
    
    for a, b in itertools.combinations(listaPK,2):
        if (igualConMargen(a, b, 0.01)):
            listaSol.append(a)
            listaSol.append(b)
            
    return listaSol

def guardaIndicesPKRep():
    listaPK = []
    listaInd = []

    df = train_df.copy()
    
    for i in range (len(df)):
        listaPK.append(df['INCI_PK_PICO'][i])
    
    for (i,_),(j,_) in itertools.combinations(enumerate(listaPK), 2):
        if (igualConMargen(listaPK[i], listaPK[j], 0.01)):
            listaInd.append(i)
            listaInd.append(j)
            
    return listaInd

def gravConPkRep(listaIndices):
    
    listaSol = []
    
    for i in range (len(listaIndices)):
        listaSol.append(train_df['INCI_I_GRAVEDAD'][listaIndices[i]])
 
    return listaSol

def fechaConPKRep(listaIndices):

    listaSol = []
    
    for i in range (len(listaIndices)):
        listaSol.append(train_df['SES_D_INICIO'][listaIndices[i]])
 
    return listaSol

def listaDeListasRes(listaPK,listaGr,listaDates):

    listaRes=[[]]

    for i in range (0,len(listaGr)):
        listaRes.append([listaPK[i],listaGr[i],listaDates[i]])
    del listaRes[0]
    return listaRes
    
           
################  METODO PARA CONTAR LAS OCURRENCIAS DE UN PK  ####################
 
def cuentaOcurrencias(lista,pk):
    cont = None
    
    if lista:
        for i in range (0,len(lista)):
            if (train_df['INCI_PK_PICO'][i] in lista):
                cont+=1
    return cont


################  METODOS AUXILIARES  ############################

def igualConMargen(operando1, operando2, margen):
    if ((operando1 == operando2) or operando1 == (operando2 + margen) or operando2 == (operando1+ margen)):
        return True
    else:
        return False


######## METODO PARA PASAR A UN DATAFRAME #############

def transListToDataFr(lista):
    df = pd.DataFrame(lista)
    return df


######################### TEST ###############################################

#listaLimpia = borraElementosIncorrectos(listaAgrupaciones)
#print(crearListaPK2())
#print(crearListaPKRepetidos())
#df = pd.DataFrame(crearListaPKRepetidos(), columns=["PK"])
#df.to_csv('list.csv', index=False)
#print(gravConPkRep(crearListaPKRepetidos()))
listaAgrupaciones = listaDeListasRes(crearListaPKRepetidos(),gravConPkRep(guardaIndicesPKRep()),fechaConPKRep(guardaIndicesPKRep()))

#print(len(crearListaPKRepetidos()))
#print(len(gravConPkRep(guardaIndicesPKRep())))

dataF = transListToDataFr(listaAgrupaciones)
dataF.to_csv('agrupaPKRepConGrD.csv')

#print(guardaIndicesPKRep())

print(listaDeListasRes(crearListaPKRepetidos(),gravConPkRep(guardaIndicesPKRep()),fechaConPKRep(guardaIndicesPKRep())))