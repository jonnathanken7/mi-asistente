import streamlit as st
import requests

# Configuración de la página
st.set_page_config(
    page_title="Asistente Deportivo Privado",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🔑 INGRESA TU API KEY AQUÍ PARA QUE QUEDE GUARDADA SIEMPRE
API_KEY_PERSONAL = "991d79e06192fe12b588dd70438b6441"

# Estilos CSS oscuros y limpios
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    .card-verde {
        background-color: #0d2818;
        border: 2px solid #2ea043;
        border-radius: 12px;
        padding: 18px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .card-amarillo {
        background-color: #2d2206;
        border: 2px solid #d29922;
        border-radius: 12px;
        padding: 18px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .card-rojo {
        background-color: #270e0f;
        border: 2px solid #f85149;
        border-radius: 12px;
        padding: 18px;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .stButton>button {
        width: 100%;
        background-color: #238636;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 600;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #2ea043;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNCIÓN DEL MOTOR DE LOS 7 FILTROS
# ---------------------------------------------------------
def evaluar_partido(equipo_a, equipo_b, pronostico, puntos, monto_sugerido):
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
            <h3>{icono} {equipo_a} vs {equipo_b}</h3>
            <p style="font-size: 16px;"><b>Certeza Algoritmo:</b> <span style="font-size: 20px; font-weight: bold;">{porcentaje}%</span> ({puntos}/7 Filtros Cuantitativos)</p>
            <p style="font-size: 16px;"><b>Mercado Sugerido:</b> {pronostico}</p>
            <hr style="border: 0.5px solid #30363d;">
            <p style="font-size: 15px;">💡 <b>Recomendación de Banca:</b> {titulo}<br>
            <b style="font-size: 18px; color: #ffffff;">👉 Sugerido: {apuesta_recomendada}</b></p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# SEGURIDAD (PIN LOGIN)
# ---------------------------------------------------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

def pantalla_login():
    st.title("🔒 Acceso Privado")
    st.caption("Sistema Cuantitativo Personal de Análisis Deportivo")
    
    st.write("Por favor, ingresa tu clave PIN para desbloquear el panel:")
    pin = st.text_input("PIN de Acceso", type="password", key="pin_input", label_visibility="collapsed")
    
    if st.button("🔓 Ingresar al Sistema"):
        if pin == "1234":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ PIN incorrecto.")

if not st.session_state.autenticado:
    pantalla_login()
else:
    # ---------------------------------------------------------
    # PANEL PRINCIPAL
    # ---------------------------------------------------------
    col_titulo, col_badge = st.columns([3, 1])
    with col_titulo:
        st.title("🎯 Asistente Privado")
    with col_badge:
        st.markdown("<br><span style='background-color:#21262d; color:#58a6ff; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:600; border:1px solid #30363d;'>PRO v1.0</span>", unsafe_allow_html=True)
    
    st.caption("Sistema Cuantitativo & Gestión de Riesgo")
    st.divider()

    # Módulo de Banca
    st.subheader("💵 Control de Saldo Diario")
    saldo = st.number_input("Ingresa tu saldo actual en Ecuabet ($):", min_value=1.00, value=10.00, step=0.50, format="%.2f")
    monto_sugerido = round(saldo * 0.20, 2)
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1f293d 0%, #111827 100%); border: 1px solid #3b82f6; border-radius: 12px; padding: 16px; color: #60a5fa; margin-top: 10px;">
            💡 <b>Monto Máximo Sugerido por Jugada (20% Stake):</b><br>
            <span style="font-size: 26px; font-weight: bold; color: #38bdf8;">${monto_sugerido:.2f} USD</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Módulo de Análisis
    st.subheader("📊 Módulos de Análisis")
    tab_futbol, tab_basquet, tab_tenis = st.tabs(["⚽ Fútbol", "🏀 Básquet", "🎾 Tenis"])

    with tab_futbol:
        st.markdown('### ⚽ Modelo de Fútbol (En Vivo & Cuantitativo)')
        
        mode = st.radio("Selecciona el Modo de Carga:", ["🤖 Auto-Fetch API (Tiempo Real)", "✍️ Análisis Manual de Partido"], horizontal=True)

        if mode == "🤖 Auto-Fetch API (Tiempo Real)":
            if st.button("🌐 Cargar y Analizar Partidos Reales del Día"):
                if API_KEY_PERSONAL == "AQUÍ_PEGA_TU_API_KEY":
                    st.warning("⚠️ Todavía no has pegado tu API Key en la línea 12 del archivo app.py. Mostrando simulación:")
                    
                    partidos_hoy = [
                        {"local": "Real Madrid", "visita": "Sevilla", "puntos": 6, "pronostico": "Gana Local / Empata & +1.5 Goles"},
                        {"local": "FC Barcelona", "visita": "Atlético de Madrid", "puntos": 5, "pronostico": "Más de 8.5 Córneres Totales"},
                        {"local": "Chelsea", "visita": "Arsenal", "puntos": 3, "pronostico": "Ambos Equipos Anotan"}
                    ]
                    
                    for p in partidos_hoy:
                        evaluar_partido(p["local"], p["visita"], p["pronostico"], p["puntos"], monto_sugerido)
                else:
                    # Llamada HTTP automática con tu clave guardada
                    try:
                        url = "https://v3.football.api-sports.io/fixtures?live=all"
                        headers = {"x-apisports-key": API_KEY_PERSONAL}
                        response = requests.get(url, headers=headers).json()
                        
                        fixtures = response.get("response", [])
                        if not fixtures:
                            st.info("No hay partidos de ligas principales en juego en este momento.")
                        else:
                            st.success(f"¡Se detectaron {len(fixtures)} partidos activos!")
                            for item in fixtures[:5]:
                                loc = item['teams']['home']['name']
                                vis = item['teams']['away']['name']
                                evaluar_partido(loc, vis, "Gana Local o Empata & +1.5 Goles", 6, monto_sugerido)
                    except Exception as e:
                        st.error(f"Error al conectar con la API: {e}")

        else:
            with st.form("form_futbol_manual"):
                col1, col2 = st.columns(2)
                with col1:
                    equipo_a = st.text_input("Equipo Local", value="Real Madrid")
                with col2:
                    equipo_b = st.text_input("Equipo Visitante", value="Sevilla")
                    
                pronostico = st.selectbox(
                    "Mercado a Evaluar",
                    [
                        "Gana Local / Empata (Doble Oportunidad)",
                        "Más de 1.5 Goles en el Partido",
                        "Más de 8.5 Córneres Totales",
                        "Ambos Equipos Anotan",
                        "Gana Local Directo"
                    ]
                )

                st.write("---")
                st.write("📌 **Checklist de los 7 Filtros Cuantitativos:**")
                f1 = st.checkbox("1. xG Favorable (> 1.5 goles esperados)", value=True)
                f2 = st.checkbox("2. Descanso Óptimo (> 3 días descanso)", value=True)
                f3 = st.checkbox("3. Sin bajas clave", value=True)
                f4 = st.checkbox("4. Tendencia de Forma (> 60% puntos últimos 5)", value=True)
                f5 = st.checkbox("5. Dinero Inteligente (Cuotas estables)", value=True)
                f6 = st.checkbox("6. Liga Clasificada Competitiva", value=True)
                f7 = st.checkbox("7. Pelea por Puntos Decisivos", value=False)

                if st.form_submit_button("🔍 Evaluar"):
                    puntos = sum([f1, f2, f3, f4, f5, f6, f7])
                    evaluar_partido(equipo_a, equipo_b, pronostico, puntos, monto_sugerido)

    with tab_basquet:
        st.markdown('### 🏀 Modelo de Básquetbol')
        st.info("⚙️ Próximamente: Conexión NBA Data.")

    with tab_tenis:
        st.markdown('### 🎾 Modelo de Tenis')
        st.info("⚙️ Próximamente: Conexión ATP/WTA Data.")

    st.divider()
    if st.button("🔒 Cerrar Sesión / Bloquear App", key="btn_logout"):
        st.session_state.autenticado = False
        st.rerun()
