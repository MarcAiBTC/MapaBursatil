import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timezone
import pytz
import pandas as pd
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

def create_world_map(market_data):
    """Crea el mapa mundial interactivo"""
    
    # Preparar datos para el mapa
    countries = []
    lats = []
    lons = []
    texts = []
    colors = []
    sizes = []
    
    for symbol, data in market_data.items():
        if data and symbol in MARKETS_CONFIG:
            config = MARKETS_CONFIG[symbol]
            
            # Datos del mercado
            price = data['price']
            change_pct = data['change_percent']
            ma200_trend = data['ma200_trend']
            
            # Status del mercado
            market_status = get_market_status(config['timezone'])
            status_emoji = "🟢" if market_status['is_open'] else "🔴"
            
            # Emoji climático
            weather_emoji = get_emoji_by_change(change_pct)
            
            # Texto del hover
            hover_text = f"""
<b>{config['name']}</b><br>
{weather_emoji} {change_pct:+.2f}%<br>
💰 ${price:,.2f}<br>
📈 MA200: {ma200_trend}<br>
{status_emoji} {market_status['status']}<br>
🕐 {market_status['next_action']}
            """.strip()
            
            countries.append(config['country'])
            lats.append(config['lat'])
            lons.append(config['lon'])
            texts.append(hover_text)
            colors.append(get_color_by_change(change_pct))
            sizes.append(abs(change_pct) * 5 + 15)  # Tamaño basado en volatilidad
    
    # Crear el mapa
    fig = go.Figure()
    
    # Añadir puntos de mercados
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        text=texts,
        mode='markers',
        marker=dict(
            size=sizes,
            color=colors,
            opacity=0.8,
            line=dict(width=2, color='white'),
            sizeref=2.*max(sizes)/(40.**2),
            sizemin=4
        ),
        hovertemplate='%{text}<extra></extra>',
        showlegend=False
    ))
    
    # Configurar el mapa
    fig.update_layout(
        title={
            'text': '🌍 Mapa Financiero Mundial en Tiempo Real',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2E86AB'}
        },
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            showocean=True,
            oceancolor='rgb(230, 245, 255)',
            showlakes=True,
            lakecolor='rgb(230, 245, 255)',
            showrivers=True,
            rivercolor='rgb(230, 245, 255)'
        ),
        height=600,
        margin=dict(t=60, b=0, l=0, r=0)
    )
    
    return fig

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
    
    # Mapa principal
    st.markdown("### 🗺️ Mapa Interactivo")
    fig = create_world_map(market_data)
    st.plotly_chart(fig, use_container_width=True)
    
    # Leyenda explicativa
    st.markdown("""
    **💡 Cómo usar el mapa:**
    - Pasa el cursor sobre cada punto para ver detalles
    - El tamaño del punto indica la volatilidad
    - Los colores representan el rendimiento actual
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
        💡 Herramienta diseñada para inversores inteligentes
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()