"""
Manejo del archivo Excel para añadir resultados
"""
import openpyxl
from openpyxl import Workbook
import os
from config import EXCEL_FILE


class ExcelHandler:
    def __init__(self, filepath=EXCEL_FILE):
        self.filepath = filepath
        self.workbook = None
        self.sheet = None
        
    def load_or_create(self):
        """Carga el Excel existente o crea uno nuevo"""
        if os.path.exists(self.filepath):
            self.workbook = openpyxl.load_workbook(self.filepath)
            self.sheet = self.workbook.active
            print(f"Excel cargado: {self.filepath}")
        else:
            self.workbook = Workbook()
            self.sheet = self.workbook.active
            self.sheet.title = "Resultados Scraper"
            print(f"Nuevo Excel creado: {self.filepath}")
    
    def add_headers_if_needed(self, headers):
        """Añade encabezados si el Excel está vacío"""
        if self.sheet.max_row == 1 and self.sheet.cell(1, 1).value is None:
            for col, header in enumerate(headers, start=1):
                self.sheet.cell(1, col, header)
            print("Encabezados añadidos")
    
    def append_results(self, results):
        """
        Añade nuevas filas con los resultados
        
        Args:
            results: lista de diccionarios con los datos
        """
        if not results:
            print("No hay resultados para añadir")
            return
        
        # Obtener todas las claves posibles (columnas)
        all_keys = set()
        for result in results:
            all_keys.update(result.keys())
        
        headers = sorted(list(all_keys))
        
        # Añadir encabezados si es necesario
        self.add_headers_if_needed(headers)
        
        # Obtener encabezados actuales del Excel
        current_headers = []
        for col in range(1, self.sheet.max_column + 1):
            header = self.sheet.cell(1, col).value
            if header:
                current_headers.append(header)
        
        # Añadir nuevos encabezados si hay columnas nuevas
        for header in headers:
            if header not in current_headers:
                self.sheet.cell(1, len(current_headers) + 1, header)
                current_headers.append(header)
        
        # Añadir filas de resultados
        for result in results:
            row_num = self.sheet.max_row + 1
            for col, header in enumerate(current_headers, start=1):
                value = result.get(header, '')
                self.sheet.cell(row_num, col, value)
        
        print(f"{len(results)} filas añadidas al Excel")
    
    def save(self):
        """Guarda los cambios en el archivo Excel"""
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        
        self.workbook.save(self.filepath)
        print(f"Excel guardado: {self.filepath}")
    
    def close(self):
        """Cierra el workbook"""
        if self.workbook:
            self.workbook.close()


def update_excel_with_results(results):
    """Función helper para actualizar el Excel"""
    handler = ExcelHandler()
    try:
        handler.load_or_create()
        handler.append_results(results)
        handler.save()
    finally:
        handler.close()


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