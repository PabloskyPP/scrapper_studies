# 📖 Guía de Uso del Scraper Genérico

## 🎯 Introducción

Este scraper ahora soporta configuración completa mediante el archivo `data/urls_config.json`. Puedes añadir tantas URLs como necesites (recomendado: 10-15) con diferentes configuraciones de búsqueda.

---

## 📝 Tipos de Configuración

### 1️⃣ Conteo de Keywords en Áreas Específicas

Cuenta palabras clave en secciones específicas del HTML.

```json
{
  "name": "Nombre descriptivo",
  "url": "https://tu-sitio.com/pagina",
  "keywords": ["palabra1", "palabra2", "palabra3"],
  "search_areas": {
    "titulo": "h1, h2, h3",
    "contenido": "article, .main-content",
    "requisitos": ".requirements, .skills-list"
  }
}
```

**Resultado en Excel:**
```
| timestamp | url | name | titulo_palabra1 | titulo_palabra2 | contenido_palabra1 | contenido_palabra2 | requisitos_palabra1 | ... |
```

**Cuándo usar:** Cuando quieres saber dónde aparecen las palabras (título vs contenido vs requisitos).

---

### 2️⃣ Conteo de Keywords en Toda la Página

Cuenta palabras clave en todo el HTML sin distinguir áreas.

```json
{
  "name": "Noticias Investigación",
  "url": "https://universidad.edu/noticias",
  "keywords": ["investigación", "doctorado", "beca", "publicación"],
  "search_areas": null
}
```

**Resultado en Excel:**
```
| timestamp | url | name | investigación | doctorado | beca | publicación |
```

**Cuándo usar:** Cuando solo te interesa el total de apariciones, sin importar dónde.

---

### 3️⃣ Tipos Especiales (Heredados)

#### date_check - Verificación de Fechas
```json
{
  "name": "UVigoProfesor",
  "url": "https://secretaria.uvigo.gal/uv/web/convocatoria/public/index",
  "type": "date_check"
}
```

**Resultado:** `status: YES/NO/ERROR`

#### keyword_check - Verificación de Presencia
```json
{
  "name": "USCEmprego",
  "url": "https://www.usc.gal/gl/emprego",
  "type": "keyword_check",
  "keywords": ["psicolog"]
}
```

**Resultado:** `status: YES/NO/ERROR`

---

## 🔍 Selectores CSS - Guía Rápida

### Ejemplos Comunes

| Selector | Significado | Ejemplo |
|----------|-------------|---------|
| `h1, h2` | Todos los h1 y h2 | Títulos principales |
| `article` | Elemento article | Contenido principal |
| `.clase` | Elementos con clase | `.job-description` |
| `#id` | Elemento con ID | `#main-content` |
| `div.clase` | Div con clase | `div.job-card` |
| `p.intro` | Párrafos con clase intro | Introducción |

### Combinaciones Útiles
```json
"search_areas": {
  "titulos": "h1, h2, h3, .title",
  "descripcion": "article, .description, .job-desc",
  "meta": ".tags, .categories, .keywords",
  "todo_principal": "main, #content, .main-wrapper"
}
```

---

## 💡 Casos de Uso Reales

### Ejemplo 1: Portal de Empleo Universitario
```json
{
  "name": "Portal Empleo UV",
  "url": "https://empleo.uv.es/ofertas",
  "keywords": ["profesor", "investigador", "docente", "postdoc"],
  "search_areas": {
    "titulo": "h2.offer-title",
    "descripcion": ".offer-description",
    "requisitos": ".requirements"
  }
}
```

**Qué mide:** Frecuencia de cada término en diferentes secciones de las ofertas.

---

### Ejemplo 2: Noticias de Investigación
```json
{
  "name": "Noticias CSIC",
  "url": "https://www.csic.es/es/noticias",
  "keywords": ["neurociencia", "psicología", "cognición", "cerebro"],
  "search_areas": null
}
```

**Qué mide:** Total de menciones de cada término en toda la página de noticias.

---

### Ejemplo 3: Convocatorias Múltiples
```json
[
  {
    "name": "Convocatorias UV",
    "url": "https://uv.es/convocatorias",
    "keywords": ["ayuda", "beca", "contrato"],
    "search_areas": {"titulo": "h3, h4"}
  },
  {
    "name": "Convocatorias UB",
    "url": "https://ub.edu/convocatorias",
    "keywords": ["ayuda", "beca", "contrato"],
    "search_areas": {"titulo": "h3, h4"}
  },
  {
    "name": "Convocatorias UAM",
    "url": "https://uam.es/convocatorias",
    "keywords": ["ayuda", "beca", "contrato"],
    "search_areas": {"titulo": "h3, h4"}
  }
]
```

