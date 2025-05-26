# report_generator.py
import os
import traceback
import html
from datetime import datetime
import io # Para generar QR en memoria

# --- Dependencias Externas ---
try:
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
    # Importaciones necesarias para estilos
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib.units import cm, mm
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape, portrait # Usar directamente los tamaños
    REPORTLAB_AVAILABLE = True
except ImportError:
    print("¡¡¡ADVERTENCIA!!! ReportLab no está instalado. La exportación a PDF no funcionará.")
    REPORTLAB_AVAILABLE = False
    # Definir stubs para evitar NameError si ReportLab no está disponible
    SimpleDocTemplate=Table=TableStyle=Paragraph=Spacer=Image=PageBreak=None
    getSampleStyleSheet=ParagraphStyle=None; TA_CENTER=TA_LEFT=TA_RIGHT=1; cm=28.3; mm=2.83; colors=None
    A4=landscape=portrait=None

try:
    import qrcode
    # No es necesario importar PILImage explícitamente si qrcode lo usa internamente para make_image
    QRCODE_AVAILABLE = True
except ImportError:
    print("¡¡¡ADVERTENCIA!!! qrcode o Pillow no están instalados. La exportación de QR no funcionará.")
    QRCODE_AVAILABLE = False
    qrcode = None
# ---------------------------

# --- Importar desde PySide2 ---
from PySide2.QtCore import QStandardPaths, QDateTime

