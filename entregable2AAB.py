# -*- coding: utf-8 -*-
#=====================================================================
# IA: Ejercicio 2 entregable para el grupo 2 de IA (TI)
# Algoritmos geneticos
# Dpto. de C. de la Computacion e I.A. (Univ. de Sevilla)
#=====================================================================

# PROFESOR: Ignacio Perez Hurtado de Mendoza
# perezh at us dot es
#ALUMNO:  Gonzalo Torres-Quevedo Acquaroni (gontoracq)

#=====================================================================
# FRAMEWORK DE ALGORITMOS GENETICOS
#=====================================================================
# En este ejercicio vamos a sacar partido de la programacion orientada a objetos
# y hacer uso de algunos patrones de disenyo para hacer un software de calidad.

# Que es un patron de disenyo?
# https://en.wikipedia.org/wiki/Software_design_pattern

# Los patrones que usaremos seran los siguientes:
# Singleton pattern: https://en.wikipedia.org/wiki/Singleton_pattern
# Strategy pattern: https://en.wikipedia.org/wiki/Strategy_pattern

# No hace falta tener conocimiento previo de patrones de disenyo, pero se recomienda
# revisar los enlaces anteriores. El ejercicio va a estar guiado punto a punto
# y solo habra que completar codigo. El objetivo de este ejercicio es aprender
# a crear un framework en Python para algoritmos geneticos y resolver un problema interesante. 
# Dicho sea de paso, tener conocimiento de patrones de disenyo es algo muy importante 
# de cara al mercado laboral, asi que aprovechad este ejercicio para tener una experiencia
# practica en Python.

# Empezamos?

#=====================================================================

# PRIMERA PARTE: DEFINICION DE CLASES Y METODOS [5 puntos]

#=====================================================================

# Necesitaremos el modulo random:
import random

# Necesitaremos el modulo time para medir tiempos:
import time

# Necesitaremos math para alguna funcion
import math

#======================================================================
# Vamos a definir una clase Cromosoma para codificar el genotipo de un individuo

class Cromosoma(object):
    
    # Constructor que recibe un cromosoma como lista de genes y crea el objeto de tipo cromosoma
    def __init__(self,cromosoma):
        if (not isinstance(cromosoma,list)): # Primeramente miramos si el cromosoma que nos han pasado es una lista
            raise Exception("Error: el cromosoma debe venir representado como lista")
        if (len(cromosoma)==0): # El cromosoma debe tener al menos un elemento
            raise Exception("Error: la longitud del cromosoma es cero")
        self.__cromosoma = cromosoma # Los atributos que empiezan por dos guiones bajos son privados, ojo se esta pasando la lista por referencia
        self.__valor = None # Este es el valor de fitness del cromosoma, inicialmente vacio
        
        
    def evalua(self,fitness): # metodo que recibe una funcion de fitness y actualiza el valor del cromosoma
        self.__valor = fitness(self.__cromosoma)    
        
        
    def getGen(self,i):
       return self.__cromosoma[i]
    
    
    @property
    def valor(self):
        return self.__valor;
     
    @property
    def cromosoma(self):
        return self.__cromosoma

    @property
    def longitud(self):
        return len(self.__cromosoma)

    def setGen(self,i,gen): # Esta funcion cambia un gen del cromosoma
        self.__cromosoma[i] = gen

    def __str__(self): # Este metodo genera una cadena de texto para el cromosoma, es como toString de Java
        cad = str(self.__cromosoma)
        if (self.__valor != None):
            cad += " " + str(self.__valor)
        return cad
        
    def __repr__(self): # Este metodo es necesario para imprimir por pantalla el cromosoma
        return self.__str__()

#========================================================================
# EJEMPLOS:

# >> cr1 = Cromosoma([1,0,1,1,1,0,1,0,0,1])
# >> cr1
# [1, 0, 1, 1, 1, 0, 1, 0, 0, 1]
# >> cr1.longitud
# 10
# >> cr1.getGen(4)
# 1
# >> cr1.setGen(4,0)
# >> cr1.getGen(4)
# 0
# >> cr1
# [1, 0, 1, 1, 0, 0, 1, 0, 0, 1]

def binario_a_decimal(x):
    return sum(b*(2**i) for (i,b) in enumerate(x)) 
    

def fitness1(cromosoma):
    x = binario_a_decimal(cromosoma)
    return x**2

# >> cr1.evalua(fitness1)
# >> cr1.valor
# 346921

#===========================================================================

# Definimos una clase Poblacion como un wrapper sobre una lista de individuos, esto
# nos vendra bien si luego queremos anyadir mas atributos, como la suma total del fitness de los individuos
# Python permite anyadir atributos a un objeto de forma dinamica

class Poblacion(object):
    def __init__(self,individuos):
        if (not isinstance(individuos,list)): # Primeramente miramos si los individuos vienen como lista
            raise Exception("Error: los individuos deben venir definidos como lista")
        if (len(individuos)==0): # Debe haber almenos un individuo
            raise Exception("Error: poblacion vacia")
        self.individuos = individuos # Es un atributo publico
   
    def __str__(self): # Este metodo genera una cadena de texto para el cromosoma, es como toString de Java
        return str(self.individuos)
        
    def __repr__(self): # Este metodo es necesario para imprimir por pantalla el cromosoma
        return self.__str__()

#========================================================================
#EJEMPLOS:

# >> cr1 = Cromosoma([1,0,1,1,1,0,1,0,0,1])
# >> cr2 = Cromosoma([0,0,1,1,0,1,0,0,1,1])
# >> individuos = [cr1,cr2]
# >> poblacion = Poblacion(individuos)
# >> poblacion
# [[1, 0, 1, 1, 1, 0, 1, 0, 0, 1], [0, 0, 1, 1, 0, 1, 0, 0, 1, 1]]

#========================================================================
# Vamos a definir una clase DefinicionGenotipo para definir las caracteristicas del genotipo de un problema genetico, 
# es decir, la lista de genes y la longitud de individuos

class DefinicionGenotipo(object):
    # La clase DefinicionGenotipo recibe una lista de genes y la longitud de individuos    
    
    def __init__(self,genes,longitud):
        if (not isinstance(genes,list)): # Primeramente miramos si los genes que nos han pasado vienen como lista
            raise Exception("Error: los genes deben venir representados como lista")
        if (len(set(x for x in genes)) != len(genes)): # No pueden haber genes repetidos
            raise Exception("Error: hay genes repetidos")
        if (len(genes)<2): # Al menos necesitamos 2 genes diferentes
            raise Exception("Error: insuficientes genes")
        if (longitud<=0):
            raise Exception("Error: la longitud de individuos debe ser mayor o igual que cero")
        self.__genes = genes
        self.__longitud = longitud
   
    @property
    def genes(self):
        return self.__genes
    
    @property
    def longitud(self):
        return self.__longitud

    def __str__(self): 
        return ''.join(("genes: ",str(self.__genes),". Longitud de individuos: ",str(self.__longitud)))
        
    def __repr__(self):
        return self.__str__()


#===============================================================================
# EJEMPLOS:
       
# >> cuad_gen = DefinicionGenotipo([0,1],10)
# >> cuad_gen
# genes: [0, 1]. Longitud de individuos: 10


#==============================================================================
# Vamos a usar el patron Estrategia para definir diferentes estrategias de mutacion, para ello
# primero crearemos una clase abstracta EstrategiaMutacion que tiene un metodo "muta" que recibe un
# objeto de tipo Cromosoma, una probabilidad de mutacion, la definicion de un genotipo y realiza una mutacion 

# Strategy pattern: https://en.wikipedia.org/wiki/Strategy_pattern

class EstrategiaMutacion(object):

    def muta(self, cromosoma, prob, definicionGenotipo):  # Habra que implementar esta funcion en las clases heredadas
         raise NotImplementedError('EstrategiaMutacion es una clase abstracta!')

#=======================================================================

# A continuacion se implementa la mutacion en un punto (pagina 10 del tema 5)
# Usaremos el patron Singleton. Este codigo se proporciona como ejemplo para los siguientes ejercicios.

#https://es.wikipedia.org/wiki/Singleton

class MutacionEnUnPunto(EstrategiaMutacion):
    # Esto implementa el patron singleton    
    instance = None
    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance

    def muta(self, cromosoma, prob, definicionGenotipo): # Implementamos el metodo
       # d = list(definicionGenotipo.genes) #he puesto esto  par                                          AREGLO  EJ 9
        for i in range(cromosoma.longitud):
            if (random.random()<prob):
                cromosoma.setGen(i,random.sample(definicionGenotipo.genes,1)[0])


#=======================================================================
# EJEMPLOS:
# >> cuad_gen = DefinicionGenotipo([0,1],10)
# >> cr1 = Cromosoma([1,0,0,1,1,0,1,0,1,0])
# >> MutacionEnUnPunto().muta(cr1,0.2,cuad_gen)
# >> cr1
# [1, 0, 0, 1, 1, 0, 0, 0, 1, 0]
# >> MutacionEnUnPunto().muta(cr1,0.2,cuad_gen)
# >> cr1
# [0, 0, 0, 1, 1, 0, 0, 0, 1, 0]

#========================================================================
#print(cr1.cromosoma[2])
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>cr1.cromosoma[2],cr1.cromosoma[6] = cr1.cromosoma[6],cr1.cromosoma[2]
#print(cr1)
                
#EJERCICIO 1 [0.5 puntos]: Define la clase MutacionPorIntercambio, que debe heredar
# de EstrategiaMutacion, ser una clase singleton e implementar la mutacion 
# por intercambio (pagina 11 del tema 5). 
# Nota: Aplicar la mutacion solo si un numero entero al azar en [0,1) es menor que la probabilidad dada.


#=======================================================================
class MutacionPorIntercambio(EstrategiaMutacion):   
    instance = None
    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance

    def muta(self, cromosoma, prob, definicionGenotipo): # Implementamos el metodo
        esprimer = 0
        g2 = definicionGenotipo.genes[0] #para que no me de problemas por no definir fuera de if                ARREGLO EJ 9
        g1 = definicionGenotipo.genes[0]
        n1 = 0
        n2 = 0
        for i in range(cromosoma.longitud):
            if (random.random()<prob):
                if esprimer == 0:
                    g1= cromosoma.getGen(i)
                    n1 = i
                    esprimer = 1
                else :
                    n2 = i
                    g2 = cromosoma.getGen(i)
        cromosoma.setGen(n1, g2)
        cromosoma.setGen(n2, g1) 

#=======================================================================
# EJEMPLOS:

#ciudades =DefinicionGenotipo(['AL','CA','CO','GR','HU','MA','JA','SE',],8)
#cr1 = Cromosoma(['HU','SE','CA','MA','AL','CO','GR','JA'])
#print(cr1)
#MutacionPorIntercambio().muta(cr1,0.5,ciudades)
#print(cr1)
# ['HU', 'MA', 'CA', 'SE', 'AL', 'CO', 'GR', 'JA']
#MutacionPorIntercambio().muta(cr1,0.5,ciudades)
#print(cr1)
# ['CA', 'MA', 'HU', 'SE', 'AL', 'CO', 'GR', 'JA']

#========================================================================

#EJERCICIO 2 [0.5 puntos]: Define la clase MutacionPorMezcla, que debe heredar
# de EstrategiaMutacion, ser una clase singleton e implementar la mutacion 
# por mezcla (pagina 11 del tema 5). 
# Nota: Aplicar la mutacion solo si un numero entero al azar en [0,1) es menor que la probabilidad
#a =  ['HU', 'MA', 'SE', 'GR', 'CA', 'AL', 'CO', 'JA']
#print(a)
#b = random.sample(a, len(a))
#print(b)
        