**Qué mide:** Compara menciones de términos en los títulos de 3 universidades.

---

## 🚀 Workflow de Configuración

### Paso 1: Identifica la Página
1. Abre la página web en tu navegador
2. Inspecciona el HTML (F12 / Clic derecho > Inspeccionar)
3. Identifica las áreas de interés

### Paso 2: Encuentra los Selectores
```html
<!-- Ejemplo de HTML -->
<article class="job-post">
  <h2 class="job-title">Profesor de Psicología</h2>
  <div class="job-description">
    Buscamos profesor con experiencia en neurociencia...
  </div>
  <ul class="requirements">
    <li>Doctorado en Psicología</li>
    <li>Investigación en cognición</li>
  </ul>
</article>
```

**Selectores correspondientes:**
```json
"search_areas": {
  "titulo": "h2.job-title, .job-title",
  "descripcion": ".job-description",
  "requisitos": ".requirements"
}
```

### Paso 3: Define las Keywords
Palabras clave relevantes para tu búsqueda:
```json
"keywords": ["psicología", "neurociencia", "cognición", "doctorado"]
```

### Paso 4: Añade a urls_config.json
```json
{
  "name": "Nombre descriptivo para identificar",
  "url": "URL completa con https://",
  "keywords": ["lista", "de", "palabras"],
  "search_areas": {
    "area1": "selectores css",
    "area2": "otros selectores"
  }
}
```

### Paso 5: Prueba Localmente
```bash
python src/main.py
```

### Paso 6: Verifica el Excel
Abre `data/scraper_estudios.xlsx` y verifica que las columnas sean correctas.

---

## 🔧 Resolución de Problemas

### Problema: No encuentra keywords
**Solución:**
1. Verifica que las keywords estén en minúsculas (búsqueda case-insensitive)
2. Comprueba los selectores CSS inspeccionando el HTML
3. Prueba con `"search_areas": null` primero para buscar en toda la página

### Problema: Selectores no funcionan
**Solución:**
1. Inspecciona el HTML real de la página
2. Usa selectores más generales: `div`, `article`, `main`
3. Combina múltiples selectores: `"h1, h2, .title"`

### Problema: Muchas columnas en Excel
**Solución:**
- Reduce el número de keywords
- Reduce el número de áreas en `search_areas`
- Usa búsqueda general (`search_areas: null`)

### Problema: Timeout o errores de red
**Solución:**
- Verifica que la URL sea accesible
- Comprueba que el sitio permita scraping (robots.txt)
- El rate limiting de 1 segundo está activo por defecto

---

## 📊 Interpretación de Resultados

### Ejemplo de Salida en Excel

```
| timestamp           | url              | name      | titulo_python | contenido_python | titulo_javascript |
|---------------------|------------------|-----------|---------------|------------------|-------------------|
| 2025-01-15 20:00:00 | https://ej.com   | Ofertas   | 5             | 12               | 3                 |
| 2025-01-17 20:00:00 | https://ej.com   | Ofertas   | 7             | 15               | 4                 |
```

**Interpretación:**
- El 15/01: "python" apareció 5 veces en títulos y 12 en contenido
- El 17/01: "python" aumentó a 7 en títulos (¡más ofertas de Python!)
- "javascript" menos frecuente pero también aumentó

**Insights:**
- Tendencia al alza en ofertas de Python
- Mayor énfasis en Python que JavaScript
- Puedes comparar entre fechas para ver tendencias

---

## 🎓 Mejores Prácticas

### ✅ Recomendaciones

1. **Nombres descriptivos**: Usa nombres claros que identifiquen la fuente
2. **Keywords relevantes**: 4-8 keywords por configuración
3. **Áreas específicas**: 2-4 áreas máximo para claridad
4. **URLs estables**: Evita páginas que cambian estructura frecuentemente
5. **Respeta robots.txt**: El scraper ya implementa rate limiting de 1s

### ❌ Evitar

1. **Demasiadas keywords**: >15 keywords hace el Excel difícil de leer
2. **Selectores muy específicos**: Pueden romperse si cambia el HTML
3. **URLs dinámicas**: Sitios que requieren JavaScript para cargar contenido
4. **Sitios que bloquean bots**: Respeta las políticas de cada sitio

---

## 📞 Soporte

Si necesitas ayuda:
1. Revisa este archivo y el `README.md`
2. Consulta `REVIEW.md` para detalles técnicos
3. Mira `data/urls_config_example.json` para ejemplos
4. Inspecciona los comentarios en el código fuente

---

**¡El scraper está listo para usar!** 🚀

Simplemente edita `data/urls_config.json`, haz commit, y el GitHub Action lo ejecutará automáticamente martes y jueves a las 20:00.
