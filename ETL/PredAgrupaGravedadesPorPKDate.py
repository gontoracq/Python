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
pred_df = pd.read_csv('kjned974r4kj9843htk', sep=';', encoding='utf-8')

    
import itertools
from itertools import repeat

###############################################################################
################### FIN TRATAMIENTO DATASET ###################################


#########  METODOS PARA CEAR LA LISTA CON LOS PK REPETIDOS Y SUS RESPECTIVAS GRAVEDADES  Y FECHAS  ##########

margen = 0.01
listaPK = []
listaSolGr = []

################  METODOS AUXILIARES  ############################

def igualConMargen(operando1, operando2, margen):
    if (np.absolute(float(operando1) - float(operando2) <= margen)):
        return True
    else:
        return False

#### METODO QUE RELLENA LAS LISTAS ARRIBA DEFINIDAS CON LOS PK QUE SE REPITEN Y SUS RESPECTIVAS GRAVEDADES Y FECHAS ####

def rellenaListas():
    
    listaAux = []
    
    for i in range (0,len(pred_df)):
        listaAux.append(pred_df['INCI_PK_PICO'].iloc[i])
    
    for j in range (len(listaAux)):
        k = j+1
        while k < len(listaAux)-1:
            if (igualConMargen(listaAux[j], listaAux[k],margen) and pred_df['DTR_IA_ID'].iloc[j] == pred_df['DTR_IA_ID'].iloc[k]):
                listaPK.append(listaAux[j])
                listaSolGr.append(pred_df['INCI_I_GRAVEDAD'].iloc[j])
                del listaAux[k]
            if listaAux[j] - listaAux[k] > margen:
                break
            k=k+1

rellenaListas()


def listaDeListasRes():

    listaRes=[[]]

    for i in range (0,len(listaSolGr)):
        listaRes.append([listaPK[i],listaSolGr[i]])
    del listaRes[0]
    return listaRes
    
           
################  METODO PARA CONTAR LAS OCURRENCIAS DE UN PK  ####################
 
def cuentaOcurrencias(lista,pk):
    cont = None
    
    if lista:
        for i in range (0,len(lista)):
            if (pred_df['INCI_PK_PICO'].iloc[i] in lista):
                cont+=1
    return cont


######## METODO PARA PASAR A UN DATAFRAME #############

def transListToDataFr(lista):
    df = pd.DataFrame(lista,columns=['INCI_PK_PICO','INCI_I_GRAVEDAD'],index=None)
    return df


######################### TEST ###############################################


listaAgrupaciones = listaDeListasRes()

dataF = transListToDataFr(listaAgrupaciones)
dataF.to_csv('PredAgrupaPKRepConGrD.csv')

print(listaDeListasRes())