# database.py (Compatible con Python 3.8, Win7 32-bit)

# --- Importaciones ---
import sqlite3
import os
import sys
from cryptography.fernet import Fernet, InvalidToken # Para encriptación simétrica
from werkzeug.security import generate_password_hash, check_password_hash # Para hashing de contraseñas
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# --- Configuración de Encriptación ---
# ¡¡¡ADVERTENCIA DE SEGURIDAD!!! ¡NO USAR ESTA CLAVE FIJA EN PRODUCCIÓN!
# Genera una clave segura (ver comentarios en tu código original) y guárdala externamente.
# Esta clave DEBE ser la misma siempre para poder desencriptar datos existentes.
ENCRYPTION_KEY = b'9pm2VMj7Vtx5J9bHCzhgq8km3b7M3PkL1C2VlhczR6c=' # ¡REEMPLAZA ESTO en un entorno real!
try:
    cipher_suite = Fernet(ENCRYPTION_KEY)
except ValueError as e:
    print(f"ERROR CRÍTICO: La clave de encriptación no es válida: {e}")
    print("Asegúrate de que ENCRYPTION_KEY sea una clave válida de Fernet (URL-safe base64 encoded 32-byte key).")
    sys.exit("Clave de encriptación inválida.")

# --- Configuración Base de Datos ---
DATABASE_FILENAME = "inventario_local.db"

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError: # Cambiado a AttributeError que es más específico para _MEIPASS
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

DB_PATH = resource_path(DATABASE_FILENAME)
print(f"Ruta de la base de datos (database.py): {DB_PATH}")

# --- Funciones de Ayuda para Encriptación (Compatibles) ---
def encrypt_data(data):
    """Encripta datos (si no son None). Devuelve bytes."""
    if data is None:
        return None
    try:
        data_bytes = str(data).encode('utf-8')
        encrypted_bytes = cipher_suite.encrypt(data_bytes)
        return encrypted_bytes
    except Exception as e:
        print(f"Error durante la encriptación: {e}")
        # Decide cómo manejar errores de encriptación. Devolver None podría ser una opción.
        # O relanzar el error si es crítico.
        return None # Devolver None si falla la encriptación

def decrypt_data(encrypted_data):
    """Desencripta datos (espera bytes). Devuelve string."""
    if not encrypted_data or not isinstance(encrypted_data, bytes):
        return None
    try:
        decrypted_bytes = cipher_suite.decrypt(encrypted_data)
        return decrypted_bytes.decode('utf-8')
    except InvalidToken:
        # print("ADVERTENCIA: Token inválido al desencriptar.") # Comentado para reducir ruido
        return "##Error Token##" # Mantener indicador claro de fallo
    except Exception as e:
        print(f"Error inesperado al desencriptar: {e}")
        return "##Error Desenc.##" # Mantener indicador claro de fallo

# --- Conexión y Inicialización DB (Compatibles) ---
def get_db_connection():
    """Establece conexión con la base de datos SQLite estándar."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10) # Añadido timeout por si acaso
        # conn.row_factory = sqlite3.Row # <- Quitado de aquí, aplicar solo donde se necesite Row o dict
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos [{DB_PATH}]: {e}")
        raise # Relanzar para que la aplicación principal sepa del error

def dict_factory(cursor, row):
    """Convierte las filas de la BD en diccionarios. Usado por varias funciones."""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def inicializar_db():
    """Crea las tablas necesarias si no existen."""
    required_tables = {'usuarios', 'equipos'}
    conn = None
    try:
        print(f"Inicializando DB en: {DB_PATH}")
        if not os.path.exists(os.path.dirname(DB_PATH)):
             print(f"Creando directorio para la BD: {os.path.dirname(DB_PATH)}")
             os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

        conn = get_db_connection()
        # Aplicar row_factory aquí específicamente para la comprobación de tablas
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        print("Verificando/Creando tablas...")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = {row['name'] for row in cursor.fetchall()}
        print(f"Tablas existentes: {existing_tables}")

        # --- Crear tabla usuarios ---
        if 'usuarios' not in existing_tables:
            print("Creando tabla 'usuarios'...")
            cursor.execute("""
                CREATE TABLE usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'manager', 'read_only')) DEFAULT 'read_only'
                )
            """)
            print("Tabla 'usuarios' creada.")
            # Crear usuario admin por defecto (cambiar contraseña en producción)
            admin_pass_hash = generate_password_hash("admin")
            cursor.execute("""
                INSERT INTO usuarios (username, password_hash, role)
                VALUES (?, ?, ?)
            """, ('admin', admin_pass_hash, 'admin'))
            print("Usuario 'admin' por defecto creado (pass: admin). ¡Cámbiala!")
        else:
             print("Tabla 'usuarios' ya existe.")

        # --- Crear tabla equipos ---
        if 'equipos' not in existing_tables:
            print("Creando tabla 'equipos'...")
            cursor.execute("""
                CREATE TABLE equipos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo_equipo TEXT NOT NULL,
                    marca TEXT,
                    modelo TEXT,
                    serial BLOB NOT NULL UNIQUE, -- <<< ESTO ES CORRECTO PARA NUEVAS BD
                    asignado_a BLOB,
                    departamento TEXT,
                    sede TEXT,
                    estatus TEXT DEFAULT 'Operativo',
                    ultimo_mantenimiento DATE,
                    proximo_mantenimiento DATE,
                    observacion BLOB,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Tabla 'equipos' creada.")
        else:
            print("Tabla 'equipos' ya existe.")
            # --- Verificar y posiblemente alterar la columna serial ---
            cursor.execute("PRAGMA table_info(equipos)")
            serial_column_info = None
            for col_info in cursor.fetchall():
                if col_info[1] == 'serial': # col_info[1] es el nombre de la columna
                    serial_column_info = col_info
                    break
            
            if serial_column_info:
                is_not_null = bool(serial_column_info[3]) # Correcto para NOT NULL
                # Comprobar si hay un índice UNIQUE en la columna 'serial'
                cursor.execute(f"PRAGMA index_list(equipos)")
                is_unique = False
                for index in cursor.fetchall():
                    if index[2] == 1: # index[2] es 'unique' (0 o 1)
                        cursor.execute(f"PRAGMA index_info('{index[1]}')") # index[1] es el nombre del índice
                        for col_in_index in cursor.fetchall():
                            if col_in_index[2] == 'serial': # col_in_index[2] es el nombre de la columna en el índice
                                is_unique = True
                                break
                    if is_unique:
                        break
                
                if not is_not_null or not is_unique:
                    print(f"ADVERTENCIA: La columna 'serial' en la tabla 'equipos' no es NOT NULL UNIQUE.")
                    print(f"  NOT NULL: {is_not_null}, UNIQUE: {is_unique}")
                    print(f"  Esto puede causar problemas. Se recomienda recrear la tabla con la constraint correcta.")
                    # Podrías intentar añadir un índice UNIQUE si no existe:
                    if not is_unique: # SOLO SI NO ES UNIQUE
                        try:
                            print("  Intentando añadir índice UNIQUE a la columna 'serial'...")
                            # ASEGURARSE QUE EL ÍNDICE SOLO SE CREA SI NO EXISTE YA OTRO ÍNDICE UNIQUE SOBRE SERIAL
                            # O si la columna no es parte de un PRIMARY KEY o UNIQUE constraint de tabla.
                            # Esta es una forma de intentarlo:
                            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_equipos_serial ON equipos(serial);")
                            conn.commit() # Commit después de crear el índice
                            print("  Índice UNIQUE 'idx_equipos_serial' intentado crear (o ya existente).")
                            # Volver a verificar si ahora es unique
                            # (Este re-check es un poco redundante aquí pero ilustra)
                        except sqlite3.Error as e_idx:
                            print(f"  Error al crear índice UNIQUE para serial: {e_idx}")
                            # Si falla (ej. por datos duplicados existentes), hacer rollback
                            conn.rollback() 
                else:
                    print("Columna 'serial' ya es NOT NULL y tiene un índice UNIQUE (o es parte de uno).")
            else:
                print("ADVERTENCIA: No se pudo verificar la columna 'serial'.")

        if 'historial_mantenimientos' not in existing_tables:
            print("Creando tabla 'historial_mantenimientos'...")
            cursor.execute("""
                CREATE TABLE historial_mantenimientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    equipo_id INTEGER NOT NULL,
                    fecha_realizado DATE NOT NULL,
                    tipo_mantenimiento TEXT, -- Ej: Preventivo, Correctivo, Actualización
                    descripcion BLOB, -- Encriptado para notas detalladas
                    realizado_por_usuario_id INTEGER, -- Opcional: Quién registró/realizó
                    fecha_registro_historial TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (equipo_id) REFERENCES equipos(id) ON DELETE CASCADE,
                    FOREIGN KEY (realizado_por_usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
                )
            """)
            print("Tabla 'historial_mantenimientos' creada.")
        else:
            print("Tabla 'historial_mantenimientos' ya existe.")

        conn.commit()
        print("Base de datos inicializada/verificada correctamente.")

    
    except sqlite3.Error as e:
        print(f"Error crítico durante inicialización/verificación de DB: {e}")
        # Considerar si relanzar o salir
        raise SystemExit(f"Fallo crítico de base de datos: {e}")
    except Exception as e:
         print(f"Error inesperado durante inicialización DB: {e}")
         raise SystemExit(f"Fallo inesperado de base de datos: {e}")
    finally:
        if conn:
             conn.close()
             # print("Conexión de inicialización cerrada.")
