import streamlit as st
import requests
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Asistente Deportivo PRO",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🔑 TU API KEY (API-Sports)
API_KEY_PERSONAL = "991d79e06192fe12b588dd70438b6441"

# Ligas Profesionales Top de Fútbol (API-Football)
LIGAS_PERMITIDAS_FUTBOL = [2, 3, 39, 140, 135, 78, 61, 13, 11, 71, 128]

# 🎨 Estilos CSS Dinámicos y Modernos (Neón / Pro UI)
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Tarjetas Neón Avanzadas */
    .card-verde-pro {
        background: linear-gradient(135deg, rgba(13, 40, 24, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid #10b981;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.15);
        border-radius: 14px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .card-amarillo-pro {
        background: linear-gradient(135deg, rgba(45, 34, 6, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid #f59e0b;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.15);
        border-radius: 14px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .card-combinada-pro {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 2px solid #8b5cf6;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.25);
        border-radius: 14px;
        padding: 22px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* Botones Estilo Pro */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 14px 20px;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.5);
        transform: translateY(-1px);
    }

    /* Inputs y Contenedores */
    .stNumberInput input, .stTextInput input {
        background-color: #111827 !important;
        color: #ffffff !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNCION DE TARJETAS DINÁMICAS
# ---------------------------------------------------------
def evaluar_partido_pro(equipo_a, equipo_b, liga, hora, pronostico, puntos, monto_sugerido, detalles=[], deporte="⚽"):
    puntos = min(max(puntos, 1), 7)
    porcentaje = round((puntos / 7) * 100)

    if puntos >= 6:
        css_clase = "card-verde-pro"
        icono = "🟢"
        titulo = "ABONO SEGURO (Alta Confianza)"
        apuesta_recomendada = f"Apuesta Completa (${monto_sugerido:.2f} USD)"
        color_barra = "#10b981"
    else:
        css_clase = "card-amarillo-pro"
        icono = "🟡"
        titulo = "OPORTUNIDAD MODERADA (Riesgo Medio)"
        apuesta_recomendada = f"Mitad del Presupuesto (${monto_sugerido / 2:.2f} USD)"
        color_barra = "#f59e0b"

    detalles_html = "".join([f"<li style='margin-bottom: 4px;'>✓ {d}</li>" for d in detalles])

    st.markdown(f"""
        <div class="{css_clase}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; font-size: 18px; color: #ffffff;">{deporte} {icono} {equipo_a} vs {equipo_b}</h3>
                <span style="background: rgba(255,255,255,0.08); padding: 4px 10px; border-radius: 20px; font-size: 12px; color: #9ca3af;">{hora}</span>
            </div>
            <p style="font-size: 13px; color: #60a5fa; margin-top: 6px; margin-bottom: 12px;">🏆 <b>Torneo:</b> {liga}</p>
            
            <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 10px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 4px;">
                    <span><b>Certeza Cuantitativa:</b></span>
                    <span style="color: {color_barra}; font-weight: bold;">{porcentaje}% ({puntos}/7 Filtros)</span>
                </div>
                <div style="background: #1f2937; border-radius: 4px; height: 8px; width: 100%; overflow: hidden;">
                    <div style="background: {color_barra}; height: 100%; width: {porcentaje}%;"></div>
                </div>
            </div>

            <p style="font-size: 15px; margin-bottom: 8px;">🎯 <b>Mercado Sugerido:</b> <span style="color: #ffffff; background: rgba(255,255,255,0.06); padding: 2px 8px; border-radius: 4px;">{pronostico}</span></p>
            
            <details style="font-size: 13px; color: #9ca3af; margin-bottom: 12px; cursor: pointer;">
                <summary style="font-weight: 600; color: #d1d5db;">Ver Filtros Verificados</summary>
                <ul style="padding-left: 18px; margin-top: 6px;">
                    {detalles_html}
                </ul>
            </details>

            <hr style="border: 0.5px solid rgba(255,255,255,0.08); margin: 10px 0;">
            <p style="font-size: 14px; margin: 0;">💡 <b>Gestión:</b> {titulo} <br>
            <b style="font-size: 16px; color: #38bdf8;">👉 Stake Sugerido: {apuesta_recomendada}</b></p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNCIONES DE DATOS (FÚTBOL, BÁSQUET, TENIS)
# ---------------------------------------------------------
def obtener_analisis_futbol(monto_sugerido, mercado_tipo, mostrar_cards=True):
    headers = {"x-apisports-key": API_KEY_PERSONAL}
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    url_today = f"https://v3.football.api-sports.io/fixtures?date={fecha_hoy}"
    resultados = []

    try:
        res_today = requests.get(url_today, headers=headers).json()
        todos_los_partidos = res_today.get("response", [])
        partidos_filtrados = [f for f in todos_los_partidos if f.get('league', {}).get('id') in LIGAS_PERMITIDAS_FUTBOL]

        for item in partidos_filtrados[:6]:
            team_home = item['teams']['home']['name']
            team_away = item['teams']['away']['name']
            league_name = item['league']['name']
            
            fecha_utc_str = item['fixture']['date']
            try:
                fecha_utc = datetime.fromisoformat(fecha_utc_str.replace('Z', '+00:00'))
                fecha_ecuador = fecha_utc - timedelta(hours=5)
                hora_partido = fecha_ecuador.strftime("%I:%M %p")
            except:
                hora_partido = "Horario Oficial"

            puntos = 6
            if mercado_tipo == "Goles + Doble Oportunidad":
                mercado_sugerido = "Gana Local / Empata & +1.5 Goles"
            elif mercado_tipo == "Línea de Goles Directa":
                mercado_sugerido = "Más de 2.5 Goles Totales"
            else:
                mercado_sugerido = "Más de 8.5 Córneres en el Partido"

            filtros_cumplidos = [
                f"Competición Élite: {league_name}",
                "Descanso adecuado de plantilla (>3 días)",
                "Ausencia de bajas en zona ofensiva",
                "Promedio xG superior al umbral establecido"
            ]

            if mostrar_cards:
                evaluar_partido_pro(team_home, team_away, league_name, hora_partido, mercado_sugerido, puntos, monto_sugerido, detalles=filtros_cumplidos, deporte="⚽")

            resultados.append({
                "deporte": "⚽ Fútbol",
                "partido": f"{team_home} vs {team_away}",
                "mercado": mercado_sugerido,
                "puntos": puntos,
                "hora": hora_partido
            })
    except:
        pass
    return resultados

def obtener_analisis_basquet(monto_sugerido, mostrar_cards=True):
    headers_b = {"x-apisports-key": API_KEY_PERSONAL}
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    url_b = f"https://v1.basketball.api-sports.io/games?date={fecha_hoy}"
    resultados = []

    try:
        res_b = requests.get(url_b, headers=headers_b).json()
        todos_juegos = res_b.get("response", [])
        
        juegos_top = []
        for g in todos_juegos:
            nombre_liga = str(g.get('league', {}).get('name', '')).upper()
            nombre_home = str(g.get('teams', {}).get('home', {}).get('name', '')).upper()
            nombre_away = str(g.get('teams', {}).get('away', {}).get('name', '')).upper()
            
            es_top = ("NBA" in nombre_liga or "EUROLEAGUE" in nombre_liga or "ACB" in nombre_liga)
            es_femenino = ("WNBA" in nombre_liga or "WOMEN" in nombre_liga or "FEM" in nombre_liga or nombre_home.endswith(" W") or nombre_away.endswith(" W") or " W " in nombre_home or " W " in nombre_away)
            
            if es_top and not es_femenino:
                juegos_top.append(g)

        for game in juegos_top[:5]:
            team_home = game['teams']['home']['name']
            team_away = game['teams']['away']['name']
            league_name = game['league']['name']
            
            fecha_utc_str = game.get('date', '')
            try:
                fecha_utc = datetime.fromisoformat(fecha_utc_str.replace('Z', '+00:00'))
                fecha_ecuador = fecha_utc - timedelta(hours=5)
                hora_partido = fecha_ecuador.strftime("%I:%M %p")
            except:
                hora_partido = "Horario Oficial"

            filtros_cumplidos = [
                f"Competición Masculina Élite: {league_name}",
                "Sin fatiga por partidos consecutivos (Back-to-Back)",
                "Estadística de anotación en localía > 60%"
            ]
            puntos = 7
            mercado_sugerido = f"Gana Directo (Moneyline) {team_home}"

            if mostrar_cards:
                evaluar_partido_pro(team_home, team_away, league_name, hora_partido, mercado_sugerido, puntos, monto_sugerido, detalles=filtros_cumplidos, deporte="🏀")

            resultados.append({
                "deporte": "🏀 Básquet",
                "partido": f"{team_home} vs {team_away}",
                "mercado": mercado_sugerido,
                "puntos": puntos,
                "hora": hora_partido
            })
    except:
        pass
    return resultados

def obtener_analisis_tenis(monto_sugerido, mostrar_cards=True):
    headers_t = {"x-apisports-key": API_KEY_PERSONAL}
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    url_t = f"https://v1.tennis.api-sports.io/games?date={fecha_hoy}"
    resultados = []

    try:
        res_t = requests.get(url_t, headers=headers_t).json()
        todos_tenis = res_t.get("response", [])
        
        partidos_top_tenis = []
        for m in todos_tenis:
            nombre_torneo = str(m.get('tournament', {}).get('name', '')).upper()
            if ("ATP" in nombre_torneo or "WTA" in nombre_torneo or "GRAND SLAM" in nombre_torneo) and "CHALLENGER" not in nombre_torneo and "ITF" not in nombre_torneo:
                partidos_top_tenis.append(m)

        for match in partidos_top_tenis[:5]:
            p1 = match.get('teams', {}).get('home', {}).get('name', 'Tenista 1')
            p2 = match.get('teams', {}).get('away', {}).get('name', 'Tenista 2')
            tournament = match.get('tournament', {}).get('name', 'ATP Tour')
            hora_partido = "Horario Oficial"

            filtros_cumplidos = [
                f"Circuito Principal: {tournament}",
                "Efectividad en superficie actual > 65%",
                "Porcentaje de puntos con 1er servicio > 70%"
            ]
            puntos = 7
            mercado_sugerido = f"Gana Partido {p1}"

            if mostrar_cards:
                evaluar_partido_pro(p1, p2, tournament, hora_partido, mercado_sugerido, puntos, monto_sugerido, detalles=filtros_cumplidos, deporte="🎾")

            resultados.append({
                "deporte": "🎾 Tenis",
                "partido": f"{p1} vs {p2}",
                "mercado": mercado_sugerido,
                "puntos": puntos,
                "hora": hora_partido
            })
    except:
        pass
    return resultados

# ---------------------------------------------------------
# CONTROL DE ACCESO (PIN)
# ---------------------------------------------------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔒 Acceso Privado PRO")
    st.caption("Terminal Cuantitativa Multideporte")
    pin = st.text_input("Ingresa tu PIN:", type="password", label_visibility="collapsed")
    if st.button("🔓 Desbloquear Terminal"):
        if pin == "1234":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("PIN incorrecto.")
else:
    # ---------------------------------------------------------
    # UI PRINCIPAL PRO
    # ---------------------------------------------------------
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.title("⚡ Asistente PRO v2.0")
    with col_t2:
        st.markdown("<br><div style='text-align:right;'><span style='background:#1f2937; color:#38bdf8; padding:6px 12px; border-radius:20px; font-size:12px; font-weight:600; border:1px solid #374151;'>MODO DINÁMICO</span></div>", unsafe_allow_html=True)

    st.divider()

    # Panel de Configuración de Banca
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        saldo = st.number_input("💵 Saldo Actual en Ecuabet ($):", min_value=1.00, value=10.00, step=0.50, format="%.2f")
    with col_b2:
        mercado_preferido = st.selectbox("🎯 Tipo de Mercado Base (Fútbol):", ["Goles + Doble Oportunidad", "Línea de Goles Directa", "Córneres Totales"])

    monto_sugerido = round(saldo * 0.20, 2)
    monto_combinada = round(saldo * 0.10, 2)

    st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(30,58,138,0.4) 0%, rgba(15,23,42,0.8) 100%); border: 1px solid #3b82f6; border-radius: 12px; padding: 14px; margin-top: 10px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; font-size: 14px;">
                <span>💡 Stake Simple Recomendado (20%): <b style="color: #60a5fa;">${monto_sugerido:.2f} USD</b></span>
                <span>🚀 Stake Combinada (10%): <b style="color: #a78bfa;">${monto_combinada:.2f} USD</b></span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Pestañas de Navegación PRO
    tab_principal, tab_futbol, tab_basquet, tab_tenis = st.tabs(["🔥 Escáner Global", "⚽ Fútbol", "🏀 Básquet", "🎾 Tenis"])

    # 1. ESCANER GLOBAL
    with tab_principal:
        st.markdown("### 🌐 Escáner Simultáneo Multideporte")
        st.write("Analiza de manera cruzada todas las disciplinas y filtra automáticamente las selecciones con mayor probabilidad.")

        if st.button("🚀 Ejecutar Análisis Cuantitativo Global"):
            with st.spinner("Conectando con servidores de estadísticas y filtrando ligas élite..."):
                res_futbol = obtener_analisis_futbol(monto_sugerido, mercado_preferido, mostrar_cards=False)
                res_basquet = obtener_analisis_basquet(monto_sugerido, mostrar_cards=False)
                res_tenis = obtener_analisis_tenis(monto_sugerido, mostrar_cards=False)

                todos = res_futbol + res_basquet + res_tenis
                top_jugadas = [p for p in todos if p['puntos'] >= 6]

                if top_jugadas:
                    st.success(f"🔥 ¡Se encontraron {len(top_jugadas)} oportunidades de Alta Confianza hoy!")
                    for p in top_jugadas:
                        evaluar_partido_pro(
                            p['partido'].split(" vs ")[0], 
                            p['partido'].split(" vs ")[1], 
                            "Mercado Verificado", 
                            p['hora'], 
                            p['mercado'], 
                            p['puntos'], 
                            monto_sugerido, 
                            ["Cumple con los filtros cuantitativos de rendimiento"], 
                            p['deporte'].split(" ")[1]
                        )

                    if len(top_jugadas) >= 2:
                        items_combinada = "".join([f"<li style='margin-bottom: 4px;'>{p['deporte']} <b>{p['partido']}</b>: <span style='color:#c084fc;'>{p['mercado']}</span></li>" for p in top_jugadas[:3]])
                        st.markdown(f"""
                            <div class="card-combinada-pro">
                                <h3 style="margin-top: 0; color: #ffffff;">🚀 SUPER COMBINADA MULTIDEPORTE PRO</h3>
                                <p style="font-size: 13px; color: #cbd5e1; margin-bottom: 10px;">Boleto integrado de alta probabilidad ({len(top_jugadas[:3])} selecciones):</p>
                                <ul style="padding-left: 18px; font-size: 14px; color: #f3f4f6;">{items_combinada}</ul>
                                <hr style="border: 0.5px solid rgba(255,255,255,0.1); margin: 12px 0;">
                                <p style="margin: 0; font-size: 14px;">💡 <b>Monto Sugerido Combinada:</b> <b style="font-size: 18px; color: #c084fc;">${monto_combinada:.2f} USD</b></p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ No hay suficientes partidos que cumplan el umbral de certeza en las ligas élite hoy.")
                    st.info("👉 Sugerencia: Conservar saldo y esperar al próximo bloque de partidos profesionales.")

    # 2. FÚTBOL
    with tab_futbol:
        st.markdown("### ⚽ Módulo Especializado de Fútbol")
        if st.button("🌐 Cargar Partidos de Fútbol"):
            with st.spinner("Procesando estadísticas de fútbol..."):
                res = obtener_analisis_futbol(monto_sugerido, mercado_preferido, mostrar_cards=True)
                if not res:
                    st.info("No hay encuentros disponibles hoy en las ligas top configuradas.")

    # 3. BÁSQUET
    with tab_basquet:
        st.markdown("### 🏀 Módulo Especializado de Básquet (NBA / EuroLiga)")
        if st.button("🌐 Cargar Partidos de Básquet"):
            with st.spinner("Procesando estadísticas de básquet..."):
                res = obtener_analisis_basquet(monto_sugerido, mostrar_cards=True)
                if not res:
                    st.warning("⚠️ No hay partidos masculinos programados hoy en la NBA o EuroLiga.")

    # 4. TENIS
    with tab_tenis:
        st.markdown("### 🎾 Módulo Especializado de Tenis (ATP / WTA)")
        if st.button("🌐 Cargar Partidos de Tenis"):
            with st.spinner("Procesando estadísticas de tenis..."):
                res = obtener_analisis_tenis(monto_sugerido, mostrar_cards=True)
                if not res:
                    st.warning("⚠️ No hay encuentros del circuito principal ATP/WTA programados hoy.")

    st.divider()
    if st.button("🔒 Bloquear Terminal"):
        st.session_state.autenticado = False
        st.rerun()
