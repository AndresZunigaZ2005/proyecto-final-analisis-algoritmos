"""
Sistema de Análisis Bibliométrico - Interfaz Web Completa
Proyecto Final - Análisis de Algoritmos
"""

import streamlit as st
import os
import sys
import asyncio
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import base64
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Análisis Bibliométrico",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Agregar directorio al path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .result-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Funciones helper
def get_pdf_download_link(file_path, link_text):
    """Genera link de descarga para PDF"""
    try:
        with open(file_path, "rb") as f:
            bytes_data = f.read()
            b64 = base64.b64encode(bytes_data).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="{os.path.basename(file_path)}">{link_text}</a>'
            return href
    except:
        return ""

def display_csv_preview(file_path, title=""):
    """Muestra preview de CSV con opción de descarga"""
    try:
        df = pd.read_csv(file_path)
        if title:
            st.markdown(f"#### 📄 {title}")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"📊 Total de registros: **{len(df)}** | Columnas: **{len(df.columns)}**")
        with col2:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name=os.path.basename(file_path),
                mime="text/csv",
                key=f"download_{os.path.basename(file_path)}"
            )
        
        st.dataframe(df.head(20), use_container_width=True)
        
        with st.expander(f"📊 Estadísticas de {title or 'datos'}"):
            st.write(df.describe())
        
        return df
    except Exception as e:
        st.error(f"Error al cargar {file_path}: {e}")
        return None

def display_image(file_path, caption=""):
    """Muestra imagen con opción de descarga"""
    try:
        st.image(file_path, caption=caption, use_column_width=True)
        with open(file_path, "rb") as f:
            st.download_button(
                label="📥 Descargar imagen",
                data=f,
                file_name=os.path.basename(file_path),
                mime="image/png",
                key=f"img_{os.path.basename(file_path)}"
            )
    except Exception as e:
        st.error(f"Error al mostrar imagen: {e}")

