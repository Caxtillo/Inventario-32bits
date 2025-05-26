# login_dialog.py (Adaptado para PySide2, Python 3.8, Win7 32-bit)

import sys
import os # Para resource_path

from PySide2.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QDialogButtonBox, QApplication,
                             QWidget, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy)
from PySide2.QtGui import QImage, QPixmap, QPainter, QColor, QBrush, QPalette, QFont, QIcon
from PySide2.QtCore import Qt, QSize

try:
    import database
except ImportError:
    print("ERROR: No se pudo importar el módulo 'database'. Funcionalidad limitada.")
    database = None

def resource_path(relative_path_within_assets):
    """ 
    Obtiene la ruta absoluta al recurso.
    Asume que los recursos del diálogo (como el logo) están en 'html_ui/assets/'.
    """
    try:

        base_path = sys._MEIPASS
        return os.path.join(base_path, 'html_ui', 'assets', relative_path_within_assets)
    except AttributeError:

        base_path_project_root = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(base_path_project_root, 'html_ui', 'assets', relative_path_within_assets)

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SISTEMA INVENTARIO EQUIPOS CORPORATIVOS")
        self.setModal(True)
        self.setMinimumWidth(400) # Un poco más ancho para el diseño
        self.user_role = None
        self.user_id = None

        flags = self.windowFlags()
        flags &= ~Qt.WindowContextHelpButtonHint # Operación AND con el NOT bit a bit
        self.setWindowFlags(flags)

        # --- Estilo General ---
        # Paleta de colores corporativos (ejemplos, ajústalos)
        self.primary_color = "#003366" # Azul oscuro corporativo
        self.secondary_color = "#E0E0E0" # Gris claro para fondos
        self.accent_color = "#0078D4" # Azul brillante para acentos
        self.text_color = "#333333" # Texto oscuro
        self.error_color = "#D32F2F" # Rojo para errores

        self._setup_ui()
        self._apply_styles()

        self.user_input.setFocus()
        self.pass_input.returnPressed.connect(self._try_login)
        # Considerar conectar returnPressed de user_input a pass_input.setFocus()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) # Sin márgenes para el layout principal
        main_layout.setSpacing(0)

        # --- Contenedor Principal con Sombra ---
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setContentsMargins(30, 30, 30, 30) # Márgenes internos
        container_layout.setSpacing(20) # Espacio entre elementos

        # --- Sección del Logo ---
        logo_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_path = resource_path("logo.png") # Asegúrate que 'logo.png' esté en 'assets'
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignCenter)
        else:
            logo_label.setText("LOGO EMPRESA")
            logo_label.setAlignment(Qt.AlignCenter)
            logo_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {self.primary_color};")
        logo_layout.addStretch()
        logo_layout.addWidget(logo_label)
        logo_layout.addStretch()
        container_layout.addLayout(logo_layout)
        container_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))


        # --- Título ---
        title_label = QLabel("Bienvenido")
        title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title_label)

        # --- Campos de Entrada ---
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Nombre de Usuario")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)

        container_layout.addWidget(self.user_input)
        container_layout.addWidget(self.pass_input)
        
        container_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # --- Etiqueta de Error (inicialmente oculta) ---
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setVisible(False) # Ocultar inicialmente
        container_layout.addWidget(self.error_label)

        container_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # --- Botones ---
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("INGRESAR")
        self.login_button.setObjectName("LoginButton") # Para QSS
        self.login_button.clicked.connect(self._try_login)
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setObjectName("CancelButton") # Para QSS
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        button_layout.addWidget(self.login_button)
        container_layout.addLayout(button_layout)
        
        main_layout.addWidget(container_widget)
        self.setLayout(main_layout)

    def _apply_styles(self):
        font_main = QFont("Segoe UI", 10) # Fuente principal
        font_title = QFont("Segoe UI Semibold", 20)
        font_button = QFont("Segoe UI Semibold", 11)

        self.setFont(font_main)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {self.secondary_color}; /* Fondo del diálogo en sí */
                border-radius: 8px; /* Redondear esquinas del diálogo si el SO lo permite */
            }}
            QWidget {{ /* Estilo para el contenedor principal dentro del diálogo */
                background-color: #FFFFFF; /* Fondo blanco para el contenido */
                border-radius: 6px;
            }}
            QLabel#TitleLabel {{ /* Si le pones un objectName al título */
                font-size: 24px;
                font-weight: bold;
                color: {self.primary_color};
                padding-bottom: 10px;
            }}
            QLineEdit {{
                border: 1px solid #BDBDBD;
                border-radius: 4px;
                padding: 10px 8px;
                font-size: 10pt;
                background-color: #F5F5F5;
            }}
            QLineEdit:focus {{
                border: 1px solid {self.accent_color};
                background-color: #FFFFFF;
            }}
            QPushButton#LoginButton {{
                background-color: {self.accent_color};
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 4px;
                font-size: 11pt;
            }}
            QPushButton#LoginButton:hover {{
                background-color: #005A9E; /* Un azul más oscuro al pasar el mouse */
            }}
            QPushButton#LoginButton:pressed {{
                background-color: #004C83; /* Aún más oscuro al presionar */
            }}
            QPushButton#CancelButton {{
                background-color: #E0E0E0; /* Gris claro */
                color: #555555;
                border: 1px solid #CCCCCC;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 11pt;
            }}
            QPushButton#CancelButton:hover {{
                background-color: #D0D0D0;
            }}
            QPushButton#CancelButton:pressed {{
                background-color: #C0C0C0;
            }}
            QLabel[objectName="errorLabel"] {{ /* Para el QLabel de error */
                color: {self.error_color};
                font-size: 9pt;
                padding-top: 5px;
            }}
        """)

        # Aplicar fuentes a elementos específicos
        title_label = self.findChild(QLabel, "Bienvenido") # Asumiendo que solo hay uno con ese texto
        if title_label: 
            title_label.setFont(font_title)
            title_label.setStyleSheet(f"color: {self.primary_color}; margin-bottom: 15px;")
        
        self.login_button.setFont(font_button)
        self.cancel_button.setFont(font_button)

        self.error_label.setObjectName("errorLabel") # Para que QSS lo tome
        self.error_label.setFont(QFont("Segoe UI", 9))


    def _show_error_message(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(True)
        # Podrías añadir una pequeña animación o cambio de color al mostrar error

    def _clear_error_message(self):
        self.error_label.setText("")
        self.error_label.setVisible(False)

    def _try_login(self):
        self._clear_error_message() # Limpiar errores previos
        username = self.user_input.text().strip()
        password = self.pass_input.text()

        if not username or not password:
            self._show_error_message("Usuario y contraseña son requeridos.")
            if not username: self.user_input.setFocus()
            else: self.pass_input.setFocus()
            return

        if database is None:
             self._show_error_message("Error interno: Módulo de base de datos no disponible.")
             return

        print(f"LoginDialog: Verificando credenciales para '{username}'...")
        try:
            login_data = database.check_user_credentials(username, password)
        except Exception as e:
             print(f"LoginDialog: Error al llamar a check_user_credentials: {e}")
             self._show_error_message(f"Error de conexión con la base de datos.")
             return

        if login_data:
            role, user_id = login_data
            print(f"LoginDialog: Autenticación exitosa. Rol: {role}, ID: {user_id}")
            self.user_role = role
            self.user_id = user_id
            super().accept()
        else:
            print(f"LoginDialog: Autenticación fallida para '{username}'.")
            self._show_error_message("Usuario o contraseña incorrectos.")
            self.pass_input.selectAll() # Seleccionar texto para fácil reingreso
            self.pass_input.setFocus()

    def accept(self): # Override para que solo se llame desde _try_login
        # No hacemos nada aquí, el super().accept() se llama desde _try_login
        pass

    def get_login_data(self):
        return (self.user_role, self.user_id)

    @staticmethod
    def execute(parent=None):
        dialog = LoginDialog(parent)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            return dialog.get_login_data()
        return None

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)

    # Crear directorio 'assets' si no existe y poner un logo de placeholder
    # Esto es solo para la prueba, en producción el logo debe estar en el lugar correcto
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    placeholder_logo_path = os.path.join(assets_dir, "logo.png")
    if not os.path.exists(placeholder_logo_path):
        try:
            # Crear un logo simple de placeholder si no tienes uno
            img = QImage(100, 100, QImage.Format_ARGB32)
            img.fill(QColor(0, 51, 102, 150)) # Azul semitransparente
            painter = QPainter(img)
            painter.setPen(QColor("white"))
            painter.setFont(QFont("Arial", 12, QFont.Bold))
            painter.drawText(img.rect(), Qt.AlignCenter, "LOGO")
            painter.end()
            img.save(placeholder_logo_path)
            print(f"Placeholder logo.png creado en {placeholder_logo_path}")
        except Exception as e_logo:
            print(f"No se pudo crear el logo de placeholder: {e_logo}")


    print("Inicializando BD para prueba de LoginDialog...")
    try:
        if database:
             database.inicializar_db()
             print("BD inicializada.")
        else:
             raise Exception("Módulo Database no importado")
    except Exception as e:
        print(f"No se pudo inicializar la BD para prueba: {e}")
        QMessageBox.critical(None, "Error DB", f"No se pudo inicializar la base de datos:\n{e}")
        sys.exit(1)

    print("Ejecutando LoginDialog de prueba...")
    login_result = LoginDialog.execute()

    if login_result:
        role, user_id = login_result
        print(f"\nPrueba de LoginDialog: Éxito. Rol: {role}, ID: {user_id}")
        QMessageBox.information(None, "Prueba Login", f"Inicio de sesión exitoso.\nRol: {role}\nID: {user_id}")
    else:
        print("\nPrueba de LoginDialog: Cancelado o fallido.")
        # QMessageBox.information(None, "Prueba Login", "Inicio de sesión cancelado o fallido.") # Opcional

    print("Saliendo de la prueba.")
    sys.exit()