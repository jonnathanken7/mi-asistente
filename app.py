import streamlit as st

# Configuración de la página en el navegador
st.set_page_config(
    page_title="Asistente Deportivo Privado",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados para una interfaz móvil limpia, oscura y elegante
st.markdown("""
<style>
    /* Ocultar elementos predeterminados de la interfaz de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Fondo oscuro y tipografía estilizada */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Tarjetas personalizadas con bordes sutiles */
    .custom-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    
    /* Tarjeta destacada para la gestión de saldo */
    .highlight-card {
        background: linear-gradient(135deg, #1f293d 0%, #111827 100%);
        border: 1px solid #3b82f6;
        border-radius: 12px;
        padding: 16px;
        color: #60a5fa;
        margin-top: 15px;
    }

    /* Estilo moderno para los botones principales */
    .stButton>button {
        width: 100%;
        background-color: #238636;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #2ea043;
        color: #ffffff;
        border: none;
    }

    /* Títulos y distintivos */
    .app-title {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 2px;
    }
    .app-subtitle {
        color: #8b949e;
        font-size: 14px;
        margin-bottom: 20px;
    }
    
    .badge {
        background-color: #21262d;
        color: #58a6ff;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. SISTEMA DE SEGURIDAD (PANTALLA DE LOGIN CON PIN)
# ---------------------------------------------------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

def pantalla_login():
    st.markdown('<div class="app-title">🔒 Acceso Privado</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Sistema Cuantitativo Personal de Análisis Deportivo</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.write("Por favor, ingresa tu clave PIN para desbloquear el panel:")
    pin = st.text_input("PIN de Acceso", type="password", key="pin_input", label_visibility="collapsed")
    
    if st.button("🔓 Ingresar al Sistema"):
        # Puedes reemplazar '1234' por tu clave secreta personal
        if pin == "1234":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ PIN incorrecto. Acceso denegado.")
    st.markdown('</div>', unsafe_allow_html=True)

# Verificar si el usuario ingresó la clave
if not st.session_state.autenticado:
    pantalla_login()
else:
    # ---------------------------------------------------------
    # 2. PANEL PRINCIPAL (SOLO VISIBLE CON CLAVE CORRECTA)
    # ---------------------------------------------------------
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="app-title">🎯 Asistente Privado</div>
            <span class="badge">PRO v1.0</span>
        </div>
        <div class="app-subtitle">Sistema Cuantitativo & Gestión de Riesgo</div>
    """, unsafe_allow_html=True)

    # Módulo de Banca Diaria
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader("💵 Control de Saldo Diario")
    
    saldo = st.number_input(
        "Ingresa tu saldo actual en Ecuabet ($):",
        min_value=1.00,
        value=10.00,
        step=0.50,
        format="%.2f"
    )
    
    monto_sugerido = round(saldo * 0.20, 2)
    
    st.markdown(f"""
        <div class="highlight-card">
            💡 <b>Monto Máximo Sugerido (20% Stake):</b><br>
            <span style="font-size: 26px; font-weight: bold; color: #38bdf8;">${monto_sugerido:.2f} USD</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Módulo de Análisis Deportivo
    st.subheader("📊 Módulos de Análisis")
    
    tab_futbol, tab_basquet, tab_tenis = st.tabs(["⚽ Fútbol", "🏀 Básquet", "🎾 Tenis"])

    with tab_futbol:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### ⚽ Modelo de Fútbol")
        st.write("**Fórmulas:** Distribución de Poisson + xG + Factor Fatiga")
        st.write("**Filtro:** Probabilidad estimada > 80%")
        st.write("")
        if st.button("🔍 Analizar Partidos de Fútbol", key="btn_futbol"):
            st.info("⚙️ *Conectando con base de datos en tiempo real... (Mañana agregamos el motor de partidos)*")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_basquet:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 🏀 Modelo de Básquetbol")
        st.write("**Fórmulas:** NetRating (Eficiencia Ofensiva vs Defensiva)")
        st.write("**Filtro:** Valor Esperado (+EV) > 8%")
        st.write("")
        if st.button("🔍 Analizar Partidos de Básquet", key="btn_basquet"):
            st.info("⚙️ *Conectando con base de datos en tiempo real... (Mañana agregamos el motor de partidos)*")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_tenis:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 🎾 Modelo de Tenis")
        st.write("**Fórmulas:** Dominance Rating en Superficie Específica")
        st.write("**Filtro:** Rendimiento histórico > 75%")
        st.write("")
        if st.button("🔍 Analizar Partidos de Tenis", key="btn_tenis"):
            st.info("⚙️ *Conectando con base de datos en tiempo real... (Mañana agregamos el motor de partidos)*")
        st.markdown('</div>', unsafe_allow_html=True)

    # Botón discreto para cerrar sesión
    st.write("")
    if st.button("🔒 Cerrar Sesión / Bloquear App", key="btn_logout"):
        st.session_state.autenticado = False
        st.rerun()