#    def setGen(self,i,gen): # Esta funcion cambia un gen del cromosoma
       # self.__cromosoma[i] = gen
        
class MutacionPorMezcla(EstrategiaMutacion):  
    instance = None    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance

    def muta(self, cromosoma, prob, definicionGenotipo): # Implementamos el metodo
        lis = []
        r = -1
        n = 0
        for i in range(cromosoma.longitud):                                                           
      #  for i in range(len(cromosoma)):                                                             #ARREGLO EJ 9
            if (random.random()<prob):
                lis.append(cromosoma.cromosoma[i])
        #        lis.append(cromosoma[i])                                                           #ARREGLO EJ 9
                if (r<0):
                    r = i
                    #print(r)
            elif (r!=-1):
                    break
        #print("****")            
        l = random.sample(lis, len(lis))
        s = r + len(l)
        #print(lis)
        #print(l)
        for i in range(r,s):
            cromosoma.setGen(i, l[n])
            n= n+1
            
#========================================================================
# EJEMPLOS:

#ciudades = DefinicionGenotipo(['AL','CA','CO','GR','HU','MA','JA','SE',],8)
#cr1 = Cromosoma(['HU','SE','CA','MA','AL','CO','GR','JA'])
#print(cr1)
#MutacionPorMezcla().muta(cr1,0.6,ciudades)
#print(cr1)
# ['HU','SE','CA','AL','MA','GR','CO','JA']
#MutacionPorMezcla().muta(cr1,0.6,ciudades)
#print(cr1)
# ['HU', 'MA', 'SE', 'GR', 'CA', 'AL', 'CO', 'JA']        
#========================================================================

# Vamos a usar el patron Estrategia tambien para definir diferentes estrategias de cruce, para ello
# primero crearemos una clase abstracta EstrategiaCruce que tiene un metodo "cruza" que recibe dos
# objetos de tipo Cromosoma y realiza un cruce devolviendo una lista de dos elementos con los dos
# cromosomas hijos.


class EstrategiaCruce(object):

    def cruza(self, cromosoma1, cromosoma2): # Habra que implementar esta funcion en las clases heredadas
         raise NotImplementedError('EstrategiaCruce es una clase abstracta!')

#=======================================================================

# A Continuacion se muestra como ejemplo la clase CruceEnUnPunto que implementa el cruce en un punto

class CruceEnUnPunto(EstrategiaCruce):
    # Esto implementa el patron singleton    
    instance = None
    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance

    def cruza(self, cromosoma1, cromosoma2):
        if (cromosoma1.longitud != cromosoma2.longitud):
            raise Exception("Error: Los cromosomas deben tener la misma longitud")
        pos=random.randrange(1,cromosoma1.longitud-1)
        l1= cromosoma1.cromosoma[:pos] + cromosoma2.cromosoma[pos:] 
        l2= cromosoma2.cromosoma[:pos] + cromosoma1.cromosoma[pos:] 
        return [Cromosoma(l1),Cromosoma(l2)]
        
        
#========================================================================
# EJEMPLOS:
# >> cr1 = Cromosoma([1,0,0,1,1,0,1,0,1,0])        
# >> cr2 = Cromosoma([0,0,1,0,0,1,1,1,0,1])        
# >> CruceEnUnPunto().cruza(cr1,cr2) 
# [[1, 0, 0, 1, 1, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1, 1, 1, 1, 0]]
# >> CruceEnUnPunto().cruza(cr1,cr2)
# [[1, 0, 1, 0, 0, 1, 1, 1, 0, 1], [0, 0, 0, 1, 1, 0, 1, 0, 1, 0]]

#=======================================================================
# EJERCICIO 3  [1 punto]: Define la clase CruceBasadoEnOrden, que debe heredar
# de EstrategiaCruce, ser una clase singleton e implementar el cruce basado
# en orden (pagina 13 del tema 5). 
     
class CruceBasadoEnOrden(EstrategiaCruce):
    instance = None
    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance

    def cruza(self, cromosoma1, cromosoma2):
        if (cromosoma1.longitud != cromosoma2.longitud):
            raise Exception("Error: Los cromosomas deben tener la misma longitud")
        pos1=random.randrange(0,cromosoma1.longitud-1)
        pos2=random.randrange(pos1,cromosoma1.longitud-1)
        #print(pos1)
        #print(pos2)
        l1 = []
        l2 = []
        for i in range(pos1,pos2+1):
            l1.append(cromosoma1.getGen(i))
            l2.append(cromosoma2.getGen(i))
        #print(l1)
        #print(l2)
        #print("****")
        res1= []
        res2= []
        n1 = 0
        n2 = 0
        f1 = []
        f2 = []
        for i in list(range(pos2+1,cromosoma1.longitud))+list(range(0,pos2+1)):
            if n1>=cromosoma1.longitud-pos2-1 and cromosoma2.cromosoma[i] not in l1 :
                res1.append(cromosoma2.cromosoma[i])
            elif cromosoma2.cromosoma[i] not in l1:
                f1.append(cromosoma2.cromosoma[i]) 
                n1 = n1 + 1
            
        for i in list(range(pos2+1,cromosoma1.longitud))+list(range(0,pos2+1)):
            if n2>=cromosoma1.longitud-pos2-1 and cromosoma1.cromosoma[i] not in l2 :
                res2.append(cromosoma1.cromosoma[i])
            elif cromosoma1.cromosoma[i] not in l2:
                f2.append(cromosoma1.cromosoma[i]) 
                n2 = n2 + 1
        resultado1 = []
        resultado2 = []
        if res1 != []:
            for i in res1:
                resultado1.append(i)
        for i in l1:
            resultado1.append(i)
        if f1 != []:
            for i in f1:
                resultado1.append(i)
        #print(resultado1)
        if res2 != []:
            for i in res2:
                resultado2.append(i)
        for i in l2:
            resultado2.append(i)
        if f2 != []:
            for i in f2:
                resultado2.append(i)
        #print(resultado2)
       
        
        return [Cromosoma(resultado1),Cromosoma(resultado2)]
    
    
 #EJEMPLOS:
#cr1 = Cromosoma(['HU','SE','CA','MA','AL','CO','GR','JA'])
#cr2 = Cromosoma(['AL','CO','HU','SE','GR','CA','JA','MA'])  
#CruceBasadoEnOrden().cruza(cr1,cr2)
# [['SE', 'CA', 'JA', 'MA', 'AL', 'CO', 'GR', 'HU'],
#  ['MA', 'AL', 'CO', 'SE', 'GR', 'CA', 'JA', 'HU']]
#CruceBasadoEnOrden().cruza(cr1,cr2)        
# [['HU', 'SE', 'CA', 'GR', 'JA', 'MA', 'AL', 'CO'],
#  ['CA', 'CO', 'HU', 'MA', 'AL', 'GR', 'JA', 'SE']]
#======================================================================
# EJERCICIO 4 [1 punto]: Define la clase CruceBasadoEnCiclos, que debe heredar
# de EstrategiaCruce, ser una clase singleton e implementar el cruce basado
# en ciclos (pagina 15 del tema 5). 
# Nota1: Recuerda que puedes usar funciones auxiliares (opcional), pero respeta el paradigma
# de programacion orientada a objetos y encapsula las funciones auxiliares como
# funciones privadas de la clase.
# Nota2: Una funcion privada debe tener un nombre que comienza por dos guiones bajos.
  

#====================================================================
class CruceBasadoEnCiclos(EstrategiaCruce): 
    instance = None
    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance
    
    def __auxCiclo__(cromosoma1, cromosoma2, lis, i):
        lis.append(cromosoma2.cromosoma[i])
        a = cromosoma1.cromosoma.index(cromosoma2.cromosoma[i])
        if cromosoma2.cromosoma[a] in lis:
            #print (lis)
            return lis
        else:
            return CruceBasadoEnCiclos.__auxCiclo__(cromosoma1, cromosoma2, lis, a)
        
    def cruza(self, cromosoma1, cromosoma2):
        if (cromosoma1.longitud != cromosoma2.longitud):
            raise Exception("Error: Los cromosomas deben tener la misma longitud")
        res1 = []
        res2 = []
        lis = CruceBasadoEnCiclos.__auxCiclo__( cromosoma1, cromosoma2, [cromosoma1.cromosoma[0]], 0)
        #print(lis)
        for i in range(cromosoma1.longitud): 
            if cromosoma1.cromosoma[i] in lis :
                res1.append(cromosoma1.cromosoma[i])
            else:
                res1.append(cromosoma2.cromosoma[i])
        #print(res1)
        for i in range(cromosoma2.longitud): 
            if cromosoma2.cromosoma[i] in lis :
                res2.append(cromosoma2.cromosoma[i])
            else:
                res2.append(cromosoma1.cromosoma[i])
        return [Cromosoma(res1), Cromosoma(res2)]

#====================================================================
# EJEMPLOS:
#cr1 = Cromosoma(['HU','SE','CA','MA','AL','CO','GR','JA'])
#cr2 = Cromosoma(['JA','HU','GR','SE','AL','CA','CO','MA'])  
#print(CruceBasadoEnCiclos().cruza(cr1,cr2))
# [['HU', 'SE', 'GR', 'MA', 'AL', 'CA', 'CO', 'JA'],
#  ['JA', 'HU', 'CA', 'SE', 'AL', 'CO', 'GR', 'MA']]

#cr1 = Cromosoma([1,2,3,4,5,6,7,8,9])
#cr2 = Cromosoma([9,3,7,8,2,6,5,1,4])  
#print(CruceBasadoEnCiclos().cruza(cr1,cr2))
# [[1, 3, 7, 4, 2, 6, 5, 8, 9], [9, 2, 3, 8, 5, 6, 7, 1, 4]]


#=====================================================================
# Para generar individuos iniciales tambien usaremos el patron Estrategia,
# mediante la clase EstrategiaGenerador que tiene el metodo generaIndividuo
# que devuelve un individuo aleatorio inicial. Tambien tiene un metodo generaPoblacion
# que devuelve una poblacion inicial

class EstrategiaGenerador(object):
    def generaIndividuo(self, definicionGenotipo):  # Habra que implementar esta funcion en las clases heredadas
         raise NotImplementedError('EstrategiaGenerador es una clase abstracta!')
         
    def generaPoblacion(self, definicionGenotipo, tamPoblacion):
         individuos = [None]*tamPoblacion         
         for i in range(tamPoblacion):
            individuos[i] = self.generaIndividuo(definicionGenotipo)
         return Poblacion(individuos)
         
    def generaPoblacionEvaluada(self, definicionGenotipo, tamPoblacion, fitness):
         individuos = [None]*tamPoblacion         
         for i in range(tamPoblacion):
            individuos[i] = self.generaIndividuo(definicionGenotipo)
            individuos[i].evalua(fitness)
         return Poblacion(individuos)

#=====================================================================
# Como ejemplo, se incluye el codigo de la clase GeneradorConRepetidos (singleton), 
# que genera un individuo inicial aleatorio permitiendo genes repetidos

class GeneradorConRepetidos(EstrategiaGenerador):
    # Esto implementa el patron singleton    
    instance = None
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance
        
    def generaIndividuo(self, definicionGenotipo):
        l = [None]*definicionGenotipo.longitud
        for i in range(definicionGenotipo.longitud):
             l[i] = random.choice(definicionGenotipo.genes)
        return Cromosoma(l)

#=======================================================================
# Ejemplos:
#cuad_gen = DefinicionGenotipo([0,1],10)
#print(GeneradorConRepetidos().generaIndividuo(cuad_gen)) 
#  [1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
#print( GeneradorConRepetidos().generaIndividuo(cuad_gen) )
# [1, 0, 1, 0, 0, 0, 1, 1, 0, 1]
#print(GeneradorConRepetidos().generaPoblacion(cuad_gen,5) )
# [[1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
#  [0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
#  [0, 1, 1, 1, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 1, 1, 0, 1, 0, 0],
#  [1, 1, 0, 0, 1, 0, 1, 0, 1, 1]]

