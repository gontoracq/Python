'''Script que se encarga de crear las estructuras de objetos para su posterior inserción como tablas, 
consulta o borrado en una base de datos Cassandra que corre en un contenedor Docker'''

from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect('gonzalotorres')

class Ciudad:
    def __init__(self, nombre, provincia, comunidad_autonoma):
        self.nombre = nombre
        self.provincia = provincia
        self.comunidad_autonoma = comunidad_autonoma

class Cine:
    def __init__(self, id_cine, nombre, ubicacion, nombre_ciudad):
        self.id_cine = id_cine
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.nombre_ciudad = nombre_ciudad

class Sala:
    def __init__(self, numero, capacidad, id_cine):
        self.numero = numero
        self.capacidad = capacidad
        self.id_cine = id_cine
        
class CineSala:
    def __init__(self, cine_nombre, sala_numero, sala_capacidad):
        self.cine_nombre = cine_nombre
        self.sala_numero = sala_numero
        self.sala_capacidad = sala_capacidad

class Pelicula:
    def __init__(self, nombre, categoria, actores):
        self.nombre = nombre
        self.categoria = categoria
        self.actores = actores

class Funcion:
    def __init__(self, fecha_hora, porcentaje_ocupacion, numero_sala,nombre_pelicula):
        self.fecha_hora = fecha_hora
        self.porcentaje_ocupacion = porcentaje_ocupacion
        self.numero_sala = numero_sala
        self.nombre_pelicula = nombre_pelicula

class Reservacion:
    def __init__(self, confirmado, numero, dni_usuario):
        self.confirmado = confirmado
        self.numero = numero
        self.dni_usuario = dni_usuario

class ReservacionPelicula:
    def __init__(self, numero_reservacion, nombre_pelicula):
        self.numero_reservacion = numero_reservacion
        self.nombre_pelicula = nombre_pelicula

class ReservacionFuncion:
    def __init__(self, numero_reservacion, fecha_hora_funcion):
        self.numero_reservacion = numero_reservacion
        self.fecha_hora_funcion = fecha_hora_funcion

class TipoBoleto:
    def __init__(self, nombre, descuento):
        self.nombre = nombre
        self.descuento = descuento

class TipoBoletoFuncion:
    def __init__(self, nombre_tipoBoleto, fecha_hora_funcion):
        self.nombre_tipoBoleto = nombre_tipoBoleto
        self.fecha_hora_funcion = fecha_hora_funcion

class TipoBoletoReservacion:
    def __init__(self, usuario_dni, numero_reservacion, nombre_tipoBoleto, numero_boletos, tipo_boleto_descuento):
        self.usuario_dni = usuario_dni
        self.numero_reservacion = numero_reservacion
        self.nombre_tipoBoleto = nombre_tipoBoleto
        self.numero_boletos = numero_boletos
        self.tipo_boleto_descuento = tipo_boleto_descuento

class Usuario:
    def __init__(self, dni, nombre, telefonos, telefono):
        self.dni = dni
        self.nombre = nombre
        self.telefonos = telefonos
        self.telefono = telefono

class Tarjeta:
    def __init__(self, numero, fecha, banco):
        self.numero = numero
        self.fecha = fecha
        self.banco = banco

class TarjetaReservacion:
    def __init__(self, tarjeta_banco, tarjeta_numero, tarjeta_fecha, reservacion_numero, reservacion_confirmado):
        self.tarjeta_banco = tarjeta_banco
        self.tarjeta_numero = tarjeta_numero
        self.tarjeta_fecha = tarjeta_fecha
        self.reservacion_numero = reservacion_numero
        self.reservacion_confirmado = reservacion_confirmado

def insertUsuario():
    #Pedimos al usuario sus datos
    dni = input ("Ingrese su dni")
    nombre = input ("Ingrese su nombre")
    telefonos = set()

    telefono1 = input ("Introduzca un telefono, vacio para parar")
    while(telefono1 != ""):
        telefonos.add(telefono1)
        telefono1 = input ("Introduzca un telefono, vacio para parar")
        
    telefono = input ("Ingrese un telefono principal")

    u = Usuario(dni,nombre,telefonos,telefono)
    insertStatement = session.prepare("INSERT INTO tabla7 (usuario_dni, usuario_nombre, usuario_telefonos, usuario_telefono) VALUES (?,?,?,?)")
    session.execute (insertStatement, [u.dni, u.nombre, u.telefonos, u.telefono])
    
