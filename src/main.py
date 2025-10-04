"""
Script principal que ejecuta el scraper completo
"""
from datetime import datetime
from scraper import WebScraper
from excel_handler import update_excel_with_results
from notifier import TelegramNotifier


def main():
    """Función principal que orquesta todo el proceso"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    notifier = TelegramNotifier()
    
    try:
        print("=" * 50)
        print(f"Iniciando scraper - {timestamp}")
        print("=" * 50)
        
        # Ejecutar scraper
        scraper = WebScraper()
        results = scraper.scrape_all()
        
        if not results:
            raise Exception("No se obtuvieron resultados del scraper")
        
        print(f"\nResultados obtenidos: {len(results)}")
        
        # Guardar en Excel
        print("\nActualizando Excel...")
        update_excel_with_results(results)
        
        # Enviar notificación de éxito
        print("\nEnviando notificación...")
        notifier.send_summary(results, timestamp)
        
        print("\n" + "=" * 50)
        print("Proceso completado exitosamente")
        print("=" * 50)
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ ERROR: {error_msg}")
        
        # Enviar notificación de error
        notifier.send_error(error_msg, timestamp)
        
        # Re-lanzar la excepción para que GitHub Actions lo marque como fallido
        raise


if __name__ == "__main__":
    main()