#print(GeneradorConRepetidos().generaPoblacionEvaluada(cuad_gen,5,fitness1))
# [[0, 0, 1, 0, 1, 1, 1, 0, 0, 1] 394384, 
#  [1, 0, 1, 0, 1, 0, 0, 0, 0, 0] 441,
#  [1, 0, 0, 1, 0, 0, 0, 1, 0, 0] 18769, 
#  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0] 74529, 
#  [0, 1, 0, 1, 1, 1, 0, 1, 1, 1] 910116]


#========================================================================
# EJERCICIO 5 [0.5 puntos]: Define la clase GeneradorPermutacion, que debe heredar de EstrategiaGenerador,
# ser una clase singleton e implementar la generacion de individuos como una permutacion
# aleatoria de la lista de genes. No se permiten genes repetidos 
class GeneradorPermutacion(EstrategiaGenerador):
    instance = None
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance
        
    def generaIndividuo(self, definicionGenotipo):
       # d = DefinicionGenotipo(definicionGenotipo.genes, definicionGenotipo.longitud)
        l = [None]*definicionGenotipo.longitud
        f = list(definicionGenotipo.genes)
        for i in range(definicionGenotipo.longitud):
             l[i] = random.choice(f)
             f.remove(l[i])
        #print(Cromosoma(l))
        return Cromosoma(l)
  
#========================================================================
# Ejemplos:
#ciudades = DefinicionGenotipo(['AL','CA','CO','GR','HU','MA','JA','SE'],8) 
#print(GeneradorPermutacion().generaIndividuo(ciudades))
#print(GeneradorPermutacion().generaIndividuo(ciudades))
# ['AL', 'CA', 'HU', 'GR', 'JA', 'SE', 'MA', 'CO']
#ciudades = DefinicionGenotipo(['AL','CA','CO','GR','HU','MA','JA','SE'],8)
#GeneradorPermutacion().generaIndividuo(ciudades)
# ['HU', 'JA', 'AL', 'MA', 'CO', 'CA', 'SE', 'GR']
#ciudades = DefinicionGenotipo(['AL','CA','CO','GR','HU','MA','JA','SE'],8) 
#print(GeneradorPermutacion().generaPoblacion(ciudades,5))
# [['CO', 'HU', 'SE', 'GR', 'MA', 'AL', 'JA', 'CA'],
#  ['CA', 'HU', 'AL', 'MA', 'CO', 'JA', 'GR', 'SE'],
#  ['CA', 'MA', 'JA', 'AL', 'HU', 'CO', 'SE', 'GR'],
#  ['HU', 'MA', 'CO', 'GR', 'SE', 'AL', 'JA', 'CA'],
#  ['MA', 'JA', 'CA', 'HU', 'SE', 'GR', 'AL', 'CO']]


#=======================================================================       
# Definamos ahora una clase Estrategia para los metodos de seleccion de individuos,
# esta clase tiene el metodo selecciona que recibe una poblacion EVALUADA (lista de cromosomas con su valor asignado)
# y devuelve un individuo de acuerdo al criterio de seleccion. Adicionalmente tiene el metodo
# seleccionaLista, que recibe una poblacion y un numero entero n (n >0), devolvera una
# lista de n individuos seleccionados.

class EstrategiaSeleccion(object):
    # Este metodo es opcional y prepara una poblacion para facilitar los calculos de 
    # de la seleccion de individuos. No poner codigo aqui, si hace falta se implementa
    # en las clases heredadas.      
    def preparaPoblacion(self, poblacionEvaluada):
        pass

    def selecciona(self, poblacionEvaluada):  # Habra que implementar esta funcion en las clases heredadas
        raise NotImplementedError('EstrategiaSeleccion es una clase abstracta!')
  
    def seleccionaLista(self, poblacionEvaluada, n):
        seleccion = [None]*n        
        for i in range(n):
            seleccion[i] = self.selecciona(poblacionEvaluada)
        return seleccion
    

#========================================================================
# EJERCICIO 6 [0.5 puntos]: Completar el codigo de la clase SeleccionTorneo.
# esta clase tiene dos atributos tamTorneo (K en los apuntes), para indicar el numero
# de individuos que se eligen aleatoriamente para participar en el torneo. Y opt
# que es la funcion max o min dependiendo de si queremos maximizar o minimizar
# Nota1: No es un singleton ya que tiene argumentos (tamTorneo y opt)
# Nota2: quitar la linea que pone pass e introducir vuestro codigo. 

class SeleccionTorneo(EstrategiaSeleccion):

    def __init__(self,tamTorneo,opt):
        self._tamTorneo = tamTorneo
        self._opt = opt
    
    @property
    def tamTorneo(self):
        return self._tamTorneo
        
    @property
    def opt(self):
        return self._opt
    
    def selecciona(self, poblacionEvaluada):
        p = list(poblacionEvaluada.individuos)
        l = []
        for i in range(self.tamTorneo):
            r = random.choice(p)
            l.append(r)
            p.remove(r)
        #print(l)    
        #print(p)
        lis = []
        for i in l :
            n = i.valor
            lis.append(n)
        if self.opt == max :
            res = max(lis)
        else :
            res = min(lis)
        num = lis.index(res)
        resul = l[num]
       # print(resul)
        return resul
       

#===========================================================================
# EJEMPLO:
#cuad_gen = DefinicionGenotipo([0,1],10)
#poblacion = GeneradorConRepetidos().generaPoblacionEvaluada(cuad_gen,5,fitness1)
#print(poblacion)
# [[1, 0, 1, 1, 1, 1, 1, 0, 1, 1] 797449,
# [1, 1, 0, 0, 0, 1, 1, 1, 1, 1] 990025,
# [1, 1, 1, 1, 1, 0, 0, 0, 1, 1] 638401,
# [1, 0, 0, 0, 1, 1, 0, 1, 1, 0] 187489,
# [0, 0, 0, 1, 1, 0, 0, 1, 0, 0] 23104]

#print(SeleccionTorneo(4,min).selecciona(poblacion))
# [0, 0, 0, 1, 1, 0, 0, 1, 0, 0] 23104

#print(SeleccionTorneo(4,max).selecciona(poblacion))
# [1, 1, 0, 0, 0, 1, 1, 1, 1, 1] 990025

#print(SeleccionTorneo(3,min).seleccionaLista(poblacion,3))
# [[1, 0, 0, 0, 1, 1, 0, 1, 1, 0] 187489,
#  [1, 0, 0, 0, 1, 1, 0, 1, 1, 0] 187489,
#  [0, 0, 0, 1, 1, 0, 0, 1, 0, 0] 23104]

#=============================================================================
# EJERCICIO 7 [0.5 puntos]: Completar el codigo de la clase SeleccionRuleta que 
# hereda de EstrategiaSeleccion.
# Esta clase es un singleton y debe implementar el metodo selecciona, 
# tambien conocido como metodo proporcional a la valoracion
# Ver tema 5 (paginas 17-19)
# Nota: quitar la linea que pone pass e introducir vuestro codigo

class SeleccionRuleta(EstrategiaSeleccion):
  # Esto implementa el patron singleton    
    instance = None
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance    
    
    
    # El metodo preparaPoblacion calcula la suma total de todas las funciones de fitness
    # y tambien la suma acumulada. En python se pueden anyadir nuevos atributos a un objeto de forma dinamica
    # previamente ordena la poblacion de mayor a menor fitness para que las selecciones sean mas eficientes
    def preparaPoblacion(self,poblacionEvaluada):
        poblacionEvaluada.individuos.sort(key= lambda x : x.valor, reverse=True)
        suma = 0
        for individuo in poblacionEvaluada.individuos:
            suma+=individuo.valor
            individuo.sumaParcial = suma
        poblacionEvaluada.sumaTotal = suma
        

    #definir el metodo selecciona, tened en cuenta que podeis usar el atributo sumaTotal de la poblacion
    #y el atributo sumaParcial para cada individuo, pues la poblacion ya ha sido preparada antes de llamar a esta funcion
    def selecciona(self, poblacionEvaluada):
       # print(poblacionEvaluada.individuos)
        res = poblacionEvaluada.individuos[0] 
        st = int(poblacionEvaluada.sumaTotal)
       # print(st)
        n = random.choice(range(st))
       # print(n)
        for i in list(poblacionEvaluada.individuos):
            if ( i.sumaParcial > n):
                res = i
                break
        return(res)


#==================================================================
# EJEMPLO:
#cuad_gen = DefinicionGenotipo([0,1],10)
#poblacion = GeneradorConRepetidos().generaPoblacionEvaluada(cuad_gen,5,fitness1)
#print(poblacion)
# [[1, 0, 0, 0, 0, 1, 0, 0, 0, 0] 1089, 
#  [0, 0, 1, 0, 1, 1, 0, 1, 1, 0] 190096, 
#  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0] 74529,
#  [0, 1, 0, 0, 1, 0, 1, 1, 0, 0] 44100,
#  [0, 0, 0, 1, 1, 0, 0, 0, 1, 1] 627264]

#SeleccionRuleta().preparaPoblacion(poblacion)
#print(poblacion)  
# [[0, 0, 0, 1, 1, 0, 0, 0, 1, 1] 627264,
#  [0, 0, 1, 0, 1, 1, 0, 1, 1, 0] 190096,
#  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0] 74529,
#  [0, 1, 0, 0, 1, 0, 1, 1, 0, 0] 44100,
#  [1, 0, 0, 0, 0, 1, 0, 0, 0, 0] 1089]

#print(SeleccionRuleta().selecciona(poblacion))
# [0, 0, 0, 1, 1, 0, 0, 0, 1, 1] 627264

#print(SeleccionRuleta().selecciona(poblacion))
# [0, 1, 0, 0, 1, 0, 1, 1, 0, 0] 44100

#print(SeleccionRuleta().selecciona(poblacion))
# [0, 0, 0, 1, 1, 0, 0, 0, 1, 1] 627264

# >> SeleccionRuleta().selecciona(poblacion)
# [0, 0, 1, 0, 1, 1, 0, 1, 1, 0] 190096

#print(SeleccionRuleta().seleccionaLista(poblacion,3))
# [[0, 0, 0, 1, 1, 0, 0, 0, 1, 1] 627264,
# [0, 0, 1, 0, 1, 1, 0, 1, 1, 0] 190096,
# [0, 0, 0, 1, 1, 0, 0, 0, 1, 1] 627264]


#================================================================================
# EJERCICIO 8 [0.5 puntos]  Completar el codigo de la clase SeleccionElitista.
# esta clase tiene dos atributos propElite (numero real entre 0 y 1), para indicar
# la proporcion de individuos de la seleccion que perteneceran a la elite. Y opt
# que es la funcion max o min dependiendo de si queremos maximizar o minimizar
# Nota1: No es un singleton ya que tiene argumentos (propElite y opt)
# Nota2: quitar la linea que pone pass e introducir vuestro codigo.
# Nota3: Fijarse que aqui no implementamos el metodo selecciona sino seleccionaLista 

