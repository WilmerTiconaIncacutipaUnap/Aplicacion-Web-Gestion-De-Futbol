import streamlit as st
import Controller.clienteController as ClienteController
import Pages.Cliente.Registro as PageRegistro
import os

def Listado():
    st.title("Listado de Clientes")
    paramId = st.query_params.get_all("id")
    if not paramId:  # Si el parámetro de modificación está vacío, lista normal de clientes.
        st.query_params.clear()
        st.title("Lista de Jugadores Registrados")

        # Ajustar el estilo del contenedor principal para ocupar todo el ancho
        st.markdown("""
        <style>
        .main-container {
            max-width: 120% ;
        }
        .row {
            display: flex;
            justify-content: center;
            width: 100%;
            margin-bottom: 5rem;
        }
        .column {
            flex: 1;
            padding: 0 1rem;
            text-align: center;
        }
        .actions {
            display: flex;
            justify-content: center;
            gap: 0.1rem; /* Ajustar el espacio entre botones */
        }
        </style>
        """, unsafe_allow_html=True)

        # Usar un container para envolver el contenido
        with st.container():
            columnas = st.columns((3, 5, 7, 4, 5, 10))  # Ajustar tamaños de las columnas
            atributos = [':file_folder: ID', ':frame_with_picture: Foto', ':page_facing_up: Nombre', ':calendar: Edad', ':construction_worker: Posicion', ':x: Eliminar / :arrows_clockwise: Modificar']
            for columna, nombre_atributo in zip(columnas, atributos):
                columna.write(nombre_atributo)

            for item in ClienteController.SeleccionarClientes():
                columnas = st.columns((3, 5, 7, 4, 5, 10))  # Ajustar tamaños de las columnas
                columnas[0].write(str(item.id))

                ## Mostrar la foto si existe
                with columnas[1]:
                    if item.foto:
                        foto_ruta = os.path.join("fotos", item.foto)  # Construir la ruta completa de la imagen
                        if os.path.exists(foto_ruta):
                            st.image(foto_ruta, width=100)  # Ajustar el tamaño de la imagen
                        else:
                            st.write("No hay foto")
                    else:
                        st.write("No hay foto")

                columnas[2].write(item.nombre)
                columnas[3].write(str(item.edad))
                columnas[5].write(item.profesion)

                # Ajustar la alineación de los botones
                with columnas[5]:
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button('Eliminar', key=f'eliminar_{item.id}'):
                            ClienteController.Eliminar(item.id)
                            st.rerun()  # Recarga la página para que el cliente desaparezca de la lista
                    with col2:
                        if st.button('Modificar', key=f'modificar_{item.id}'):
                            st.query_params.id = [item.id]  # Establecer el parámetro ID en la URL para obtener en la página de registro
                            st.rerun()  # Recarga para garantizar

    else:
        PageRegistro.Registrar()  # Registro en modo 'Modificar' porque el parámetro ID no está vacío.
        clickBack = st.button('Volver')
        if clickBack:
            st.query_params.clear()  # Limpiar el parámetro para liberar de la pantalla de modificación
            st.rerun()  # Recarga

