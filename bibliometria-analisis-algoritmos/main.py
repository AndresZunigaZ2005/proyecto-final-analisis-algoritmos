from src.download.downloader import descargar_datos
from src.similarity.edit_distance import calcular_distancia
from src.visualization.worldclouds import generar_nube

def main():
    print("=== Proyecto Bibliometría y Análisis de Algoritmos ===")

    # Requerimiento 1: Descargar y unificar datos
    archivo = descargar_datos("generative artificial intelligence")
    print(f"Datos descargados en: {archivo}")

    # Requerimiento 2: Similitud textual (ejemplo)
    t1 = "Generative AI models are transforming education"
    t2 = "AI generative models are changing the way we learn"
    dist = calcular_distancia(t1, t2)
    print(f"Distancia de edición entre abstracts: {dist}")

    # Requerimiento 5: Nube de palabras
    generar_nube([t1, t2], output_path="docs/nube.png")

if __name__ == "__main__":
    main()