def display_html(file_path, title=""):
    """Muestra HTML embebido"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        if title:
            st.markdown(f"#### 🗺️ {title}")
        
        # Usar iframe para mostrar HTML
        st.components.v1.html(html_content, height=600, scrolling=True)
        
        with open(file_path, "rb") as f:
            st.download_button(
                label="📥 Descargar HTML",
                data=f,
                file_name=os.path.basename(file_path),
                mime="text/html",
                key=f"html_{os.path.basename(file_path)}"
            )
    except Exception as e:
        st.error(f"Error al mostrar HTML: {e}")

# Header
st.markdown('<div class="main-header">📚 Sistema de Análisis Bibliométrico</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Análisis de Algoritmos - Proyecto Final</div>', unsafe_allow_html=True)

# Sidebar con navegación
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/literature.png", width=80)
    st.markdown("### 🧭 Navegación")
    
    page = st.radio(
        "Selecciona un módulo:",
        ["🏠 Inicio", 
         "📥 Descarga de Artículos", 
         "🔍 Análisis de Similitud", 
         "📊 Estadísticas y Reportes",
         "🌳 Clustering Jerárquico", 
         "📈 Visualizaciones",
         "📁 Ver Todos los Resultados"]
    )
    
    st.divider()
    
    # Estado de archivos
    st.markdown("### 📁 Estado del Sistema")
    data_dir = Path("data")
    
    if data_dir.exists():
        csv_files = list(data_dir.rglob("*.csv"))
        png_files = list(data_dir.rglob("*.png"))
        pdf_files = list(data_dir.rglob("*.pdf"))
        html_files = list(data_dir.rglob("*.html"))
        
        st.metric("📄 CSV", len(csv_files))
        st.metric("🖼️ PNG", len(png_files))
        st.metric("📑 PDF", len(pdf_files))
        st.metric("🗺️ HTML", len(html_files))
    else:
        st.info("No hay datos aún")

# ==================== PÁGINA: INICIO ====================
if page == "🏠 Inicio":
    st.markdown("## 👋 Bienvenido al Sistema de Análisis Bibliométrico")
    
    st.markdown("""
    Este sistema te permite realizar análisis bibliométricos completos de forma automatizada.
    """)
    
    # Métricas en columnas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 📥 Módulo 1")
        st.markdown("**Descarga de Artículos**")
        st.markdown("Extrae artículos de OpenAlex, arXiv y PubMed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Módulo 2")
        st.markdown("**Análisis de Similitud**")
        st.markdown("Identifica artículos similares usando IA")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Módulo 3")
        st.markdown("**Estadísticas**")
        st.markdown("Genera reportes y métricas bibliométricas")
        st.markdown('</div>', unsafe_allow_html=True)
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🌳 Módulo 4")
        st.markdown("**Clustering**")
        st.markdown("Agrupa artículos por similitud temática")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 📈 Módulo 5")
        st.markdown("**Visualizaciones**")
        st.markdown("Mapas, wordclouds y gráficos interactivos")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Instrucciones
    with st.expander("📖 ¿Cómo usar el sistema?", expanded=True):
        st.markdown("""
        ### Flujo de trabajo recomendado:
        
        1. **📥 Descarga**: Comienza extrayendo artículos de bases de datos académicas
        2. **🔍 Similitud**: Analiza qué artículos son similares entre sí
        3. **📊 Estadísticas**: Genera reportes con métricas bibliométricas
        4. **🌳 Clustering**: Visualiza agrupaciones de artículos relacionados
        5. **📈 Visualizaciones**: Explora mapas geográficos y tendencias temporales
        6. **📁 Resultados**: Ve todos los archivos generados en un solo lugar
        
        ### Bases de datos disponibles:
        - **OpenAlex**: 250M+ artículos multidisciplinarios
        - **arXiv**: 2M+ preprints de física, CS y matemáticas
        - **PubMed**: 35M+ artículos biomédicos
        
        ### Características:
        - ✅ 100% gratuito y open source
        - ✅ Sin necesidad de API keys
        - ✅ Análisis con modelos de IA modernos
        - ✅ Exportación a PDF, CSV, PNG y HTML
        """)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        Desarrollado para el curso de Análisis de Algoritmos<br>
        Universidad del Quindío • 2024
    </div>
    """, unsafe_allow_html=True)

