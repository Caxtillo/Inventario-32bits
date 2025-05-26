# cargar_datos_ejemplo_v3.py
import sqlite3
import os
import sys
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
import traceback

# --- ¡¡¡IMPORTANTE!!! ---
ENCRYPTION_KEY = b'9pm2VMj7Vtx5J9bHCzhgq8km3b7M3PkL1C2VlhczR6c=' # <<< ¡TU CLAVE!

DATABASE_FILENAME = "inventario_local.db"

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except AttributeError: base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

DB_PATH = resource_path(DATABASE_FILENAME)

try:
    cipher_suite = Fernet(ENCRYPTION_KEY)
except ValueError as e:
    print(f"ERROR CRÍTICO: Clave inválida: {e}")
    sys.exit("Clave inválida. Copia la correcta de database.py.")

def encrypt_data(data_to_encrypt):
    if data_to_encrypt is None or (isinstance(data_to_encrypt, str) and not data_to_encrypt.strip()):
        return None
    return cipher_suite.encrypt(str(data_to_encrypt).encode('utf-8'))

# --- DATOS DE EJEMPLO ---
nombres_asignados = [
    "Ana Pérez", "Luis García", "María Rodríguez", "Carlos Sánchez", "Laura Gómez", 
    "Juan Martínez", "Sofía López", "Pedro Hernández", "Elena Torres", "Miguel Vargas",
    "Claudia Bravo", "Ricardo Núñez", "Verónica Soto", "Esteban Paredes", "Isidora Díaz"
]
departamentos = [
    "Recursos Humanos", "Finanzas", "Tecnología", "Marketing", "Operaciones", 
    "Ventas", "Legal", "Atención al Cliente", "Presidencia", "Gerencia General"
]
tipos_equipo_principales = ["Laptop", "Desktop", "Servidor Blade", "Impresora Multifuncional Láser"]
tipos_equipo_perifericos = ["Monitor Curvo 27\"", "Teclado Ergonómico", "Mouse Vertical", "Teléfono VoIP Ejecutivo", "Webcam 4K", "UPS Interactivo"]

marcas_pc = ["Dell Precision", "HP ZBook", "Lenovo ThinkPad P", "Apple MacBook Pro", "Acer ConceptD", "Asus ProArt", "VIT Xeon"]
modelos_laptop_dell = ["Latitude 7450 Ultralight", "XPS 17 (9730)", "Precision 7780 Mobile Workstation"]
modelos_desktop_hp = ["Elite Tower 800 G9", "Z2 Mini G9 Workstation", "ENVY Desktop"]
marcas_monitor = ["Dell UltraSharp PremierColor", "LG UltraFine OLED", "Samsung ViewFinity", "Eizo ColorEdge"]
marcas_impresora = ["HP LaserJet Enterprise", "Epson WorkForce Pro", "Canon MAXIFY", "Brother INKvestment"]
estatus_opciones = ["Operativo", "En Reparación Programada", "En Almacén Temporal", "Pendiente Desincorporar"]

tipos_mantenimiento_hist = [
    "Preventivo General", "Correctivo Menor", "Limpieza Profunda", "Actualización de Seguridad", 
    "Reemplazo de Consumibles", "Verificación de Rendimiento", "Diagnóstico Completo", "Optimización de Sistema"
]

# Fecha de referencia (hoy para el script, AHORA EN 2025)
hoy_script = datetime(2025, 5, 15).date()

datos_equipos_nuevos = []
num_equipos_a_generar = 20
seriales_usados = set()

