import yfinance as yf
import pandas as pd
from datetime import datetime, timezone, time
import pytz
import streamlit as st

# Configuración de mercados principales
MARKETS_CONFIG = {
    '^GSPC': {  # S&P 500
        'name': 'S&P 500 (NYSE)',
        'country': 'United States',
        'timezone': 'America/New_York',
        'lat': 40.7128,
        'lon': -74.0060,
        'open_time': time(9, 30),
        'close_time': time(16, 0)
    },
    '^IXIC': {  # NASDAQ
        'name': 'NASDAQ',
        'country': 'United States',
        'timezone': 'America/New_York',
        'lat': 40.7589,
        'lon': -73.9851,
        'open_time': time(9, 30),
        'close_time': time(16, 0)
    },
    '^FTSE': {  # FTSE 100
        'name': 'FTSE 100 (Londres)',
        'country': 'United Kingdom',
        'timezone': 'Europe/London',
        'lat': 51.5074,
        'lon': -0.1278,
        'open_time': time(8, 0),
        'close_time': time(16, 30)
    },
    '^GDAXI': {  # DAX
        'name': 'DAX (Frankfurt)',
        'country': 'Germany',
        'timezone': 'Europe/Berlin',
        'lat': 50.1109,
        'lon': 8.6821,
        'open_time': time(9, 0),
        'close_time': time(17, 30)
    },
    '^FCHI': {  # CAC 40
        'name': 'CAC 40 (París)',
        'country': 'France',
        'timezone': 'Europe/Paris',
        'lat': 48.8566,
        'lon': 2.3522,
        'open_time': time(9, 0),
        'close_time': time(17, 30)
    },
    '^IBEX': {  # IBEX 35
        'name': 'IBEX 35 (Madrid)',
        'country': 'Spain',
        'timezone': 'Europe/Madrid',
        'lat': 40.4168,
        'lon': -3.7038,
        'open_time': time(9, 0),
        'close_time': time(17, 30)
    },
    '^N225': {  # Nikkei 225
        'name': 'Nikkei 225 (Tokio)',
        'country': 'Japan',
        'timezone': 'Asia/Tokyo',
        'lat': 35.6762,
        'lon': 139.6503,
        'open_time': time(9, 0),
        'close_time': time(15, 0)
    },
    '000001.SS': {  # Shanghai Composite
        'name': 'Shanghai Composite',
        'country': 'China',
        'timezone': 'Asia/Shanghai',
        'lat': 31.2304,
        'lon': 121.4737,
        'open_time': time(9, 30),
        'close_time': time(15, 0)
    },
    '^HSI': {  # Hang Seng
        'name': 'Hang Seng (Hong Kong)',
        'country': 'Hong Kong',
        'timezone': 'Asia/Hong_Kong',
        'lat': 22.3193,
        'lon': 114.1694,
        'open_time': time(9, 30),
        'close_time': time(16, 0)
    },
    '^BVSP': {  # Bovespa
        'name': 'Bovespa (São Paulo)',
        'country': 'Brazil',
        'timezone': 'America/Sao_Paulo',
        'lat': -23.5505,
        'lon': -46.6333,
        'open_time': time(10, 0),
        'close_time': time(17, 0)
    },
    '^GSPTSE': {  # TSX
        'name': 'TSX (Toronto)',
        'country': 'Canada',
        'timezone': 'America/Toronto',
        'lat': 43.6532,
        'lon': -79.3832,
        'open_time': time(9, 30),
        'close_time': time(16, 0)
    },
    '^AXJO': {  # ASX 200
        'name': 'ASX 200 (Sídney)',
        'country': 'Australia',
        'timezone': 'Australia/Sydney',
        'lat': -33.8688,
        'lon': 151.2093,
        'open_time': time(10, 0),
        'close_time': time(16, 0)
    },
    '^KS11': {  # KOSPI
        'name': 'KOSPI (Seúl)',
        'country': 'South Korea',
        'timezone': 'Asia/Seoul',
        'lat': 37.5665,
        'lon': 126.9780,
        'open_time': time(9, 0),
        'close_time': time(15, 30)
    },
    '^TWII': {  # Taiwan Weighted
        'name': 'TWII (Taipéi)',
        'country': 'Taiwan',
        'timezone': 'Asia/Taipei',
        'lat': 25.0330,
        'lon': 121.5654,
        'open_time': time(9, 0),
        'close_time': time(13, 30)
    },
    '^NSEI': {  # Nifty 50
        'name': 'Nifty 50 (Mumbai)',
        'country': 'India',
        'timezone': 'Asia/Kolkata',
        'lat': 19.0760,
        'lon': 72.8777,
        'open_time': time(9, 15),
        'close_time': time(15, 30)
    }
}