# ==================== PÁGINA: DESCARGA ====================
elif page == "📥 Descarga de Artículos":
    st.markdown("## 📥 Descarga de Artículos Científicos")
    
    st.markdown('<div class="info-box">Extrae artículos académicos de bases de datos abiertas usando APIs REST</div>', unsafe_allow_html=True)
    
    with st.form("download_form"):
        query = st.text_input(
            "🔎 Cadena de búsqueda:",
            placeholder="Ejemplo: machine learning algorithms",
            help="Ingresa términos de búsqueda en inglés para mejores resultados"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            sources = st.multiselect(
                "📚 Bases de datos:",
                ["openalex", "arxiv", "pubmed"],
                default=["openalex"],
                help="Selecciona una o más bases de datos"
            )
        
        with col2:
            max_results = st.number_input(
                "📊 Artículos por fuente:",
                min_value=1,
                max_value=50,
                value=10,
                help="Cantidad de artículos a descargar de cada base"
            )
        
        submitted = st.form_submit_button("🚀 Iniciar Descarga", use_container_width=True)
    
    if submitted:
        if not query:
            st.error("❌ Debes ingresar una cadena de búsqueda")
        elif not sources:
            st.error("❌ Debes seleccionar al menos una base de datos")
        else:
            try:
                with st.spinner("⏳ Descargando artículos... Esto puede tomar unos minutos."):
                    from src.download.downloader import run_all
                    from src.download.merger import merge_and_deduplicate
                    
                    asyncio.run(run_all(query=query, sources=sources, max_results=max_results))
                    merge_and_deduplicate()
                
                st.markdown('<div class="success-box">✅ Descarga completada exitosamente</div>', unsafe_allow_html=True)
                
                unified_path = "data/download/unified.csv"
                if os.path.exists(unified_path):
                    df = display_csv_preview(unified_path, "Artículos Unificados")
                    
                    if df is not None:
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("📄 Total artículos", len(df))
                        col2.metric("👥 Autores únicos", df['authors'].nunique() if 'authors' in df.columns else 0)
                        col3.metric("📚 Journals únicos", df['journal'].nunique() if 'journal' in df.columns else 0)
                        col4.metric("📅 Años", df['year'].nunique() if 'year' in df.columns else 0)
                        
                        if 'source' in df.columns and len(df) > 0:
                            st.markdown("### 📊 Distribución por base de datos")
                            fig = px.pie(df, names='source', title='Artículos por fuente')
                            st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error durante la descarga: {e}")
                st.exception(e)

# ==================== PÁGINA: SIMILITUD ====================
elif page == "🔍 Análisis de Similitud":
    st.markdown("## 🔍 Análisis de Similitud Semántica")
    
    st.markdown('<div class="info-box">Identifica artículos similares usando embeddings de transformers</div>', unsafe_allow_html=True)
    
    unified_path = "data/download/unified.csv"
    
    if not os.path.exists(unified_path):
        st.markdown('<div class="warning-box">⚠️ Primero debes ejecutar el módulo de Descarga</div>', unsafe_allow_html=True)
    else:
        df = pd.read_csv(unified_path)
        st.info(f"📄 Artículos disponibles para análisis: **{len(df)}**")
        
        threshold = st.slider(
            "🎯 Umbral de similitud:",
            min_value=0.0,
            max_value=1.0,
            value=0.75,
            step=0.05,
            help="Valores más altos = mayor similitud requerida"
        )
        
        if st.button("🔍 Analizar Similitudes", use_container_width=True):
            try:
                with st.spinner("⏳ Calculando similitudes... Esto puede tomar varios minutos."):
                    from src.similarity.ai_models import load_sentence_model
                    from src.similarity.vector_models import compute_embeddings
                    from src.similarity.compare import compute_similarity
                    
                    progress_text = st.empty()
                    progress_text.text("🤖 Cargando modelo...")
                    model = load_sentence_model()
                    
                    progress_text.text("🔧 Preprocesando...")
                    df_clean = df[df['abstract'].notna()].copy()
                    df_clean = df_clean[df_clean['abstract'].astype(str).str.strip() != '']
                    
                    if len(df_clean) == 0:
                        st.error("❌ No hay abstracts válidos")
                        st.stop()
                    
                    progress_text.text("🧮 Generando embeddings...")
                    embeddings = compute_embeddings(model, df_clean['abstract'].tolist())
                    
                    progress_text.text("🔗 Calculando similitudes...")
                    sim_df = compute_similarity(df_clean, embeddings, threshold=threshold)
                    
                    os.makedirs("data/similarity", exist_ok=True)
                    sim_path = "data/similarity/similarities.csv"
                    sim_df.to_csv(sim_path, index=False, encoding='utf-8')
                    
                    progress_text.empty()
                
                st.markdown('<div class="success-box">✅ Análisis completado</div>', unsafe_allow_html=True)
                
                if os.path.exists(sim_path):
                    display_csv_preview(sim_path, "Similitudes Encontradas")
                    
                    if len(sim_df) > 0 and 'similarity' in sim_df.columns:
                        st.markdown("### 📊 Distribución de similitudes")
                        fig = px.histogram(sim_df, x='similarity', nbins=20, 
                                         title='Distribución de scores de similitud')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning(f"⚠️ No se encontraron pares similares con threshold ≥ {threshold}")
                
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.exception(e)

# ==================== PÁGINA: ESTADÍSTICAS ====================
elif page == "📊 Estadísticas y Reportes":
    st.markdown("## 📊 Análisis Estadístico y Reportes")
    
    st.markdown('<div class="info-box">Genera reportes con métricas bibliométricas detalladas</div>', unsafe_allow_html=True)
    
    unified_path = "data/download/unified.csv"
    
    if not os.path.exists(unified_path):
        st.markdown('<div class="warning-box">⚠️ Primero debes ejecutar el módulo de Descarga</div>', unsafe_allow_html=True)
    else:
        df = pd.read_csv(unified_path)
        
        st.markdown("### 📈 Métricas Generales")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📄 Total artículos", len(df))
        col2.metric("👥 Autores", df['authors'].nunique() if 'authors' in df.columns else 0)
        col3.metric("📚 Journals", df['journal'].nunique() if 'journal' in df.columns else 0)
        col4.metric("📅 Años", df['year'].nunique() if 'year' in df.columns else 0)
        
        if 'year' in df.columns:
            st.markdown("### 📅 Producción por Año")
            year_counts = df['year'].value_counts().sort_index()
            fig = px.bar(x=year_counts.index, y=year_counts.values,
                        labels={'x': 'Año', 'y': 'Artículos'})
            st.plotly_chart(fig, use_container_width=True)
        
        if 'journal' in df.columns:
            st.markdown("### 📚 Top 10 Journals")
            top_journals = df['journal'].value_counts().head(10)
            fig = px.bar(x=top_journals.values, y=top_journals.index, orientation='h',
                        labels={'x': 'Artículos', 'y': 'Journal'})
            st.plotly_chart(fig, use_container_width=True)
        
        if st.button("📄 Generar Reporte PDF", use_container_width=True):
            with st.spinner("⏳ Generando reporte..."):
                try:
                    import subprocess
                    subprocess.run([sys.executable, "runnables/run_analysis.py"], check=True)
                    
                    pdf_path = "data/reports/analysis_report.pdf"
                    if os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="📥 Descargar Reporte PDF",
                                data=f,
                                file_name="analisis_bibliometrico.pdf",
                                mime="application/pdf"
                            )
                        st.success("✅ Reporte generado")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ==================== PÁGINA: CLUSTERING ====================
