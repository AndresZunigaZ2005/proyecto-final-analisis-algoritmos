import os
import sys
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.download.downloader import run_all
from src.download.merger import merge_and_deduplicate

if __name__ == "__main__":
    print("🔍 Requerimiento 1 - Descarga de artículos")

    query = input("🧠 Ingresa la cadena de búsqueda: ").strip()
    print("\nBases de datos disponibles:")
    print("1. ACM\n2. ScienceDirect\n3. SAGE\n4. Todas")
    option = input("Selecciona la base de datos (1-4): ").strip()

    if option == "1":
        sources = ["acm"]
    elif option == "2":
        sources = ["sciencedirect"]
    elif option == "3":
        sources = ["sage"]
    else:
        sources = ["acm", "sciencedirect", "sage"]

    max_results = int(input("¿Cuántos artículos deseas descargar (máximo 10 por fuente)? ") or "10")

    print(f"\n🧩 Buscando '{query}' en {', '.join(sources)} ...")
    asyncio.run(run_all(query=query, sources=sources, max_results=max_results, headless=False))

    print("\n🔗 Unificando resultados...")
    merge_and_deduplicate()
    print("✅ Descarga y unificación completadas.")
