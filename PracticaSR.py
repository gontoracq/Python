#encoding:utf-8
from tkinter import *
import sqlite3
from tkinter.tix import COLUMN
from datetime import datetime
import time
import csv
from math import sqrt

###############################CREACIÓN BASE DE DATOS#########################

db = sqlite3.connect('db.db') 
db.text_factory = str
db.execute('''DROP TABLE IF EXISTS ARTISTA''')
db.execute('''DROP TABLE IF EXISTS ETIQUETA''')
db.execute('''DROP TABLE IF EXISTS USUARIOARTISTA''')
db.execute('''DROP TABLE IF EXISTS USUARIOETIQUETAARTISTA''')
db.execute('''DROP TABLE IF EXISTS USUARIOAMIGO''')
db.execute('''CREATE TABLE ARTISTA
             (ID_ARTISTA     INT    NOT NULL,
             NOMBRE       TEXT    NOT NULL,
             URL     TEXT    NOT NULL,
             PICTURE_URL       TEXT    NOT NULL);
             ''')
db.execute('''CREATE TABLE ETIQUETA
             (ID_TAG     INT    NOT NULL,
             TAG_VALUE       TEXT    NOT NULL);
             ''')
db.execute('''CREATE TABLE USUARIOARTISTA
             (ID_USUARIO     INT    NOT NULL,
             ID_ARTISTA      INT    NOT NULL,
             WEIGHT        LONG    NOT NULL);
             ''')
db.execute('''CREATE TABLE USUARIOAMIGO
             (ID_USUARIO     INT    NOT NULL,
             ID_AMIGO      INT    NOT NULL);
             ''')
db.execute('''CREATE TABLE USUARIOETIQUETAARTISTA
             (ID_USUARIO     INT    NOT NULL,
             ID_ARTISTA      INT    NOT NULL,
             ID_TAG        INT    NOT NULL,
             DIA        INT        NOT NULL,
             MES        INT        NOT NULL,
             ANYO    INT        NOT NULL);
             ''')
 

with open('artists/artist.csv', encoding='utf8', errors='ignore') as File:
    reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        id_ = row[0]
        name = row[1]
        url = row[2]
        pictureURL = row[3]
        db.execute("INSERT INTO ARTISTA (ID_ARTISTA,NOMBRE,URL,PICTURE_URL) VALUES (?,?,?,?)",(id_,name,url,pictureURL))
    db.commit()
    print("ok")
    
with open('artists/tags.csv', encoding='utf8', errors='ignore') as File:
    reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        id_tag = row[0]
        tag_value = row[1]
        db.execute("INSERT INTO ETIQUETA (ID_TAG,TAG_VALUE) VALUES (?,?)",(id_tag,tag_value))
    db.commit()
    print("ok")
        
with open('artists/user_artists.csv', encoding='utf8', errors='ignore') as File:
    reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        id_usuario = row[0]
        id_artista = row[1]
        weight = row[2]
        db.execute("INSERT INTO USUARIOARTISTA (ID_USUARIO,ID_ARTISTA,WEIGHT) VALUES (?,?,?)",(id_usuario,id_artista,weight))
    db.commit()
    print("ok")
        
with open('artists/user_friends.csv', encoding='utf8', errors='ignore') as File:
    reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        id_usuario = row[0]
        id_amigo = row[1]
        db.execute("INSERT INTO USUARIOAMIGO (ID_USUARIO,ID_AMIGO) VALUES (?,?)",(id_usuario,id_amigo))
    db.commit()
    print("ok")
        
with open('artists/user_taggedartists.csv', encoding='utf8', errors='ignore') as File:
    reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        id_usuario = row[0]
        id_amigo = row[1]
        id_tag = row[2]
        dia = row[3]
        mes = row[4]
        anyo = row[5]
        db.execute("INSERT INTO USUARIOETIQUETAARTISTA (ID_USUARIO,ID_ARTISTA,ID_TAG,DIA,MES,ANYO) VALUES (?,?,?,?,?,?)",(id_usuario,id_amigo,id_tag,dia,mes,anyo))
    db.commit()
    print("ok")
    

###############################METODOS AUXILIARES#####################################
    
def buscarArtistasEscuchados():
    def listar_busqueda(event):
        conn = sqlite3.connect('db.db')
        conn.text_factory = str
        i = '%'+en.get()+'%'
        cursor = conn.execute("""SELECT * FROM USUARIOARTISTA WHERE ID_USUARIO LIKE ?""",(i,))   
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, yscrollcommand=sc.set)
        for row in cursor:
            lb.insert(END,"Id_Artista: "+str(row[1]))
            cursor2=conn.execute("""SELECT NOMBRE FROM ARTISTA WHERE ID_ARTISTA LIKE ?""",(row[1],))
            var=cursor2.fetchone()
            lb.insert(END,"Nombre: "+str(var[0]))
            lb.insert(END,"Veces escuchado: "+str(row[2]))
            lb.insert(END," ")
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)
        conn.close()
    
    v = Toplevel()
    lb = Label(v, text="Introduzca palabra:")
    
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda)
    en.pack(side = LEFT)
    
