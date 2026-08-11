import streamlit as st
import requests

# 1. Configuración de pantalla
st.set_page_config(
    page_title="QUANT-BET VIP | Terminal Cuantitativo",
    page_icon="👑",
    layout="centered"
)

# 2. Inicializar la clave en la memoria de la sesión
if "api_key_usuario" not in st.session_state:
    st.session_state["api_key_usuario"] = ""

# 3. Campo en la barra lateral para ingresar la clave de forma segura
st.sidebar.header("🔑 Configuración de Acceso")
clave_ingresada = st.sidebar.text_input(
    "Ingresa tu API Key de API-Sports:",
    value=st.session_state["api_key_usuario"],
    type="password", # Oculta los caracteres como contraseña
    help="Tu clave se mantendrá en memoria solo mientras uses la app y no se guardará en GitHub."
)

# Guardar en sesión
if clave_ingresada:
    st.session_state["api_key_usuario"] = clave_ingresada

# Variable que usará la función de consulta
API_KEY_AUTOMATICA = st.session_state["api_key_usuario"]

# ---------------------------------------------------------
# 4. Botón de escaneo (Solo consulta a la API cuando tú haces clic)
# ---------------------------------------------------------
if st.button("⚡ ESCANEAR PARTIDOS DE HOY"):
    if not API_KEY_AUTOMATICA:
        st.warning("⚠️ Por favor, ingresa tu API Key en la barra lateral izquierda antes de escanear.")
    else:
        st.info("Consultando datos en vivo...")
        # Aquí continúa el resto de tu función de consulta a la API
