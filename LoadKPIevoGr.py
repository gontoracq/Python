# -*- coding: utf-8 -*-
import pandas as pd
import itertools
from itertools import repeat
#loading dataset
df = pd.read_csv('C:/Users/gtorres/Desktop/Proyectos/DATA SCIENCE TREN/Scripts/agrupaPKRepConGrD.csv', sep=';')

#######################  SUPER METODO QUE NOS CUENTA LAS VECES QUE SE CAMBIA DE GRAVEDAD DE CADA TIPO SEGÚN PK  ############################


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
    
    tuplaX = (df['INCI_PK_PICO'][0],df['INCI_I_GRAVEDAD'][0])
    tuplaY = (df['INCI_PK_PICO'][1],df['INCI_I_GRAVEDAD'][1])
    
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

        
        if ((tuplaX[1] == 1 and tuplaY[1] == 1) and tuplaX[0] == tuplaY[0]):
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

        
        if ((tuplaX[1] == 1 and tuplaY[1] == 2) and tuplaX[0] == tuplaY[0]):
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

        
        if ((tuplaX[1] == 1 and tuplaY[1] == 1) and tuplaX[0] == tuplaY[0]):
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


#############################  FIN DE SUPER METODO  #################################
    
def transListToDataFr(lista):
    df = pd.DataFrame(lista)
    return df

                        
print(cuentaCambios(df))
dataF = transListToDataFr(cuentaCambios(df))
dataF.to_csv('exportOrdenado.csv',encoding='utf-8-sig')