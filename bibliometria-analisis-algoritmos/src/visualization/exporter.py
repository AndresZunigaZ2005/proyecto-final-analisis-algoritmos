import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

def images_to_pdf(image_paths, out_pdf):
    """
    Combina varias imágenes en un solo archivo PDF.
    Parámetros:
        image_paths: lista de rutas de las imágenes a incluir.
        out_pdf: ruta del PDF de salida.
    """
    os.makedirs(os.path.dirname(out_pdf), exist_ok=True)

    with PdfPages(out_pdf) as pdf:
        for img in image_paths:
            if not os.path.exists(img):
                print(f"⚠️ Imagen no encontrada: {img}")
                continue
            fig = plt.figure()
            plt.imshow(plt.imread(img))
            plt.axis("off")
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

    print(f"✅ PDF generado correctamente en: {out_pdf}")
