from services import database as db
import streamlit as st
from Controller.models.Cliente import Cliente
import mysql.connector  # Importar mysql.connector directamente
import hashlib 

def Incluir(cliente):
    db.cursor.execute(f'INSERT INTO clientes (nombreCliente, edadCliente, profesionCliente, fotoCliente) VALUES ("{cliente.nombre}", {cliente.edad}, "{cliente.profesion}", "{cliente.foto}")')
    db.bdConnection.commit()

def SeleccionarClientes():
    selectCommand = f'SELECT * FROM clientes'
    db.cursor.execute(selectCommand)
    listaClientes = []
    for row in db.cursor.fetchall():
        listaClientes.append(Cliente(row[0], row[1], row[2], row[3], row[4],  row[5]))

    return listaClientes

def Eliminar(id):
    deleteCommand = f'DELETE FROM clientes WHERE id= {id}'
    db.cursor.execute(deleteCommand)
    db.bdConnection.commit()

def Modificar(cliente):
    updateCommand = f'UPDATE clientes SET nombreCliente = "{cliente.nombre}", edadCliente = {cliente.edad}, profesionCliente = "{cliente.profesion}", fotoCliente = "{cliente.foto}" WHERE id = {cliente.id}'
    db.cursor.execute(updateCommand)
    db.bdConnection.commit()

def SeleccionarPorID(id):
    selectId = f'SELECT * FROM clientes WHERE id = {id}'
    db.cursor.execute(selectId)
    listaId = []
    for row in db.cursor.fetchall():
        listaId.append(Cliente(row[0], row[1], row[2], row[3], row[4]))

    return listaId[0]  # Retornando solo el valor necesario, que es el ID, de la columna 0 en la base de datos



# Nuevas funciones para manejar equipos
def CrearEquipo(nombreEquipo):
    try:
        db.cursor.execute(f'INSERT INTO equipos (nombreEquipo) VALUES ("{nombreEquipo}")')
        db.bdConnection.commit()
    except mysql.connector.errors.IntegrityError:  # Usar mysql.connector directamente
        return False  # Si hay un error de integridad (nombre duplicado), retorna False
    return True

def AsignarJugadorAEquipo(idCliente, idEquipo):
    try:
        updateCommand = f'UPDATE clientes SET idEquipo = {idEquipo} WHERE id = {idCliente} AND idEquipo IS NULL'  # Asegúrate de que el jugador no esté asignado a otro equipo
        db.cursor.execute(updateCommand)
        db.bdConnection.commit()
    except mysql.connector.errors.IntegrityError:  # Usar mysql.connector directamente
        return False  # Si hay un error de integridad (jugador ya asignado a otro equipo), retorna False
    return True

def SeleccionarEquipos():
    selectCommand = 'SELECT * FROM equipos'
    db.cursor.execute(selectCommand)
    listaEquipos = []
    for row in db.cursor.fetchall():
        listaEquipos.append({"id": row[0], "nombreEquipo": row[1]})
    return listaEquipos

def SeleccionarJugadoresPorEquipo(idEquipo):
    selectCommand = f'SELECT * FROM clientes WHERE idEquipo = {idEquipo}'
    db.cursor.execute(selectCommand)
    listaJugadores = []
    for row in db.cursor.fetchall():
        listaJugadores.append(Cliente(row[0], row[1], row[2], row[3], row[4], row[5]))
    return listaJugadores

def GuardarResultadoPartido(equipo1_id, goles_equipo1, equipo2_id, goles_equipo2):
    try:
        db.cursor.execute(
            f'INSERT INTO resultados (equipo1_id, goles_equipo1, equipo2_id, goles_equipo2) VALUES ({equipo1_id}, {goles_equipo1}, {equipo2_id}, {goles_equipo2})'
        )
        db.bdConnection.commit()
    except mysql.connector.Error as err:
        st.error(f"Error al guardar el resultado: {err}")
        


