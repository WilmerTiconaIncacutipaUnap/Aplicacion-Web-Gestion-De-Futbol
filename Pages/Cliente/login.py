import streamlit as st
from services.database import bdConnection, cursor
import hashlib
from Pages.Cliente.Registro import Registrar # Importa la función Listado
import base64
import mysql.connector

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    # Estilos específicos para la página de login

    st.markdown("""
        <style>
            .login-title {
                text-align: center;
                font-size: 2rem;
                margin-bottom: 1rem;
            }
            .login-input {
                width: 100%;
                padding: 0.5rem;
                margin-bottom: 1rem;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .login-button {
                width: 100%;
                padding: 0.5rem;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .login-button:hover {
                background-color: #45a049;
            }
            .registro-container {
                margin-top: 2rem;
                padding: 1rem;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .registro-title {
                text-align: center;
                font-size: 1.5rem;
                margin-bottom: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Crear el contenedor HTML alrededor de los componentes de Streamlit en la barra lateral
    st.sidebar.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="login-title">Acceso</div>', unsafe_allow_html=True)

    username = st.sidebar.text_input('Username', key='login_username', placeholder='Ingrese su usuario')
    password = st.sidebar.text_input('Password', type='password', key='login_password', placeholder='Ingrese su contraseña')

    if st.sidebar.button('Ingresar', key='login_button'):
        if username and password:
            query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
            cursor.execute(query, (username, hash_password(password)))
            user = cursor.fetchone()

            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = user[1]  # Assuming username is the second column
                st.sidebar.success('Login successful!')

                # Redirigir al usuario a la página de registro después del login exitoso
                st.rerun()  # Recargar la página para actualizar la barra lateral
            else:
                st.sidebar.error('Invalid username or password')
        else:
            st.sidebar.error('Please enter both username and password')

    # Sección para registro de nuevos usuarios
    st.sidebar.markdown('<div class="registro-container">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="registro-title">Registro</div>', unsafe_allow_html=True)

    nuevo_username = st.sidebar.text_input('Nuevo Username', key='registro_username', placeholder='Ingrese el nuevo usuario')
    nuevo_password = st.sidebar.text_input('Nuevo Password', type='password', key='registro_password', placeholder='Ingrese la nueva contraseña')

    if st.sidebar.button('Registrar', key='registro_button'):
        if nuevo_username and nuevo_password:
            hashed_password = hash_password(nuevo_password)
            try:
                cursor.execute('INSERT INTO usuarios (username, password) VALUES (%s, %s)', (nuevo_username, hashed_password))
                bdConnection.commit()
                st.sidebar.success('Usuario creado exitosamente!')
            except mysql.connector.Error as err:
                st.sidebar.error(f"Error al crear usuario: {err}")
        else:
            st.sidebar.error('Por favor ingrese un nuevo usuario y contraseña')

    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.rerun()  # Recargar la página para volver al estado de login
    
    