def buscar4Etiquetas():
    def listar_busqueda2(event):
        conn = sqlite3.connect('db.db')
        conn.text_factory = str
        i = '%'+en.get()+'%'
        cursor = conn.execute("""SELECT ID_TAG,COUNT(*) FROM USUARIOETIQUETAARTISTA WHERE ID_ARTISTA LIKE ? GROUP BY ID_TAG ORDER BY COUNT(*) DESC""",(i,))   
        lista=cursor.fetchall()
        lista2=[]
        
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, yscrollcommand=sc.set)
        
        for elem in lista[0:4]:
            lista2.append(elem[0])
        lb.insert(END,"Etiquetas: "+str(lista2))
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)
        conn.close()
        print(lista)
        print(lista2)
        print(cursor.rowcount)
        #return lista2
    v = Toplevel()   
    lb = Label(v, text="Introduzca palabra:")
    
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda2)
    en.pack(side = LEFT)
    
def buscar4Etiquetas2(id_artista):
    conn = sqlite3.connect('db.db')
    conn.text_factory = str
    cursor = conn.execute("""SELECT ID_TAG,COUNT(*) FROM USUARIOETIQUETAARTISTA WHERE ID_ARTISTA LIKE ? GROUP BY ID_TAG ORDER BY COUNT(*) DESC""",(id_artista,))   
    lista=cursor.fetchall()
    lista2=[]
    
    for elem in lista[0:4]:
        lista2.append(elem[0])
    conn.close()
    return lista2

print("Estas son las 4 etiquetas más repetidas según artista: "+ str(buscar4Etiquetas2(703)))

def artistasMasEscuchados(id_usuario):
    conn = sqlite3.connect('db.db')
    conn.text_factory = str
    cursor = conn.execute("""SELECT ID_ARTISTA FROM USUARIOARTISTA WHERE ID_USUARIO LIKE ? ORDER BY WEIGHT DESC""",(id_usuario,))   
    lista=cursor.fetchall()
    lista2=[]
    
    for elem in lista[0:2]:
        lista2.append(elem[0])
    conn.close()
    return lista2

print("Artistas más escuchados: "+ str(artistasMasEscuchados(2)))

def artistasMasEscuchadosEstiquetas(id_usuario):
    conn = sqlite3.connect('db.db')
    conn.text_factory = str
    cursor = conn.execute("""SELECT ID_ARTISTA FROM USUARIOARTISTA WHERE ID_USUARIO LIKE ? ORDER BY WEIGHT DESC""",(id_usuario,))   
    lista=cursor.fetchall()
    lista3=[]
    
    for elem in lista[0:2]:
        cursor2=conn.execute("""SELECT ID_TAG,COUNT(*) FROM USUARIOETIQUETAARTISTA WHERE ID_ARTISTA LIKE ? GROUP BY ID_TAG ORDER BY COUNT(*) DESC""",(elem[0],))
        lista2=cursor2.fetchall()
    for elem in lista2[0:4]:
        if elem not in lista3:
            lista3.append(elem[0])
    return lista3

print("4 etiquetas más repetidas de los 2 artistas más escuchados: "+ str(artistasMasEscuchadosEstiquetas(2)))

#############################SISTEMA DE RECOMENDACION##################################

#Primero tenemos que saber cuales son los artistas que no ha escuchado un usuario

def artistasNoEscuchados(id_user):
    conn = sqlite3.connect('db.db')
    conn.text_factory = str
    cursor = conn.execute("""SELECT ID_ARTISTA FROM USUARIOARTISTA WHERE ID_USUARIO LIKE ?""",(id_user,))
    cursor2 = conn.execute("""SELECT ID_ARTISTA FROM USUARIOARTISTA""")
    lista=cursor.fetchall()
    lista2=cursor2.fetchall()
    lista4=[]
    lista3=[elem
            for elem in lista2
            if elem not in lista]
    for elem in lista3:
        if elem not in lista4:
            lista4.append(elem[0])
    lista4.pop(0)
    return lista4

#Este metodo recomienda 4 artistas a un usuario comparando las 4 etiquetas mas frecuentes del usuario con las
#4 etiquetas mas frecuentes de los artistas que no ha escuchado

def recomendarArtistas(id_user):
    etiquetasUser=artistasMasEscuchadosEstiquetas(id_user)
    artistasNo=artistasNoEscuchados(id_user)
    listaAux=[]
    for artista in artistasNo:
        etiquetasArtista=buscar4Etiquetas2(artista)
        cont=0
        for etiqueta in etiquetasArtista:
            if etiqueta in etiquetasUser:
                cont+=1
        listaAux.append([artista,cont])
    listaAux.sort(key=lambda contador: contador[1],reverse=True)
    res=set(listaAux)
    return res[0:4]

# Returns a distance-based similarity score for person1 and person2
""" sim_distance(user, artist):
    # Get the list of shared_items
    si = {}
    for item in buscar4Etiquetas2(artist): 
        if item in artistasMasEscuchadosEstiquetas(user): si[item] = 1

        # if they have no ratings in common, return 0
        if len(si) == 0: return 0

        # Add up the squares of all the differences
        sum_of_squares = sum([pow(buscar4Etiquetas2(artist)[item] - artistasMasEscuchadosEstiquetas(user)[item], 2) 
                    for item in buscar4Etiquetas2(artist) if item in artistasMasEscuchadosEstiquetas(user)])
        
        return 1 / (1 + sum_of_squares)"""

#print(artistasNoEscuchados(2))
print("Artistas recomendados: "+str(recomendarArtistas(2)))
#print(sim_distance(2, 703))

root = Tk()
menubar = Menu(root)    
buscarmenu = Menu(menubar, tearoff=0)
buscarmenu.add_command(label="Escuchados", command=buscarArtistasEscuchados)
buscarmenu.add_command(label="Etiquetas", command=buscar4Etiquetas)
menubar.add_cascade(label="Buscar", menu=buscarmenu)
root.config(menu=menubar)

root.mainloop()
    