def analizar_partido_seguro(equipo_local, equipo_visitante, cuota_local, racha_local, racha_visitante, promedio_goles):
    print("=" * 60)
    print(f" ANÁLISIS DE RIESGO: {equipo_local} vs {equipo_visitante}")
    print("=" * 60)
    
    # Cálculo de puntos según los últimos resultados (G = 3 pts, E = 1 pt, P = 0 pts)
    puntos_local = racha_local.count("G") * 3 + racha_local.count("E")
    puntos_visitante = racha_visitante.count("G") * 3 + racha_visitante.count("E")
    
    print(f"1. Forma Reciente (Últimos 5 partidos):")
    print(f"   - {equipo_local}: {puntos_local} puntos (Racha: {racha_local})")
    print(f"   - {equipo_visitante}: {puntos_visitante} puntos (Racha: {racha_visitante})")
    print(f"2. Promedio combinado de goles estimado: {promedio_goles}")

    # ESCUDO ANTI-TRAMPA (Evita cuotas engañosas en favoritos irregulares)
    alerta_trampa = False
    if cuota_local < 1.60 and puntos_local < 9:
        alerta_trampa = True

    print(3 * " " + f"3. Verificación de Cuota ({cuota_local}):")

    if alerta_trampa:
        print("    🚨 ¡ALERTA ROJA: PARTIDO TRAMPA DETECTADO!")
        print(f"    -> La cuota para {equipo_local} es muy baja y su rendimiento reciente es irregular.")
        recomendacion = "❌ PROHIBIDO APOSTAR (Alto riesgo de tropiezo / Evitar favorito)"
        confianza = "0% - PELIGROSO"
    elif promedio_goles >= 2.2 and puntos_local >= puntos_visitante:
        print("    ✅ Estadísticas estables y favorables.")
        recomendacion = "✔️ APUESTA RESPONSABLE APROBADA (Mercado de goles o doble oportunidad)"
        confianza = "80% - SEGURO"
    else:
        print("    ⚠️ Estadísticas divididas o poco claras.")
        recomendacion = "⚠️ MEJOR PASAR DE LARGO (Conservar el dinero)"
        confianza = "40% - DUDOSO"

    print("-" * 60)
    print(f"💡 VEREDICTO FINAL PARA TU DECISIÓN:")
    print(f"   Acción: {recomendacion}")
    print(f"   Nivel de Confianza: {confianza}")
    print("=" * 60 + "\n")

# Ejemplo evaluando un escenario real de riesgo (como el tropiezo que tuvimos)
analizar_partido_seguro(
    equipo_local="Grêmio", 
    equipo_visitante="Bolívar", 
    cuota_local=1.37, 
    racha_local=["G", "P", "E", "G", "P"], 
    racha_visitante=["G", "G", "P", "E", "G"], 
    promedio_goles=2.1
)