def insertPelicula():
    nombre = input ("Ingrese el nombre de una pelicula")
    categoria = input ("Ingrese una categoria")
    actores = set()

    actor = input ("Introduzca un actor, vacio para parar")
    while(actor != ""):
        actores.add(actor)
        actor = input ("Introduzca un actor, vacio para parar")

    u = Pelicula(nombre,categoria, actores)
    insertStatement = session.prepare("INSERT INTO tabla1 (pelicula_nombre, pelicula_categoria, pelicula_actores) VALUES (?,?,?)")
    session.execute (insertStatement, [u.nombre, u.categoria, u.actores])
    insertStatement = session.prepare("INSERT INTO tabla6 (pelicula_nombre, pelicula_categoria, pelicula_actores) VALUES (?,?,?)")
    session.execute (insertStatement, [u.nombre, u.categoria, u.actores])
    insertStatement = session.prepare("INSERT INTO "+'"SoportePelicula"'+" (nombre, categoria, actores) VALUES (?,?,?)")
    session.execute (insertStatement, [u.nombre, u.categoria, u.actores])
    
def insertCine():
    id_cine = int(input ("Ingrese el id del cine"))
    nombre = input ("Ingrese un nombre para el cine")
    ubicacion = input ("Ingrese una ubicación para el cine")
    nombre_ciudad = input ("Ingrese una ciudad")

    u = Cine(id_cine, nombre, ubicacion, nombre_ciudad)
    insertStatement = session.prepare("INSERT INTO "+'"SoporteCine"'+" (id, nombre, ubicacion, nombre_ciudad) VALUES (?,?,?,?)")
    session.execute (insertStatement, [u.id_cine, u.nombre, u.ubicacion, u.nombre_ciudad])
        
def insertReservaCompra():
    usuario_dni = input("Ingrese su dni")
    numero_reservacion = int(input("Ingrese el numero de reserva"))
    nombre_tipoBoleto = input("Ingrese el tipo de boleto")
    numero_boletos = int(input("Ingrese el numero de boletos que quiere comprar"))
    tipo_boleto_descuento = float(input("Ingrese si tiene descuento de cuanto es"))
    
    u = TipoBoletoReservacion(usuario_dni, numero_reservacion, nombre_tipoBoleto, numero_boletos, tipo_boleto_descuento)
    insertStatement = session.prepare("INSERT INTO tabla2 (usuario_dni, reservacion_numero, tipo_boleto_nombre, compra_numero_boletos, tipo_boleto_descuento) VALUES (?,?,?,?,?)")
    session.execute (insertStatement, [u.usuario_dni, u.numero_reservacion, u.nombre_tipoBoleto, u.numero_boletos, u.tipo_boleto_descuento])

def insertCineSala():
    cine_nombre = input("Ingrese nombre del cine")
    sala_numero = int(input("Ingrese numero de sala"))
    sala_capacidad = int(input("Ingrese la capacidad de la sala"))
    
    u = CineSala(cine_nombre, sala_numero, sala_capacidad)
    insertStatement = session.prepare("INSERT INTO tabla3 (cine_nombre, sala_numero, sala_capacidad) VALUES (?,?,?)")
    session.execute (insertStatement, [u.cine_nombre, u.sala_numero, u.sala_capacidad])

def actualizaCategoriaPelicula():
    #Una pelicula no tiene id tiene nombre. Además en la tabla1 la clave es la categoria por lo que
    #no se podra actualizar aqui, tendrá que ser en la tabla de soporte
    categoria = input ("Ingrese la nueva categoria")
    nombre = input ("Ingrese el nombre de una pelicula")
    
    updateCategoriaPelicula = session.prepare("UPDATE "+'"SoportePelicula"'+" SET categoria = ? WHERE nombre = ?")
    session.execute(updateCategoriaPelicula, [categoria,nombre])
    
def borraTarjetaReservas():
    banco = input ("Ingrese el nombre del banco")
    
    deleteTarjetaReservas = session.prepare("DELETE FROM tabla5 WHERE tarjeta_banco = ?")
    session.execute(deleteTarjetaReservas, [banco])
    
