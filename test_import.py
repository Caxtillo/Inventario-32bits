# test_import.py
print("Intentando importar QWebEngineSettings...")
try:
    from PySide2.QtWebEngineCore import QWebEngineSettings
    print("Importación desde QtWebEngineCore ¡EXITOSA!")
    print(QWebEngineSettings) # Imprimir la clase para ver si existe
except ImportError as e1:
    print(f"FALLO al importar desde QtWebEngineCore: {e1}")
    print("\nIntentando importar desde QtWebEngineWidgets...")
    try:
        from PySide2.QtWebEngineWidgets import QWebEngineSettings # Intento alternativo
        print("Importación desde QtWebEngineWidgets ¡EXITOSA!")
        print(QWebEngineSettings)
    except ImportError as e2:
        print(f"FALLO al importar desde QtWebEngineWidgets: {e2}")
    except Exception as e_other:
        print(f"Otro error al importar desde Widgets: {e_other}")

except Exception as e_other_core:
    print(f"Otro error al importar desde Core: {e_other_core}")

print("\nIntento de importación terminado.")
input("Presiona Enter para salir...") # Pausa para ver la salida