class SeleccionElitista(EstrategiaSeleccion):

    def __init__(self,propElite,opt):
        self.__propElite = propElite
        self.__opt = opt
    
    @property
    def propElite(self):
        return self.__propElite
        
    @property
    def opt(self):
        return self.__opt
    
     
    # El metodo preparaPoblacion ordena la poblacion de mejor a peor fitness 
    def preparaPoblacion(self,poblacionEvaluada):
        if (self.__opt == max):
            poblacionEvaluada.individuos.sort(key= lambda x : x.valor, reverse=True)
        else:
            poblacionEvaluada.individuos.sort(key= lambda x : x.valor)
    # Esta clase modifica el metodo seleccionaLista de la clase padre.
    # No es necesario implementar el metodo selecciona.
    # Elegir los primeros n*propEliteindividuos de la poblacion evaluada
 # Elegir aleatoriamente los restantes individuos de entre el resto 
    # (hasta completar n)
    # Mirar explicacion en pagina 20 del tema 5
    def seleccionaLista(self, poblacionEvaluada, n):
        pob = list(poblacionEvaluada.individuos)
        numP = int(self.propElite * n)
        res = []
        for i in range(numP):
            res.append(pob[0])
            pob.remove(pob[0])
        while len(res)<n:
            l = random.choice(pob)
            res.append(l)
            pob.remove(l)
        return res


#===============================================================================
#cuad_gen = DefinicionGenotipo([0,1],10)
#poblacion = GeneradorConRepetidos().generaPoblacionEvaluada(cuad_gen,5,fitness1)
# [[0, 0, 0, 0, 1, 0, 0, 1, 0, 1] 430336, 
#  [0, 1, 0, 0, 0, 0, 1, 0, 1, 1] 695556, 
#  [0, 0, 1, 0, 1, 0, 0, 1, 0, 0] 21904, 
#  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] 116281, 
#  [1, 0, 0, 1, 1, 1, 1, 1, 1, 0] 255025]


#SeleccionElitista(0.5,min).preparaPoblacion(poblacion)
#print(poblacion)
# [[0, 0, 1, 0, 1, 0, 0, 1, 0, 0] 21904, 
#  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] 116281, 
#  [1, 0, 0, 1, 1, 1, 1, 1, 1, 0] 255025, 
#  [0, 0, 0, 0, 1, 0, 0, 1, 0, 1] 430336,
#  [0, 1, 0, 0, 0, 0, 1, 0, 1, 1] 695556]

#print(SeleccionElitista(0.5,min).seleccionaLista(poblacion,4))
# [[0, 0, 1, 0, 1, 0, 0, 1, 0, 0] 21904,
# [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] 116281,
# [1, 0, 0, 1, 1, 1, 1, 1, 1, 0] 255025,
# [0, 1, 0, 0, 0, 0, 1, 0, 1, 1] 695556]

#print(SeleccionElitista(0.5,min).seleccionaLista(poblacion,4))
# [[0, 0, 1, 0, 1, 0, 0, 1, 0, 0] 21904,
# [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] 116281,
# [0, 1, 0, 0, 0, 0, 1, 0, 1, 1] 695556,
# [0, 0, 0, 0, 1, 0, 0, 1, 0, 1] 430336]



#================================================================================
# Vamos a definir la clase ProblemaGenetico incluyendo todo lo necesario:
# DefinicionGenotipo
# EstrategiaMutacion
# EstrategiaCruce
# EstrategiaGenerador
# EstrategiaSeleccion
# Funcion de fitness (igual que en la practica 5)
# Funcion decodifica (igual que en la practica 5)

class ProblemaGenetico(object):
    
    def __init__(self,definicionGenotipo, 
                      estrategiaMutacion, 
                      estrategiaCruce, 
                      estrategiaGenerador, 
                      estrategiaSeleccion,
                      fitness,
                      decodifica):

        self.definicionGenotipo = definicionGenotipo
        self.estrategiaMutacion = estrategiaMutacion
        self.estrategiaCruce = estrategiaCruce
        self.estrategiaGenerador = estrategiaGenerador
        self.estrategiaSeleccion = estrategiaSeleccion
        self.fitness = fitness
        self.decodifica = decodifica

    def muta(self,c,prob):
        self.estrategiaMutacion.muta(c,prob,self.definicionGenotipo)
   
    def cruza(self, c1, c2):
        return self.estrategiaCruce.cruza(c1,c2)
        
    def generaPoblacionInicial(self, tamPoblacion):
        return self.estrategiaGenerador.generaPoblacionEvaluada(self.definicionGenotipo,tamPoblacion,self.fitness)
    
    def preparaPoblacion(self,p):
        self.estrategiaSeleccion.preparaPoblacion(p)
        
    def seleccionaLista(self,p,n):
        return self.estrategiaSeleccion.seleccionaLista(p,n)

    def decodifica(self,c):
        return self.decodifica(c)
        
    def evalua(self,c):
        c.evalua(self.fitness)
      
    # Algoritmo genetico segun pseudocodigo de la pagina 22 del tema 5
      # Parametros: 
      # propCruce: proporcion de individuos que se van a cruzar (numero real en [0,1]
      # probMutar: probabilidad de mutacion (numero real en [0,1])
      # generaciones: numero de generaciones en el bucle principal (numero entero >0)
      # tamPoblacion: numero de individuos en la poblacion
      # opt: funcion "max" si estamos maximizando o "min" si estamos minimizando
      # Salida:
      # Una lista con el tiempo de ejecucion en segundos, 
      # el fenotipo y el valor del mejor individuo encontrado
    def ejecutaAlgoritmoGenetico(self,propCruce,probMutar,generaciones,tamPoblacion,opt):
        t0 = time.clock()
        poblacion = self.generaPoblacionInicial(tamPoblacion)
        individuosACruzar = int(round(propCruce * tamPoblacion))
        if (individuosACruzar%2!=0):
            individuosACruzar+=1
        individuosANoCruzar = tamPoblacion - individuosACruzar
        assert (individuosACruzar + individuosANoCruzar) == tamPoblacion
        for generacion in range(generaciones):
            self.preparaPoblacion(poblacion)
            p1 = self.seleccionaLista(poblacion,individuosACruzar)
            p2 = self.seleccionaLista(poblacion,individuosANoCruzar)
            random.shuffle(p1)
            for i in range (0,len(p1),2):
                hijos = self.cruza(p1[i],p1[i+1])
                p1[i] = hijos[0]
                p1[i+1] = hijos[1]
            p4 = p1 + p2
            for individuo in p4:
                self.muta(individuo,probMutar)
                self.evalua(individuo)
            poblacion.individuos = p4
        mejor = opt(poblacion.individuos,key=lambda x : x.valor)
        t1 = time.clock()
        return [t1-t0,self.decodifica(mejor.cromosoma),mejor.valor]
            
      
      
#===============================================================================
           
#EJEMPLO:

#cuad_gen1 = ProblemaGenetico(DefinicionGenotipo([0,1],10),MutacionEnUnPunto(),CruceEnUnPunto(),GeneradorConRepetidos(),SeleccionRuleta(),fitness1,binario_a_decimal)
#print(cuad_gen1.ejecutaAlgoritmoGenetico(0.6,0.1,500,100,max))
# [1.0463019999999972, 1023, 1046529]


#cuad_gen2 = ProblemaGenetico(DefinicionGenotipo([0,1],10),MutacionEnUnPunto(),CruceEnUnPunto(),GeneradorConRepetidos(),SeleccionTorneo(10,min),fitness1,binario_a_decimal)
#print(cuad_gen2.ejecutaAlgoritmoGenetico(0.6,0.1,500,100,min))  
# [1.5345849999999999, 0, 0]




#==================================================================================    
           
# SEGUNDA PARTE: EXPERIMENTACION  [5 puntos]
           
#==================================================================================

# PROBLEMA DEL VIAJANTE
# A continuacion se detallan las coordenadas cartesianas de 53 localizaciones en la ciudad de Berlin.

localizacion = [None]*53
localizacion[0]= (386.0, 825.0)
localizacion[1]= (565.0, 575.0)
localizacion[2]= (25.0, 185.0)
localizacion[3]= (345.0, 750.0)
localizacion[4]= (945.0, 685.0)
localizacion[5]= (845.0, 655.0)
localizacion[6]= (880.0, 660.0)
localizacion[7]= (25.0, 230.0)
localizacion[8]= (525.0, 1000.0)
localizacion[9]= (580.0, 1175.0)
localizacion[10]= (650.0, 1130.0)
localizacion[11]= (1605.0, 620.0)
localizacion[12]= (1220.0, 580.0)
localizacion[13]= (1465.0, 200.0)
localizacion[14]= (1530.0, 5.0)
localizacion[15]= (845.0, 680.0)
localizacion[16]= (725.0, 370.0)
localizacion[17]= (145.0, 665.0)
localizacion[18]= (415.0, 635.0)
localizacion[19]= (510.0, 875.0) 
localizacion[20]= (560.0, 365.0)
localizacion[21]= (300.0, 465.0)
localizacion[22]= (520.0, 585.0)
localizacion[23]= (480.0, 415.0)
localizacion[24]= (835.0, 625.0)
localizacion[25]= (975.0, 580.0)
localizacion[26]= (1215.0, 245.0)
localizacion[27]= (1320.0, 315.0)
localizacion[28]= (1250.0, 400.0)
localizacion[29]= (660.0, 180.0)
localizacion[30]= (410.0, 250.0)
localizacion[31]= (420.0, 555.0)
localizacion[32]= (575.0, 665.0)
localizacion[33]= (1150.0, 1160.0)
localizacion[34]= (700.0, 580.0)
localizacion[35]= (685.0, 595.0)
localizacion[36]= (685.0, 610.0)
localizacion[37]= (770.0, 610.0)
localizacion[38]= (795.0, 645.0)
localizacion[39]= (720.0, 635.0)
localizacion[40]= (760.0, 650.0)
localizacion[41]= (475.0, 960.0)
localizacion[42]= (95.0, 260.0)
localizacion[43]= (875.0, 920.0)
localizacion[44]= (700.0, 500.0)
localizacion[45]= (555.0, 815.0)
localizacion[46]= (830.0, 485.0)
localizacion[47]= (1170.0, 65.0)
localizacion[48]= (830.0, 610.0)
localizacion[49]= (605.0, 625.0)
localizacion[50]= (595.0, 360.0)
localizacion[51]= (1340.0, 725.0)
localizacion[52]= (1740.0, 245.0)


# Esta es la definicion del genotipo, en donde cada ciudad es un numero en [0,52]:

berlin_genetico = DefinicionGenotipo([gen for gen in range(0,53)],53)

# Usaremos una clase singleton para precomputar la matriz de distancias y tener disponibles
# todas las distancias sin que tener que calcular una y otra vez la distancia euclidea

class BerlinDistancias(object):
     # Esto implementa el patron singleton    
    instance = None
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
            cls.instance.__generaDistancias()
        return cls.instance

    def __calculaDistancia(self,i,j):
        return math.sqrt(sum([(a-b)**2 for (a,b) in zip(localizacion[i],localizacion[j])]))
    
    def __generaDistancias(self):
        self.__distancia = [[0 for x in range(len(localizacion))] for y in range(len(localizacion))] 
        self.__minDistancia = None
        self.__maxDistancia = None
        for i in range(len(localizacion)):
            self.__distancia[i][i] = 0.0
            for j in range (i+1,len(localizacion)):
                self.__distancia[i][j] = self.__calculaDistancia(i,j)
                self.__distancia[j][i] = self.__distancia[i][j]
                if (self.__maxDistancia==None or self.__distancia[j][i]>self.__maxDistancia):
                    self.__maxDistancia=self.__distancia[j][i]
                if (self.__minDistancia==None or self.__distancia[j][i]<self.__minDistancia):
                    self.__minDistancia=self.__distancia[j][i]   
                    
    # Devuelve la maxima distancia entre dos localizaciones
    @property
    def maxDistancia(self):
        return self.__maxDistancia
     
    # Devuelve la minima distancia entre dos localizaciones
    @property
    def minDistancia(self):
        return self.__minDistancia
      
    # Devuelve la distancia entre dos localizaciones    
    def distancia(self,i,j):
        return self.__distancia[i][j]
        
   
                            
