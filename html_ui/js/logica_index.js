document.addEventListener('DOMContentLoaded', () => {

    // --- Referencias a Elementos del DOM ---
    const userRoleDisplay = document.getElementById('user-role-display');
    const logoutButton = document.getElementById('logout-button');
    const userMgmtButton = document.getElementById('user-mgmt-button');
    const addEquipmentFloatButton = document.getElementById('add-equipment-float-button');
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const darkModeIcon = document.getElementById('dark-mode-icon');
    const htmlElement = document.documentElement; // Referencia al <html>
    const dashboardButton = document.getElementById('dashboard-button');

    // --- ¡AÑADIR REFERENCIAS FALTANTES PARA IMPORTACIÓN! ---
    const downloadTemplateButton = document.getElementById('download-template-button');
    const importExcelButton = document.getElementById('import-excel-button'); // <-- ¡ESTA FALTABA!
    const excelFileInput = document.getElementById('excel-file-input');
    const importFeedback = document.getElementById('import-feedback');
    const importFeedbackMessage = document.getElementById('import-feedback-message'); // <-- ¡AÑADIR ESTA! El span para el texto
    const closeImportFeedbackButton = document.getElementById('close-import-feedback'); // <-- ¡ASEGÚRATE QUE ESTÉ ESTA! El botón 'x'
    const exportButton = document.getElementById('export-button'); // El botón principal "Exportar Vista..."
    const exportChoiceModal = document.getElementById('export-choice-modal');
    const closeExportChoiceButton = document.getElementById('close-export-choice-button');
    const cancelExportChoiceButton = document.getElementById('cancel-export-choice-button');
    const exportTableButton = document.getElementById('export-table-button');
    const exportQrButton = document.getElementById('export-qr-button');

    // Elementos del Modal de Formulario
    const equipmentModal = document.getElementById('equipment-modal');
    const modalTitle = document.getElementById('modal-title');
    const closeModalButton = document.getElementById('close-modal-button');
    const cancelModalButton = document.getElementById('cancel-modal-button');
    const equipmentForm = document.getElementById('equipment-form');
    const equipmentIdInput = document.getElementById('equipment-id'); // Input oculto para ID
    const saveButton = document.getElementById('save-button');
    const saveButtonText = document.getElementById('save-button-text'); // Span dentro del botón Guardar
    const formFeedback = document.getElementById('form-feedback');

    // --- NUEVAS Referencias a Elementos de Paginación/Ordenamiento ---
    const itemsPerPageSelect = document.getElementById('items-per-page');
    const prevPageButton = document.getElementById('prev-page-button');
    const nextPageButton = document.getElementById('next-page-button');
    const currentPageDisplay = document.getElementById('current-page-display');
    const totalPagesDisplay = document.getElementById('total-pages-display');
    const itemsShowingSpan = document.getElementById('items-showing');
    const itemsTotalSpan = document.getElementById('items-total');
    const filteredInfoSpan = document.getElementById('filtered-info');
    // Refs para controles inferiores (opcional)
    const prevPageButtonBottom = document.getElementById('prev-page-button-bottom');
    const nextPageButtonBottom = document.getElementById('next-page-button-bottom');
    const currentPageDisplayBottom = document.getElementById('current-page-display-bottom');
    const totalPagesDisplayBottom = document.getElementById('total-pages-display-bottom');
    const tableHeaders = document.querySelectorAll('#equipment-table-body th.sortable-header'); // Seleccionar encabezados

    const maintenanceModal = document.getElementById('maintenance-modal');
    const maintenanceModalTitle = document.getElementById('maintenance-modal-title');
    const closeMaintenanceModalButton = document.getElementById('close-maintenance-modal-button');
    const cancelMaintenanceModalButton = document.getElementById('cancel-maintenance-modal-button');
    const maintenanceForm = document.getElementById('maintenance-form');
    const maintenanceEquipmentIdInput = document.getElementById('maintenance-equipment-id');
    const maintenanceEquipmentInfo = document.getElementById('maintenance-equipment-info'); // Para mostrar info del equipo
    const maintenanceFechaRealizadoInput = document.getElementById('maintenance-fecha-realizado');
    const maintenanceTipoInput = document.getElementById('maintenance-tipo');
    const maintenanceProximoMesesInput = document.getElementById('maintenance-proximo-meses');
    const maintenanceDescripcionInput = document.getElementById('maintenance-descripcion');
    const saveMaintenanceButton = document.getElementById('save-maintenance-button');
    const maintenanceFormFeedback = document.getElementById('maintenance-form-feedback');

    const maintenanceHistorySection = document.getElementById('maintenance-history-section');
    const maintenanceHistoryTableBody = document.getElementById('maintenance-history-table-body');
    const maintenanceHistoryFeedback = document.getElementById('maintenance-history-feedback');

        // --- NUEVAS REFERENCIAS DOM PARA SELECCIÓN MÚLTIPLE ---
    const selectAllCheckbox = document.getElementById('select-all-checkbox');
    const bulkActionsPanel = document.getElementById('bulk-actions-panel');
    const selectedCountSpan = document.getElementById('selected-count');
    const bulkEditButton = document.getElementById('bulk-edit-button');
    const bulkDeleteButton = document.getElementById('bulk-delete-button');

    const bulkEditModal = document.getElementById('bulk-edit-modal');
    const closeBulkEditModalButton = document.getElementById('close-bulk-edit-modal-button');
    const bulkEditForm = document.getElementById('bulk-edit-form');
    const bulkEditFormFeedback = document.getElementById('bulk-edit-form-feedback');
    const bulkEditCountSpan = document.getElementById('bulk-edit-count');
    const cancelBulkEditButton = document.getElementById('cancel-bulk-edit-button');
    const saveBulkEditButton = document.getElementById('save-bulk-edit-button');


    let currentEquipmentForMaintenance = null;

     // Inputs del formulario (para llenar/resetear)
     const formInputs = {
        tipo_equipo: document.getElementById('tipo_equipo'),
        marca: document.getElementById('marca'),
        modelo: document.getElementById('modelo'),
        serial: document.getElementById('serial'),
        asignado_a: document.getElementById('asignado_a'),
        departamento: document.getElementById('departamento'),
        sede: document.getElementById('sede'),
        estatus: document.getElementById('estatus'),
        ultimo_mantenimiento: document.getElementById('ultimo_mantenimiento'),
        proximo_mantenimiento: document.getElementById('proximo_mantenimiento'),
        observacion: document.getElementById('observacion')
     };

     const formSelects = {
        tipo_equipo: document.getElementById('tipo_equipo-select'),
        marca: document.getElementById('marca-select'),
        modelo: document.getElementById('modelo-select'),
        asignado_a: document.getElementById('asignado_a-select'),
        departamento: document.getElementById('departamento-select'),
        sede: document.getElementById('sede-select')
    };
    const formDisplaySpans = {
        tipo_equipo: document.getElementById('tipo_equipo-display'),
        marca: document.getElementById('marca-display'),
        modelo: document.getElementById('modelo-display'),
        serial: document.getElementById('serial-display'),
        asignado_a: document.getElementById('asignado_a-display'),
        departamento: document.getElementById('departamento-display'),
        sede: document.getElementById('sede-display'), // Asegúrate de tener esta referencia
        estatus: document.getElementById('estatus-display'),
        ultimo_mantenimiento: document.getElementById('ultimo_mantenimiento-display'),
        proximo_mantenimiento: document.getElementById('proximo_mantenimiento-display'),
        observacion: document.getElementById('observacion-display')
    };

    const filtBtn = document.getElementById('filter-button');
    if(filtBtn) filtBtn.addEventListener('click', applyFiltersAndRender); // CORRECTO
    else console.error("Botón 'filter-button' no encontrado");

    dashboardButton?.addEventListener('click', () => {
    if (backend) { // Asegúrate que backend existe
        console.log("INDEX.JS: Solicitando navegación a Dashboard..."); // Log para ver si se dispara
        try {
            backend.navigate_to('dashboard');
        } catch (e) {
            console.error("INDEX.JS: Error al intentar navegar al dashboard:", e);
            alert('No se pudo iniciar la navegación al dashboard.'); // Feedback simple
        }
    } else {
        console.error("INDEX.JS: Backend no disponible para navegar al dashboard.");
        alert('Error de conexión. No se puede navegar al dashboard.'); // Feedback simple
    }
    });

    // Listener Botón Limpiar Filtros (X)
    const clearFilterButton = document.getElementById('clear-filter-button'); 
    if(clearFilterButton ) { // Referencia única
        clearFilterButton .addEventListener('click', () => { 
            console.log("--- Botón Limpiar Filtros CLICADO ---");
            if(searchTermInput) searchTermInput.value = ''; 
            console.log("  Llamando a applyFiltersAndRender() para limpiar...");
            applyFiltersAndRender(); // Llamar a la función central
        });
        console.log("Listener añadido a clearFilterButton");
    } else console.error("Botón 'clear-filter-button' no encontrado");

     // Listener Input Búsqueda (Enter)
     const searchInput = document.getElementById('search-term');
     if(searchInput) {
         searchInput.addEventListener('keypress', (e) => { 
             if (e.key === 'Enter') {
                 applyFiltersAndRender(); // Aplicar filtro al presionar Enter
             }
         });
     } else console.error("Input 'search-term' no encontrado");

     if (itemsPerPageSelect) {
        itemsPerPageSelect.addEventListener('change', (event) => {
            const newValue = parseInt(event.target.value, 10); // Obtener y convertir a número
            console.log(`Cambiando itemsPerPage de ${itemsPerPage} a ${newValue}`);
            itemsPerPage = newValue; // *** ASEGURAR que actualiza la variable global ***
            currentPage = 1; // Resetear a página 1 SIEMPRE que se cambia items por página
            console.log("Llamando a renderPagedTable() desde el listener de itemsPerPageSelect...");
            renderPagedTable(); // Volver a renderizar con la nueva cantidad
        });
         console.log("Listener añadido a itemsPerPageSelect");
    } else {
        console.error("Select 'items-per-page' no encontrado.");
    }

    // Listener Botón Mantenimiento
    const maintBtn = document.getElementById('filter-maintenance-button');
    if(maintBtn) maintBtn.addEventListener('click', filterMaintenance); // CORRECTO
    else console.error("Botón 'filter-maintenance-button' no encontrado");
    
    console.log("--- Añadiendo Listeners a los Selects Dinámicos ---");
    Object.keys(formSelects).forEach(fieldName => {
        const selectElement = formSelects[fieldName]; // Obtener el elemento select del objeto

        // Log ANTES de intentar añadir el listener
        console.log(`  Intentando añadir listener a select para [${fieldName}]:`, selectElement);

        if (selectElement) {
            // Verificar si ya tiene un listener (opcional, para evitar duplicados si algo va mal)
             // if (!selectElement.dataset.listenerAdded) { // Forma de evitar duplicados
                selectElement.addEventListener('change', handleSelectChange);
                // selectElement.dataset.listenerAdded = 'true'; // Marcar como añadido
                 console.log(`  ✅ Listener 'change' -> handleSelectChange AÑADIDO a select '${selectElement.id}'`);
             // } else {
             //    console.log(`  ❕ Listener ya existe en select '${selectElement.id}'`);
             // }
        } else {
            // Si el selectElement es null o undefined
            console.error(`  ❌ ERROR: Select para '${fieldName}' (ID: ${fieldName}-select) NO encontrado. No se pudo añadir listener.`);
        }
    });
    console.log("--- Fin de añadir Listeners a los Selects Dinámicos ---");
    // -----------------------------------------------------
        const bulkEditFields = {
        estatus: {
            checkbox: document.getElementById('bulk-edit-estatus-checkbox'),
            input: document.getElementById('bulk-edit-estatus')
        },
        departamento: {
            checkbox: document.getElementById('bulk-edit-departamento-checkbox'),
            select: document.getElementById('bulk-edit-departamento'),
            input: document.getElementById('bulk-edit-departamento-input')
        },
        sede: {
            checkbox: document.getElementById('bulk-edit-sede-checkbox'),
            select: document.getElementById('bulk-edit-sede'),
            input: document.getElementById('bulk-edit-sede-input')
        },
        observacion: {
            checkbox: document.getElementById('bulk-edit-observacion-checkbox'),
            input: document.getElementById('bulk-edit-observacion')
        }
    };
    // Elementos de Filtro/Búsqueda
    const searchTermInput = document.getElementById('search-term');
    const filterButton = document.getElementById('filter-button');
    const filterMaintenanceButton = document.getElementById('filter-maintenance-button');


    // Tabla
    const equipmentTableBody = document.getElementById('equipment-table-body');

    // Elementos del Modal de Confirmación Delete
    const deleteConfirmModal = document.getElementById('delete-confirm-modal');
    const deleteConfirmMessage = document.getElementById('delete-confirm-message');
    const confirmDeleteButton = document.getElementById('confirm-delete-button');
    const cancelDeleteButton = document.getElementById('cancel-delete-button');

    // Elementos del Modal QR
    const qrCodeModal = document.getElementById('qr-code-modal');
    const qrModalTitle = document.getElementById('qr-modal-title');
    const qrImageContainer = document.getElementById('qr-image-container');
    const qrCodeImage = document.getElementById('qr-code-image');
    const qrSpinner = document.getElementById('qr-spinner');
    const qrModalInfo = document.getElementById('qr-modal-info');
    const closeQrButton = document.getElementById('close-qr-button');

    // Referencias a los datalists
    const tipoEquipoDataList = document.getElementById('tipo-equipo-list');
    const marcaDataList = document.getElementById('marca-list');
    const modeloDataList = document.getElementById('modelo-list');
    const asignadoDataList = document.getElementById('asignado-list');
    const deptoDataList = document.getElementById('dept-list'); // El que ya existía

    // --- Estado de la Aplicación ---
    let backend = null;
    let currentUserRole = 'read_only';
    let editingEquipmentId = null;
    let equipmentToDeleteId = null;
    let allEquipmentData = []; // Caché de TODOS los datos del backend
    let currentFilteredData = []; // Datos después de aplicar filtros de búsqueda/select
    let isDarkMode = false; // Estado inicial (se ajustará al cargar)
     let selectedEquipmentIds = new Set();

    // --- NUEVO Estado para Paginación y Ordenamiento ---
    let currentPage = 1;
    let itemsPerPage = parseInt(itemsPerPageSelect?.value || '10', 10); // Valor inicial del select
    let sortColumn = null; // 'index', 'tipo_equipo', 'marca', etc. (o null)
    let sortDirection = 'asc'; // 'asc' o 'desc'

    // --- Funciones Auxiliares (Existentes: safe, showModal, hideModal, displayFormFeedback, etc.) ---
    const safe = (value) => value === null || value === undefined ? '' : value;
    function showModal(modalElement) { modalElement.classList.add('is-active'); }
    function hideModal(modalElement) { modalElement.classList.remove('is-active'); }
        function formatIsoDateToDMY(isoDateString) {
        if (!isoDateString) return '';
        try {
            // Intenta crear un objeto Date desde el string ISO (YYYY-MM-DD)
            const parts = isoDateString.split('-');
            if (parts.length === 3) {
                const year = parseInt(parts[0], 10);
                const month = parseInt(parts[1], 10);
                const day = parseInt(parts[2], 10);
                // Usar Date.UTC para evitar problemas de zona horaria si solo se dan año, mes, día
                const date = new Date(Date.UTC(year, month - 1, day)); // Meses son 0-index
                
                // Formatear a DD/MM/YYYY
                const dayStr = String(date.getUTCDate()).padStart(2, '0');
                const monthStr = String(date.getUTCMonth() + 1).padStart(2, '0'); // getUTCMonth es 0-index
                const yearStr = date.getUTCFullYear();
                return `${dayStr}/${monthStr}/${yearStr}`;
            }
        } catch (e) {
            console.error("Error al formatear fecha ISO:", isoDateString, e);
        }
        return isoDateString; // Devolver el original si hay error o no es formato esperado
    }
        Object.values(bulkEditFields).forEach(field => {
        if (field.checkbox) {
            field.checkbox.addEventListener('change', (event) => {
                const checked = event.target.checked;
                const targetElement = field.input || field.select; // El input o select que debe habilitarse/deshabilitarse
                
                if (targetElement) {
                    targetElement.disabled = !checked; // <-- ESTA ES LA LÍNEA CRÍTICA
                    
                    if (checked) {
                        targetElement.classList.remove('bg-gray-100', 'cursor-not-allowed'); // <-- QUITAR ESTILOS DE DESHABILITADO
                        // Si es un select/input combinado, y se marca, mostrar el select por defecto
                        if (field.select) field.select.classList.remove('hidden'); 
                        if (field.input) field.input.classList.add('hidden'); // Ocultar input de texto por defecto
                        if (field.select && field.select.value === '__nuevo__') { // Si el valor es 'nuevo'
                            field.input.classList.remove('hidden'); // Entonces mostrar el input de texto
                        }
                    } else {
                        targetElement.classList.add('bg-gray-100', 'cursor-not-allowed'); // <-- AÑADIR ESTILOS DE DESHABILITADO
                        targetElement.value = ''; // Limpiar valor si se deshabilita
                        if (field.select) field.select.classList.add('hidden'); // Ocultar select si se deshabilita
                        if (field.input) field.input.classList.add('hidden'); // Ocultar input si se deshabilita
                    }
                }
            });
        }
    });
    // Mostrar/Ocultar Modal
    function showModal(modalElement) {
        modalElement.classList.add('is-active');
    }
    function hideModal(modalElement) {
        modalElement.classList.remove('is-active');
    }

    function applyTheme(isDark) {
        isDarkMode = isDark; // Actualizar estado global
        if (isDark) {
            htmlElement.classList.add('dark');
            if(darkModeIcon) darkModeIcon.classList.replace('fa-moon', 'fa-sun'); // Cambiar a icono de sol
            localStorage.setItem('theme', 'dark'); // Guardar preferencia
            console.log("Tema cambiado a Oscuro");
        } else {
            htmlElement.classList.remove('dark');
            if(darkModeIcon) darkModeIcon.classList.replace('fa-sun', 'fa-moon'); // Cambiar a icono de luna
            localStorage.setItem('theme', 'light'); // Guardar preferencia
            console.log("Tema cambiado a Claro");
        }
        // Actualizar título del botón (opcional)
        if (darkModeToggle) {
            darkModeToggle.title = isDark ? "Cambiar a Tema Claro" : "Cambiar a Tema Oscuro";
        }
    }

    // --- NUEVA: Función para manejar el clic del botón ---
    function handleThemeToggle() {
        applyTheme(!isDarkMode); // Invertir el estado actual
    }

    

    // --- NUEVA: Función para inicializar el tema al cargar ---
    function initializeTheme() {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const savedTheme = localStorage.getItem('theme');
        let initialDarkMode = false;

        if (savedTheme === 'dark') {
            initialDarkMode = true;
        } else if (savedTheme === 'light') {
            initialDarkMode = false;
        } else {
            // Si no hay tema guardado, usar preferencia del OS
            initialDarkMode = prefersDark;
        }
        console.log(`Inicializando tema. Guardado: ${savedTheme}, Prefiere OS: ${prefersDark}, Inicial: ${initialDarkMode ? 'Oscuro' : 'Claro'}`);
        applyTheme(initialDarkMode); // Aplicar tema inicial
    }

    // Mostrar Feedback en Formulario
    function displayFormFeedback(type, message) {
         formFeedback.textContent = message;
         formFeedback.className = 'mb-4 p-3 rounded text-sm'; // Reset clases
         if (type === 'success') {
             formFeedback.classList.add('bg-green-100', 'text-green-700');
         } else if (type === 'error') {
              formFeedback.classList.add('bg-red-100', 'text-red-700');
         } else { // info
              formFeedback.classList.add('bg-blue-100', 'text-blue-700');
         }
         formFeedback.classList.remove('hidden'); // Mostrar
         setTimeout(() => { formFeedback.classList.add('hidden'); formFeedback.textContent=''; }, 5000);
    }

     // Mostrar Feedback General (podría ser un toast o alert)
     function displayGeneralFeedback(type, message) {
        console.log(`Feedback General (${type}): ${message}`);
        // Implementar un toast o usar el feedback del formulario si no hay otra área
         displayFormFeedback(type, message); // Reutilizar feedback del form por ahora
     }

     function applyFiltersAndRender() {
        console.log("--- applyFiltersAndRender INVOCADA ---");
        
        // 1. Llama a filterData para obtener los datos según el estado ACTUAL de los filtros (ej. searchTermInput)
        //    filterData debe devolver [...allEquipmentData] si los filtros están vacíos.
        currentFilteredData = filterData(allEquipmentData); 
        console.log(`  applyFiltersAndRender: currentFilteredData actualizado a ${currentFilteredData.length} items.`);
        
        // 2. Resetear SIEMPRE a la primera página al aplicar/limpiar filtros
        currentPage = 1; 
        console.log(`  applyFiltersAndRender: currentPage reseteado a ${currentPage}.`);
        
        // 3. Llamar a la función que renderiza la tabla PAGINADA
        console.log("  applyFiltersAndRender: Llamando a renderPagedTable()...");
        renderPagedTable(); // Esta función usa currentPage, itemsPerPage y currentFilteredData
        
        // 4. Actualizar la información sobre filtros activos (opcional)
        updateFilteredInfo(); 
        console.log("--- applyFiltersAndRender FINALIZADA ---");
    }

    function updateFilteredInfo(isMaintenanceFilter = false) {
        const searchTerm = searchTermInput?.value?.trim(); // Usar optional chaining
        let info = "";
        if (isMaintenanceFilter) {
            info = "(Filtro: Mantenimiento Pendiente)";
        } else if (searchTerm) {
            info = "(Filtro de búsqueda activo)";
        }
        
        // Actualizar el span
        if (filteredInfoSpan) {
             filteredInfoSpan.textContent = info;
             console.log(`  updateFilteredInfo: Mostrando info "${info}"`);
        } else {
             console.warn("updateFilteredInfo: filteredInfoSpan no encontrado.");
        }
    }

    function sortData() {
        if (!sortColumn) return; // No ordenar si no hay columna seleccionada

        console.log(`Ordenando por: ${sortColumn}, Dirección: ${sortDirection}`);

        currentFilteredData.sort((a, b) => {
            let valA, valB;

            // Caso especial para la columna N° (ordenar por índice original)
            if (sortColumn === 'index') {
                valA = a.originalIndex;
                valB = b.originalIndex;
            } else {
                valA = a[sortColumn];
                valB = b[sortColumn];
            }

            // Manejo de nulls/undefined (ponerlos al final)
            if (valA == null && valB == null) return 0;
            if (valA == null) return 1; // nulls van al final
            if (valB == null) return -1; // nulls van al final

            // Comparación (sensible a tipo)
            let comparison = 0;
            if (typeof valA === 'string' && typeof valB === 'string') {
                // Comparación string case-insensitive
                comparison = valA.toLowerCase().localeCompare(valB.toLowerCase());
            } else if (typeof valA === 'number' && typeof valB === 'number') {
                comparison = valA - valB;
            } else {
                // Intentar convertir a string si los tipos difieren o no son num/str
                comparison = String(valA).toLowerCase().localeCompare(String(valB).toLowerCase());
            }

            return sortDirection === 'asc' ? comparison : comparison * -1;
        });
    }

    // --- NUEVA Función Central de Renderizado (reemplaza renderTable) ---
    function renderPagedTable() {
        // Verificar si las referencias necesarias existen
        if (!equipmentTableBody || !itemsShowingSpan || !itemsTotalSpan || !currentPageDisplay || !totalPagesDisplay || typeof updatePaginationControls !== 'function' || typeof updateSortIcons !== 'function' || typeof sortData !== 'function') {
            console.error("renderPagedTable: Faltan referencias a elementos DOM o funciones helper (equipmentTableBody, spans de conteo, displays de página, updatePaginationControls, updateSortIcons, sortData).");
            return;
        }
    
        console.log(`--- renderPagedTable INVOCADA ---`);
        console.log(`  Estado Actual: currentPage=${currentPage}, itemsPerPage=${itemsPerPage}, sortColumn=${sortColumn}, sortDirection=${sortDirection}`);
        console.log(`  Filtrados Actuales (currentFilteredData): ${currentFilteredData.length} items.`);
    
        // 1. Aplicar Ordenamiento a los datos filtrados actuales
        //    sortData() debe modificar 'currentFilteredData' in-place.
        sortData(); 
    
        // 2. Calcular Paginación basada en los datos filtrados y ordenados
        const totalItems = currentFilteredData.length;
        const totalPages = Math.ceil(totalItems / itemsPerPage) || 1; // Asegurar al menos 1 página
        
        // Validar y ajustar currentPage si está fuera de rango (ej. después de filtrar)
        if (currentPage > totalPages) {
            console.log(`  Ajustando currentPage de ${currentPage} a ${totalPages}`);
            currentPage = totalPages;
        }
         if (currentPage < 1) { // Asegurar que no sea menor a 1
             currentPage = 1;
         }
    
        const startIndex = (currentPage - 1) * itemsPerPage;
        // endIndex es exclusivo, así que va hasta el índice anterior al siguiente inicio
        const endIndex = Math.min(startIndex + itemsPerPage, totalItems); 
        const itemsToShow = currentFilteredData.slice(startIndex, endIndex);
    
        console.log(`  Calculado: totalPages=${totalPages}, startIndex=${startIndex}, endIndex=${endIndex}. Mostrando ${itemsToShow.length} items.`);
    
        // 3. Limpiar Tabla y Renderizar Filas
         equipmentTableBody.innerHTML = '';
        if(selectAllCheckbox) selectAllCheckbox.checked = false; // Desmarcar "seleccionar todo" al re-renderizar
        
        if (itemsToShow.length === 0) {
            // ... (mensaje de tabla vacía) ...
            if(selectAllCheckbox) selectAllCheckbox.disabled = true;
        } else {
            if(selectAllCheckbox) selectAllCheckbox.disabled = false;
            // Verificar si todos los equipos DE LA PÁGINA ACTUAL están seleccionados
            const allOnPageSelected = itemsToShow.every(eq => selectedEquipmentIds.has(eq.id));
            if(selectAllCheckbox) selectAllCheckbox.checked = allOnPageSelected;


            const cellClassBase = "px-4 py-3 whitespace-nowrap text-sm text-center";
            const cellClassData = `${cellClassBase} text-gray-800`;
            const cellClassMono = `${cellClassData} font-mono`;

            itemsToShow.forEach((eq, index) => {
                const globalIndex = startIndex + index;
                const row = equipmentTableBody.insertRow();
                row.className = 'hover:bg-gray-100 transition duration-150';

                // Usamos innerHTML para la fila, así que debemos asegurarnos de que el checkbox tenga el ID correcto
                // y que el listener se añada DESPUÉS de que el elemento exista en el DOM.
                const isChecked = selectedEquipmentIds.has(eq.id);
                row.innerHTML = `
                    <td class="px-2 py-3 text-center"><input type="checkbox" class="row-checkbox form-checkbox h-4 w-4 text-indigo-600 rounded" value="${eq.id}" ${isChecked ? 'checked' : ''}></td>
                    <td class="${cellClassData}">${globalIndex + 1}</td>
                    <td class="${cellClassData}">${safe(eq.tipo_equipo)}</td>
                    <td class="${cellClassData}">${safe(eq.marca)}</td>
                    <td class="${cellClassData}">${safe(eq.modelo)}</td>
                    <td class="${cellClassMono}">${safe(eq.serial)}</td>
                    <td class="${cellClassData}">${safe(eq.asignado_a)}</td>
                    <td class="${cellClassData}">${safe(eq.departamento)}</td>
                    <td class="${cellClassData}">${safe(eq.sede)}</td>
                    <td class="${cellClassData}">
                        <span class="inline-block px-2.5 py-0.5 rounded-full text-xs font-medium ${getEstatusClass(eq.estatus)}">
                            ${safe(eq.estatus) || 'N/A'}
                        </span>
                    </td>
                    <td class="${cellClassData} space-x-1 actions-cell"></td>
                `;

                // Añadir listener al checkbox de la fila (debe hacerse después de innerHTML)
                const rowCheckbox = row.querySelector('.row-checkbox');
                if (rowCheckbox) {
                    rowCheckbox.addEventListener('change', (event) => {
                        const eqId = parseInt(event.target.value, 10);
                        if (event.target.checked) {
                            selectedEquipmentIds.add(eqId);
                        } else {
                            selectedEquipmentIds.delete(eqId);
                        }
                        updateBulkActionsPanel();
                        // Actualizar el checkbox "seleccionar todo" de la cabecera
                        if(selectAllCheckbox) {
                            const allOnCurrentPageChecked = itemsToShow.every(item => selectedEquipmentIds.has(item.id));
                            selectAllCheckbox.checked = allOnCurrentPageChecked;
                        }
                    });
                }
                
                // Añadir botones de acción individual
                const actionsCell = row.querySelector('.actions-cell');
                if (actionsCell) { addActionsButtons(actionsCell, eq); }
            });
        }
        updateBulkActionsPanel(); // Asegurarse de que el panel se actualice después de renderizar
    }
    function updateBulkActionsPanel() {
        if (selectedEquipmentIds.size > 0) {
            if(selectedCountSpan) selectedCountSpan.textContent = `${selectedEquipmentIds.size} equipo(s) seleccionado(s)`;
            if(bulkActionsPanel) bulkActionsPanel.classList.remove('hidden');
            // Habilitar/deshabilitar botones según permisos y si hay algo seleccionado
            const canManage = currentUserRole === 'admin' || currentUserRole === 'manager';
            if(bulkEditButton) bulkEditButton.disabled = !canManage;
            if(bulkDeleteButton) bulkDeleteButton.disabled = currentUserRole !== 'admin';
        } else {
            if(bulkActionsPanel) bulkActionsPanel.classList.add('hidden');
        }
    }

    // --- ACCIÓN: Eliminar Múltiples ---
    async function deleteSelectedEquipment() {
        if (selectedEquipmentIds.size === 0) {
            displayGeneralFeedback('warning', 'No hay equipos seleccionados para eliminar.');
            return;
        }
        if (currentUserRole !== 'admin') {
            displayGeneralFeedback('error', 'Permiso denegado para eliminar equipos.');
            return;
        }

        const confirmMessage = `¿Está seguro de que desea ELIMINAR ${selectedEquipmentIds.size} equipo(s) seleccionado(s)? Esta acción es irreversible.`;
        // Reutilizar el modal de confirmación de borrado individual, pero adaptar mensaje
        equipmentToDeleteId = null; // No hay un solo ID, se usa el Set
        deleteConfirmMessage.textContent = confirmMessage;
        showModal(deleteConfirmModal); // Abrir modal de confirmación

        // MODIFICACIÓN: La confirmación de eliminación individual/múltiple
        // La función `executeDelete` deberá ser modificada para manejar ambos casos.
        // Por ahora, simplemente llamaremos directamente si no queremos el modal de confirmación.
        // Para usar el modal de confirmación, `executeDelete` necesita saber si es bulk o no.
        
        // Temporizador para esperar la decisión del modal de confirmación
        // Esta es una solución rudimentaria, lo ideal es usar promesas o callbacks.
        // Por ahora, vamos a hacer un nuevo modal de confirmación o adaptar el existente.
        // O más simple: adaptar executeDelete para que acepte un flag 'isBulk'
    }
    // --- Funciones Helper para Renderizado ---
    function showLoadingMessage(message) {
        equipmentTableBody.innerHTML = `<tr><td colspan="9" class="text-center ...">${message}</td></tr>`;
    }
     function showEmptyMessage(message) {
        equipmentTableBody.innerHTML = `<tr><td colspan="9" class="text-center ...">${message}</td></tr>`;
    }
    function showErrorMessage(message) {
         equipmentTableBody.innerHTML = `<tr><td colspan="9" class="text-center ... text-red-600">${message}</td></tr>`;
     }

     function addActionsButtons(cell, equipment) {
        // Asegúrate que 'equipment' aquí sea el objeto correcto
        // console.log("Adding buttons for:", equipment); // Log para depurar

        const canEdit = currentUserRole === 'admin' || currentUserRole === 'manager';
        const canDelete = currentUserRole === 'admin';

        // Función interna para crear botones
        const createBtn = (title, color, icon, onClick) => {
            const btn = document.createElement('button');
            btn.title = title;
            btn.className = `text-${color}-600 dark:text-${color}-400 hover:text-${color}-900 dark:hover:text-${color}-300 transition duration-150 mx-1 focus:outline-none`;
            btn.innerHTML = `<i class="fas fa-${icon} fa-fw"></i>`;
            // Asignar la función directamente al onclick
            btn.onclick = onClick;
            // console.log(`Button '${title}' created. Onclick assigned:`, typeof onClick); // Log para depurar
            return btn;
        };

        cell.appendChild(createBtn('Ver Detalles', 'gray', 'eye', () => openViewModal(equipment)));
        if (canEdit) {
            cell.appendChild(createBtn('Editar', 'indigo', 'edit', () => openEditModal(equipment)));
        }
        if (canEdit) { // O define un nuevo permiso si es necesario
            cell.appendChild(createBtn('Registrar Mantenimiento', 'teal', 'tools', () => openMaintenanceModal(equipment)));
        }
        if (canDelete) {
            cell.appendChild(createBtn('Eliminar', 'red', 'trash', () => confirmDelete(equipment)));
        }
        cell.appendChild(createBtn('Ver Código QR', 'green', 'qrcode', () => showQrCodeModal(equipment)));
        
    }

    // --- NUEVA: Actualizar Controles de Paginación ---
    function updatePaginationControls(totalItems, totalPages) {
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = Math.min(startIndex + itemsPerPage, totalItems); // <-- FORMA CORRECTA

        if (itemsShowingSpan) itemsShowingSpan.textContent = totalItems > 0 ? `${startIndex + 1}-${endIndex}` : '0';
        if (itemsTotalSpan) itemsTotalSpan.textContent = totalItems;
        if (currentPageDisplay) currentPageDisplay.textContent = currentPage;
        if (totalPagesDisplay) totalPagesDisplay.textContent = totalPages;
        if (currentPageDisplayBottom) currentPageDisplayBottom.textContent = currentPage;
        if (totalPagesDisplayBottom) totalPagesDisplayBottom.textContent = totalPages;

        const canGoPrev = currentPage > 1;
        const canGoNext = currentPage < totalPages;

        if (prevPageButton) prevPageButton.disabled = !canGoPrev;
        if (nextPageButton) nextPageButton.disabled = !canGoNext;
        if (prevPageButtonBottom) prevPageButtonBottom.disabled = !canGoPrev;
        if (nextPageButtonBottom) nextPageButtonBottom.disabled = !canGoNext;
    }

     // --- NUEVA: Actualizar Iconos de Ordenamiento ---
     function updateSortIcons() {
        document.querySelectorAll('th.sortable-header .sort-icon').forEach(icon => {
            const header = icon.closest('th');
            const key = header.dataset.sortKey;
            icon.classList.remove('fa-sort', 'fa-sort-up', 'fa-sort-down', 'active');

            if (key === sortColumn) {
                icon.classList.add(sortDirection === 'asc' ? 'fa-sort-up' : 'fa-sort-down');
                icon.classList.add('active');
            } else {
                icon.classList.add('fa-sort'); // Icono por defecto
            }
        });
    }


    // --- Lógica Principal ---

    // Conexión a Backend y Carga Inicial
    function connectAndInitialize() {
        const tryConnect = setInterval(() => {
            if (typeof qt !== 'undefined' && qt.webChannelTransport) {
                clearInterval(tryConnect);
                console.log("Conectando a QWebChannel...");
                new QWebChannel(qt.webChannelTransport, (channel) => {
                    if (channel.objects.backend) {
                        backend = channel.objects.backend;
                        console.log("Objeto Backend conectado:", backend);

                        // Conectar señales
                        if (backend.equipment_updated) backend.equipment_updated.connect(loadAndRenderEquipment);
                        if (backend.show_message) backend.show_message.connect(displayGeneralFeedback);
                        if (backend.import_excel_finished) { // Verificar si la señal existe
                            backend.import_excel_finished.connect(handleImportResult); // Conectar al handler
                            console.log("JS: Señal 'import_excel_finished' conectada.");
                        } else {
                            console.warn("JS: Señal 'import_excel_finished' no encontrada en el backend.");
                        }

                        // Cargar datos iniciales
                        initializeSession();
                    } else {
                        console.error("Error: Objeto 'backend' no encontrado.");
                        displayGeneralFeedback('error', 'Error crítico: No se pudo conectar con el backend.');
                        equipmentTableBody.innerHTML = `<tr><td colspan="9" class="text-center py-4 text-red-500">Error de conexión con Backend.</td></tr>`;
                    }
                });
            } else {
                console.log("Esperando qt.webChannelTransport...");
            }
        }, 200);
        // Timeout opcional
        setTimeout(() => { if (!backend) { clearInterval(tryConnect); console.error("Timeout Conexión"); displayGeneralFeedback('error', 'Timeout'); }}, 10000);
        initializeTheme();
    }

    async function initializeSession() {
        if (!backend) return;
        try {
            currentUserRole = await backend.get_current_role();
            console.log("Rol obtenido:", currentUserRole);
            userRoleDisplay.textContent = currentUserRole.charAt(0).toUpperCase() + currentUserRole.slice(1);
            adjustUIVisibility();
            // Cargar datos principales y luego las sugerencias
            await loadAndRenderEquipment();
            await loadAllSuggestions(); // <-- LLAMADA A CARGAR SUGERENCIAS
        } catch (error) {
            console.error("Error inicializando sesión:", error);
            displayGeneralFeedback('error', 'Error al cargar datos iniciales.');
        }
    }
    
    let isViewingOnly = false;
    
    // Ajustar UI por Rol
     function adjustUIVisibility() {
        console.log('>>> adjustUIVisibility llamada con rol:', currentUserRole); // Verificar llamada y rol
        const adminElements = document.querySelectorAll('.requires-admin');
        const managerElements = document.querySelectorAll('.requires-manager');
        const canManage = currentUserRole === 'admin' || currentUserRole === 'manager';

        // Mostrar/Ocultar elementos Admin
        console.log(`   Ajustando ${adminElements.length} elementos 'requires-admin'. Visible: ${currentUserRole === 'admin'}`);
        adminElements.forEach(el => {
            // Usar 'inline-block' o 'block' según el tipo de elemento si es necesario
            // Para botones, 'inline-block' suele ser adecuado.
            el.style.display = (currentUserRole === 'admin') ? 'inline-block' : 'none';
        });

        // Mostrar/Ocultar elementos Manager (se muestran si es admin O manager)
        console.log(`   Ajustando ${managerElements.length} elementos 'requires-manager'. Visible: ${canManage}`);
        managerElements.forEach(el => {
             // Usar 'inline-block' o 'block'
            el.style.display = canManage ? 'inline-block' : 'none';
        });

        console.log('<<< Fin adjustUIVisibility');
    }


    // Cargar y Renderizar Tabla
    async function loadAndRenderEquipment() {
        if (!backend) return;
        // Mostrar mensaje de carga en la tabla
        showLoadingMessage("Cargando equipos...");
        try {
            allEquipmentData = await backend.get_equipment() || [];
            allEquipmentData.forEach((item, index) => item.originalIndex = index);

            // IMPORTANTE: Limpiar selección al cargar datos nuevos completamente
            selectedEquipmentIds.clear();
            if(selectAllCheckbox) selectAllCheckbox.checked = false; // Desmarcar el principal
            updateBulkActionsPanel(); // Ocultar el panel

            applyFiltersAndRender(); // Esto llamará a renderPagedTable
        } catch (error) {
            // --- Bloque CATCH ---
            console.error("Error detallado al cargar equipos:", error); // Loguear el error real del backend


            showErrorMessage("Error al cargar equipos. Verifique la conexión o consulte al administrador.");


            // Usar el mensaje de error del backend si está disponible y es útil para el usuario
            const errorMessage = error?.message || "Error desconocido al cargar datos.";
            displayGeneralFeedback('error', `Error al cargar datos: ${errorMessage}`);

            // Asegurarse que los datos cacheados se limpien para evitar mostrar datos viejos/inválidos
            allEquipmentData = [];
            currentFilteredData = [];

            // Actualizar controles para reflejar el estado vacío/error
            updatePaginationControls(0, 1); // Mostrar 0 items, 1 página
            updateFilteredInfo(); // Actualizar info de filtros (puede que no haya)
            updateSortIcons(); // Resetear iconos de ordenamiento
            // --- Fin Bloque CATCH ---
        }
     }


    // Filtrar Datos
    function filterData(data) {
        // Asegúrate que searchTermInput se referencie correctamente aquí o se pase como argumento
        const localSearchTermInput = document.getElementById('search-term'); // O usa la referencia global
        const searchTerm = localSearchTermInput ? localSearchTermInput.value.toLowerCase().trim() : ""; // Obtener valor actual
        
        console.log(`  filterData: Filtrando ${data.length} items con término: "${searchTerm}"`);
        
        if (!searchTerm) { // Si el término está vacío
            console.log("  filterData: Término vacío, devolviendo todos los datos (copia).");
            return [...data]; // Devuelve una NUEVA copia de TODOS los datos originales
        }
        
        // Si hay término, filtra
        const filtered = data.filter(eq => {
           const safeLower = (val) => (val ? String(val).toLowerCase() : '');
           // Tu lógica de filtrado...
           return safeLower(eq.serial).includes(searchTerm) ||
                  safeLower(eq.modelo).includes(searchTerm) ||
                  safeLower(eq.marca).includes(searchTerm) ||
                  safeLower(eq.asignado_a).includes(searchTerm) ||
                  safeLower(eq.tipo_equipo).includes(searchTerm) ||
                  safeLower(eq.estatus).includes(searchTerm) || 
                  safeLower(eq.departamento).includes(searchTerm) ||
                  safeLower(eq.sede).includes(searchTerm);
        });
        console.log(`  filterData: Filtrado resultó en ${filtered.length} items.`);
        return filtered;
   }

    function createActionButton(title, color, icon, onClick) {
        const btn = document.createElement('button');
        btn.title = title;
        // Clases de Tailwind para estilo y espaciado
        btn.className = `text-${color}-600 hover:text-${color}-900 transition duration-150 mx-1 focus:outline-none`;
        // Icono de Font Awesome
        btn.innerHTML = `<i class="fas fa-${icon} fa-fw"></i>`;
        // Asignar la función a ejecutar al hacer clic
        btn.onclick = onClick;
        return btn;
     }
    // Renderizar Tabla
    function renderTable(equipmentList) {
        console.log(`>>> renderTable llamada con ${equipmentList?.length ?? 0} equipos.`);
        equipmentTableBody.innerHTML = ''; // Limpiar tabla
        if (!equipmentList || equipmentList.length === 0) {
            // Usa el colspan original
            equipmentTableBody.innerHTML = '<tr><td colspan="9" class="text-center ...">No se encontraron equipos...</td></tr>';
            console.log("   Tabla vacía.");
            return;
        }
    
        equipmentList.forEach((eq, index) => {
            // console.log(`   [${index}] Renderizando fila para ID: ${eq.id}`);
            const row = equipmentTableBody.insertRow();
            row.className = 'hover:bg-gray-50 transition duration-150';
            const cellClass = "px-4 py-3 whitespace-nowrap text-sm";
            const cellClassGray = `${cellClass} text-gray-600`;
            const cellClassHeader = `${cellClass} font-medium text-gray-800`;
            const cellClassMono = `${cellClassGray} font-mono`;
    
            // --- NÚMERO DE FILA (Contador + 1) ---
            const rowNumber = index + 1;
            // --------------------------------------
    
            // Crear celdas con innerHTML, añadiendo la celda del contador
            row.innerHTML = `
                <td class="${cellClassGray} text-center">${rowNumber}</td> <!-- CONTADOR VISUAL -->
                <td class="${cellClassGray} text-center">${safe(eq.tipo_equipo)}</td>
                <td class="${cellClassGray} text-center">${safe(eq.marca)}</td>
                <td class="${cellClassGray} text-center">${safe(eq.modelo)}</td>
                <td class="${cellClassMono} text-center">${safe(eq.serial)}</td>
                <td class="${cellClassGray} text-center">${safe(eq.asignado_a)}</td>
                <td class="${cellClassGray} text-center">${safe(eq.departamento)}</td>
                <td class="${cellClassGray} text-center">
                    <span class="inline-block px-2.5 py-0.5 rounded-full text-xs font-medium ${getEstatusClass(eq.estatus)}">
                        ${safe(eq.estatus) || 'Desconocido'}
                    </span>
                </td>
                <td class="${cellClass} text-center space-x-1 actions-cell"></td>
            `;
    
            // --- Añadir Botones de Acción (como antes) ---
            const actionsCell = row.querySelector('.actions-cell');
            if (!actionsCell) { console.error(`ERROR: No se encontró .actions-cell`); return; }
            const canEdit = currentUserRole === 'admin' || currentUserRole === 'manager';
            const canDelete = currentUserRole === 'admin';
            const viewBtn = createActionButton('Ver Detalles', 'gray', 'eye', () => openViewModal(eq));
            actionsCell.appendChild(viewBtn);
            if (canEdit) { actionsCell.appendChild(createActionButton('Editar', 'indigo', 'edit', () => openEditModal(eq))); }
            if (canDelete) { actionsCell.appendChild(createActionButton('Eliminar', 'red', 'trash', () => confirmDelete(eq))); }
            actionsCell.appendChild(createActionButton('Ver Código QR', 'green', 'qrcode', () => showQrCodeModal(eq)));
        });
        console.log("<<< Fin renderTable");
    }

    // Helper para clases de estatus
    function getEstatusClass(estatus) {
        switch (estatus) {
            case 'Operativo': return 'bg-green-100 text-green-800';
            case 'En Reparación': return 'bg-yellow-100 text-yellow-800';
            case 'En Almacén': return 'bg-blue-100 text-blue-800';
            case 'Desincorporado': return 'bg-gray-100 text-gray-800';
            case 'Dañado': return 'bg-red-100 text-red-800';
            default: return 'bg-gray-100 text-gray-800';
         }
    }
    function getEstatusDarkClass(estatus) { // Ejemplo, ajustar colores!
        switch (estatus) {
            case 'Operativo': return 'bg-green-900 bg-opacity-50 text-green-200';
            case 'En Reparación': return 'bg-yellow-900 bg-opacity-50 text-yellow-200';
            case 'En Almacén': return 'bg-blue-900 bg-opacity-50 text-blue-200';
            case 'Desincorporado': return 'bg-gray-700 text-gray-300';
            case 'Dañado': return 'bg-red-900 bg-opacity-50 text-red-200';
            default: return 'bg-gray-700 text-gray-300';
         }
    }

    // --- Funciones de Modales y Formulario ---

    function openExportChoiceModal() {
        if (exportChoiceModal) { // Verificar si el modal existe
            showModal(exportChoiceModal);
        } else {
            console.error("El modal de elección de exportación no se encontró.");
            displayGeneralFeedback('error', 'Error: No se pudo abrir opciones de exportación.');
        }
    }
    
    function closeExportChoiceModal() {
        if (exportChoiceModal) {
            hideModal(exportChoiceModal);
        }
    }
    
    function handleImportResult(jsonStringResult) {
        console.log("JS: Señal import_excel_finished RECIBIDA:", jsonStringResult);
        console.log("JS: Tipo respuesta STRING (Señal):", typeof jsonStringResult);
        let result = null; // Para el objeto parseado
        try {
            if (typeof jsonStringResult === 'string' && jsonStringResult.trim() !== '') {
                // Parsear el string JSON
                result = JSON.parse(jsonStringResult);
                console.log("JS: Objeto JS parseado desde JSON string (Señal Import):", result);
            } else {
                console.warn("JS: Señal import_excel_finished recibió string vacío o no válido.");
            }
        } catch (parseError) {
            console.error("JS: Error parseando JSON string de señal import:", parseError, "String:", jsonStringResult);
            result = null; // Asegurar que es null si falla el parseo
        }
    
        // --- MANEJAR EL OBJETO 'result' PARSEADO ---
        if (result && result.message !== undefined) { // Verificar si tenemos un objeto parseado válido
            // Determinar tipo de mensaje
            const messageType = (result.errors?.length > 0 || result.db_ignored > 0 || result.batch_ignored > 0 || result.success === false) ? 'error' : 'success';
            // Mostrar feedback detallado usando la función existente
            displayImportFeedback(messageType, result.message, result);
        } else {
            // Si result es null o no tiene la estructura esperada
            console.error("Respuesta inválida o parseo fallido desde señal import:", result);
            displayImportFeedback('error', 'Respuesta inválida recibida del proceso de importación.');
        }
    
        // Re-habilitar botón y resetear input aquí, al final del flujo
        if (importExcelButton) importExcelButton.disabled = false;
        if (excelFileInput) excelFileInput.value = '';
    } // --- FIN handleImportResult ---

    // --- Función para manejar la solicitud de exportación/impresión ---
    async function handleExportRequest(format) {
        if (!backend) {
            displayGeneralFeedback('error', 'Error: No hay conexión con el backend.');
            return;
        }
        // Asumiendo que REPORTLAB_AVAILABLE es una variable global o la verificas en el backend
        // if (!REPORTLAB_AVAILABLE && format === 'table') { ... } 
    
        // --- CORRECCIÓN AQUÍ ---
        // 1. Usa la variable global que ya tiene los datos filtrados que se muestran en pantalla
        console.log("handleExportRequest: Obteniendo datos desde la variable global 'currentFilteredData'.");
        const dataToExport = [...currentFilteredData]; // Usa una copia
        console.log(`  -> Se exportarán ${dataToExport.length} registros.`);
        // ----------------------
    
        if (!dataToExport || dataToExport.length === 0) {
            displayGeneralFeedback('info', 'No hay datos en la vista actual para exportar.');
            if (closeExportChoiceModal) closeExportChoiceModal(); // Cerrar modal elección
            return;
        }
    
        console.log(`Solicitando exportación de ${dataToExport.length} registros en formato: ${format}`);
        if (closeExportChoiceModal) closeExportChoiceModal(); // Cerrar modal elección
        displayImportFeedback('info', `Generando archivo PDF (${format})... Espere por favor.`);
    
        try {
            // 2. Envía los datos CORRECTOS (dataToExport) al backend
            const jsonStringResult = await backend.export_view_to_pdf(dataToExport, format); 
            
            console.log("Resultado STRING del backend (export_view_to_pdf):", jsonStringResult); 
            console.log("Tipo de resultado STRING:", typeof jsonStringResult); 
    
            let result = null; 
            
            if (typeof jsonStringResult === 'string' && jsonStringResult.trim() !== '') {
                try {
                    result = JSON.parse(jsonStringResult); 
                    console.log("Objeto JS parseado desde JSON string:", result); 
                } catch (parseError) {
                    console.error("JS: Error parseando JSON string del backend:", parseError, "String recibido:", jsonStringResult);
                }
            } else {
                 console.warn("JS: Se recibió una respuesta vacía o no string del backend para exportación.");
            }
    
            console.log("handleExportRequest: ANTES de llamar a displayImportFeedback, result es:", JSON.stringify(result)); 
    
            if (result && result.success) { 
                console.log("handleExportRequest: Llamando displayImportFeedback para ÉXITO...");
                displayImportFeedback('success', result.message || 'Archivo PDF generado con éxito.', result); 
            } else { 
                console.log("handleExportRequest: Llamando displayImportFeedback para ERROR/FALLO...");
                let errorMessage = 'Error desconocido al generar el archivo PDF.';
                 if (result && result.message) { errorMessage = result.message; }
                 else if (result === null) { errorMessage = 'No se recibió respuesta válida del servidor para la exportación.'; } 
                 else if (result && result.success === false) { errorMessage = result.message || 'El servidor indicó un fallo en la exportación.'; }
                displayImportFeedback('error', errorMessage, result || {}); 
            }
    
        } catch (error) {
            console.error(`Error al llamar a backend.export_view_to_pdf (${format}):`, error);
            displayImportFeedback('error', `Error de comunicación al exportar PDF: ${error.message || error}`, {});
        }
    }
    
    const REPORTLAB_AVAILABLE = true;
    // --- Añadir al final del archivo, junto a los otros addEventListener ---

    darkModeToggle?.addEventListener('click', handleThemeToggle); // <-- AÑADIR ESTE
    
    if (exportButton) {
        exportButton.addEventListener('click', openExportChoiceModal);
    } else {
        console.warn("El botón principal de exportación (#export-button) no se encontró.");
    }
    
    if (closeExportChoiceButton) {
        closeExportChoiceButton.addEventListener('click', closeExportChoiceModal);
    }
    if (cancelExportChoiceButton) {
        cancelExportChoiceButton.addEventListener('click', closeExportChoiceModal);
    }
    if (exportTableButton) {
        exportTableButton.addEventListener('click', () => handleExportRequest('table'));
    }
    if (exportQrButton) {
        exportQrButton.addEventListener('click', () => handleExportRequest('qr'));
    }
    
    // Verificar que el input oculto de importación todavía tenga su listener
    if (excelFileInput) {
         excelFileInput.addEventListener('change', handleFileSelect);
    } else {
         console.warn("El input de archivo Excel (#excel-file-input) no se encontró.");
    }

    function resetForm() {
        console.log("resetForm called: Restableciendo el formulario y la UI a estado inicial (todo oculto).");
        if (equipmentForm) equipmentForm.reset();
        editingEquipmentId = null;
        isViewingOnly = false;
        if (equipmentIdInput) equipmentIdInput.value = '';
        if (modalTitle) modalTitle.textContent = 'Agregar Nuevo Equipo';
        if (saveButtonText) saveButtonText.textContent = 'Guardar';
        if (formFeedback) formFeedback.classList.add('hidden');

        // Asegurar que todos los selects, inputs y spans estén inicialmente ocultos y vacíos
        Object.keys(formInputs).forEach(fieldName => {
            const inputElement = formInputs[fieldName];
            const selectElement = formSelects[fieldName];
            const displaySpan = formDisplaySpans[fieldName];

            if (selectElement) {
                selectElement.value = "";
                selectElement.classList.add('hidden'); // Siempre oculto por defecto
            }
            if (inputElement) {
                inputElement.value = '';
                inputElement.classList.add('hidden'); // Siempre oculto por defecto
                inputElement.required = (fieldName === 'serial' || fieldName === 'tipo_equipo');
            }
            if (displaySpan) {
                displaySpan.textContent = '';
                displaySpan.classList.remove('is-active'); // <--- CRÍTICO: Remover esta clase, no añadir hidden
            }
        });

        // Asegurar que los inputs directos también estén ocultos por defecto
        const directInputs = ['serial', 'estatus', 'ultimo_mantenimiento', 'proximo_mantenimiento', 'observacion'];
        directInputs.forEach(fieldName => {
            const inputElement = formInputs[fieldName];
            const displaySpan = formDisplaySpans[fieldName];
            if (inputElement) inputElement.classList.add('hidden');
            if (displaySpan) displaySpan.classList.remove('is-active'); // <--- CRÍTICO: Remover esta clase
        });

        if (saveButton) saveButton.classList.remove('hidden');
    }

   // --- MODIFICAR openAddModal() ---
    function openAddModal() {
        console.log("openAddModal called: Preparando para agregar equipo.");
        if (currentUserRole !== 'admin' && currentUserRole !== 'manager') { displayGeneralFeedback('error', 'Permiso denegado.'); return; }
        if (!equipmentModal) { console.error("openAddModal: Elementos del modal no encontrados."); return; }

        resetForm(); // Limpia y resetea la visibilidad a "todo oculto"
        modalTitle.textContent = 'Agregar Nuevo Equipo';
        saveButtonText.textContent = 'Guardar Nuevo';
        
        loadAllSuggestions(); // Cargar/refrescar sugerencias para los selects
        setFormEnabled(true); // Establece la visibilidad para "Agregar": inputs/selects visibles, spans ocultos.
        
        showModal(equipmentModal);
        if(formInputs.tipo_equipo) formInputs.tipo_equipo.focus();
    }

    // --- MODIFICAR openEditModal() ---
    function openEditModal(equipment) {
        console.log("openEditModal called with:", equipment);
        if (currentUserRole !== 'admin' && currentUserRole !== 'manager') { displayGeneralFeedback('error', 'No tiene permiso para editar.'); return; }
        if (!equipmentModal) { console.error("Modal element not found!"); return; }

        resetForm(); // Limpia y resetea la visibilidad a "todo oculto"
        editingEquipmentId = equipment.id;
        if (equipmentIdInput) equipmentIdInput.value = equipment.id;
        if (modalTitle) modalTitle.textContent = `Editar Equipo ID: ${equipment.id}`;
        if (saveButtonText) saveButtonText.textContent = 'Actualizar Equipo';
        
        fillForm(equipment); // Llenar con datos
        loadAllSuggestions(); // Refrescar sugerencias
        setFormEnabled(true); // Establece la visibilidad para "Editar": inputs/selects visibles, spans ocultos.
        
        showModal(equipmentModal);
        if(formInputs.tipo_equipo) formInputs.tipo_equipo.focus();
    }

    // --- MODIFICAR openViewModal() ---
    async function openViewModal(equipment) {
        console.log("openViewModal called with:", equipment);
        if (!equipmentModal) { console.error("Modal de equipo no encontrado!"); return; }

        resetForm(); // Limpia y resetea la visibilidad a "todo oculto"
        isViewingOnly = true; // Establecer estado de solo lectura
        editingEquipmentId = equipment.id;
        if (equipmentIdInput) equipmentIdInput.value = equipment.id;
        if (modalTitle) modalTitle.textContent = `Detalles Equipo ID: ${equipment.id} (${safe(equipment.tipo_equipo)} - ${safe(equipment.serial)})`;
        
        fillForm(equipment); // Llenar con datos
        // NOTA: setFormEnabled(false) ahora activará los spans y ocultará lo demás.
        setFormEnabled(false); 
        
        if (maintenanceHistorySection) maintenanceHistorySection.classList.remove('hidden');
        await loadAndRenderMaintenanceHistory(equipment.id);

        showModal(equipmentModal);
    }


    // --- fillForm(equipment) -- Esta función solo llena los valores, NO CONTROLA VISIBILIDAD ---
    function fillForm(equipment) {
        console.log("fillForm called: Llenando formulario con datos de equipo.");

        // Campos directos (serial, estatus, fechas, observacion)
        const directFields = ['serial', 'estatus', 'ultimo_mantenimiento', 'proximo_mantenimiento', 'observacion'];
        directFields.forEach(fieldName => {
            const inputElement = formInputs[fieldName];
            const displaySpan = formDisplaySpans[fieldName];
            const value = safe(equipment[fieldName]);

            if (fieldName.includes('mantenimiento')) { // Aplicar formato de fecha para campos de mantenimiento
                if (inputElement) inputElement.value = value; // input type="date" sigue con YYYY-MM-DD
                if (displaySpan) displaySpan.textContent = formatIsoDateToDMY(value) || 'N/A'; // Formato DD/MM/YYYY para display
            } else { // Para otros campos no-fecha
                if (inputElement) inputElement.value = value;
                if (displaySpan) displaySpan.textContent = value || 'N/A';
            }
        });
    
        // Campos con Select + Input (tipo_equipo, marca, modelo, asignado_a, departamento, sede)
        const fieldsWithSelect = ['tipo_equipo', 'marca', 'modelo', 'asignado_a', 'departamento', 'sede']; 
        fieldsWithSelect.forEach(fieldName => {
            const selectElement = formSelects[fieldName];
            const inputElement = formInputs[fieldName];
            const displaySpan = formDisplaySpans[fieldName];
            const equipmentValue = safe(equipment[fieldName]);
            
            // Llenar el span de display SIEMPRE
            if (displaySpan) displaySpan.textContent = equipmentValue || 'N/A';

            if (selectElement && inputElement) {
                const optionExists = Array.from(selectElement.options).some(opt => opt.value === equipmentValue && opt.value !== '__nuevo__' && opt.value !== "");
    
                if (optionExists) {
                    selectElement.value = equipmentValue;
                    inputElement.value = ''; // Limpiar input de texto si el valor existe en el select
                } else if (equipmentValue) { // Hay valor, pero no está en la lista (es un valor "nuevo")
                    selectElement.value = '__nuevo__';
                    inputElement.value = equipmentValue; // Poner el valor en el input de texto
                } else { // No hay valor (equipmentValue es vacío o null)
                    selectElement.value = ""; // Seleccionar "-- Seleccione --"
                    inputElement.value = ''; // Limpiar input de texto
                }
            } else {
                console.warn(`fillForm: Elementos para '${fieldName}' (select/input) no encontrados. Solo se llenará el span.`);
            }
        });
    }

    // --- populateSelectWithNewOption (con la corrección de possibleValues) ---
    async function populateSelectWithNewOption(selectElement, inputElement, backendFunctionName, includeSelectOption = true) {
        if (!backend || !selectElement || !backend[backendFunctionName] || typeof backend[backendFunctionName] !== 'function') {
            console.error(`populateSelectWithNewOption: Invalid args for ${backendFunctionName}`);
            return;
        }
    
        console.log(`Poblando select '${selectElement.id}' (input: '${inputElement?.id || "N/A"}') llamando a backend.${backendFunctionName}...`);
        try {
            const rawResponse = await backend[backendFunctionName]();
            let values = [];
            if (rawResponse && typeof rawResponse === 'string') {
                 try { values = JSON.parse(rawResponse); } catch (e) { console.error("Error parsing JSON", e); }
            } else if (Array.isArray(rawResponse)) { values = rawResponse; }
            if (!Array.isArray(values)) { values = []; }
    
            const currentValue = selectElement.value; // Guardar valor actual
            selectElement.innerHTML = ''; // Limpiar select
    
            // 1. Opción "-- Seleccione --"
            if (includeSelectOption) {
                const selectOpt = document.createElement('option');
                selectOpt.value = "";
                let placeholderText = selectElement.id.replace('bulk-edit-', '').replace('-select', '').replace('-', ' ');
                placeholderText = placeholderText.charAt(0).toUpperCase() + placeholderText.slice(1);
                selectOpt.textContent = `-- Seleccione ${placeholderText} --`;
                selectElement.appendChild(selectOpt);
            }
            
            // 2. Opción "-- Nuevo ... --"
            if (inputElement) { // Solo añadir opción "Nuevo" si hay un input de texto asociado
                const newOpt = document.createElement('option');
                newOpt.value = "__nuevo__"; 
                let newOptionText = selectElement.id.replace('bulk-edit-', '').replace('-select', '').replace('-', ' ');
                newOptionText = newOptionText.charAt(0).toUpperCase() + newOptionText.slice(1);
                newOpt.textContent = `-- Nuevo ${newOptionText} --`; 
                selectElement.appendChild(newOpt);
            }
    
            // 3. Opciones de la base de datos (ordenadas)
            const validValues = [...new Set(values)].filter(v => v !== null && v !== undefined && String(v).trim() !== '').sort((a, b) => String(a).localeCompare(String(b), undefined, { sensitivity: 'base' }));
            validValues.forEach(value => {
                const option = document.createElement('option');
                option.value = String(value).trim();
                option.textContent = String(value).trim();
                selectElement.appendChild(option);
            });
    
            // Declarar possibleValues antes de usar
            const possibleValues = ["", "__nuevo__"].concat(validValues.map(String)); 

            // Restaurar valor previo si aún existe en las opciones, o dejar vacío
            if (possibleValues.includes(currentValue)) { 
                selectElement.value = currentValue;
            } else {
                selectElement.value = "";
            }
            
            // CRÍTICO: AL FINALIZAR EL POBLAMIENTO, SIEMPRE OCULTAR EL INPUT DE TEXTO ASOCIADO AL SELECT
            // Su visibilidad la gestionará el listener del checkbox.
            if (inputElement) {
                inputElement.classList.add('hidden');
                inputElement.value = '';
                inputElement.required = false; 
            }
    
        } catch (error) {
            console.error(`Error al poblar select '${selectElement.id}' desde ${backendFunctionName}:`, error);
            if (selectElement) {
                selectElement.innerHTML = `<option value="">-- Error al cargar --</option>`;
                selectElement.classList.remove('bg-gray-100', 'cursor-not-allowed'); // Asegurar que no se quede deshabilitado visualmente
                selectElement.disabled = false; // Asegurar que no se quede deshabilitado funcionalmente
            }
        }
    }


    // Al cerrar el modal de equipo, ocultar el historial
    function closeModal() { // Modal de equipo
        hideModal(equipmentModal);
        resetForm();
        if (maintenanceHistorySection) maintenanceHistorySection.classList.add('hidden'); // Ocultar historial
        if (maintenanceHistoryTableBody) maintenanceHistoryTableBody.innerHTML = '<tr><td colspan="4" class="text-center p-4 text-gray-500">Cargando historial...</td></tr>'; // Resetear
        if (maintenanceHistoryFeedback) maintenanceHistoryFeedback.classList.add('hidden');
    }
        function resetMaintenanceForm() {
        if (maintenanceForm) maintenanceForm.reset();
        if (maintenanceEquipmentIdInput) maintenanceEquipmentIdInput.value = '';
        if (maintenanceEquipmentInfo) maintenanceEquipmentInfo.textContent = '-';
        currentEquipmentForMaintenance = null;
        if (maintenanceFormFeedback) {
            maintenanceFormFeedback.classList.add('hidden');
            maintenanceFormFeedback.textContent = '';
        }
        // Poner fecha actual por defecto
        if(maintenanceFechaRealizadoInput) maintenanceFechaRealizadoInput.valueAsDate = new Date();
    }

    function openMaintenanceModal(equipment) {
        if (currentUserRole !== 'admin' && currentUserRole !== 'manager') {
            displayGeneralFeedback('error', 'Permiso denegado.'); // Usar un feedback general
            return;
        }
        if (!maintenanceModal || !equipment) {
            console.error("Modal de mantenimiento o datos del equipo no disponibles.");
            return;
        }
        resetMaintenanceForm();
        currentEquipmentForMaintenance = equipment; // Guardar el equipo actual
        if (maintenanceEquipmentIdInput) maintenanceEquipmentIdInput.value = equipment.id;
        if (maintenanceModalTitle) maintenanceModalTitle.textContent = `Registrar Mantenimiento para ID: ${equipment.id}`;
        if (maintenanceEquipmentInfo) maintenanceEquipmentInfo.textContent = `${safe(equipment.tipo_equipo)} - Serial: ${safe(equipment.serial)}`;
        
        showModal(maintenanceModal);
        if(maintenanceFechaRealizadoInput) maintenanceFechaRealizadoInput.focus();
    }

    function closeMaintenanceModalAction() {
        hideModal(maintenanceModal);
        resetMaintenanceForm();
    }

    async function handleMaintenanceFormSubmit(event) {
        event.preventDefault();
        if (!backend || !currentEquipmentForMaintenance) {
            displayMaintenanceFormFeedback('error', 'Error de conexión o equipo no seleccionado.');
            return;
        }

        const equipmentId = parseInt(maintenanceEquipmentIdInput.value, 10);
        const fechaRealizado = maintenanceFechaRealizadoInput.value; // YYYY-MM-DD
        const tipoMantenimiento = maintenanceTipoInput.value.trim();
        const descripcion = maintenanceDescripcionInput.value.trim();
        const proximoMeses = maintenanceProximoMesesInput.value.trim(); // Puede ser "" o "0"

        if (!fechaRealizado) {
            displayMaintenanceFormFeedback('error', 'La fecha de realización es obligatoria.');
            return;
        }
        // Validación opcional para proximoMeses si se ingresa algo no numérico
        if (proximoMeses && isNaN(parseInt(proximoMeses, 10))) {
            displayMaintenanceFormFeedback('error', "Próximo en meses debe ser un número (o vacío/cero).");
            return;
        }


        console.log("Enviando datos de mantenimiento:", { equipmentId, fechaRealizado, tipoMantenimiento, descripcion, proximoMeses });
        displayMaintenanceFormFeedback('info', 'Guardando mantenimiento...');
        if (saveMaintenanceButton) saveMaintenanceButton.disabled = true;

        try {
            const jsonResponse = await backend.add_maintenance_record(
                equipmentId,
                fechaRealizado,
                tipoMantenimiento,
                descripcion,
                proximoMeses // Enviar como string, el backend lo parseará
            );
            const result = JSON.parse(jsonResponse);

            if (result.success) {
                displayMaintenanceFormFeedback('success', result.message);
                // La señal equipment_updated debería refrescar la tabla principal.
                // Si el modal de detalles del equipo está abierto, podríamos refrescar su historial también.
                if (editingEquipmentId === equipmentId && !equipmentModal.classList.contains('hidden') && isViewingOnly) {
                    await loadAndRenderMaintenanceHistory(equipmentId); // Refrescar historial si se está viendo
                }
                setTimeout(() => { // Cerrar modal después de un breve delay
                    closeMaintenanceModalAction();
                }, 1500);
            } else {
                displayMaintenanceFormFeedback('error', result.message || "Error guardando mantenimiento.");
            }
        } catch (error) {
            console.error("Error al guardar mantenimiento:", error);
            displayMaintenanceFormFeedback('error', `Error de comunicación: ${error.message || error}`);
        } finally {
            if (saveMaintenanceButton) saveMaintenanceButton.disabled = false;
        }
    }

    function displayMaintenanceFormFeedback(type, message) {
        if (!maintenanceFormFeedback) return;
        maintenanceFormFeedback.textContent = message;
        maintenanceFormFeedback.className = 'mb-4 p-3 rounded text-sm'; // Reset
        if (type === 'success') maintenanceFormFeedback.classList.add('bg-green-100', 'text-green-700');
        else if (type === 'error') maintenanceFormFeedback.classList.add('bg-red-100', 'text-red-700');
        else maintenanceFormFeedback.classList.add('bg-blue-100', 'text-blue-700'); // info
        maintenanceFormFeedback.classList.remove('hidden');
    }
    // -----------------------------------------------------


    // --- NUEVAS FUNCIONES PARA CARGAR Y RENDERIZAR HISTORIAL ---
    async function loadAndRenderMaintenanceHistory(equipmentId) {
        if (!backend || !maintenanceHistoryTableBody || !maintenanceHistoryFeedback) return;

        maintenanceHistoryTableBody.innerHTML = '<tr><td colspan="4" class="text-center p-4 text-gray-500">Cargando historial...</td></tr>';
        maintenanceHistoryFeedback.classList.add('hidden');

        try {
            const jsonResponse = await backend.get_maintenance_history(equipmentId);
            const result = JSON.parse(jsonResponse);

            if (result.success && result.history) {
                renderMaintenanceHistory(result.history);
                if (result.history.length === 0) {
                    maintenanceHistoryFeedback.textContent = "No hay registros de mantenimiento para este equipo.";
                    maintenanceHistoryFeedback.className = 'mb-3 p-2 rounded text-sm bg-blue-50 text-blue-700'; // Info
                    maintenanceHistoryFeedback.classList.remove('hidden');
                }
            } else {
                maintenanceHistoryTableBody.innerHTML = '<tr><td colspan="4" class="text-center p-4 text-red-500">Error al cargar historial.</td></tr>';
                maintenanceHistoryFeedback.textContent = result.error || "Error desconocido al cargar historial.";
                maintenanceHistoryFeedback.className = 'mb-3 p-2 rounded text-sm bg-red-100 text-red-700'; // Error
                maintenanceHistoryFeedback.classList.remove('hidden');
            }
        } catch (error) {
            console.error("Error al cargar historial de mantenimiento:", error);
            maintenanceHistoryTableBody.innerHTML = '<tr><td colspan="4" class="text-center p-4 text-red-500">Error de comunicación.</td></tr>';
            maintenanceHistoryFeedback.textContent = `Error de comunicación: ${error.message}`;
            maintenanceHistoryFeedback.className = 'mb-3 p-2 rounded text-sm bg-red-100 text-red-700';
            maintenanceHistoryFeedback.classList.remove('hidden');
        }
    }

    function renderMaintenanceHistory(historyArray) {
        if (!maintenanceHistoryTableBody) return;
        maintenanceHistoryTableBody.innerHTML = ''; // Limpiar

        if (historyArray.length === 0) {
            // El feedback ya se maneja en loadAndRenderMaintenanceHistory
            maintenanceHistoryTableBody.innerHTML = '<tr><td colspan="4" class="text-center p-4 text-gray-500">No hay registros.</td></tr>';
            return;
        }

        historyArray.forEach(record => {
            const row = maintenanceHistoryTableBody.insertRow();
            row.className = "hover:bg-gray-50";
            row.innerHTML = `
                <td class="px-4 py-2 whitespace-nowrap">${safe(record.fecha_realizado)}</td>
                <td class="px-4 py-2">${safe(record.tipo_mantenimiento) || '-'}</td>
                <td class="px-4 py-2 max-w-xs truncate" title="${safe(record.descripcion)}">${safe(record.descripcion) || '-'}</td>
                <td class="px-4 py-2 whitespace-nowrap">${safe(record.realizado_por_username) || 'Sistema'}</td>
            `;
        });
    }
    // -----------------------------------------------------------


    // --- ASIGNACIÓN DE EVENT LISTENERS (Añadir para nuevo modal) ---
    // ... (listeners existentes para equipmentModal, form, delete, QR, etc.) ...
    if (closeModalButton) closeModalButton.addEventListener('click', closeModal); // Modificada para ocultar historial
    if (cancelModalButton) cancelModalButton.addEventListener('click', closeModal); // Modificada

    if (closeMaintenanceModalButton) closeMaintenanceModalButton.addEventListener('click', closeMaintenanceModalAction);
    if (cancelMaintenanceModalButton) cancelMaintenanceModalButton.addEventListener('click', closeMaintenanceModalAction);
    if (maintenanceForm) maintenanceForm.addEventListener('submit', handleMaintenanceFormSubmit);
    
    // ... (connectAndInitialize y el resto del script como antes) ...
    // No olvides llamar a connectAndInitialize()
    connectAndInitialize(); 


    async function handleFormSubmit(event) {
        event.preventDefault(); // Prevenir envío HTML normal
        console.log("--- handleFormSubmit INVOCADO ---");
    
        if (isViewingOnly) {
            console.log("  -> Modo solo vista, saliendo.");
            return; // No hacer nada si solo se está viendo
        }
        if (currentUserRole !== 'admin' && currentUserRole !== 'manager') {
            displayFormFeedback('error', 'Permiso denegado para guardar.');
            console.log("  -> Permiso denegado.");
            return;
        }
    
        // Verificar que las referencias necesarias existen
        if (!equipmentForm || !saveButton || !formSelects || !formInputs) {
             displayFormFeedback('error', 'Error interno: Elementos del formulario no encontrados.');
             console.error("  -> Error: Elementos del formulario (form, botón, selects, inputs) no referenciados.");
             return;
        }
        
        // --- 1. Recolectar Datos del Formulario ---
        const formData = new FormData(equipmentForm);
        const data = {};
        formData.forEach((value, key) => {
            // Ignorar los selects auxiliares (ej. 'marca_select')
            if (!key.endsWith('_select')) {
                const processedValue = (typeof value === 'string') ? value.trim() : value;
                 // Tratar campos específicos vacíos como null
                 if ((key === 'n_producto' || key === 'ultimo_mantenimiento' || key === 'proximo_mantenimiento') && processedValue === '') {
                     data[key] = null;
                 } else if (key !== 'equipment_id') { // Ignorar el ID del form
                     data[key] = processedValue;
                 }
            }
        });
    
        // --- 2. Corregir Valores basados en la Selección del Select ---
        let validationError = false;
        Object.keys(formSelects).forEach(fieldName => {
             const selectElement = formSelects[fieldName];
             const inputElement = formInputs[fieldName];
             const isRequired = (fieldName === 'tipo_equipo'); // Marcar campos requeridos
    
             if (selectElement && inputElement) {
                if (selectElement.value === '__nuevo__') {
                    // Valor ya está en data[fieldName] desde el input. Validar si no está vacío y es requerido.
                    if (isRequired && !data[fieldName]) {
                        displayFormFeedback('error', `El nuevo valor para '${fieldName.replace('_', ' ')}' es obligatorio.`);
                        console.log(`  -> Validación fallida: Nuevo valor para ${fieldName} está vacío.`);
                        validationError = true;
                    }
                } else if (selectElement.value) {
                    // Se seleccionó una opción existente. Usar valor del select.
                    data[fieldName] = selectElement.value;
                } else {
                    // Se dejó en "-- Seleccione --". Poner null o ''.
                    data[fieldName] = null; // O ''
                    if (isRequired) { // Validar si era requerido y quedó vacío
                         displayFormFeedback('error', `El campo '${fieldName.replace('_', ' ')}' es obligatorio.`);
                         console.log(`  -> Validación fallida: Campo requerido ${fieldName} está vacío (select).`);
                         validationError = true;
                    }
                }
             }
        });
    
        // Detener si hubo error de validación en los campos nuevos/vacíos requeridos
        if (validationError) {
            console.log("  -> Saliendo debido a error de validación (select/nuevo).");
            return; 
        }
        
        // --- 3. Validación Estándar Adicional ---
        if (!data.serial || String(data.serial).trim() === "") { // <<< ASEGURAR VALIDACIÓN DE SERIAL VACÍO
            displayFormFeedback('error', 'Serial es obligatorio y no puede estar vacío.');
            console.log("  -> Validación fallida: Serial vacío (JS).");
            // Re-habilitar botón si la validación falla aquí mismo
            if(saveButton) {
                 saveButton.disabled = false;
                 saveButton.classList.remove('opacity-50', 'cursor-not-allowed');
            }
            return;
        }
        // Asegurarse que tipo_equipo (después de la corrección) tenga valor
        if (!data.tipo_equipo) {
             displayFormFeedback('error', 'Tipo Equipo es obligatorio.');
             console.log("  -> Validación fallida: Tipo Equipo vacío (después de corrección).");
             return;
        }
    
        // --- 4. Preparar y Enviar ---
        const currentId = editingEquipmentId; // Usar el ID guardado al abrir el modal
        console.log(`  -> Preparando para ${currentId ? 'actualizar ID: ' + currentId : 'agregar nuevo'}.`);
        console.log("  -> Datos finales a enviar:", data);
    
        saveButton.disabled = true; // Deshabilitar botón antes de la llamada async
        saveButton.classList.add('opacity-50', 'cursor-not-allowed'); // Estilo visual
    
        try {
            const jsonDataString = JSON.stringify(data);
            console.log("  -> Enviando JSON string a Python:", jsonDataString);
    
            // --- USANDO ASYNC/AWAIT (el backend devuelve bool directamente) ---
            console.log("  -> Llamando al backend con await (esperando booleano)...");
            let success_flag = false; 
    
            if (currentId) {
                console.log(`     Llamando: await backend.update_equipment(${currentId}, ...)`);
                success_flag = await backend.update_equipment(currentId, jsonDataString); 
            } else {
                console.log("     Llamando: await backend.add_equipment(...)");
                success_flag = await backend.add_equipment(jsonDataString); 
            }
    
            console.log("  <- Resultado booleano recibido del backend:", success_flag);
            console.log("  <- Tipo de resultado:", typeof success_flag);
    
            // --- 5. Manejar el Resultado ---
        if (success_flag === true) {
            console.log("  <- Éxito reportado por backend.");
            hideModal(equipmentModal);
            const successMessage = currentId ? 'Equipo actualizado correctamente.' : 'Equipo agregado correctamente.';
            displayImportFeedback('success', successMessage);
        } else { // success_flag es false o un valor inesperado (null, undefined, etc.)
            console.log("  <- Fallo reportado por backend (false o valor inesperado).");
            // Determinar el mensaje de error más específico si es posible
            let errorMessage = 'Error al guardar. Verifique los datos.';
            // Si el backend pudiera devolver un objeto con un mensaje de error específico, sería ideal.
            // Por ahora, asumimos que `false` puede significar serial duplicado.
            // Esto es una suposición, sería mejor si el backend fuera más explícito.
            if (success_flag === false) { // Específicamente si el backend devolvió false
                errorMessage = 'Error al guardar. Es posible que el serial ya exista o haya un problema con los datos ingresados. Por favor, revise.';
            }
            displayFormFeedback('error', errorMessage);
        }
            // --- Fin Async/Await ---
    
        } catch (error) {
            // Error durante la llamada await o JSON.stringify
            console.error("  <- ERROR durante llamada async o procesamiento:", error);
            displayFormFeedback('error', `Error de comunicación o procesamiento: ${error.message || 'Error desconocido'}`);
        } finally {
            // Re-habilitar el botón en cualquier caso (éxito, fallo o excepción)
            if(saveButton) {
                 saveButton.disabled = false;
                 saveButton.classList.remove('opacity-50', 'cursor-not-allowed');
                 console.log("  -> Botón Guardar re-habilitado.");
            }
        }
        console.log("--- handleFormSubmit FINALIZADO ---");
    }
    
    function filterMaintenance() {
        console.log("--- filterMaintenance INVOCADA ---");
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0); 
    
        const pendientes = allEquipmentData.filter(eq => {
            if (!eq.proximo_mantenimiento) return false;
            try {
                const parts = eq.proximo_mantenimiento.split('-');
                if (parts.length === 3) {
                    const fechaProxMantenimiento = new Date(Date.UTC(parts[0], parts[1] - 1, parts[2]));
                    const hoyUTC = new Date(Date.UTC(hoy.getFullYear(), hoy.getMonth(), hoy.getDate()));
                    return fechaProxMantenimiento <= hoyUTC;
                }
                return false;
            } catch (e) { return false; }
        });
    
        console.log(`  Mantenimientos pendientes encontrados: ${pendientes.length}`);
    
        // --- PASOS CLAVE ---
        // 1. Actualizar los datos a mostrar
        currentFilteredData = pendientes; 
        // 2. Resetear página
        currentPage = 1; 
        // 3. Renderizar la tabla con estos datos
        renderPagedTable(); 
        // 4. Actualizar información de filtros
        updateFilteredInfo(true); // Pasar true para indicar filtro especial
        // --------------------
    
        // Opcional: Mostrar feedback general
        // displayGeneralFeedback('info', `Mostrando ${pendientes.length} equipos con mantenimiento pendiente.`);
        
        console.log("--- filterMaintenance FINALIZADA ---");
    }

    function setFormEnabled(enabled) {
        console.log(`setFormEnabled called: enabled=${enabled} (isViewingOnly=${isViewingOnly})`);

        Object.keys(formInputs).forEach(fieldName => {
            const inputElement = formInputs[fieldName];
            const selectElement = formSelects[fieldName];
            const displaySpan = formDisplaySpans[fieldName];

            if (!inputElement || !displaySpan) { 
                console.warn(`setFormEnabled: Faltan elementos DOM para campo '${fieldName}'. Saltando.`);
                return;
            }

            // Primero, restablecemos la visibilidad y estado para este campo
            // Aseguramos que el span de display esté OCULTO por si acaso
            displaySpan.classList.remove('is-active'); // <--- CRÍTICO: Asegurar que el span no esté activo

            // Lógica principal de visibilidad y habilitación
            if (enabled) { // Modo Editar o Agregar
                inputElement.disabled = false; // Habilitar input
                inputElement.classList.remove('hidden'); // Mostrar input principal

                if (selectElement) { // Si el campo tiene un select
                    selectElement.classList.remove('hidden'); // Mostrar el select
                    // Mostrar input de texto de "nuevo valor" SOLO si el select está en "__nuevo__"
                    if (selectElement.value === '__nuevo__') {
                        inputElement.classList.remove('hidden');
                    } else { // Si no es "__nuevo__", ocultar el input de texto
                        inputElement.classList.add('hidden');
                    }
                }
                
                // Ajustar 'required' para los inputs editables
                if (fieldName === 'serial' || fieldName === 'tipo_equipo') {
                    inputElement.required = true;
                } else {
                    inputElement.required = false; // Asegurar que otros no sean requeridos
                }

            } else { // Modo Ver (enabled === false)
                displaySpan.classList.add('is-active'); // <--- CRÍTICO: Activar el span de display
                inputElement.classList.add('hidden'); // Ocultar input principal (ya deshabilitado)
                inputElement.disabled = true; // Deshabilitar input principal
                if (selectElement) selectElement.classList.add('hidden'); // Ocultar el select
            }
        });

        // Asegurar que el botón Guardar se muestre o no según el modo
        if(saveButton) {
             if (!enabled && isViewingOnly) { // Modo "Ver"
                 saveButton.classList.add('hidden');
             } else { // Modo "Agregar" o "Editar"
                 saveButton.classList.remove('hidden');
             }
        }
        if(saveButton) saveButton.disabled = !enabled;
    }
    

    // Confirmación de Borrado
    function confirmDelete(equipment) {
        if (currentUserRole !== 'admin') return;
        equipmentToDeleteId = equipment.id;
        deleteConfirmMessage.textContent = `¿Está seguro de que desea eliminar el equipo "${safe(equipment.tipo_equipo)} ${safe(equipment.serial)}" (ID: ${equipment.id})?`;
        showModal(deleteConfirmModal);
    }

     function cancelDeleteAction() {
         hideModal(deleteConfirmModal);
         equipmentToDeleteId = null;
     }

    async function executeDelete() {
        if (!backend) return;

        let idsToDelete = [];
        let isBulkDelete = false;

        if (equipmentToDeleteId !== null) { // Eliminación individual
            idsToDelete.push(equipmentToDeleteId);
            isBulkDelete = false;
        } else if (selectedEquipmentIds.size > 0) { // Eliminación múltiple
            idsToDelete = Array.from(selectedEquipmentIds);
            isBulkDelete = true;
        } else {
            console.warn("No hay IDs para eliminar.");
            hideModal(deleteConfirmModal);
            return;
        }

        if (currentUserRole !== 'admin') {
            displayGeneralFeedback('error', 'Permiso denegado para eliminar equipos.');
            hideModal(deleteConfirmModal);
            return;
        }

        console.log(`Confirmado eliminar ${idsToDelete.length} equipo(s):`, idsToDelete);
        hideModal(deleteConfirmModal); // Ocultar modal inmediatamente

        try {
            // Asumimos que backend.delete_equipment ahora puede manejar una lista de IDs
            // Si tu backend solo espera un ID a la vez, necesitarás un nuevo slot en backend_handler.py
            // (ej. `bulk_delete_equipment(ids_list_json)`) o llamar `delete_equipment` en un bucle.
            // Por simplicidad y eficiencia, crearemos un nuevo slot en el backend.

            const jsonResponse = await backend.bulk_delete_equipment(JSON.stringify(idsToDelete)); // Nuevo slot
            const result = JSON.parse(jsonResponse);

            if (result.success) {
                displayGeneralFeedback('success', result.message);
                // Limpiar selección después de eliminar
                selectedEquipmentIds.clear();
                updateBulkActionsPanel(); // Ocultar panel
                // Refrescar la tabla completa
                loadAndRenderEquipment();
            } else {
                displayGeneralFeedback('error', result.message || 'Error al eliminar equipos.');
            }
        } catch (error) {
            console.error("Error al eliminar:", error);
            displayGeneralFeedback('error', `Error al eliminar: ${error}`);
        } finally {
            equipmentToDeleteId = null; // Limpiar ID a borrar
        }
    }
    async function openBulkEditModal() {
        console.log("openBulkEditModal called.");
        if (selectedEquipmentIds.size === 0) {
            displayGeneralFeedback('warning', 'No hay equipos seleccionados para editar.');
            return;
        }
        if (currentUserRole !== 'admin' && currentUserRole !== 'manager') {
            displayGeneralFeedback('error', 'Permiso denegado para edición múltiple.');
            return;
        }

        if(bulkEditCountSpan) bulkEditCountSpan.textContent = selectedEquipmentIds.size;
        resetBulkEditForm(); // Limpiar y deshabilitar campos del modal

        console.log("Cargando sugerencias para bulk edit selects...");
        try {
            // Pasamos null para inputElement si el select no tiene un input de texto asociado
            // o pasamos el input de texto asociado si existe.
            await Promise.all([
                populateSelectWithNewOption(bulkEditFields.departamento.select, bulkEditFields.departamento.input, 'get_distinct_departamentos'),
                populateSelectWithNewOption(bulkEditFields.sede.select, bulkEditFields.sede.input, 'get_distinct_sedes')
            ]);
            console.log("Sugerencias de edición múltiple cargadas exitosamente.");
        } catch (error) {
            console.error("Error cargando sugerencias para edición múltiple:", error);
            displayBulkEditFormFeedback('error', 'Error al cargar opciones para Departamento/Sede.');
        }

        showModal(bulkEditModal);
    }
    function resetBulkEditForm() {
        console.log("resetBulkEditForm called: Reseteando modal de edición múltiple.");
        if(bulkEditForm) bulkEditForm.reset();
        if(bulkEditFormFeedback) bulkEditFormFeedback.classList.add('hidden');
        
        Object.values(bulkEditFields).forEach(field => {
            // Aseguramos que el checkbox esté desmarcado
            if(field.checkbox) field.checkbox.checked = false;

            // Restablecemos el estado y apariencia de los campos asociados a los checkboxes
            // Esto incluye el select (si existe) y el input de texto asociado
            const inputEl = field.input;
            const selectEl = field.select;

            if (inputEl) {
                inputEl.disabled = true;
                inputEl.classList.add('bg-gray-100', 'cursor-not-allowed');
                inputEl.value = '';
                inputEl.classList.add('hidden'); // Ocultar input de texto por defecto
            }
            if (selectEl) {
                selectEl.disabled = true;
                selectEl.classList.add('bg-gray-100', 'cursor-not-allowed');
                selectEl.value = ''; // Limpiar select
                selectEl.classList.add('hidden'); // Ocultar select por defecto
            }
            // Para la observación, si tiene un campo de texto directo
            if (field.input && field.input.type === 'textarea') {
                field.input.classList.add('bg-gray-100', 'cursor-not-allowed');
            }
        });
        if(saveBulkEditButton) saveBulkEditButton.disabled = false;
    }


    // --- MODIFICAR el listener del checkbox de Edición Múltiple ---
    Object.values(bulkEditFields).forEach(field => {
        if (field.checkbox) {
            field.checkbox.addEventListener('change', (event) => {
                const checked = event.target.checked;
                const inputEl = field.input;
                const selectEl = field.select;

                if (inputEl) {
                    inputEl.disabled = !checked; // Habilita/Deshabilita el input
                    if (checked) {
                        inputEl.classList.remove('bg-gray-100', 'cursor-not-allowed');
                        if (!selectEl) inputEl.classList.remove('hidden'); // Mostrar input si no hay select (ej. Observación, Estatus)
                    } else {
                        inputEl.classList.add('bg-gray-100', 'cursor-not-allowed');
                        inputEl.value = ''; // Limpiar valor si se deshabilita
                        if (!selectEl) inputEl.classList.add('hidden'); // Ocultar input si no hay select
                    }
                }

                if (selectEl) {
                    selectEl.disabled = !checked; // Habilita/Deshabilita el select
                    if (checked) {
                        selectEl.classList.remove('bg-gray-100', 'cursor-not-allowed');
                        selectEl.classList.remove('hidden'); // Mostrar el select
                        // Lógica para select+input combinado
                        if (selectEl.value === '__nuevo__') {
                            inputEl.classList.remove('hidden'); // Mostrar input si es 'nuevo'
                        } else {
                            inputEl.classList.add('hidden'); // Ocultar input si no es 'nuevo'
                        }
                    } else { // Si se desmarca el checkbox
                        selectEl.classList.add('bg-gray-100', 'cursor-not-allowed');
                        selectEl.value = ''; // Limpiar select
                        selectEl.classList.add('hidden'); // Ocultar select
                        if (inputEl) { // Ocultar input asociado
                            inputEl.classList.add('hidden');
                            inputEl.value = '';
                        }
                    }
                }
            });
        }
    });


        async function loadAllBulkEditSuggestions() {
        if (!backend) { console.error("Backend no disponible para bulk edit suggestions."); return; }
        try {
            // Poblar selects específicos para edición múltiple
            // Asegúrate que los IDs de los selects en el HTML del modal bulk-edit sean únicos
            await Promise.all([
                populateSelectWithNewOption(bulkEditFields.departamento.select, bulkEditFields.departamento.input, 'get_distinct_departamentos', false), // No incluir "-- Seleccione --" si ya lo tiene el select.value = ""
                populateSelectWithNewOption(bulkEditFields.sede.select, bulkEditFields.sede.input, 'get_distinct_sedes', false)
            ]);
        } catch (error) {
            console.error("Error cargando sugerencias para edición múltiple:", error);
        }
    }


    function handleBulkEditSelectChange(event) {
        const selectElement = event.target;
        let fieldName = null;
        if (selectElement.id === 'bulk-edit-departamento') fieldName = 'departamento';
        else if (selectElement.id === 'bulk-edit-sede') fieldName = 'sede';

        if (!fieldName) return;

        const fieldConfig = bulkEditFields[fieldName];
        const inputElement = fieldConfig.input;

        if (inputElement) {
            if (selectElement.value === '__nuevo__') {
                inputElement.classList.remove('hidden');
                inputElement.value = '';
                // Asegurarse de que no esté deshabilitado si se seleccionó 'nuevo'
                inputElement.disabled = false; 
                inputElement.classList.remove('bg-gray-100', 'cursor-not-allowed');
            } else { // Si se selecciona una opción existente o "-- Seleccione --"
                inputElement.classList.add('hidden'); // Ocultar el input de texto
                inputElement.value = ''; // Limpiar su valor
            }
        }
    }
    // Añadir listeners de cambio a los selects en el modal de bulk edit
    if (bulkEditFields.departamento.select) bulkEditFields.departamento.select.addEventListener('change', handleBulkEditSelectChange);
    if (bulkEditFields.sede.select) bulkEditFields.sede.select.addEventListener('change', handleBulkEditSelectChange);


    // --- ENVIAR CAMBIOS DE EDICIÓN MÚLTIPLE ---
    async function handleBulkEditFormSubmit(event) {
        event.preventDefault();
        if (!backend || selectedEquipmentIds.size === 0) {
            displayBulkEditFormFeedback('error', 'No hay equipos seleccionados o conexión con el backend.');
            return;
        }

        const idsToUpdate = Array.from(selectedEquipmentIds);
        const updates = {};
        let fieldsToUpdateCount = 0;

        // Recopilar los valores de los campos que tienen su checkbox marcado
        Object.keys(bulkEditFields).forEach(fieldName => {
            const field = bulkEditFields[fieldName];
            if (field.checkbox && field.checkbox.checked) {
                let valueToUse = null;
                if (fieldName === 'estatus' || fieldName === 'observacion') {
                    valueToUse = field.input.value.trim();
                    if (fieldName === 'observacion' && valueToUse === '') valueToUse = null; // Permitir borrar observación
                } else if (field.select) { // Para departamento y sede
                    if (field.select.value === '__nuevo__') {
                        valueToUse = field.input.value.trim();
                        if (valueToUse === '') {
                            displayBulkEditFormFeedback('error', `El nuevo valor para '${fieldName}' es obligatorio.`);
                            return; // Salir de la función si hay un campo nuevo vacío
                        }
                    } else if (field.select.value === "") {
                        valueToUse = null; // Si se seleccionó "-- Seleccione --"
                    } else {
                        valueToUse = field.select.value;
                    }
                }
                
                // Solo añadir a updates si valueToUse no es null/undefined (o si es null intencional como observacion)
                if (valueToUse !== null || (fieldName === 'observacion' && field.input.value === '')) {
                     updates[fieldName] = valueToUse;
                     fieldsToUpdateCount++;
                }
            }
        });

        if (fieldsToUpdateCount === 0) {
            displayBulkEditFormFeedback('warning', 'Seleccione al menos un campo para editar.');
            return;
        }

        console.log("Bulk Update: IDs:", idsToUpdate, "Updates:", updates);
        displayBulkEditFormFeedback('info', `Aplicando cambios a ${idsToUpdate.length} equipos...`);
        if(saveBulkEditButton) saveBulkEditButton.disabled = true;

        try {
            // Nuevo slot en el backend: update_multiple_equipment(ids_json_string, updates_json_string)
            const jsonResponse = await backend.update_multiple_equipment(JSON.stringify(idsToUpdate), JSON.stringify(updates));
            const result = JSON.parse(jsonResponse);

            if (result.success) {
                displayBulkEditFormFeedback('success', result.message);
                selectedEquipmentIds.clear(); // Limpiar selección
                updateBulkActionsPanel(); // Ocultar panel de bulk actions
                loadAndRenderEquipment(); // Recargar la tabla
                setTimeout(() => hideModal(bulkEditModal), 1500);
            } else {
                displayBulkEditFormFeedback('error', result.message || 'Error al aplicar edición múltiple.');
            }
        } catch (error) {
            console.error("Error en edición múltiple:", error);
            displayBulkEditFormFeedback('error', `Error de comunicación: ${error.message || error}`);
        } finally {
            if(saveBulkEditButton) saveBulkEditButton.disabled = false;
        }
    }

    function displayBulkEditFormFeedback(type, message) {
        if (!bulkEditFormFeedback) return;
        bulkEditFormFeedback.textContent = message;
        bulkEditFormFeedback.className = 'mb-4 p-3 rounded text-sm';
        if (type === 'success') bulkEditFormFeedback.classList.add('bg-green-100', 'text-green-700');
        else if (type === 'error') bulkEditFormFeedback.classList.add('bg-red-100', 'text-red-700');
        else bulkEditFormFeedback.classList.add('bg-blue-100', 'text-blue-700');
        bulkEditFormFeedback.classList.remove('hidden');
        setTimeout(() => bulkEditFormFeedback.classList.add('hidden'), 5000);
    }

    // --- ASIGNACIÓN DE EVENT LISTENERS (Añadir para nueva funcionalidad) ---
    // Checkbox de seleccionar todo
     if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', (event) => {
            const isChecked = event.target.checked;
            // Iterar SOLO sobre los equipos actualmente mostrados en la tabla
            document.querySelectorAll('#equipment-table-body .row-checkbox').forEach(checkbox => {
                const eqId = parseInt(checkbox.value, 10);
                if (isChecked) {
                    selectedEquipmentIds.add(eqId);
                } else {
                    selectedEquipmentIds.delete(eqId);
                }
                checkbox.checked = isChecked; // Asegurar que el checkbox de la fila se actualice
            });
            updateBulkActionsPanel(); // Actualizar el panel
        });
    }

    // Botones del panel de acciones múltiples
    if(bulkEditButton) bulkEditButton.addEventListener('click', openBulkEditModal);
    if(bulkDeleteButton) bulkDeleteButton.addEventListener('click', deleteSelectedEquipment); // Llama a la función que inicia el proceso de borrado múltiple

    // Botones del modal de edición múltiple
    if(closeBulkEditModalButton) closeBulkEditModalButton.addEventListener('click', () => hideModal(bulkEditModal));
    if(cancelBulkEditButton) cancelBulkEditButton.addEventListener('click', () => hideModal(bulkEditModal));
    if(bulkEditForm) bulkEditForm.addEventListener('submit', handleBulkEditFormSubmit);
     // Modal QR
     async function showQrCodeModal(equipment) {
         if (!backend) return;
         qrModalTitle.textContent = `Código QR - Equipo ID: ${equipment.id}`;
         qrModalInfo.textContent = `Serial: ${safe(equipment.serial)}\nAsignado: ${safe(equipment.asignado_a)}`;
         qrCodeImage.src = ''; // Limpiar
         qrCodeImage.classList.add('hidden');
         qrSpinner.classList.remove('hidden'); // Mostrar spinner
         showModal(qrCodeModal);

         try {
            const qrDataUri = await backend.get_qr_code_base64(equipment.id);
             if (qrDataUri) {
                 qrCodeImage.src = qrDataUri;
                 qrCodeImage.classList.remove('hidden');
             } else {
                 qrModalInfo.textContent += "\nError al generar QR.";
             }
         } catch (error) {
            console.error("Error al obtener QR:", error);
            qrModalInfo.textContent += "\nError al obtener QR.";
         } finally {
             qrSpinner.classList.add('hidden'); // Ocultar spinner
         }
     }

     function closeQrCodeModal() {
         hideModal(qrCodeModal);
     }

    async function handleDownloadTemplate() {
        if (!backend) {
            displayImportFeedback('error', 'Error: Backend no conectado.');
            return;
        }
        displayImportFeedback('info', 'Solicitando descarga de plantilla...');
        if(downloadTemplateButton) downloadTemplateButton.disabled = true;

        try {
            console.log("JS: Llamando a backend.download_template_file()...");
            const jsonStringResult = await backend.download_template_file();
            console.log("JS: Respuesta STRING de download_template_file:", jsonStringResult);
            console.log("JS: Tipo de respuesta STRING:", typeof jsonStringResult);

            let result = null;
            if (typeof jsonStringResult === 'string' && jsonStringResult.trim() !== '') {
                try {
                    result = JSON.parse(jsonStringResult);
                    console.log("JS: Objeto JS parseado desde JSON string:", result);
                } catch (parseError) {
                    console.error("JS: Error parseando JSON string del backend (download):", parseError, "String recibido:", jsonStringResult);
                    displayImportFeedback('error', 'Error procesando respuesta del servidor (formato inválido).');
                    if(downloadTemplateButton) downloadTemplateButton.disabled = false;
                    return;
                }
            } else {
                 console.warn("JS: Se recibió una respuesta vacía o no string del backend para descarga.");
            }

            // --- MANEJAR EL OBJETO 'result' PARSEADO Y AÑADIR BOTÓN DE ABRIR ---
            if (result && result.success) {
                // Si la descarga fue exitosa y tenemos un 'filepath'
                if (result.filepath) {
                    // Reutilizamos displayImportFeedback que ya sabe añadir el botón "Abrir"
                    // Le pasamos el filePath para que lo use en el botón.
                    displayImportFeedback('success', result.message || 'Plantilla descargada correctamente.', { filepath: result.filepath });
                } else {
                    // Si no hay filepath (inesperado si es exitoso)
                    displayImportFeedback('success', result.message || 'Plantilla descargada correctamente.');
                }
            } else {
                let errorMessage = 'Error desconocido al descargar plantilla.';
                 if (result && result.message) {
                    errorMessage = result.message;
                 } else if (result === null) {
                     errorMessage = 'No se recibió respuesta válida del servidor para la descarga.';
                 } else if (result && result.success === false) {
                     errorMessage = result.message || 'El servidor indicó un fallo en la descarga.';
                 }
                displayImportFeedback('error', errorMessage);
            }
            // -----------------------------------------------------------------

        } catch (error) {
            console.error("Error llamando a backend.download_template_file:", error);
            displayImportFeedback('error', `Error de comunicación al descargar: ${error.message || error}`);
        } finally {
            if(downloadTemplateButton) downloadTemplateButton.disabled = false;
        }
    }

    

    function hideImportFeedback() {
        if (importFeedback) {
            importFeedback.classList.add('hidden');
        }
    }

    // --- Asignación de Event Listeners ---
    addEquipmentFloatButton.addEventListener('click', openAddModal);
    closeModalButton.addEventListener('click', closeModal);
    cancelModalButton.addEventListener('click', closeModal);
    equipmentForm.addEventListener('submit', handleFormSubmit);
    downloadTemplateButton?.addEventListener('click', handleDownloadTemplate);
    closeImportFeedbackButton?.addEventListener('click', hideImportFeedback);
    

    itemsPerPageSelect?.addEventListener('change', (event) => {
        itemsPerPage = parseInt(event.target.value, 10);
        currentPage = 1; // Volver a la página 1
        renderPagedTable();
    });
    prevPageButton?.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderPagedTable();
        }
    });
    nextPageButton?.addEventListener('click', () => {
        // Calcular totalPages de nuevo aquí o pasarlo como argumento
        const totalPages = Math.ceil(currentFilteredData.length / itemsPerPage) || 1;
        if (currentPage < totalPages) {
            currentPage++;
            renderPagedTable();
        }
    });
     // Listeners para botones inferiores (opcional)
     prevPageButtonBottom?.addEventListener('click', () => prevPageButton?.click()); // Simular clic en el de arriba
     nextPageButtonBottom?.addEventListener('click', () => nextPageButton?.click());
     
     if (importFeedback) { // Asegurarse que el contenedor del feedback existe
        importFeedback.addEventListener('click', (event) => {
            // Encontrar el botón específico que fue clickeado (o su ancestro cercano)
            const openButton = event.target.closest('button.open-pdf-button'); 
    
            if (openButton) { // Verificar si se hizo clic en nuestro botón
                console.log("Clic detectado en botón 'Abrir Archivo' (delegado).");
                const filePath = openButton.dataset.filepath; // Obtener ruta desde data-filepath
    
                if (filePath) {
                    console.log(`Intentando abrir archivo: ${filePath}`);
                    // Llamar a la función del backend (aquí 'backend' SÍ está disponible)
                    if (backend && typeof backend.open_file === 'function') {
                        backend.open_file(filePath);
                    } else {
                         console.error("Error: backend.open_file no está disponible al intentar abrir desde listener delegado.");
                         alert("Error: No se pudo ejecutar la acción para abrir el archivo.");
                    }
                } else {
                    console.error("Error: No se encontró el atributo data-filepath en el botón:", openButton);
                    alert("Error: No se pudo obtener la ruta del archivo a abrir.");
                }
            }
            // Si no se hizo clic en openButton, no hacer nada.
        });
        console.log("Listener delegado 'click' añadido a importFeedback para botones .open-pdf-button");
    } else {
        console.warn("Contenedor 'importFeedback' no encontrado, no se pudo añadir listener delegado.");
    }

     // --- NUEVO Listener para Ordenamiento ---
     document.querySelectorAll('th.sortable-header').forEach(header => {
        header.addEventListener('click', () => {
            const key = header.dataset.sortKey;
            if (!key) return;

            if (sortColumn === key) {
                // Cambiar dirección si es la misma columna
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                // Nueva columna, empezar ascendente
                sortColumn = key;
                sortDirection = 'asc';
            }
            // Opcional: ¿volver a página 1 al ordenar? Sí, suele ser mejor.
            currentPage = 1;
            renderPagedTable(); // Re-renderizar con el nuevo orden/página
        });
    });

    importExcelButton?.addEventListener('click', () => {
        console.log("Clic en Botón Importar detectado."); // <-- Log 1
        console.log("Referencia a excelFileInput:", excelFileInput); // <-- Log 2
        if (excelFileInput) {
            excelFileInput.click(); // Intenta el clic si la referencia existe
            console.log("Llamada a excelFileInput.click() realizada."); // <-- Log 3
        } else {
            console.error("Error: La referencia a excelFileInput es nula o inválida."); // <-- Log 4 (Error)
        }
    });
    excelFileInput?.addEventListener('change', handleFileSelect);

     filterMaintenanceButton.addEventListener('click', filterMaintenance); // <-- Nuevo Listener


     // Listeners Modales (Confirmación y QR)
     confirmDeleteButton.addEventListener('click', executeDelete);
     cancelDeleteButton.addEventListener('click', cancelDeleteAction);
     closeQrButton.addEventListener('click', closeQrCodeModal);

     // Logout y User Management
    logoutButton?.addEventListener('click', () => {
        backend.request_close_application();
    });
     userMgmtButton?.addEventListener('click', () => {
        if (backend && currentUserRole === 'admin') {
            console.log("Solicitando navegación a Gestión de Usuarios..."); // Log
            try {
                backend.navigate_to('users'); // Llamada al backend para ir a users.html
            } catch (e) {
                console.error("Error al intentar navegar a usuarios:", e);
                displayGeneralFeedback('error', 'No se pudo iniciar la navegación.');
            }
        } else if (!backend) {
             console.error("Backend no disponible para navegar.");
             displayGeneralFeedback('error', 'Error de conexión.');
        } else {
             console.warn("Intento de navegación a usuarios sin permisos.");
        }
    });

    // --- NUEVO: Función para cargar todas las sugerencias ---
    async function loadAllSuggestions() {
        console.log("--- loadAllSuggestions INVOCADA ---");
        if (!backend) { console.error("Backend no disponible."); return; }
        
        try {
            console.log("  Iniciando llamadas para poblar selects...");
            await Promise.all([
                populateSelectWithNewOption(formSelects.tipo_equipo, formInputs.tipo_equipo, 'get_distinct_tipos_equipo'),
                populateSelectWithNewOption(formSelects.marca, formInputs.marca, 'get_distinct_marcas'),
                populateSelectWithNewOption(formSelects.modelo, formInputs.modelo, 'get_distinct_modelos'),
                populateSelectWithNewOption(formSelects.asignado_a, formInputs.asignado_a, 'get_distinct_asignados'),
                populateSelectWithNewOption(formSelects.departamento, formInputs.departamento, 'get_distinct_departamentos'),
                populateSelectWithNewOption(formSelects.sede, formInputs.sede, 'get_distinct_sedes') // NUEVA LLAMADA PARA SEDE
            ]);
            console.log("--- loadAllSuggestions: Todas las llamadas completadas. ---");
        } catch (error) {
             console.error("Error general durante loadAllSuggestions:", error);
        }
    }

    function handleSelectChange(event) {
        const selectElement = event.target;
        // Derivar ID del input asociado (ej: 'marca-select' -> 'marca')
        const targetInputId = selectElement.id.replace('-select', ''); 
        const targetInputElement = document.getElementById(targetInputId);
    
        console.log(`Cambio en select: ${selectElement.id}, Valor: ${selectElement.value}, Buscando input: #${targetInputId}`); // Log Principal
    
        if (targetInputElement) {
            const isRequired = (targetInputId === 'tipo_equipo'); // Marcar si este campo es requerido cuando es nuevo
    
            if (selectElement.value === '__nuevo__') {
                console.log(`  -> Opción '__nuevo__' seleccionada. Mostrando input #${targetInputId}`);
                targetInputElement.classList.remove('hidden');
                targetInputElement.value = ''; 
                targetInputElement.required = isRequired; 
                // Añadir un pequeño delay antes del focus puede ayudar en algunos navegadores
                setTimeout(() => targetInputElement.focus(), 0); 
            } else {
                console.log(`  -> Opción existente o vacía seleccionada. Ocultando input #${targetInputId}`);
                targetInputElement.classList.add('hidden');
                targetInputElement.required = false; // Quitar 'required'
                targetInputElement.value = ''; 
            }
        } else {
            console.error(`*** ERROR en handleSelectChange: No se encontró el input #${targetInputId} asociado a ${selectElement.id}`);
        }
    }
    
    async function populateSelectWithNewOption(selectElement, inputElement, backendFunctionName, includeSelectOption = true) {
        if (!backend || !selectElement || !inputElement || !backend[backendFunctionName] || typeof backend[backendFunctionName] !== 'function') {
            console.error(`populateSelectWithNewOption: Invalid args for ${backendFunctionName}`);
            return;
        }
    
        console.log(`Poblando select '${selectElement.id}' (input: '${inputElement.id}') llamando a backend.${backendFunctionName}...`);
        try {
            const rawResponse = await backend[backendFunctionName]();
            let values = [];
            if (rawResponse && typeof rawResponse === 'string') {
                 try { values = JSON.parse(rawResponse); } catch (e) { console.error("Error parsing JSON", e); }
            } else if (Array.isArray(rawResponse)) { values = rawResponse; }
            if (!Array.isArray(values)) { values = []; }
    
            const currentValue = selectElement.value; // Guardar valor actual
            selectElement.innerHTML = ''; // Limpiar select
    
            // 1. Opción "-- Seleccione --"
            if (includeSelectOption) {
                const selectOpt = document.createElement('option');
                selectOpt.value = "";
                let placeholderText = inputElement.name.replace(/_/g, ' ');
                placeholderText = placeholderText.charAt(0).toUpperCase() + placeholderText.slice(1);
                selectOpt.textContent = `-- Seleccione ${placeholderText} --`;
                selectElement.appendChild(selectOpt);
            }
            
            // 2. Opción "-- Nuevo ... --"
            const newOpt = document.createElement('option');
            newOpt.value = "__nuevo__"; 
            let newOptionText = inputElement.name.replace(/_/g, ' ');
            newOptionText = newOptionText.charAt(0).toUpperCase() + newOptionText.slice(1);
            newOpt.textContent = `-- Nuevo ${newOptionText} --`; 
            selectElement.appendChild(newOpt);
    
            // 3. Opciones de la base de datos (ordenadas)
            const validValues = [...new Set(values)].filter(v => v !== null && v !== undefined && String(v).trim() !== '').sort((a, b) => String(a).localeCompare(String(b), undefined, { sensitivity: 'base' }));
            validValues.forEach(value => {
                const option = document.createElement('option');
                option.value = String(value).trim();
                option.textContent = String(value).trim();
                selectElement.appendChild(option);
            });
    
            // --- CORRECCIÓN AQUÍ: Declarar possibleValues ---
            const possibleValues = ["", "__nuevo__", ...validValues.map(String)]; // Convertir a String explícitamente
            // Restaurar valor previo si aún existe en las opciones, o dejar vacío
            if (possibleValues.includes(currentValue)) { 
                selectElement.value = currentValue;
            } else {
                selectElement.value = "";
            }
            
            // Ocultar input al (re)poblar, solo se muestra si se selecciona '__nuevo__' en modo ENABLED
            if (inputElement) { // Asegurar que inputElement no es null
                inputElement.classList.add('hidden');
                inputElement.value = '';
                inputElement.required = false; 
            }
    
        } catch (error) {
            console.error(`Error al poblar select '${selectElement.id}' desde ${backendFunctionName}:`, error);
            // Asegurar que el select no quede en blanco si falla
            if (selectElement) selectElement.innerHTML = `<option value="">-- Error al cargar --</option>`;
        }
    }

    function handleFileSelect(event) { // Ya no necesita ser async
        // Verificar backend
        if (!backend) {
            displayImportFeedback('error', 'Error: Backend no conectado.');
            return;
        }
        const file = event.target.files[0];
        if (!file) {
            console.log("JS: No se seleccionó archivo.");
            return;
        }
    
        // Verificar tipo de archivo
        if (file.type !== 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' &&
            !file.name.toLowerCase().endsWith('.xlsx')) {
            displayImportFeedback('error', 'Error: Seleccione un archivo Excel (.xlsx).');
            if(excelFileInput) excelFileInput.value = '';
            return;
        }
    
        // Mostrar feedback inicial y deshabilitar botón
        displayImportFeedback('info', 'Leyendo archivo...'); // Mensaje más corto aquí
        if (importExcelButton) importExcelButton.disabled = true; // Deshabilitar AHORA
    
        const reader = new FileReader();
    
        reader.onload = (e) => { // Quitar async
            const fileBase64 = e.target.result;
            try {
                console.log("JS: Enviando datos Base64 al backend para importar (SIN ESPERAR RESPUESTA)...");
                // --- SIMPLEMENTE LLAMAR AL SLOT ---
                backend.import_excel_data(fileBase64);
                // ---------------------------------
                // Mostrar mensaje de que se envió, el resultado llegará por señal
                displayImportFeedback('info', 'Archivo enviado. Procesando importación en el servidor...');
            } catch (error) {
                // Error SÍNCRONO al intentar llamar al backend
                console.error("Error llamando a backend.import_excel_data:", error);
                displayImportFeedback('error', `Error de comunicación al iniciar importación: ${error.message || error}`);
                // Re-habilitar en caso de error inmediato
                if (importExcelButton) importExcelButton.disabled = false;
                if (excelFileInput) excelFileInput.value = '';
            }
            // Ya no hay finally aquí, se maneja en handleImportResult
        }; // Fin reader.onload
    
        reader.onerror = (e) => {
            console.error("Error leyendo archivo:", e);
            displayImportFeedback('error', 'Error al leer el archivo seleccionado.');
            if (importExcelButton) importExcelButton.disabled = false;
            if (excelFileInput) excelFileInput.value = '';
        };
    
        reader.readAsDataURL(file);
    } // --- FIN handleFileSelect ---
    

    function displayImportFeedback(type, summaryMessage, resultData = {}) {
        // Verificar referencias DOM (Asegúrate que importFeedback, importFeedbackMessage, closeImportFeedbackButton existan)
        if (!importFeedback || !importFeedbackMessage || !closeImportFeedbackButton) {
            console.error("displayImportFeedback: Elementos DOM para feedback no encontrados.");
            return; 
        }
    
        // --- Mensaje Principal y Detalles (Como antes) ---
        let cleanSummaryMessage = escapeHtml(safe(summaryMessage).replace(/^\s+|\s+$/g, '').replace(/\u0000/g, ''));
        let fullMessageHtml = cleanSummaryMessage; 
        const createListHtml = (details) => (details || []).map(d => `- ${escapeHtml(safe(d).replace(/^\s+|\s+$/g, '').replace(/\u0000/g, ''))}`).join("<br>");
        if (resultData.errors?.length > 0) fullMessageHtml += "<br><br>--- Errores ---<br>" + createListHtml(resultData.errors);
        if (resultData.db_ignored_details?.length > 0) fullMessageHtml += "<br><br>--- Ignorados (BD) ---<br>" + createListHtml(resultData.db_ignored_details);
        if (resultData.batch_ignored_details?.length > 0) fullMessageHtml += "<br><br>--- Ignorados (Archivo) ---<br>" + createListHtml(resultData.batch_ignored_details);
        // --- Fin Mensaje Principal y Detalles ---
    
        // --- Lógica para añadir el botón "Abrir" ---
        let openButtonHtml = '';
        if (type === 'success' && resultData && typeof resultData.filepath === 'string' && resultData.filepath.trim() !== '') {
            // NO necesitamos escapar filePathForJs ahora, se guarda en data-attribute
            const filename = resultData.filepath.split(/[\\/]/).pop() || 'reporte.pdf'; 
            
            console.log(`displayImportFeedback: Añadiendo botón 'Abrir' con data-filepath: ${resultData.filepath}`);
            
            // Construir HTML SIN onclick, con clase y data-attribute
            openButtonHtml = `
                <button 
                    data-filepath="${escapeHtml(resultData.filepath)}" 
                    title="Abrir ${escapeHtml(filename)}"
                    type="button" 
                    class="open-pdf-button ml-4 px-3 py-1 border border-blue-500 text-blue-600 dark:border-blue-400 dark:text-blue-300 rounded text-xs hover:bg-blue-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:ring-offset-1 dark:focus:ring-offset-gray-800 transition-colors duration-150"
                >
                    <i class="fas fa-external-link-alt mr-1"></i>Abrir Archivo 
                </button>
            `;
            fullMessageHtml += openButtonHtml; 
        }
        // --- Fin lógica botón "Abrir" ---
    
        // Asignar HTML y Estilos (Como antes)
        console.log("displayImportFeedback: Contenido final innerHTML:", fullMessageHtml);
        importFeedbackMessage.innerHTML = fullMessageHtml;
    
        importFeedback.className = 'mt-4 p-3 pr-8 rounded-lg text-sm relative shadow border'; 
        closeImportFeedbackButton.className = 'absolute top-2 right-2 text-xl font-semibold leading-none focus:outline-none'; 
        const typeStyles = { /* ... tus estilos ... */ 
            success: { container: ['bg-green-50', /*...*/], closeButton: ['text-green-600', /*...*/] },
            error:   { container: ['bg-red-50',   /*...*/], closeButton: ['text-red-600',   /*...*/] },
            info:    { container: ['bg-blue-50',  /*...*/], closeButton: ['text-blue-600',  /*...*/] }
        };
        const styles = typeStyles[type] || typeStyles.info; 
        importFeedback.classList.add(...styles.container);
        closeImportFeedbackButton.classList.add(...styles.closeButton);
        closeImportFeedbackButton.innerHTML = '×'; 
    
        importFeedback.classList.remove('hidden');
    }
    
    
    // --- Función Auxiliar para Escapar HTML (Importante por seguridad con innerHTML) ---
    function escapeHtml(unsafe) {
        if (unsafe === null || unsafe === undefined) return '';
        return String(unsafe)
             .replace(/&/g, "&")
             .replace(/</g, "<")
             .replace(/>/g, ">")
             .replace(/"/g, "'")
             .replace(/'/g, "'"); // o '
    }
    
    
    // --- Iniciar Conexión ---
    connectAndInitialize();

}); // Fin DOMContentLoaded