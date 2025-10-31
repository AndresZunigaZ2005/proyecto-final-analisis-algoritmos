from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

class ReportGenerator:
    def __init__(self, metrics, output_dir="data/analysis"):
        self.metrics = metrics
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save_summary(self):
        """Genera un PDF con el resumen completo del análisis."""
        pdf_path = os.path.join(self.output_dir, "reporte_requerimiento_3.pdf")
        doc = SimpleDocTemplate(pdf_path)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("<b>Reporte Requerimiento 3 - Análisis Bibliométrico</b>", styles["Title"]))
        elements.append(Spacer(1, 12))

        # Frecuencias
        elements.append(Paragraph("<b>Frecuencia de palabras asociadas</b>", styles["Heading2"]))
        freq_data = [["Palabra", "Frecuencia"]] + [[k, v] for k, v in self.metrics["keyword_freq"].items()]
        table = Table(freq_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.grey),
            ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

        # Nuevas palabras
        elements.append(Paragraph("<b>Nuevas palabras relevantes (TF-IDF)</b>", styles["Heading2"]))
        for word in self.metrics["new_keywords"]:
            elements.append(Paragraph(f"• {word}", styles["Normal"]))

        # Precisión
        elements.append(Spacer(1, 12))
        precision = round(self.metrics["precision"] * 100, 2)
        elements.append(Paragraph(f"<b>Precisión de nuevas palabras:</b> {precision}% de coincidencia con las palabras base", styles["Normal"]))

        doc.build(elements)
        print(f"✅ Reporte generado en {pdf_path}")
