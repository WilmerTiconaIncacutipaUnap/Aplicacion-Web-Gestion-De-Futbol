import streamlit as st
import Controller.models.Cliente as Cliente  # Importar la clase Cliente
import Controller.clienteController as ClienteController  # Funciones de cliente
import os

def Registrar():
    idModificar = st.query_params.get_all("id")
    st.query_params.clear()
    clienteRecuperado = None
    if idModificar:
        # Si el parámetro no está vacío, significa que el usuario ha seleccionado para modificar
        idModificar = idModificar[0]  # idModificar = primer valor del array ID
        clienteRecuperado = ClienteController.SeleccionarPorID(idModificar)  # clienteRecuperado = cliente seleccionado para modificar
        st.query_params.id = [clienteRecuperado.id]  # Establecer el parámetro de modificación para el cliente a ser modificado
        st.title('Modificar registro :pencil2:')
    else:
        st.title('Registrar :white_check_mark:')

    with st.form(key='incluir_cliente'):
        listaTrabajos = ['Portero', 'Lateral', 'Defensa', 'Volante', 'Central', 'Centrocampista', 'Delantero']
        if clienteRecuperado is None:
            input_nombre = st.text_input(label='Ingrese el nombre del cliente:', placeholder='Nombre', key='nombre_nuevo')
            input_edad = st.number_input(label='Ingrese la edad del cliente:', format='%i', step=1, min_value=18, max_value=120, key='edad_nuevo')
            input_trabajo = st.selectbox('Seleccione la profesión del cliente:', options=listaTrabajos, key='trabajo_nuevo')
            input_numero_camiseta = st.number_input(label='Ingrese el número de camiseta del jugador:', format='%i', step=1, min_value=1, max_value=99, key='camiseta_nuevo')
            input_foto = st.file_uploader("Sube una foto del cliente", type=["jpg", "png"], key='foto_nuevo')
        else:
            input_nombre = st.text_input(label='Ingrese el nombre del cliente:', value=clienteRecuperado.nombre, key='nombre_modificar')
            input_edad = st.number_input(label='Ingrese la edad del cliente:', format='%i', step=1, min_value=18, max_value=120, value=clienteRecuperado.edad, key='edad_modificar')
            input_trabajo = st.selectbox('Seleccione la profesión del cliente:', options=listaTrabajos, index=listaTrabajos.index(clienteRecuperado.profesion), key='trabajo_modificar')
            input_numero_camiseta = st.number_input(label='Ingrese el número de camiseta del jugador:', format='%i', step=1, min_value=1, max_value=99, value=clienteRecuperado.numero_camiseta, key='camiseta_modificar')
            input_foto = st.file_uploader("Sube una foto del cliente", type=["jpg", "png"], key='foto_modificar')

        input_button_submit = st.form_submit_button("Enviar")

    if input_button_submit:
        foto_nombre = None
        if input_foto is not None:
            foto_nombre = input_foto.name
            foto_ruta = os.path.join("fotos", foto_nombre)  # Guardar en el directorio 'fotos'
            os.makedirs("fotos", exist_ok=True)  # Crear el directorio si no existe
            with open(foto_ruta, "wb") as f:
                f.write(input_foto.getbuffer())

        if clienteRecuperado is None:
            ClienteController.Incluir(Cliente.Cliente(0, input_nombre, input_edad, input_trabajo, foto_nombre))  # Guardar solo el nombre del archivo en la base de datos
            st.success("¡Éxito! Cliente registrado.")
        else:
            ClienteController.Modificar(Cliente.Cliente(clienteRecuperado.id, input_nombre, input_edad, input_trabajo, foto_nombre if input_foto else clienteRecuperado.foto))  # Guardar solo el nombre del archivo en la base de datos
            st.success("¡Éxito! Cliente modificado.")
