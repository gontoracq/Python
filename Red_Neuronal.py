# -*- coding: utf-8 -*-
#-------------------------------------------------------------#
#---------------------RED NEURONAL----------------------------#
#-------------------------------------------------------------#
#Hay que permitir que haya pesos negativos

import numpy as np
from copy import deepcopy

class RedNeuronal:
    
    
    def __init__(self, neuronas_entrada, neuronas_oculta1, neuronas_oculta2, neuronas_salida):
         
        self._n_entrada = neuronas_entrada
        self._n_oculta1 = neuronas_oculta1
        self._n_oculta2 = neuronas_oculta2
        self._n_salida = neuronas_salida
         
        #Se definen los pesos de manera aleatoria
        #Con rand generamos una matriz con valores entre 0 y 1
        #Primer parametro filas, segundo columnas
        self._w1 = np.random.rand(self._n_entrada, self._n_oculta1)
        self._w2 = np.random.rand(self._n_oculta1, self._n_oculta2)
        self._w3 = np.random.rand(self._n_oculta2, self._n_salida)
        
         
    #X es la matriz de entradas
    #dot 
    
    def activacion(self,x):
                     
        self._z1 = np.dot(x, self._w1)
        self._a1 = self.sigmoid(self._z1)
        self._z2 = np.dot(self._a1, self._w2)
        self._a2 = self.sigmoid(self._z2)
        self._z3 = np.dot(self._a2, self._w3)
        
        
        salida = self.sigmoid(self._z3)
        
        return salida
        
    def sigmoid(self, z):
        return 1/(1+np.exp(-z))
    
    def pesosEnLista(self):
        wl1 = self._w1.tolist()
        wl2 = self._w2.tolist()
        wl3 = self._w3.tolist()
        
        res = []
        
        
        for i in range(48):
            for e in range(5):
                res.append(wl1[i][e])
        for x in range(5):
            for z in range(5):
                res.append(wl2[x][z])
        for w in range(5):
            res.append(wl3[w][0])
            
        return res
    
    
    def actualizaPesos(self,lista):
        l1 = []
        l2 = []
        l3 = []
        
        listaAux = lista
        
        for i in range(48):
            aux = []
            for e in range(5):
                x = listaAux[0]
                aux.append(x)
                listaAux.pop(0)
            l1.append(aux)
            
        self._w1 = l1
        
        for elem in range(5):
            aux = []
            for y in range(5):
                x = listaAux[0]
                aux.append(x)
                listaAux.pop(0)
            l2.append(aux)
            
        self._w2 = l2
            
        for elem in range(5):
            aux = []
            x = listaAux[0]
            aux.append(x)
            listaAux.pop(0)
            l3.append(aux)
            
        self._w3 = l3