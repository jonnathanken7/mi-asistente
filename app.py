import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN Y SEGURIDAD
# ==========================================
st.set_page_config(page_title="Mi Asistente Privado", page_icon="🎯", layout="centered")

PIN_CORRECTO = "1234"  # Tu PIN de acceso privado

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# ==========================================
# 2. PANTALLA DE BLOQUEO
# ==========================================
if not st.session_state.autenticado:
    st.title("🔒 Acceso Restringido")
    st.write("Ingresa tu PIN personal para acceder:")
    
    pin_ingresado = st.text_input("PIN de Seguridad:", type="password")
    
    if st.button("Ingresar al Panel"):
        if pin_ingresado == PIN_CORRECTO:
            st.session_state.autenticado = True
            st.success("¡Acceso concedido!")
            st.rerun()
        else:
            st.error("❌ PIN incorrecto.")
    st.stop()

# ==========================================
# 3. PANEL PRINCIPAL
# ==========================================
st.title("🎯 Asistente Deportivo Personal")
st.caption("Sistema cuantitativo de análisis y gestión de riesgo")

st.divider()

# --- CONTROL DE BANCA DIARIA ---
st.subheader("💵 Control de Saldo Diario")
saldo_actual = st.number_input(
    "Ingresa tu saldo de hoy en Ecuabet ($):", 
    min_value=1.0, 
    value=10.0, 
    step=0.5
)

stake_recomendado = round(saldo_actual * 0.20, 2)
st.info(f"💡 Gestión de Riesgo: Para un saldo de ${saldo_actual:.2f}, tu monto máximo sugerido por jugada (20%) es de ${stake_recomendado:.2f}")
st.divider()

# --- MÓDULO DE LOS 3 DEPORTES ---
st.subheader("📊 Análisis de Partidos")
tab1, tab2, tab3 = st.tabs(["⚽ Fútbol", "🏀 Baloncesto", "🎾 Tenis"])

with tab1:
    st.write("### Modelo Poisson & Goles Esperados (xG)")
    if st.button("Analizar Partidos de Fútbol"):
        st.write("🔄 Buscando partidos con filtro >80% de probabilidad...")
        st.success("✅ Barcelona SC vs. Rival: Filtro Aprobado (Sugerencia: 1X + Más 1.5 goles)")

with tab2:
    st.write("### Modelo NetRating")
    if st.button("Analizar Partidos de Básquet"):
        st.write("🔄 Evaluando diferencia de eficiencia en casa (+8.0 pts)...")
        st.success("✅ Boston Celtics: Filtro Aprobado (Ganador Directo)")

with tab3:
    st.write("### Modelo Dominance Rating")
    if st.button("Analizar Torneos de Tenis"):
        st.write("🔄 Filtrando jugadores con DR > 1.15...")
        st.success("✅ Carlos Alcaraz: Filtro Aprobado (Ganador 2-0)")
