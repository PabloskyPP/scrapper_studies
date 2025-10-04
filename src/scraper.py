"""
Scraper principal para extraer frecuencia de palabras clave
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
from config import REQUEST_TIMEOUT, USER_AGENT, URLS_CONFIG


class WebScraper:
    def __init__(self):
        self.headers = {'User-Agent': USER_AGENT}
        self.results = []
    
    def load_urls_config(self):
        """Carga la configuración de URLs y términos desde JSON"""
        try:
            with open(URLS_CONFIG, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"No se encontró el archivo {URLS_CONFIG}")
    
    def fetch_page(self, url):
        """Obtiene el contenido HTML de una URL"""
        try:
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener {url}: {e}")
            return None
    
    def count_keywords(self, html, keywords, search_areas=None):
        """
        Cuenta la frecuencia de palabras clave en el HTML
        
        Args:
            html: contenido HTML
            keywords: lista de palabras clave a buscar
            search_areas: dict con selectores CSS para áreas específicas
                         ej: {"title": "h1", "content": "article"}
        """
        soup = BeautifulSoup(html, 'html.parser')
        counts = {}
        
        if search_areas:
            # Buscar en áreas específicas
            for area_name, selector in search_areas.items():
                elements = soup.select(selector)
                area_text = ' '.join([el.get_text().lower() for el in elements])
                
                for keyword in keywords:
                    key = f"{area_name}_{keyword}"
                    counts[key] = area_text.count(keyword.lower())
        else:
            # Buscar en todo el HTML
            full_text = soup.get_text().lower()
            for keyword in keywords:
                counts[keyword] = full_text.count(keyword.lower())
        
        return counts
    
    def scrape_all(self):
        """Ejecuta el scraping de todas las URLs configuradas"""
        config = self.load_urls_config()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for item in config:
            url = item['url']
            name = item.get('name', url)
            keywords = item['keywords']
            search_areas = item.get('search_areas', None)
            
            print(f"Scrapeando: {name}")
            html = self.fetch_page(url)
            
            if html:
                counts = self.count_keywords(html, keywords, search_areas)
                
                result = {
                    'timestamp': timestamp,
                    'url': url,
                    'name': name,
                    **counts
                }
                self.results.append(result)
                
                # Pausa entre peticiones para ser respetuoso
                time.sleep(1)
            else:
                # Registrar fallo
                self.results.append({
                    'timestamp': timestamp,
                    'url': url,
                    'name': name,
                    'error': 'Failed to fetch'
                })
        
        return self.results


if __name__ == "__main__":
    scraper = WebScraper()
    results = scraper.scrape_all()
    
    for result in results:
        print(result)