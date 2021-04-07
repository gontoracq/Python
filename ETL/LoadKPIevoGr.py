# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import itertools
from itertools import repeat

import os
import csv
#loading dataset
df = pd.read_csv('kjb37g4ib395h45jb23957g45ijb97', sep=';')

#######################  SUPER METODO QUE NOS CUENTA LAS VECES QUE SE CAMBIA DE GRAVEDAD DE CADA TIPO SEGÚN PK  ############################

# Hay que saber a que cambio de gravedad corresponde un diccionario y otro
def cuentaCambios(df):
    
    tuplaX = ()
    tuplaY = ()
    dicOcurrencias00 = dict()
    dicOcurrencias01 = dict()
    dicOcurrencias02 = dict()
    dicOcurrencias10 = dict()
    dicOcurrencias11 = dict()
    dicOcurrencias12 = dict()
    dicOcurrencias20 = dict()
    dicOcurrencias21 = dict()
    dicOcurrencias22 = dict()
    
    cont00 = 0
    cont01 = 0
    cont02 = 0
    
    cont10 = 0
    cont12 = 0
    cont11 = 0
    
    cont20 = 0
    cont21 = 0
    cont22 = 0
    
    #Inicialización de las tuplas
    #tuplaX = (df['INCI_PK_PICO'][0],df['INCI_I_GRAVEDAD'][0])
    #tuplaY = (df['INCI_PK_PICO'][1],df['INCI_I_GRAVEDAD'][1])
    
    listaDic = []
    
    for i in range (0,len(df['INCI_PK_PICO'])-1):
      
        pkActual = df['INCI_PK_PICO'][i]
        
        tuplaX = (df['INCI_PK_PICO'][i],df['INCI_I_GRAVEDAD'][i])
        tuplaY = (df['INCI_PK_PICO'][i+1],df['INCI_I_GRAVEDAD'][i+1])
        
   
        if ((tuplaX[1] == 0 and tuplaY[1] == 0) and tuplaX[0] == tuplaY[0]):
                cont00 = cont00 + 1
                dicOcurrencias00[pkActual] = cont00
                if dicOcurrencias00 not in listaDic:
                    listaDic.append(dicOcurrencias00)    
        if(tuplaX[0] != tuplaY[0]):
            cont00 = 0
                
                
    for i in range (0,len(df['INCI_PK_PICO'])-1):
        
        pkActual = df['INCI_PK_PICO'][i]
        
        tuplaX = (df['INCI_PK_PICO'][i],df['INCI_I_GRAVEDAD'][i])
        tuplaY = (df['INCI_PK_PICO'][i+1],df['INCI_I_GRAVEDAD'][i+1])

        
        if ((tuplaX[1] == 0 and tuplaY[1] == 1) and tuplaX[0] == tuplaY[0]):
                cont01 = cont01 + 1
                dicOcurrencias01[pkActual] = cont01
                if dicOcurrencias01 not in listaDic:
                    listaDic.append(dicOcurrencias01)
        if(tuplaX[0] != tuplaY[0]):
            cont01 = 0


    
    for i in range (0,len(df['INCI_PK_PICO'])-1):
        
        pkActual = df['INCI_PK_PICO'][i]
        
        tuplaX = (df['INCI_PK_PICO'][i],df['INCI_I_GRAVEDAD'][i])
        tuplaY = (df['INCI_PK_PICO'][i+1],df['INCI_I_GRAVEDAD'][i+1])

        
        if ((tuplaX[1] == 0 and tuplaY[1] == 2) and tuplaX[0] == tuplaY[0]):
                cont02 = cont02 + 1
                dicOcurrencias02[pkActual] = cont01
                if dicOcurrencias02 not in listaDic:
                    listaDic.append(dicOcurrencias02)
        if(tuplaX[0] != tuplaY[0]):
            cont02 = 0
            
            
    for i in range (0,len(df['INCI_PK_PICO'])-1):
        
        pkActual = df['INCI_PK_PICO'][i]
        
        tuplaX = (df['INCI_PK_PICO'][i],df['INCI_I_GRAVEDAD'][i])
        tuplaY = (df['INCI_PK_PICO'][i+1],df['INCI_I_GRAVEDAD'][i+1])

        
        if ((tuplaX[1] == 1 and tuplaY[1] == 0) and tuplaX[0] == tuplaY[0]):
                cont10 = cont10 + 1
                dicOcurrencias10[pkActual] = cont10
                if dicOcurrencias10 not in listaDic:
                    listaDic.append(dicOcurrencias10)
        if(tuplaX[0] != tuplaY[0]):
            cont10 = 0
            
    
    for i in range (0,len(df['INCI_PK_PICO'])-1):
        
        pkActual = df['INCI_PK_PICO'][i]
        
        tuplaX = (df['INCI_PK_PICO'][i],df['INCI_I_GRAVEDAD'][i])
        tuplaY = (df['INCI_PK_PICO'][i+1],df['INCI_I_GRAVEDAD'][i+1])

        
        if ((tuplaX[1] == 1 and tuplaY[1] == 1) and tuplaX[0] == tuplaY[0]):
                cont12 = cont12 + 1
                dicOcurrencias12[pkActual] = cont12
                if dicOcurrencias12 not in listaDic:
                    listaDic.append(dicOcurrencias12)
        if(tuplaX[0] != tuplaY[0]):
            cont12 = 0
            
            
    for i in range (0,len(df['INCI_PK_PICO'])-1):
        
        pkActual = df['INCI_PK_PICO'][i]
        
        tuplaX = (df['INCI_PK_PICO'][i],df['INCI_I_GRAVEDAD'][i])
        tuplaY = (df['INCI_PK_PICO'][i+1],df['INCI_I_GRAVEDAD'][i+1])

        
        if ((tuplaX[1] == 1 and tuplaY[1] == 2) and tuplaX[0] == tuplaY[0]):
                cont11 = cont11 + 1
                dicOcurrencias11[pkActual] = cont11
                if dicOcurrencias11 not in listaDic:
                    listaDic.append(dicOcurrencias11)
        if(tuplaX[0] != tuplaY[0]):
            cont11 = 0
            
            
    for i in range (0,len(df['INCI_PK_PICO'])-1):
        
        pkActual = df['INCI_PK_PICO'][i]
        
        tuplaX = (df['INCI_PK_PICO'][i],df['INCI_I_GRAVEDAD'][i])
        tuplaY = (df['INCI_PK_PICO'][i+1],df['INCI_I_GRAVEDAD'][i+1])

        
        if ((tuplaX[1] == 2 and tuplaY[1] == 0) and tuplaX[0] == tuplaY[0]):
                cont20 = cont20 + 1
                dicOcurrencias20[pkActual] = cont20
                if dicOcurrencias20 not in listaDic:
                    listaDic.append(dicOcurrencias20)
        if(tuplaX[0] != tuplaY[0]):
            cont20 = 0
            
    
    for i in range (0,len(df['INCI_PK_PICO'])-1):
        
        pkActual = df['INCI_PK_PICO'][i]
        
        tuplaX = (df['INCI_PK_PICO'][i],df['INCI_I_GRAVEDAD'][i])
        tuplaY = (df['INCI_PK_PICO'][i+1],df['INCI_I_GRAVEDAD'][i+1])

        
        if ((tuplaX[1] == 2 and tuplaY[1] == 1) and tuplaX[0] == tuplaY[0]):
                cont21 = cont21 + 1
                dicOcurrencias21[pkActual] = cont21
                if dicOcurrencias21 not in listaDic:
                    listaDic.append(dicOcurrencias21)
        if(tuplaX[0] != tuplaY[0]):
            cont21 = 0
            
        
    for i in range (0,len(df['INCI_PK_PICO'])-1):
        
        pkActual = df['INCI_PK_PICO'][i]
        
        tuplaX = (df['INCI_PK_PICO'][i],df['INCI_I_GRAVEDAD'][i])
        tuplaY = (df['INCI_PK_PICO'][i+1],df['INCI_I_GRAVEDAD'][i+1])

        
        if ((tuplaX[1] == 2 and tuplaY[1] == 2) and tuplaX[0] == tuplaY[0]):
                cont22 = cont22 + 1
                dicOcurrencias22[pkActual] = cont22
                if dicOcurrencias22 not in listaDic:
                    listaDic.append(dicOcurrencias22)
        if(tuplaX[0] != tuplaY[0]):
            cont22 = 0


    return listaDic


