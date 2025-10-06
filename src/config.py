"""
Configuración central del scraper.
Este archivo contiene todas las configuraciones globales del proyecto,
incluyendo credenciales, rutas de archivos y parámetros del scraper.
"""
import os  # Para acceder a variables de entorno del sistema
from dotenv import load_dotenv  # Para cargar variables desde archivo .env

# Carga las variables de entorno desde el archivo .env (si existe)
# Esto permite configurar credenciales localmente sin exponerlas en el código
load_dotenv()

# ============== Configuración de Telegram ==============
# Token del bot de Telegram para enviar notificaciones
# Se obtiene de las variables de entorno para mayor seguridad
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# ID del chat de Telegram donde se enviarán las notificaciones
# Se obtiene del bot @userinfobot en Telegram
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# ============== Rutas de archivos ==============
# Ruta del archivo Excel donde se almacenan los resultados del scraping
EXCEL_FILE = 'data/scraper_estudios.xlsx' 

# Ruta del archivo JSON con la configuración de URLs a scrapear
URLS_CONFIG = 'data/urls_config.json'

# ============== Configuración del scraper ==============
# Tiempo máximo de espera para cada petición HTTP (en segundos)
REQUEST_TIMEOUT = 10  # segundos

# User-Agent para las peticiones HTTP (simula ser un navegador real)
# Esto ayuda a evitar bloqueos por parte de algunos sitios web
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Tiempo de espera entre peticiones HTTP (en segundos)
# Implementa rate limiting para respetar robots.txt y evitar sobrecargar servidores
RATE_LIMIT_DELAY = 1  # 1 segundo entre peticiones