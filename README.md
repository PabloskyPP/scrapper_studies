# 🔍 Scraper Estudios

Scraper automatizado que extrae frecuencia de palabras clave de páginas web y almacena los resultados en Excel.

## 📋 Características

- Scraping de 10-15 páginas web con HTML estático
- Conteo de palabras clave en áreas específicas o generales del HTML
- Almacenamiento automático en Excel
- Ejecución programada: martes y jueves a las 20:00
- Notificaciones por Telegram
- Sincronización automática con OneDrive

## 🚀 Configuración inicial

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/scraper-estudios.git
cd scraper-estudios 
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Telegram

1. Crea un bot con [@BotFather](https://t.me/botfather):
   - Envía `/newbot`
   - Sigue las instrucciones
   - Guarda el token

2. Obtén tu Chat ID con [@userinfobot](https://t.me/userinfobot)

3. Para uso local, crea archivo `.env`:

```bash
cp .env.example .env
# Edita .env con tus credenciales
```

### 4. Configurar URLs y palabras clave

Edita `data/urls_config.json` con tus URLs y términos:

```json
[
  {
    "name": "Nombre descriptivo",
    "url": "https://tu-url.com",
    "keywords": ["palabra1", "palabra2"],
    "search_areas": {
      "titulo": "h1, h2",
      "contenido": "article"
    }
  }
]
```

**Opciones de `search_areas`:**
- Si defines áreas específicas, se contarán las palabras en cada área
- Si lo dejas como `null`, se buscará en todo el HTML

### 5. Configurar GitHub Secrets

Ve a: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

Añade:
- `TELEGRAM_BOT_TOKEN`: tu token de Telegram
- `TELEGRAM_CHAT_ID`: tu chat ID

## 🧪 Prueba local

```bash
python src/main.py
```

## 📅 Ejecución automática

El workflow se ejecuta automáticamente martes y jueves a las 20:00 (hora España).

**Nota importante:** GitHub Actions usa UTC. El cron está configurado para:
- **Invierno (CET/UTC+1):** `0 19 * * 2,4`
- **Verano (CEST/UTC+2):** Cambiar a `0 18 * * 2,4`

### Ejecución manual

Puedes ejecutarlo manualmente desde GitHub:
1. Ve a la pestaña `Actions`
2. Selecciona `Scraper Estudios`
3. Click en `Run workflow`

## 📊 Estructura del Excel

El Excel generado tendrá columnas como:

| timestamp | url | name | keyword1 | keyword2 | area_keyword1 |
|-----------|-----|------|----------|----------|---------------|
| 2025-01-15 20:00 | https://... | Sitio 1 | 5 | 3 | 2 |

## 📁 Estructura del proyecto

```
scraper-estudios/
├── .github/
│   └── workflows/
│       └── scraper.yml          # Workflow de GitHub Actions
├── src/
│   ├── config.py                # Configuración central
│   ├── scraper.py               # Lógica del scraper
│   ├── excel_handler.py         # Manejo del Excel
│   ├── notifier.py              # Notificaciones Telegram
│   └── main.py                  # Orquestador principal
├── data/
│   ├── scraper_estudios.xlsx    # Excel con resultados
│   └── urls_config.json         # Configuración de URLs
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

## 🔧 Mantenimiento

### Actualizar URLs
Edita `data/urls_config.json` y haz commit de los cambios.

### Ver resultados
- El Excel se actualiza en cada ejecución en el repositorio
- También se guarda como artefacto en GitHub Actions (30 días)
- Si tienes OneDrive sincronizado con tu carpeta local, verás los cambios automáticamente

### Logs
Revisa los logs en: `Actions` → selecciona una ejecución → mira los pasos

## ⚠️ Consideraciones

- **Respetar robots.txt**: El scraper incluye pausas entre peticiones
- **Rate limiting**: 1 segundo entre peticiones por defecto
- **HTML estático**: Este scraper está optimizado para HTML estático sin JavaScript dinámico
- **Sincronización OneDrive**: Si el Excel está en una carpeta sincronizada, asegúrate de hacer pull antes de trabajar localmente

## 📝 Notas adicionales

- El Excel se versiona en Git para tener historial completo
- Se guardan copias de seguridad en GitHub Actions (artifacts)
- Las notificaciones incluyen resumen de páginas procesadas y errores

## 🆘 Solución de problemas

**El workflow no se ejecuta:**
- Verifica que el repositorio no esté en modo privado sin GitHub Actions habilitado
- Comprueba la sintaxis del cron en el workflow

**No recibo notificaciones:**
- Verifica que los secrets de Telegram estén configurados correctamente
- Inicia conversación con tu bot antes de la primera ejecución

**Errores al guardar Excel:**
- Asegúrate de que la carpeta `data/` exista en el repositorio
- Verifica permisos de escritura en el workflow

## 📄 Licencia

MIT
