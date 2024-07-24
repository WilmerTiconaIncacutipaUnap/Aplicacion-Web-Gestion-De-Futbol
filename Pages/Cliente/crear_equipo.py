import streamlit as st
import Controller.clienteController as ClienteController

def CrearEquipo():
    # Establece el título de la página
    st.title("Crear Equipo")

    # Crear nuevo equipo
    with st.form("form_equipo"):
        # Entrada de texto para el nombre del equipo
        nombre_equipo = st.text_input("Nombre del Equipo")
        # Botón para enviar el formulario y crear el equipo
        submit = st.form_submit_button("Crear Equipo")

        # Si se envía el formulario
        if submit:
            # Verifica que el nombre del equipo no esté vacío
            if nombre_equipo:
                # Intenta crear el equipo
                if ClienteController.CrearEquipo(nombre_equipo):
                    # Muestra un mensaje de éxito y refresca la página
                    st.success(f"Equipo '{nombre_equipo}' creado exitosamente.")
                    st.experimental_rerun()
                else:
                    # Muestra un mensaje de error si el equipo ya existe
                    st.error(f"El equipo '{nombre_equipo}' ya existe. Por favor, elige otro nombre.")
            else:
                # Muestra un mensaje de error si el nombre está vacío
                st.error("El nombre del equipo no puede estar vacío.")

    # Listar equipos existentes
    st.subheader("Equipos Existentes")
    equipos = ClienteController.SeleccionarEquipos()
    if equipos:
        # Itera sobre cada equipo y muestra su nombre
        for equipo in equipos:
            st.markdown(f"**{equipo['nombreEquipo']}**")
            jugadores = ClienteController.SeleccionarJugadoresPorEquipo(equipo["id"])
            if jugadores:
                # Muestra los jugadores asignados a cada equipo
                for jugador in jugadores:
                    st.write(f"- {jugador.nombre} (ID: {jugador.id})")
            else:
                # Mensaje si no hay jugadores asignados al equipo
                st.write("No hay jugadores asignados a este equipo.")

    # Asignar jugadores a equipos
    st.subheader("Asignar Jugadores a Equipos")
    equipos_disponibles = ClienteController.SeleccionarEquipos()
    jugadores_disponibles = ClienteController.SeleccionarClientes()

    if equipos_disponibles and jugadores_disponibles:
        with st.form("form_asignar_jugadores"):
            # Selecciona un equipo de los disponibles
            equipo_seleccionado = st.selectbox("Selecciona un equipo", [equipo["nombreEquipo"] for equipo in equipos_disponibles])
            # Selecciona un jugador disponible (no asignado a ningún equipo)
            jugador_seleccionado = st.selectbox("Selecciona un jugador", [f"{jugador.nombre} (ID: {jugador.id})" for jugador in jugadores_disponibles if jugador.idEquipo is None])

            # Botón para enviar el formulario y asignar el jugador al equipo
            submit_asignar = st.form_submit_button("Asignar Jugador")

            if submit_asignar:
                if equipo_seleccionado and jugador_seleccionado:
                    # Obtiene el ID del equipo seleccionado
                    equipo_id = next(equipo["id"] for equipo in equipos_disponibles if equipo["nombreEquipo"] == equipo_seleccionado)
                    # Obtiene el ID del jugador seleccionado
                    jugador_id = int(jugador_seleccionado.split(" (ID: ")[1][:-1])
                    # Intenta asignar el jugador al equipo
                    if ClienteController.AsignarJugadorAEquipo(jugador_id, equipo_id):
                        # Muestra un mensaje de éxito y refresca la página
                        st.success(f"Jugador asignado al equipo '{equipo_seleccionado}' exitosamente.")
                        st.experimental_rerun()
                    else:
                        # Muestra un mensaje de error si hay problemas en la asignación
                        st.error("Error al asignar el jugador al equipo. Asegúrate de que el jugador no esté ya asignado a otro equipo.")
                else:
                    # Muestra un mensaje de error si no se seleccionó equipo o jugador
                    st.error("Debe seleccionar un equipo y un jugador.")