elif page == "🌳 Clustering Jerárquico":
    st.markdown("## 🌳 Clustering Jerárquico")
    
    st.markdown('<div class="info-box">Agrupa artículos similares usando algoritmos de clustering</div>', unsafe_allow_html=True)
    
    unified_path = "data/download/unified.csv"
    
    if not os.path.exists(unified_path):
        st.markdown('<div class="warning-box">⚠️ Primero debes ejecutar el módulo de Descarga</div>', unsafe_allow_html=True)
    else:
        method = st.selectbox(
            "🔗 Método de linkage:",
            ["average", "single", "complete"],
            help="Average generalmente da mejores resultados"
        )
        
        if st.button("🌳 Generar Dendrograma", use_container_width=True):
            with st.spinner("⏳ Generando clustering..."):
                try:
                    import subprocess
                    subprocess.run([sys.executable, "runnables/run_clustering.py"], check=True)
                    
                    st.success("✅ Clustering completado")
                    
                    st.markdown("### 📊 Dendrogramas Generados")
                    cols = st.columns(3)
                    for idx, m in enumerate(["single", "complete", "average"]):
                        img_path = f"data/clustering/dendrogram_{m}.png"
                        if os.path.exists(img_path):
                            with cols[idx]:
                                st.markdown(f"**{m.capitalize()} Linkage**")
                                display_image(img_path, f"Dendrograma {m}")
                
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.exception(e)