def cuentaCambiosPro(df):
    
    df_new = pd.DataFrame(columns=['INCI_PK_PICO','DE_0_A_0','DE_0_A_1','DE_0_A_2','DE_1_A_0','DE_1_A_1','DE_1_A_2','DE_2_A_0','DE_2_A_1','DE_2_A_2'])

    tuplaX = ()
    tuplaY = ()
    
    for i in range (0,len(df['INCI_PK_PICO'])-1):
      
        pkActual = df['INCI_PK_PICO'][i]
        
        tuplaX = (df['INCI_PK_PICO'][i],df['INCI_I_GRAVEDAD'][i])
        tuplaY = (df['INCI_PK_PICO'][i+1],df['INCI_I_GRAVEDAD'][i+1])
        
   
        if ((tuplaX[1] == 0 and tuplaY[1] == 0) and tuplaX[0] == tuplaY[0]):
            list00 = pd.Series([pkActual,1,0,0,0,0,0,0,0,0],index=df_new.columns)
            df_new.loc[i] = list00

        elif ((tuplaX[1] == 0 and tuplaY[1] == 1) and tuplaX[0] == tuplaY[0]):
            list01 = pd.Series([pkActual,0,1,0,0,0,0,0,0,0],index=df_new.columns)
            df_new.loc[i] = list01
        
        elif ((tuplaX[1] == 0 and tuplaY[1] == 2) and tuplaX[0] == tuplaY[0]):
            list02 = pd.Series([pkActual,0,0,1,0,0,0,0,0,0],index=df_new.columns)
            df_new.loc[i] = list02

        elif ((tuplaX[1] == 1 and tuplaY[1] == 0) and tuplaX[0] == tuplaY[0]):
            list10 = pd.Series([pkActual,0,0,0,1,0,0,0,0,0],index=df_new.columns)
            df_new.loc[i] = list10 

        elif ((tuplaX[1] == 1 and tuplaY[1] == 1) and tuplaX[0] == tuplaY[0]):
            list11 = pd.Series([pkActual,0,0,0,0,1,0,0,0,0],index=df_new.columns)
            df_new.loc[i] = list11

        elif ((tuplaX[1] == 1 and tuplaY[1] == 2) and tuplaX[0] == tuplaY[0]):
            list12 = pd.Series([pkActual,0,0,0,0,0,1,0,0,0],index=df_new.columns)
            df_new.loc[i] = list12

        elif ((tuplaX[1] == 2 and tuplaY[1] == 0) and tuplaX[0] == tuplaY[0]):
            list20 = pd.Series([pkActual,0,0,0,0,0,0,1,0,0],index=df_new.columns)
            df_new.loc[i] = list20

        elif ((tuplaX[1] == 2 and tuplaY[1] == 1) and tuplaX[0] == tuplaY[0]):
            list21 = pd.Series([pkActual,0,0,0,0,0,0,0,1,0],index=df_new.columns)
            df_new.loc[i] = list21

        elif ((tuplaX[1] == 2 and tuplaY[1] == 2) and tuplaX[0] == tuplaY[0]):
            list22 = pd.Series([pkActual,0,0,0,0,0,0,0,0,1],index=df_new.columns)
            df_new.loc[i] = list22

    df_new = df_new.groupby(['INCI_PK_PICO'],as_index=False).sum()
    df_new.to_csv('exportOrdenado2.csv',index=False,encoding='utf-8-sig',sep=';')
    
    return df_new


#############################  FIN DE SUPER METODO  #################################
def transListToDataFr(lista):
    df = pd.DataFrame.from_dict([(i, j) for a in lista for i, j in a.items()])
    return df

def transListToDataFr1(lista):

    dictlist = []
    for i in lista:
        for key, value in i.items():
            res = [key,value]
            dictlist.append(res)
    print(dictlist)
    df = pd.DataFrame(dictlist)
    return df

#,columns=[x.keys() for x in range (0,len(dictlist))]
                        
#print(cuentaCambios(df))
#dataF = transListToDataFr(cuentaCambios(df))
#dataF.transpose()

#dataF = pd.DataFrame.from_dict(transListToDataFr(cuentaCambios(df)), orient='columns', dtype=None)
#dataF.to_csv('exportOrdenado1.csv',encoding='utf-8-sig')

print(cuentaCambiosPro(df))