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

#loading dataset
ruta = 'kjbf94kjb4398t34k'
train_df = pd.read_excel(ruta)

    
import itertools
from itertools import repeat


#########  METODOS PARA CEAR LA LISTA CON LOS PK REPETIDOS Y SUS RESPECTIVAS GRAVEDADES  Y FECHAS  ##########

margen = 0.05
listaPK = []
listaSolDate = []
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
    
    for i in range (0,len(train_df)):
        listaAux.append(train_df['INCI_PK_PICO'].iloc[i])
    
    for j in range (len(listaAux)):
        k = j+1
        while k < len(listaAux)-1:
            if (igualConMargen(listaAux[j], listaAux[k],margen) and train_df['DTR_IA_ID'].iloc[j] == train_df['DTR_IA_ID'].iloc[k]):
                if(listaAux[j] not in listaPK):
                    listaPK.append(round(listaAux[j], 4))
                    listaSolGr.append(train_df['INCI_I_GRAVEDAD'].iloc[j])
                    listaSolDate.append(train_df['SES_D_INICIO'].iloc[j])
                listaPK.append(round(listaAux[k],4))
                listaSolGr.append(train_df['INCI_I_GRAVEDAD'].iloc[k])
                listaSolDate.append(train_df['SES_D_INICIO'].iloc[k])
                del listaAux[k]
            if listaAux[j] - listaAux[k] > margen:
                break
            k=k+1

rellenaListas()

def listaDeListasRes():

    listaRes=[[]]

    for i in range (0,len(listaSolGr)):
        listaRes.append([listaPK[i],listaSolGr[i],listaSolDate[i]])
    del listaRes[0]
    return listaRes

######## METODO PARA PASAR A UN DATAFRAME #############

def transListToDataFr(lista):
    df = pd.DataFrame(lista,columns=['INCI_PK_PICO','INCI_I_GRAVEDAD','SES_D_INICIO'],index=None)
    return df

#######  METODO QUE NOS CUENTA LAS VECES QUE SE CAMBIA DE GRAVEDAD DE CADA TIPO SEGÚN PK  #############

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

######################### MAIN ###############################################

def main():

    listaAgrupaciones = listaDeListasRes()

    dataF = transListToDataFr(listaAgrupaciones)
    dataF.sort_values(['INCI_PK_PICO', 'SES_D_INICIO'], ascending=[1, 1])
    dataF.to_csv('agrupaPKRepConGrD.csv', index=False, sep=';')
    ruta = 'jn45834h5on3l4jkn386'
    df = pd.read_csv(ruta, sep=';')
    cuentaCambiosPro(df)

main()

########  VAMOS A CREAR UNA GRÁFICA DE TIPO PIECHART PARA VER LA EVOLUCIÓN DE LAS GRAVEDADES  ########

#loading dataset
ruta2 = 'lkj4n593485n4l350ij'
data = pd.read_csv(ruta2, sep=';')
# import xlsxwriter module 
import xlsxwriter 
  
# Workbook() takes one, non-optional, argument   
# which is the filename that we want to create. 
workbook = xlsxwriter.Workbook('chart_pie.xlsx') 
  
# The workbook object is then used to add new   
# worksheet via the add_worksheet() method.  
worksheet = workbook.add_worksheet() 
  
# Create a new Format object to formats cells 
# in worksheets using add_format() method . 
  
# here we create bold format object . 
bold = workbook.add_format({'bold': 1}) 
  
# create a data list . 
headings = ['DE_0_A_0','DE_0_A_1','DE_0_A_2','DE_1_A_0','DE_1_A_1','DE_1_A_2','DE_2_A_0','DE_2_A_1','DE_2_A_2'] 

sum00 = data['DE_0_A_0'].sum()
sum01 = data['DE_0_A_1'].sum()
sum02 = data['DE_0_A_2'].sum()
sum10 = data['DE_1_A_0'].sum()
sum11 = data['DE_1_A_1'].sum()
sum12 = data['DE_1_A_2'].sum()
sum20 = data['DE_2_A_0'].sum()
sum21 = data['DE_2_A_1'].sum()
sum22 = data['DE_2_A_2'].sum()
  
# here we create a pie chart object . 
chart1 = workbook.add_chart({'type': 'pie'}) 

worksheet.write('B1', sum00)
worksheet.write('B2', sum01)
worksheet.write('B3', sum02)
worksheet.write('B4', sum10)
worksheet.write('B5', sum11)
worksheet.write('B6', sum12)
worksheet.write('B7', sum20)
worksheet.write('B8', sum21)
worksheet.write('B9', sum22)

worksheet.write('A1', 'DE_0_A_0')
worksheet.write('A2', 'DE_0_A_1')
worksheet.write('A3', 'DE_0_A_2')
worksheet.write('A4', 'DE_1_A_0')
worksheet.write('A5', 'DE_1_A_1')
worksheet.write('A6', 'DE_1_A_2')
worksheet.write('A7', 'DE_2_A_0')
worksheet.write('A8', 'DE_2_A_1')
worksheet.write('A9', 'DE_2_A_2')
  
# Add a data series to a chart 
# using add_series method. 
# Configure the first series. 
#[sheetname, first_row, first_col, last_row, last_col]. 
chart1.add_series({ 
    'name':       'Evolucion gravedad',
    'categories': ['Sheet1', 0, 0, 8, 0], 
    'values':     ['Sheet1', 0, 1, 8, 1], 
}) 
  
# Add a chart title  
chart1.set_title({'name': 'Evolucion gravedad'}) 
  
# Set an Excel chart style. Colors with white outline and shadow. 
chart1.set_style(10) 
  
# Insert the chart into the worksheet(with an offset). 
# the top-left corner of a chart is anchored to cell C2.  
worksheet.insert_chart('C2', chart1, {'x_offset': 25, 'y_offset': 10}) 
  
# Finally, close the Excel file   
# via the close() method.   
workbook.close()  
