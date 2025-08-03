# 🌍 Mapa Financiero Mundial

**Tu radar bursátil global en tiempo real** - Una aplicación web interactiva que muestra el estado de los principales mercados financieros mundiales de forma visual e intuitiva.

## 🚀 Características Principales

### 🗺️ Mapa Interactivo
- **Visualización global**: Mapa mundial con los principales mercados bursátiles
- **Indicadores climáticos**: Emoticonos que representan el rendimiento
- **Datos en tiempo real**: Actualización automática de precios e índices
- **Interactividad**: Hover para detalles completos de cada mercado

### 📊 Métricas Avanzadas
- **Precio actual** del índice principal de cada bolsa
- **Variación porcentual** respecto al cierre anterior
- **Tendencia MA200**: Media móvil de 200 períodos
- **Estado del mercado**: Abierto/cerrado con horarios locales
- **Análisis de sentimiento** global

### 🌤️ Sistema de Emoticonos Climáticos
- ☀️ **Subida fuerte** (>1%): Mercado muy alcista
- 🌤️ **Subida leve** (0-1%): Mercado ligeramente positivo
- ☁️ **Bajada leve** (0 a -1%): Mercado ligeramente negativo  
- 🌩️ **Bajada fuerte** (<-1%): Mercado muy bajista

## 🏛️ Mercados Incluidos

| Región | Mercado | Índice | Zona Horaria |
|--------|---------|--------|--------------|
| 🇺🇸 Norte América | NYSE/NASDAQ | S&P 500, NASDAQ | New York (EST) |
| 🇪🇺 Europa | Londres, Frankfurt, París, Madrid | FTSE, DAX, CAC40, IBEX35 | CET/GMT |
| 🇯🇵 Asia-Pacífico | Tokio, Hong Kong, Shanghái | Nikkei, Hang Seng, SSE | JST/HKT/CST |
| 🇧🇷 Latinoamérica | São Paulo | Bovespa | BRT |
| 🇦🇺 Oceanía | Sídney | ASX 200 | AEST |

## 🛠️ Instalación y Uso

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/mapa-financiero-mundial.git
cd mapa-financiero-mundial
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

4. **Abrir en el navegador**
La aplicación se abrirá automáticamente en `http://localhost:8501`

### Despliegue en Streamlit Cloud

