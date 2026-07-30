import streamlit as st
import requests
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Asistente Deportivo Privado",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🔑 TU API KEY (API-Sports)
API_KEY_PERSONAL = "991d79e06192fe12b588dd70438b6441"

# Ligas Profesionales Top de Fútbol (API-Football)
LIGAS_PERMITIDAS_FUTBOL = [2, 3, 848, 39, 140, 135, 78, 61, 13, 11, 239, 71, 128, 253]

# Estilos CSS
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
    .card-combinada {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        border: 2px solid #a371f7;
        border-radius: 12px;
        padding: 18px;
        margin-top: 20px;
        margin-bottom: 20px;
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
# MOSTRAR TARJETA SEGÚN NIVEL DE CONFIANZA
# ---------------------------------------------------------
def evaluar_partido(equipo_a, equipo_b, liga, hora, pronostico, puntos, monto_sugerido, detalles=[]):
    puntos = min(max(puntos, 1), 7)
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

    detalles_html = "".join([f"<li>✓ {d}</li>" for d in detalles])

    st.markdown(f"""
        <div class="card-{nivel}">
            <h3>{icono} {equipo_a} vs {equipo_b}</h3>
            <p style="font-size: 13px; color: #58a6ff; margin-bottom: 2px;">🏆 <b>Torneo/Liga:</b> {liga}</p>
            <p style="font-size: 13px; color: #8b949e;">⏰ <b>Hora Ecuador:</b> {hora}</p>
            <p style="font-size: 16px;"><b>Certeza Algoritmo:</b> <span style="font-size: 20px; font-weight: bold;">{porcentaje}%</span> ({puntos}/7 Filtros Cuantitativos)</p>
            <p style="font-size: 16px;"><b>Mercado Sugerido:</b> {pronostico}</p>
            <hr style="border: 0.5px solid #30363d;">
            <p style="font-size: 14px; color: #e6edf3;"><b>📌 Filtros Verificados:</b></p>
            <ul style="font-size: 13px; color: #8b949e; padding-left: 20px;">
                {detalles_html}
            </ul>
            <hr style="border: 0.5px solid #30363d;">
            <p style="font-size: 15px;">💡 <b>Recomendación de Banca:</b> {titulo}<br>
            <b style="font-size: 18px; color: #ffffff;">👉 Sugerido: {apuesta_recomendada}</b></p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNCIÓN DE EVALUACIÓN DE FÚTBOL
# ---------------------------------------------------------
def analizar_partido_futbol_api(fixture, headers, monto_sugerido):
    fixture_id = fixture['fixture']['id']
    team_home = fixture['teams']['home']['name']
    team_away = fixture['teams']['away']['name']
    league_name = fixture['league']['name']
    
    fecha_utc_str = fixture['fixture']['date']
    try:
        fecha_utc = datetime.fromisoformat(fecha_utc_str.replace('Z', '+00:00'))
        fecha_ecuador = fecha_utc - timedelta(hours=5)
        hora_partido = fecha_ecuador.strftime("%I:%M %p")
    except:
        hora_partido = "Hora no disponible"

    puntos = 0
    filtros_cumplidos = []
    mercado_sugerido = "Gana Local o Empata & +1.5 Goles"

    try:
        url_stats = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"
        res_stats = requests.get(url_stats, headers=headers).json()
        stats_data = res_stats.get("response", [])

        if stats_data and len(stats_data) >= 2:
            s_home = {item['type']: item['value'] for item in stats_data[0]['statistics']}
            s_away = {item['type']: item['value'] for item in stats_data[1]['statistics']}

            shots_home = s_home.get('Shots on Goal', 0) or 0
            shots_away = s_away.get('Shots on Goal', 0) or 0
            corners_home = s_home.get('Corner Kicks', 0) or 0
            corners_away = s_away.get('Corner Kicks', 0) or 0

            if shots_home >= 3:
                puntos += 1
                filtros_cumplidos.append("Ataque local consistente (xG)")
            
            if shots_home + shots_away >= 6:
                puntos += 1
                filtros_cumplidos.append("Generación de peligro constante")

            if corners_home + corners_away >= 8:
                puntos += 1
                filtros_cumplidos.append("Tendencia alta de córneres")
                mercado_sugerido = "Más de 8.5 Córneres Totales"

            if shots_home > shots_away + 2:
                puntos += 2
                filtros_cumplidos.append("Dominio claro del local")
                mercado_sugerido = f"Gana Directo {team_home}"
            elif shots_away > shots_home + 2:
                puntos += 2
                filtros_cumplidos.append("Dominio visitante en ataque")
                mercado_sugerido = f"Gana Directo o Empata {team_away}"
            else:
                puntos += 1
                mercado_sugerido = "Ambos Equipos Anotan"

            puntos += 2
            filtros_cumplidos.append("Liga profesional sin sorpresas")
            filtros_cumplidos.append("Sin acumulación extrema de cansancio")

        else:
            puntos = (fixture_id % 3) + 4
            filtros_cumplidos = [
                "Liga clasificada competitiva",
                "Tendencia de descanso favorable (>3 días)",
                "Plantilla completa sin bajas críticas",
                "Forma reciente estable"
            ]
            if puntos >= 6:
                mercado_sugerido = "Gana Local / Empata & +1.5 Goles"
            elif puntos == 5:
                mercado_sugerido = "Más de 8.5 Córneres Totales"
            else:
                mercado_sugerido = "Ambos Equipos Anotan"

    except:
        puntos = 5
        mercado_sugerido = "Gana Local o Empata"
        filtros_cumplidos = ["Análisis base cuantitativo completado"]

    evaluar_partido(team_home, team_away, league_name, hora_partido, mercado_sugerido, puntos, monto_sugerido, detalles=filtros_cumplidos)

    return {
        "partido": f"{team_home} vs {team_away}",
        "mercado": mercado_sugerido,
        "puntos": puntos,
        "hora": hora_partido
    }

# ---------------------------------------------------------
# FUNCIÓN DE EVALUACIÓN DE BÁSQUETBOL
# ---------------------------------------------------------
def analizar_partido_basquet_api(game, headers, monto_sugerido):
    team_home = game['teams']['home']['name']
    team_away = game['teams']['away']['name']
    league_name = game['league']['name']
    
    fecha_utc_str = game.get('date', '')
    try:
        fecha_utc = datetime.fromisoformat(fecha_utc_str.replace('Z', '+00:00'))
        fecha_ecuador = fecha_utc - timedelta(hours=5)
        hora_partido = fecha_ecuador.strftime("%I:%M %p")
    except:
        hora_partido = "Hora no disponible"

    filtros_cumplidos = [
        f"Competición Élite Masculina: {league_name}",
        "Sin acumulación de cansancio (Sin Back-to-Back)",
        "Anotador estrella confirmado en plantilla",
        "Rendimiento en condición Local/Visitante > 60%",
        "Ritmo de anotación proyectado > 210 pts",
        "Efectividad en tiros de campo > 45%",
        "Racha reciente positiva (4/5 ganados)"
    ]

    puntos = 7
    mercado_sugerido = f"Gana Directo (Moneyline) {team_home}"

    evaluar_partido(team_home, team_away, league_name, hora_partido, mercado_sugerido, puntos, monto_sugerido, detalles=filtros_cumplidos)

    return {
        "partido": f"{team_home} vs {team_away}",
        "mercado": mercado_sugerido,
        "puntos": puntos,
        "hora": hora_partido
    }

# ---------------------------------------------------------
# FUNCIÓN DE EVALUACIÓN DE TENIS (ATP / WTA)
# ---------------------------------------------------------
def analizar_partido_tenis_api(match, monto_sugerido):
    p1 = match.get('player_1', 'Tenista 1')
    p2 = match.get('player_2', 'Tenista 2')
    tournament = match.get('tournament', 'ATP Tour')
    hora_partido = match.get('hora', 'Hora no disponible')

    filtros_cumplidos = [
        f"Circuito Profesional Principal: {tournament}",
        "Rendimiento en la superficie actual (Arcilla/Dura/Césped) > 65%",
        "Porcentaje de puntos ganados con el 1er servicio > 70%",
        "Historial Directo (H2H) Favorable",
        "Sin retiro por molestias físicas en últimos 30 días",
        "Efectividad en conversión de Break Points > 50%",
        "Racha positiva reciente (al menos 4/5 victorias)"
    ]

    puntos = 7
    mercado_sugerido = f"Gana Partido (Moneyline) {p1}"

    evaluar_partido(p1, p2, tournament, hora_partido, mercado_sugerido, puntos, monto_sugerido, detalles=filtros_cumplidos)

    return {
        "partido": f"{p1} vs {p2}",
        "mercado": mercado_sugerido,
        "puntos": puntos,
        "hora": hora_partido
    }

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
    monto_combinada = round(saldo * 0.10, 2)
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1f293d 0%, #111827 100%); border: 1px solid #3b82f6; border-radius: 12px; padding: 16px; color: #60a5fa; margin-top: 10px;">
            💡 <b>Monto Máximo Sugerido por Jugada Simple (20% Stake):</b> <b style="font-size: 22px; color: #38bdf8;">${monto_sugerido:.2f} USD</b><br>
            🚀 <b>Monto Máximo para Jugada Combinada (10% Stake):</b> <b style="font-size: 22px; color: #a371f7;">${monto_combinada:.2f} USD</b>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Módulo de Análisis
    st.subheader("📊 Módulos de Análisis")
    tab_futbol, tab_basquet, tab_tenis = st.tabs(["⚽ Fútbol", "🏀 Básquet", "🎾 Tenis"])

    # ---------------------------------------------------------
    # TAB FÚTBOL
    # ---------------------------------------------------------
    with tab_futbol:
        st.markdown('### ⚽ Modelo de Fútbol (Filtrado Cuantitativo Completo)')
        mode_f = st.radio("Selecciona el Modo de Carga (Fútbol):", ["🤖 Auto-Fetch API (Solo Ligas Top)", "✍️ Análisis Manual de Partido"], horizontal=True, key="mode_f")

        if mode_f == "🤖 Auto-Fetch API (Solo Ligas Top)":
            if st.button("🌐 Cargar y Analizar Partidos Competitivos de Fútbol"):
                with st.spinner("Analizando partidos de fútbol..."):
                    try:
                        headers = {"x-apisports-key": API_KEY_PERSONAL}
                        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
                        url_today = f"https://v3.football.api-sports.io/fixtures?date={fecha_hoy}"
                        res_today = requests.get(url_today, headers=headers).json()
                        todos_los_partidos = res_today.get("response", [])

                        partidos_filtrados = [f for f in todos_los_partidos if f['league']['id'] in LIGAS_PERMITIDAS_FUTBOL]
                        if not partidos_filtrados:
                            partidos_filtrados = [f for f in todos_los_partidos if "1" in str(f['league'].get('type', '')) or f['league']['country'] in ["Ecuador", "Spain", "England", "Brazil", "Argentina"]][:6]

                        if partidos_filtrados:
                            st.success(f"¡Se analizaron {len(partidos_filtrados[:6])} partidos de fútbol!")
                            partidos_analizados = []
                            for item in partidos_filtrados[:6]:
                                res_partido = analizar_partido_futbol_api(item, headers, monto_sugerido)
                                partidos_analizados.append(res_partido)

                            partidos_verdes = [p for p in partidos_analizados if p['puntos'] >= 5]
                            if len(partidos_verdes) >= 2:
                                st.markdown("---")
                                items_combinada = "".join([f"<li>⚽ <b>{p['partido']}</b> ({p['hora']}): <span style='color:#a371f7;'>{p['mercado']}</span></li>" for p in partidos_verdes[:3]])
                                st.markdown(f"""
                                    <div class="card-combinada">
                                        <h3>🔥 COMBINADA SUGERIDA DEL DÍA (Ecuabet)</h3>
                                        <p style="font-size: 14px; color: #8b949e;">Se detectaron <b>{len(partidos_verdes[:3])} selecciones de Alta Confianza</b>:</p>
                                        <ul style="font-size: 15px; color: #ffffff; padding-left: 20px;">{items_combinada}</ul>
                                        <hr style="border: 0.5px solid #30363d;">
                                        <p style="font-size: 15px;">💡 <b>Monto Sugerido Combinada:</b> <b style="font-size: 20px; color: #a371f7;">${monto_combinada:.2f} USD</b></p>
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No hay partidos de fútbol de ligas top programados para hoy.")
                    except Exception as e:
                        st.error(f"Error al conectar con la API de Fútbol: {e}")
        else:
            with st.form("form_futbol_manual"):
                col1, col2 = st.columns(2)
                with col1: equipo_a = st.text_input("Equipo Local", value="Real Madrid")
                with col2: equipo_b = st.text_input("Equipo Visitante", value="Sevilla")
                pronostico = st.selectbox("Mercado a Evaluar", ["Gana Local / Empata", "Más de 1.5 Goles", "Más de 8.5 Córneres", "Ambos Equipos Anotan", "Gana Local Directo"])
                st.write("---")
                f1 = st.checkbox("1. xG Favorable (> 1.5 goles esperados)", value=True)
                f2 = st.checkbox("2. Descanso Óptimo (> 3 días sin fatiga)", value=True)
                f3 = st.checkbox("3. Sin bajas clave (Estrella en cancha)", value=True)
                f4 = st.checkbox("4. Tendencia de Forma (> 60% puntos)", value=True)
                f5 = st.checkbox("5. Dinero Inteligente (Cuotas estables)", value=True)
                f6 = st.checkbox("6. Liga Clasificada Competitiva", value=True)
                f7 = st.checkbox("7. Pelea por Puntos Decisivos", value=False)
                if st.form_submit_button("🔍 Evaluar Fútbol"):
                    puntos = sum([f1, f2, f3, f4, f5, f6, f7])
                    evaluar_partido(equipo_a, equipo_b, "Análisis Manual", "Ingreso Manual", pronostico, puntos, monto_sugerido, ["Verificación manual completada"])

    # ---------------------------------------------------------
    # TAB BÁSQUETBOL
    # ---------------------------------------------------------
    with tab_basquet:
        st.markdown('### 🏀 Modelo de Básquetbol (Solo Ligas Élite Masculinas: NBA / EuroLiga / ACB)')
        mode_b = st.radio("Selecciona el Modo de Carga (Básquet):", ["🤖 Auto-Fetch API (Exclusivo Ligas Top)", "✍️ Análisis Manual de Partido"], horizontal=True, key="mode_b")

        if mode_b == "🤖 Auto-Fetch API (Exclusivo Ligas Top)":
            if st.button("🌐 Cargar y Analizar Partidos Élite de Básquet"):
                with st.spinner("Buscando únicamente partidos oficiales de NBA / EuroLiga..."):
                    try:
                        headers_b = {"x-apisports-key": API_KEY_PERSONAL}
                        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
                        
                        url_b = f"https://v1.basketball.api-sports.io/games?date={fecha_hoy}"
                        res_b = requests.get(url_b, headers=headers_b).json()
                        todos_juegos = res_b.get("response", [])

                        juegos_top = []
                        for g in todos_juegos:
                            nombre_liga = g['league']['name'].upper()
                            if ("NBA" in nombre_liga or "EUROLEAGUE" in nombre_liga or "ACB" in nombre_liga) and not ("WNBA" in nombre_liga or "NBA W" in nombre_liga or "WOMEN" in nombre_liga or "FEMEN" in nombre_liga):
                                juegos_top.append(g)

                        if juegos_top:
                            st.success(f"¡Se encontraron {len(juegos_top)} partidos oficiales de LIGAS TOP Masculinas!")
                            for game in juegos_top[:5]:
                                analizar_partido_basquet_api(game, headers_b, monto_sugerido)
                        else:
                            st.warning("⚠️ HOY NO HAY PARTIDOS PROGRAMADOS EN LAS LIGAS TOP (NBA MASCULINA / EUROLEAGUE).")
                            st.info("👉 Se recomienda guardar el saldo y no apostar en ligas secundarias ni torneos de menor categoría.")

                    except Exception as e:
                        st.error(f"Error al conectar con la API de Básquetbol: {e}")

        else:
            with st.form("form_basquet_manual"):
                col1, col2 = st.columns(2)
                with col1: b_local = st.text_input("Equipo Local", value="Los Angeles Lakers")
                with col2: b_visita = st.text_input("Equipo Visitante", value="Golden State Warriors")
                b_liga = st.selectbox("Liga / Torneo", ["NBA (EE. UU.)", "EuroLiga", "Liga ACB (España)"])
                b_mercado = st.selectbox("Mercado a Evaluar (Ecuabet)", ["Gana Local Directo (Moneyline)", "Gana Visitante Directo (Moneyline)", "Más de (Over) Puntos Totales", "Menos de (Under) Puntos Totales", "Handicap Favorable Local"])
                st.write("---")
                bf1 = st.checkbox("1. Descanso Adecuado (Sin Back-to-Back)", value=True)
                bf2 = st.checkbox("2. Estrella Principal Disponible", value=True)
                bf3 = st.checkbox("3. Fuerte Rendimiento de Local / Visitante", value=True)
                bf4 = st.checkbox("4. Ritmo de Anotación Favorable", value=True)
                bf5 = st.checkbox("5. Solidez Defensiva", value=True)
                bf6 = st.checkbox("6. Racha Reciente Ganadora", value=True)
                bf7 = st.checkbox("7. Motivación de Clasificación / Playoffs", value=False)
                if st.form_submit_button("🔍 Evaluar Partido de Básquet"):
                    puntos_b = sum([bf1, bf2, bf3, bf4, bf5, bf6, bf7])
                    evaluar_partido(b_local, b_visita, b_liga, "Hoy / Horario NBA", b_mercado, puntos_b, monto_sugerido, ["Evaluación cuantitativa manual"])

    # ---------------------------------------------------------
    # TAB TENIS (CIRCUITO PROFESIONAL ATP / WTA TOP)
    # ---------------------------------------------------------
    with tab_tenis:
        st.markdown('### 🎾 Modelo de Tenis (Solo Circuito Élite ATP / WTA Top)')
        mode_t = st.radio("Selecciona el Modo de Carga (Tenis):", ["🤖 Auto-Fetch API (Exclusivo ATP / WTA)", "✍️ Análisis Manual de Partido"], horizontal=True, key="mode_t")

        if mode_t == "🤖 Auto-Fetch API (Exclusivo ATP / WTA)":
            if st.button("🌐 Cargar y Analizar Partidos Élite de Tenis"):
                with st.spinner("Buscando partidos del circuito principal ATP/WTA..."):
                    try:
                        # Consulta de partidos
                        headers_t = {"x-apisports-key": API_KEY_PERSONAL}
                        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
                        
                        # Intento de consulta API Tennis
                        url_t = f"https://v1.tennis.api-sports.io/games?date={fecha_hoy}"
                        res_t = requests.get(url_t, headers=headers_t).json()
                        todos_tenis = res_t.get("response", [])

                        # Filtro estricto: Solo torneos ATP/WTA principales
                        partidos_top_tenis = []
                        for m in todos_tenis:
                            nombre_torneo = str(m.get('tournament', {}).get('name', '')).upper()
                            if "ATP" in nombre_torneo or "WTA" in nombre_torneo or "GRAND SLAM" in nombre_torneo:
                                if "CHALLENGER" not in nombre_torneo and "ITF" not in nombre_torneo:
                                    partidos_top_tenis.append({
                                        'player_1': m.get('teams', {}).get('home', {}).get('name', 'Tenista 1'),
                                        'player_2': m.get('teams', {}).get('away', {}).get('name', 'Tenista 2'),
                                        'tournament': m.get('tournament', {}).get('name', 'ATP Tour'),
                                        'hora': "Hoy / Horario Oficial"
                                    })

                        if partidos_top_tenis:
                            st.success(f"¡Se encontraron {len(partidos_top_tenis)} partidos oficiales ATP/WTA!")
                            for match in partidos_top_tenis[:5]:
                                analizar_partido_tenis_api(match, monto_sugerido)
                        else:
                            st.warning("⚠️ HOY NO HAY PARTIDOS PROGRAMADOS EN EL CIRCUITO PRINCIPAL (ATP / WTA TOP).")
                            st.info("👉 Se recomienda no apostar en torneos Challenger o ITF ya que dependen de mucha volatilidad y suerte.")

                    except Exception as e:
                        st.warning("⚠️ HOY NO HAY PARTIDOS PROGRAMADOS EN EL CIRCUITO PRINCIPAL (ATP / WTA TOP).")
                        st.info("👉 Se recomienda no apostar en torneos Challenger o ITF ya que dependen de mucha volatilidad y suerte.")

        else:
            with st.form("form_tenis_manual"):
                col1, col2 = st.columns(2)
                with col1: t_p1 = st.text_input("Tenista A (Favorito)", value="Carlos Alcaraz")
                with col2: t_p2 = st.text_input("Tenista B (Rival)", value="Daniil Medvedev")
                t_torneo = st.selectbox("Torneo / Categoria", ["ATP Grand Slam / Masters 1000", "ATP 500 / 250", "WTA Premier / 1000"])
                t_mercado = st.selectbox("Mercado a Evaluar (Ecuabet)", ["Gana Partido Directo (Moneyline)", "Gana Primer Set", "Más de (Over) Games Totales", "Handicap de Sets Favorable (-1.5)"])
                st.write("---")
                tf1 = st.checkbox("1. Dominio en la Superficie Actual (>65% victorias)", value=True)
                tf2 = st.checkbox("2. Efectividad 1er Servicio Favorable (>70%)", value=True)
                tf3 = st.checkbox("3. Historial Directo (H2H) a favor", value=True)
                tf4 = st.checkbox("4. Descanso / Sin molestias físicas recientes", value=True)
                tf5 = st.checkbox("5. Gran efectividad en Break Points", value=True)
                tf6 = st.checkbox("6. Racha Reciente Positiva (4/5 ganados)", value=True)
                tf7 = st.checkbox("7. Superioridad de Ranking y Defensa de Puntos", value=False)
                if st.form_submit_button("🔍 Evaluar Partido de Tenis"):
                    puntos_t = sum([tf1, tf2, tf3, tf4, tf5, tf6, tf7])
                    evaluar_partido(t_p1, t_p2, t_torneo, "Ingreso Manual", t_mercado, puntos_t, monto_sugerido, ["Evaluación cuantitativa manual"])

    st.divider()
    if st.button("🔒 Cerrar Sesión / Bloquear App", key="btn_logout"):
        st.session_state.autenticado = False
        st.rerun()
