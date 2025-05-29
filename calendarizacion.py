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

    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("Sube un archivo .txt con procesos", type="txt")

    with col2:
        selected_algorithms = st.multiselect(
            "Selecciona uno o más algoritmos de planificación",
            ["FIFO", "SJF", "SRT", "Round Robin", "Priority"],
            default=["FIFO"] 
        )


    if uploaded_file:
        processes = load_processes(uploaded_file)
        max_step = 0
        step = 0
        resultados = {}

        if "Round Robin" in selected_algorithms:
            quantum = st.number_input("Quantum para Round Robin", min_value=1, value=2, step=1)

        for alg in selected_algorithms:
            if alg == "FIFO":
                timeline, avg, executed = fifo_scheduler(processes)
            elif alg == "SJF":
                timeline, avg, executed = sjf_scheduler(processes)
            elif alg == "SRT":
                timeline, avg, executed = srtf_scheduler(processes)
            elif alg == "Priority":
                timeline, avg, executed = priority_scheduler(processes)
            elif alg == "Round Robin":
                timeline, avg, executed = round_robin_scheduler(processes, quantum)
            
            resultados[alg] = (timeline, avg, executed)
            max_step = max(max_step, len(timeline))

        step = st.slider("Ciclo actual", 1, max_step, max_step)

        for alg, (timeline, avg, executed) in resultados.items():
            st.markdown(f"### {alg}")
            fig = draw_gantt(executed, timeline, step)
            st.pyplot(fig)
            st.markdown(f"**Tiempo de Espera Promedio {alg}:** {avg:.2f} ciclos")