@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_single_market_data(symbol):
    """Obtiene datos de un mercado específico"""
    try:
        ticker = yf.Ticker(symbol)
        
        # Obtener datos históricos (2 años para MA200)
        hist = ticker.history(period="1y")
        
        if hist.empty:
            return None
        
        # Datos actuales
        current_price = hist['Close'].iloc[-1]
        previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        
        # Calcular cambio porcentual
        change_percent = ((current_price - previous_close) / previous_close) * 100
        
        # Calcular MA200 si hay suficientes datos
        if len(hist) >= 200:
            ma200 = hist['Close'].rolling(window=200).mean().iloc[-1]
            ma200_trend = "Alcista" if current_price > ma200 else "Bajista"
        else:
            ma200_trend = "Insuficientes datos"
        
        return {
            'price': float(current_price),
            'change_percent': float(change_percent),
            'ma200_trend': ma200_trend,
            'last_update': datetime.now().strftime('%H:%M:%S')
        }
        
    except Exception as e:
        print(f"Error obteniendo datos para {symbol}: {e}")
        return None

def get_market_data():
    """Obtiene datos de todos los mercados configurados"""
    market_data = {}
    
    # Usar progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_markets = len(MARKETS_CONFIG)
    
    for i, symbol in enumerate(MARKETS_CONFIG.keys()):
        status_text.text(f'Obteniendo datos de {MARKETS_CONFIG[symbol]["name"]}...')
        progress_bar.progress((i + 1) / total_markets)
        
        market_data[symbol] = get_single_market_data(symbol)
    
    # Limpiar elementos de progreso
    progress_bar.empty()
    status_text.empty()
    
    return market_data

def get_market_status(timezone_str):
    """Determina si un mercado está abierto o cerrado"""
    try:
        # Zona horaria del mercado
        market_tz = pytz.timezone(timezone_str)
        now_market = datetime.now(market_tz)
        
        # Obtener día de la semana (0=lunes, 6=domingo)
        weekday = now_market.weekday()
        
        # Mercados cerrados en fin de semana
        if weekday >= 5:  # Sábado o domingo
            next_monday = now_market.replace(hour=9, minute=0, second=0, microsecond=0)
            while next_monday.weekday() != 0:  # Buscar próximo lunes
                next_monday = next_monday.replace(day=next_monday.day + 1)
            
            return {
                'is_open': False,
                'status': 'Cerrado (Fin de semana)',
                'next_action': f'Abre el lunes a las 09:00'
            }
        
        # Horarios de apertura y cierre (simplificado)
        market_open = now_market.replace(hour=9, minute=0, second=0, microsecond=0)
        market_close = now_market.replace(hour=17, minute=0, second=0, microsecond=0)
        
        current_time = now_market.time()
        
        if market_open.time() <= current_time <= market_close.time():
            return {
                'is_open': True,
                'status': 'Abierto',
                'next_action': f'Cierra a las {market_close.strftime("%H:%M")}'
            }
        elif current_time < market_open.time():
            return {
                'is_open': False,
                'status': 'Pre-mercado',
                'next_action': f'Abre a las {market_open.strftime("%H:%M")}'
            }
        else:
            return {
                'is_open': False,
                'status': 'Post-mercado',
                'next_action': f'Abre mañana a las {market_open.strftime("%H:%M")}'
            }
            
    except Exception as e:
        return {
            'is_open': False,
            'status': 'Estado desconocido',
            'next_action': 'Verificar zona horaria'
        }

def get_global_sentiment():
    """Calcula el sentimiento global del mercado"""
    market_data = get_market_data()
    
    if not market_data:
        return "Neutral"
    
    # Contar mercados por tendencia
    positive = sum(1 for data in market_data.values() 
                  if data and data['change_percent'] > 0)
    negative = sum(1 for data in market_data.values() 
                  if data and data['change_percent'] < 0)
    total = len([d for d in market_data.values() if d])
    
    if total == 0:
        return "Sin datos"
    
    positive_ratio = positive / total
    
    if positive_ratio > 0.7:
        return "Muy optimista"
    elif positive_ratio > 0.6:
        return "Optimista"
    elif positive_ratio > 0.4:
        return "Neutral"
    elif positive_ratio > 0.3:
        return "Pesimista"
    else:
        return "Muy pesimista"

def format_currency(value, symbol="$"):
    """Formatea valores monetarios"""
    if value >= 1_000_000_000:
        return f"{symbol}{value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{symbol}{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{symbol}{value/1_000:.2f}K"
    else:
        return f"{symbol}{value:.2f}"

def get_market_hours_info():
    """Información sobre horarios de mercados"""
    info = {}
    
    for symbol, config in MARKETS_CONFIG.items():
        market_status = get_market_status(config['timezone'])
        info[symbol] = {
            'name': config['name'],
            'timezone': config['timezone'],
            'status': market_status
        }
    
    return info