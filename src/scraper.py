"""
Scraper principal para procesar ofertas de empleo.
Este módulo contiene la lógica principal para extraer información
de las diferentes fuentes web configuradas.
Implementa scraping genérico basado en configuración JSON con soporte para:
- Conteo de palabras clave en áreas específicas del HTML
- Búsqueda en todo el HTML si no se especifican áreas
- Rate limiting para respetar robots.txt
"""

# Importaciones necesarias
import requests  # Para realizar peticiones HTTP
from bs4 import BeautifulSoup  # Para parsear y analizar HTML
from datetime import datetime  # Para manejar fechas y timestamps
import json  # Para procesamiento de JSON y lectura de configuración
import time  # Para implementar delays entre peticiones (rate limiting)
import os  # Para verificar existencia de archivos
from config import REQUEST_TIMEOUT, USER_AGENT, URLS_CONFIG, RATE_LIMIT_DELAY  # Configuraciones globales


class WebScraper:
    def __init__(self):
        """
        Constructor de la clase WebScraper.
        Inicializa las cabeceras HTTP, el timestamp de ejecución y carga la configuración.
        """
        # Configura el User-Agent para las peticiones HTTP (simula un navegador real)
        self.headers = {'User-Agent': USER_AGENT}
        
        # Timestamp de ejecución en formato YYYY-MM-DD HH:MM:SS
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Carga la configuración de URLs desde el archivo JSON
        self.urls_config = self._load_config()
    
    def _load_config(self):
        """
        Carga la configuración de URLs desde el archivo JSON.
        
        Returns:
            list: Lista de diccionarios con la configuración de cada URL.
                  Retorna una lista vacía si el archivo no existe o hay error.
        """
        try:
            # Verifica si el archivo de configuración existe
            if not os.path.exists(URLS_CONFIG):
                print(f"Advertencia: No se encontró el archivo {URLS_CONFIG}")
                return []
            
            # Lee y parsea el archivo JSON
            with open(URLS_CONFIG, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"Configuración cargada: {len(config)} URL(s) encontradas")
            return config
            
        except json.JSONDecodeError as e:
            # Error al parsear el JSON (formato incorrecto)
            print(f"Error al parsear {URLS_CONFIG}: {e}")
            return []
        except Exception as e:
            # Cualquier otro error al cargar la configuración
            print(f"Error cargando configuración: {e}")
            return []
    
    def count_keywords_in_area(self, soup, area_selector, keywords):
        """
        Cuenta las ocurrencias de palabras clave en un área específica del HTML.
        
        Args:
            soup (BeautifulSoup): Objeto BeautifulSoup con el HTML parseado.
            area_selector (str): Selector CSS del área donde buscar (ej: "article", "h1, h2").
            keywords (list): Lista de palabras clave a buscar.
            
        Returns:
            dict: Diccionario con el conteo de cada palabra clave en el área.
                  Formato: {keyword: count}
        """
        # Inicializa el diccionario de resultados con ceros
        counts = {keyword: 0 for keyword in keywords}
        
        # Busca todos los elementos que coincidan con el selector
        elements = soup.select(area_selector)
        
        # Combina el texto de todos los elementos encontrados
        text = ' '.join([elem.get_text().lower() for elem in elements])
        
        # Cuenta cada palabra clave en el texto (búsqueda case-insensitive)
        for keyword in keywords:
            counts[keyword] = text.count(keyword.lower())
        
        return counts
    
    def count_keywords_in_whole_page(self, soup, keywords):
        """
        Cuenta las ocurrencias de palabras clave en todo el HTML de la página.
        
        Args:
            soup (BeautifulSoup): Objeto BeautifulSoup con el HTML parseado.
            keywords (list): Lista de palabras clave a buscar.
            
        Returns:
            dict: Diccionario con el conteo de cada palabra clave.
                  Formato: {keyword: count}
        """
        # Inicializa el diccionario de resultados con ceros
        counts = {keyword: 0 for keyword in keywords}
        
        # Obtiene todo el texto de la página en minúsculas
        text = soup.get_text().lower()
        
        # Cuenta cada palabra clave en el texto completo
        for keyword in keywords:
            counts[keyword] = text.count(keyword.lower())
        
        return counts
    
    def check_uvigo_profesor(self, soup):
        """
        Procesa la página de UVigo Profesor para buscar ofertas activas.
        Método específico heredado de la implementación original.
        
        Args:
            soup (BeautifulSoup): Objeto BeautifulSoup con el HTML parseado.
            
        Returns:
            str: "YES" si hay ofertas activas, "NO" si no hay, "ERROR" en caso de error.
        """
        try:
            # Buscar todos los elementos de oferta de empleo
            rows = soup.select("div.row.uvigo-row-nopadding")
            
            # Itera sobre cada oferta encontrada
            for row in rows:
                # Encontrar el elemento que contiene el plazo
                plazo_text = row.select_one("div.uvigo-card-summary strong:contains('Plazo:')")
                if plazo_text:
                    # Extraer el texto de las fechas (formato DD/MM/YYYY – DD/MM/YYYY)
                    dates_text = plazo_text.find_next_sibling(string=True)
                    if dates_text:
                        # Convertir las fechas de texto a objetos datetime para comparación
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
            # Manejo de errores en el procesamiento
            print(f"Error procesando UVigo: {e}")
            return "ERROR"
    
    def check_usc_emprego(self, soup):
        """
        Procesa la página de USC Emprego buscando ofertas de psicología.
        Método específico heredado de la implementación original.
        
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
            
            # Buscar todos los enlaces de ofertas dentro del contenedor
            job_links = container.select("div.ml-specs.is-job h2.at-title a")
            
            # Revisar cada oferta buscando la palabra clave
            for link in job_links:
                if "psicolog" in link.text.lower():  # Búsqueda case-insensitive
                    return "YES"  # Se encontró al menos una oferta relevante
            
            return "NO"  # No se encontraron ofertas relevantes
            
        except Exception as e:
            # Manejo de errores en el procesamiento
            print(f"Error procesando USC: {e}")
            return "ERROR"
    
    def scrape_site(self, url):
        """
        Obtiene y parsea el contenido HTML de una URL.
        Implementa rate limiting para respetar robots.txt.
        
        Args:
            url (str): URL del sitio a scrapear.
            
        Returns:
            BeautifulSoup: Objeto con el HTML parseado, o None si hay error.
        """
        try:
            # Realizar la petición HTTP con los headers configurados
            response = requests.get(
                url,  # URL a consultar
                headers=self.headers,  # Headers configurados (User-Agent)
                timeout=REQUEST_TIMEOUT  # Timeout de la petición en segundos
            )
            response.raise_for_status()  # Lanza excepción si hay error HTTP (4xx, 5xx)
            
            # Parsear el HTML con BeautifulSoup usando el parser html.parser
            return BeautifulSoup(response.text, 'html.parser')
            
        except requests.exceptions.Timeout:
            # Error específico de timeout
            print(f"Timeout al acceder a {url}")
            return None
        except requests.exceptions.RequestException as e:
            # Otros errores de petición HTTP
            print(f"Error de petición HTTP en {url}: {e}")
            return None
        except Exception as e:
            # Cualquier otro error inesperado
            print(f"Error inesperado en {url}: {e}")
            return None
    
    def process_url_config(self, config):
        """
        Procesa una URL según su configuración y extrae los datos solicitados.
        Maneja diferentes tipos de scraping: keyword_check, date_check, o conteo genérico.
        
        Args:
            config (dict): Diccionario con la configuración de la URL:
                - name: Nombre descriptivo
                - url: URL a scrapear
                - type: Tipo de procesamiento (opcional)
                - keywords: Lista de palabras clave a buscar
                - search_areas: Diccionario con áreas específicas donde buscar
                
        Returns:
            dict: Diccionario con los resultados del scraping.
                  Incluye timestamp, url, name y los conteos/resultados.
        """
        # Inicializa el diccionario de resultados con información básica
        result = {
            'timestamp': self.timestamp,  # Fecha y hora de ejecución
            'url': config['url'],  # URL scrapeada
            'name': config['name']  # Nombre descriptivo de la fuente
        }
        
        # Obtiene el HTML de la página
        soup = self.scrape_site(config['url'])
        
        if not soup:
            # Si no se pudo obtener el HTML, marca como error
            result['error'] = 'Failed to fetch page'
            return result
        
        # Implementa rate limiting: espera entre peticiones
        time.sleep(RATE_LIMIT_DELAY)
        
        # Obtiene el tipo de procesamiento (por defecto: conteo de keywords)
        processing_type = config.get('type', 'keyword_count')
        
        # ============ Procesamiento específico por tipo ============
        
        if processing_type == 'date_check':
            # Tipo especial: verificación de fechas (UVigo)
            result['status'] = self.check_uvigo_profesor(soup)
            
        elif processing_type == 'keyword_check':
            # Tipo especial: verificación de presencia de keywords (USC)
            result['status'] = self.check_usc_emprego(soup)
            
        else:
            # Procesamiento genérico: conteo de palabras clave
            keywords = config.get('keywords', [])  # Lista de keywords a buscar
            
            if not keywords:
                # Si no hay keywords configuradas, marca como error
                result['error'] = 'No keywords configured'
                return result
            
            # Obtiene las áreas específicas donde buscar (opcional)
            search_areas = config.get('search_areas', None)
            
            if search_areas:
                # Si hay áreas específicas configuradas, cuenta en cada área
                for area_name, area_selector in search_areas.items():
                    # Cuenta keywords en el área específica
                    counts = self.count_keywords_in_area(soup, area_selector, keywords)
                    
                    # Agrega los resultados con el prefijo del área
                    for keyword, count in counts.items():
                        result[f"{area_name}_{keyword}"] = count
            else:
                # Si no hay áreas específicas, busca en toda la página
                counts = self.count_keywords_in_whole_page(soup, keywords)
                
                # Agrega los resultados directamente
                for keyword, count in counts.items():
                    result[keyword] = count
        
        return result
    
    def scrape_all(self):
        """
        Ejecuta el scraping de todas las URLs configuradas en urls_config.json.
        Procesa cada URL según su configuración específica.
        
        Returns:
            list: Lista de diccionarios con los resultados del scraping.
                  Cada diccionario contiene los datos de una URL procesada.
        """
        results = []  # Lista para almacenar todos los resultados
        
        # Verifica si hay configuración cargada
        if not self.urls_config:
            print("No hay URLs configuradas para scrapear")
            return results
        
        print(f"\n{'='*60}")
        print(f"Iniciando scraping de {len(self.urls_config)} URL(s)")
        print(f"{'='*60}\n")
        
        # Procesa cada URL configurada
        for idx, config in enumerate(self.urls_config, 1):
            print(f"[{idx}/{len(self.urls_config)}] Procesando: {config['name']}")
            print(f"  URL: {config['url']}")
            
            # Procesa la URL según su configuración
            result = self.process_url_config(config)
            
            # Agrega el resultado a la lista
            results.append(result)
            
            # Muestra el resultado
            if 'error' in result:
                print(f"  ❌ Error: {result['error']}")
            elif 'status' in result:
                print(f"  ✓ Status: {result['status']}")
            else:
                print(f"  ✓ Completado")
            
            print()  # Línea en blanco para separación
        
        print(f"{'='*60}")
        print(f"Scraping completado: {len(results)} resultado(s)")
        print(f"{'='*60}\n")
        
        return results


if __name__ == "__main__":
    scraper = WebScraper()
    results = scraper.scrape_all()
    print(results)