def delete_multiple_equipment_by_ids(equipment_ids, current_user_id):
    """Elimina múltiples equipos por sus IDs."""
    if not equipment_ids: return 0

    conn = None
    deleted_count = 0
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Eliminar en lotes para evitar límites de placeholders
        batch_size = 500
        for i in range(0, len(equipment_ids), batch_size):
            batch_ids = equipment_ids[i : i + batch_size]
            placeholders = ','.join('?' * len(batch_ids))
            sql_delete = f"DELETE FROM equipos WHERE id IN ({placeholders})"
            cursor.execute(sql_delete, batch_ids)
            deleted_count += cursor.rowcount
        
        conn.commit()
        return deleted_count
    except sqlite3.Error as e:
        print(f"DB Error delete_multiple_equipment_by_ids: {e}")
        if conn: conn.rollback()
        return 0
    except Exception as e:
        print(f"Error inesperado delete_multiple_equipment_by_ids: {e}")
        traceback.print_exc()
        if conn: conn.rollback()
        return 0
    finally:
        if conn: conn.close()

def update_multiple_equipment_fields(equipment_ids, updates_data):
    """
    Actualiza campos comunes para múltiples equipos.
    `updates_data` es un diccionario con {campo: nuevo_valor}.
    """
    if not equipment_ids or not updates_data: return 0, ["No hay IDs o datos para actualizar."]

    conn = None
    updated_count = 0
    errors = []
    
    # Mapeo de campos a la forma en que deben ser manejados (encriptados/no)
    updatable_fields_info = {
        'estatus': {'encrypted': False},
        'departamento': {'encrypted': False}, # Departamento no encriptado
        'sede': {'encrypted': False}, # Sede no encriptada
        'observacion': {'encrypted': True} # Observación encriptada
        # Añade más campos aquí si son comunes y no únicos
    }

    set_clauses = []
    update_values = []

    try:
        for field, value in updates_data.items():
            if field in updatable_fields_info:
                processed_value = value
                if updatable_fields_info[field]['encrypted']:
                    processed_value = encrypt_data(value)
                
                set_clauses.append(f"{field} = ?")
                update_values.append(processed_value)
            else:
                errors.append(f"Campo '{field}' no permitido para actualización masiva.")
        
        if not set_clauses: return 0, errors + ["No hay campos válidos para actualizar."]

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Actualizar en lotes para evitar límites de placeholders
        batch_size = 500
        for i in range(0, len(equipment_ids), batch_size):
            batch_ids = equipment_ids[i : i + batch_size]
            placeholders = ','.join('?' * len(batch_ids))
            
            sql_update = f"UPDATE equipos SET {', '.join(set_clauses)} WHERE id IN ({placeholders})"
            
            try:
                cursor.execute(sql_update, update_values + batch_ids) # Valores + IDs
                updated_count += cursor.rowcount
            except sqlite3.Error as e:
                errors.append(f"Error DB al actualizar lote de IDs {batch_ids[0]}...: {e}")
                
        conn.commit()
        return updated_count, errors

    except sqlite3.Error as e:
        print(f"DB Error update_multiple_equipment_fields: {e}")
        if conn: conn.rollback()
        return 0, errors + [f"Error de base de datos: {e}"]
    except Exception as e:
        print(f"Error inesperado update_multiple_equipment_fields: {e}")
        traceback.print_exc()
        if conn: conn.rollback()
        return 0, errors + [f"Error inesperado: {e}"]
    finally:
        if conn: conn.close()

# --- Funciones de Autenticación (Compatibles) ---
def check_user_credentials(username, password):
    """Verifica usuario y contraseña. Devuelve (rol, id) si es válido, None si no."""
    sql = "SELECT id, password_hash, role FROM usuarios WHERE username = ?"
    conn = None
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row # Aplicar Row factory aquí
        cursor = conn.cursor()
        cursor.execute(sql, (username,))
        user_data = cursor.fetchone()
        if user_data and check_password_hash(user_data['password_hash'], password):
            # print(f"Usuario '{username}' autenticado con rol '{user_data['role']}'.") # Debug
            return (user_data['role'], user_data['id']) # Devolver tupla
        else:
            # print(f"Fallo de autenticación para usuario '{username}'.") # Debug
            return None
    except sqlite3.Error as e:
        print(f"DB Error (check_user_credentials) para '{username}': {e}")
        return None
    finally:
        if conn: conn.close()

# --- Funciones CRUD Equipos (Adaptadas/Revisadas para compatibilidad y claridad) ---

def get_all_equipment():
    """Obtiene todos los equipos, desencriptando campos necesarios."""
    sql = "SELECT * FROM equipos ORDER BY id"
    conn = None
    equipos_list = []
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory # Usar dict_factory para obtener diccionarios
        cursor = conn.cursor()
        cursor.execute(sql)
        equipos_raw = cursor.fetchall()

        if not equipos_raw: return [] # Lista vacía si no hay equipos

        # print(f"get_all_equipment: Procesando {len(equipos_raw)} equipos crudos...") # Debug
        encrypted_fields = ['serial', 'asignado_a', 'observacion']
        for equipo_dict in equipos_raw:
            # No es necesario copiar con dict(equipo_dict) si dict_factory ya crea dicts
            processed_equipo = equipo_dict
            # Desencriptar
            for field in encrypted_fields:
                if field in processed_equipo and processed_equipo[field] is not None:
                    processed_equipo[field] = decrypt_data(processed_equipo[field]) # Actualizar in-place

            # Formatear fechas si es necesario (str() es seguro)
            for date_field in ['ultimo_mantenimiento', 'proximo_mantenimiento', 'fecha_registro']:
                 if processed_equipo.get(date_field):
                      processed_equipo[date_field] = str(processed_equipo[date_field])

            equipos_list.append(processed_equipo)

        # print(f"get_all_equipment: Devolviendo {len(equipos_list)} equipos procesados.") # Debug
        return equipos_list
    except sqlite3.Error as e:
        print(f"DB Error (get_all_equipment): {e}")
        return [] # Devolver lista vacía en caso de error SQL
    except Exception as e:
         print(f"Error inesperado en get_all_equipment (posiblemente desencriptación): {e}")
         import traceback
         traceback.print_exc() # Imprimir stack trace completo para depurar
         return []
    finally:
        if conn: conn.close()

