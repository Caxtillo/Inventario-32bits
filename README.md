MANUAL DE USUARIO: Sistema de Inventario de Equipos Corporativos
Versión 1.0
Fecha: 16 de Mayo de 2025
Índice:
Introducción
1.1. Propósito del Sistema
1.2. Requisitos del Sistema (si aplica para el cliente)
Primeros Pasos
2.1. Acceso al Sistema (Login)
Interfaz Principal (Dashboard)
3.1. Vista General
3.2. Indicadores Clave (KPIs)
3.3. Gráficos del Dashboard
3.4. Navegación
Gestión de Inventario
4.1. Vista de la Tabla de Inventario
4.2. Búsqueda y Filtrado
4.3. Paginación
4.4. Agregar Nuevo Equipo (Roles: Admin, Manager)
4.5. Ver Detalles del Equipo
4.6. Editar Equipo (Roles: Admin, Manager)
4.7. Eliminar Equipo (Rol: Admin)
4.8. Generar Código QR
4.9. Registrar Mantenimiento (Roles: Admin, Manager)
4.10. Ver Historial de Mantenimiento
Gestión de Usuarios (Rol: Admin)
5.1. Acceso a la Gestión de Usuarios
5.2. Vista de la Tabla de Usuarios
5.3. Agregar Nuevo Usuario
5.4. Editar Rol de Usuario
5.5. Restablecer Contraseña de Usuario
5.6. Eliminar Usuario
Importación y Exportación de Datos
6.1. Descargar Plantilla Excel
6.2. Importar Datos desde Excel (Roles: Admin, Manager)
6.3. Exportar Vista a PDF (Tabla o Códigos QR)
Cerrar Sesión
Solución de Problemas / Preguntas Frecuentes (FAQ)
1. Introducción
1.1. Propósito del Sistema
El Sistema de Inventario de Equipos Corporativos está diseñado para facilitar la gestión, seguimiento y mantenimiento de todos los activos de hardware de la organización. Permite registrar equipos, asignar usuarios, llevar un control de su estado, programar y registrar mantenimientos, y generar reportes.
1.2. Requisitos del Sistema
Este es un sistema de escritorio. Para ejecutarlo, necesita tener el software proporcionado instalado en un computador con sistema operativo Windows 7 (32-bit) o superior.
2. Primeros Pasos
2.1. Acceso al Sistema (Login)
Al iniciar la aplicación, se presentará una ventana de inicio de sesión.
Usuario: Ingrese su nombre de usuario asignado.
Contraseña: Ingrese su contraseña.
Haga clic en el botón "Ingresar" o presione la tecla Enter.
Si las credenciales son correctas, accederá al sistema.
Si las credenciales son incorrectas, se mostrará un mensaje de error. Verifique sus datos e intente nuevamente.
Para salir sin ingresar, haga clic en "Cancelar".
[IMAGEN: Captura de pantalla del diálogo de Login]
3. Interfaz Principal (Dashboard)
Al ingresar exitosamente, se mostrará el Dashboard principal del sistema.
3.1. Vista General
El Dashboard ofrece una vista resumida del estado del inventario a través de indicadores clave y gráficos interactivos.
3.2. Indicadores Clave (KPIs)
En la parte superior, encontrará tarjetas con información relevante, como:
Total Equipos: Número total de equipos registrados.
Mantenim. Próximos (30d): Cantidad de equipos con mantenimiento programado en los próximos 30 días.
Total Usuarios: Número total de usuarios registrados en el sistema.
Otros indicadores según configuración.
[IMAGEN: Sección de KPIs del Dashboard]
3.3. Gráficos del Dashboard
El dashboard presenta varios gráficos para visualizar la distribución del inventario:
Equipos por Tipo: Gráfico de pastel o dona mostrando la proporción de cada tipo de equipo.
Equipos por Estatus: Gráfico de pastel mostrando la distribución de equipos según su estado actual (Operativo, En Reparación, etc.).
Equipos por Departamento: Gráfico de barras mostrando la cantidad de equipos asignados a cada departamento.
Top Marcas: Gráfico de barras mostrando las marcas de equipos más comunes.
Puede pasar el cursor sobre los segmentos de los gráficos para ver detalles.
[IMAGEN: Sección de Gráficos del Dashboard]
3.4. Navegación
En la barra superior (navbar), encontrará los siguientes botones de navegación:
Logo/Nombre: (Puede o no ser un enlace a la página principal).
Dashboard: (Si está en otra vista, este botón lo regresa al Dashboard).
Inventario: Lo lleva a la vista detallada de la tabla de inventario.
Usuarios: (Visible solo para rol Admin) Lo lleva a la gestión de usuarios.
Salir: Cierra su sesión y la aplicación.
Nombre de Usuario: Muestra el rol del usuario actualmente conectado.
4. Gestión de Inventario
Haciendo clic en el botón "Inventario" en la barra de navegación, accederá a la lista detallada de equipos.
4.1. Vista de la Tabla de Inventario
Se muestra una tabla con la siguiente información por cada equipo:
N° (Número de fila)
Tipo
Marca
Modelo
Serial
Asignado a
Departamento (Depto)
Estatus
Acciones
[IMAGEN: Tabla de Inventario]
4.2. Búsqueda y Filtrado
Barra de Búsqueda: Ingrese términos (serial, modelo, asignado, etc.) para buscar equipos específicos. Presione Enter o haga clic en el botón "Filtrar".
Botón "Filtrar": Aplica los criterios de la barra de búsqueda.
Botón "X" (Limpiar Filtros): Borra el término de búsqueda y muestra todos los equipos.
Botón "Mantenim.": Filtra y muestra solo los equipos que tienen mantenimientos pendientes o vencidos.
4.3. Paginación
Mostrar X por página: Seleccione cuántos equipos desea ver por página (10, 25, 50, 100).
Botones "< Ant" y "Sig >": Para navegar entre las páginas de resultados.
Indicador "Página X de Y": Muestra la página actual y el total de páginas.
4.4. Agregar Nuevo Equipo (Roles: Admin, Manager)
Haga clic en el botón flotante verde con el símbolo "+" ubicado en la esquina inferior derecha.
Se abrirá el modal "Agregar Nuevo Equipo".
Campos del Formulario:
Tipo Equipo*: Obligatorio. Seleccione de la lista o elija "-- Nuevo Tipo Equipo --" e ingrese el nuevo tipo en el campo de texto que aparecerá.
Marca, Modelo, Asignado a, Departamento: Puede seleccionar de la lista o elegir "-- Nuevo/a ... --" para ingresar un valor nuevo.
Serial*: Obligatorio. Ingrese el número de serial único del equipo.
Estatus: Seleccione el estado actual del equipo (por defecto "Operativo").
Últ. Mantenimiento: Fecha del último mantenimiento realizado (opcional).
Próx. Mantenimiento: Fecha del próximo mantenimiento programado (opcional).
Observación: Cualquier nota adicional sobre el equipo.
Haga clic en "Guardar Nuevo" para agregar el equipo.
Haga clic en "Cerrar" o la "X" para cancelar.
Un campo marcado con * es obligatorio.
[IMAGEN: Modal de Agregar Equipo]
4.5. Ver Detalles del Equipo
En la columna "Acciones" de la tabla, haga clic en el icono del ojo (<i class="fas fa-eye"></i>).
Se abrirá el modal con los detalles del equipo en modo solo lectura.
También se mostrará el Historial de Mantenimientos para ese equipo (ver sección 4.10).
4.6. Editar Equipo (Roles: Admin, Manager)
En la columna "Acciones", haga clic en el icono del lápiz (<i class="fas fa-edit"></i>).
Se abrirá el modal "Editar Equipo ID: X" con los datos del equipo cargados en el formulario.
Modifique los campos necesarios.
Haga clic en "Actualizar Equipo" para guardar los cambios.
4.7. Eliminar Equipo (Rol: Admin)
En la columna "Acciones", haga clic en el icono de la papelera (<i class="fas fa-trash"></i>).
Aparecerá un mensaje de confirmación.
Haga clic en "Sí, Eliminar" para confirmar la eliminación. Esta acción es irreversible.
Haga clic en "Cancelar" para no eliminar el equipo.
4.8. Generar Código QR
En la columna "Acciones", haga clic en el icono del código QR (<i class="fas fa-qrcode"></i>).
Se mostrará un modal con el código QR generado para ese equipo, conteniendo información básica del mismo. Puede ser escaneado con una aplicación de lectura de QR.
[IMAGEN: Modal de Código QR]
4.9. Registrar Mantenimiento (Roles: Admin, Manager)
En la columna "Acciones", haga clic en el icono de herramientas (<i class="fas fa-tools"></i>).
Se abrirá el modal "Registrar Mantenimiento para ID: X".
Campos del Formulario:
Equipo: Muestra información básica del equipo seleccionado.
Fecha Realizado*: Obligatorio. Fecha en que se realizó el mantenimiento (por defecto la fecha actual).
Tipo Mantenimiento: Describa el tipo de mantenimiento (ej. Preventivo, Correctivo, Limpieza).
Próximo Mtto. en (meses): Ingrese el número de meses hasta el próximo mantenimiento. Deje vacío o en 0 si no desea programar uno automáticamente.
Descripción / Notas: Detalles sobre el trabajo realizado.
Haga clic en "Guardar Mantenimiento".
Esto registrará el mantenimiento en el historial del equipo y actualizará las fechas de "Último Mantenimiento" y "Próximo Mantenimiento" en la ficha del equipo.
[IMAGEN: Modal de Registrar Mantenimiento]
4.10. Ver Historial de Mantenimiento
Cuando visualiza los detalles de un equipo (ver sección 4.5), en la parte inferior del modal aparecerá la sección "Historial de Mantenimientos".
Se mostrará una tabla con todos los mantenimientos registrados para ese equipo, ordenados por fecha descendente.
Columnas: Fecha Realizado, Tipo, Descripción, Registró (usuario que hizo el registro).
[IMAGEN: Sección de Historial de Mantenimiento en el Modal de Detalles]
5. Gestión de Usuarios (Rol: Admin)
Si su rol es Administrador, tendrá acceso a la gestión de usuarios.
5.1. Acceso a la Gestión de Usuarios
Haga clic en el botón "Usuarios" en la barra de navegación superior.
5.2. Vista de la Tabla de Usuarios
Se muestra una tabla con los usuarios del sistema:
ID
Nombre de Usuario
Rol (admin, manager, read_only)
Acciones
[IMAGEN: Tabla de Gestión de Usuarios]
5.3. Agregar Nuevo Usuario
Haga clic en el botón "Agregar Usuario".
Ingrese el Nombre de Usuario, una Contraseña y seleccione el Rol.
Haga clic en "Guardar".
5.4. Editar Rol de Usuario
En la columna "Acciones" de la tabla de usuarios, haga clic en el icono de editar rol (<i class="fas fa-user-shield"></i>).
Seleccione el nuevo rol para el usuario.
Haga clic en "Guardar Rol".
Nota: No se puede cambiar el rol del último administrador a un rol inferior.
5.5. Restablecer Contraseña de Usuario
En la columna "Acciones", haga clic en el icono de llave (<i class="fas fa-key"></i>).
Ingrese la Nueva Contraseña para el usuario.
Haga clic en "Restablecer".
5.6. Eliminar Usuario
En la columna "Acciones", haga clic en el icono de la papelera (<i class="fas fa-user-times"></i>).
Confirme la eliminación.
Nota: Un administrador no puede eliminarse a sí mismo. No se puede eliminar al último administrador del sistema.
6. Importación y Exportación de Datos
Estas funciones se encuentran en la vista de "Gestión de Inventario", encima de la tabla.
6.1. Descargar Plantilla Excel
Haga clic en el botón "Descargar Plantilla".
Se descargará un archivo Excel (plantilla_inventario_xxxx.xlsx) con el formato requerido para la importación masiva de equipos.
Llene esta plantilla con los datos de los equipos que desea importar. Las columnas con * son obligatorias.
6.2. Importar Datos desde Excel (Roles: Admin, Manager)
Haga clic en el botón "Importar Excel".
Se abrirá un diálogo para seleccionar el archivo Excel (debe ser la plantilla llenada o un archivo con el mismo formato).
Seleccione el archivo .xlsx y haga clic en "Abrir".
El sistema procesará el archivo. Se mostrará un mensaje con el resultado: equipos insertados, ignorados (por duplicados) y errores.
6.3. Exportar Vista a PDF (Tabla o Códigos QR)
Filtre la tabla de inventario según los equipos que desea incluir en el reporte (o no filtre para incluirlos todos).
Haga clic en el botón "Exportar Vista...".
Se abrirá un pequeño modal preguntando el formato:
Exportar como Tabla PDF: Genera un PDF con los datos de los equipos visibles en formato de tabla.
Exportar Códigos QR PDF: Genera un PDF con los códigos QR de los equipos visibles, útil para etiquetado.
Seleccione una opción. Se le pedirá que elija una ubicación y nombre para guardar el archivo PDF.
Una vez generado, se mostrará un mensaje de confirmación con un botón para intentar abrir el archivo PDF.
7. Cerrar Sesión
Para salir del sistema de forma segura, haga clic en el botón "Salir" ubicado en la esquina superior derecha de la pantalla.
Esto cerrará la aplicación.
8. Solución de Problemas / Preguntas Frecuentes (FAQ)
P: Olvidé mi contraseña.
R: Póngase en contacto con un administrador del sistema para que pueda restablecer su contraseña.
P: No puedo agregar/editar equipos.
R: Verifique su rol de usuario. Solo los roles "Admin" y "Manager" tienen permisos para estas acciones. Si cree que debería tener permisos, contacte a un administrador.
P: La importación de Excel da errores.
R: Asegúrese de estar utilizando la plantilla descargada y que los datos obligatorios (como "Tipo Equipo" y "Serial") estén completos y en el formato correcto (especialmente las fechas). Revise los mensajes de error detallados que proporciona el sistema.
P: El sistema se muestra lento.
R: Si maneja una cantidad muy grande de equipos, algunas operaciones como la carga inicial o filtros complejos pueden tomar un momento. Si la lentitud es persistente, informe al soporte técnico o al administrador.
P: No encuentro un equipo que sé que existe.
R: Verifique que no tenga filtros activos que puedan estar ocultándolo. Use el botón "X" para limpiar todos los filtros. Intente buscar por diferentes criterios (serial, modelo, etc.).
Este manual es una guía general. Las funcionalidades y la apariencia exacta pueden variar ligeramente. Si encuentra algún problema o tiene preguntas no cubiertas aquí, por favor contacte al administrador del sistema o al equipo de soporte técnico.
