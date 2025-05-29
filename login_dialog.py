import sys
import os

from PySide2.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QApplication,
                             QWidget, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy)
from PySide2.QtGui import QImage, QPixmap, QPainter, QColor, QFont
from PySide2.QtCore import Qt, QSize

# Importación de database con manejo de error y mock básico
try:
    import database
    DATABASE_AVAILABLE = True
except ImportError:
    print("ERROR CRÍTICO: No se pudo importar el módulo 'database'.")
    DATABASE_AVAILABLE = False
    class MockDatabase:
        def check_user_credentials(self, u, p): return None
        def inicializar_db(self): pass
    database = MockDatabase()
    print("ADVERTENCIA: Usando módulo 'database' simulado.")

def resource_path(relative_path_within_assets):
    """ Obtiene la ruta absoluta al recurso en 'html_ui/assets/' """
    try:
        base_path = sys._MEIPASS
        return os.path.join(base_path, 'html_ui', 'assets', relative_path_within_assets)
    except AttributeError:
        current_script_dir = os.path.dirname(__file__)
        return os.path.join(current_script_dir, 'html_ui', 'assets', relative_path_within_assets)

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SISTEMA INVENTARIO EQUIPOS CORPORATIVOS")
        self.setModal(True)
        self.setMinimumSize(420, 500) # Ajustado para asegurar espacio

        self.user_role = None
        self.user_id = None
        self.login_attempted_successfully = False

        flags = self.windowFlags()
        flags &= ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

        # Paleta de colores (igual que antes)
        self.primary_color = "#003366"    # Azul oscuro corporativo
        self.secondary_color = "#F0F0F0"  # Gris claro para el fondo del diálogo
        self.accent_color = "#0078D4"     # Azul brillante para botones principales
        self.text_color = "#333333"
        self.error_color = "#D32F2F"
        self.container_bg_color = "#FFFFFF" # Blanco para el contenedor principal

        # Referencias a widgets clave para simplificar acceso
        self.container_widget = None
        self.title_label = None
        self.user_input = None
        self.pass_input = None
        self.error_label = None
        self.login_button = None
        self.cancel_button = None

        self._setup_ui_reworked()
        self._apply_styles_reworked()

        self.user_input.setFocus()
        self.user_input.returnPressed.connect(self.pass_input.setFocus)
        self.pass_input.returnPressed.connect(self._on_login_button_clicked)

    def _setup_ui_reworked(self):
        # Layout principal para el diálogo (fondo gris)
        main_dialog_layout = QVBoxLayout(self)
        main_dialog_layout.setContentsMargins(15, 15, 15, 15) # Margen para ver el fondo del diálogo
        main_dialog_layout.setSpacing(0)

        # Contenedor principal para el contenido (fondo blanco, con sombra)
        self.container_widget = QWidget()
        self.container_widget.setObjectName("ContentContainer")
        
        container_layout = QVBoxLayout(self.container_widget)
        container_layout.setContentsMargins(30, 25, 30, 25)
        container_layout.setSpacing(18) # Espacio entre elementos dentro del contenedor

        # 1. Sección del Logo
        logo_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_path = resource_path("logo.png") # Asegúrate que esta ruta sea correcta
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaled(180, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)) # Ajusta tamaño según tu logo
        else:
            logo_label.setText("LOGO") # Placeholder si no hay imagen
            logo_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {self.primary_color};")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label) # El logo se centrará por el QHBoxLayout
        container_layout.addLayout(logo_layout)

        # 2. Título
        self.title_label = QLabel("Bienvenido")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.title_label)

        # Espaciador vertical
        container_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # 3. Campos de Entrada
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Nombre de Usuario")
        self.user_input.setObjectName("UserInput")
        container_layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setObjectName("PassInput")
        container_layout.addWidget(self.pass_input)

        # 4. Etiqueta de Error
        self.error_label = QLabel(" ") # Espacio para mantener altura
        self.error_label.setObjectName("ErrorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setVisible(False) # Oculta inicialmente
        container_layout.addWidget(self.error_label)
        
        # Espaciador flexible para empujar botones hacia abajo
        container_layout.addStretch(1)

        # 5. Botones
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10) # Espacio entre botones

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setObjectName("CancelButton")
        self.cancel_button.setAutoDefault(False)
        self.cancel_button.clicked.connect(self.reject)
        
        self.login_button = QPushButton("INGRESAR")
        self.login_button.setObjectName("LoginButton")
        self.login_button.setAutoDefault(True)
        self.login_button.setDefault(True)
        self.login_button.clicked.connect(self._on_login_button_clicked)

        button_layout.addStretch(1) # Empuja los botones a la derecha
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.login_button)
        # Si prefieres Cancelar a la izquierda e Ingresar a la derecha separados:
        # button_layout.addWidget(self.cancel_button)
        # button_layout.addStretch(1)
        # button_layout.addWidget(self.login_button)
        # --> Voy a usar la segunda opción que es más estándar: Cancelar | ---stretch--- | Ingresar

        # Re-haciendo el layout de botones para la disposición estándar:
        proper_button_layout = QHBoxLayout()
        proper_button_layout.setSpacing(10)
        proper_button_layout.addWidget(self.cancel_button)
        proper_button_layout.addStretch(1) # ESTE ES EL STRETCH CLAVE
        proper_button_layout.addWidget(self.login_button)
        
        container_layout.addLayout(proper_button_layout)
        
        # Añadir el contenedor principal (blanco) al layout del diálogo (gris)
        main_dialog_layout.addWidget(self.container_widget)
        self.setLayout(main_dialog_layout)


    def _apply_styles_reworked(self):
        # Fuentes
        font_main = QFont("Segoe UI", 10)
        font_title = QFont("Segoe UI Semibold", 22) # Un poco más grande
        font_button = QFont("Segoe UI Semibold", 11)
        font_input = QFont("Segoe UI", 10)
        font_error = QFont("Segoe UI", 9)

        self.setFont(font_main) # Fuente por defecto para el diálogo

        # Aplicar fuentes específicas
        self.title_label.setFont(font_title)
        self.user_input.setFont(font_input)
        self.pass_input.setFont(font_input)
        self.error_label.setFont(font_error)
        self.login_button.setFont(font_button)
        self.cancel_button.setFont(font_button)
        
        # Sombra para el contenedor (aplicada directamente al widget)
        shadow = QGraphicsDropShadowEffect(self) # Parent del efecto es el diálogo
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 70)) # Sombra un poco más sutil
        self.container_widget.setGraphicsEffect(shadow)

        # Hoja de estilos QSS
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {self.secondary_color}; /* Fondo del diálogo */
            }}
            QWidget#ContentContainer {{
                background-color: {self.container_bg_color}; /* Fondo blanco del contenedor */
                border-radius: 8px; /* Bordes redondeados para el contenedor */
            }}
            QLabel#TitleLabel {{
                color: {self.primary_color};
                padding-top: 5px; /* Espacio arriba del título */
                padding-bottom: 5px; /* Espacio abajo del título */
                font-weight: bold; /* Asegurar que sea negrita si la fuente no lo es */
            }}
            QLineEdit {{
                border: 1px solid #B0B0B0;
                border-radius: 4px;
                padding: 10px 12px; /* Aumentar padding para mejor tacto */
                background-color: #FDFDFD;
                min-height: 20px; /* Altura mínima */
            }}
            QLineEdit:focus {{
                border: 1px solid {self.accent_color};
                background-color: #FFFFFF;
            }}
            QLabel#ErrorLabel {{
                color: {self.error_color};
                padding-top: 4px;
                min-height: 20px; /* Altura para que ocupe espacio */
            }}
            QPushButton#LoginButton {{
                background-color: {self.accent_color};
                color: white;
                border: none;
                padding: 10px 28px; /* Más padding horizontal */
                border-radius: 4px;
                min-height: 22px; /* Altura mínima */
            }}
            QPushButton#LoginButton:hover {{
                background-color: #005A9E; /* Un poco más oscuro al pasar el mouse */
            }}
            QPushButton#LoginButton:pressed {{
                background-color: #004C83; /* Aún más oscuro al presionar */
            }}
            QPushButton#CancelButton {{
                background-color: #E0E0E0;
                color: #444444; /* Texto un poco más oscuro */
                border: 1px solid #BBBBBB;
                padding: 10px 22px;
                border-radius: 4px;
                min-height: 22px; /* Altura mínima */
            }}
            QPushButton#CancelButton:hover {{
                background-color: #D0D0D0;
                border-color: #ADADAD;
            }}
            QPushButton#CancelButton:pressed {{
                background-color: #C0C0C0;
            }}
        """)

    def _show_error_message(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(True)

    def _clear_error_message(self):
        self.error_label.setText(" ") # Dejar un espacio para mantener la altura
        self.error_label.setVisible(False)

    def _on_login_button_clicked(self):
        self._clear_error_message()
        username = self.user_input.text().strip()
        password = self.pass_input.text()

        if not username or not password:
            self._show_error_message("Usuario y contraseña son requeridos.")
            if not username: self.user_input.setFocus()
            else: self.pass_input.setFocus()
            return

        if not DATABASE_AVAILABLE:
            self._show_error_message("Error interno: Servicio de autenticación no disponible.")
            return

        try:
            login_data = database.check_user_credentials(username, password)
        except Exception as e_db:
            print(f"LoginDialog: Excepción al llamar a database.check_user_credentials: {e_db}")
            self._show_error_message("Error al contactar el servicio de autenticación.")
            return

        if login_data:
            role, user_id_val = login_data
            self.user_role = role
            self.user_id = user_id_val
            self.login_attempted_successfully = True
            super().accept()
        else:
            self._show_error_message("Usuario o contraseña incorrectos.")
            self.pass_input.selectAll()
            self.pass_input.setFocus()

    def get_login_data(self):
        if self.login_attempted_successfully:
            return (self.user_role, self.user_id)
        return None

    @staticmethod
    def execute(parent=None):
        dialog = LoginDialog(parent)
        result_code = dialog.exec_()
        if result_code == QDialog.Accepted and dialog.login_attempted_successfully:
            return dialog.get_login_data()
        return None

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)

    # Creación de logo y assets (como en tu original, ajustado)
    current_script_dir_for_main = os.path.dirname(__file__)
    assets_dir_for_main = os.path.join(current_script_dir_for_main, 'html_ui', 'assets')
    if not os.path.exists(assets_dir_for_main):
        try:
            os.makedirs(assets_dir_for_main)
        except OSError as e:
            print(f"Advertencia: No se pudo crear el directorio de assets: {e}")

    placeholder_logo_path_for_main = os.path.join(assets_dir_for_main, "logo.png")
    if not os.path.exists(placeholder_logo_path_for_main):
        try:
            img = QImage(180, 60, QImage.Format_ARGB32_Premultiplied)
            img.fill(Qt.transparent)
            p = QPainter(img)
            p.setRenderHint(QPainter.Antialiasing)
            
            # Usar los colores definidos en la clase para el placeholder
            temp_dialog = LoginDialog() # Para acceder a los colores
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(temp_dialog.primary_color))
            p.drawRoundedRect(0,0, 180, 60, 10, 10) # Rectángulo redondeado como base

            p.setPen(Qt.white)
            font_logo = QFont("Segoe UI", 20, QFont.Bold)
            p.setFont(font_logo)
            p.drawText(img.rect(), Qt.AlignCenter, "EMPRESA")
            p.end()
            img.save(placeholder_logo_path_for_main)
            print(f"Logo de placeholder creado en: {placeholder_logo_path_for_main}")
        except Exception as e_logo:
            print(f"No se pudo crear el logo de placeholder: {e_logo}")
    else:
        print(f"Usando logo existente en: {placeholder_logo_path_for_main}")

    print("Inicializando BD para prueba de LoginDialog...")
    try:
        if DATABASE_AVAILABLE and not isinstance(database, MockDatabase):
            database.inicializar_db() # Asume que esto crea usuarios de prueba si es necesario
            print("BD real inicializada.")
        elif isinstance(database, MockDatabase):
             print("Usando BD simulada para la prueba.")
             database.inicializar_db()
        else:
            raise Exception("Configuración de base de datos inválida.")
    except Exception as e:
        print(f"No se pudo inicializar la BD para prueba: {e}")
        QMessageBox.critical(None, "Error DB", f"No se pudo inicializar la base de datos para la prueba:\n{e}")

    print("Ejecutando LoginDialog de prueba...")
    login_result = LoginDialog.execute()

    if login_result:
        role, user_id_res = login_result
        print(f"\nPrueba de LoginDialog: Éxito. Rol: {role}, ID: {user_id_res}")
        QMessageBox.information(None, "Prueba Login", f"Inicio de sesión exitoso.\nRol: {role}\nID: {user_id_res}")
    else:
        print("\nPrueba de LoginDialog: Cancelado o login fallido.")

    print("Saliendo de la prueba.")
    sys.exit(app.exec_())