def _is_serial_duplicate(conn, serial_plaintext, current_equipment_id=None):
    """
    Verifica si un serial (en texto plano) ya existe en la base de datos,
    excluyendo opcionalmente el equipo actual que se está editando.
    Devuelve True si es duplicado, False si no.
    """
    cursor = conn.cursor()
    # Necesitamos obtener todos los seriales encriptados y desencriptarlos para comparar.
    # Esto puede ser costoso en tablas muy grandes.
    sql_select_serials = "SELECT id, serial FROM equipos"
    cursor.execute(sql_select_serials)
    
    for row_id, serial_blob in cursor.fetchall():
        if current_equipment_id is not None and row_id == current_equipment_id:
            continue # Omitir el propio equipo que se está editando

        decrypted_existing_serial = decrypt_data(serial_blob)
        if decrypted_existing_serial == serial_plaintext:
            print(f"Error: Serial '{serial_plaintext}' ya existe para el equipo ID {row_id}.")
            return True # Duplicado encontrado
    return False # No es duplicado

def add_new_equipment(data):
    """
    Agrega un nuevo equipo. Verifica unicidad del serial desencriptado.
    """
    conn = None
    data_to_insert = {}
    valid_keys_for_defaults = ['tipo_equipo', 'marca', 'modelo', 'asignado_a', 
                               'departamento', 'sede', 'estatus', 
                               'ultimo_mantenimiento', 'proximo_mantenimiento', 'observacion']
    encrypted_fields = ['serial', 'asignado_a', 'observacion']

    try:
        raw_serial = data.get('serial')
        if not raw_serial or not str(raw_serial).strip():
            raise ValueError("El campo Serial es obligatorio y no puede estar vacío.")
        
        serial_plaintext_to_check = str(raw_serial).strip()
        
        # --- ABRIR CONEXIÓN ANTES PARA CHEQUEO DE DUPLICADO ---
        conn = get_db_connection()
        if _is_serial_duplicate(conn, serial_plaintext_to_check):
            # Devolver un error específico o un código que el backend handler pueda interpretar
            # Para mantener la devolución booleana simple por ahora, devolvemos False.
            # Idealmente, se lanzaría una excepción personalizada o se devolvería un objeto de resultado.
            # Para que el mensaje específico llegue al frontend, backend_handler.py necesitaría
            # saber que este 'False' es por 'duplicate_serial'.
            raise sqlite3.IntegrityError("DUPLICATE_SERIAL_CUSTOM_ERROR") # Simular error para que el except lo capture

        # Si no es duplicado, proceder
        data_to_insert['serial'] = serial_plaintext_to_check # Guardar texto plano para encriptar

        for key in valid_keys_for_defaults:
            # ... (lógica de defaults como antes, pero SIN el default para serial) ...
            value = data.get(key)
            if isinstance(value, str): value = value.strip()
            if key == 'marca' and (value is None or value == ''): value = "SIN MARCA"
            # ... otros defaults ...
            if value is not None: data_to_insert[key] = value
        
        if not data_to_insert.get('tipo_equipo'): raise ValueError("Tipo de equipo es obligatorio.")

        for field in encrypted_fields:
            if field in data_to_insert and data_to_insert[field] is not None:
                value_to_encrypt = data_to_insert[field]
                encrypted_value = encrypt_data(value_to_encrypt)
                if encrypted_value is None:
                    raise ValueError(f"Fallo al encriptar el campo '{field}' con valor '{value_to_encrypt}'.")
                data_to_insert[field] = encrypted_value
            elif field == 'serial' and (field not in data_to_insert or data_to_insert[field] is None):
                 raise ValueError("Error crítico: El serial se volvió nulo antes de la encriptación final.")

        columnas = list(data_to_insert.keys())
        placeholders = ', '.join(['?'] * len(columnas))
        valores_tupla = tuple(data_to_insert[col] for col in columnas)
        sql = f"INSERT INTO equipos ({', '.join(columnas)}) VALUES ({placeholders})"
        
        print(f"SQL Insert: {sql}") 
        print(f"Valores Tupla (para serial, es el blob encriptado): {valores_tupla}") 

        # La conexión ya está abierta desde el chequeo de duplicados
        cursor = conn.cursor()
        cursor.execute(sql, valores_tupla)
        conn.commit()
        print(f"Equipo agregado con ID: {cursor.lastrowid}")
        return True

    except sqlite3.IntegrityError as e:
        # Esto ahora capturaría el DUPLICATE_SERIAL_CUSTOM_ERROR o errores de otras constraints
        error_message = str(e).lower()
        if "duplicate_serial_custom_error" in error_message or "unique constraint failed" in error_message : # Incluir la constraint original por si acaso
            print(f"DB Error (add - Integrity): Serial duplicado. Error: {e}")
            original_serial_for_log = data.get('serial', "DESCONOCIDO")
            print(f"  Serial original que causó el duplicado: '{original_serial_for_log}'")
            return False 
        else:
            print(f"DB Error (add - Integrity no manejado específicamente para serial): {e}")
            return False
    except sqlite3.Error as e:
        print(f"DB Error (add): {e}")
        return False
    except ValueError as e: # Errores de validación o encriptación
        print(f"Error de Datos (add): {e}")
        return False
    except Exception as e:
        print(f"Error inesperado (add): {e}")
        import traceback; traceback.print_exc()
        return False
    finally:
        if conn: conn.close()