def seleccionaPeliculaCategoria():
    categoria = input("Ingrese una categoria")
    peliculasNombre = []
    select = session.prepare("SELECT pelicula_categoria, pelicula_nombre, pelicula_actores FROM tabla1 WHERE pelicula_categoria = ?")
    filas = session.execute(select, [categoria])
    for fila in filas:
        peliculasNombre.append(fila.pelicula_nombre)
    
    print(peliculasNombre)    
    return peliculasNombre

def seleccionaReservasYTipoBoletoSegunDNIUsuario():
    dni = input("Ingrese un DNI")
    reservas = []
    select = session.prepare("SELECT usuario_dni, reservacion_numero, tipo_boleto_nombre, compra_numero_boletos, tipo_boleto_descuento FROM tabla2 WHERE usuario_dni = ?")
    filas = session.execute(select, [dni])
    for fila in filas:
        reservas.append([fila.usuario_dni, fila.reservacion_numero,fila.tipo_boleto_nombre, fila.compra_numero_boletos, fila.tipo_boleto_descuento])
    
    print(reservas)    
    return reservas

def seleccionaSalasSegunCine():
    cine = input("Ingrese el nombre de un cine")
    cines = []
    select = session.prepare("SELECT cine_nombre, sala_numero, sala_capacidad FROM tabla3 WHERE cine_nombre = ?")
    filas = session.execute(select, [cine])
    for fila in filas:
        cines.append([fila.cine_nombre, fila.sala_numero,fila.sala_capacidad])
    
    print(cines)    
    return cines

def seleccionaReservasUsuario():
    dni = input("Ingrese el dni de un usuario")
    reservas = []
    select = session.prepare("SELECT usuario_dni, reservacion_numero FROM tabla4 WHERE usuario_dni = ?")
    filas = session.execute(select, [dni])
    for fila in filas:
        reservas.append([fila.usuario_dni, fila.reservacion_numero])
    
    print(reservas)    
    return reservas

#Obtener con el banco de una tarjeta todas las reservas que se hayan realizado.

def seleccionaReservasSegunBanco():
    banco = input("Ingrese el banco")
    reservas = []
    select = session.prepare("SELECT tarjeta_banco, tarjeta_numero, tarjeta_fecha, reservacion_numero, reservacion_confirmado FROM tabla5 WHERE tarjeta_banco = ?")
    filas = session.execute(select, [banco])
    for fila in filas:
        reservas.append([fila.tarjeta_banco, fila.tarjeta_numero, fila.tarjeta_fecha, fila.reservacion_numero])
    
    print(reservas)    
    return reservas

def seleccionaPeliculaCategoriaOptima():
    categoria = input("Ingrese una categoria")
    peliculas = []
    select = session.prepare("SELECT pelicula_categoria, pelicula_nombre, pelicula_actores FROM tabla6 WHERE pelicula_categoria = ? ALLOW FILTERING")
    filas = session.execute(select, [categoria])
    for fila in filas:
        peliculas.append([fila.pelicula_nombre, fila.pelicula_categoria, fila.pelicula_actores])
    
    print(peliculas)  
    return peliculas

def seleccionaUsuarioSegunTelefono():
    telefono = input("Ingrese el telefono de un usuario")
    usuarios = []
    select = session.prepare("SELECT usuario_dni, usuario_nombre, usuario_telefono FROM tabla7 WHERE usuario_telefono = ?")
    filas = session.execute(select, [telefono])
    for fila in filas:
        usuarios.append([fila.usuario_dni, fila.usuario_nombre, fila.usuario_telefono])
    
    print(usuarios)    
    return usuarios

'''INSERT INTO gonzalotorres.tabla2 (
	usuario_dni, 
	reservacion_numero, 
	tipo_boleto_nombre, 
	compra_numero_boletos, 
	tipo_boleto_descuento
) VALUES ('77819695T',1234,'simple',3,2);'''
    
'''INSERT INTO gonzalotorres.tabla3(
	cine_nombre,
	sala_numero,
	sala_capacidad) 
	VALUES ('Yelmo',2,80);'''
    
'''UPDATE gonzalotorres.tabla4 SET reservacion_numero = reservacion_numero + 1 
WHERE usuario_dni = '77819695T';'''

'''INSERT INTO gonzalotorres.tabla5(
	tarjeta_banco,
	tarjeta_numero,
	tarjeta_fecha,
	reservacion_numero,
	reservacion_confirmado) 
	VALUES ('Santander',12345,12112024,123,true);'''


#insertCineSala()
seleccionaUsuarioSegunTelefono()

session.shutdown()

