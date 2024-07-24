import streamlit as st
import Controller.models.Cliente as Cliente  # Importar la clase Cliente
import Controller.clienteController as ClienteController  # Funciones de cliente
import os

def Registrar():
    # Obtener parámetros de consulta y limpiar
    idModificar = st.query_params.get_all("id")
    st.query_params.clear()
    clienteRecuperado = None

    # Si hay un ID de modificación, recuperarlo
    if idModificar:
        idModificar = idModificar[0]  # Obtener el primer valor del array ID
        clienteRecuperado = ClienteController.SeleccionarPorID(idModificar)  # Recuperar cliente por ID
        st.query_params.id = [clienteRecuperado.id]  # Establecer parámetro de modificación
        st.title('Modificar registro :pencil2:')  # Título para modificar
    else:
        st.title('Registrar :white_check_mark:')  # Título para registrar

    # Crear formulario para incluir cliente
    with st.form(key='incluir_cliente'):
        listaTrabajos = ['Portero', 'Lateral', 'Defensa', 'Volante', 'Central', 'Centrocampista', 'Delantero']

        # Campos del formulario para nuevo cliente
        if clienteRecuperado is None:
            input_nombre = st.text_input(label='Ingrese el nombre del cliente:', placeholder='Nombre', key='nombre_nuevo')
            input_edad = st.number_input(label='Ingrese la edad del cliente:', format='%i', step=1, min_value=18, max_value=120, key='edad_nuevo')
            input_trabajo = st.selectbox('Seleccione la profesión del cliente:', options=listaTrabajos, key='trabajo_nuevo')
            input_numero_camiseta = st.number_input(label='Ingrese el número de camiseta del jugador:', format='%i', step=1, min_value=1, max_value=99, key='camiseta_nuevo')
            input_foto = st.file_uploader("Sube una foto del cliente", type=["jpg", "png"], key='foto_nuevo')
        else:
            # Campos del formulario para modificar cliente existente
            input_nombre = st.text_input(label='Ingrese el nombre del cliente:', value=clienteRecuperado.nombre, key='nombre_modificar')
            input_edad = st.number_input(label='Ingrese la edad del cliente:', format='%i', step=1, min_value=18, max_value=120, value=clienteRecuperado.edad, key='edad_modificar')
            input_trabajo = st.selectbox('Seleccione la profesión del cliente:', options=listaTrabajos, index=listaTrabajos.index(clienteRecuperado.profesion), key='trabajo_modificar')
            input_numero_camiseta = st.number_input(label='Ingrese el número de camiseta del jugador:', format='%i', step=1, min_value=1, max_value=99, value=clienteRecuperado.numero_camiseta, key='camiseta_modificar')
            input_foto = st.file_uploader("Sube una foto del cliente", type=["jpg", "png"], key='foto_modificar')

        # Botón para enviar el formulario
        input_button_submit = st.form_submit_button("Enviar")

    # Procesar el envío del formulario
    if input_button_submit:
        foto_nombre = None
        if input_foto is not None:
            foto_nombre = input_foto.name
            foto_ruta = os.path.join("fotos", foto_nombre)  # Ruta para guardar la foto
            os.makedirs("fotos", exist_ok=True)  # Crear directorio si no existe
            with open(foto_ruta, "wb") as f:
                f.write(input_foto.getbuffer())  # Guardar foto en el directorio

        if clienteRecuperado is None:
            # Incluir nuevo cliente
            ClienteController.Incluir(Cliente.Cliente(0, input_nombre, input_edad, input_trabajo, foto_nombre))  # Guardar cliente nuevo
            st.success("¡Éxito! Cliente registrado.")  # Mensaje de éxito
        else:
            # Modificar cliente existente
            ClienteController.Modificar(Cliente.Cliente(clienteRecuperado.id, input_nombre, input_edad, input_trabajo, foto_nombre if input_foto else clienteRecuperado.foto))  # Actualizar cliente
            st.success("¡Éxito! Cliente modificado.")  # Mensaje de éxito