class ReportGenerator:
    """Genera reportes PDF (Tablas y QR) usando ReportLab."""

    def __init__(self):
        print("ReportGenerator: Instancia creada.")
        if REPORTLAB_AVAILABLE:
            self.styles = getSampleStyleSheet()

            # --- CORRECCIÓN DE ESTILOS PERSONALIZADOS ---
            # Estilo para la fecha de generación del reporte
            self.styles.add(ParagraphStyle(name='GenerationDate', parent=self.styles['Normal']))
            self.styles['GenerationDate'].fontSize = 8
            self.styles['GenerationDate'].textColor = colors.grey
            self.styles['GenerationDate'].alignment = TA_RIGHT
            self.styles['GenerationDate'].spaceAfter = 2*mm # Espacio después de este párrafo

            # Estilo para el título principal del reporte
            self.styles.add(ParagraphStyle(name='ReportTitle', parent=self.styles['h1'])) # Usar 'h1' como base
            self.styles['ReportTitle'].fontSize = 16
            self.styles['ReportTitle'].leading = 18 # Espaciado entre líneas
            self.styles['ReportTitle'].alignment = TA_CENTER
            self.styles['ReportTitle'].spaceAfter = 8*mm # Espacio después del título

            # Estilo para el contenido de las celdas de la tabla
            self.styles.add(ParagraphStyle(name='TableContent', parent=self.styles['Normal']))
            self.styles['TableContent'].fontSize = 7
            self.styles['TableContent'].leading = 8 # Espaciado entre líneas en caso de wrap de texto
            self.styles['TableContent'].spaceAfter = 0*mm # Sin espacio extra entre párrafos en la tabla
            self.styles['TableContent'].alignment = TA_LEFT # Por defecto alineado a la izquierda

            # Estilo para el contenido de las celdas de la tabla (centrado)
            self.styles.add(ParagraphStyle(name='TableContentCenter', parent=self.styles['TableContent'])) # Basado en TableContent
            self.styles['TableContentCenter'].alignment = TA_CENTER

            # --- Estilos específicos para el reporte QR ---
            self.styles.add(ParagraphStyle(name='QRTitle', parent=self.styles['Normal']))
            self.styles['QRTitle'].fontSize = 8
            self.styles['QRTitle'].leading = 9
            self.styles['QRTitle'].alignment = TA_CENTER
            self.styles['QRTitle'].spaceAfter = 1*mm
            self.styles['QRTitle'].fontName = 'Helvetica-Bold'

            self.styles.add(ParagraphStyle(name='QRInfo', parent=self.styles['Normal']))
            self.styles['QRInfo'].fontSize = 6.5
            self.styles['QRInfo'].leading = 7.5
            self.styles['QRInfo'].alignment = TA_CENTER
            self.styles['QRInfo'].spaceAfter = 0*mm
            # --- FIN CORRECCIÓN DE ESTILOS ---

        else:
            self.styles = None # Asegurar que es None si ReportLab no está

    def _safe_str(self, value, default=''):
        """Convierte a string seguro."""
        return str(value) if value is not None else default

    def _get_output_path(self, format_type):
        """Determina la ruta de salida del archivo PDF en Descargas o Documentos."""
        try:
            timestamp = QDateTime.currentDateTime().toString("yyyyMMdd_HHmmss")
            filename = f"inventario_{format_type}_{timestamp}.pdf"

            download_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
            if not download_dir or not os.path.isdir(download_dir):
                print(f"  Advertencia: Carpeta de Descargas no accesible, usando Documents.")
                download_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
                if not download_dir or not os.path.isdir(download_dir):
                    print(f"  Advertencia: Carpeta de Documents no accesible, usando directorio de la app.")
                    download_dir = os.path.abspath(".") # Directorio actual como último recurso

            os.makedirs(download_dir, exist_ok=True)
            destination_path = os.path.normpath(os.path.join(download_dir, filename))
            print(f"  ReportGenerator: Ruta destino PDF: {destination_path}")
            return destination_path, download_dir
        except Exception as e:
            print(f"!!! Error determinando ruta de guardado: {e}")
            traceback.print_exc()
            return None, None

    def generate_table_report(self, data):
        print("ReportGenerator: Iniciando generate_table_report...")
        if not REPORTLAB_AVAILABLE or not self.styles:
            return {'success': False, 'message': 'Error: ReportLab o estilos no están disponibles.'}
        if not data:
            return {'success': False, 'message': 'No hay datos para generar el reporte de tabla.'}

        destination_path, download_dir = self._get_output_path('tabla_inventario')
        if not destination_path:
            return {'success': False, 'message': 'Generación de PDF de tabla cancelada por el usuario.'}

        try:
            doc = SimpleDocTemplate(destination_path, pagesize=landscape(A4),
                                    leftMargin=1*cm, rightMargin=1*cm,
                                    topMargin=1.5*cm, bottomMargin=1.5*cm)
            story = []

            # Encabezado del reporte
            story.append(Paragraph("Reporte de Inventario de Equipos", self.styles['ReportTitle']))
            story.append(Paragraph(f"Generado: {QDateTime.currentDateTime().toString('dd/MM/yyyy HH:mm')}", self.styles['GenerationDate']))
            story.append(Spacer(1, 0.5*cm)) # Espacio después de la fecha

            # Encabezados de la tabla (AÑADIR 'Sede')
            headers = ['N°', 'Tipo', 'Marca', 'Modelo', 'Serial', 'Asignado a', 'Departamento', 'Sede', 'Estatus']
            # Claves en tus objetos 'eq' que corresponden a los headers
            keys_in_data = ['tipo_equipo', 'marca', 'modelo', 'serial', 'asignado_a', 'departamento', 'sede', 'estatus']

            table_data = [headers]
            for idx, eq in enumerate(data):
                row_data = [Paragraph(str(idx + 1), self.styles['TableContentCenter'])] # N° centrado
                for key in keys_in_data:
                    # Usar self.styles['TableContent'] para el texto normal
                    row_data.append(Paragraph(self._safe_str(eq.get(key, '')), self.styles['TableContent']))
                table_data.append(row_data)

            # Anchos de Columna para A4 Landscape (aprox. 27.7cm disponibles)
            # Total 9 columnas (N° + 8 campos)
            col_widths = [1*cm, 3.5*cm, 3.5*cm, 3.5*cm, 4*cm, 3.5*cm, 3.5*cm, 3.5*cm, 2.7*cm] # Total aprox. 28.7cm
            
            current_total_width = sum(col_widths)
            available_width = doc.width
            print(f"  Ancho total de columnas propuesto: {current_total_width:.2f} cm")
            print(f"  Ancho disponible en página: {available_width:.2f} cm")

            if current_total_width > available_width:
                scale_factor = available_width / current_total_width
                col_widths = [w * scale_factor for w in col_widths]
                print(f"  Anchos escalados a: {[f'{w:.2f}cm' for w in col_widths]}")
            else:
                print("  Anchos de columna no necesitan escalado.")

            pdf_table = Table(table_data, colWidths=col_widths, repeatRows=1)
            pdf_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#000080')), # Azul oscuro para header
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,0), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 8),
                ('BOTTOMPADDING', (0,0), (-1,0), 4*mm),
                ('TOPPADDING', (0,0), (-1,0), 3*mm),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                # El tamaño de fuente para los datos ya está en el estilo TableContent
                ('ALIGN', (0,1), (0,-1), 'CENTER'), # N° centrado
            ]))
            story.append(pdf_table)

            doc.build(story)
            print(f"  ReportGenerator: PDF tabla generado con éxito en: {destination_path}")
            return {'success': True, 
                            'message': f'Reporte de tabla generado en: \n{download_dir}',
                            'filepath': destination_path}

        except Exception as e:
            print(f"!!! Error generando PDF Tabla: {e}"); traceback.print_exc()
            return {'success': False, 'message': f'Error al generar PDF de Tabla: {e}'}

    def generate_qr_report(self, data): # 'data' es equipment_data_list
        print("ReportGenerator: Iniciando generate_qr_report...")
        if not REPORTLAB_AVAILABLE or not QRCODE_AVAILABLE:
            missing = []
            if not REPORTLAB_AVAILABLE: missing.append("ReportLab")
            if not QRCODE_AVAILABLE: missing.append("qrcode/Pillow")
            return {'success': False, 'message': f'Error: Falta(n) librería(s) esencial(es): {", ".join(missing)}.'}
        if not self.styles:
             return {'success': False, 'message': 'Error: Estilos de ReportLab no disponibles.'}
        if not data:
            return {'success': False, 'message': 'No hay datos para generar el reporte QR.'}

        destination_path, download_dir = self._get_output_path('qr_detallado')
        if not destination_path:
            return {'success': False, 'message': 'Generación de PDF QR cancelada por el usuario.'}

        try:
            doc = SimpleDocTemplate(destination_path, pagesize=portrait(A4),
                                    leftMargin=1*cm, rightMargin=1*cm,
                                    topMargin=1*cm, bottomMargin=1*cm)
            story = []

            # --- Configuración Cuadrícula ---
            qr_img_size_pdf = 3.0 * cm
            cell_padding = 0.2 * cm
            cell_width = 4.5 * cm

            cols = int((doc.width - 2 * cell_padding) / cell_width)
            print(f"  ReportGenerator QR: Calculadas {cols} columnas para ancho de celda {cell_width}.")
            if cols == 0: cols = 1

            col_widths_qr = [cell_width] * cols

            qr_data_grid = []
            current_row_cells = []

            print(f"  ReportGenerator QR: Generando {len(data)} códigos QR...")
            for i, item in enumerate(data):
                tipo_equipo = self._safe_str(item.get('tipo_equipo'), 'N/A')
                serial_val = self._safe_str(item.get('serial'), 'N/A')
                sede_val = self._safe_str(item.get('sede'), 'N/A') # <--- Obtener la sede
                asignado_val = self._safe_str(item.get('asignado_a'), 'N/A')
                item_id_for_qr = self._safe_str(item.get('id'), 'NO_ID')

                # --- TEXTO PARA EL CÓDIGO QR ---
                qr_content_str = (
                    f"ID_Interno:{item_id_for_qr}\n"
                    f"Tipo:{tipo_equipo}\n"
                    f"Serial:{serial_val}\n"
                    f"Sede:{sede_val}\n" # <--- Añadir Sede al contenido QR
                    f"Asignado:{asignado_val}"
                )
                
                qr_img_flowable = self._create_qr_image_flowable(qr_content_str, qr_img_size_pdf)
                
                if not qr_img_flowable:
                    error_text = Paragraph(f"Error QR<br/>S/N: {serial_val}", self.styles['QRInfo']) # Usar estilo QRInfo
                    current_row_cells.append(error_text)
                else:
                    # --- TEXTO VISIBLE DEBAJO DEL QR ---
                    p_tipo_equipo = Paragraph(tipo_equipo, self.styles['QRTitle'])
                    
                    details_text = (
                        f"Serial: {serial_val}<br/>"
                        f"Sede: {sede_val}<br/>" # <--- Añadir Sede al texto visible
                        f"Asignado: {asignado_val}"
                    )
                    p_details = Paragraph(details_text, self.styles['QRInfo']) # Usar estilo QRInfo

                    cell_elements = [
                        p_tipo_equipo,
                        Spacer(1, 1*mm),
                        qr_img_flowable,
                        Spacer(1, 1*mm),
                        p_details
                    ]
                    current_row_cells.append(cell_elements)

                if len(current_row_cells) == cols:
                    qr_data_grid.append(current_row_cells)
                    current_row_cells = []

            if current_row_cells:
                while len(current_row_cells) < cols:
                    current_row_cells.append(Spacer(0,0))
                qr_data_grid.append(current_row_cells)

            print(f"  ReportGenerator QR: Cuadrícula con {len(qr_data_grid)} filas.")

            if qr_data_grid:
                qr_table = Table(qr_data_grid, colWidths=col_widths_qr)
                qr_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('LEFTPADDING', (0,0), (-1,-1), cell_padding),
                    ('RIGHTPADDING', (0,0), (-1,-1), cell_padding),
                    ('TOPPADDING', (0,0), (-1,-1), cell_padding),
                    ('BOTTOMPADDING', (0,0), (-1,-1), cell_padding + (0.2*cm)),
                ]))
                story.append(qr_table)
            else:
                story.append(Paragraph("No se generaron códigos QR (posiblemente no hay datos válidos).", self.styles['Normal']))

            report_title_qr = Paragraph("Reporte de Códigos QR de Equipos", self.styles['ReportTitle'])
            generation_date_qr = Paragraph(f"Generado: {QDateTime.currentDateTime().toString('dd/MM/yyyy HH:mm')}", self.styles['GenerationDate'])
            
            final_story = [report_title_qr, generation_date_qr] + story

            doc.build(final_story)
            print(f"  ReportGenerator QR: PDF QR detallado generado en: {destination_path}")
            return {'success': True, 'message': f'Reporte QR generado en: \n{download_dir}', 'filepath': destination_path}

        except Exception as e:
            print(f"!!! Error generando PDF QR detallado: {e}"); traceback.print_exc()
            return {'success': False, 'message': f'Error al generar el PDF de QR detallado: {e}'}

    def generate_qr_report(self, data): # 'data' es equipment_data_list
        print("ReportGenerator: Iniciando generate_qr_report...")
        if not REPORTLAB_AVAILABLE or not QRCODE_AVAILABLE:
            missing = []
            if not REPORTLAB_AVAILABLE: missing.append("ReportLab")
            if not QRCODE_AVAILABLE: missing.append("qrcode/Pillow") # qrcode usa Pillow internamente
            return {'success': False, 'message': f'Error: Falta(n) librería(s) esencial(es): {", ".join(missing)}.'}
        if not self.styles:
             return {'success': False, 'message': 'Error: Estilos de ReportLab no disponibles.'}
        if not data:
            return {'success': False, 'message': 'No hay datos para generar el reporte QR.'}

        destination_path, download_dir = self._get_output_path('qr_detallado') # Nombre de archivo diferente
        if not destination_path:
            return {'success': False, 'message': 'Error crítico: No se pudo determinar la ruta para guardar el archivo.'}

        try:
            doc = SimpleDocTemplate(destination_path, pagesize=portrait(A4),
                                    leftMargin=1*cm, rightMargin=1*cm,
                                    topMargin=1*cm, bottomMargin=1*cm)
            story = []

            # --- Configuración Cuadrícula ---
            # Ajusta estos valores para el diseño deseado
            qr_img_size_pdf = 3.0 * cm  # Tamaño de la imagen QR en el PDF
            cell_padding = 0.2 * cm     # Espacio alrededor del contenido dentro de una celda
            
            # Ancho total por celda: QR + texto + algo de margen.
            # La altura dependerá del texto, pero podemos fijar un mínimo o dejar que la tabla la ajuste.
            # Si el texto es variable, usar rowHeights='*' puede ser mejor, o calcularla.
            cell_width = 4.5 * cm  # Aumentar un poco para más texto
            # cell_height = 5.5 * cm # Aumentar para más líneas de texto

            cols = int((doc.width - 2 * cell_padding) / cell_width) # Columnas basadas en ancho útil
            print(f"  ReportGenerator QR: Calculadas {cols} columnas para ancho de celda {cell_width}.")
            if cols == 0: cols = 1

            col_widths_qr = [cell_width] * cols
            # -----------------------------

            qr_data_grid = []
            current_row_cells = []

            # Estilos para el texto debajo del QR (puedes definirlos en __init__ o aquí)
            style_qr_title = ParagraphStyle( # Para el "Tipo Equipo"
                'QRTitle',
                parent=self.styles['Normal'],
                fontSize=8, # Un poco más grande para el tipo
                leading=9,
                alignment=TA_CENTER,
                spaceAfter=1*mm,
                fontName='Helvetica-Bold'
            )
            style_qr_details = ParagraphStyle( # Para los otros detalles
                'QRInfo',
                parent=self.styles['Normal'],
                fontSize=6.5, # Pequeño para que quepa más
                leading=7.5,
                alignment=TA_CENTER, # Centrado debajo del QR
                spaceAfter=0 # Sin espacio extra después
            )


            print(f"  ReportGenerator QR: Generando {len(data)} códigos QR...")
            for i, item in enumerate(data):
                # Campos a mostrar
                tipo_equipo = self._safe_str(item.get('tipo_equipo'), 'N/A')
                serial_val = self._safe_str(item.get('serial'), 'N/A') # No usar S/N: si ya es el serial
                sede_val = self._safe_str(item.get('sede'), 'N/A')
                asignado_val = self._safe_str(item.get('asignado_a'), 'N/A')
                # ID para el QR interno (opcional, puedes quitarlo si no lo necesitas en el QR)
                item_id_for_qr = self._safe_str(item.get('id'), 'NO_ID')


                # --- TEXTO PARA EL CÓDIGO QR ---
                # Incluye lo que necesites escanear. Menos es mejor para la legibilidad del QR.
                qr_content_str = (
                    f"ID_Interno:{item_id_for_qr}\n" # Puedes mantener el ID aquí si es útil para el escaneo
                    f"Tipo:{tipo_equipo}\n"
                    f"Serial:{serial_val}\n"
                    f"Sede:{sede_val}\n"
                    f"Asignado:{asignado_val}"
                )
                
                qr_img_flowable = self._create_qr_image_flowable(qr_content_str, qr_img_size_pdf)
                
                if not qr_img_flowable:
                    # Añadir placeholder si falla la generación de QR para no romper la tabla
                    error_text = Paragraph(f"Error QR<br/>S/N: {serial_val}", style_qr_details)
                    current_row_cells.append(error_text)
                else:
                    # --- TEXTO VISIBLE DEBAJO DEL QR ---
                    # 1. Tipo de Equipo (como un título)
                    p_tipo_equipo = Paragraph(tipo_equipo, style_qr_title)
                    
                    # 2. Otros detalles
                    details_text = (
                        f"Serial: {serial_val}<br/>"
                        f"Sede: {sede_val}<br/>"
                        f"Asignado: {asignado_val}"
                    )
                    p_details = Paragraph(details_text, style_qr_details)

                    # Celda contendrá: Título, QR, Detalles
                    cell_elements = [
                        p_tipo_equipo,
                        Spacer(1, 1*mm), # Pequeño espacio
                        qr_img_flowable,
                        Spacer(1, 1*mm), # Pequeño espacio
                        p_details
                    ]
                    current_row_cells.append(cell_elements)

                # Lógica para completar filas y la cuadrícula
                if len(current_row_cells) == cols:
                    qr_data_grid.append(current_row_cells)
                    current_row_cells = []

            if current_row_cells: # Añadir última fila si no estaba completa
                while len(current_row_cells) < cols:
                    current_row_cells.append(Spacer(0,0)) # Celda vacía
                qr_data_grid.append(current_row_cells)

            print(f"  ReportGenerator QR: Cuadrícula con {len(qr_data_grid)} filas.")

            if qr_data_grid:
                # Podrías considerar no fijar rowHeights si el texto es muy variable,
                # o calcular una altura adecuada. Por ahora, la dejamos comentada.
                # qr_table = Table(qr_data_grid, colWidths=col_widths_qr, rowHeights=cell_height)
                qr_table = Table(qr_data_grid, colWidths=col_widths_qr)
                
                qr_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), # Alinear verticalmente al medio todo el contenido de la celda
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),  # Alinear horizontalmente al centro
                    ('LEFTPADDING', (0,0), (-1,-1), cell_padding),
                    ('RIGHTPADDING', (0,0), (-1,-1), cell_padding),
                    ('TOPPADDING', (0,0), (-1,-1), cell_padding),
                    ('BOTTOMPADDING', (0,0), (-1,-1), cell_padding + (0.2*cm)), # Un poco más de padding abajo
                    # ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey), # Descomentar para ver bordes de celda
                ]))
                story.append(qr_table)
            else:
                story.append(Paragraph("No se generaron códigos QR (posiblemente no hay datos válidos).", self.styles['Normal']))

            # Añadir título general al reporte QR
            report_title_qr = Paragraph("Reporte de Códigos QR de Equipos", self.styles['ReportTitle'])
            generation_date_qr = Paragraph(f"Generado: {QDateTime.currentDateTime().toString('dd/MM/yyyy HH:mm')}", self.styles['GenerationDate'])
            
            # Insertar título y fecha al principio de la historia
            final_story = [report_title_qr, generation_date_qr] + story


            print(f"  ReportGenerator QR: Construyendo PDF... ({len(final_story)} flowables)")
            doc.build(final_story) # Usar final_story
            print(f"  ReportGenerator QR: PDF QR detallado generado en: {destination_path}")
            return {'success': True, 'message': f'Reporte QR generado en: \n{download_dir}', 'filepath': destination_path}

        except Exception as e:
            print(f"!!! Error generando PDF QR detallado: {e}"); traceback.print_exc()
            return {'success': False, 'message': f'Error al generar el PDF de QR detallado: {e}'}


    def _create_qr_image_flowable(self, content, size_cm):
        """Genera una imagen QR y la devuelve como flowable Image de ReportLab."""
        if not QRCODE_AVAILABLE: return None
        try:
            qr_code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1) # Borde más pequeño
            qr_code.add_data(content)
            qr_code.make(fit=True)
            img_pil = qr_code.make_image(fill_color="black", back_color="white").convert('RGB')

            buffer = io.BytesIO()
            img_pil.save(buffer, format="PNG")
            buffer.seek(0) # Rebobinar el buffer

            # Crear flowable Image de ReportLab
            img_flowable = Image(buffer, width=size_cm, height=size_cm, kind='direct') # kind='direct' para BytesIO
            return img_flowable
        except Exception as e:
            print(f"Error al crear imagen QR para contenido '{content[:30]}...': {e}")
            return None