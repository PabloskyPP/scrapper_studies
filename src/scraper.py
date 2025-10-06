"""
Scraper principal para procesar ofertas de empleo.
Este módulo contiene la lógica principal para extraer información
de las diferentes fuentes web configuradas.
"""

# Importaciones necesarias
import requests  # Para realizar peticiones HTTP
from bs4 import BeautifulSoup  # Para parsear y analizar HTML
from datetime import datetime  # Para manejar fechas y timestamps
import json  # Para procesamiento de JSON
from config import REQUEST_TIMEOUT, USER_AGENT, URLS_CONFIG  # Configuraciones


class WebScraper:
    def __init__(self):
        """
        Constructor de la clase WebScraper.
        Inicializa las cabeceras HTTP y el timestamp de ejecución.
        """
        self.headers = {'User-Agent': USER_AGENT}  # Configura el User-Agent para las peticiones
        self.timestamp = datetime.now().strftime('%Y-%m-%d')  # Fecha actual en formato YYYY-MM-DD
    
    def check_uvigo_profesor(self, soup):
        """
        Procesa la página de UVigo Profesor para buscar ofertas activas.
        
        Args:
            soup (BeautifulSoup): Objeto BeautifulSoup con el HTML parseado.
            
        Returns:
            str: "YES" si hay ofertas activas, "NO" si no hay, "ERROR" en caso de error.
        """
        try:
            # Buscar todos los elementos de oferta de empleo
            rows = soup.select("div.row.uvigo-row-nopadding")
            
            for row in rows:
                # Encontrar el elemento que contiene el plazo
                plazo_text = row.select_one("div.uvigo-card-summary strong:contains('Plazo:')")
                if plazo_text:
                    # Extraer el texto de las fechas (formato DD/MM/YYYY – DD/MM/YYYY)
                    dates_text = plazo_text.find_next_sibling(string=True)
                    if dates_text:
                        # Convertir las fechas de texto a objetos datetime
                        start_date, end_date = [
                            datetime.strptime(d.strip(), '%d/%m/%Y')
                            for d in dates_text.split('–')
                        ]
                        current_date = datetime.now()
                        
                        # Verificar si la fecha actual está dentro del rango del plazo
                        if start_date <= current_date <= end_date:
                            return "YES"  # Hay al menos una oferta activa
            
            return "NO"  # No se encontraron ofertas activas
            
        except Exception as e:
            print(f"Error procesando UVigo: {e}")
            return "ERROR"
    
    def check_usc_emprego(self, soup):
        """
        Procesa la página de USC Emprego buscando ofertas de psicología.
        
        Args:
            soup (BeautifulSoup): Objeto BeautifulSoup con el HTML parseado.
            
        Returns:
            str: "YES" si hay ofertas con la palabra clave, "NO" si no hay, 
                 "ERROR" si hay problemas al procesar.
        """
        try:
            # Buscar el contenedor principal de ofertas
            container = soup.select_one("div#NHrsmAWmGreTiSMyIMnwjg-OkgfJwm")
            if not container:
                return "ERROR"  # No se encontró el contenedor principal
            
            # Buscar todos los enlaces de ofertas
            job_links = container.select("div.ml-specs.is-job h2.at-title a")
            
            # Revisar cada oferta buscando la palabra clave
            for link in job_links:
                if "psicolog" in link.text.lower():  # Búsqueda case-insensitive
                    return "YES"  # Se encontró al menos una oferta relevante
            
            return "NO"  # No se encontraron ofertas relevantes
            
        except Exception as e:
            print(f"Error procesando USC: {e}")
            return "ERROR"
    
    def scrape_site(self, url):
        """
        Obtiene y parsea el contenido HTML de una URL.
        
        Args:
            url (str): URL del sitio a scrapear.
            
        Returns:
            BeautifulSoup: Objeto con el HTML parseado, o None si hay error.
        """
        try:
            # Realizar la petición HTTP
            response = requests.get(
                url,  # URL a consultar
                headers=self.headers,  # Headers configurados (User-Agent)
                timeout=REQUEST_TIMEOUT  # Timeout de la petición
            )
            response.raise_for_status()  # Lanza excepción si hay error HTTP
            
            # Parsear el HTML con BeautifulSoup
            return BeautifulSoup(response.text, 'html.parser')
            
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def scrape_all(self):
        """
        Ejecuta el scraping de todas las URLs configuradas.
        
        Returns:
            list: Lista con un diccionario conteniendo los resultados del scraping.
                 El diccionario incluye la fecha y el estado de cada sitio ("YES"/"NO"/"ERROR").
        """
        # Inicializar diccionario de resultados con valores por defecto
        results = {
            'date': self.timestamp,  # Fecha actual
            'UVigoProfesor': 'NO',   # Estado inicial UVigo
            'USCEmprego': 'NO'       # Estado inicial USC
        }
        
        # Procesar página de UVigo
        soup = self.scrape_site("https://secretaria.uvigo.gal/uv/web/convocatoria/public/index")
        if soup:  # Si se pudo obtener el HTML
            results['UVigoProfesor'] = self.check_uvigo_profesor(soup)
        
        # Procesar página de USC
        soup = self.scrape_site("https://www.usc.gal/gl/emprego")
        if soup:  # Si se pudo obtener el HTML
            results['USCEmprego'] = self.check_usc_emprego(soup)
        
        # Retornar resultados en formato lista para mantener compatibilidad
        # con el sistema de procesamiento de resultados
        return [results]


if __name__ == "__main__":
    scraper = WebScraper()
    results = scraper.scrape_all()
    print(results)