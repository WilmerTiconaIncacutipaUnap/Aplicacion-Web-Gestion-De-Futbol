import streamlit as st
from Pages.Cliente import login as PageLogin
from Pages.Cliente import Registro as PageRegistro
from Pages.Cliente import Listado as PageListado
from Pages.Cliente import crear_equipo as PageCrearEquipo  # Importar la página de creación de equipos
from Pages.Cliente import sorteo as PageSorteo  # Importar la página de sorteo
import os
import base64



# Verificar si el usuario está autenticado
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    
# Ruta de la imagen de fondo
background_image_path = 'C:\\Users\\HP\\Desktop\\softwaretarea\\1.jpg'

# Aplicar CSS para la imagen de fondo sólo si no está autenticado
if not st.session_state['logged_in']:
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
    background: url("data:image/png;base64,{base64.b64encode(open(background_image_path, "rb").read()).decode()}");
    background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Título de la aplicación
st.title(' :soccer: TORNEOS DE FUTBOL :soccer: ')

if not st.session_state['logged_in']:
    PageLogin.login()  # Mostrar la página de login si no está autenticado
else:
    # Mostrar el menú y opciones si está autenticado
    st.sidebar.title(' Menú')
    opciones_sidebar = st.sidebar.selectbox('Cliente', ['Registro', 'Consultar/Modificar', 'Crear equipo', 'Sorteo Torneo', 'Logout'])

    if opciones_sidebar == 'Registro':
        st.query_params.clear()  # Limpiar los parámetros de la consulta
        PageRegistro.Registrar()  # Mostrar la página de registro

    elif opciones_sidebar == 'Consultar/Modificar':
        PageListado.Listado()  # Mostrar la página de listado de clientes

    elif opciones_sidebar == 'Crear equipo':
        PageCrearEquipo.CrearEquipo()  # Mostrar la página de creación de equipos
    
    
    elif opciones_sidebar == 'Sorteo Torneo':
        PageSorteo.sortear_torneo()  # Llamar a la función de sorteo de torneo  

    elif opciones_sidebar == 'Logout':
        PageLogin.logout()  # Realizar logout si el usuario elige salir
        