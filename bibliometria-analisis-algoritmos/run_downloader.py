import asyncio
from src.download.downloader import run_all
from src.download.merger import merge_and_deduplicate

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Descarga y unifica artículos científicos (Requerimiento 1).")
    parser.add_argument("--query", "-q", default="generative artificial intelligence", help="Cadena de búsqueda")
    parser.add_argument("--max", "-m", type=int, default=30, help="Número máximo de artículos por base de datos")
    parser.add_argument("--headless", action="store_true", help="Ejecutar sin interfaz gráfica (modo headless)")
    parser.add_argument("--delay", type=float, default=1.0, help="Retraso entre acciones (segundos)")
    args = parser.parse_args()

    print(f"\n🔍 Iniciando scraping con query: '{args.query}'")
    asyncio.run(run_all(
        query=args.query,
        max_results=args.max,
        headless=args.headless,
        delay_between_requests=args.delay
    ))

    print("\n📂 Unificando y eliminando duplicados...")
    merge_and_deduplicate()
    print("\n✅ Proceso terminado. Revisa la carpeta 'data/' para ver los CSV generados.")