#==============================================================================      
# EJEMPLOS        
    
#print( BerlinDistancias().distancia(4,2))
# 1047.091209016674
#print(BerlinDistancias().distancia(2,4))
#  1047.091209016674

#print(BerlinDistancias().distancia(2,2))
#  0.0

#print(BerlinDistancias().maxDistancia)
# 1716.049241717731

#print(BerlinDistancias().minDistancia)
#  15.0



#==============================================================================
# A continuacion proporcionamos la funcion berlinFitness1 que devuelve la distancia del recorrido
# codificado en un cromosoma que viene como lista de genes. No olvidar que la ultima ciudad conecta con la primera 
# Nota: cuando useis esta funcion en el algoritmo genetico, recordad que hay que minimizar

def berlinFitness1(c):               # MINIMIZAR
    distancia = 0.0
    for i in range(0,len(c)-1,2):
        distancia += BerlinDistancias().distancia(c[i],c[i+1])
    distancia+=BerlinDistancias().distancia(c[52],c[0])
    return distancia    

#==============================================================================
# EJEMPLOS:
# >> c1 = [x for x in range(0,53)]
# >> berlinFitness1(c1)
# 13066.991153587061

# >> c2 =  [x for x in range(0,53,2)] + [x for x in range(1,53,2)]
# >> berlinFitness1(c2)
# 14328.89331480243

#===============================================================================
# Proporcionamos tambien la funcion berlinFitnesss2 para maximizar, es decir devuelve
# un numero mas grande cuanto mas corto sea el recorrido.


def berlinFitness2(c):                #MAXIMIZAR
    return BerlinDistancias().maxDistancia * 53 - berlinFitness1(c)

#================================================================================
# EJEMPLOS:
# >> c1 = [x for x in range(0,53)]
# >> berlinFitness2(c1)
# 77883.61865745268

# >> c2 =  [x for x in range(0,53,2)] + [x for x in range(1,53,2)]
# >> berlinFitness2(c2)
#  76621.71649623732


#==============================================================================
# EJERCICIO 9 [5 puntos]: crear al menos 5 instancias de la clase ProblemaGenetico denominadas
# problemaBerlin1, problemaBerlin2, etc, con las siguientes caracteristicas (elegir a vuestro criterio):
# 1.- Usar la variable berlin_genetico como definicion del genotipo
# 2.- Elegir entre mutacion por intercambio y mutacion por mezcla como estrategia de mutacion
# 3.- Elegir entre cruce basado en orden y cruce basado en ciclos como estrategia de cruces
# 4.- Usar el generador de permutaciones como estrategia de generacion 
# 5.- Elegir entre seleccion por torneo, seleccion por ruleta o seleccion elitista como estrategia de seleccion
# 6.- Elegir la funcion de fitness adecuada entre berlinFitness1 y berlinFitness2 segun la estrategia de seleccion elegida
# 7.- Usar la funcion identidad como funcion decodifica (puede ser una funcion lambda)

# Los parametros de los algoritmos geneticos resultante son:
# 1.- Tamanyo de torneo (si procede). Valores interesantes: 1, 3, 5, 15, 20, 25, 30, 40, 53
# 2.- Proporcion de elite (si procede). Valores interesantes: 0.0, 0.2, 0.4, 0.6, 0.8, 1.0
# 3.- Proporcion de cruce. Valores interesantes: 0.0, 0.2, 0.4, 0.6, 0.8, 1.0
# 4.- Probabilidad de mutacion. Valores interesantes: 0.0, 0.01, 0.1, 0.2, 0.5, 0.8, 1.0
# 5.- Numero de generaciones. Valores interesantes: 100, 200, 500, 1000, 2000, 5000
# 6.- Tamanyo de la poblacion. Valores interesantes: 10, 50, 100, 500, 1000

# Nota: No todos los valores daran buenos resultados, pero son interesantes desde el punto 
# de vista de la comprension de los algoritmos geneticos.

# SE PIDE:

# Realizar al menos 5 ejecuciones del algoritmo genetico por cada instancia definida del problema (25 experimentos en total),
# variando los valores de los parametros del algoritmo en cada ejecucion,
# podeis tomar como referencia los valores interesantes que se mencinal (o elegir los valores que querais). 
# Para cada ejecucion se pide escribir lo siguiente (con comentarios en el propio codigo)

# 1.- Las estrategias del problema genetico (mutacion, cruce, seleccion)
# 2.- Decir que funcion de fitness se ha usado
# 3.- Los valores de los parametros utilizados en el algoritmo genetico 
# 4.- La deficinion de la variable problemaBerlin1
# 5.- La llamada al metodo ejecutaAlgoritmoGenetico.
# 6.- La salida del metodo ejecutaAlgoritmoGenetico.
# 7.- El tiempo de ejecucion y el valor de fitness de la mejor solucion obtenida
# 8.- Un parrafo CORTO de conclusiones sobre el resultado.


# SE VALORARA:
# a) La relevancia de las combinaciones de estrategias y parametros elegidos
# b) Buena organizacion y presentacion de los resultados, claridad y sintesis 
# c) Saber explicar que ocurre cuando se escogen valores extremos (probabilidad de mutacion 0 o 1 por ejemplo)
# d) Encontrar al menos una buena combinacion de estrategias y parametros que haga converger EN POCO TIEMPO al algoritmo al optimo global

# HAY UNA PLANTILLA PARA LA DOCUMENTACION AL FINAL DE ESTE DOCUMENTO



#prueba1 = ProblemaGenetico(DefinicionGenotipo([0,1],53),
#                              MutacionPorMezcla(),
#                              CruceBasadoEnCiclos(),
#                              GeneradorPermutacion(),
#                              SeleccionElitista(0.8, min),
#                              berlinFitness2,
#                              lambda x : x)
    
#print(prueba1.ejecutaAlgoritmoGenetico(0.6,0.1,500,100,min))  
# [1.5345849999999999, 0, 0]

# ejecutaAlgoritmoGenetico(self,propCruce,probMutar,generaciones,tamPoblacion,opt):

#prueba1.ejecutaAlgoritmoGenetico(0.6,0.2,10,53,min) 

#==================================================================================
# EJEMPLO (incluyendo documentacion):

# EXPERIMENTO NUMERO 0
# --------------------

# ESTRATEGIAS:
# Las estrategias de este ejemplo son:
# 1.- Mutacion por intercambio
# 2.- Cruce basado en orden
# 3.- Seleccion por torneo

# FITNESS:
# He usado la funcion berlinFitness1 como fitness

# PARAMETROS:
# Los parametros de este ejemplo son:
# 1.- Tamanyo de torneo = 30
# 2.- Proporcion de cruce = 0.6
# 3.- Probabilidad de mutacion = 0.2
# 4.- Numero de generaciones = 1000
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin0 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnOrden(),
#                                   GeneradorPermutacion(),
#                                   SeleccionTorneo(30,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
# problemaBerlin0.ejecutaAlgoritmoGenetico(0.6,0.2,1000,100,min) 
    
# SALIDA DEL ALGORITMO:
# Esta es la salida del algoritmo genetico:
#[11.667443000000006,
# [7,
#  42,
#  6,
#  15,
#  50,
#  20,
#  14,
#  52,
#  47,
#  26,
#  32,
#  49,
#  37,
#  38,
#  12,
#  28,
#  10,
#  9,
#  4,
#  25,
#  40,
#  39,
#  51,
#  11,
#  3,
#  0,
#  24,
#  5,
#  29,
#  16,
#  48,
#  46,
#  18,
#  31,
#  21,
#  17,
#  22,
#  1,
#  41,
#  8,
#  23,
#  30,
#  44,
#  34,
#  27,
#  13,
#  35,
#  36,
#  45,
#  19,
#  33,
#  43,
#  2],
# 3282.4725918022136]

# TIEMPO Y FITNESS:
# Ha tardado 11.66 segundos y el fitness de la mejor solucion es 3282.47

# CONCLUSIONES: 
# ...
# ...
# ...


#================================================================================================================
#                       RESPUESTAS DE GONZALO TORRES-QUEVEDO
#===============================================================================================================
# EXPERIMENTO NUMERO 1
#---------------------

# ESTRATEGIAS:
    #-Muacion por Mezcla
    #-Cruce basado en Ciclos
    #-Seleccion Elitista

# FITNESS: he usado berlinFitness1 ya que quiero minimizr para el Problema del Viajero

# PARAMETROS:
# 1.- Porcentaje elititsta = 1.0
# 2.- Proporcion de cruce = 0.2
# 3.- Probabilidad de mutacion = 0.5
# 4.- Numero de generaciones = 2000
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
#problemaBerlin1 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorMezcla(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(1.0,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
#print(problemaBerlin1.ejecutaAlgoritmoGenetico(0.2,0.5,2000,100,min))

# SALIDA DEL ALGORITMO:
#[8.750122303757962, [36, 35, 10, 33, 32, 19, 44, 49, 51, 11, 27, 28, 23, 25, 3, 41, 22,
# 16, 15, 34, 8, 38, 48, 9, 14, 52, 6, 5, 50, 30, 45, 21, 17, 29, 0, 37, 24, 20, 42, 2, 31,
# 46, 18, 1, 26, 7, 4, 43, 40, 12, 13, 47, 39], 9070.31294161445]

# TIEMPO Y FITNESS:
# Ha tardado 10.3 segundos y el fitness de la mejor solucion es 9070.31294161445

# CONCLUSIONES: 
    # Comparado con el ejempo dado ( experimento 0) veo que mi mejor fitness es mucho
    # mas alto y ya que estoy haciendo minimo, no deberia ser asi. 
    #Este valor se ve afectado por escoger un valor tan extremo en seleccion elitista
    
    
#=============================================================================

# EXPERIMENTO NUMERO 2
#---------------------

# ESTRATEGIAS:
    #-Muacion por Mezcla
    #-Cruce basado en Ciclos
    #-Seleccion Elitista

# FITNESS: he usado berlinFitness1 ya que quiero minimizr para resolver  el Problema del Viajero

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.8
# 2.- Proporcion de cruce = 0.6
# 3.- Probabilidad de mutacion = 0.5
# 4.- Numero de generaciones = 2000
# 5.- Tamanyo de poblacion = 500
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
#problemaBerlin1 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorMezcla(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.8,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
#print(problemaBerlin1.ejecutaAlgoritmoGenetico(0.6,0.5,2000,500,min)) 

# SALIDA DEL ALGORITMO:
#[59.64035111726844, [50, 20, 44, 40, 1, 22, 49, 32, 19, 45, 18, 
#3, 26, 14, 24, 33, 29, 47, 10, 41, 35, 36, 25, 4, 0, 8, 39, 5, 34,
# 6, 27, 13, 21, 31, 23, 30, 43, 9, 2, 7, 11, 51, 46, 37, 48, 38,
# 17, 42, 52, 28, 15, 12, 16], 5820.459390372824]

# TIEMPO Y FITNESS:
# Ha tardado 71.78 segundos y el fitness de la mejor solucion es 5820.459390372824

# CONCLUSIONES: 
# Ha tardado tanto ya que he puesto un tamaño de poblacion muy grande con muchas generaciones
# el fitness de la mejor solucon es mucho mejor al haber alejado de los extremos el porcentaje de 
#seleccion elitista. Creo que Mutacion por mezcla va muy bien con este problema.
#=============================================================================

# EXPERIMENTO NUMERO 3
#---------------------

# ESTRATEGIAS:
    #-Muacion por Mezcla
    #-Cruce basado en Ciclos
    #-Seleccion Elitista