for i in range(1, num_equipos_a_generar + 1):
    es_periferico = random.random() < 0.25 # 25% de probabilidad de ser periférico
    if es_periferico:
        tipo = random.choice(tipos_equipo_perifericos)
    else:
        tipo = random.choice(tipos_equipo_principales)

    marca = "Genérico"
    modelo = "Estándar"
    serial_real = None 

    asignado_a = random.choice(nombres_asignados) if random.random() > 0.05 else None # 5% sin asignar
    depto = random.choice(departamentos)
    estatus = random.choice(estatus_opciones) if random.random() > 0.05 else "Operativo"
    
    ultimo_mantenimiento_dt = None
    proximo_mantenimiento_dt = None

    # La mayoría de los equipos tendrán mantenimientos
    tiene_mantenimiento_programado = random.random() > 0.1 # 90% tendrán mantenimientos

    if tipo in tipos_equipo_principales:
        marca = random.choice(marcas_pc)
        if marca == "Dell Precision" and tipo == "Laptop": modelo = random.choice(modelos_laptop_dell)
        elif marca == "HP ZBook" and tipo == "Desktop": modelo = random.choice(modelos_desktop_hp)
        else: modelo = f"{marca.split()[0]} Modelo {random.randint(100,999)}"
        
        while True:
            temp_serial = f"EQP{random.randint(1000000,9999999)}{random.choice('XYZ')}"
            if temp_serial not in seriales_usados:
                serial_real = temp_serial; seriales_usados.add(serial_real); break
        
        if tiene_mantenimiento_programado:
            ultimo_mantenimiento_dt = hoy_script - timedelta(days=random.randint(15, 150)) # Más recientes
            
            # Próximo mantenimiento
            # La fecha de referencia es 15 de Mayo 2025
            if i % 3 == 0: # Próximo en Abril 2025 (si es posterior al último)
                fecha_prox_abril = datetime(2025, 4, random.randint(1, 28)).date()
                if ultimo_mantenimiento_dt and fecha_prox_abril < ultimo_mantenimiento_dt:
                     proximo_mantenimiento_dt = ultimo_mantenimiento_dt + relativedelta(months=random.choice([2,3,4]))
                else:
                    proximo_mantenimiento_dt = fecha_prox_abril
            else: # Próximo entre (hoy_script + 15 días) y (hoy_script + 3 meses)
                dias_futuro_max = (hoy_script + relativedelta(months=3) - (hoy_script + timedelta(days=14))).days
                proximo_mantenimiento_dt = hoy_script + timedelta(days=random.randint(15, 15 + dias_futuro_max if dias_futuro_max > 0 else 15))


    elif tipo.startswith("Monitor"):
        marca = random.choice(marcas_monitor)
        modelo = f"{marca.split()[0]} {random.choice([27, 32, 34])}X{random.randint(100,999)}K"
        if random.random() > 0.3: # 70% con serial
            while True: temp_serial = f"DISP{random.randint(10000,99999)}{random.choice('AB')}"; 
        if temp_serial not in seriales_usados: serial_real = temp_serial; seriales_usados.add(serial_real); break
    elif tipo.startswith("Impresora"):
        marca = random.choice(marcas_impresora)
        modelo = f"{marca.split()[0]} Pro {random.randint(500,999)}"
        while True: temp_serial = f"PRN{random.choice('LM')}{random.randint(1000,9999)}"; 
    if temp_serial not in seriales_usados: serial_real = temp_serial; seriales_usados.add(serial_real); break
    if tiene_mantenimiento_programado:
            ultimo_mantenimiento_dt = hoy_script - timedelta(days=random.randint(45, 200))
            proximo_mantenimiento_dt = ultimo_mantenimiento_dt + relativedelta(months=random.choice([3,6]))
    else: # Otros periféricos
        if tipo.startswith("Teclado"): marca = random.choice(["Logitech", "Corsair", "Razer", "Microsoft"])
        elif tipo.startswith("Mouse"): marca = random.choice(["Logitech", "Razer", "SteelSeries", "HP"])
        elif tipo.startswith("Teléfono"): marca = random.choice(["Cisco", "Yealink", "Polycom"])
        # Serial para estos periféricos será None (no se generará)

    observacion_text = f"{tipo} marca {marca}, modelo {modelo}. Serial: {serial_real if serial_real else 'N/A'}."
    if asignado_a: observacion_text += f" Asignado a {asignado_a} (Dpto: {depto})."
    else: observacion_text += f" Ubicado en Dpto: {depto}."
    if estatus != "Operativo": observacion_text += f" Estado actual: {estatus}."


    datos_equipos_nuevos.append({
        'id_temporal': i,
        'tipo_equipo': tipo, 'marca': marca, 'modelo': modelo, 'serial': serial_real,
        'asignado_a': asignado_a, 'departamento': depto, 'estatus': estatus,
        'ultimo_mantenimiento': ultimo_mantenimiento_dt.isoformat() if ultimo_mantenimiento_dt else None,
        'proximo_mantenimiento': proximo_mantenimiento_dt.isoformat() if proximo_mantenimiento_dt else None,
        'observacion': observacion_text
    })