# ==================== PÁGINA: VISUALIZACIONES ====================
elif page == "📈 Visualizaciones":
    st.markdown("## 📈 Visualizaciones Interactivas")
    
    st.markdown('<div class="info-box">Explora los datos con mapas geográficos, wordclouds y timelines</div>', unsafe_allow_html=True)
    
    if st.button("🎨 Generar Todas las Visualizaciones", use_container_width=True):
        with st.spinner("⏳ Generando visualizaciones..."):
            try:
                import subprocess
                subprocess.run([sys.executable, "runnables/run_viz_geo.py"], check=True)
                
                st.success("✅ Visualizaciones generadas")
                
                viz_dir = Path("data/visualization")
                if viz_dir.exists():
                    # Mostrar imágenes
                    images = list(viz_dir.glob("*.png"))
                    if images:
                        st.markdown("### 🖼️ Gráficos Generados")
                        for img in images:
                            st.markdown(f"#### {img.stem.replace('_', ' ').title()}")
                            display_image(str(img), img.stem)
                    
                    # Mostrar HTMLs
                    htmls = list(viz_dir.glob("*.html"))
                    if htmls:
                        st.markdown("### 🗺️ Mapas Interactivos")
                        for html in htmls:
                            display_html(str(html), html.stem.replace('_', ' ').title())
                    
                    # PDF
                    pdf_path = viz_dir / "visual_analysis.pdf"
                    if pdf_path.exists():
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="📥 Descargar Reporte Visual PDF",
                                data=f,
                                file_name="visualizaciones.pdf",
                                mime="application/pdf"
                            )
            
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.exception(e)

