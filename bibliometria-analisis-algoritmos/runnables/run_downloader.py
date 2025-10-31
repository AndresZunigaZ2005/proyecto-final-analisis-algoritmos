import os
import sys
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.download.downloader import run_all
from src.download.merger import merge_and_deduplicate

if __name__ == "__main__":
    print("🔍 Requerimiento 1 - Descarga de artículos")

    query = input("🧠 Ingresa la cadena de búsqueda: ").strip()
    
    print("\n📚 Bases de datos disponibles (100% ABIERTAS - Sin captcha):")
    print("1. OpenAlex    - 250M+ artículos, todas las disciplinas")
    print("2. arXiv       - 2M+ preprints (física, CS, matemáticas)")
    print("3. PubMed      - 35M+ artículos biomédicos")
    print("4. Todas las disponibles")
    
    option = input("\nSelecciona la base de datos (1-4): ").strip()

    if option == "1":
        sources = ["openalex"]
    elif option == "2":
        sources = ["arxiv"]
    elif option == "3":
        sources = ["pubmed"]
    else:
        sources = ["openalex", "arxiv", "pubmed"]

    max_results = int(input("\n¿Cuántos artículos deseas descargar por fuente? (recomendado: 10-50): ") or "10")

    print(f"\n🚀 Buscando '{query}' en {', '.join(sources)}...")
    print("⚡ Usando solo APIs REST - Sin web scraping - Rápido y confiable")
    
    asyncio.run(run_all(query=query, sources=sources, max_results=max_results))

    print("\n🔗 Unificando resultados...")
    merge_and_deduplicate()
    print("\n✅ Descarga y unificación completadas.")
    print("📁 Archivos guardados en: data/download/")