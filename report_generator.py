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
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY # Añadir TA_JUSTIFY
    from reportlab.lib.pagesizes import A4, landscape, portrait
    from reportlab.lib.utils import ImageReader
    REPORTLAB_AVAILABLE = True
except ImportError:
    print("¡¡¡ADVERTENCIA!!! ReportLab no está instalado. La exportación a PDF no funcionará.")
    REPORTLAB_AVAILABLE = False
    SimpleDocTemplate=Table=TableStyle=Paragraph=Spacer=Image=PageBreak=getSampleStyleSheet=ParagraphStyle=None
    TA_CENTER=TA_LEFT=TA_RIGHT=TA_JUSTIFY=1

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    print("¡¡¡ADVERTENCIA!!! qrcode o Pillow no están instalados. La exportación de QR no funcionará.")
    QRCODE_AVAILABLE = False
    qrcode = None

from PySide2.QtCore import QStandardPaths, QDateTime

class ReportGenerator:
    def __init__(self):
        print("ReportGenerator: Instancia creada.")
        self.styles = None
        if REPORTLAB_AVAILABLE:
            try:
                self.styles = getSampleStyleSheet()
                self.base_font_name = 'Helvetica'
                self.base_font_name_bold = 'Helvetica-Bold'

                # TÍTULO DEL DOCUMENTO (NOTA DE...)
                self.styles.add(ParagraphStyle(name='DocumentMainTitle', parent=self.styles['h1'],
                                               fontSize=14, leading=18, alignment=TA_CENTER,
                                               spaceAfter=8*mm, textColor=colors.black, # Color Negro
                                               fontName=self.base_font_name_bold,
                                               # Para subrayado, se usa en el Paragraph: <U>Texto</U>
                                               ))

                self.styles.add(ParagraphStyle(name='GenerationDate', fontSize=8, textColor=colors.grey, alignment=TA_RIGHT, spaceBefore=1*mm, spaceAfter=6*mm, fontName=self.base_font_name))
                
                self.styles.add(ParagraphStyle(name='DocumentFieldValue', parent=self.styles['Normal'], fontName=self.base_font_name, fontSize=10, leading=14, spaceAfter=2*mm))

                self.styles.add(ParagraphStyle(name='IntroText', parent=self.styles['Normal'], fontName=self.base_font_name, fontSize=10, leading=14, spaceBefore=4*mm, spaceAfter=4*mm, alignment=TA_LEFT))
                
                self.styles.add(ParagraphStyle(name='TableText', parent=self.styles['Normal'], fontName=self.base_font_name, fontSize=9, leading=11))
                self.styles.add(ParagraphStyle(name='TableHeaderText', parent=self.styles['TableText'], fontName=self.base_font_name_bold, alignment=TA_CENTER))

                # NOTA LEGAL EN NEGRITA
                self.styles.add(ParagraphStyle(name='LegalText', parent=self.styles['Normal'],
                                               fontName=self.base_font_name_bold, # NEGRITA
                                               fontSize=8.5, leading=11, alignment=TA_JUSTIFY,
                                               spaceBefore=6*mm, spaceAfter=6*mm))

                self.styles.add(ParagraphStyle(name='SignatureAttn', parent=self.styles['Normal'], fontName=self.base_font_name, fontSize=10, leading=12, spaceBefore=8*mm, spaceAfter=4*mm, alignment=TA_CENTER)) # Centrado

                # BLOQUE DE FIRMA CENTRADO Y EN NEGRITA
                self.styles.add(ParagraphStyle(name='SignatureBlock', parent=self.styles['Normal'],
                                               fontName=self.base_font_name_bold, # NEGRITA
                                               fontSize=9, leading=11, alignment=TA_CENTER))
                print("  ReportGenerator: Estilos de ReportLab inicializados.")
            except Exception as e_styles:
                print(f"!!! EXCEPCIÓN al inicializar estilos: {e_styles}"); traceback.print_exc(); self.styles = None
        else:
            print("  ReportGenerator: ReportLab no disponible.")

    def _safe_str(self, value, default=''): # Cambiado default a '' para que no aparezca "N/A" si se omite
        if value is None:
            return default
        s_value = str(value).strip()
        return s_value if s_value else default

    def _get_output_path(self, report_name_suffix):
        try:
            timestamp = QDateTime.currentDateTime().toString("yyyyMMdd_HHmmss")
            filename = f"documento_{report_name_suffix}_{timestamp}.pdf" # Nombre genérico
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

    def _draw_header_footer(self, canvas, doc, header_path, footer_path, is_first_page=True):
        canvas.saveState()
        page_width = doc.pagesize[0]
        page_height = doc.pagesize[1]

        draw_h_height = 0 
        if header_path and os.path.exists(header_path):
            try:
                img_obj = ImageReader(header_path)
                img_w, img_h = img_obj.getSize()
                aspect = img_h / float(img_w)
                
                available_header_width = doc.width 
                draw_width = available_header_width
                draw_h_height = draw_width * aspect
                
                x_pos_header = doc.leftMargin
                y_pos_header = page_height - draw_h_height - (1 * cm)

                canvas.drawImage(img_obj, x_pos_header, y_pos_header,
                                 width=draw_width, height=draw_h_height, 
                                 preserveAspectRatio=True, anchor='n', mask='auto')
            except Exception as e: 
                print(f"Error dibujando encabezado '{header_path}': {e}")
                draw_h_height = 0

        if footer_path and os.path.exists(footer_path):
            try:
                img_obj = ImageReader(footer_path)
                img_w, img_h = img_obj.getSize()
                aspect = img_h / float(img_w)
                available_footer_width = doc.width
                draw_width_f = available_footer_width
                draw_height_f = draw_width_f * aspect
                x_pos_footer = doc.leftMargin
                y_pos_footer = 1 * cm 
                canvas.drawImage(img_obj, x_pos_footer, y_pos_footer,
                                 width=draw_width_f, height=draw_height_f, 
                                 preserveAspectRatio=True, anchor='s', mask='auto')
            except Exception as e: 
                print(f"Error dibujando pie de página '{footer_path}': {e}")
        
        if is_first_page: 
            canvas.setFont(self.base_font_name, 9)
            canvas.setFillColor(colors.black)
            text_uso_interno = "USO INTERNO"
            text_width_ui = canvas.stringWidth(text_uso_interno, self.base_font_name, 9)
            
            x_pos_ui = page_width - doc.rightMargin - text_width_ui 
            
            if draw_h_height > 0:
                y_base_header_inferior = y_pos_header # y_pos_header es la Y del borde superior de la imagen
                margen_debajo_header_para_texto = 0.5 * cm
                altura_aprox_texto_ui = 0.3 * cm 
                y_pos_ui = y_base_header_inferior - margen_debajo_header_para_texto - altura_aprox_texto_ui
            else:
                y_pos_ui = page_height - (2.5 * cm) # Fallback si no hay header

            canvas.drawString(x_pos_ui, y_pos_ui, text_uso_interno)

        canvas.restoreState()

    def generate_table_report(self, equipment_list):
        # ... (código de generate_table_report como lo tenías) ...
        # Asegúrate que está correctamente indentado y funcional.
        # Por brevedad, asumo que esta función está completa y correcta.
        print(f"ReportGenerator: Iniciando generate_table_report para {len(equipment_list)} equipos.")
        if not REPORTLAB_AVAILABLE or self.styles is None: return {'success': False, 'message': 'Error: Componente PDF o sus estilos no están disponibles.'}
        if not equipment_list: return {'success': False, 'message': 'No hay datos para generar el reporte de tabla.'}
        destination_path, download_dir = self._get_output_path('tabla_inventario')
        if not destination_path: return {'success': False, 'message': 'No se pudo determinar la ruta para guardar el archivo.'}
        try:
            doc = SimpleDocTemplate(destination_path, pagesize=landscape(A4), leftMargin=0.8*cm, rightMargin=0.8*cm, topMargin=1.2*cm, bottomMargin=1.2*cm)
            story = [Paragraph("Reporte de Inventario de Equipos", self.styles['ReportTitle']),
                     Paragraph(f"Generado: {QDateTime.currentDateTime().toString('dd/MM/yyyy HH:mm:ss')}", self.styles['GenerationDate']),
                     Spacer(1, 0.4*cm)]
            headers = ['N°', 'Tipo', 'Marca', 'Modelo', 'Serial', 'Asignado', 'Dpto.', 'Sede', 'Estatus']
            keys_in_data = ['tipo_equipo', 'marca', 'modelo', 'serial', 'asignado_a', 'departamento', 'sede', 'estatus']
            table_data = [headers]
            for idx, eq_data in enumerate(equipment_list):
                row_content = [Paragraph(str(idx + 1), self.styles['TableContentCenter'])]
                for key in keys_in_data:
                    value = self._safe_str(eq_data.get(key))
                    row_content.append(Paragraph(value, self.styles['TableContent']))
                table_data.append(row_content)
            col_widths = [1.0*cm, 3.5*cm, 3.5*cm, 4.0*cm, 4.0*cm, 4.0*cm, 3.5*cm, 3.5*cm, 2.6*cm]
            pdf_table = Table(table_data, colWidths=col_widths, repeatRows=1)
            pdf_table.setStyle(TableStyle([ ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")), ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke), ('ALIGN', (0,0), (-1,0), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,0), 7.5), ('BOTTOMPADDING', (0,0), (-1,0), 3*mm), ('TOPPADDING', (0,0), (-1,0), 2.5*mm), ('GRID', (0,0), (-1,-1), 0.5, colors.darkgrey), ('ALIGN', (0,1), (0,-1), 'CENTER'), ('ALIGN', (8,1), (8,-1), 'CENTER'), ]))
            story.append(pdf_table)
            doc.build(story)
            return {'success': True, 'message': f'Reporte de tabla generado en:\n{download_dir}', 'filepath': destination_path}
        except Exception as e:
            print(f"!!! Error EXCEPCIÓN generando PDF Tabla: {e}"); traceback.print_exc()
            return {'success': False, 'message': f'Error al generar PDF de Tabla: {e}'}


    def generate_qr_report(self, equipment_list):
        # ... (código de generate_qr_report como lo tenías, SIN la duplicación) ...
        # Asegúrate que está correctamente indentado y funcional.
        # Por brevedad, asumo que esta función está completa y correcta.
        print(f"ReportGenerator: Iniciando generate_qr_report para {len(equipment_list)} equipos.")
        if not REPORTLAB_AVAILABLE or not QRCODE_AVAILABLE or self.styles is None: missing = []; #... (resto de tu chequeo de dependencias)
        if not equipment_list: return {'success': False, 'message': 'No hay equipos para generar QRs.'}
        destination_path, download_dir = self._get_output_path('qrs_equipos_basico')
        if not destination_path: return {'success': False, 'message': 'No se pudo determinar la ruta de guardado.'}
        try:
            doc = SimpleDocTemplate(destination_path, pagesize=portrait(A4), leftMargin=1*cm, rightMargin=1*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
            story = [Paragraph("Reporte de Códigos QR de Equipos", self.styles['ReportTitle']), Paragraph(f"Generado: {QDateTime.currentDateTime().toString('dd/MM/yyyy HH:mm:ss')}", self.styles['GenerationDate']), Spacer(1, 0.5*cm)]
            qr_img_display_size = 2.8 * cm; qrs_per_row = 3; cell_width = doc.width / qrs_per_row; col_widths_for_qr_table = [cell_width] * qrs_per_row
            qr_data_for_table = []; current_qr_row_cells = []
            for i, equipo_data in enumerate(equipment_list):
                observacion_valor = equipo_data.get('observacion'); observacion_para_qr = "";
                if observacion_valor is not None: observacion_para_qr = self._safe_str(str(observacion_valor)[:40], '')
                qr_content_lines = [ f"ID: {self._safe_str(equipo_data.get('id'))}", f"Tipo: {self._safe_str(equipo_data.get('tipo_equipo'))}", f"Marca: {self._safe_str(equipo_data.get('marca'))}", f"Modelo: {self._safe_str(equipo_data.get('modelo'))}", f"Serial: {self._safe_str(equipo_data.get('serial'))}", f"Asignado: {self._safe_str(equipo_data.get('asignado_a'))}", f"Depto: {self._safe_str(equipo_data.get('departamento'))}", f"Sede: {self._safe_str(equipo_data.get('sede'))}", f"Estatus: {self._safe_str(equipo_data.get('estatus'))}", f"Registro: {self._safe_str(equipo_data.get('fecha_registro'))}" ]
                qr_data_string = "\n".join(line for line in qr_content_lines if line.split(": ",1)[-1].strip() and line.split(": ",1)[-1].strip() != 'N/A')
                qr_image_flowable = self._create_qr_image_flowable(qr_data_string, qr_img_display_size)
                cell_content_flowables = []
                if qr_image_flowable:
                    cell_content_flowables.append(qr_image_flowable); cell_content_flowables.append(Spacer(1, 1.5*mm))
                    visible_text_title = Paragraph(f"<b>{self._safe_str(equipo_data.get('tipo_equipo'))}</b>", self.styles['QRItemTitle'])
                    visible_text_details = (f"ID: {self._safe_str(equipo_data.get('id'))}<br/>S/N: {self._safe_str(equipo_data.get('serial'))}<br/>Sede: {self._safe_str(equipo_data.get('sede'))}")
                    visible_text_para = Paragraph(visible_text_details, self.styles['QRItemDetail'])
                    cell_content_flowables.extend([visible_text_title, visible_text_para])
                else: cell_content_flowables.append(Paragraph(f"Error QR<br/>ID: {self._safe_str(equipo_data.get('id'))}<br/>S/N: {self._safe_str(equipo_data.get('serial'))}", self.styles['QRItemDetail']))
                current_qr_row_cells.append(cell_content_flowables)
                if len(current_qr_row_cells) == qrs_per_row: qr_data_for_table.append(current_qr_row_cells); current_qr_row_cells = []
            if current_qr_row_cells:
                while len(current_qr_row_cells) < qrs_per_row: current_qr_row_cells.append(Paragraph("", self.styles['Normal']))
                qr_data_for_table.append(current_qr_row_cells)
            if qr_data_for_table:
                qr_layout_table = Table(qr_data_for_table, colWidths=col_widths_for_qr_table)
                qr_layout_table.setStyle(TableStyle([ ('VALIGN', (0,0), (-1,-1), 'TOP'), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('LEFTPADDING', (0,0), (-1,-1), 1*mm), ('RIGHTPADDING', (0,0), (-1,-1), 1*mm), ('TOPPADDING', (0,0), (-1,-1), 1*mm), ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm), ]))
                story.append(qr_layout_table)
            else: story.append(Paragraph("No se pudieron generar códigos QR.", self.styles['Normal']))
            doc.build(story)
            return {'success': True, 'message': f'Reporte QR generado en:\n{download_dir}', 'filepath': destination_path}
        except Exception as e:
            print(f"!!! Error EXCEPCIÓN generando PDF de QRs: {e}"); traceback.print_exc()
            return {'success': False, 'message': f'Error crítico al generar el PDF de QRs: {e}'}

    # --- generate_custom_document DEBE ESTAR AQUÍ, AL MISMO NIVEL DE INDENTACIÓN ---
    def generate_custom_document(self, document_type, form_data, equipment_data, header_image_path, footer_image_path):
        print(f"ReportGenerator: Generando documento tipo '{document_type}'")
        if not REPORTLAB_AVAILABLE or self.styles is None:
            return {'success': False, 'message': 'Componente PDF o estilos no disponibles.'}

        doc_type_slug = document_type.lower().replace(" ", "_").replace("ó", "o").replace("ñ", "n")
        numero_doc_completo = self._safe_str(form_data.get('numero_documento'), '').replace("N/A", "").strip()
        
        # TÍTULO DEL DOCUMENTO: NEGRO Y SUBRAYADO
        # El subrayado se hace con la etiqueta <U> de ReportLab
        document_title_text_content = f"{document_type.upper()}"
        if numero_doc_completo:
            document_title_text_content += f" {numero_doc_completo}"
        document_title_para = Paragraph(f"<u>{document_title_text_content}</u>", self.styles['DocumentMainTitle'])

        destination_path, download_dir = self._get_output_path(f"{doc_type_slug}_{form_data.get('numero_documento_editable','doc')}")
        if not destination_path:
            return {'success': False, 'message': 'No se pudo determinar la ruta para guardar.'}

        try:
            doc_left_margin = 3*cm
            doc_right_margin = 3*cm
            doc_top_margin = 3.5*cm # Espacio para que _draw_header_footer dibuje header.png
            doc_bottom_margin = 3.0*cm # Espacio para que _draw_header_footer dibuje footer.jpg

            doc = SimpleDocTemplate(destination_path, pagesize=portrait(A4),
                                    leftMargin=doc_left_margin, rightMargin=doc_right_margin,
                                    topMargin=doc_top_margin, bottomMargin=doc_bottom_margin)
            story = [document_title_para] # Título primero
            # No añadir Spacer aquí, el estilo ReportMainTitle y GenerationDate tienen spaceAfter

            # --- Metadatos: PARA, DE, ASUNTO, FECHA (CON NEGRITAS EN ETIQUETAS) ---
            meta_data_flowables = []
            para_val = self._safe_str(form_data.get('para'), '')
            de_val = self._safe_str(form_data.get('de_parte'), '')
            asunto_val = self._safe_str(form_data.get('asunto'), '')
            fecha_input = self._safe_str(form_data.get('fecha'), '')
            fecha_display = datetime.now().strftime('%d/%m/%Y')
            if fecha_input:
                try: fecha_display = datetime.strptime(fecha_input, '%Y-%m-%d').strftime('%d/%m/%Y')
                except ValueError: fecha_display = fecha_input
            
            # Usando formato enriquecido de Paragraph para negritas
            meta_data_flowables.append(Paragraph(f"<font name='{self.base_font_name_bold}'>PARA:</font> {para_val}", self.styles['DocumentFieldValue']))
            meta_data_flowables.append(Paragraph(f"<font name='{self.base_font_name_bold}'>DE:</font> {de_val}", self.styles['DocumentFieldValue']))
            meta_data_flowables.append(Paragraph(f"<font name='{self.base_font_name_bold}'>ASUNTO:</font> {asunto_val}", self.styles['DocumentFieldValue']))
            meta_data_flowables.append(Paragraph(f"<font name='{self.base_font_name_bold}'>FECHA:</font> {fecha_display}", self.styles['DocumentFieldValue']))
            
            story.extend(meta_data_flowables)
            story.append(Spacer(1, 0.6*cm))

            # --- Texto introductorio ---
            intro_text_map = { # ... (como lo tenías) ...
                "Nota de Retiro": "POR MEDIO DEL PRESENTE HACEMOS CONSTANCIA DEL RETIRO DEL EQUIPO(S), CON LAS SIGUIENTES CARACTERÍSTICAS:",
                "Acta de Entrega": "POR MEDIO DEL PRESENTE HACEMOS CONSTANCIA DE LA ENTREGA DEL EQUIPO(S), CON LAS SIGUIENTES CARACTERÍSTICAS:",
                "Constancia de Cambio": "POR MEDIO DEL PRESENTE HACEMOS CONSTANCIA DEL CAMBIO DE EQUIPO(S), SEGÚN LAS SIGUIENTES CARACTERÍSTICAS:",
                "Acta de Asignación": "POR MEDIO DEL PRESENTE HACEMOS CONSTANCIA DE LA ASIGNACIÓN DEL EQUIPO(S), CON LAS SIGUIENTES CARACTERÍSTICAS:"
            }
            intro_text = intro_text_map.get(document_type, "CON LAS SIGUIENTES CARACTERÍSTICAS:")
            story.append(Paragraph(intro_text, self.styles['IntroText']))

            # --- Tabla de Equipos (Fuente Base, sin colores de fondo) ---
            headers_equipos_str = ['Ítem', 'TIPO DE EQUIPO', 'SERIAL', 'MARCA', 'MODELO']
            headers_equipos_para = [Paragraph(h, self.styles['TableHeaderText']) for h in headers_equipos_str]
            data_equipos_tabla = [headers_equipos_para]

            for idx, eq in enumerate(equipment_data):
                row = [ Paragraph(str(idx + 1), self.styles['TableText']), # Ítem centrado por estilo TableContentCenter si lo usas
                        Paragraph(self._safe_str(eq.get('tipo_equipo')), self.styles['TableText']),
                        Paragraph(self._safe_str(eq.get('serial')), self.styles['TableText']),
                        Paragraph(self._safe_str(eq.get('marca')), self.styles['TableText']),
                        Paragraph(self._safe_str(eq.get('modelo')), self.styles['TableText']),]
                data_equipos_tabla.append(row)
            
            col_widths_equipos = [1.5*cm, 3.5*cm, 3.5*cm, 3.0*cm, 3.5*cm] # Ajustar para que sumen <= 15cm (ancho útil)
            
            equipos_table = Table(data_equipos_tabla, colWidths=col_widths_equipos, repeatRows=1)
            equipos_table.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, colors.black), # Rejilla simple negra
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ALIGN', (0,0), (0,-1), 'CENTER'), 
                ('FONTNAME', (0,0), (-1,-1), self.base_font_name), 
                ('FONTNAME', (0,0), (-1,0), self.base_font_name_bold),
                ('FONTSIZE', (0,0), (-1,-1), 9), # Fuente más pequeña para la tabla
                ('TEXTCOLOR', (0,0), (-1,0), colors.black), # Encabezados en negro
                ('BACKGROUND', (0,0), (-1,0), colors.white), # Sin fondo en encabezados
                ('BOTTOMPADDING', (0,0), (-1,-1), 1.5*mm),
                ('TOPPADDING', (0,0), (-1,-1), 1.5*mm),
            ]))
            story.append(equipos_table)

            # --- Nota Legal (EN NEGRITA) ---
            nota_legal_texto_base = """NOTA: DEJA CONSTANCIA QUE EL EQUIPO ANTES DESCRITO EN ESTA NOTA, ES PARA EL USO EXCLUSIVO DEL TRABAJADOR EN LAS LABORES EJECUTADAS PARA CORPOELEC, Y ESTE NO PUEDE SER RETIRADO, NI TRASLADADO DEL CENTRO DE TRABAJO SIN NOTIFICAR A LA UNIDAD DE ATIT.<br/><br/>ES RESPONSABILIDAD DEL TRABAJADOR VELAR POR EL BUEN USO DEL EQUIPO ASIGNADO, ASI COMO DE SU CUSTODIA DENTRO DE SU HORARIO DE TRABAJO Y CUANDO SEA AUTORIZADO SU TRASLADO, FUERA DEL CENTRO DE TRABAJO; POR LO QUE DEBE TOMAR TODAS LAS MEDIDAS DE SEGURIDAD CORRESPONDIENTES PARA EL RESGUARDO Y CUIDADO DEL EQUIPO.<br/><br/>EN CASO DE NEGLIGENCIA, DETERIORO O PÉRDIDA DE TODO O PARTE DEL EQUIPO, EL TRABAJADOR SERÁ RESPONSABLE DEL EQUIPO ASIGNADO, POR LO TANTO, DEBERÁ RESARCIR LOS DAÑOS CAUSADOS."""
            story.append(Paragraph(nota_legal_texto_base, self.styles['LegalText']))

            # --- Firma (CENTRADO Y EN NEGRITA) ---
            story.append(Paragraph("Atentamente,", self.styles['SignatureAttn']))
            # No hay línea "___________"
            story.append(Spacer(1, 0.5*cm)) # Pequeño espacio antes del nombre
            story.append(Paragraph("ESP. FELIX A FERNANDEZ B", self.styles['SignatureBlock']))
            story.append(Paragraph("GERENTE ESTADAL DE AUTOMATIZACIÓN, TECNOLOGÍA", self.styles['SignatureBlock']))
            story.append(Paragraph("DE LA INFORMACIÓN Y TELECOMUNICACIONES (ATIT MONAGAS).", self.styles['SignatureBlock']))
            story.append(Paragraph("Designado mediante el N°GGTH-0405-09-2024 de fecha 06/09/2024", self.styles['SignatureBlock']))
            story.append(Paragraph("Corporación Eléctrica Nacional, S.A. (CORPOELEC)", self.styles['SignatureBlock']))

            def on_first_page_wrapper(canvas, doc):
                self._draw_header_footer(canvas, doc, header_image_path, footer_image_path, is_first_page=True)
            def on_later_pages_wrapper(canvas, doc):
                self._draw_header_footer(canvas, doc, header_image_path, footer_image_path, is_first_page=False)

            doc.build(story, onFirstPage=on_first_page_wrapper, onLaterPages=on_later_pages_wrapper)
            return {'success': True, 'message': f'Documento generado en:\n{download_dir}', 'filepath': destination_path}

        except Exception as e:
            print(f"!!! Error EXCEPCIÓN generando documento '{document_type}': {e}")
            traceback.print_exc()
            return {'success': False, 'message': f'Error crítico al generar el documento: {e}'}