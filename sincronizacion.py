import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from Recursos import Mutex, Semaforo

def parse_processes(file):
    return [line.strip().split(",") for line in file.read().decode("utf-8").strip().split("\n")]

def parse_resources(file):
    resources = {}
    for line in file.read().decode("utf-8").strip().split("\n"):
        name, count = line.strip().split(",")
        resources[name.strip()] = int(count.strip())
    return resources

def parse_actions(file):
    actions = []
    for line in file.read().decode("utf-8").strip().split("\n"):
        pid, action, resource, cycle = line.strip().split(",")
        actions.append((pid.strip(), action.strip().upper(), resource.strip(), int(cycle.strip())))
    return sorted(actions, key=lambda x: x[3])


def simulate_with_mechanism(actions, resource_defs, mechanism):
    timeline = []

    # resources = {
    #     name: Mutex(name, 1) if count == 1 else Semaforo(name, count)
    #     for name, count in resource_defs.items()
    # }

    resources = {
        name: Mutex(name, 1) if mechanism == "Mutex" else Semaforo(name, count)
        for name, count in resource_defs.items()
    }


    acciones_por_proceso = {}
    for pid, accion, recurso, ciclo in actions:
        acciones_por_proceso.setdefault(pid, []).append((accion, recurso, ciclo))

    acciones_en_proceso = {pid: None for pid in acciones_por_proceso}
    recursos_a_liberar = []
    ciclo = 0
    MAX_CICLOS = 200

    while ciclo < MAX_CICLOS:
        for recurso in recursos_a_liberar:
            print(f"[{ciclo}] LIBERA {recurso}")
            resources[recurso].release()
        recursos_a_liberar = []

        hay_pendientes = False

        for pid in acciones_por_proceso:
            if acciones_en_proceso[pid] is None and acciones_por_proceso[pid]:
                accion, recurso, ciclo_obj = acciones_por_proceso[pid][0]
                if ciclo >= ciclo_obj:
                    acciones_en_proceso[pid] = (accion, recurso, ciclo_obj)

            if acciones_en_proceso[pid] is not None:
                accion, recurso, ciclo_obj = acciones_en_proceso[pid]
                r = resources[recurso]
                print(f"[{ciclo}] {pid} intenta {accion} en {recurso} (ciclo objetivo: {ciclo_obj})")
                print(f"    Estado recurso: in_use={r.in_use}, count={r.count}")
                if r.try_access():
                    print(f"[{ciclo}] {pid} ACCEDE a {recurso}")
                    timeline.append((ciclo, pid, recurso, accion, "ACCESSED"))
                    recursos_a_liberar.append(recurso)
                    acciones_por_proceso[pid].pop(0)
                    acciones_en_proceso[pid] = None
                else:
                    print(f"[{ciclo}] {pid} ESPERA por {recurso}")
                    timeline.append((ciclo, pid, recurso, accion, "WAITING"))

                hay_pendientes = True

        if not hay_pendientes:
            break

        ciclo += 1

    return timeline


def draw_sync_gantt(timeline, step):
    procesos = sorted(set(pid for _, pid, *_ in timeline))
    alto_por_proceso = 6  # altura por barra individual
    altura_total = max(2, len(procesos) * alto_por_proceso / 10)  # altura mínima 2
    ancho_total = max(6, min(12, step))  # limitar ancho a 12 máx

    fig, ax = plt.subplots(figsize=(ancho_total, altura_total))
    y_map = {pid: i * alto_por_proceso for i, pid in enumerate(procesos)}

    for cycle, pid, res, action, state in timeline:
        if cycle >= step:
            continue
        color = "green" if state == "ACCESSED" else "red"
        y = y_map[pid]
        ax.broken_barh([(cycle, 1)], (y, alto_por_proceso - 2), facecolors=color)
        ax.text(cycle + 0.05, y + 1.5, f"{action}:{res}", fontsize=5, color="white" if color == "red" else "black")

    ax.set_xlim(0, step)
    ax.set_ylim(0, len(procesos) * alto_por_proceso)
    ax.set_xlabel("Ciclos", fontsize=8)
    ax.set_yticks([y + alto_por_proceso / 2 for y in y_map.values()])
    ax.set_yticklabels(procesos, fontsize=7)
    ax.set_title("Simulación de Accesos a Recursos", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    return fig

# ---------------------------------------
# Construcción de tabla por ciclo
# ---------------------------------------
def build_state_table(timeline):
    data = {}
    for cycle, pid, res, action, state in timeline:
        if cycle not in data:
            data[cycle] = {}
        abbrev = "A" if state == "ACCESSED" else "W"
        data[cycle][pid] = f"{action}:{res} ({abbrev})"
    
    df = pd.DataFrame.from_dict(data, orient="index").sort_index()
    df.index.name = "Ciclo"
    df.fillna("", inplace=True)
    return df

def show_sincronizacion_tab():
    st.header("Simulación de Mecanismos de Sincronización")

    with st.expander("Cargar archivos de simulación"):
        p_file = st.file_uploader("Archivo de procesos", type="txt", key="proc_file")
        r_file = st.file_uploader("Archivo de recursos", type="txt", key="res_file")
        a_file = st.file_uploader("Archivo de acciones", type="txt", key="act_file")

    if p_file and r_file and a_file:
        # st.markdown("### Configuración Automática de Recursos")
        # Para asignacion automatica de Mutex y Semáforos
        # st.info("Los recursos con `count = 1` se manejan como **Mutex**, y los que tienen `count > 1` como **Semáforos**.")
        st.markdown("### Configuración")
        mechanism = st.radio("Selecciona mecanismo de sincronización", ["Mutex", "Semáforo"])

        processes = parse_processes(p_file)
        resource_counts = parse_resources(r_file)
        actions = parse_actions(a_file)

        if mechanism == "Semáforo":
            st.markdown("### Configuración de semáforos")
            semaphore_counts = {}
            for resource in resource_counts.keys():
                semaphore_counts[resource] = st.number_input(
                    f"Contador para {resource}:", min_value=1, value=resource_counts[resource], key=f"sem_{resource}"
                )
            resource_counts = semaphore_counts


        # st.markdown("### Recursos y tipo de sincronización asignado:")
        # resource_types = {}
        # for name, count in resource_counts.items():
        #     tipo = "Mutex" if count == 1 else "Semáforo"
        #     resource_types[name] = tipo
        #     st.markdown(f"- **{name}**: {tipo} (count = {count})")

        # resources = {}
        # for name, count in resource_counts.items():
        #     if count == 1:
        #         resources[name] = Mutex(name, 1)
        #     else:
        #         resources[name] = Semaforo(name, count)

        timeline = simulate_with_mechanism(actions, resource_counts, mechanism)
        max_cycle = max(c for c, *_ in timeline) + 1

        step = st.slider("Ciclo actual", 1, max_cycle, max_cycle, key="sync_slider")
        fig = draw_sync_gantt(timeline, step)
        st.pyplot(fig)

        with st.expander("Tabla de Estados por Ciclo"):
            state_table = build_state_table(timeline)
            st.dataframe(state_table, use_container_width=True)

        with st.expander("Ver timeline (datos crudos)"):
            st.dataframe(timeline, use_container_width=True)