# FITNESS: he usado berlinFitness1 ya que quiero minimizr para el Problema del Viajero

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.6
# 2.- Proporcion de cruce = 0.4
# 3.- Probabilidad de mutacion = 0.2
# 4.- Numero de generaciones = 1000
# 5.- Tamanyo de poblacion = 50
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
#problemaBerlin1 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorMezcla(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.6,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
#print(problemaBerlin1.ejecutaAlgoritmoGenetico(0.4,0.2,1000,50,min)) 

# SALIDA DEL ALGORITMO:
#[2.4828187452585553, [39, 40, 47, 26, 2, 36, 27, 52, 8, 0, 15, 6, 28, 12, 30,
# 49, 35, 24, 17, 21, 42, 7, 31, 23, 45, 18, 34, 32, 48, 38, 16, 11, 37, 44, 4, 46, 13, 51,
# 20, 10, 41, 3, 1, 50, 19, 33, 29, 14, 43, 9, 25, 5, 22], 8755.291453961003]

# TIEMPO Y FITNESS:
# Ha tardado 3.8 segundos y el fitness de la mejor solucion es 8755.291453961003

# CONCLUSIONES: 
#Se ha reducido muchisimo el tiempo al esoger un tamaño de poblacion tan pequeño, aunque puenso que demasiado pequeño
#ya que afecta al resultado. No es la unica razon ya que he cmbiado otros parametros que pienso que han empeorado el resultado
#com bajar la probabilidad de mitacion y la proporcion de cruce
#=============================================================================

# EXPERIMENTO NUMERO 4
#---------------------

# ESTRATEGIAS:
    #-Muacion por Mezcla
    #-Cruce basado en Ciclos
    #-Seleccion Elitista

# FITNESS: he usado berlinFitness1 ya que quiero minimizr para el Problema del Viajero

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.6
# 2.- Proporcion de cruce = 0.6
# 3.- Probabilidad de mutacion = 0.5
# 4.- Numero de generaciones = 1000
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
#problemaBerlin1 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorMezcla(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.4,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
#print(problemaBerlin1.ejecutaAlgoritmoGenetico(0.6,0.5,1000,100,min)) 

# SALIDA DEL ALGORITMO:
#[5.860388407083519, [15, 12, 34, 39, 32, 23, 14, 47, 51, 11, 44, 46, 25,
# 26, 42, 21, 17, 0, 16, 4, 52, 13, 35, 20, 10, 41, 33, 38, 3, 6, 19, 18, 9, 8, 43, 36, 
#45, 31, 5, 48, 49, 37, 1, 22, 40, 50, 2, 7, 29, 30, 27, 28, 24], 6984.481626350187]

# TIEMPO Y FITNESS:
# Ha tardado 5.8 segundos y el fitness de la mejor solucion es 6984.481626350187

# CONCLUSIONES: 
#Ha mejorado mucho el fitness de la mejor solucion, el tiempo ha sido rapido, todos los parametros son bastante centrales, 
# entre sus posibles valores. 
#=============================================================================
# EXPERIMENTO NUMERO 5
#---------------------

# ESTRATEGIAS:
    #-Muacion por Mezcla
    #-Cruce basado en Ciclos
    #-Seleccion Elitista

# FITNESS: he usado berlinFitness1 ya que quiero minimizr para el Problema del Viajero

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.6
# 2.- Proporcion de cruce = 0.6
# 3.- Probabilidad de mutacion = 0.5
# 4.- Numero de generaciones = 1000
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
#problemaBerlin1 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorMezcla(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.6,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
#print(problemaBerlin1.ejecutaAlgoritmoGenetico(0.6,0.5,1500,200,min)) 

# SALIDA DEL ALGORITMO:
#[17.3000108334345, [4, 43, 40, 38, 32, 36, 11, 52, 46, 37, 44, 50, 18, 2, 14,
# 13, 1, 34, 24, 25, 26, 27, 3, 19, 31, 17, 29, 20, 5, 15, 30, 21, 49, 35, 7, 42, 41, 10,
# 48, 47, 45, 39, 33, 51, 28, 12, 9, 22, 23, 16, 8, 0, 6], 6389.671906450081]

# TIEMPO Y FITNESS:
# Ha tardado 18.04 segundos y el fitness de la mejor solucion es 6389.671906450081

# CONCLUSIONES: 
#Ha mejorado un poco el fitness de la mejor solucion, esta vez he cambiado menos paramtros. 
#aumentar numero generaciones, tamaño poblacion ha aumentado mucho el tiempo respecto a la mejora del fitness
#aumentar el porcentaje elitista ha mejorado resultado pero mas alto empieza a empeorar resultado
#=============================================================================


# EXPERIMENTO NUMERO 6
#---------------------

# ESTRATEGIAS:
#  - Mutacion por Intercambio
#  - Cruce basado en ciclos
#  - Seleccion torneo

# FITNESS: he usado berlinFitness1 ya que quiero minimizr para resolver  el Problema del Viajero

# PARAMETROS:
# Los parametros de este ejemplo son:
# 1.- Tamanyo de torneo = 40
# 2.- Proporcion de cruce = 0.6
# 3.- Probabilidad de mutacion = 0.5
# 4.- Numero de generaciones = 1500
# 5.- Tamanyo de poblacion = 150
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin2 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionTorneo(40 ,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin2.ejecutaAlgoritmoGenetico(0.6,0.5,1500,150,min) )


# SALIDA DEL ALGORITMO:
#[40.724955668451, [24, 48, 27, 47, 33, 10, 43, 15, 31, 22, 30, 26, 2, 7, 52, 14, 
#5, 4, 17, 19, 34, 18, 6, 23, 28, 46, 13, 1, 29, 16, 12, 11, 20, 8, 9, 35, 40, 36,
# 44, 32, 51, 25, 37, 50, 42, 21, 49, 39, 41, 45, 0, 3, 38], 8516.130264301182]


# TIEMPO Y FITNESS:
# Ha tardado 36.1 segundos y el fitness de la mejor solucion es 8516.130264301182

# CONCLUSIONES: 
#Selecciona torneo ha aumentado el tiempo de ejecucion, comparado con experimento 0
#sigue siendo un fitness muy elevado 
    
    
#=============================================================================

# EXPERIMENTO NUMERO 7
#---------------------

# ESTRATEGIAS:
#  - Mutacion por Intercambio
#  - Cruce basado en ciclos
#  - Seleccion torneo

# FITNESS: he usado berlinFitness1 ya que quiero minimizr para resolver  el Problema del Viajero

# PARAMETROS:
# Los parametros de este ejemplo son:
# 1.- Tamanyo de torneo = 20
# 2.- Proporcion de cruce = 0.8
# 3.- Probabilidad de mutacion = 0.8
# 4.- Numero de generaciones = 1500
# 5.- Tamanyo de poblacion = 150
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin2 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionTorneo(20 ,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin2.ejecutaAlgoritmoGenetico(0.8,0.8,1500,150,min) )


# SALIDA DEL ALGORITMO:
#[40.724955668451, [24, 48, 27, 47, 33, 10, 43, 15, 31, 22, 30, 26, 2, 7, 52, 14, 
#5, 4, 17, 19, 34, 18, 6, 23, 28, 46, 13, 1, 29, 16, 12, 11, 20, 8, 9, 35, 40, 36,
# 44, 32, 51, 25, 37, 50, 42, 21, 49, 39, 41, 45, 0, 3, 38], 8516.130264301182]


# TIEMPO Y FITNESS:
# Ha tardado 31.68 segundos y el fitness de la mejor solucion es 8516.130264301182

# CONCLUSIONES: 
#Reducir el tamaño de torneo en Selecciona torneo  ha reducido un poco el tiempo de ejecucion
#El mejor fitness ha aumentado al acercar la prop. cruce y prob. muacion a sus extremos
    
    
#=============================================================================

# EXPERIMENTO NUMERO 8
#---------------------

# ESTRATEGIAS:
#  - Mutacion por Intercambio
#  - Cruce basado en ciclos
#  - Seleccion torneo

# FITNESS: he usado berlinFitness1 ya que quiero minimizr para resolver  el Problema del Viajero

# PARAMETROS:
# Los parametros de este ejemplo son:
# 1.- Tamanyo de torneo = 30
# 2.- Proporcion de cruce = 0.4
# 3.- Probabilidad de mutacion = 0.2
# 4.- Numero de generaciones = 1500
# 5.- Tamanyo de poblacion = 150
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin2 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionTorneo(30 ,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin2.ejecutaAlgoritmoGenetico(0.4,0.2,1500,150,min) )


# SALIDA DEL ALGORITMO:
#[31.428536403189355, [34, 37, 2, 7, 51, 11, 13, 27, 44, 16, 52, 14, 32, 49, 40, 38, 8, 9, 46, 
#47, 19, 41, 23, 31, 25, 12, 28, 26, 15, 6, 29, 50, 43,
#45, 42, 21, 18, 17, 5, 4, 48, 24, 20, 30, 33, 10, 0, 3, 39, 36, 1, 22, 35], 4635.833734016538]


# TIEMPO Y FITNESS:
# Ha tardado 32.9 segundos y el fitness de la mejor solucion es 4635.833734016538

# CONCLUSIONES: 
#Mejor soucion hasta el momento. Mantener parametros en valores medios esta dando buenos resultados
#tiempo ejecucuon alto comparado con problemaBerlin1, creo que es debido a seleccion torneo
    
    
#=============================================================================

# EXPERIMENTO NUMERO 9
#---------------------

# ESTRATEGIAS:
#  - Mutacion por Intercambio
#  - Cruce basado en ciclos
#  - Seleccion torneo

# FITNESS: he usado berlinFitness1 ya que quiero minimizr para resolver  el Problema del Viajero

# PARAMETROS:
# Los parametros de este ejemplo son:
# 1.- Tamanyo de torneo = 30
# 2.- Proporcion de cruce = 0.4
# 3.- Probabilidad de mutacion = 0.4
# 4.- Numero de generaciones = 1000
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin2 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionTorneo(30 ,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin2.ejecutaAlgoritmoGenetico(0.4,0.4,1000,100,min) )


# SALIDA DEL ALGORITMO:
#[12.979063535232854, [27, 13, 5, 40, 8, 9, 49, 36, 20, 50, 34, 46, 39, 15, 22, 32, 
#10, 41, 25, 6, 37, 48, 29, 21, 16, 38, 12, 35, 0, 30, 7, 42, 24, 43, 
#18, 3, 4, 33, 52, 14, 23, 44, 26, 47, 1, 2, 31, 17, 51, 11, 45, 19, 28], 6441.741966092605]


# TIEMPO Y FITNESS:
# Ha tardado 13.55 segundos y el fitness de la mejor solucion es 6441.741966092605

# CONCLUSIONES: 
#Tiempo ha reducido mucho al reducir num. generaciones y tamaño poblacion
#Ademas de este cambio he aumentado un poco la prob. mutacion y resultado es peor
#mantendre porcentaje de mutacion mas cerca a 0 que 0.5
    
    
#=============================================================================


# EXPERIMENTO NUMERO 10
#---------------------

# ESTRATEGIAS:
#  - Mutacion por Intercambio
#  - Cruce basado en ciclos
#  - Seleccion torneo

# FITNESS: he usado berlinFitness1 ya que quiero minimizr para resolver  el Problema del Viajero

# PARAMETROS:
# Los parametros de este ejemplo son:
# 1.- Tamanyo de torneo = 40
# 2.- Proporcion de cruce = 0.4
# 3.- Probabilidad de mutacion = 0.2
# 4.- Numero de generaciones = 1000
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin2 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionTorneo(40 ,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin2.ejecutaAlgoritmoGenetico(0.4,0.2,1000,100,min) )


