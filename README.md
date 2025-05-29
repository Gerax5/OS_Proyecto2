# Proyecto 2

- Gerardo Pineda 22880

github: https://github.com/Gerax5/OS_Proyecto2

---

# 💀 Simulador de Planificadores y Mecanismos de Sincronización

Este proyecto es una aplicación web interactiva construida con Streamlit para simular algoritmos de planificación de procesos y mecanismos de sincronización como Mutex y Semáforos.

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/Gerax5/OS_Proyecto2.git
cd simulador-planificadores
```

2. Instala las dependecias

```bash
pip install streamlit matplotlib pandas
```

## 🔪 Ejecución

```bash
streamlit run main.py
```

## Estructura de proyecto

```bash
📦simulador-planificadores
 ┣ 📁algorithms/               # Implementación de algoritmos de planificación (FIFO, SJF, SRT, etc.)
 ┣ 📁components/               # Componentes de visualización como diagramas de Gantt
 ┣ 📄calendarizacion.py        # Lógica y UI para planificación de procesos
 ┣ 📄sincronizacion.py         # Lógica y UI para sincronización de procesos
 ┣ 📄main.py                   # Archivo principal de entrada
```

## Funcionalidad

### Calendarizacion

- Carga de procesos desde un archivo .txt con estructura

```bash
<PID>, <BT>, <AT>, <Priority>
```

Donde:

- `PID`: identificador del proceso (ej. P1)
- `BT`: Burst Time o duración
- `AT`: Arrival Time o tiempo de llegada
- `Priority`: prioridad

**Ejemplo:**

```txt
P1, 8, 0, 1
P2, 4, 1, 2
P3, 9, 2, 3
```

- Algoritmos disponibles
  - FIFO
  - SJF
  - SRT
  - Round Robin (con seleccion de quantum)
  - Priority

### Sincronización

- Carga de procesos, recursos y acciones desde un archivo .txt
- Simulación con:

  - Mutex
  - Semáforos

- Procesos.txt

```txt
P1,0,5,1  # (nombre, tiempo llegada, duración, prioridad)
```

- Recursos

```txt
R1, 2     # (nombre recurso, cantidad)
```

- Acciones:

```txt
P1, READ, R1, 0   # (proceso, acción, recurso, ciclo)
```
