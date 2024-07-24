import mysql.connector
from os import environ

HOST = environ.get('HOST', 'localhost')
PASSWD = environ.get('PASSWD', '')
USER = environ.get('USER', 'root')
DATABASE = environ.get('DATABASE', 'tarea')

bdConnection = mysql.connector.connect(
    host=f'{HOST}',
    user=f'{USER}',
    password=f'{PASSWD}',
    database=f'{DATABASE}',
 
    
)  # defincicion de la conexion al abase de datos

cursor = bdConnection.cursor()  
bdConnection.commit()