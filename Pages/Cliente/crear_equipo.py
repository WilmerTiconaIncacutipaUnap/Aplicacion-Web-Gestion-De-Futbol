import streamlit as st
import Controller.clienteController as ClienteController

def CrearEquipo():
    st.title("Crear Equipo")

    # Crear nuevo equipo
    with st.form("form_equipo"):
        nombre_equipo = st.text_input("Nombre del Equipo")
        submit = st.form_submit_button("Crear Equipo")

        if submit:
            if nombre_equipo:
                if ClienteController.CrearEquipo(nombre_equipo):
                    st.success(f"Equipo '{nombre_equipo}' creado exitosamente.")
                    st.experimental_rerun()  # Refresca la página para mostrar el nuevo equipo
                else:
                    st.error(f"El equipo '{nombre_equipo}' ya existe. Por favor, elige otro nombre.")
            else:
                st.error("El nombre del equipo no puede estar vacío.")

    # Listar equipos existentes
    st.subheader("Equipos Existentes")
    equipos = ClienteController.SeleccionarEquipos()
    if equipos:
        for equipo in equipos:
            st.markdown(f"**{equipo['nombreEquipo']}**")
            jugadores = ClienteController.SeleccionarJugadoresPorEquipo(equipo["id"])
            if jugadores:
                for jugador in jugadores:
                    st.write(f"- {jugador.nombre} (ID: {jugador.id})")
            else:
                st.write("No hay jugadores asignados a este equipo.")

    # Asignar jugadores a equipos
    st.subheader("Asignar Jugadores a Equipos")
    equipos_disponibles = ClienteController.SeleccionarEquipos()
    jugadores_disponibles = ClienteController.SeleccionarClientes()

    if equipos_disponibles and jugadores_disponibles:
        with st.form("form_asignar_jugadores"):
            equipo_seleccionado = st.selectbox("Selecciona un equipo", [equipo["nombreEquipo"] for equipo in equipos_disponibles])
            jugador_seleccionado = st.selectbox("Selecciona un jugador", [f"{jugador.nombre} (ID: {jugador.id})" for jugador in jugadores_disponibles if jugador.idEquipo is None])

            submit_asignar = st.form_submit_button("Asignar Jugador")

            if submit_asignar:
                if equipo_seleccionado and jugador_seleccionado:
                    equipo_id = next(equipo["id"] for equipo in equipos_disponibles if equipo["nombreEquipo"] == equipo_seleccionado)
                    jugador_id = int(jugador_seleccionado.split(" (ID: ")[1][:-1])
                    if ClienteController.AsignarJugadorAEquipo(jugador_id, equipo_id):
                        st.success(f"Jugador asignado al equipo '{equipo_seleccionado}' exitosamente.")
                        st.experimental_rerun()  # Refresca la página para actualizar la lista de jugadores asignados
                    else:
                        st.error("Error al asignar el jugador al equipo. Asegúrate de que el jugador no esté ya asignado a otro equipo.")
                else:
                    st.error("Debe seleccionar un equipo y un jugador.")