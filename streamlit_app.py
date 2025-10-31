"""
Sistema de Análisis Bibliométrico - Interfaz Web
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

# Configuración de la página
st.set_page_config(
    page_title="Análisis Bibliométrico",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Agregar directorio al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

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
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
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
</style>
""", unsafe_allow_html=True)

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
         "📈 Visualizaciones"]
    )
    
    st.divider()
    
    # Estado de archivos
    st.markdown("### 📁 Estado del Sistema")
    data_dir = Path("data")
    
    if data_dir.exists():
        csv_files = list(data_dir.rglob("*.csv"))
        png_files = list(data_dir.rglob("*.png"))
        pdf_files = list(data_dir.rglob("*.pdf"))
        
        st.metric("📄 Archivos CSV", len(csv_files))
        st.metric("🖼️ Imágenes", len(png_files))
        st.metric("📑 PDFs", len(pdf_files))
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
        
        ### Bases de datos disponibles:
        - **OpenAlex**: 250M+ artículos multidisciplinarios
        - **arXiv**: 2M+ preprints de física, CS y matemáticas
        - **PubMed**: 35M+ artículos biomédicos
        
        ### Características:
        - ✅ 100% gratuito y open source
        - ✅ Sin necesidad de API keys
        - ✅ Análisis con modelos de IA modernos
        - ✅ Exportación a PDF y CSV
        """)
    
    # Footer con info del proyecto
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
    
    # Formulario de búsqueda
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
                    # Importar módulos
                    from src.download.downloader import run_all
                    from src.download.merger import merge_and_deduplicate
                    
                    # Ejecutar descarga
                    asyncio.run(run_all(query=query, sources=sources, max_results=max_results))
                    
                    # Unificar resultados
                    merge_and_deduplicate()
                
                st.markdown('<div class="success-box">✅ Descarga completada exitosamente</div>', unsafe_allow_html=True)
                
                # Mostrar resultados
                unified_path = "data/download/unified.csv"
                if os.path.exists(unified_path):
                    df = pd.read_csv(unified_path)
                    
                    # Métricas
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("📄 Total artículos", len(df))
                    col2.metric("👥 Autores únicos", df['authors'].nunique())
                    col3.metric("📚 Journals únicos", df['journal'].nunique())
                    col4.metric("📅 Años cubiertos", df['year'].nunique())
                    
                    # Tabla de resultados
                    st.markdown("### 📋 Artículos descargados")
                    st.dataframe(
                        df[['title', 'authors', 'year', 'journal', 'source']].head(20),
                        use_container_width=True
                    )
                    
                    # Gráfico de distribución por fuente
                    if len(df) > 0:
                        st.markdown("### 📊 Distribución por base de datos")
                        fig = px.pie(df, names='source', title='Artículos por fuente')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Descarga del CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descargar CSV completo",
                        data=csv,
                        file_name="articulos_descargados.csv",
                        mime="text/csv"
                    )
                
            except Exception as e:
                st.error(f"❌ Error durante la descarga: {e}")
                st.info("💡 Consejo: Verifica tu conexión a internet y que las APIs estén disponibles")

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
                    
                    # Cargar modelo
                    progress_text = st.empty()
                    progress_text.text("🤖 Cargando modelo de embeddings...")
                    model = load_sentence_model()
                    
                    # Preprocesar
                    progress_text.text("🔧 Preprocesando abstracts...")
                    df_clean = df[df['abstract'].notna()].copy()
                    df_clean = df_clean[df_clean['abstract'].astype(str).str.strip() != '']
                    
                    if len(df_clean) == 0:
                        st.error("❌ No hay abstracts válidos para analizar")
                        st.stop()
                    
                    # Generar embeddings
                    progress_text.text("🧮 Generando embeddings...")
                    embeddings = compute_embeddings(model, df_clean['abstract'].tolist())
                    
                    # Calcular similitudes
                    progress_text.text("🔗 Calculando similitudes...")
                    sim_df = compute_similarity(df_clean, embeddings, threshold=threshold)
                    
                    # Guardar
                    os.makedirs("data/similarity", exist_ok=True)
                    sim_path = "data/similarity/similarities.csv"
                    sim_df.to_csv(sim_path, index=False, encoding='utf-8')
                    
                    progress_text.empty()
                
                st.markdown('<div class="success-box">✅ Análisis completado</div>', unsafe_allow_html=True)
                
                # Métricas
                col1, col2, col3 = st.columns(3)
                col1.metric("🔗 Pares similares", len(sim_df))
                col2.metric("📄 Artículos analizados", len(df_clean))
                col3.metric("🎯 Umbral usado", f"{threshold:.2f}")
                
                if len(sim_df) > 0:
                    # Mostrar resultados
                    st.markdown("### 🔗 Pares de artículos similares")
                    st.dataframe(sim_df.head(20), use_container_width=True)
                    
                    # Histograma de similitudes
                    st.markdown("### 📊 Distribución de similitudes")
                    fig = px.histogram(
                        sim_df,
                        x='similarity',
                        nbins=20,
                        title='Distribución de scores de similitud'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Descarga
                    csv = sim_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descargar resultados",
                        data=csv,
                        file_name="similitudes.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning(f"⚠️ No se encontraron pares similares con threshold ≥ {threshold}")
                    st.info("💡 Intenta reducir el umbral de similitud")
                
            except Exception as e:
                st.error(f"❌ Error: {e}")

# ==================== PÁGINA: ESTADÍSTICAS ====================
elif page == "📊 Estadísticas y Reportes":
    st.markdown("## 📊 Análisis Estadístico y Reportes")
    
    st.markdown('<div class="info-box">Genera reportes con métricas bibliométricas detalladas</div>', unsafe_allow_html=True)
    
    unified_path = "data/download/unified.csv"
    
    if not os.path.exists(unified_path):
        st.markdown('<div class="warning-box">⚠️ Primero debes ejecutar el módulo de Descarga</div>', unsafe_allow_html=True)
    else:
        df = pd.read_csv(unified_path)
        
        # Métricas generales
        st.markdown("### 📈 Métricas Generales")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📄 Total artículos", len(df))
        col2.metric("👥 Autores", df['authors'].nunique())
        col3.metric("📚 Journals", df['journal'].nunique())
        col4.metric("📅 Años", df['year'].nunique())
        
        # Artículos por año
        if 'year' in df.columns:
            st.markdown("### 📅 Producción por Año")
            year_counts = df['year'].value_counts().sort_index()
            fig = px.bar(
                x=year_counts.index,
                y=year_counts.values,
                labels={'x': 'Año', 'y': 'Número de artículos'},
                title='Distribución temporal de publicaciones'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Top journals
        if 'journal' in df.columns:
            st.markdown("### 📚 Top 10 Journals")
            top_journals = df['journal'].value_counts().head(10)
            fig = px.bar(
                x=top_journals.values,
                y=top_journals.index,
                orientation='h',
                labels={'x': 'Número de artículos', 'y': 'Journal'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Generar reporte PDF
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
                        st.success("✅ Reporte generado exitosamente")
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
                    
                    # Mostrar dendrogramas
                    img_path = f"data/clustering/dendrogram_{method}.png"
                    if os.path.exists(img_path):
                        st.image(img_path, caption=f"Dendrograma ({method} linkage)")
                    
                    # Mostrar todos los métodos
                    st.markdown("### 📊 Comparación de Métodos")
                    cols = st.columns(3)
                    for idx, m in enumerate(["single", "complete", "average"]):
                        img = f"data/clustering/dendrogram_{m}.png"
                        if os.path.exists(img):
                            with cols[idx]:
                                st.image(img, caption=f"{m.capitalize()}")
                
                except Exception as e:
                    st.error(f"❌ Error: {e}")

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
                
                # Mostrar imágenes generadas
                viz_dir = Path("data/visualization")
                if viz_dir.exists():
                    images = list(viz_dir.glob("*.png"))
                    
                    if images:
                        st.markdown("### 🖼️ Visualizaciones Generadas")
                        for img in images:
                            st.image(str(img), caption=img.stem.replace('_', ' ').title())
                    
                    # PDF si existe
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