# Proyecto: Bibliometría - Análisis de Algoritmos

Este repositorio contiene el trabajo para el curso *Análisis de Algoritmos* enfocado en análisis bibliométrico. Incluye scrapers (Playwright) para ACM, ScienceDirect y SAGE, procesamiento y unificación de metadatos, y análisis de similitud entre abstracts usando modelos modernos (Sentence-Transformers) y métodos clásicos.

> **Resumen rápido:**
>
> * `run_downloader.py`: descarga artículos por fuente y unifica/deduplica en `data/unified.csv`.
> * `run_similarity.py`: calcula similitud semántica entre abstracts y genera `data/similarities.csv`.

---

## Estructura del proyecto

```
bibliometria-analisis-algoritmos/
├─ data/                      # Salida: acm.csv, sciencedirect.csv, sage.csv, unified.csv, duplicates.csv, similarities.csv
├─ docs/
├─ notebooks/
├─ src/
│  ├─ download/
│  │  ├─ downloader.py        # scrapers por fuente
│  │  └─ merger.py            # unifica y deduplica CSV
│  ├─ similarity/
│  │  ├─ ai_models.py
│  │  ├─ vector_models.py
│  │  ├─ compare.py
│  │  ├─ classical.py
│  │  └─ edit_distance.py
│  └─ visualization/
├─ run_downloader.py
├─ run_similarity.py
├─ requirements.txt
└─ README.md
```

---

## Requisitos previos

* Python 3.8+ (preferible 3.10 o superior)
* Conexión a internet (descarga de modelos y acceso a sitios)
* Acceso institucional (opcional) para ScienceDirect/Elsevier si quieres extraer contenido detrás de paywall

---

## Instalación y primeros pasos (recomendado)

> Aconsejable: usar un entorno virtual para aislar dependencias.

### 1. Crear y activar entorno virtual

**Windows (PowerShell o CMD)**

```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python -m venv venv
source venv/bin/activate
```

Para salir del entorno (cuando termines):

```bash
deactivate
```

---

### 2. Instalar dependencias

Con el entorno virtual activado, en la raíz del proyecto:

```bash
pip install -r requirements.txt
```

> Si agregas nuevas librerías, actualiza `requirements.txt` y vuelve a ejecutar `pip install -r requirements.txt`.

### 3. Instalar navegadores para Playwright

```bash
python -m playwright install chromium
```

(Instala Chromium; si necesitas WebKit/Firefox puedes instalarlos también: `python -m playwright install webkit firefox`)

### 4. (Opcional) Instalar modelos SpaCy

Si utilizas funciones que requieran SpaCy con modelo en inglés:

```bash
python -m spacy download en_core_web_md
```

---

## Uso: Descarga y unificación (Requerimiento 1)

`run_downloader.py` orquesta la descarga y la unificación. Ejecuta desde la raíz del proyecto.

**Ejemplo (modo visible, recomendado para el primer run si necesitas hacer login manual):**

```bash
python run_downloader.py --query "generative artificial intelligence" --max 10 --delay 2
```

**Ejemplo (modo headless):**

```bash
python run_downloader.py --query "generative artificial intelligence" --max 30 --headless --delay 1
```

Parámetros principales:

* `--query` / `-q`: cadena de búsqueda.
* `--max` / `-m`: máximo artículos por base.
* `--headless`: si se pasa, el navegador corre sin interfaz (útil en servidores).
* `--delay`: segundos de `slow_mo` entre acciones (útil para evitar bloqueos).

### Notas sobre autenticación (ScienceDirect / Elsevier)

* Si ScienceDirect solicita login (pantalla de acceso institucional), ejecuta sin `--headless` para ver el navegador y accede manualmente.
* Para automatizar este inicio de sesión una vez, guarda el estado de sesión (cookies + localStorage) con Playwright y reutilízalo:

```python
# ejemplo rápido para guardar auth_state.json (ejecutar interactivo, iniciar sesión manualmente en la página y luego pulsar Enter)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.sciencedirect.com')
    input('Inicia sesión en la web y presiona Enter para guardar el estado...')
    context.storage_state(path='auth_state.json')
    browser.close()
```

Luego, modifica `src/download/downloader.py` para crear el contexto con `storage_state="auth_state.json"`:

```python
context = await browser.new_context(storage_state='auth_state.json')
```

Así la sesión se reutilizará y no tendrás que loguearte cada vez.

---

## Uso: Similitud de abstracts (Requerimiento 2)

Tras ejecutar `run_downloader.py` y obtener `data/unified.csv`, ejecuta:

```bash
python run_similarity.py
```

Esto realizará:

* Carga de `data/unified.csv`.
* Filtrado de abstracts vacíos.
* Cálculo de embeddings con `sentence-transformers/all-MiniLM-L6-v2`.
* Cálculo de similitud coseno entre todos los pares.
* Guardado de pares con similitud por encima del umbral en `data/similarities.csv`.

Parámetros (si deseas modificar):

* Ajusta el umbral dentro de `run_similarity.py` (valor por defecto 0.75).

---

## Archivos generados

* `data/acm.csv` — artículos extraídos de ACM
* `data/sciencedirect.csv` — artículos extraídos de ScienceDirect
* `data/sage.csv` — artículos extraídos de SAGE
* `data/unified.csv` — archivo unificado y deduplicado (salida de `merger.py`)
* `data/duplicates.csv` — registros considerados duplicados
* `data/similarities.csv` — pares de artículos con alta similitud semántica

---

## Debugging y problemas comunes

* **`pandas.errors.EmptyDataError: No columns to parse from file`** → indica que alguno de los CSV está vacío. Verifica `data/` y revisa los archivos fuente (`acm.csv`, `sciencedirect.csv`, `sage.csv`). Si están vacíos, ejecuta `run_downloader.py` en modo visible para ver errores o problemas de acceso.

* **ScienceDirect pide login** → ejecuta sin `--headless` y realiza login manual; luego guarda `auth_state.json` como se explicó.

* **Selectores rotos (no extrae título/abstract)** → abre la página en el navegador y usa el inspector (DevTools) para identificar selectores actuales en `src/download/downloader.py` y actualízalos.

* **Errores `.str` en pandas** → si aparece `Can only use .str accessor with string values`, convierta la columna con `df['abstract'] = df['abstract'].astype(str)` antes de aplicar `.str`.

---

## Buenas prácticas y recomendaciones

* Usa `--delay 1` o `--delay 2` en scraping para reducir la probabilidad de bloqueo por parte de los sitios.
* Mantén `requirements.txt` actualizado y crea un `venv` nuevo si cambias muchas dependencias.
* Respeta los términos de uso y `robots.txt` de cada proveedor. No automatices descargas de material con copyright sin autorización.

---

## Añadir nuevos scrapers o mejorar selectores

1. Abre `src/download/downloader.py` y busca la función correspondiente (`scrape_acm`, `scrape_sciencedirect`, `scrape_sage`).
2. Actualiza los selectores CSS en las líneas que usan `get_text()` o `eval_on_selector_all()`.
3. Prueba localmente en modo visible para depurar.
