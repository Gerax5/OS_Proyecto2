import streamlit as st
from algorithms.fifo import fifo_scheduler
from components.gantt import draw_gantt
from algorithms.Sjf import sjf_scheduler
from algorithms.Srt import srtf_scheduler
from algorithms.Rr import round_robin_scheduler
from algorithms.P import priority_scheduler

def load_processes(uploaded_file):
    content = uploaded_file.read().decode("utf-8")
    lines = content.strip().split("\n")
    processes = []
    for line in lines:
        parts = line.strip().split(",")
        processes.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))
    return processes

def show_calendarizacion_tab():
    st.header("Planificación de Procesos")

    # Usamos columnas para hacer más compacto
    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("Sube un archivo .txt con procesos", type="txt")

    with col2:
        scheduler_option = st.selectbox("Algoritmo de planificación", ["FIFO", "SJF", "SRT", "Round Robin", "Priority"])

    if uploaded_file:
        processes = load_processes(uploaded_file)

        if scheduler_option == "FIFO":
            timeline, avg_waiting_time, executed = fifo_scheduler(processes)
            print(f"Procesos ejecutados fifo: {executed}")

        elif scheduler_option == "SJF":
            timeline, avg_waiting_time, executed = sjf_scheduler(processes)
            print(f"Procesos ejecutados sjf: {executed}")

        elif scheduler_option == "SRT":
            timeline, avg_waiting_time, executed = srtf_scheduler(processes)
            print(f"Procesos ejecutados srt: {executed}")
        
        elif scheduler_option == "Round Robin":
            quantum = st.number_input("Quantum (ciclos)", min_value=1, value=2, step=1)
            timeline, avg_waiting_time, executed = round_robin_scheduler(processes, quantum)
        
        elif scheduler_option == "Priority":
            timeline, avg_waiting_time, executed = priority_scheduler(processes)
            print(f"Procesos ejecutados priority: {executed}")

        max_step = len(timeline)
        step = st.slider("Ciclo actual", 1, max_step, 1, key=f"slider_{scheduler_option}")

        # Compactamos los datos con un expander opcional
        with st.expander("Ver estadísticas del planificador"):
            st.markdown(f"**Ciclo actual:** {step}")
            st.markdown(f"**Tiempo de Espera Promedio:** {avg_waiting_time:.2f} ciclos")

        fig = draw_gantt(executed, timeline, step)
        st.pyplot(fig)
