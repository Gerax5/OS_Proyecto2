import streamlit as st
from calendarizacion import show_calendarizacion_tab
from sincronizacion import show_sincronizacion_tab

st.set_page_config(layout="wide")
st.title("Simulador de Planificadores")

tab1, tab2 = st.tabs(["Calendarización", "Sincronización"])

with tab1:
    show_calendarizacion_tab()

with tab2:
    show_sincronizacion_tab()