def get_maintenance_history_for_equipment(equipo_id):
    """Obtiene el historial de mantenimientos para un equipo específico."""
    conn = None
    historial_list = []
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory # Para obtener diccionarios
        cursor = conn.cursor()
        # Opcional: Unir con tabla usuarios para obtener nombre de quien registró
        sql = """
            SELECT hm.id, hm.equipo_id, hm.fecha_realizado, hm.tipo_mantenimiento, hm.descripcion, 
                   hm.fecha_registro_historial, u.username as realizado_por_username
            FROM historial_mantenimientos hm
            LEFT JOIN usuarios u ON hm.realizado_por_usuario_id = u.id
            WHERE hm.equipo_id = ?
            ORDER BY hm.fecha_realizado DESC, hm.id DESC
        """
        cursor.execute(sql, (equipo_id,))
        raw_historial = cursor.fetchall()

        for item_dict in raw_historial:
            if 'descripcion' in item_dict and item_dict['descripcion'] is not None:
                item_dict['descripcion'] = decrypt_data(item_dict['descripcion'])
            # Formatear fechas si es necesario
            for date_field in ['fecha_realizado', 'fecha_registro_historial']:
                 if item_dict.get(date_field):
                      item_dict[date_field] = str(item_dict[date_field])
            historial_list.append(item_dict)
            
        return historial_list
    except sqlite3.Error as e:
        print(f"DB Error en get_maintenance_history_for_equipment: {e}")
        return []
    except Exception as e:
        print(f"Error general en get_maintenance_history_for_equipment: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        if conn:
            conn.close()
            
def add_maintenance(equipo_id, fecha_realizado_str, tipo_mantenimiento, descripcion, proximo_en_meses, usuario_id=None):
    """
    Registra un mantenimiento y actualiza las fechas en la tabla equipos.
    Devuelve (True, "Mensaje de éxito") o (False, "Mensaje de error").
    """
    conn = None
    try:
        # Validación de datos de entrada
        if not equipo_id or not fecha_realizado_str:
            return False, "ID de equipo y fecha de realización son obligatorios."
        
        try:
            fecha_realizado_dt = datetime.strptime(fecha_realizado_str, '%Y-%m-%d').date()
        except ValueError:
            return False, "Formato de fecha de realización inválido. Use YYYY-MM-DD."

        if proximo_en_meses is not None:
            try:
                proximo_en_meses_int = int(proximo_en_meses)
                if proximo_en_meses_int <= 0:
                    # Permitir 0 si significa "no programar próximo", o tratarlo como error
                    # Aquí lo tomaremos como que no se programa el siguiente si es 0 o negativo
                    proximo_en_meses_int = None 
            except ValueError:
                return False, "Valor para 'próximo en meses' debe ser un número."
        else: # Si es None explícitamente
            proximo_en_meses_int = None


        descripcion_encriptada = encrypt_data(descripcion) if descripcion else None

        conn = get_db_connection()
        cursor = conn.cursor()

        # Iniciar transacción
        cursor.execute("BEGIN TRANSACTION")

        # 1. Insertar en historial_mantenimientos
        sql_historial = """
            INSERT INTO historial_mantenimientos 
            (equipo_id, fecha_realizado, tipo_mantenimiento, descripcion, realizado_por_usuario_id)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql_historial, (
            equipo_id, 
            fecha_realizado_dt.isoformat(), 
            tipo_mantenimiento,
            descripcion_encriptada,
            usuario_id
        ))
        
        # 2. Actualizar tabla equipos
        nueva_fecha_proximo_mantenimiento_iso = None
        if proximo_en_meses_int is not None and proximo_en_meses_int > 0 :
            nueva_fecha_proximo_mantenimiento_dt = fecha_realizado_dt + relativedelta(months=proximo_en_meses_int)
            nueva_fecha_proximo_mantenimiento_iso = nueva_fecha_proximo_mantenimiento_dt.isoformat()

        sql_update_equipo = """
            UPDATE equipos 
            SET ultimo_mantenimiento = ?, proximo_mantenimiento = ?
            WHERE id = ?
        """
        cursor.execute(sql_update_equipo, (
            fecha_realizado_dt.isoformat(),
            nueva_fecha_proximo_mantenimiento_iso, # Puede ser None
            equipo_id
        ))

        conn.commit()
        return True, "Mantenimiento registrado y equipo actualizado exitosamente."

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        print(f"DB Error en add_maintenance: {e}")
        return False, f"Error de base de datos: {e}"
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error general en add_maintenance: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error inesperado: {e}"
    finally:
        if conn:
            conn.close()

def get_distinct_sedes():
    """Obtiene valores únicos para el campo sede."""
    # Reutilizar get_distinct_field_values si 'sede' no es encriptado
    return get_distinct_field_values('sede')

def update_existing_equipment(equipment_id, data):
    """Actualiza un equipo existente."""
    conn = None
    # --- Preparación de Datos ---
    updates_dict = {}
    valid_keys = ['tipo_equipo', 'marca', 'modelo', 'serial', 'asignado_a', 'departamento', 'sede', 'estatus', 'ultimo_mantenimiento', 'proximo_mantenimiento', 'observacion']
    encrypted_fields = ['serial', 'asignado_a', 'observacion']

    try:
        raw_serial_update = data.get('serial')
        if raw_serial_update is not None: # Solo verificar duplicado si el serial está siendo modificado
            if not str(raw_serial_update).strip():
                raise ValueError("El campo Serial es obligatorio y no puede estar vacío al actualizar.")
            
            serial_plaintext_to_check = str(raw_serial_update).strip()
            
            conn = get_db_connection()
            if _is_serial_duplicate(conn, serial_plaintext_to_check, current_equipment_id=equipment_id):
                raise sqlite3.IntegrityError("DUPLICATE_SERIAL_CUSTOM_ERROR_UPDATE")
            
            updates_dict['serial'] = serial_plaintext_to_check # Guardar texto plano para encriptar
        
        # Procesar OTROS campos para la actualización
        for key in data: # Iterar sobre las claves que vienen en 'data'
            if key == 'serial': continue # Ya manejamos el serial
            if key in ['tipo_equipo', 'marca', 'modelo', 'asignado_a', 'departamento', 'sede', 'estatus', 'ultimo_mantenimiento', 'proximo_mantenimiento', 'observacion']:
                value = data[key]
                if isinstance(value, str): value = value.strip()
                # Aplicar defaults si es necesario (ej. si se envía vacío un campo que no puede serlo)
                if key == 'marca' and (value is None or value == ''): value = "SIN MARCA"
                # ... otros defaults ...
                updates_dict[key] = value # Añadir al diccionario de updates

        if not updates_dict: # Si no hay nada que actualizar (ej. solo se envió el ID)
            print("Advertencia (update_existing_equipment): No hay campos para actualizar.")
            return True # O False si se considera un fallo no tener nada que actualizar

        # Encriptar los campos necesarios que están en updates_dict
        for field in encrypted_fields:
            if field in updates_dict and updates_dict[field] is not None:
                value_to_encrypt = updates_dict[field]
                encrypted_value = encrypt_data(value_to_encrypt)
                if encrypted_value is None:
                    raise ValueError(f"Fallo al encriptar el campo '{field}' con valor '{value_to_encrypt}' en update.")
                updates_dict[field] = encrypted_value
        
        if not updates_dict: # Revisar de nuevo por si solo había campos que se volvieron None tras encriptar algo
            return False 

        set_clauses = [f"{col} = ?" for col in updates_dict.keys()]
        valores_tupla = tuple(updates_dict.values()) + (equipment_id,)
        sql = f"UPDATE equipos SET {', '.join(set_clauses)} WHERE id = ?"

        print(f"SQL Update: {sql}")
        print(f"Valores Tupla Update: {valores_tupla}")

        if not conn: # Si la conexión no se abrió para el chequeo de serial
            conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, valores_tupla)
        conn.commit()

        return cursor.rowcount > 0

    except sqlite3.IntegrityError as e:
        error_message = str(e).lower()
        if "duplicate_serial_custom_error_update" in error_message or "unique constraint failed" in error_message:
            print(f"DB Error (update - Integrity): Serial duplicado. Error: {e}")
            original_serial_for_log = data.get('serial', "DESCONOCIDO")
            print(f"  Serial original que causó el duplicado en update: '{original_serial_for_log}'")
            return False
        else:
            print(f"DB Error (update - Integrity no manejado): {e}")
            return False
    except sqlite3.Error as e:
        print(f"DB Error (update): {e}")
        return False
    except ValueError as e: # Errores de validación o encriptación
        print(f"Error de Datos (update): {e}")
        return False
    except Exception as e:
        print(f"Error inesperado (update): {e}")
        import traceback; traceback.print_exc()
        return False
    finally:
        if conn: conn.close()


def delete_equipment_by_id(equipment_id):
    """Elimina un equipo por su ID."""
    # print(f"Intentando eliminar equipo ID: {equipment_id}") # Debug
    sql = "DELETE FROM equipos WHERE id = ?"
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (equipment_id,))
        conn.commit()
        deleted_rows = cursor.rowcount
        if deleted_rows > 0:
            # print(f"Equipo ID {equipment_id} eliminado correctamente.") # Debug
            return True
        else:
            # print(f"Advertencia: No se encontró equipo con ID {equipment_id} para eliminar.") # Debug
            return False # No se borró nada
    except sqlite3.Error as e:
        print(f"DB Error (delete_equipment_by_id) para ID {equipment_id}: {e}")
        return False
    finally:
        if conn: conn.close()


def get_equipment_by_id(equipment_id):
    """Obtiene los detalles de un equipo específico por su ID, desencriptando."""
    sql = "SELECT * FROM equipos WHERE id = ?"
    conn = None
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory # Usar dict_factory
        cursor = conn.cursor()
        cursor.execute(sql, (equipment_id,))
        equipment = cursor.fetchone() # Obtiene un diccionario o None

        if equipment:
            processed_equipment = equipment
            encrypted_fields = ['serial', 'asignado_a', 'observacion']
            for field in encrypted_fields:
                if field in processed_equipment and processed_equipment[field] is not None:
                     processed_equipment[field] = decrypt_data(processed_equipment[field])

            for date_field in ['ultimo_mantenimiento', 'proximo_mantenimiento', 'fecha_registro']:
                 if processed_equipment.get(date_field):
                      processed_equipment[date_field] = str(processed_equipment[date_field])
            return processed_equipment
        else:
            # print(f"No se encontró equipo con ID {equipment_id}") # Debug
            return None
    except sqlite3.Error as e:
        print(f"Error DB get ID {equipment_id}: {e}")
        return None
    except Exception as e:
         print(f"Error inesperado en get_equipment_by_id (posiblemente desencriptación) para ID {equipment_id}: {e}")
         import traceback; traceback.print_exc()
         return None
    finally:
        if conn: conn.close()


# --- Funciones CRUD Usuarios (Compatibles) ---

def get_all_users():
    """Obtiene todos los usuarios (ID, Username, Rol). SIN CONTRASEÑA."""
    sql = "SELECT id, username, role FROM usuarios ORDER BY username"
    conn = None
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory # Usar dict_factory
        cursor = conn.cursor()
        cursor.execute(sql)
        users = cursor.fetchall() # Lista de diccionarios
        return users if users else []
    except sqlite3.Error as e:
        print(f"DB Error (get_all_users): {e}")
        return []
    finally:
        if conn: conn.close()

def add_new_user(username, password, role):
    """Agrega un nuevo usuario. Hashea la contraseña."""
    if not username or not password or not role:
        print("Error: Username, password, y role son requeridos para añadir usuario.")
        return False, "Datos incompletos." # Devolver False y mensaje
    role = role.lower().strip()
    username = username.strip()
    if role not in ['admin', 'manager', 'read_only']:
        print(f"Error: Rol inválido '{role}'.")
        return False, "Rol inválido." # Devolver False y mensaje

    password_hash = generate_password_hash(password)
    sql = "INSERT INTO usuarios (username, password_hash, role) VALUES (?, ?, ?)"
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (username, password_hash, role))
        conn.commit()
        print(f"Usuario '{username}' añadido con rol '{role}'.")
        return True, f"Usuario '{username}' creado." # Devolver True y mensaje
    except sqlite3.IntegrityError:
        msg = f"El nombre de usuario '{username}' ya existe."
        print(f"DB Error (add_new_user): {msg}")
        return False, msg # Devolver False y mensaje
    except sqlite3.Error as e:
        print(f"DB Error (add_new_user): {e}")
        return False, f"Error de base de datos: {e}" # Devolver False y mensaje
    finally:
        if conn: conn.close()


def update_user_role(user_id, new_role):
    """Actualiza el rol de un usuario existente."""
    new_role = new_role.lower().strip()
    if new_role not in ['admin', 'manager', 'read_only']:
        print(f"Error: Rol inválido '{new_role}'.")
        return False, "Rol inválido."

    conn = None
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory # Necesario para leer conteo/rol actual
        cursor = conn.cursor()

        # Medida de seguridad: No permitir cambiar el último admin a otro rol
        if new_role != 'admin':
            cursor.execute("SELECT role FROM usuarios WHERE id = ?", (user_id,))
            current_user_data = cursor.fetchone()
            if not current_user_data:
                 return False, "Usuario no encontrado."
            if current_user_data['role'] == 'admin':
                cursor.execute("SELECT COUNT(*) as admin_count FROM usuarios WHERE role = 'admin'")
                admin_count = cursor.fetchone()['admin_count']
                if admin_count <= 1:
                    msg = "No se puede cambiar el rol del último administrador."
                    print(f"Error (update_user_role): {msg}")
                    return False, msg

        # Proceder a actualizar
        sql_update = "UPDATE usuarios SET role = ? WHERE id = ?"
        cursor.execute(sql_update, (new_role, user_id))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"Rol del usuario ID {user_id} actualizado a '{new_role}'.")
            return True, "Rol actualizado."
        else:
            # Esto no debería pasar si la verificación inicial tuvo éxito
            print(f"Advertencia: No se encontró usuario con ID {user_id} para actualizar rol (inesperado).")
            return False, "Usuario no encontrado para actualizar."

    except sqlite3.Error as e:
        print(f"DB Error (update_user_role): {e}")
        return False, f"Error de base de datos: {e}"
    finally:
        if conn: conn.close()
def get_count_equipos_por_departamento(sede_filtrar=None):
    """
    Obtiene el conteo de equipos agrupados por departamento.
    Si se proporciona sede_filtrar, filtra por esa sede.
    Maneja campos encriptados y no encriptados.
    """
    conn = None
    counts = {}
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_sql = "SELECT COALESCE(NULLIF(TRIM(departamento), ''), 'No Asignado') as item, COUNT(*) as count FROM equipos"
        params = []

        if sede_filtrar and sede_filtrar.strip() != "":
            # Asumiendo que 'sede' NO está encriptado. Si lo estuviera, la lógica es más compleja.
            base_sql += " WHERE LOWER(TRIM(sede)) = LOWER(?)" # Comparación insensible a mayúsculas/minúsculas
            params.append(sede_filtrar.strip())
        
        base_sql += " GROUP BY item ORDER BY count DESC"
        
        cursor.execute(base_sql, params)
        
        for row in cursor.fetchall():
            counts[row[0]] = row[1]
        
        return [{"name": name, "value": value} for name, value in counts.items()]

    except sqlite3.Error as e:
        print(f"Error DB en get_count_equipos_por_departamento (sede: {sede_filtrar}): {e}")
        return []
    except Exception as e:
        print(f"Error general en get_count_equipos_por_departamento: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        if conn:
            conn.close()

def reset_user_password(user_id, new_password):
    """Establece una nueva contraseña para un usuario (hasheada)."""
    if not new_password:
        print("Error: La nueva contraseña no puede estar vacía.")
        return False, "Contraseña vacía."

    new_password_hash = generate_password_hash(new_password)
    sql = "UPDATE usuarios SET password_hash = ? WHERE id = ?"
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (new_password_hash, user_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Contraseña para usuario ID {user_id} reseteada.")
            return True, "Contraseña actualizada."
        else:
            print(f"Advertencia: No se encontró usuario con ID {user_id} para resetear contraseña.")
            return False, "Usuario no encontrado."
    except sqlite3.Error as e:
        print(f"DB Error (reset_user_password): {e}")
        return False, f"Error de base de datos: {e}"
    finally:
        if conn: conn.close()


def delete_user_by_id(user_id_to_delete, current_admin_id):
    """Elimina un usuario por ID, con chequeos de seguridad."""
    if user_id_to_delete == current_admin_id:
        msg = "Un administrador no puede eliminarse a sí mismo."
        print(f"Error (delete_user_by_id): {msg}")
        return False, msg # No permitimos auto-eliminación

    conn = None
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory # Necesario para leer rol
        cursor = conn.cursor()

        # Verificar si existe y si es el último admin
        cursor.execute("SELECT role FROM usuarios WHERE id = ?", (user_id_to_delete,))
        user_to_delete = cursor.fetchone()
        if not user_to_delete:
             msg = f"Usuario con ID {user_id_to_delete} no encontrado para eliminar."
             print(f"Error (delete_user_by_id): {msg}")
             return False, msg

        if user_to_delete['role'] == 'admin':
            cursor.execute("SELECT COUNT(*) as admin_count FROM usuarios WHERE role = 'admin'")
            admin_count = cursor.fetchone()['admin_count']
            if admin_count <= 1:
                msg = "No se puede eliminar al último administrador."
                print(f"Error (delete_user_by_id): {msg}")
                return False, msg

        # Proceder a eliminar
        sql_delete = "DELETE FROM usuarios WHERE id = ?"
        cursor.execute(sql_delete, (user_id_to_delete,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"Usuario ID {user_id_to_delete} eliminado correctamente.")
            return True, "Usuario eliminado."
        else:
            # No debería ocurrir si la verificación inicial tuvo éxito
            msg = f"Error inesperado: No se pudo eliminar el usuario ID {user_id_to_delete} después de las verificaciones."
            print(f"Error (delete_user_by_id): {msg}")
            return False, msg

    except sqlite3.Error as e:
        print(f"DB Error (delete_user_by_id): {e}")
        # Considerar rollback si la conexión sigue activa
        # if conn: conn.rollback()
        return False, f"Error de base de datos: {e}"
    finally:
        if conn: conn.close()


# --- Funciones de Utilidad y Bulk (Compatibles, pero revisar rendimiento en Win7 32) ---

# Nota: Las funciones como apply_default_values_to_existing_equipment,
# get_distinct..., bulk_insert..., delete_duplicate... son complejas.
# Aunque sintácticamente compatibles, su rendimiento en un sistema antiguo
# con muchos datos podría ser lento debido a las operaciones de lectura/escritura
# y especialmente la desencriptación repetida. No se modifican aquí por compatibilidad,
# pero tenlo en cuenta si la aplicación se vuelve lenta.

def apply_default_values_to_existing_equipment():
    """Chequea y aplica valores default a equipos existentes si están vacíos/nulos."""
    print("Iniciando chequeo/actualización de defaults para equipos existentes...")
    conn = None; updated_count = 0; error_count = 0
    try:
        conn = get_db_connection()
        # Usar row_factory de bajo nivel para obtener tuplas (id, serial_blob, marca, modelo)
        # Es más eficiente para este tipo de bucle grande
        cursor_read = conn.cursor()
        cursor_update = conn.cursor() # Cursor separado para updates

        cursor_read.execute("SELECT id, serial, marca, modelo FROM equipos")

        conn.execute("BEGIN TRANSACTION") # Iniciar transacción para updates

        while True:
            rows = cursor_read.fetchmany(100) # Procesar en lotes de 100
            if not rows: break # Salir si no hay más filas

            print(f"  Procesando lote de {len(rows)} equipos...")
            for row in rows:
                equipo_id, serial_blob, marca, modelo = row
                updates_needed = {}
                try:
                    if marca is None or not marca.strip(): updates_needed['marca'] = "SIN MARCA"
                    if modelo is None or not modelo.strip(): updates_needed['modelo'] = "SIN MODELO"

                except Exception as prep_e:
                    print(f"  ERROR Preparando datos para ID {equipo_id}: {prep_e}")
                    error_count += 1
                    continue # Saltar al siguiente equipo en el lote

                if updates_needed:
                    set_clauses = [f"{key} = ?" for key in updates_needed.keys()]
                    ordered_params = list(updates_needed.values()) + [equipo_id]
                    sql_update = f"UPDATE equipos SET {', '.join(set_clauses)} WHERE id = ?"
                    try:
                        cursor_update.execute(sql_update, ordered_params)
                        updated_count += 1
                    except sqlite3.Error as ue: # Captura IntegrityError también
                        print(f"  ERROR DB Update ID {equipo_id}: {ue} (omitido)")
                        error_count += 1
                    except Exception as ex:
                        print(f"  ERROR Inesp. Update ID {equipo_id}: {ex} (omitido)")
                        error_count += 1

        # Commit final de la transacción
        print(f"Commit final para defaults...")
        conn.commit()
        print("Commit realizado.")

        print(f"Actualización de defaults completada.")
        print(f" - Equipos modificados: {updated_count}")
        print(f" - Errores encontrados (omitidos): {error_count}")

    except sqlite3.Error as e:
        print(f"Error DB masivo (lectura/conexión/transacción) en apply_defaults: {e}")
        if conn: conn.rollback() # Rollback si hubo error en la transacción
    except Exception as e:
        print(f"Error inesperado masivo en apply_defaults: {e}")
        import traceback; traceback.print_exc()
        if conn: conn.rollback()
    finally:
        if conn: conn.close()


def get_distinct_field_values(field_name):
    """Obtiene valores únicos y no vacíos/nulos para campos de TEXTO."""
    allowed_fields = ['marca', 'modelo', 'departamento', 'tipo_equipo', 'estatus', 'sede']
    if field_name not in allowed_fields:
        print(f"Error: Campo no permitido para get_distinct_field_values: {field_name}")
        return []

    sql = f"""
        SELECT DISTINCT LOWER(TRIM({field_name})) as valor
        FROM equipos
        WHERE {field_name} IS NOT NULL AND TRIM({field_name}) != '' AND LOWER(TRIM({field_name})) NOT LIKE 'sin %'
        ORDER BY valor
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        # Devolver la lista directamente como viene (minúsculas)
        distinct_values = [row[0] for row in cursor.fetchall()]
        # print(f"Obtenidos {len(distinct_values)} valores distintos para '{field_name}'.") # Debug
        return distinct_values
    except sqlite3.Error as e:
        print(f"Error DB obteniendo valores distintos para '{field_name}': {e}")
        return []
    finally:
        if conn: conn.close()


def get_distinct_decrypted_field_values(field_name):
    """Obtiene valores únicos y no vacíos/nulos para campos BLOB encriptados."""
    allowed_encrypted_fields = ['asignado_a', 'serial', 'observacion']
    if field_name not in allowed_encrypted_fields:
        print(f"Error: Campo no permitido para get_distinct_decrypted_field_values: {field_name}")
        return []

    sql = f"SELECT DISTINCT {field_name} FROM equipos WHERE {field_name} IS NOT NULL"
    conn = None
    decrypted_values = set()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        while True:
            blobs = cursor.fetchmany(500) # Procesar en lotes
            if not blobs: break
            for blob_tuple in blobs:
                decrypted = decrypt_data(blob_tuple[0])
                if decrypted and decrypted.strip() and not decrypted.startswith("##Error") and not decrypted.startswith("SIN_SERIAL") and decrypted != "SIN SERIAL":
                    decrypted_values.add(decrypted.strip()) # Añadir limpio al set

    except sqlite3.Error as e:
        print(f"Error DB obteniendo BLOBs para distinct decrypted '{field_name}': {e}")
        return [] # Devolver vacío en caso de error
    finally:
        if conn: conn.close()

    sorted_list = sorted(list(decrypted_values), key=str.lower) # Ordenar ignorando may/min
    # print(f"Obtenidos {len(sorted_list)} valores desencriptados distintos para '{field_name}'.") # Debug
    return sorted_list


def bulk_insert_equipment(equipment_data_list):
    """Inserta equipos en lote, validando y evitando duplicados."""
    conn = None
    results = { 'inserted': 0, 'db_ignored': 0, 'batch_ignored': 0, 'errors': [],
                'db_ignored_details': [], 'batch_ignored_details': [] }
    existing_serials_decrypted = set()
    processed_serials_in_this_batch_decrypted = set()
    encrypted_fields = ['serial', 'asignado_a', 'observacion']
    column_order = ['tipo_equipo', 'marca', 'modelo', 'serial', 'asignado_a',
                    'departamento', 'sede', 'estatus',
                    'ultimo_mantenimiento', 'proximo_mantenimiento', 'observacion']
    sql_insert = f"INSERT INTO equipos ({', '.join(column_order)}) VALUES ({', '.join(['?'] * len(column_order))})"

    print("\n--- Iniciando bulk_insert_equipment ---")
    try:
        conn = get_db_connection(); cursor = conn.cursor()
        # 1. Obtener seriales existentes (optimizado)
        print("  [Bulk] Obteniendo seriales existentes...");
        serials_to_decrypt = set()
        cursor.execute("SELECT DISTINCT serial FROM equipos WHERE serial IS NOT NULL")
        while True:
             blobs = cursor.fetchmany(500)
             if not blobs: break
             for blob_tuple in blobs: serials_to_decrypt.add(blob_tuple[0])

        for serial_blob in serials_to_decrypt:
            decrypted = decrypt_data(serial_blob)
            if decrypted and not decrypted.startswith("##Error"): existing_serials_decrypted.add(decrypted)
        print(f"  [Bulk] {len(existing_serials_decrypted)} seriales existentes únicos cargados.")

        # 2. Procesar e insertar lote
        conn.execute("BEGIN TRANSACTION")
        for index, equipo_data_original in enumerate(equipment_data_list):
            row_num_excel = index + 2 # Asumiendo cabecera en fila 1
            serial_for_check = None; processed_data = {}; skip_row = False; row_errors = []

            # --- Validación y Preparación por fila ---
            try:
                for col in column_order:
                    original_value = equipo_data_original.get(col); final_value = None
                    if isinstance(original_value, str): original_value = original_value.strip()

                    # Aplicar defaults y lógica
                    if col == 'tipo_equipo':
                        final_value = original_value if original_value else None
                        if not final_value: row_errors.append("Tipo Equipo obligatorio.")
                    elif col == 'serial':
                        final_value = original_value if original_value else "SIN SERIAL"
                        serial_for_check = final_value # Guardar antes de encriptar
                    elif col == 'marca': final_value = original_value if original_value else "SIN MARCA"
                    elif col == 'modelo': final_value = original_value if original_value else "SIN MODELO"
                    elif col == 'estatus': final_value = original_value if original_value else "Operativo"
                    elif col in ['ultimo_mantenimiento', 'proximo_mantenimiento']: final_value = original_value if original_value else None # Permitir None
                    else: final_value = original_value if original_value else None # Permitir None para otros
                    processed_data[col] = final_value

                if row_errors: raise ValueError("; ".join(row_errors))

                # --- Chequeo Duplicados (antes de encriptar) ---
                if serial_for_check in existing_serials_decrypted:
                    results['db_ignored'] += 1
                    results['db_ignored_details'].append(f"Fila {row_num_excel}: '{serial_for_check}' (ya en BD)")
                    skip_row = True
                elif serial_for_check in processed_serials_in_this_batch_decrypted:
                    results['batch_ignored'] += 1
                    results['batch_ignored_details'].append(f"Fila {row_num_excel}: '{serial_for_check}' (duplicado en archivo)")
                    skip_row = True

                if skip_row: continue # Saltar al siguiente item del loop

                # --- Encriptar ---
                for field in encrypted_fields:
                    if field in processed_data and processed_data[field] is not None:
                        encrypted = encrypt_data(processed_data[field])
                        if encrypted is None: raise ValueError(f"Error encriptando '{field}'")
                        processed_data[field] = encrypted

                # --- Insertar ---
                valores_tupla = tuple(processed_data.get(col) for col in column_order)
                cursor.execute(sql_insert, valores_tupla)
                results['inserted'] += 1
                processed_serials_in_this_batch_decrypted.add(serial_for_check)
                existing_serials_decrypted.add(serial_for_check) # Añadir a existentes para chequeos futuros en el mismo lote

            except ValueError as ve: # Capturar errores de validación/encriptación
                 results['errors'].append(f"Fila {row_num_excel} (Serial: {serial_for_check or 'N/A'}): {ve}")
            except sqlite3.Error as db_err: # Capturar error de DB en esta fila
                 results['errors'].append(f"Fila {row_num_excel} (Serial: {serial_for_check or 'N/A'}): Error DB Insert - {db_err}")
            except Exception as e_row: # Capturar cualquier otro error en la fila
                 results['errors'].append(f"Fila {row_num_excel} (Serial: {serial_for_check or 'N/A'}): Error Inesperado - {e_row}")

        # Fin del bucle, intentar commit
        print(f"\n[Bulk] Finalizado bucle. Insertados: {results['inserted']}, Ignorados BD: {results['db_ignored']}, Ignorados Lote: {results['batch_ignored']}, Otros Errores: {len(results['errors'])}")
        conn.commit()
        print("[Bulk] Commit OK.")

    except sqlite3.Error as e:
        print(f"Error general DB en bulk_insert (posiblemente en BEGIN, COMMIT, o lectura inicial): {e}")
        if conn: conn.rollback(); print("[Bulk] Rollback realizado por error general.")
        results['errors'].append(f"Error general de BD: {e}")
    except Exception as e:
        print(f"Error inesperado fuera del bucle principal en bulk_insert: {e}")
        import traceback; traceback.print_exc()
        if conn: conn.rollback(); print("[Bulk] Rollback realizado por error inesperado.")
        results['errors'].append(f"Error inesperado general: {e}")
    finally:
        if conn: conn.close()

    return results


def delete_duplicate_serial_equipment():
    """Encuentra y elimina seriales duplicados, conservando el ID más bajo."""
    print("\n--- Iniciando búsqueda y eliminación de seriales duplicados ---")
    conn = None; deleted_count = 0; serials_processed = {}; ids_to_delete = []
    try:
        conn = get_db_connection(); cursor = conn.cursor()
        print("  Obteniendo todos los IDs y seriales (ordenados por ID)...")
        cursor.execute("SELECT id, serial FROM equipos ORDER BY id ASC")

        while True:
             rows = cursor.fetchmany(500) # Procesar en lotes
             if not rows: break
             for equipo_id, serial_blob in rows:
                 try:
                     decrypted_serial = decrypt_data(serial_blob)
                     # Ignorar inválidos/defaults
                     if decrypted_serial is None or \
                        decrypted_serial.startswith("##Error") or \
                        decrypted_serial == "SIN SERIAL" or \
                        decrypted_serial.startswith("SIN_SERIAL_"):
                         continue
                     decrypted_serial = decrypted_serial.strip()
                     if not decrypted_serial: continue

                     # Marcar para eliminar si ya se vio
                     if decrypted_serial in serials_processed:
                         ids_to_delete.append(equipo_id)
                         # print(f"  ID {equipo_id}: Marcado (serial '{decrypted_serial}', conserva ID {serials_processed[decrypted_serial]})") # Debug
                     else:
                         serials_processed[decrypted_serial] = equipo_id
                 except Exception as e_row:
                     print(f"  ERROR procesando fila ID {equipo_id} para duplicados: {e_row}. Se omitirá.")

        # Ejecutar eliminación si hay IDs marcados
        if ids_to_delete:
            print(f"\n  Se marcaron {len(ids_to_delete)} equipos para eliminar por serial duplicado.")
            # --- ¡¡¡ELIMINAR LA CONFIRMACIÓN INTERACTIVA SI ESTO SE LLAMA DESDE UNA GUI!!! ---
            # confirm = input("  ¿Está ABSOLUTAMENTE SEGURO? (Escriba 'si' para confirmar): ")
            # if confirm.lower() == 'si':
            # --- Asumir confirmación si se llama a la función ---
            print("  Procediendo con la eliminación (¡SIN CONFIRMACIÓN INTERACTIVA!)...")
            try:
                conn.execute("BEGIN TRANSACTION")
                # Eliminar en lotes para evitar límites de placeholders
                batch_size = 500
                for i in range(0, len(ids_to_delete), batch_size):
                    batch_ids = ids_to_delete[i:i + batch_size]
                    placeholders = ','.join('?' * len(batch_ids))
                    sql_delete = f"DELETE FROM equipos WHERE id IN ({placeholders})"
                    cursor.execute(sql_delete, batch_ids)
                    deleted_count += cursor.rowcount
                conn.commit()
                print(f"  ¡ELIMINACIÓN COMPLETADA! Se eliminaron {deleted_count} registros.")
                if deleted_count != len(ids_to_delete):
                     print(f"  ADVERTENCIA: Se esperaba eliminar {len(ids_to_delete)} pero se eliminaron {deleted_count}.")
            except sqlite3.Error as e_del:
                print(f"  ERROR durante la eliminación: {e_del}. Intentando rollback...")
                if conn: conn.rollback(); print("  Rollback realizado.")
                deleted_count = 0 # Resetear contador si falló
            # else: # Corresponde al 'if confirm...' comentado
            #    print("  Eliminación cancelada.")
        else:
            print("  No se encontraron seriales duplicados válidos para eliminar.")

    except sqlite3.Error as e:
        print(f"Error de base de datos durante búsqueda/eliminación duplicados: {e}")
    except Exception as e:
        print(f"Error inesperado durante búsqueda/eliminación duplicados: {e}")
        import traceback; traceback.print_exc()
    finally:
        if conn: conn.close()
    return deleted_count

# --- Bloque de prueba (Opcional, ejecutar solo si __name__ == '__main__') ---
if __name__ == '__main__':
    print("\nEjecutando pruebas básicas del módulo database...")
    try:
        inicializar_db()
        print("\n--- Prueba de Conexión ---")
        conn_test = get_db_connection()
        print("Conexión exitosa.")
        conn_test.close()

        print("\n--- Prueba check_user_credentials (admin/admin) ---")
        result = check_user_credentials('admin', 'admin')
        if result: print(f"Login OK: Rol={result[0]}, ID={result[1]}")
        else: print("Login FAILED")
        result_fail = check_user_credentials('admin', 'wrongpass')
        if not result_fail: print("Login con pass incorrecta FAILED (esperado)")
        else: print("Login con pass incorrecta OK (¡ERROR!)")

        print("\n--- Prueba get_all_users ---")
        users = get_all_users()
        print(f"Usuarios encontrados: {len(users)}")
        # print(users) # Descomentar para ver detalles

        print("\n--- Prueba get_all_equipment (puede estar vacío) ---")
        equipos = get_all_equipment()
        print(f"Equipos encontrados: {len(equipos)}")
        # if equipos: print(equipos[0]) # Mostrar primer equipo si existe

        print("\n--- Pruebas de valores distintos (pueden estar vacíos) ---")
        marcas = get_distinct_field_values('marca')
        print(f"Marcas distintas: {marcas}")
        asignados = get_distinct_decrypted_field_values('asignado_a')
        print(f"Asignados distintos: {asignados}")

        print("\nPruebas finalizadas.")

    except Exception as e:
        print(f"\nError durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

def get_count_by_field(field_name, is_encrypted=False, sede_filtrar=None):
    conn = None
    counts = {}
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        base_query_select_count = f"SELECT COALESCE(NULLIF(TRIM({field_name}), ''), 'No Asignado') as item, COUNT(*) as count FROM equipos"
        group_by_clause = "GROUP BY item ORDER BY count DESC"
        
        where_conditions = []
        params = []

        # Condición para el campo principal (si es encriptado, se filtra después)
        if not is_encrypted:
            # Para campos no encriptados, nos aseguramos de que el campo en sí no sea nulo o vacío
            # antes de COALESCE, aunque COALESCE ya lo maneja.
            # Esto es más para asegurar que contamos solo registros con datos válidos en field_name
            # where_conditions.append(f"{field_name} IS NOT NULL AND TRIM({field_name}) != ''") # Opcional si COALESCE es suficiente
            pass


        # Añadir filtro de sede SIEMPRE que sede_filtrar esté presente
        if sede_filtrar and sede_filtrar.strip() != "":
            # Asumiendo que 'sede' NO está encriptado.
            where_conditions.append("LOWER(TRIM(sede)) = LOWER(?)")
            params.append(sede_filtrar.strip())

        # Construir la consulta final
        final_sql = base_query_select_count
        if where_conditions:
            final_sql += " WHERE " + " AND ".join(where_conditions)
        final_sql += " " + group_by_clause
        
        # Debug: Imprimir la consulta y parámetros
        print(f"  DB (get_count_by_field for '{field_name}', sede: '{sede_filtrar}'):")
        print(f"    SQL: {final_sql}")
        print(f"    PARAMS: {params}")

        if is_encrypted:
            # Para campos encriptados, la lógica de filtrado por sede DEBE OCURRIR ANTES de la desencriptación masiva.
            # La consulta base para obtener los blobs debe incluir el WHERE de sede.
            
            # Paso 1: Obtener los blobs del campo encriptado, YA FILTRADOS POR SEDE (si aplica)
            select_blobs_sql = f"SELECT {field_name} FROM equipos"
            if where_conditions: # Si hay filtro de sede (u otros futuros)
                 # Nota: Si field_name fuera 'sede' y is_encrypted, esto sería un problema.
                 # Pero para tipo_equipo/estatus (no encriptados) con filtro de sede, esto está bien.
                 # El problema es si field_name ES encriptado Y queremos filtrar por sede.
                 # La lógica aquí se complica si field_name es encriptado.
                 # Por ahora, tus campos tipo_equipo y estatus NO son encriptados.
                 # Si tipo_equipo o estatus FUERAN encriptados, necesitarías:
                 # 1. Leer TODOS los registros que cumplen el WHERE de sede.
                 # 2. Desencriptar el field_name de esos registros.
                 # 3. Agrupar y contar en Python.
                 # La implementación actual para is_encrypted no maneja bien el filtrado por OTRO campo (sede).
                 
                 # ***** CORRECCIÓN IMPORTANTE PARA is_encrypted CON FILTRO DE SEDE *****
                 # Si el campo a contar (field_name) es encriptado, Y se quiere filtrar por sede (no encriptada):
                select_blobs_sql += " WHERE " + " AND ".join(where_conditions) # Aplicar filtro de sede
            else: # Sin filtro de sede
                select_blobs_sql += f" WHERE {field_name} IS NOT NULL" # Solo tomar no nulos del campo encriptado

            print(f"    ENCRYPTED SQL for blobs: {select_blobs_sql}")
            print(f"    ENCRYPTED PARAMS for blobs: {params}")
            cursor.execute(select_blobs_sql, params) # Usar los mismos params (solo de sede)
            
            all_values_blob = [row[0] for row in cursor.fetchall()]
            
            temp_counts = {}
            for blob_value in all_values_blob:
                decrypted_val = decrypt_data(blob_value)
                # Usar 'No Asignado' si la desencriptación falla o es None/vacío
                val_to_count = "No Asignado" 
                if decrypted_val and not decrypted_val.startswith("##Error") and decrypted_val.strip():
                    val_to_count = decrypted_val.strip()
                temp_counts[val_to_count] = temp_counts.get(val_to_count, 0) + 1
            counts = temp_counts

        else: # Campos NO encriptados (tipo_equipo, estatus, departamento)
            cursor.execute(final_sql, params)
            for row in cursor.fetchall():
                counts[row[0]] = row[1] # row[0] es 'item', row[1] es 'count'
        
        return [{"name": str(name), "value": value} for name, value in counts.items()]

    except sqlite3.Error as e:
        print(f"Error DB en get_count_by_field para '{field_name}' (sede: {sede_filtrar}): {e}")
        return []
    except Exception as e:
        print(f"Error general en get_count_by_field para '{field_name}': {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        if conn:
            conn.close()
def count_equipment_for_sede(sede_filtrar=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM equipos"
        params = []
        if sede_filtrar and sede_filtrar.strip() != "":
            # Asumiendo que 'sede' NO está encriptado
            sql += " WHERE LOWER(TRIM(sede)) = LOWER(?)"
            params.append(sede_filtrar.strip())
        
        cursor.execute(sql, params)
        count = cursor.fetchone()[0]
        return count if count is not None else 0
    except sqlite3.Error as e:
        print(f"Error DB en count_equipment_for_sede (sede: {sede_filtrar}): {e}")
        return 0
    finally:
        if conn:
            conn.close()
            
def get_proximos_mantenimientos_count(days_ahead=30):
    """Cuenta equipos con próximo mantenimiento en los siguientes 'days_ahead' días."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # SQLite date functions: date('now') y date('now', '+X days')
        sql = """
            SELECT COUNT(*) 
            FROM equipos
            WHERE proximo_mantenimiento IS NOT NULL 
              AND proximo_mantenimiento != ''
              AND date(proximo_mantenimiento) >= date('now')
              AND date(proximo_mantenimiento) <= date('now', ?)
        """
        # El placeholder debe ser un string con los días
        cursor.execute(sql, (f'+{days_ahead} days',))
        count = cursor.fetchone()[0]
        return count if count is not None else 0
    except sqlite3.Error as e:
        print(f"Error DB en get_proximos_mantenimientos_count: {e}")
        return 0
    finally:
        if conn:
            conn.close()

def get_total_equipment_count():
    """Obtiene el número total de equipos."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM equipos")
        count = cursor.fetchone()[0]
        return count if count is not None else 0
    except sqlite3.Error as e:
        print(f"Error DB en get_total_equipment_count: {e}")
        return 0
    finally:
        if conn:
            conn.close()

def get_total_users_count():
    """Obtiene el número total de usuarios."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        count = cursor.fetchone()[0]
        return count if count is not None else 0
    except sqlite3.Error as e:
        print(f"Error DB en get_total_users_count: {e}")
        return 0
    finally:
        if conn:
            conn.close()