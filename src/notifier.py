"""
Sistema de notificaciones por Telegram.
Este módulo gestiona el envío de notificaciones al usuario a través de Telegram,
incluyendo notificaciones de éxito, error y resúmenes detallados.
"""
import requests  # Para realizar peticiones HTTP a la API de Telegram
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID  # Credenciales de Telegram


class TelegramNotifier:
    def __init__(self):
        """
        Constructor de la clase TelegramNotifier.
        Inicializa las credenciales y la URL base de la API de Telegram.
        """
        # Token del bot de Telegram (obtenido de @BotFather)
        self.bot_token = TELEGRAM_BOT_TOKEN
        
        # ID del chat donde enviar los mensajes (obtenido de @userinfobot)
        self.chat_id = TELEGRAM_CHAT_ID
        
        # URL base de la API de Telegram para este bot
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(self, message):
        """
        Envía un mensaje a través de Telegram usando la API Bot.
        
        Args:
            message (str): Mensaje a enviar. Puede incluir formato HTML.
            
        Returns:
            bool: True si el mensaje se envió correctamente, False en caso contrario.
        """
        # Verifica que las credenciales estén configuradas
        if not self.bot_token or not self.chat_id:
            print("Telegram no configurado. Mensaje no enviado.")
            return False
        
        # Construye la URL del endpoint de envío de mensajes
        url = f"{self.base_url}/sendMessage"
        
        # Prepara el payload con los datos del mensaje
        payload = {
            'chat_id': self.chat_id,  # Destinatario del mensaje
            'text': message,  # Contenido del mensaje
            'parse_mode': 'HTML'  # Permite formato HTML en el mensaje
        }
        
        try:
            # Realiza la petición POST a la API de Telegram
            response = requests.post(url, json=payload, timeout=10)
            
            # Verifica que la respuesta sea exitosa (status code 2xx)
            response.raise_for_status()
            
            print("Notificación de Telegram enviada")
            return True
            
        except requests.exceptions.RequestException as e:
            # Captura cualquier error de red o HTTP
            print(f"Error al enviar notificación de Telegram: {e}")
            return False
    
    def send_success(self, results_count, timestamp):
        """
        Envía una notificación de éxito cuando el scraper se ejecuta correctamente.
        
        Args:
            results_count (int): Número de páginas procesadas exitosamente.
            timestamp (str): Fecha y hora de la ejecución.
            
        Returns:
            bool: True si la notificación se envió correctamente.
        """
        # Construye el mensaje con formato HTML
        message = f"""
✅ <b>Scraper ejecutado exitosamente</b>

📅 Fecha: {timestamp}
📊 Páginas procesadas: {results_count}
✨ Estado: Completado

Los datos han sido guardados en el Excel.
"""
        # Envía el mensaje usando el método base
        return self.send_message(message)
    
    def send_error(self, error_msg, timestamp):
        """
        Envía una notificación de error cuando el scraper falla.
        
        Args:
            error_msg (str): Descripción del error ocurrido.
            timestamp (str): Fecha y hora cuando ocurrió el error.
            
        Returns:
            bool: True si la notificación se envió correctamente.
        """
        # Construye el mensaje de error con formato HTML
        message = f"""
❌ <b>Error en el Scraper</b>

📅 Fecha: {timestamp}
⚠️ Error: {error_msg}

Por favor, revisa los logs en GitHub Actions.
"""
        # Envía el mensaje usando el método base
        return self.send_message(message)
    
    def send_summary(self, results, timestamp):
        """
        Envía un resumen detallado de los resultados del scraping.
        Incluye estadísticas de éxitos y fallos.
        
        Args:
            results (list): Lista de diccionarios con los resultados del scraping.
            timestamp (str): Fecha y hora de la ejecución.
            
        Returns:
            bool: True si la notificación se envió correctamente.
        """
        # Filtra los resultados exitosos (sin errores)
        successful = [r for r in results if 'error' not in r]
        
        # Filtra los resultados con errores
        failed = [r for r in results if 'error' in r]
        
        # Construye el mensaje con el resumen
        message = f"""
📊 <b>Resumen del Scraper</b>

📅 {timestamp}

✅ Exitosas: {len(successful)}
❌ Fallidas: {len(failed)}

"""
        
        # Si hay fallos, agrega la lista de URLs con error
        if failed:
            message += "<b>URLs con error:</b>\n"
            for result in failed:
                # Agrega cada URL fallida al mensaje
                message += f"• {result.get('name', 'N/A')}\n"
        
        # Envía el mensaje usando el método base
        return self.send_message(message)


if __name__ == "__main__":
    # Código de prueba para verificar el funcionamiento del notificador
    # Se ejecuta solo cuando este archivo se ejecuta directamente (no cuando se importa)
    
    # Crea una instancia del notificador
    notifier = TelegramNotifier()
    
    # Envía un mensaje de prueba de éxito
    notifier.send_success(10, "2025-01-15 20:00:00")