# --- Función para Insertar Datos ---
def insertar_datos_completos_v3():
    conn = None
    try:
        print(f"Conectando a la base de datos en: {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("Conexión OK.")

        map_temp_to_real_id = {}
        sql_equipo = """
            INSERT INTO equipos (
                tipo_equipo, marca, modelo, serial, asignado_a, departamento, 
                estatus, ultimo_mantenimiento, proximo_mantenimiento, observacion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        print(f"\n--- Insertando {len(datos_equipos_nuevos)} Equipos ---")
        for equipo_data in datos_equipos_nuevos:
            serial_encriptado = encrypt_data(equipo_data['serial']) # encrypt_data maneja None
            asignado_encriptado = encrypt_data(equipo_data.get('asignado_a'))
            observacion_encriptada = encrypt_data(equipo_data.get('observacion'))
            valores = (
                equipo_data['tipo_equipo'], equipo_data['marca'], equipo_data['modelo'],
                serial_encriptado, asignado_encriptado, equipo_data['departamento'],
                equipo_data['estatus'], equipo_data['ultimo_mantenimiento'],
                equipo_data['proximo_mantenimiento'], observacion_encriptada
            )
            try:
                cursor.execute(sql_equipo, valores)
                if cursor.rowcount > 0: map_temp_to_real_id[equipo_data['id_temporal']] = cursor.lastrowid
            except sqlite3.IntegrityError as e: print(f"Err Integridad (serial '{equipo_data['serial']}'): {e}")
            except sqlite3.Error as e: print(f"Err SQL equipo (serial '{equipo_data['serial']}'): {e}")
        conn.commit()
        print(f"{len(map_temp_to_real_id)} equipos procesados para inserción.")

        if not map_temp_to_real_id: print("No se insertaron equipos, no se generará historial."); return

        print(f"\n--- Insertando Historial de Mantenimientos (5-10 por equipo) ---")
        sql_historial = """
            INSERT INTO historial_mantenimientos
            (equipo_id, fecha_realizado, tipo_mantenimiento, descripcion, realizado_por_usuario_id)
            VALUES (?, ?, ?, ?, ?)
        """
        admin_user_id = 1 
        historial_total_count = 0

        for equipo_data in datos_equipos_nuevos:
            id_temporal = equipo_data['id_temporal']
            if id_temporal not in map_temp_to_real_id: continue
            equipo_id_real = map_temp_to_real_id[id_temporal]
            
            num_historial_registros = random.randint(5, 10) # Generar entre 5 y 10 registros
            
            # El 'ultimo_mantenimiento' del equipo es el más reciente en el historial
            fecha_referencia_historial = None
            if equipo_data.get('ultimo_mantenimiento'):
                fecha_referencia_historial = datetime.strptime(equipo_data['ultimo_mantenimiento'], '%Y-%m-%d').date()
            else:
                # Si no hay ultimo_mantenimiento, generamos uno reciente para el historial
                fecha_referencia_historial = hoy_script - timedelta(days=random.randint(10, 60))

            for j in range(num_historial_registros):
                fecha_mant_actual = fecha_referencia_historial - relativedelta(months=random.randint(2, 6) * j) # Espaciados
                # Asegurarse que no sea antes de, por ejemplo, 2022
                if fecha_mant_actual.year < 2022:
                    fecha_mant_actual = datetime(2022, random.randint(1,12), random.randint(1,28)).date()

                tipo_mant_hist = random.choice(tipos_mantenimiento_hist)
                desc_hist_base = f"{tipo_mant_hist} el {fecha_mant_actual.strftime('%d/%m/%Y')}."
                detalles_adicionales = [
                    "Componentes revisados.", "Sistema operativo actualizado.", "Limpieza de ventiladores efectuada.",
                    "Pruebas de diagnóstico completadas.", "Firmware actualizado a la última versión.",
                    "Batería calibrada.", "Disco desfragmentado y optimizado."
                ]
                desc_hist = f"{desc_hist_base} {random.choice(detalles_adicionales)}"
                if tipo_mant_hist == "Correctivo Menor":
                    desc_hist = f"Se reemplazó {random.choice(['cable de poder', 'tecla defectuosa', 'pad térmico'])}. {desc_hist}"
                
                try:
                    cursor.execute(sql_historial, (
                        equipo_id_real, fecha_mant_actual.isoformat(), tipo_mant_hist,
                        encrypt_data(desc_hist), admin_user_id 
                    ))
                    historial_total_count += 1
                except sqlite3.Error as e: print(f"Err hist eqID {equipo_id_real}: {e}")
        
        conn.commit()
        print(f"{historial_total_count} registros de historial de mantenimiento insertados en total.")

    except sqlite3.Error as e: print(f"Error BD: {e}"); conn.rollback() if conn else None
    except Exception as e: print(f"Error script: {e}"); traceback.print_exc(); conn.rollback() if conn else None
    finally: conn.close(); print("Conexión cerrada.") if conn else None

if __name__ == "__main__":
    print("--- Iniciando Carga de Datos de EJEMPLO V3 (Año 2025, Historial Extenso) ---")
    respuesta = input(f"¿Está SEGURO de querer BORRAR la BD '{DATABASE_FILENAME}' (si existe) y cargar estos datos? (s/N): ")
    if respuesta.lower() == 's':
        if os.path.exists(DB_PATH):
            try: os.remove(DB_PATH); print(f"BD '{DB_PATH}' eliminada.")
            except OSError as e: print(f"Error al eliminar BD: {e}. Cancelando."); sys.exit(1)
        try:
            import database 
            print("Creando nueva estructura de BD..."); database.inicializar_db(); print("Estructura creada.")
        except ImportError: print("ERROR: No se pudo importar 'database.py'."); sys.exit(1)
        except Exception as init_e: print(f"ERROR al inicializar BD: {init_e}"); sys.exit(1)
        print("Insertando datos de ejemplo..."); insertar_datos_completos_v3()
    else: print("Carga cancelada.")
    print("--- Fin Carga de Datos de EJEMPLO V3 ---")