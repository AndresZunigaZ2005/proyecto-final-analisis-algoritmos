import os
import sys
import subprocess

def run_script(script_name):
    """Ejecuta un script Python dentro de la carpeta runnables/."""
    script_path = os.path.join("runnables", script_name)
    if not os.path.exists(script_path):
        print(f"❌ No se encontró el archivo {script_path}")
        return
    subprocess.run([sys.executable, script_path])

def main():
    while True:
        print("\n=== PROYECTO BIBLIOMETRÍA - ANÁLISIS DE ALGORITMOS ===")
        print("1. Requerimiento 1 - Descarga y Unificación de Artículos")
        print("2. Requerimiento 2 - Análisis de Similitud Semántica")
        print("3. Requerimiento 3 - Análisis Estadístico y Reporte PDF")
        print("4. Requerimiento 4 - Clustering jerárquico y Dendrogramas")
        print("5. Requerimiento 5 - Visualización de la producción científica (mapa, nube dinámica, timeline, export PDF)")
        print("6. Salir")
        opcion = input("\nSelecciona una opción (1-6): ").strip()

        if opcion == "1":
            run_script("run_downloader.py")
        elif opcion == "2":
            run_script("run_similarity.py")
        elif opcion == "3":
            run_script("run_analysis.py")
        elif opcion == "4":
            run_script("run_clustering.py")
        elif opcion == "5":
            run_script("run_viz_geo.py")
        elif opcion == "6":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
