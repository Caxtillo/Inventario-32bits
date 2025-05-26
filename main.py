# main.py (Adaptado para PySide2, Python 3.8, Win7 32-bit)

import sys
import os
import traceback

# --- Importaciones de PySide2 ---
from PySide2.QtWidgets import (QApplication, QMainWindow, QMessageBox, QDialog, QFileDialog)
from PySide2.QtGui import QScreen, QPageLayout, QPageSize
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PySide2.QtCore import (QUrl, QObject, Slot, Signal, QDateTime,
                            QStandardPaths, QFileInfo, QTimer, Qt, QMarginsF, QLocale)
from PySide2.QtWebChannel import QWebChannel

# Importar nuestros módulos locales
import database
from login_dialog import LoginDialog # Asegúrate que usa PySide2
from backend_handler import BackendHandler # Asegúrate que usa PySide2

# Función para obtener rutas
def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


# Ventana Principal
class MainWindow(QMainWindow):
    def __init__(self, html_path_to_load, user_role, user_id):
        super().__init__()
        self.user_role = user_role
        self.user_id = user_id
        self.setWindowTitle(f"Inventario de Equipos Corporativos (Rol: {self.user_role.capitalize()}) - PySide2")

        # --- Maximizar Ventana ---
        screen = QApplication.primaryScreen()
        if screen:
            self.showMaximized()
            print(f"MainWindow: Iniciando maximizada.")
        else:
            print("Advertencia: No se pudo obtener la pantalla principal. Usando tamaño por defecto.")
            self.setGeometry(100, 100, 1200, 800)

        # --- Configuración de QWebEngineView ---
        self.view = QWebEngineView(self)
        self.setCentralWidget(self.view)
        self.page = self.view.page() # Obtener página por defecto

        settings = self.page.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.PrintElementBackgrounds, True)

        # --- HABILITAR HERRAMIENTAS DE DESARROLLADOR (Intento PySide2/Qt5 - Directo) ---
        try:
            # Intenta acceder a las constantes directamente
            settings.setAttribute(QWebEngineSettings.RemoteDebuggingEnabled, True) # SIN WebAttribute
            print(">>> RemoteDebuggingEnabled Habilitado (Conectar desde chrome://inspect)")
        except AttributeError:
            print(">>> ERROR: QWebEngineSettings.RemoteDebuggingEnabled no encontrado directamente. La depuración remota podría no funcionar.")
            traceback.print_exc() # Imprimir el error exacto

        try:
            settings.setAttribute(QWebEngineSettings.DeveloperExtrasEnabled, True) # SIN WebAttribute
            print(">>> DeveloperExtrasEnabled Habilitado (Intentar clic derecho -> Inspeccionar)")
        except AttributeError:
            print(">>> ERROR: QWebEngineSettings.DeveloperExtrasEnabled no encontrado directamente. El menú Inspeccionar podría no funcionar.")
            traceback.print_exc() # Imprimir el error exacto
        # ---------------------------------------------------------------------

        print("MainWindow: Configuraciones de WebEngine aplicadas (con intentos para DevTools).")

        # --- Configurar QWebChannel ---
        self.channel = QWebChannel(self.page)
        self.page.setWebChannel(self.channel)

        # --- Crear e registrar el objeto backend ---
        print("Creando instancia de BackendHandler...")
        self.backend_handler = BackendHandler(user_role=self.user_role, user_id=self.user_id)
        self.channel.registerObject("backend", self.backend_handler)
        print("BackendHandler creado y registrado en WebChannel.")

        # --- Conectar Señales ---
        print("Conectando señales...")
        self._connect_signals()

        # --- Cargar HTML inicial ---
        if not self.load_html(html_path_to_load):
             print(f"ERROR FATAL: Falló la carga inicial de {html_path_to_load}")


    def _connect_signals(self):
        """Método helper para conectar las señales del backend."""
        try:
            if hasattr(self.backend_handler, 'navigation_requested'):
                 self.backend_handler.navigation_requested.connect(self.handle_navigation)
                 print("  CONECTADO: navigation_requested -> handle_navigation")
            # Eliminar o comentar si show_message no se usa en backend_handler
            # if hasattr(self.backend_handler, 'show_message'):
            #      self.backend_handler.show_message.connect(self.display_message_popup)
            #      print("  CONECTADO: show_message")
            if hasattr(self.backend_handler, 'close_application_requested'):
                 self.backend_handler.close_application_requested.connect(self.close)
                 print("  CONECTADO: close_application_requested -> self.close")
            if hasattr(self.backend_handler, 'print_requested'):
                self.backend_handler.print_requested.connect(self.handle_print_request)
                print("  CONECTADO: print_requested -> handle_print_request")
            else:
                print("  ADVERTENCIA: BackendHandler no tiene la señal 'print_requested'.")

            print("Señales conectadas correctamente.")
        except Exception as e:
             print(f"ERROR FATAL conectando señales: {e}")
             traceback.print_exc()
             QMessageBox.critical(self, "Error Crítico", f"Error al conectar componentes internos:\n{e}")

    def load_html(self, file_path):
        """Carga un archivo HTML local en la vista web."""
        file_info = QFileInfo(file_path)
        if not file_info.exists():
            msg = f"No se encuentra el archivo HTML:\n{file_path}"
            print(f"ERROR FATAL: {msg}")
            QMessageBox.critical(self, "Error Fatal", msg)
            self.close()
            return False

        local_url = QUrl.fromLocalFile(file_info.absoluteFilePath())
        print(f"MainWindow: Cargando URL local: {local_url.toString()}")

        if self.page and self.view:
             self.page.load(local_url)
             return True
        else:
             print("ERROR FATAL: self.page o self.view no están inicializados antes de load_html.")
             QMessageBox.critical(self, "Error Fatal", "Error interno: Componentes web no listos.")
             self.close()
             return False

    # --- SLOTS DE MANEJO ---
    @Slot(str)
    def handle_navigation(self, page_name):
        """Maneja la señal de navegación del backend."""
        print(f"MainWindow: Navegación solicitada a '{page_name}'")
        html_filename = ""
        if page_name == 'inventory':
            html_filename = "index.html"
        elif page_name == 'users':
            if self.user_role != 'admin':
                print("Permiso denegado para acceder a la gestión de usuarios.")
                self.display_message_popup('warning', 'No tiene permisos para acceder a esta sección.')
                return
            html_filename = "users.html"
        elif page_name == 'dashboard': # <-- AÑADIR ESTO
            html_filename = "dashboard.html" # <-- AÑADIR ESTO
        else:
            print(f"Advertencia: Nombre de página desconocido para navegación: {page_name}")
            self.display_message_popup('warning', f"Página '{page_name}' no reconocida.")
            return

        html_path = resource_path(os.path.join("html_ui", html_filename))
        if not self.load_html(html_path):
            print(f"Error: No se pudo cargar la página '{page_name}' desde {html_path}")
            self.display_message_popup('error', f"No se pudo cargar la página '{page_name}'.")

    @Slot(str, str)
    def display_message_popup(self, msg_type, message):
         """Muestra un mensaje popup al usuario."""
         print(f"Mensaje Popup [{msg_type.upper()}]: {message}")
         msg_type = msg_type.lower()
         if msg_type == 'success': QMessageBox.information(self, "Éxito", message)
         elif msg_type == 'error': QMessageBox.critical(self, "Error", message)
         elif msg_type == 'info': QMessageBox.information(self, "Información", message)
         elif msg_type == 'warning': QMessageBox.warning(self, "Aviso", message)
         else: QMessageBox.information(self, "Mensaje", message)

    # --- SLOT PARA IMPRESIÓN / EXPORTACIÓN PDF DIRECTA ---
    @Slot(list, str)
    def handle_print_request(self, filtered_data, print_format):
        """Maneja la solicitud de impresión/exportación directa a PDF desde JS."""
        print(f"MainWindow: Solicitud handle_print_request recibida. Formato: {print_format}, Items: {len(filtered_data)}")

        if not self.page:
            print("ERROR: No se puede imprimir/exportar, self.page no es válido.")
            self.display_message_popup('error', "La página web no está lista para imprimir/exportar.")
            return

        timestamp = QDateTime.currentDateTime().toString("yyyyMMdd_hhmmss")
        filename_hint = f"reporte_{print_format}_{timestamp}.pdf"
        documents_path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        suggested_path = os.path.join(documents_path, filename_hint)

        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(self, f"Guardar Reporte {print_format.upper()} como PDF", suggested_path, "Archivos PDF (*.pdf);;Todos los archivos (*.*)", options=options)

        if filePath:
            if not filePath.lower().endswith(".pdf"): filePath += ".pdf"
            print(f"Generando PDF ({print_format}) en: {filePath}")

            page_layout = QPageLayout()
            page_layout.setPageSize(QPageSize(QPageSize.StandardKey.A4))
            orientation = QPageLayout.Orientation.Landscape if print_format == 'table' else QPageLayout.Orientation.Portrait
            page_layout.setOrientation(orientation)
            margins_mm = QMarginsF(10, 10, 10, 10)
            page_layout.setMargins(margins_mm, QPageLayout.Unit.Millimeter)

            def pdf_export_finished(success):
                if success:
                    print(f"PDF ({print_format}) generado con éxito: {filePath}")
                    self.display_message_popup('success', f"El reporte ({print_format}) se ha guardado como:\n{filePath}")
                else:
                    print(f"ERROR: Falló la generación de PDF ({print_format}) a: {filePath}")
                    self.display_message_popup('error', f"Ocurrió un error al generar el archivo PDF ({print_format}).")

            try:
                print(f"Llamando a self.page.printToPdf para formato '{print_format}'...")
                self.page.printToPdf(pdf_export_finished, page_layout)
            except Exception as e:
                 print(f"ERROR EXCEPCIÓN al llamar a printToPdf: {e}")
                 traceback.print_exc()
                 self.display_message_popup('error', f"Excepción al exportar PDF:\n{e}")
        else:
            print("Generación de PDF cancelada por el usuario.")


    def closeEvent(self, event):
        """Acciones al intentar cerrar la ventana principal."""
        print("Cerrando aplicación.")
        event.accept()

