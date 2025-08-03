import streamlit as st
import pandas as pd
from datetime import datetime, timezone
import pytz
from data_utils import get_market_data, get_market_status, MARKETS_CONFIG
import time

# Configuración de la página
st.set_page_config(
    page_title="Mapa Financiero Mundial",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_emoji_by_change(change_pct):
    """Determina el emoji según el cambio porcentual"""
    if change_pct > 1:
        return "☀️"  # Subida fuerte
    elif change_pct > 0:
        return "🌤️"  # Subida leve
    elif change_pct > -1:
        return "☁️"  # Bajada leve
    else:
        return "🌩️"  # Bajada fuerte

def get_color_by_change(change_pct):
    """Determina el color según el cambio porcentual"""
    if change_pct > 1:
        return "#00C851"  # Verde fuerte
    elif change_pct > 0:
        return "#7CB342"  # Verde claro
    elif change_pct > -1:
        return "#FF8A65"  # Naranja claro
    else:
        return "#FF1744"  # Rojo fuerte

def create_visual_map(market_data):
    """Crea un mapa visual usando componentes de Streamlit"""
    
    # Organizar mercados por regiones
    regions = {
        "🇺🇸 América del Norte": ["^GSPC", "^IXIC", "^GSPTSE"],
        "🇪🇺 Europa": ["^FTSE", "^GDAXI", "^FCHI", "^IBEX"],
        "🇯🇵 Asia-Pacífico": ["^N225", "000001.SS", "^HSI", "^AXJO", "^KS11", "^TWII", "^NSEI"],
        "🇧🇷 América Latina": ["^BVSP"]
    }
    
    st.markdown("### 🗺️ Mapa Financiero Mundial")
    
    for region, symbols in regions.items():
        st.markdown(f"#### {region}")
        
        # Crear columnas para esta región
        cols = st.columns(len(symbols))
        
        for i, symbol in enumerate(symbols):
            if symbol in market_data and market_data[symbol]:
                data = market_data[symbol]
                config = MARKETS_CONFIG[symbol]
                
                with cols[i]:
                    # Datos del mercado
                    change_pct = data['change_percent']
                    price = data['price']
                    ma200_trend = data['ma200_trend']
                    
                    # Status del mercado
                    market_status = get_market_status(config['timezone'])
                    status_color = "🟢" if market_status['is_open'] else "🔴"
                    
                    # Emoji climático
                    weather_emoji = get_emoji_by_change(change_pct)
                    color = get_color_by_change(change_pct)
                    
                    # Crear tarjeta visual
                    st.markdown(f"""
                    <div style="
                        border: 2px solid {color};
                        border-radius: 10px;
                        padding: 15px;
                        margin: 5px;
                        background: linear-gradient(135deg, {color}15, {color}05);
                        text-align: center;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    ">
                        <h4 style="margin:0; color: {color};">{weather_emoji} {config['name'].split('(')[0].strip()}</h4>
                        <h2 style="margin:5px 0; color: {color};">{change_pct:+.2f}%</h2>
                        <p style="margin:2px 0; font-size:14px;"><strong>${price:,.2f}</strong></p>
                        <p style="margin:2px 0; font-size:12px;">📈 {ma200_trend}</p>
                        <p style="margin:2px 0; font-size:12px;">{status_color} {market_status['status']}</p>
                        <p style="margin:2px 0; font-size:11px; color:#666;">{market_status['next_action']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")

def create_world_map_alternative(market_data):
    """Mapa mundial simplificado usando emojis y texto"""
    
    st.markdown("### 🌍 Vista Global de Mercados")
    
    # Crear un mapa de texto estilizado
    map_html = """
    <div style="background: linear-gradient(180deg, #e3f2fd 0%, #bbdefb 100%); 
                border-radius: 15px; padding: 30px; margin: 20px 0;">
        <h3 style="text-align: center; color: #1976d2; margin-bottom: 30px;">
            🌍 Estado Global de Mercados Bursátiles
        </h3>
    """
    
    # Organizar por zonas horarias/regiones geográficas
    zones = [
        ("🌅 Asia-Pacífico", ["^N225", "000001.SS", "^HSI", "^AXJO", "^KS11", "^TWII", "^NSEI"]),
        ("🌍 Europa", ["^FTSE", "^GDAXI", "^FCHI", "^IBEX"]),
        ("🌎 América", ["^GSPC", "^IXIC", "^GSPTSE", "^BVSP"])
    ]
    
    for zone_name, symbols in zones:
        map_html += f"""
        <div style="margin: 20px 0; padding: 20px; background: rgba(255,255,255,0.7); 
                    border-radius: 10px; border-left: 5px solid #1976d2;">
            <h4 style="color: #1976d2; margin-bottom: 15px;">{zone_name}</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center;">
        """
        
        for symbol in symbols:
            if symbol in market_data and market_data[symbol]:
                data = market_data[symbol]
                config = MARKETS_CONFIG[symbol]
                
                change_pct = data['change_percent']
                weather_emoji = get_emoji_by_change(change_pct)
                color = get_color_by_change(change_pct)
                market_status = get_market_status(config['timezone'])
                status_emoji = "🟢" if market_status['is_open'] else "🔴"
                
                map_html += f"""
                <div style="background: white; border-radius: 8px; padding: 10px; 
                           min-width: 120px; text-align: center; border: 2px solid {color};
                           box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-size: 24px;">{weather_emoji}</div>
                    <div style="font-weight: bold; font-size: 12px; color: #333;">
                        {config['name'].split('(')[0].strip()[:8]}
                    </div>
                    <div style="color: {color}; font-weight: bold; font-size: 14px;">
                        {change_pct:+.1f}%
                    </div>
                    <div style="font-size: 10px; color: #666;">
                        {status_emoji} {market_status['status'][:6]}
                    </div>
                </div>
                """
        
        map_html += """
            </div>
        </div>
        """
    
    map_html += "</div>"
    
    st.markdown(map_html, unsafe_allow_html=True)

def create_summary_cards(market_data):
    """Crea tarjetas resumen de los mercados"""
    
    # Contar mercados por estado
    strong_up = sum(1 for data in market_data.values() 
                   if data and data['change_percent'] > 1)
    light_up = sum(1 for data in market_data.values() 
                  if data and 0 < data['change_percent'] <= 1)
    light_down = sum(1 for data in market_data.values() 
                    if data and -1 <= data['change_percent'] < 0)
    strong_down = sum(1 for data in market_data.values() 
                     if data and data['change_percent'] < -1)
    
    # Mercados abiertos
    open_markets = sum(1 for symbol in market_data.keys() 
                      if symbol in MARKETS_CONFIG and 
                      get_market_status(MARKETS_CONFIG[symbol]['timezone'])['is_open'])
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="☀️ Subida Fuerte",
            value=f"{strong_up} mercados",
            delta=f"{strong_up/len([d for d in market_data.values() if d])*100:.1f}%"
        )
    
    with col2:
        st.metric(
            label="🌤️ Subida Leve",
            value=f"{light_up} mercados",
            delta=f"{light_up/len([d for d in market_data.values() if d])*100:.1f}%"
        )
    
    with col3:
        st.metric(
            label="☁️ Bajada Leve",
            value=f"{light_down} mercados",
            delta=f"-{light_down/len([d for d in market_data.values() if d])*100:.1f}%"
        )
    
    with col4:
        st.metric(
            label="🌩️ Bajada Fuerte",
            value=f"{strong_down} mercados",
            delta=f"-{strong_down/len([d for d in market_data.values() if d])*100:.1f}%"
        )
    
    with col5:
        st.metric(
            label="🟢 Mercados Abiertos",
            value=f"{open_markets}/{len(MARKETS_CONFIG)}",
            delta=f"{open_markets/len(MARKETS_CONFIG)*100:.1f}%"
        )

def create_detailed_table(market_data):
    """Crea tabla detallada de mercados"""
    
    table_data = []
    
    for symbol, data in market_data.items():
        if data and symbol in MARKETS_CONFIG:
            config = MARKETS_CONFIG[symbol]
            market_status = get_market_status(config['timezone'])
            
            table_data.append({
                'Mercado': config['name'],
                'Clima': get_emoji_by_change(data['change_percent']),
                'Precio': f"${data['price']:,.2f}",
                'Cambio (%)': f"{data['change_percent']:+.2f}%",
                'MA200': data['ma200_trend'],
                'Estado': "🟢 Abierto" if market_status['is_open'] else "🔴 Cerrado",
                'Próxima Acción': market_status['next_action']
            })
    
    # Ordenar por cambio porcentual (descendente)
    table_data.sort(key=lambda x: float(x['Cambio (%)'].replace('%', '').replace('+', '')), reverse=True)
    
    df = pd.DataFrame(table_data)
    
    # Mostrar tabla con estilo
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Clima': st.column_config.TextColumn('🌤️', width="small"),
            'Cambio (%)': st.column_config.TextColumn('📈 Cambio (%)', width="medium"),
            'MA200': st.column_config.TextColumn('📊 MA200', width="medium"),
            'Estado': st.column_config.TextColumn('🚦 Estado', width="medium")
        }
    )

def main():
    """Función principal de la aplicación"""
    
    # Título principal
    st.title("🌍 Mapa Financiero Mundial")
    st.markdown("### Tu radar bursátil global en tiempo real")
    
    # Sidebar con información
    with st.sidebar:
        st.header("📊 Cómo Interpretar")
        
        st.markdown("""
        **🌤️ Emoticonos Climáticos:**
        - ☀️ Subida fuerte (>1%)
        - 🌤️ Subida leve (0-1%)
        - ☁️ Bajada leve (0 a -1%)
        - 🌩️ Bajada fuerte (<-1%)
        
        **📈 Indicadores:**
        - **Precio**: Valor actual del índice
        - **MA200**: Media móvil 200 períodos
        - **Estado**: Mercado abierto/cerrado
        
        **🎯 Utilidad:**
        Identifica rápidamente oportunidades y riesgos globales para optimizar tu estrategia de inversión.
        """)
        
        st.markdown("---")
        st.info("💡 **Versión Compatible**: Esta versión funciona sin dependencias externas problemáticas.")
        
        # Botón de actualización
        if st.button("🔄 Actualizar Datos", type="primary"):
            st.rerun()
        
        st.markdown(f"**⏰ Última actualización:**  \n{datetime.now().strftime('%H:%M:%S')}")
    
    # Mostrar mensaje de carga
    with st.spinner("📡 Obteniendo datos de mercados globales..."):
        market_data = get_market_data()
    
    # Verificar si hay datos
    if not any(market_data.values()):
        st.error("❌ No se pudieron obtener datos de mercado. Intenta nuevamente en unos minutos.")
        return
    
    # Tarjetas resumen
    st.markdown("### 📊 Resumen Global")
    create_summary_cards(market_data)
    
    st.markdown("---")
    
    # Mapa visual alternativo
    create_world_map_alternative(market_data)
    
    st.markdown("---")
    
    # Mapa regional detallado
    create_visual_map(market_data)
    
    # Leyenda explicativa
    st.markdown("""
    **💡 Cómo interpretar:**
    - Los colores y emoticonos representan el rendimiento actual
    - El tamaño indica la importancia del mercado
    - Los estados muestran si el mercado está operando
    """)
    
    st.markdown("---")
    
    # Tabla detallada
    st.markdown("### 📋 Detalles por Mercado")
    create_detailed_table(market_data)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        🚀 <b>Mapa Financiero Mundial</b> | Datos proporcionados por Yahoo Finance<br>
        💡 Herramienta diseñada para inversores inteligentes | Versión Compatible
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
