# report_generator.py
import os
import traceback
from datetime import datetime
import io

try:
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib.units import cm, mm
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape, portrait
    from reportlab.lib.utils import ImageReader
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    SimpleDocTemplate=Table=TableStyle=Paragraph=Spacer=Image=PageBreak=getSampleStyleSheet=ParagraphStyle=None
    TA_CENTER=TA_LEFT=TA_RIGHT=1; cm=28.3; mm=2.83; colors=None; A4=landscape=portrait=ImageReader=None

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False
    qrcode = None

from PySide2.QtCore import QStandardPaths, QDateTime

class ReportGenerator:
    A4_PORTRAIT_WIDTH_MM = 210 # ... y otras constantes si las usas ...

    def __init__(self):
        print("ReportGenerator: Instancia creada.")
        self.styles = None
        if REPORTLAB_AVAILABLE:
            try:
                self.styles = getSampleStyleSheet()
                self.styles.add(ParagraphStyle(name='GenerationDate', parent=self.styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_RIGHT, spaceBefore=1*mm, spaceAfter=4*mm))
                self.styles.add(ParagraphStyle(name='ReportTitle', parent=self.styles['h1'], fontSize=16, leading=18, alignment=TA_CENTER, spaceAfter=6*mm, textColor=colors.HexColor("#003366")))
                self.styles.add(ParagraphStyle(name='TableContent', parent=self.styles['Normal'], fontSize=7.5, leading=9, alignment=TA_LEFT))
                self.styles.add(ParagraphStyle(name='TableContentCenter', parent=self.styles['TableContent'], alignment=TA_CENTER))
                self.styles.add(ParagraphStyle(name='QRItemTitle', parent=self.styles['Normal'], fontSize=8, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=0.5*mm, textColor=colors.HexColor("#003366")))
                self.styles.add(ParagraphStyle(name='QRItemDetail', parent=self.styles['Normal'], fontSize=6.5, leading=8, alignment=TA_CENTER, spaceBefore=0.5*mm, textColor=colors.darkgrey))
                print("  ReportGenerator: Estilos de ReportLab inicializados correctamente.")
            except Exception as e_styles:
                print(f"!!! EXCEPCIÓN al inicializar estilos de ReportLab: {e_styles}")
                traceback.print_exc()
                self.styles = None
        else:
            print("  ReportGenerator: ReportLab no está disponible, self.styles será None.")

    def _safe_str(self, value, default='N/A'):
        if value is None:
            return default
        s_value = str(value).strip()
        return s_value if s_value else default

    def _get_output_path(self, report_name_suffix):
        try:
            timestamp = QDateTime.currentDateTime().toString("yyyyMMdd_HHmmss")
            filename = f"inventario_{report_name_suffix}_{timestamp}.pdf"
            download_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
            if not download_dir or not os.path.isdir(download_dir):
                download_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
            if not download_dir or not os.path.isdir(download_dir):
                download_dir = os.path.abspath(".")
            os.makedirs(download_dir, exist_ok=True)
            destination_path = os.path.normpath(os.path.join(download_dir, filename))
            return destination_path, download_dir
        except Exception as e:
            print(f"Error en _get_output_path: {e}")
            return None, None

    def _create_qr_image_flowable(self, content_str, size_in_cm):
        if not QRCODE_AVAILABLE or not qrcode: return None
        try:
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2)
            qr.add_data(content_str)
            qr.make(fit=True)
            img_pil = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img_pil.save(buffer, format="PNG")
            buffer.seek(0)
            return Image(buffer, width=size_in_cm, height=size_in_cm)
        except Exception as e:
            print(f"Error al crear imagen QR (contenido '{content_str[:30]}...'): {e}")
            return None

    def generate_table_report(self, equipment_list):
        print(f"ReportGenerator: Iniciando generate_table_report para {len(equipment_list)} equipos.")
        if not REPORTLAB_AVAILABLE or self.styles is None:
            return {'success': False, 'message': 'Error: Componente PDF o sus estilos no están disponibles.'}
        if not equipment_list:
            return {'success': False, 'message': 'No hay datos para generar el reporte de tabla.'}

        destination_path, download_dir = self._get_output_path('tabla_inventario')
        if not destination_path:
            return {'success': False, 'message': 'No se pudo determinar la ruta para guardar el archivo.'}

        try:
            # --- AJUSTE DE MÁRGENES AQUÍ ---
            # 3 cm es bastante, pero si eso es lo que necesitas:
            custom_left_margin = 2 * cm
            custom_right_margin = 2 * cm
            custom_top_margin = 1.5 * cm  # Puedes ajustar estos también si quieres
            custom_bottom_margin = 1.5 * cm

            doc = SimpleDocTemplate(destination_path, pagesize=landscape(A4),
                                    leftMargin=custom_left_margin, 
                                    rightMargin=custom_right_margin,
                                    topMargin=custom_top_margin, 
                                    bottomMargin=custom_bottom_margin)
            # --- FIN AJUSTE DE MÁRGENES ---

            story = [Paragraph("Reporte de Inventario de Equipos", self.styles['ReportTitle']),
                     Paragraph(f"Generado: {QDateTime.currentDateTime().toString('dd/MM/yyyy HH:mm:ss')}", self.styles['GenerationDate']),
                     Spacer(1, 0.4*cm)]
            
            # Encabezados y claves (como los tenías, sin campos de mantenimiento)
            headers = ['N°', 'Tipo', 'Marca', 'Modelo', 'Serial', 'Asignado', 'Dpto.', 'Sede', 'Estatus']
            keys_in_data = ['tipo_equipo', 'marca', 'modelo', 'serial', 'asignado_a', 'departamento', 'sede', 'estatus']
            
            table_data = [headers]
            for idx, eq_data in enumerate(equipment_list):
                row_content = [Paragraph(str(idx + 1), self.styles['TableContentCenter'])]
                for key in keys_in_data:
                    value = self._safe_str(eq_data.get(key))
                    # No necesitas formatear fechas aquí si ya no están
                    row_content.append(Paragraph(value, self.styles['TableContent']))
                table_data.append(row_content)

            # Anchos de Columna para 9 columnas
            # Ancho útil A4 Landscape (29.7cm) - (3cm + 3cm de márgenes) = 23.7cm
            # Debes recalcular estos anchos para que quepan en el nuevo espacio útil.
            # Ejemplo (necesitarás ajustar estos valores con precisión):
            # N°     Tipo   Marca  Modelo Serial Asignado Dpto. Sede   Estatus
            # 1.0cm  3.0cm  3.0cm  3.5cm  3.5cm  3.5cm    3.0cm 3.0cm  2.0cm  = 25.5cm (AÚN MUY ANCHO para 23.7cm)
            
            # Intentemos con anchos más pequeños:
            # N°     Tipo   Marca  Modelo Serial Asignado Dpto. Sede   Estatus
            # 0.8cm  2.8cm  2.8cm  3.0cm  3.0cm  3.0cm    2.8cm 2.8cm  2.0cm  = 23.0cm (Esto debería caber)

            col_widths = [0.8*cm, 2.8*cm, 3.8*cm, 4.0*cm, 4.0*cm, 4.0*cm, 2.8*cm, 2.8*cm, 2.0*cm] 
            print(f"  Ancho de página útil con márgenes de 3cm: {doc.width/cm:.2f} cm") # doc.width ya considera los márgenes
            print(f"  Suma de anchos de columna propuestos: {sum(col_widths)/cm:.2f} cm")


            pdf_table = Table(table_data, colWidths=col_widths, repeatRows=1)
            pdf_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,0), 'CENTER'), 
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 7), # Reducir un poco la fuente del encabezado si es necesario
                ('BOTTOMPADDING', (0,0), (-1,0), 2.5*mm), # Ajustar padding
                ('TOPPADDING', (0,0), (-1,0), 2*mm),   # Ajustar padding
                ('GRID', (0,0), (-1,-1), 0.5, colors.darkgrey),
                ('ALIGN', (0,1), (0,-1), 'CENTER'), 
                ('ALIGN', (8,1), (8,-1), 'CENTER'), # Estatus centrado (columna 9, índice 8)
            ]))
            story.append(pdf_table)
            
            doc.build(story)
            print(f"  ReportGenerator: PDF tabla generado: {destination_path}")
            return {'success': True, 'message': f'Reporte de tabla generado en:\n{download_dir}', 'filepath': destination_path}

        except Exception as e:
            print(f"!!! Error EXCEPCIÓN generando PDF Tabla: {e}"); traceback.print_exc()
            return {'success': False, 'message': f'Error al generar PDF de Tabla: {e}'}
        
    def generate_qr_report(self, equipment_list):
        print(f"ReportGenerator: Iniciando generate_qr_report para {len(equipment_list)} equipos.")
        if not REPORTLAB_AVAILABLE or not QRCODE_AVAILABLE or self.styles is None:
            missing = []
            if not REPORTLAB_AVAILABLE: missing.append("ReportLab")
            if not QRCODE_AVAILABLE: missing.append("qrcode/Pillow")
            if self.styles is None: missing.append("Estilos de ReportLab (fallo inicialización)")
            return {'success': False, 'message': f'Error: Dependencia(s) faltante(s): {", ".join(missing)}.'}
        if not equipment_list:
            return {'success': False, 'message': 'No hay equipos para generar QRs.'}

        destination_path, download_dir = self._get_output_path('qrs_equipos_basico') # Nombre de archivo diferente
        if not destination_path:
            return {'success': False, 'message': 'No se pudo determinar la ruta de guardado.'}

        try:
            doc = SimpleDocTemplate(destination_path, pagesize=portrait(A4), leftMargin=1*cm, rightMargin=1*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
            story = [Paragraph("Reporte de Códigos QR de Equipos", self.styles['ReportTitle']),
                     Paragraph(f"Generado: {QDateTime.currentDateTime().toString('dd/MM/yyyy HH:mm:ss')}", self.styles['GenerationDate']),
                     Spacer(1, 0.5*cm)]

            qr_img_display_size = 2.8 * cm
            qrs_per_row = 3
            available_page_width = doc.width
            cell_width = available_page_width / qrs_per_row
            col_widths_for_qr_table = [cell_width] * qrs_per_row
            qr_data_for_table = []
            current_qr_row_cells = []

            for i, equipo_data in enumerate(equipment_list):
                # --- Contenido para el CÓDIGO QR (SIN MANTENIMIENTOS NI OBSERVACIÓN) ---
                qr_content_lines = [
                    f"ID: {self._safe_str(equipo_data.get('id'))}",
                    f"Tipo: {self._safe_str(equipo_data.get('tipo_equipo'))}",
                    f"Marca: {self._safe_str(equipo_data.get('marca'))}",
                    f"Modelo: {self._safe_str(equipo_data.get('modelo'))}",
                    f"Serial: {self._safe_str(equipo_data.get('serial'))}",
                    f"Asignado: {self._safe_str(equipo_data.get('asignado_a'))}",
                    f"Depto: {self._safe_str(equipo_data.get('departamento'))}",
                    f"Sede: {self._safe_str(equipo_data.get('sede'))}",
                    f"Estatus: {self._safe_str(equipo_data.get('estatus'))}",
                    f"Registro: {self._safe_str(equipo_data.get('fecha_registro'))}"
                ]
                qr_data_string = "\n".join(line for line in qr_content_lines if line.split(": ",1)[-1].strip() and line.split(": ",1)[-1].strip() != 'N/A')
                # --------------------------------------------------------------------

                qr_image_flowable = self._create_qr_image_flowable(qr_data_string, qr_img_display_size)
                cell_content_flowables = []
                if qr_image_flowable:
                    cell_content_flowables.append(qr_image_flowable)
                    cell_content_flowables.append(Spacer(1, 1.5*mm))
                    visible_text_title = Paragraph(f"<b>{self._safe_str(equipo_data.get('tipo_equipo'))}</b>", self.styles['QRItemTitle'])
                    visible_text_details = (f"ID: {self._safe_str(equipo_data.get('id'))}<br/>"
                                            f"S/N: {self._safe_str(equipo_data.get('serial'))}<br/>"
                                            f"Sede: {self._safe_str(equipo_data.get('sede'))}<br/>"
                                            f"Asignado: {self._safe_str(equipo_data.get('asignado_a'))}")
                    visible_text_para = Paragraph(visible_text_details, self.styles['QRItemDetail'])
                    cell_content_flowables.extend([visible_text_title, visible_text_para])
                else:
                    error_para = Paragraph(f"Error QR<br/>ID: {self._safe_str(equipo_data.get('id'))}<br/>S/N: {self._safe_str(equipo_data.get('serial'))}", self.styles['QRItemDetail'])
                    cell_content_flowables.append(error_para)
                current_qr_row_cells.append(cell_content_flowables)

                if len(current_qr_row_cells) == qrs_per_row:
                    qr_data_for_table.append(current_qr_row_cells)
                    current_qr_row_cells = []
            
            if current_qr_row_cells:
                while len(current_qr_row_cells) < qrs_per_row:
                    current_qr_row_cells.append(Paragraph("", self.styles['Normal']))
                qr_data_for_table.append(current_qr_row_cells)

            if qr_data_for_table:
                qr_layout_table = Table(qr_data_for_table, colWidths=col_widths_for_qr_table)
                qr_layout_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'), ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('LEFTPADDING', (0,0), (-1,-1), 1*mm), ('RIGHTPADDING', (0,0), (-1,-1), 1*mm),
                    ('TOPPADDING', (0,0), (-1,-1), 1*mm), ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm),
                ]))
                story.append(qr_layout_table)
            else:
                story.append(Paragraph("No se pudieron generar códigos QR.", self.styles['Normal']))
            
            doc.build(story)
            return {'success': True, 'message': f'Reporte QR generado en:\n{download_dir}', 'filepath': destination_path}
        except Exception as e:
            print(f"!!! Error EXCEPCIÓN generando PDF de QRs: {e}"); traceback.print_exc()
            return {'success': False, 'message': f'Error crítico al generar el PDF de QRs: {e}'}