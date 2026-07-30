import streamlit as st

# Configuración de la página en el navegador
st.set_page_config(
    page_title="Asistente Deportivo Privado",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados para una interfaz limpia y oscura
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
    
    /* Tarjeta personalizada */
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

    /* Tarjetas de Alerta por Nivel de Riesgo */
    .card-verde {
        background-color: #0d2818;
        border: 1px solid #2ea043;
        border-radius: 12px;
        padding: 16px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .card-amarillo {
        background-color: #2d2206;
        border: 1px solid #d29922;
        border-radius: 12px;
        padding: 16px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .card-rojo {
        background-color: #270e0f;
        border: 1px solid #f85149;
        border-radius: 12px;
        padding: 16px;
        margin-top: 15px;
        margin-bottom: 15px;
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
# FUNCIÓN DEL MOTOR DE LOS 7 FILTROS Y GESTIÓN DE RIESGO
# ---------------------------------------------------------
def evaluar_partido(partido, monto_sugerido):
    puntos = 0
    if partido["xg_favorable"]: puntos += 1
    if partido["descanso_ok"]: puntos += 1
    if partido["sin_bajas_clave"]: puntos += 1
    if partido["clima_favorable"]: puntos += 1
    if partido["apoyo_dinero_inteligente"]: puntos += 1
    if partido["liga_top"]: puntos += 1
    if partido["motivacion_alta"]: puntos += 1

    porcentaje = round((puntos / 7) * 100)

    if puntos >= 6:
        nivel = "verde"
        icono = "🟢"
        titulo = "ABONO SEGURO (Alta Confianza)"
        apuesta_recomendada = f"Apuesta Completa (${monto_sugerido:.2f} USD)"
    elif puntos >= 4:
        nivel = "amarillo"
        icono = "🟡"
        titulo = "OPORTUNIDAD MODERADA (Riesgo Medio)"
        apuesta_recomendada = f"Mitad del Presupuesto (${monto_sugerido / 2:.2f} USD)"
    else:
        nivel = "rojo"
        icono = "🔴"
        titulo = "ZONA DE PELIGRO (No Recomendado)"
        apuesta_recomendada = "⚠️ NO APOSTAR - Guardar Saldo"

    st.markdown(f"""
        <div class="card-{nivel}">
            <h4>{icono} {partido['equipo_a']} vs {partido['equipo_b']}</h4>
            <p><b>Certeza del Algoritmo:</b> {porcentaje}% ({puntos}/7 Filtros Aprobados)</p>
            <p><b>Mercado Sugerido:</b> {partido['pronostico']}</p>
            <hr style="border: 0.5px solid #30363d;">
            <p>💡 <b>Recomendación de Banca:</b> {titulo}<br>
            <b style="font-size: 18px;">👉 Sugerido: {apuesta_recomendada}</b></p>
        </div>
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
    # 2. PANEL PRINCIPAL
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
            💡 <b>Monto Máximo Sugerido por Jugada (20% Stake):</b><br>
            <span style="font-size: 26px; font-weight: bold; color: #38bdf8;">${monto_sugerido:.2f} USD</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Módulo de Análisis Deportivo
    st.subheader("📊 Módulos de Análisis")
    
    tab_futbol, tab_basquet, tab_tenis = st.tabs(["⚽ Fútbol", "🏀 Básquet", "🎾 Tenis"])

    with tab_futbol:
        st.markdown('### ⚽ Modelo de Fútbol')
        st.write("**Evaluación:** 7 Filtros Cuantitativos + Control de Banca")
        st.write("")
        
        if st.button("🔍 Analizar Partidos de Fútbol", key="btn_futbol"):
            st.success("✅ Análisis completado con éxito:")
            
            partido_ejemplo = {
                "equipo_a": "Real Madrid",
                "equipo_b": "Sevilla",
                "pronostico": "Gana Real Madrid o Empata & Más de 1.5 goles",
                "xg_favorable": True,
                "descanso_ok": True,
                "sin_bajas_clave": True,
                "clima_favorable": True,
                "apoyo_dinero_inteligente": True,
                "liga_top": True,
                "motivacion_alta": False
            }
            
            evaluar_partido(partido_ejemplo, monto_sugerido)

    with tab_basquet:
        st.markdown('### 🏀 Modelo de Básquetbol')
        st.write("**Fórmulas:** NetRating (Eficiencia Ofensiva vs Defensiva)")
        st.write("")
        if st.button("🔍 Analizar Partidos de Básquet", key="btn_basquet"):
            st.info("⚙️ Conectando datos de la NBA...")

    with tab_tenis:
        st.markdown('### 🎾 Modelo de Tenis')
        st.write("**Fórmulas:** Dominance Rating en Superficie Específica")
        st.write("")
        if st.button("🔍 Analizar Partidos de Tenis", key="btn_tenis"):
            st.info("⚙️ Conectando datos de la ATP/WTA...")

    st.write("")
    if st.button("🔒 Cerrar Sesión / Bloquear App", key="btn_logout"):
        st.session_state.autenticado = False
        st.rerun()
