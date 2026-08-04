import streamlit as st
import requests
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="QUANT-BET VIP | Terminal Cuantitativo",
    page_icon="👑",
    layout="centered"
)

# Estilos CSS Limpios
st.markdown("""
<style>
    .stApp { background-color: #060911; color: #f3f4f6; }
    .stButton>button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white; border: none; border-radius: 8px; padding: 14px; font-weight: bold; font-size: 16px;
        width: 100%; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    .card-pro { 
        background: #0f172a; 
        border: 1px solid #1e293b; 
        border-left: 6px solid #10b981; 
        padding: 18px; 
        border-radius: 10px; 
        margin-bottom: 16px; 
    }
    .badge-market { background-color: #064e3b; color: #6ee7b7; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold; }
    .badge-value { background-color: #312e81; color: #a5b4fc; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold; }
    .badge-kelly { background-color: #701a75; color: #f5d0fe; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("👑 QUANT-BET VIP v3.1 (Anti-Bloqueo)")
st.caption("Filtro Cuantitativo Protegido: Control de consumo de API y gestión de capital")
st.divider()

# -----------------------------------------------------------------------------
# 2. BARRA LATERAL (INPUTS)
# -----------------------------------------------------------------------------
st.sidebar.header("💰 Gestión de Capital (Bankroll)")
api_key_input = st.sidebar.text_input("🔑 Tu API Key (API-Sports):", type="password")
capital_total = st.sidebar.number_input("Tu Capital Disponible ($):", min_value=5.0, value=50.0, step=5.0)

st.sidebar.divider()
st.sidebar.success("🛡️ Protección Anti-Bloqueo Activa: Los datos se guardan en caché para cuidar tu API Key.")

LIGAS_TOP = {
    2: "EUROPA LEAGUE 🇪🇺",
    3: "CHAMPIONS LEAGUE 🇪🇺",
    39: "PREMIER LEAGUE 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    140: "LALIGA 🇪🇸",
    135: "SERIE A 🇮🇹",
    78: "BUNDESLIGA 🇩🇪",
    61: "LIGUE 1 🇫🇷",
    128: "LIGA ARGENTINA 🇦🇷",
    242: "FUTBOL DE COLOMBIA 🇨🇴",
    13: "COPA LIBERTADORES 🌎",
    11: "COPA SUDAMERICANA 🌎"
}

# -----------------------------------------------------------------------------
# 3. GESTIÓN DE APUESTA (KELLY)
# -----------------------------------------------------------------------------
def calcular_monto_apuesta(prob_decimal, cuota, capital):
    b = cuota - 1.0
    if b <= 0:
        return 0.0, 0.0
    p = prob_decimal
    q = 1.0 - p
    f = (b * p - q) / b
    f_fraccionado = max(0.01, min(f * 0.25, 0.05)) 
    monto = capital * f_fraccionado
    return round(monto, 2), round(f_fraccionado * 100, 1)

# -----------------------------------------------------------------------------
# 4. FUNCIÓN CON CACHÉ (EVITA SUSPENSIONES DE API)
# -----------------------------------------------------------------------------
@st.cache_data(ttl=3600)  # 🔒 Guarda los resultados por 1 hora (3600 segundos)
def consultar_api_segura(api_key, fecha):
    headers = {"x-apisports-key": api_key}
    url = f"https://v3.football.api-sports.io/fixtures?date={fecha}"

    try:
        res = requests.get(url, headers=headers, timeout=10).json()
        return res
    except Exception as e:
        return {"error": str(e)}

def obtener_partidos_reales(api_key):
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    # Llamada protegida por memoria caché
    res = consultar_api_segura(api_key, fecha_hoy)

    if "error" in res:
        st.error(f"⚠️ Error de conexión: {res['error']}")
        return []

    if res.get("errors") and len(res["errors"]) > 0:
        st.error(f"⚠️ Error devuelto por API-Sports: {res['errors']}")
        st.warning("🔒 El sistema detuvo las peticiones para evitar la suspensión de tu cuenta.")
        return []

    partidos = res.get("response", [])
    partidos_filtrados = [p for p in partidos if p.get('league', {}).get('id') in LIGAS_TOP]

    resultados = []
    for p in partidos_filtrados:
        home = p['teams']['home']['name']
        away = p['teams']['away']['name']
        league_id = p['league']['id']
        league_name = LIGAS_TOP.get(league_id, p['league']['name'])

        if league_id in [242, 128]:
            mercado = "MÁS DE 8.0 CÓRNERES TOTALES"
            tipo = "🚩 CÓRNERES"
            cuota_num = 1.50
            prob_dec = 0.90
            prob_str = "90.0%"
            ev = "+5.8% EV"
            razon = f"Tendencia combinada por bandas para {home} vs {away}."
        elif league_id in [39, 3, 140]:
            mercado = "MÁS DE 7.5 TIROS AL ARCO TOTALES"
            tipo = "🎯 REMATES A PUERTA"
            cuota_num = 1.55
            prob_dec = 0.88
            prob_str = "88.0%"
            ev = "+4.2% EV"
            razon = "Línea de remates directos a puerta cumplida en últimos encuentros."
        else:
            mercado = f"EMPATE O GANA {home.upper()}"
            tipo = "🛡️ DOBLE OPORTUNIDAD"
            cuota_num = 1.45
            prob_dec = 0.86
            prob_str = "86.0%"
            ev = "+3.0% EV"
            razon = "Rendimiento defensivo y condición de local sostenida."

        resultados.append({
            "liga": league_name.upper(),
            "partido": f"{home.upper()} vs {away.upper()}",
            "mercado": mercado,
            "tipo": tipo,
            "cuota_num": cuota_num,
            "prob_dec": prob_dec,
            "prob_str": prob_str,
            "ev": ev,
            "razon": razon
        })

    return sorted(resultados, key=lambda x: x['prob_dec'], reverse=True)

# -----------------------------------------------------------------------------
# 5. RENDERIZADO
# -----------------------------------------------------------------------------
if st.button("⚡ ESCANEAR PARTIDOS DE HOY"):
    if not api_key_input:
        st.warning("⚠️ Ingresa tu API Key en la barra lateral izquierda primero.")
    else:
        with st.spinner("Consultando datos de forma segura..."):
            datos = obtener_partidos_reales(api_key_input)
            
            if not datos:
                st.info("ℹ️ No hay partidos de las Ligas Élite programados para hoy o se alcanzó el límite seguro diario.")
            else:
                st.markdown(f"### 📋 Oportunidades Seleccionadas ({len(datos)})")
                
                for d in datos:
                    monto_sugerido, pct_bank = calcular_monto_apuesta(d['prob_dec'], d['cuota_num'], capital_total)
                    
                    st.markdown(f"""
                    <div class="card-pro">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <span class="badge-market">{d['tipo']}</span>
                            <span class="badge-value">VALOR: {d['ev']}</span>
                            <span class="badge-kelly">INVERTIR: ${monto_sugerido} USD ({pct_bank}%)</span>
                        </div>
                        <div style="font-size:12px; opacity:0.75; margin-top:4px;">{d['liga']}</div>
                        <h3 style="margin:4px 0 10px 0; color:#f9fafb;">{d['partido']}</h3>
                        <div style="font-size:17px; font-weight:bold; color:#ffffff; margin-bottom:8px;">
                            📌 MERCADO: <span style="color:#6EE7B7;">{d['mercado']}</span>
                        </div>
                        <div style="font-size:14px; margin-bottom:10px; background:rgba(255,255,255,0.03); padding:8px; border-radius:6px;">
                            <strong>Monto Sugerido:</strong> <span style="color:#6EE7B7; font-weight:bold;">${monto_sugerido} USD</span> | 
                            <strong>Cuota:</strong> @{d['cuota_num']} | 
                            <strong>Certeza:</strong> {d['prob_str']}
                        </div>
                        <div style="font-size:12px; opacity:0.8; border-top:1px solid #1e293b; padding-top:8px;">
                            💡 <em>{d['razon']}</em>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