# SALIDA DEL ALGORITMO:
#[14.8003500909399, [37, 39, 51, 11, 29, 16, 32, 36, 6, 15, 44, 46, 20, 50,
# 8, 45, 42, 21, 22, 31, 52, 14, 38, 5, 12, 26, 41, 19, 28, 13, 4, 25, 18, 17, 27, 47, 10, 9,
# 49, 1, 24, 48, 35, 34, 23, 30, 0, 3, 33, 43, 2, 7, 40], 4116.123393334891]


# TIEMPO Y FITNESS:
# Ha tardado 15.54 segundos y el fitness de la mejor solucion es 4116.123393334891

# CONCLUSIONES: 
#Mejor fitness hasta ahora. en relacion a experimiento 8 (con fitness mas cercano):
#he reducidp numero de generaciones y tamaño de poblacion que ha reducido tiempo en la 1/2 aprox. y no ha empeorado res.
#he aumentado tamaño de torneo que ha mejorado solucion. 
    
    
#=============================================================================


# EXPERIMENTO NUMERO 11
#---------------------

# ESTRATEGIAS:
#  - Mutacion por mezcla
#  - Cruce basado en orden 
#  - Seleccion ruleta

# FITNESS: he usado berlinFitness2 

# PARAMETROS:
# Los parametros de este ejemplo son:
# .- Proporcion de cruce = 0.4
# .- Probabilidad de mutacion = 0.2
# .- Numero de generaciones = 1500
# .- Tamanyo de poblacion = 150
# .- Funcion "max" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin3 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorMezcla(),
#                                   CruceBasadoEnOrden(),
#                                   GeneradorPermutacion(),
#                                   SeleccionRuleta(),
#                                   berlinFitness2,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin3.ejecutaAlgoritmoGenetico(0.4,0.2,1500,150,max) )


# SALIDA DEL ALGORITMO:
#[18.395126095449086, [21, 0, 37, 45, 5, 15, 46, 20, 23, 40, 44, 12, 6, 8, 9, 19, 1,
# 18, 34, 28, 10, 43, 50, 7, 48, 11, 41, 38, 22, 30, 39, 2, 27, 32, 14, 52,
# 36, 24, 17, 31, 13, 26, 3, 49, 42, 29, 35, 16, 51, 47, 4, 33, 25], 79420.10154684729]


# TIEMPO Y FITNESS:
# Ha tardado 19.65 segundos y el fitness de la mejor solucion es 79420.10154684729

# CONCLUSIONES: 
#fitness bastante alto pero razonable ya uqe estamos usando fitness 2 y max
#el tiempo voy a reducirlo al reducir numero de generaciones y tamaño de poblacion. 
    
#=============================================================================


# EXPERIMENTO NUMERO 12
#---------------------

# ESTRATEGIAS:
#  - Mutacion por mezcla
#  - Cruce basado en orden 
#  - Seleccion ruleta

# FITNESS: he usado berlinFitness2 

# PARAMETROS:
# Los parametros de este ejemplo son:
# .- Proporcion de cruce = 0.2
# .- Probabilidad de mutacion = 0.1
# .- Numero de generaciones = 1000
# .- Tamanyo de poblacion = 100
# .- Funcion "max" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin3 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorMezcla(),
#                                   CruceBasadoEnOrden(),
#                                   GeneradorPermutacion(),
#                                   SeleccionRuleta(),
#                                   berlinFitness2,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin3.ejecutaAlgoritmoGenetico(0.2,0.1,1000,100,max) )


# SALIDA DEL ALGORITMO:
#[6.288186996462173, [15, 17, 21, 50, 19, 26, 13, 14, 30, 23, 7, 24, 11, 51, 3, 18, 44, 29, 1,
# 6, 16, 47, 28, 36, 35, 4, 2, 5, 37, 20, 52, 39, 43, 9,
# 42, 27, 31, 46, 48, 22, 45, 41, 0, 49, 12, 8, 38, 34, 33, 10, 40, 32, 25], 78277.24074153016]


# TIEMPO Y FITNESS:
# Ha tardado 7.63 segundos y el fitness de la mejor solucion es 78277.24074153016

# CONCLUSIONES: 
#fitness de la mejor solucion es muy parecido a la ejecucion anterior 
#el tiempo ha mejorado muchisimo al reducir un poco tamaño poblacion y numero de generaiones
    
#=============================================================================


# EXPERIMENTO NUMERO 13
#---------------------

# ESTRATEGIAS:
#  - Mutacion por mezcla
#  - Cruce basado en orden 
#  - Seleccion ruleta

# FITNESS: he usado berlinFitness2 

# PARAMETROS:
# Los parametros de este ejemplo son:
# .- Proporcion de cruce = 0.6
# .- Probabilidad de mutacion = 0.5
# .- Numero de generaciones = 1000
# .- Tamanyo de poblacion = 100
# .- Funcion "max" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin3 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorMezcla(),
#                                   CruceBasadoEnOrden(),
#                                   GeneradorPermutacion(),
#                                   SeleccionRuleta(),
#                                   berlinFitness2,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin3.ejecutaAlgoritmoGenetico(0.6,0.5,1000,100,max) )


# SALIDA DEL ALGORITMO:
#[9.538322414373397, [6, 28, 8, 1, 15, 44, 51, 39, 36, 18, 52, 13, 9, 43, 5, 4, 46,
# 12, 22, 40, 2, 42, 20, 34, 29, 19, 10, 14, 11, 27, 38, 16, 45, 30, 37, 49, 25, 33,
# 32, 31, 24, 41, 48, 26, 7, 17, 23, 47, 35, 21, 0, 3, 50], 79622.29992977527]


# TIEMPO Y FITNESS:
# Ha tardado 10.37 segundos y el fitness de la mejor solucion es 79622.29992977527

# CONCLUSIONES: 
#tiempo sique siendo bueno aunque ha aumentado, pienso que puede estar relacionado con la subida de los valores
#de los parámetros de probabilidad de mutacion y prop. cruce. 
    
#=============================================================================

# EXPERIMENTO NUMERO 14
#---------------------

# ESTRATEGIAS:
#  - Mutacion por mezcla
#  - Cruce basado en orden 
#  - Seleccion ruleta

# FITNESS: he usado berlinFitness2 

# PARAMETROS:
# Los parametros de este ejemplo son:
# .- Proporcion de cruce = 1.0
# .- Probabilidad de mutacion = 1.0
# .- Numero de generaciones = 1000
# .- Tamanyo de poblacion = 100
# .- Funcion "max" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin3 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorMezcla(),
#                                   CruceBasadoEnOrden(),
#                                   GeneradorPermutacion(),
#                                   SeleccionRuleta(),
#                                   berlinFitness2,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin3.ejecutaAlgoritmoGenetico(1.0,1.0,1000,100,max) )


# SALIDA DEL ALGORITMO:
#[21.831169497600058, [46, 14, 38, 19, 0, 45, 50, 10, 11, 25, 15, 3, 9, 52, 49, 8,
# 24, 29, 40, 34, 31, 23, 32, 36, 18, 21, 47, 39, 28, 26, 7, 30, 51, 27, 16, 37, 1,
# 17, 35, 42, 4, 22, 5, 2, 6, 33, 48, 13, 43, 41, 20, 44, 12], 78000.02548687713]


# TIEMPO Y FITNESS:
# Ha tardado 22.4 segundos y el fitness de la mejor solucion es 78000.02548687713

# CONCLUSIONES: 
#el tiempo a aumentado casi a el doble y confirmo que aumentar prob. mutacion y prop. cruce aumente tiempo ejecucuin
#resultado de mejor fitness no ha cambiado mucho 
    
#=============================================================================


# EXPERIMENTO NUMERO 15
#---------------------

# ESTRATEGIAS:
#  - Mutacion por mezcla
#  - Cruce basado en orden 
#  - Seleccion ruleta

# FITNESS: he usado berlinFitness2 

# PARAMETROS:
# Los parametros de este ejemplo son:
# .- Proporcion de cruce = 0.0
# .- Probabilidad de mutacion = 0.0
# .- Numero de generaciones = 1000
# .- Tamanyo de poblacion = 100
# .- Funcion "max" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin3 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorMezcla(),
#                                   CruceBasadoEnOrden(),
#                                   GeneradorPermutacion(),
#                                   SeleccionRuleta(),
#                                   berlinFitness2,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin3.ejecutaAlgoritmoGenetico(0.0,0.0,1000,100,max) )


# SALIDA DEL ALGORITMO:
#[4.432919952334487, [19, 35, 2, 32, 13, 49, 22, 16, 20, 47, 21, 1, 40, 39,
# 25, 15, 37, 30, 6, 9, 3, 7, 42, 34, 43, 11, 28, 12, 4, 5, 8, 10, 44, 23, 38, 45, 
#51, 52, 0, 50, 14, 24, 33, 48, 27, 18, 36, 46, 26, 17, 29, 31, 41], 77733.80663617303]


# TIEMPO Y FITNESS:
# Ha tardado 4.74 segundos y el fitness de la mejor solucion es 77733.80663617303

# CONCLUSIONES: 
#el tiempo ha disminuido muchisimo y confirmo que poner al minimo prob. mutacion y prop. cruce minimiza tiempo ejecucuin
#resultado de mejor fitness no ha variado apenas
    
#=============================================================================

# EXPERIMENTO NUMERO 16
#---------------------

# ESTRATEGIAS:
#  - Mutacion por intercambio
#  - Cruce basado en ciclos
#  - Seleccion elitista

# FITNESS: he usado berlinFitness1

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.4
# 2.- Proporcion de cruce = 0.2
# 3.- Probabilidad de mutacion = 0.3
# 4.- Numero de generaciones = 1000
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin4 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.4,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin4.ejecutaAlgoritmoGenetico(0.2,0.3,1000,100,min) )


# SALIDA DEL ALGORITMO:
#[4.544328127580229, [1, 49, 30, 7, 23, 20, 32, 45, 26, 47, 43, 4, 38, 6, 11, 12, 
#33, 52, 18, 17, 42, 2, 5, 51, 41, 8, 35, 36, 39, 19, 24, 16, 0, 3, 48, 25, 46, 
#15, 34, 44, 27, 28, 9, 10, 37, 40, 14, 13, 31, 21, 50, 29, 22], 5574.60663511805]


# TIEMPO Y FITNESS:
# Ha tardado 5.4 segundos y el fitness de la mejor solucion es 5574.60663511805

# CONCLUSIONES: 
#el tiempo de ejecuciones muy bueno, el resultado no es tan malo como con primeras pruebas
#todavia queda mejore en el fitness (resultado)
    
#=============================================================================

# EXPERIMENTO NUMERO 17
#---------------------

# ESTRATEGIAS:
#  - Mutacion por intercambio
#  - Cruce basado en ciclos
#  - Seleccion elitista

# FITNESS: he usado berlinFitness1

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.6
# 2.- Proporcion de cruce = 0.4
# 3.- Probabilidad de mutacion = 0.4
# 4.- Numero de generaciones = 1000
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin4 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.6,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin4.ejecutaAlgoritmoGenetico(0.4,0.4,1000,100,min) )


# SALIDA DEL ALGORITMO:
#[5.61742301133927, [15, 6, 16, 34, 31, 23, 18, 3, 37, 35, 52, 11, 39, 40,
# 12, 25, 26, 13, 30, 46, 48, 4, 14, 47, 21, 17, 0, 24, 36, 44, 45, 19, 7, 2, 49, 32, 33, 51, 42, 
#50, 28, 27, 43, 38, 22, 1, 9, 10, 8, 41, 20, 29, 5], 5384.206703575793]


# TIEMPO Y FITNESS:
# Ha tardado 5.5 segundos y el fitness de la mejor solucion es 5384.206703575793

# CONCLUSIONES: 
#el tiempo de ejecucion sigue siendo muy bueno, el resultado ha mejorado un poco
#todavia queda mejore en el fitness (resultado)
    