# ==================== PÁGINA: VER TODOS LOS RESULTADOS ====================
elif page == "📁 Ver Todos los Resultados":
    st.markdown("## 📁 Explorador de Resultados")
    
    st.markdown('<div class="info-box">Visualiza todos los archivos generados por cada requerimiento</div>', unsafe_allow_html=True)
    
    data_dir = Path("data")
    
    if not data_dir.exists():
        st.warning("⚠️ No hay datos generados aún. Ejecuta primero los módulos de análisis.")
    else:
        # Tabs por requerimiento
        tabs = st.tabs(["📥 Req 1: Descarga", "🔍 Req 2: Similitud", "📊 Req 3: Análisis", 
                        "🌳 Req 4: Clustering", "📈 Req 5: Visualización"])
        
        # REQUERIMIENTO 1: Descarga
        with tabs[0]:
            st.markdown("### 📥 Requerimiento 1 - Descarga y Unificación")
            download_dir = data_dir / "download"
            
            if download_dir.exists():
                csv_files = list(download_dir.glob("*.csv"))
                if csv_files:
                    for csv_file in csv_files:
                        with st.expander(f"📄 {csv_file.stem}", expanded=(csv_file.stem == "unified")):
                            display_csv_preview(str(csv_file), csv_file.stem)
                else:
                    st.info("No hay archivos CSV de descarga aún")
            else:
                st.info("Ejecuta el módulo de descarga primero")
        
        # REQUERIMIENTO 2: Similitud
        with tabs[1]:
            st.markdown("### 🔍 Requerimiento 2 - Análisis de Similitud")
            similarity_dir = data_dir / "similarity"
            
            if similarity_dir.exists():
                csv_files = list(similarity_dir.glob("*.csv"))
                if csv_files:
                    for csv_file in csv_files:
                        with st.expander(f"📄 {csv_file.stem}", expanded=True):
                            display_csv_preview(str(csv_file), csv_file.stem)
                else:
                    st.info("No hay resultados de similitud aún")
            else:
                st.info("Ejecuta el módulo de similitud primero")
        
        # REQUERIMIENTO 3: Análisis
        with tabs[2]:
            st.markdown("### 📊 Requerimiento 3 - Análisis Estadístico")
            reports_dir = data_dir / "reports"
            
            if reports_dir.exists():
                # PDFs
                pdf_files = list(reports_dir.glob("*.pdf"))
                if pdf_files:
                    st.markdown("#### 📑 Reportes PDF")
                    for pdf in pdf_files:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{pdf.stem}**")
                        with col2:
                            with open(pdf, "rb") as f:
                                st.download_button(
                                    label="📥 Descargar",
                                    data=f,
                                    file_name=pdf.name,
                                    mime="application/pdf",
                                    key=f"pdf_{pdf.stem}"
                                )
                
                # CSVs de análisis
                csv_files = list(reports_dir.glob("*.csv"))
                if csv_files:
                    st.markdown("#### 📊 Datos de Análisis")
                    for csv in csv_files:
                        with st.expander(f"📄 {csv.stem}"):
                            display_csv_preview(str(csv), csv.stem)
                
                if not pdf_files and not csv_files:
                    st.info("No hay reportes generados aún")
            else:
                st.info("Ejecuta el módulo de análisis primero")
        
        # REQUERIMIENTO 4: Clustering
        with tabs[3]:
            st.markdown("### 🌳 Requerimiento 4 - Clustering Jerárquico")
            clustering_dir = data_dir / "clustering"
            
            if clustering_dir.exists():
                png_files = list(clustering_dir.glob("*.png"))
                if png_files:
                    cols = st.columns(min(len(png_files), 3))
                    for idx, png in enumerate(png_files):
                        with cols[idx % 3]:
                            st.markdown(f"**{png.stem.replace('_', ' ').title()}**")
                            display_image(str(png), png.stem)
                else:
                    st.info("No hay dendrogramas generados aún")
            else:
                st.info("Ejecuta el módulo de clustering primero")
        
        # REQUERIMIENTO 5: Visualización
        with tabs[4]:
            st.markdown("### 📈 Requerimiento 5 - Visualizaciones")
            viz_dir = data_dir / "visualization"
            
            if viz_dir.exists():
                # Imágenes PNG
                png_files = list(viz_dir.glob("*.png"))
                if png_files:
                    st.markdown("#### 🖼️ Gráficos")
                    for png in png_files:
                        with st.expander(f"📊 {png.stem.replace('_', ' ').title()}", expanded=True):
                            display_image(str(png), png.stem)
                
                # Mapas HTML
                html_files = list(viz_dir.glob("*.html"))
                if html_files:
                    st.markdown("#### 🗺️ Mapas Interactivos")
                    for html in html_files:
                        with st.expander(f"🗺️ {html.stem.replace('_', ' ').title()}", expanded=True):
                            display_html(str(html), html.stem)
                
                # PDFs
                pdf_files = list(viz_dir.glob("*.pdf"))
                if pdf_files:
                    st.markdown("#### 📑 Reportes Visuales")
                    for pdf in pdf_files:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{pdf.stem}**")
                        with col2:
                            with open(pdf, "rb") as f:
                                st.download_button(
                                    label="📥 Descargar",
                                    data=f,
                                    file_name=pdf.name,
                                    mime="application/pdf",
                                    key=f"viz_pdf_{pdf.stem}"
                                )
                
                if not png_files and not html_files and not pdf_files:
                    st.info("No hay visualizaciones generadas aún")
            else:
                st.info("Ejecuta el módulo de visualización primero")
        
        # Resumen general
        st.divider()
        st.markdown("### 📊 Resumen General de Archivos")
        
        all_files = {
            "CSV": list(data_dir.rglob("*.csv")),
            "PNG": list(data_dir.rglob("*.png")),
            "PDF": list(data_dir.rglob("*.pdf")),
            "HTML": list(data_dir.rglob("*.html"))
        }
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📄 CSV", len(all_files["CSV"]))
        col2.metric("🖼️ PNG", len(all_files["PNG"]))
        col3.metric("📑 PDF", len(all_files["PDF"]))
        col4.metric("🗺️ HTML", len(all_files["HTML"]))
        
        # Botón para descargar todo
        if any(len(files) > 0 for files in all_files.values()):
            if st.button("📦 Descargar Todos los Archivos (ZIP)", use_container_width=True):
                try:
                    import zipfile
                    from io import BytesIO
                    
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for file_type, files in all_files.items():
                            for file_path in files:
                                arcname = f"{file_path.parent.name}/{file_path.name}"
                                zip_file.write(file_path, arcname)
                    
                    zip_buffer.seek(0)
                    st.download_button(
                        label="📥 Descargar ZIP",
                        data=zip_buffer.getvalue(),
                        file_name="resultados_bibliometria.zip",
                        mime="application/zip"
                    )
                except Exception as e:
                    st.error(f"Error al crear ZIP: {e}")