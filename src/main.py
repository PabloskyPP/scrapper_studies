"""
Script principal que ejecuta el scraper completo.
Este es el punto de entrada de la aplicación que orquesta todo el proceso:
1. Ejecuta el scraping de todas las URLs configuradas
2. Guarda los resultados en Excel
3. Envía notificaciones de Telegram
"""
# Importaciones necesarias
from datetime import datetime  # Para generar timestamps de ejecución
from scraper import WebScraper  # Clase principal del scraper
from excel_handler import update_excel_with_results  # Función para guardar en Excel
from notifier import TelegramNotifier  # Clase para enviar notificaciones


def main():
    """
    Función principal que orquesta todo el proceso de scraping.
    Maneja la ejecución completa desde el inicio hasta el final,
    incluyendo manejo de errores y notificaciones.
    """
    # Genera el timestamp de ejecución en formato YYYY-MM-DD HH:MM:SS
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Crea una instancia del notificador para enviar mensajes
    notifier = TelegramNotifier()
    
    try:
        # ============ Inicio del proceso ============
        print("=" * 50)
        print(f"Iniciando scraper - {timestamp}")
        print("=" * 50)
        
        # ============ Fase 1: Ejecutar scraper ============
        # Crea una instancia del scraper con la configuración cargada
        scraper = WebScraper()
        
        # Ejecuta el scraping de todas las URLs configuradas
        results = scraper.scrape_all()
        
        # Verifica que se obtuvieron resultados
        if not results:
            raise Exception("No se obtuvieron resultados del scraper")
        
        print(f"\nResultados obtenidos: {len(results)}")
        
        # ============ Fase 2: Guardar en Excel ============
        print("\nActualizando Excel...")
        # Guarda todos los resultados en el archivo Excel
        update_excel_with_results(results)
        
        # ============ Fase 3: Enviar notificación ============
        print("\nEnviando notificación...")
        # Envía un resumen con estadísticas a Telegram
        notifier.send_summary(results, timestamp)
        
        # ============ Finalización exitosa ============
        print("\n" + "=" * 50)
        print("Proceso completado exitosamente")
        print("=" * 50)
        
    except Exception as e:
        # ============ Manejo de errores ============
        # Convierte la excepción a string para logging
        error_msg = str(e) 
        print(f"\n❌ ERROR: {error_msg}")
        
        # Envía notificación de error a Telegram
        notifier.send_error(error_msg, timestamp)
        
        # Re-lanza la excepción para que GitHub Actions marque el workflow como fallido
        # Esto es importante para el monitoreo y debugging
        raise


if __name__ == "__main__":
    # Punto de entrada cuando el script se ejecuta directamente
    # (no cuando se importa como módulo)
    main()