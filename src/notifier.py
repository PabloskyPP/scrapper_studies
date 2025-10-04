"""
Sistema de notificaciones por Telegram
"""
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


class TelegramNotifier:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(self, message):
        """Envía un mensaje a través de Telegram"""
        if not self.bot_token or not self.chat_id:
            print("Telegram no configurado. Mensaje no enviado.")
            return False
        
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            print("Notificación de Telegram enviada")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error al enviar notificación de Telegram: {e}")
            return False
    
    def send_success(self, results_count, timestamp):
        """Envía notificación de éxito"""
        message = f"""
✅ <b>Scraper ejecutado exitosamente</b>

📅 Fecha: {timestamp}
📊 Páginas procesadas: {results_count}
✨ Estado: Completado

Los datos han sido guardados en el Excel.
"""
        return self.send_message(message)
    
    def send_error(self, error_msg, timestamp):
        """Envía notificación de error"""
        message = f"""
❌ <b>Error en el Scraper</b>

📅 Fecha: {timestamp}
⚠️ Error: {error_msg}

Por favor, revisa los logs en GitHub Actions.
"""
        return self.send_message(message)
    
    def send_summary(self, results, timestamp):
        """Envía un resumen detallado de los resultados"""
        successful = [r for r in results if 'error' not in r]
        failed = [r for r in results if 'error' in r]
        
        message = f"""
📊 <b>Resumen del Scraper</b>

📅 {timestamp}

✅ Exitosas: {len(successful)}
❌ Fallidas: {len(failed)}

"""
        
        if failed:
            message += "<b>URLs con error:</b>\n"
            for result in failed:
                message += f"• {result.get('name', 'N/A')}\n"
        
        return self.send_message(message)


if __name__ == "__main__":
    # Test de notificación
    notifier = TelegramNotifier()
    notifier.send_success(10, "2025-01-15 20:00:00")