# Función principal de la aplicación (main)
def main():
    # --- FIJAR PUERTO DE DEPURACIÓN REMOTA ---
    # Es importante hacerlo ANTES de crear QApplication si se usa la variable de entorno
    debug_port = '9223'
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = debug_port
    print(f"Intentando fijar puerto de depuración remota a: {debug_port}")
    QLocale.setDefault(QLocale("es_ES")) # Otra forma más simple
    print(f"Locale de la aplicación establecido a: {QLocale().name()}") # Para verificar
    # -----------------------------------------

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)

    # Inicializar Base de Datos
    print("Inicializando base de datos...")
    try:
        database.inicializar_db()
        print("Base de datos lista.")
    except Exception as e:
         print(f"Error Crítico inicializando DB: {e}")
         traceback.print_exc()
         QMessageBox.critical(None, "Error Crítico de Base de Datos", f"No se pudo inicializar la base de datos:\n{e}\n\nLa aplicación se cerrará.")
         sys.exit(1)

    # Mostrar Diálogo de Login
    print("Mostrando diálogo de login...")
    login_dialog = LoginDialog()
    login_result = login_dialog.execute() # O exec_()

    if login_result:
        user_role, user_id = login_result
        print(f"Login exitoso. Rol: {user_role}, ID: {user_id}. Iniciando ventana principal...")

        # --- CAMBIO AQUÍ: Cargar dashboard.html por defecto ---
        html_filename = "dashboard.html" # <-- CAMBIADO
        # html_filename = "index.html" # <-- ORIGINAL
        # -----------------------------------------------------
        html_path = resource_path(os.path.join("html_ui", html_filename))

        if not os.path.exists(html_path):
             msg = f"No se encuentra el archivo HTML principal ({html_filename}):\n{html_path}\n\nLa aplicación se cerrará." # Mensaje actualizado
             print(f"ERROR FATAL: {msg}")
             QMessageBox.critical(None, "Error Fatal de Archivo", msg)
             sys.exit(1)

        # Crear y mostrar la ventana principal
        main_window = MainWindow(html_path, user_role, user_id)
        main_window.show()

        print("Iniciando bucle de eventos de la aplicación...")
        sys.exit(app.exec_())

    else:
        print("Login cancelado o fallido. Saliendo.")
        sys.exit(0)


# Punto de entrada del script
if __name__ == "__main__":
     main()