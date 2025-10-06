"""
Configuración central del scraper
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Rutas de archivos
EXCEL_FILE = 'data/scraper_estudios.xlsx' 
URLS_CONFIG = 'data/urls_config.json'

# Configuración del scraper
REQUEST_TIMEOUT = 10  # segundos
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'