from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import os
from models import Cliente, Factura, LineaFactura
from config import settings

class GeneradorPDF:
    def __init__(self):
        self.width, self.height = A4
        if not os.path.exists(settings.PDF_OUTPUT_DIR):
            os.makedirs(settings.PDF_OUTPUT_DIR)

    def generar_factura(self, factura: Factura, cliente: Cliente):
        filename = f"{settings.PDF_OUTPUT_DIR}/factura_{factura.numero_factura}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        
        # Encabezado
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, self.height - 50, "FACTURA")
        
        # Datos de la empresa
        c.setFont("Helvetica", 12)
        c.drawString(50, self.height - 100, "Tu Empresa S.L.")
        c.drawString(50, self.height - 115, "CIF: B12345678")
        c.drawString(50, self.height - 130, "Dirección de la empresa")
        
        # Datos del cliente
        c.drawString(50, self.height - 180, f"Cliente: {cliente.nombre}")
        c.drawString(50, self.height - 195, f"NIF: {cliente.nif}")
        c.drawString(50, self.height - 210, f"Dirección: {cliente.direccion}")
        c.drawString(50, self.height - 225, f"{cliente.codigo_postal} - {cliente.ciudad}")
        
        # Datos de la factura
        c.drawString(400, self.height - 100, f"Nº Factura: {factura.numero_factura}")
        c.drawString(400, self.height - 115, f"Fecha: {factura.fecha_emision.strftime('%d/%m/%Y')}")
        
        # Tabla de líneas de factura
        data = [["Concepto", "Cantidad", "Precio", "Subtotal"]]
        for linea in factura.lineas:
            data.append([
                linea.concepto,
                str(linea.cantidad),
                f"{linea.precio_unitario:.2f} €",
                f"{linea.subtotal:.2f} €"
            ])
            
        table = Table(data, colWidths=[250, 75, 75, 75])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        table.wrapOn(c, self.width, self.height)
        table.drawOn(c, 50, self.height - 400)
        
        # Totales
        y_position = self.height - 450
        c.drawString(350, y_position, f"Base Imponible: {factura.base_imponible:.2f} €")
        c.drawString(350, y_position - 20, f"IVA ({int(factura.iva)}%): {(factura.base_imponible * factura.iva / 100):.2f} €")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(350, y_position - 40, f"Total: {factura.total:.2f} €")
        
        c.save()
        return filename 