1. **Fork este repositorio** en tu cuenta de GitHub
2. **Conectar con Streamlit Cloud**:
   - Visita [share.streamlit.io](https://share.streamlit.io)
   - Conecta tu cuenta de GitHub
   - Selecciona este repositorio
   - Archivo principal: `app.py`
3. **Deploy automático**: La aplicación se desplegará automáticamente

### Despliegue en Heroku

```bash
# Crear aplicación en Heroku
heroku create tu-mapa-financiero

# Configurar buildpack de Python
heroku buildpacks:set heroku/python

# Desplegar
git push heroku main
```

## 📁 Estructura del Proyecto

```
mapa-financiero-mundial/
│
├── app.py                 # Aplicación principal de Streamlit
├── data_utils.py          # Módulo de obtención y procesamiento de datos
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Documentación del proyecto
└── .streamlit/
    └── config.toml       # Configuración de Streamlit (opcional)
```

### Descripción de Archivos

- **`app.py`**: Interfaz principal con Streamlit, manejo del mapa interactivo y visualizaciones
- **`data_utils.py`**: Lógica de negocio, APIs de datos financieros, cálculos de métricas
- **`requirements.txt`**: Lista de todas las dependencias necesarias para el proyecto

## 🔧 Tecnologías Utilizadas

### Backend y Datos
- **🐍 Python 3.8+**: Lenguaje principal
- **📊 yfinance**: API gratuita para datos financieros de Yahoo Finance
- **🐼 Pandas**: Manipulación y análisis de datos
- **⏰ pytz**: Manejo de zonas horarias

### Frontend y Visualización
- **🎛️ Streamlit**: Framework web para aplicaciones de datos
- **📈 Plotly**: Gráficos interactivos y mapas
- **🗺️ Plotly Geo**: Visualizaciones geográficas

## 📊 Funcionalidades Detalladas

### 1. Mapa Interactivo Mundial
```python
# Características del mapa
- Proyección "Natural Earth" para visualización óptima
- Puntos escalables según volatilidad del mercado
- Colores dinámicos basados en rendimiento
- Tooltips informativos con datos completos
- Responsive design para móviles y desktop
```

### 2. Sistema de Métricas
```python
# Indicadores calculados
- Precio actual del índice
- Variación porcentual diaria
- Tendencia MA200 (Media Móvil 200 períodos)
- Estado del mercado (abierto/cerrado)
- Horarios de apertura/cierre locales
```

### 3. Panel de Control
```python
# Funcionalidades del sidebar
- Leyenda explicativa completa
- Botón de actualización manual
- Timestamp de última actualización
- Guía de interpretación de datos
```

## 🎯 Casos de Uso

### Para Inversores Individuales
- **Vista rápida global**: Identificar tendencias mundiales en segundos
- **Timing de operaciones**: Conocer horarios de mercados internacionales
- **Análisis técnico básico**: Tendencia MA200 para decisiones informadas
- **Diversificación geográfica**: Evaluar oportunidades por regiones

### Para Analistas Financieros
- **Monitoreo institucional**: Seguimiento de múltiples mercados simultáneamente
- **Informes de mercado**: Datos actualizados para presentaciones
- **Análisis de correlaciones**: Identificar patrones entre mercados regionales
- **Research de mercados emergentes**: Seguimiento de Asia-Pacífico y Latinoamérica

### Para Educación Financiera
- **Herramienta didáctica**: Visualización clara para estudiantes
- **Comprensión global**: Interconexión de mercados mundiales
- **Análisis técnico**: Introducción a indicadores como MA200
- **Geografía financiera**: Ubicación y horarios de centros financieros

## 🔄 Actualizaciones de Datos

### Frecuencia de Actualización
- **Datos de precios**: Cada 5 minutos (configurable)
- **Estado de mercados**: En tiempo real
- **Cache inteligente**: Optimización para rendimiento
- **Manejo de errores**: Reintentos automáticos

### Fuentes de Datos
- **Yahoo Finance**: Datos gratuitos y confiables
- **Cobertura**: 15+ mercados principales mundiales
- **Historial**: Hasta 1 año para cálculo de MA200
- **Latencia**: <30 segundos en condiciones normales

## 🚨 Limitaciones y Consideraciones

### Limitaciones Técnicas
- **Datos gratuitos**: Puede haber retrasos de 15-20 minutos
- **Rate limits**: Límites de API de Yahoo Finance
- **Fines de semana**: Mercados cerrados, datos del viernes
- **Festivos**: No considera festivos locales específicos

### Descargo de Responsabilidad
⚠️ **IMPORTANTE**: Esta aplicación es solo para fines educativos e informativos. No constituye asesoramiento financiero. Las decisiones de inversión deben basarse en análisis profesional y consideración de riesgos individuales.

## 🤝 Contribuciones

### Cómo Contribuir
1. **Fork** el repositorio
2. **Crear rama** para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crear Pull Request**

### Ideas para Mejoras
- [ ] Agregar más mercados (Medio Oriente, África)
- [ ] Incluir criptomonedas principales
- [ ] Alerts por email/SMS para cambios significativos
- [ ] Análisis histórico y backtesting
- [ ] API REST para integración externa
- [ ] Versión móvil nativa
- [ ] Integración con brokers

## 📞 Soporte y Contacto

### Reportar Problemas
- **GitHub Issues**: Para bugs y solicitudes de funcionalidades
- **Discusiones**: Para preguntas generales y ideas

### Documentación Adicional
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Plotly Docs**: [plotly.com/python](https://plotly.com/python/)
- **yfinance Docs**: [pypi.org/project/yfinance](https://pypi.org/project/yfinance/)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 🚀 Quick Start

```bash
# Instalación rápida
git clone https://github.com/tu-usuario/mapa-financiero-mundial.git
cd mapa-financiero-mundial
pip install -r requirements.txt
streamlit run app.py
```

**¡Listo!** Tu mapa financiero mundial estará corriendo en `http://localhost:8501`

---

### 💡 Tips de Uso

1. **Usa el hover** sobre los puntos del mapa para detalles completos
2. **Actualiza manualmente** con el botón del sidebar cuando necesites datos frescos
3. **Observa los tamaños** de los puntos - indican volatilidad del mercado
4. **Presta atención a los horarios** - mercados cerrados muestran datos del último cierre
5. **Usa la tabla detallada** para análisis más profundo de cada mercado

### 🎨 Personalización

El código está estructurado para fácil personalización:

- **Agregar mercados**: Modifica `MARKETS_CONFIG` en `data_utils.py`
- **Cambiar colores**: Ajusta `get_color_by_change()` en `app.py`
- **Modificar emoticonos**: Edita `get_emoji_by_change()` en `app.py`
- **Ajustar métricas**: Personaliza cálculos en `get_single_market_data()`

¡Haz tuyo este mapa financiero! 🌍📈