#=============================================================================

# EXPERIMENTO NUMERO 18
#---------------------

# ESTRATEGIAS:
#  - Mutacion por intercambio
#  - Cruce basado en ciclos
#  - Seleccion elitista

# FITNESS: he usado berlinFitness1

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.7
# 2.- Proporcion de cruce = 0.5
# 3.- Probabilidad de mutacion = 0.5
# 4.- Numero de generaciones = 1000
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin4 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.7,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin4.ejecutaAlgoritmoGenetico(0.5,0.5,1000,100,min) )


# SALIDA DEL ALGORITMO:
#[5.804132099452545, [31, 21, 43, 33, 9, 10, 4, 38, 3, 0, 19, 45, 40, 36, 16,
# 20, 23, 30, 11, 15, 50, 47, 37, 35, 5, 26, 44, 39, 27, 52, 7, 2, 24, 48, 14, 13, 12, 28, 6,
# 46, 25, 51, 32, 49, 41, 8, 34, 29, 42, 17, 1, 22, 18], 6026.661785727538]


# TIEMPO Y FITNESS:
# Ha tardado 6.38 segundos y el fitness de la mejor solucion es 6026.661785727538

# CONCLUSIONES: 
#el tiempo de ejecucion sigue siendo bueno, el resultado ha empeorado
    
#=============================================================================

# EXPERIMENTO NUMERO 19
#---------------------

# ESTRATEGIAS:
#  - Mutacion por intercambio
#  - Cruce basado en ciclos
#  - Seleccion elitista

# FITNESS: he usado berlinFitness1

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.6
# 2.- Proporcion de cruce = 0.3
# 3.- Probabilidad de mutacion = 0.3
# 4.- Numero de generaciones = 1000
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin4 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.6,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin4.ejecutaAlgoritmoGenetico(0.3,0.3,1000,100,min) )


# SALIDA DEL ALGORITMO:
#[[4.887324883253314, [48, 5, 6, 25, 10, 9, 41, 8, 50, 20, 49, 32, 18, 31, 27, 14,
# 52, 11, 36, 44, 0, 3, 24, 38, 23, 1, 28, 13, 29, 46, 45, 39, 16, 22, 12, 51, 37, 
#40, 34, 35, 7, 2, 30, 42, 47, 26, 17, 21, 33, 43, 15, 4, 19], 4793.840953600338]


# TIEMPO Y FITNESS:
# Ha tardado 5.44 segundos y el fitness de la mejor solucion es 4793.840953600338

# CONCLUSIONES: 
#el tiempo de ejecucion sigue siendo bueno, el resultado es el mejor de este problema
    
#=============================================================================

# EXPERIMENTO NUMERO 20
#---------------------

# ESTRATEGIAS:
#  - Mutacion por intercambio
#  - Cruce basado en ciclos
#  - Seleccion elitista

# FITNESS: he usado berlinFitness1

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.5
# 2.- Proporcion de cruce = 0.3
# 3.- Probabilidad de mutacion = 0.3
# 4.- Numero de generaciones = 800
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin4 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                    CruceBasadoEnCiclos(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.5,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin4.ejecutaAlgoritmoGenetico(0.3,0.3,800,100,min) )


# SALIDA DEL ALGORITMO:
#[3.9267682728532236, [36, 39, 44, 34, 23, 20, 6, 15, 21, 31, 51, 11, 10, 33, 
#2, 7, 43, 4, 45, 41, 32, 22, 27, 26, 38, 37, 30, 50, 0, 18, 29, 16, 5, 25, 1, 49, 14, 28,
# 3, 19, 13, 52, 12, 47, 17, 42, 9, 8, 48, 40, 46, 24, 35], 5052.5432445187125]


# TIEMPO Y FITNESS:
# Ha tardado 4.09 segundos y el fitness de la mejor solucion es 5052.5432445187125

# CONCLUSIONES: 
#el tiempo de ejecucion ha mejorado un poco al disminuir el numero de generaciones
#ha empeorado un poco el mejor fitness, el porcentaje elitista que ha dado mejor resultado es 0.6
    
#=============================================================================

# EXPERIMENTO NUMERO 21
#---------------------

# ESTRATEGIAS:
#  - Mutacion por intercambio
#  - Cruce basado en orden
#  - Seleccion elitista

# FITNESS: he usado berlinFitness1

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.6
# 2.- Proporcion de cruce = 0.3
# 3.- Probabilidad de mutacion = 0.3
# 4.- Numero de generaciones = 800
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin5 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnOrden(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.6,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin5.ejecutaAlgoritmoGenetico(0.3,0.3,800,100,min) )


# SALIDA DEL ALGORITMO:
#[4.888591254566563, [20, 31, 38, 35, 10, 8, 47, 26, 7, 2, 34, 49, 37, 
#6, 22, 5, 50, 29, 3, 17, 42, 21, 16, 44, 14, 52, 9, 41, 43, 25, 18, 0, 27, 11, 24, 15, 13, 28, 30, 46, 
#51, 12, 32, 39, 48, 40, 36, 23, 45, 19, 4, 33, 1], 6012.387007525473]


# TIEMPO Y FITNESS:
# Ha tardado 5.34 segundos y el fitness de la mejor solucion es 6012.387007525473

# CONCLUSIONES: 
#el tiempo de ejecucion ha aumentado un poco respecto al prblema anterior pero sigue siendo bueno
#el mejor fitness ha empeorado respecto a la prueba anterior
#=============================================================================
# EXPERIMENTO NUMERO 22
#---------------------

# ESTRATEGIAS:
#  - Mutacion por intercambio
#  - Cruce basado en orden
#  - Seleccion elitista

# FITNESS: he usado berlinFitness1

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.5
# 2.- Proporcion de cruce = 0.3
# 3.- Probabilidad de mutacion = 0.3
# 4.- Numero de generaciones = 1000
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin5 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnOrden(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.5,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin5.ejecutaAlgoritmoGenetico(0.3,0.3,1000,100,min) )


# SALIDA DEL ALGORITMO:
#[6.119863954882021, [4, 12, 14, 13, 33, 51, 2, 7, 38, 24, 52, 11, 32, 37,
# 27, 28, 42, 17, 1, 22, 0, 39, 30, 21, 40, 44, 50, 34, 10, 9, 25, 48, 16, 18, 29, 20, 47, 26,
# 45, 23, 31, 3, 19, 41, 5, 36, 46, 6, 8, 43, 35, 15, 49], 6237.306252913161]


# TIEMPO Y FITNESS:
# Ha tardado 6.6 segundos y el fitness de la mejor solucion es 6237.306252913161

# CONCLUSIONES: 
#el tiempo de ejecucion ha aumentado un poco respecto a la ejecucion anterior
#el mejor fitness tamben ha empeorado asi que dejar seleccion elitista a 0.6


#===========================================================================================

# EXPERIMENTO NUMERO 23
#---------------------

# ESTRATEGIAS:
#  - Mutacion por intercambio
#  - Cruce basado en orden
#  - Seleccion elitista

# FITNESS: he usado berlinFitness1

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.6
# 2.- Proporcion de cruce = 0.5
# 3.- Probabilidad de mutacion = 0.3
# 4.- Numero de generaciones = 800
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin5 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnOrden(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.6,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin5.ejecutaAlgoritmoGenetico(0.5,0.3,800,100,min) )


# SALIDA DEL ALGORITMO:
#[6.184574901781161, [32, 0, 35, 29, 2, 7, 17, 41, 47, 26, 28, 13, 6, 38, 14,
# 52, 50, 30, 21, 42, 39, 43, 27, 12, 16, 46, 24, 5, 3, 45, 40, 20, 51, 11, 8, 9, 25, 37, 4, 
#15, 33, 10, 49, 36, 48, 44, 23, 31, 34, 22, 19, 18, 1], 6113.010574723471]


# TIEMPO Y FITNESS:
# Ha tardado 7.05 segundos y el fitness de la mejor solucion es 6113.010574723471

# CONCLUSIONES: 
#el tiempo de ejecucion ha aumentado un poco respecto a la ejecucion anterior
#el mejor fitness ha mejorado un poco pero sigue siendo alto


#===========================================================================================

# EXPERIMENTO NUMERO 24
#---------------------

# ESTRATEGIAS:
#  - Mutacion por intercambio
#  - Cruce basado en orden
#  - Seleccion elitista

# FITNESS: he usado berlinFitness1

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.6
# 2.- Proporcion de cruce = 0.5
# 3.- Probabilidad de mutacion = 0.4
# 4.- Numero de generaciones = 800
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin5 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnOrden(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.6,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin5.ejecutaAlgoritmoGenetico(0.5,0.4,800,100,min) )


# SALIDA DEL ALGORITMO:
#[6.307178004717571, [37, 43, 17, 18, 38, 6, 9, 10, 39, 32, 42, 7, 8, 3, 49, 
#44, 19, 41, 29, 50, 51, 28, 21, 2, 12, 27, 45, 0, 11, 52, 25, 4, 13, 26, 14, 47, 34, 24, 
#31, 1, 46, 48, 33, 15, 30, 16, 20, 23, 5, 35, 36, 22, 40], 5842.851386380815]


# TIEMPO Y FITNESS:
# Ha tardado 6.75 segundos y el fitness de la mejor solucion es  5842.851386380815

# CONCLUSIONES: 
#el tiempo de ejecucion ha disminuido un poco respecto a la ejecucion anterior
#el mejor fitness ha mejorado un poco


#===========================================================================================

# EXPERIMENTO NUMERO 25
#---------------------

# ESTRATEGIAS:
#  - Mutacion por intercambio
#  - Cruce basado en orden
#  - Seleccion elitista

# FITNESS: he usado berlinFitness1

# PARAMETROS:
# 1.- Porcentaje elititsta = 0.6
# 2.- Proporcion de cruce = 0.5
# 3.- Probabilidad de mutacion = 0.4
# 4.- Numero de generaciones = 800
# 5.- Tamanyo de poblacion = 80
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
#problemaBerlin5 = ProblemaGenetico(berlin_genetico,
#                                   MutacionPorIntercambio(),
#                                   CruceBasadoEnOrden(),
#                                   GeneradorPermutacion(),
#                                   SeleccionElitista(0.6,min),
#                                   berlinFitness1,
#                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
#print(problemaBerlin5.ejecutaAlgoritmoGenetico(0.5,0.4,800,80,min) )


# SALIDA DEL ALGORITMO:
#[5.000475530701806, [38, 43, 14, 13, 5, 40, 29, 16, 27, 52, 23, 36, 2, 7, 24,
# 25, 18, 3, 48, 15, 1, 0, 8, 41, 30, 42, 33, 39, 49, 17, 10, 9, 20, 50, 4, 12, 26, 47, 46,
# 44, 28, 11, 31, 21, 45, 19, 6, 51, 22, 32, 35, 34, 37], 5709.780994964269]


# TIEMPO Y FITNESS:
# Ha tardado 5.55 segundos y el fitness de la mejor solucion es  5709.780994964269

# CONCLUSIONES: 
#el tiempo de ejecucion ha disminuido un poco respecto a la ejecucion anterior es muy buen tiempo de ejcucion
#el mejor fitness ha mejorado un poco respecto a el experimento aterior pero sigue sin ser el mejor resultado de 
# los experimentos hechos


#===========================================================================================

# EXPERIMENTO NUMERO X
#---------------------

# ESTRATEGIAS:

# FITNESS:

# PARAMETROS:

# DEFINICION DEL PROBLEMA:

# LLAMADA AL ALGORITMO:  

# SALIDA DEL ALGORITMO:

# TIEMPO Y FITNESS:

# CONCLUSIONES: 
