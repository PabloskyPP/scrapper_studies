"""
Manejo del archivo Excel para añadir resultados.
Este módulo se encarga de toda la interacción con el archivo Excel,
incluyendo creación, lectura, escritura y actualización de datos.
"""

# Importación de módulos necesarios
import openpyxl  # Para manipular archivos Excel
from openpyxl import Workbook  # Para crear nuevos archivos Excel
import os  # Para operaciones con el sistema de archivos
from config import EXCEL_FILE  # Importa la ruta del archivo Excel desde la configuración


class ExcelHandler:
    def __init__(self, filepath=EXCEL_FILE):
        """
        Constructor de la clase ExcelHandler.
        Args:
            filepath (str): Ruta del archivo Excel a manejar. Por defecto usa EXCEL_FILE de config.
        """
        self.filepath = filepath  # Almacena la ruta del archivo Excel
        self.workbook = None     # Referencia al libro de Excel (se inicializa en None)
        self.sheet = None        # Referencia a la hoja activa (se inicializa en None)
        
    def load_or_create(self):
        """
        Carga un archivo Excel existente o crea uno nuevo si no existe.
        """
        if os.path.exists(self.filepath):  # Verifica si el archivo existe
            # Si existe, lo carga
            self.workbook = openpyxl.load_workbook(self.filepath)
            self.sheet = self.workbook.active  # Obtiene la hoja activa
            print(f"Excel cargado: {self.filepath}")
        else:
            # Si no existe, crea uno nuevo
            self.workbook = Workbook()
            self.sheet = self.workbook.active
            self.sheet.title = "Resultados Scraper"  # Establece el nombre de la hoja
            print(f"Nuevo Excel creado: {self.filepath}")
    
    def add_headers_if_needed(self, headers):
        """
        Añade encabezados al Excel si está vacío.
        Args:
            headers (list): Lista de nombres de columnas a añadir.
        """
        # Verifica si la primera fila está vacía
        if self.sheet.max_row == 1 and self.sheet.cell(1, 1).value is None:
            # Añade cada encabezado en su respectiva columna
            for col, header in enumerate(headers, start=1):
                self.sheet.cell(1, col, header)
            print("Encabezados añadidos")
    
    def append_results(self, results):
        """
        Añade nuevas filas con los resultados al Excel.
        
        Args:
            results (list): Lista de diccionarios con los datos a añadir.
                          Cada diccionario representa una fila.
        """
        if not results:  # Verifica si hay resultados para añadir
            print("No hay resultados para añadir")
            return
        
        # Recopila todas las claves únicas de todos los resultados para usar como columnas
        all_keys = set()
        for result in results:
            all_keys.update(result.keys())  # Añade todas las claves al conjunto
        
        headers = sorted(list(all_keys))  # Convierte a lista y ordena alfabéticamente
        
        # Asegura que el Excel tenga los encabezados necesarios
        self.add_headers_if_needed(headers)
        
        # Obtiene los encabezados actuales del Excel
        current_headers = []
        for col in range(1, self.sheet.max_column + 1):
            header = self.sheet.cell(1, col).value
            if header:  # Solo añade headers no vacíos
                current_headers.append(header)
        
        # Añade nuevos encabezados si hay columnas que no existían
        for header in headers:
            if header not in current_headers:  # Si es un nuevo header
                # Añade al final de las columnas existentes
                self.sheet.cell(1, len(current_headers) + 1, header)
                current_headers.append(header)
        
        # Añade los datos de cada resultado en nuevas filas
        for result in results:
            row_num = self.sheet.max_row + 1  # Obtiene el número de la siguiente fila
            for col, header in enumerate(current_headers, start=1):
                # Obtiene el valor del resultado o '' si no existe
                value = result.get(header, '')
                # Escribe el valor en la celda correspondiente
                self.sheet.cell(row_num, col, value)
        
        print(f"{len(results)} filas añadidas al Excel")
    
    def save(self):
        """
        Guarda los cambios en el archivo Excel.
        Crea el directorio si no existe.
        """
        # Asegura que el directorio exista
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        
        # Guarda el archivo
        self.workbook.save(self.filepath)
        print(f"Excel guardado: {self.filepath}")
    
    def close(self):
        """
        Cierra el archivo Excel para liberar recursos.
        """
        if self.workbook:  # Verifica que el workbook esté abierto
            self.workbook.close()


def update_excel_with_results(results):
    """
    Función auxiliar que encapsula todo el proceso de actualización del Excel.
    Args:
        results (list): Lista de diccionarios con los resultados a guardar.
    """
    handler = ExcelHandler()  # Crea una instancia del manejador
    try:
        handler.load_or_create()  # Carga o crea el archivo
        handler.append_results(results)  # Añade los resultados
        handler.save()  # Guarda los cambios
    finally:
        handler.close()  # Asegura que el archivo se cierre aunque haya errores


if __name__ == "__main__":
    # Ejemplo de uso
    test_results = [ 
        {
            'timestamp': '2025-01-15 20:00:00',
            'url': 'https://ejemplo.com',
            'name': 'Página Test',
            'keyword1': 5,
            'keyword2': 3
        }
    ]
    
    update_excel_with_results(test_results)