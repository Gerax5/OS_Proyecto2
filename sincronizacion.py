import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

class Recurso:
    def __init__(self, name, count):
        self.name = name
        self.count = count
        self.in_use = 0

    def try_access(self):
        raise NotImplementedError

    def release(self):
        if self.in_use > 0:
            self.in_use -= 1

class Mutex(Recurso):
    def try_access(self):
        if self.in_use == 0:
            self.in_use = 1
            return True
        return False

class Semaforo(Recurso):
    def try_access(self):
        if self.in_use < self.count:
            self.in_use += 1
            return True
        return False

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
    waiting_queue = []

    # Recursos
    resources = {}
    for name, count in resource_defs.items():
        resources[name] = Mutex(name, 1) if mechanism == "Mutex" else Semaforo(name, count)

    # Acciones aún no ejecutadas
    pending_actions = actions[:]
    executed_actions = set()
    cycle = 0

    while pending_actions or waiting_queue:
        # Agregar acciones nuevas de este ciclo
        acciones_en_ciclo = [a for a in pending_actions if a[3] == cycle]
        waiting_queue.extend(acciones_en_ciclo)
        pending_actions = [a for a in pending_actions if a not in acciones_en_ciclo]

        liberaciones_pendientes = []
        still_waiting = []

        for pid, accion, recurso, orig_ciclo in waiting_queue:
            if (pid, accion, recurso, orig_ciclo) in executed_actions:
                continue  # Ya fue atendida

            r = resources[recurso]
            if r.try_access():
                timeline.append((cycle, pid, recurso, accion, "ACCESSED"))
                executed_actions.add((pid, accion, recurso, orig_ciclo))
                liberaciones_pendientes.append(recurso)
            else:
                timeline.append((cycle, pid, recurso, accion, "WAITING"))
                still_waiting.append((pid, accion, recurso, orig_ciclo))

        for recurso in liberaciones_pendientes:
            resources[recurso].release()

        waiting_queue = still_waiting
        cycle += 1

        if cycle > 200:
            break  # evitar ciclos infinitos por error

    return timeline


def draw_sync_gantt(timeline, step):
    fig, ax = plt.subplots(figsize=(min(20, step), 5))
    y_map = {}
    ypos = 10

    for _, pid, *_ in timeline:
        if pid not in y_map:
            y_map[pid] = ypos
            ypos += 10

    for cycle, pid, res, action, state in timeline:
        if cycle >= step:
            continue
        color = "green" if state == "ACCESSED" else "red"
        y = y_map[pid]
        ax.broken_barh([(cycle, 1)], (y, 8), facecolors=color)
        ax.text(cycle + 0.05, y + 3, f"{action}:{res}", fontsize=6, color="white" if color == "red" else "black")

    ax.set_xlim(0, step)
    ax.set_ylim(0, ypos + 10)
    ax.set_xlabel("Ciclos")
    ax.set_yticks([y + 4 for y in y_map.values()])
    ax.set_yticklabels(y_map.keys())
    ax.set_title("Simulación de Accesos a Recursos")
    ax.grid(True)
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

# ---------------------------------------
# Componente de interfaz
# ---------------------------------------
def show_sincronizacion_tab():
    st.header("🔗 Simulación de Mecanismos de Sincronización")

    with st.expander("📄 Cargar archivos de simulación"):
        p_file = st.file_uploader("Archivo de procesos", type="txt", key="proc_file")
        r_file = st.file_uploader("Archivo de recursos", type="txt", key="res_file")
        a_file = st.file_uploader("Archivo de acciones", type="txt", key="act_file")

    if p_file and r_file and a_file:
        st.markdown("### ⚙️ Configuración")
        mechanism = st.radio("Selecciona mecanismo de sincronización", ["Mutex", "Semáforo"])

        processes = parse_processes(p_file)
        resources = parse_resources(r_file)
        actions = parse_actions(a_file)

        if mechanism == "Semáforo":
            st.markdown("### Configuración de semáforos")
            semaphore_counts = {}
            for resource in resources.keys():
                semaphore_counts[resource] = st.number_input(
                    f"Contador para {resource}:", min_value=1, value=resources[resource], key=f"sem_{resource}"
                )
            resources = semaphore_counts

        timeline = simulate_with_mechanism(actions, resources, mechanism)
        max_cycle = max(c for c, *_ in timeline) + 1

        step = st.slider("Ciclo actual", 1, max_cycle, max_cycle, key="sync_slider")
        fig = draw_sync_gantt(timeline, step)
        st.pyplot(fig)

        with st.expander("📋 Tabla de Estados por Ciclo"):
            state_table = build_state_table(timeline)
            st.dataframe(state_table, use_container_width=True)

        with st.expander("👁️ Ver timeline (datos crudos)"):
            st.dataframe(timeline, use_container_width=True)

# ---------------------------------------
# Ejecutar la interfaz
# ---------------------------------------
if __name__ == "__main__":
    show_sincronizacion_tab()
