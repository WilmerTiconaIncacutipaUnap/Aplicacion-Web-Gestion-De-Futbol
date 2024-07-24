import streamlit as st
import random
from graphviz import Digraph
import Controller.clienteController as ClienteController

# Función para generar el árbol de llaves en forma de pirámide
def generar_arbol_llaves(llaves, ronda):
    dot = Digraph()
    dot.attr(rankdir='BT')  # Dibujar el gráfico de abajo hacia arriba

    for ronda_actual in range(1, ronda + 1):
        if f"llaves_ronda_{ronda_actual}" in st.session_state:
            llaves_ronda = st.session_state[f"llaves_ronda_{ronda_actual}"]
            for idx, (equipo1, equipo2) in enumerate(llaves_ronda, start=1):
                dot.node(f"R{ronda_actual}_E{equipo1['id']}", equipo1['nombreEquipo'])
                if equipo2:
                    dot.node(f"R{ronda_actual}_E{equipo2['id']}", equipo2['nombreEquipo'])
                    dot.edge(f"R{ronda_actual}_E{equipo1['id']}", f"R{ronda_actual + 1}_W{idx}", label=f"Partido {idx}")
                    dot.edge(f"R{ronda_actual}_E{equipo2['id']}", f"R{ronda_actual + 1}_W{idx}", label=f"Partido {idx}")

    if f"ronda_{ronda + 1}_llaves" in st.session_state:
        ganadores = st.session_state[f"ronda_{ronda + 1}_llaves"]
        for idx, ganador in enumerate(ganadores, start=1):
            dot.node(f"R{ronda + 1}_W{idx}", ganador['nombreEquipo'])

    return dot

# Función para guardar los resultados
def guardar_resultado(partido_key, equipo1, equipo1_goles, equipo2, equipo2_goles, ronda):
    if equipo1_goles > equipo2_goles:
        ganador = {'id': equipo1['id'], 'nombreEquipo': equipo1['nombreEquipo'], 'equipo1_id': equipo1['id'], 'equipo2_id': equipo2['id']}
    elif equipo2_goles > equipo1_goles:
        ganador = {'id': equipo2['id'], 'nombreEquipo': equipo2['nombreEquipo'], 'equipo1_id': equipo1['id'], 'equipo2_id': equipo2['id']}
    else:
        st.warning("El partido no puede terminar en empate.")
        return

    if f"ronda_{ronda}_resultados" not in st.session_state:
        st.session_state[f"ronda_{ronda}_resultados"] = {}

    st.session_state[f"ronda_{ronda}_resultados"][partido_key] = ganador
    st.success(f"Resultado guardado: {ganador['nombreEquipo']} es el ganador.")
    st.experimental_rerun()

# Función para mostrar las llaves y obtener los resultados
def mostrar_llaves(llaves, ronda):
    st.subheader(f"Ronda {ronda}")

    for idx, (equipo1, equipo2) in enumerate(llaves):
        partido_key = f"partido_{ronda}_{idx}"
        if equipo2:
            with st.form(key=f"form_{partido_key}"):
                st.markdown(f"### Partido {idx + 1}: {equipo1['nombreEquipo']} vs {equipo2['nombreEquipo']}")
                equipo1_goles = st.number_input(f"Goles de {equipo1['nombreEquipo']}", min_value=0, key=f"goles_{equipo1['id']}_r{ronda}")
                equipo2_goles = st.number_input(f"Goles de {equipo2['nombreEquipo']}", min_value=0, key=f"goles_{equipo2['id']}_r{ronda}")
                if st.form_submit_button("Guardar Resultado"):
                    guardar_resultado(partido_key, equipo1, equipo1_goles, equipo2, equipo2_goles, ronda)
        else:
            st.markdown(f"### Partido {idx + 1}: {equipo1['nombreEquipo']} pasa automáticamente a la siguiente ronda.")
            ganador = {'id': equipo1['id'], 'nombreEquipo': equipo1['nombreEquipo'], 'equipo1_id': equipo1['id'], 'equipo2_id': None}
            if f"ronda_{ronda}_resultados" not in st.session_state:
                st.session_state[f"ronda_{ronda}_resultados"] = {}
            st.session_state[f"ronda_{ronda}_resultados"][partido_key] = ganador

# Función principal para sortear el torneo
def sortear_torneo():
    st.title("Sortear Torneo")

    # Botón para sortear de nuevo
    if st.button("Sortear de Nuevo"):
        # Limpiar sólo las variables relacionadas con el sorteo
        keys_to_remove = [key for key in st.session_state.keys() if key.startswith("ronda_") or key in ["llaves", "ronda"]]
        for key in keys_to_remove:
            del st.session_state[key]
        st.experimental_rerun()

    # Obtener la lista de equipos desde ClienteController
    clientes = ClienteController.SeleccionarClientes()
    equipos = [{"id": cliente.id, "nombreEquipo": cliente.nombre} for cliente in clientes]

    if not equipos:
        st.error("No hay equipos disponibles para sortear.")
        return

    # Guardar el estado del torneo en la sesión
    if "llaves" not in st.session_state:
        st.session_state.llaves = []

    if "ronda" not in st.session_state:
        st.session_state.ronda = 1

    ronda_actual = st.session_state.ronda

    # Sortear los equipos si es la primera ronda
    if ronda_actual == 1 and not st.session_state.llaves:
        random.shuffle(equipos)
        llaves = []
        for i in range(0, len(equipos), 2):
            if i + 1 < len(equipos):
                llaves.append((equipos[i], equipos[i + 1]))
            else:
                llaves.append((equipos[i], None))  # Equipo libre si el número de equipos es impar
        st.session_state.llaves = llaves
        st.session_state[f"llaves_ronda_{ronda_actual}"] = llaves
    else:
        llaves = st.session_state.llaves

    # Mostrar las llaves y obtener los resultados de la ronda actual
    mostrar_llaves(llaves, ronda_actual)

    # Mostrar el árbol de llaves para la ronda actual
    if st.button("Generar Árbol de Llaves"):
        dot = generar_arbol_llaves(llaves, ronda_actual)
        st.graphviz_chart(dot)

    # Si hay resultados de la ronda actual, avanzar a la siguiente ronda
    if st.button("Avanzar a la Siguiente Ronda"):
        if f"ronda_{ronda_actual}_resultados" in st.session_state:
            resultados = list(st.session_state[f"ronda_{ronda_actual}_resultados"].values())
            if len(resultados) == len(llaves):
                if len(resultados) == 1:
                    st.success(f"¡{resultados[0]['nombreEquipo']} es el campeón del torneo!")
                else:
                    st.session_state.ronda += 1
                    ronda_actual = st.session_state.ronda
                    st.session_state.llaves = [(resultados[i], resultados[i + 1] if i + 1 < len(resultados) else None) for i in range(0, len(resultados), 2)]
                    st.session_state[f"llaves_ronda_{ronda_actual}"] = st.session_state.llaves
                    st.experimental_rerun()
            else:
                st.warning("Por favor, ingresa los resultados de todos los partidos.")
        else:
            st.warning("Por favor, ingresa los resultados de todos los partidos.")