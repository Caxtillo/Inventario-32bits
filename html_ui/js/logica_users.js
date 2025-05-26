// js/logica_users.js
document.addEventListener('DOMContentLoaded', () => {
    console.log("User Logic: DOMContentLoaded.");

    // --- Referencias ---
    const htmlElement = document.documentElement; // Referencia a <html>
    const darkModeToggle = document.getElementById('dark-mode-toggle'); // Botón añadido en HTML
    const darkModeIcon = document.getElementById('dark-mode-icon'); // Icono dentro del botón
    const userRoleDisplay = document.getElementById('user-role-display');
    const backToInventoryButton = document.getElementById('back-to-inventory-button');
    const addUserButton = document.getElementById('add-user-button');
    const userTableBody = document.getElementById('user-table-body');
    const userModal = document.getElementById('user-modal');
    const userModalTitle = document.getElementById('user-modal-title');
    const closeUserModalButton = document.getElementById('close-user-modal-button');
    const cancelUserModalButton = document.getElementById('cancel-user-modal-button');
    const userForm = document.getElementById('user-form');
    const userIdInput = document.getElementById('user-id');
    const usernameInput = document.getElementById('username');
    const passwordSection = document.getElementById('password-section');
    const passwordInput = document.getElementById('password');
    const passwordRequiredIndicator = document.getElementById('password-required-indicator');
    const confirmPasswordSection = document.getElementById('confirm-password-section');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const confirmPasswordRequiredIndicator = document.getElementById('confirm-password-required-indicator');
    const roleInput = document.getElementById('role');
    const saveUserButton = document.getElementById('save-user-button');
    const userFormFeedback = document.getElementById('user-form-feedback');
    const deleteUserConfirmModal = document.getElementById('delete-user-confirm-modal');
    const deleteUserConfirmMessage = document.getElementById('delete-user-confirm-message');
    const confirmDeleteUserButton = document.getElementById('confirm-delete-user-button');
    const cancelDeleteUserButton = document.getElementById('cancel-delete-user-button');
    const logoutButton = document.getElementById('logout-button');
    const successFeedbackModal = document.getElementById('success-feedback-modal');
    const successModalTitle = document.getElementById('success-modal-title');
    const successModalMessage = document.getElementById('success-modal-message');
    const acceptSuccessModalButton = document.getElementById('accept-success-modal-button');
    const resetPasswordModal = document.getElementById('reset-password-modal');
    const closeResetModalButton = document.getElementById('close-reset-modal-button');
    const resetModalTitle = document.getElementById('reset-modal-title');
    const resetFormFeedback = document.getElementById('reset-form-feedback');
    const resetPasswordForm = document.getElementById('reset-password-form');
    const resetUserIdInput = document.getElementById('reset-user-id');
    const resetUsernameInput = document.getElementById('reset-username');
    const resetModalUserInfo = document.getElementById('reset-modal-user-info');
    const newPasswordInput = document.getElementById('new-password');
    const confirmNewPasswordInput = document.getElementById('confirm-new-password');
    const cancelResetModalButton = document.getElementById('cancel-reset-modal-button');
    const saveResetPasswordButton = document.getElementById('save-reset-password-button');
    const itemsPerPageSelect = document.getElementById('items-per-page');
    // Quitado Banner General si no se usa en esta página
    // const generalFeedbackBanner = document.getElementById('general-feedback-banner'); ...


     // --- Estado ---
    let backend = null;
    let currentUserRole = 'read_only';
    let currentUserId = null;
    let editingUserId = null;
    let userToDelete = null;
    let isLoadingUsers = false;
    // let generalFeedbackTimeout = null; // Quitado si no hay banner
    let userIdToReset = null;
    let usernameToReset = null;


    // --- Funciones Dark Mode ---
    function applyTheme(theme) {
        if (theme === 'dark') {
            htmlElement.classList.add('dark');
            if (darkModeIcon) darkModeIcon.classList.replace('fa-moon', 'fa-sun');
        } else {
            htmlElement.classList.remove('dark');
            if (darkModeIcon) darkModeIcon.classList.replace('fa-sun', 'fa-moon');
        }
    }

    function toggleTheme() {
        const isDarkMode = htmlElement.classList.contains('dark');
        const newTheme = isDarkMode ? 'light' : 'dark';
        applyTheme(newTheme);
        try {
            localStorage.setItem('theme', newTheme);
        } catch (e) {
            console.error("Error guardando tema en localStorage:", e);
        }
    }

    function loadTheme() {
        let theme = 'light'; // Default
        try {
            const storedTheme = localStorage.getItem('theme');
            if (storedTheme) {
                theme = storedTheme;
            } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                theme = 'dark'; // Usar preferencia del sistema si no hay nada guardado
            }
        } catch (e) {
            console.error("Error leyendo tema de localStorage:", e);
            // Podrías optar por usar la preferencia del sistema como fallback aquí también
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                 theme = 'dark';
            }
        }
        applyTheme(theme);
    }


    // --- Funciones Auxiliares (Modales, etc.) ---
    const safe = (value) => value === null || value === undefined ? '' : value;

    function showModal(modalElement) {
        if (modalElement) modalElement.classList.add('is-active');
        else console.error("showModal: Elemento nulo", modalElement);
    }
    function hideModal(modalElement) {
        if (modalElement) modalElement.classList.remove('is-active');
        else console.error("hideModal: Elemento nulo", modalElement);
    }

    function displayUserFormFeedback(type, message) {
        if (!userFormFeedback) { console.warn("Elemento user-form-feedback no encontrado"); return; }
        userFormFeedback.textContent = message;
        userFormFeedback.className = 'form-feedback mb-5 p-3 rounded text-sm'; // Base classes + custom
        if (type === 'success') {
            userFormFeedback.classList.add('bg-green-100', 'dark:bg-green-900', 'dark:bg-opacity-30', 'text-green-700', 'dark:text-green-300');
        } else if (type === 'error') {
            userFormFeedback.classList.add('bg-red-100', 'dark:bg-red-900', 'dark:bg-opacity-30', 'text-red-700', 'dark:text-red-300');
        } else { // info
            userFormFeedback.classList.add('bg-blue-100', 'dark:bg-blue-900', 'dark:bg-opacity-30', 'text-blue-700', 'dark:text-blue-300');
        }
        userFormFeedback.classList.remove('hidden');
        if (type === 'success') {
           setTimeout(() => { if (userFormFeedback) userFormFeedback.classList.add('hidden'); }, 3000);
        }
    }

    // Función de feedback general (usando alert como fallback si no hay banner)
    function displayGeneralFeedback(type, message) {
         console.log(`User Feedback Backend (${type}): ${message}`);
         // Aquí podrías reintroducir un banner si lo deseas, o simplemente usar alert
         alert(`[${type.toUpperCase()}] ${message}`);
     }

    function showSuccessModal(title, message) {
        if (!successFeedbackModal || !successModalTitle || !successModalMessage) {
            console.error("Elementos del modal de éxito no encontrados.");
            alert(`ÉXITO: ${title}\n${message}`);
            return;
        }
        successModalTitle.textContent = title;
        successModalMessage.textContent = message;
        showModal(successFeedbackModal);
    }

    function hideSuccessModal() {
        if (successFeedbackModal) hideModal(successFeedbackModal);
    }

    function openResetPasswordModal(userId, username) {
        if (!resetPasswordModal || !resetModalUserInfo || !resetPasswordForm || !newPasswordInput || !confirmNewPasswordInput || !resetFormFeedback) {
            console.error("Elementos del modal de reset de contraseña no encontrados.");
            displayGeneralFeedback('error', 'No se puede abrir el diálogo de reseteo.'); // Usa alert
            return;
        }
        userIdToReset = userId;
        usernameToReset = username;
        resetPasswordForm.reset();
        resetFormFeedback.classList.add('hidden');
        resetFormFeedback.textContent = '';
        resetFormFeedback.className = 'form-feedback mb-5 p-3 rounded text-sm hidden'; // Reset completo

        resetModalUserInfo.textContent = `Ingrese la nueva contraseña para el usuario: ${username} (ID: ${userId})`;
        showModal(resetPasswordModal);
        newPasswordInput.focus();
    }

    function closeResetPasswordModal() {
         if (resetPasswordModal) hideModal(resetPasswordModal);
         userIdToReset = null;
         usernameToReset = null;
         resetPasswordForm.reset();
         resetFormFeedback.classList.add('hidden');
    }

    function displayResetFormFeedback(type, message) {
         if (!resetFormFeedback) { console.warn("Elemento reset-form-feedback no encontrado"); return; }
         resetFormFeedback.textContent = message;
         resetFormFeedback.className = 'form-feedback mb-5 p-3 rounded text-sm'; // Base classes + custom
         if (type === 'error') {
             resetFormFeedback.classList.add('bg-red-100', 'dark:bg-red-900', 'dark:bg-opacity-30', 'text-red-700', 'dark:text-red-300');
         }
         else { // info/default
             resetFormFeedback.classList.add('bg-blue-100', 'dark:bg-blue-900', 'dark:bg-opacity-30', 'text-blue-700', 'dark:text-blue-300');
         }
         resetFormFeedback.classList.remove('hidden');
    }


     // --- Lógica Principal (Conexión, Inicialización, Carga) ---
     function connectAndInitialize() {
        console.log("User Logic: Iniciando connectAndInitialize...");
        const connectTimeout = 10000;
        let connectionEstablished = false;
        const tryConnect = setInterval(() => {
            if (typeof qt !== 'undefined' && qt.webChannelTransport) {
                clearInterval(tryConnect);
                new QWebChannel(qt.webChannelTransport, (channel) => {
                    connectionEstablished = true;
                    if (channel.objects.backend) {
                        backend = channel.objects.backend;
                        console.log("User Logic: Objeto Backend conectado.");
                        try {
                            backend.users_updated?.connect(loadAndRenderUsers);
                            // Conectar show_message si se usa para algo más que éxito/error manejados
                            // backend.show_message?.connect(displayGeneralFeedback);
                        } catch(e) { console.error("Error conectando señales:", e);}
                        initializeUserData();
                    } else {
                        console.error("User Logic: Error - Objeto 'backend' NO encontrado.");
                        displayGeneralFeedback('error', 'Error crítico: No se pudo conectar con el backend.');
                        if(userTableBody) userTableBody.innerHTML = '<tr><td colspan="4" class="text-center py-4 px-6 text-red-600 dark:text-red-400">Error de conexión con Backend.</td></tr>';
                    }
                });
            } else { console.log("User Logic: Esperando qt.webChannelTransport..."); }
        }, 300);
        setTimeout(() => {
            if (!connectionEstablished) {
                clearInterval(tryConnect); console.error("User Logic: Timeout Conexión.");
                displayGeneralFeedback('error', 'Error crítico: Timeout al conectar con el backend.');
                if(userTableBody) userTableBody.innerHTML = '<tr><td colspan="4" class="text-center py-4 px-6 text-red-600 dark:text-red-400">Error: Timeout de conexión.</td></tr>';
            }
        }, connectTimeout);
    }

    async function initializeUserData() {
         console.log("User Logic: Iniciando initializeUserData...");
         if (!backend) { console.error("Backend no listo."); return; }
         isLoadingUsers = true;
         try {
             currentUserRole = await backend.get_current_role();
             currentUserId = await backend.get_current_user_id();
             console.log("Rol:", currentUserRole, "ID:", currentUserId);
             if(userRoleDisplay) userRoleDisplay.textContent = currentUserRole ? (currentUserRole.charAt(0).toUpperCase() + currentUserRole.slice(1)).replace('_', ' ') : '?';

             if (currentUserRole !== 'admin') {
                 displayGeneralFeedback('error', 'Acceso denegado. Permisos insuficientes.');
                 if(addUserButton) addUserButton.style.display = 'none'; // Ocultar botón
                 if(userTableBody) userTableBody.innerHTML = '<tr><td colspan="4" class="text-center py-6 text-gray-500 dark:text-gray-400">Acceso denegado.</td></tr>';
                 isLoadingUsers = false; return;
             } else {
                  if(addUserButton) addUserButton.style.display = ''; // Asegurar visibilidad
             }
             await loadAndRenderUsers();
         } catch (error) {
             console.error("Error inicializando:", error);
             displayGeneralFeedback('error', `Error al inicializar datos: ${error.message || error}`);
             isLoadingUsers = false;
        }
    }

    async function loadAndRenderUsers() {
         if (!backend || currentUserRole !== 'admin') { return; }
         isLoadingUsers = true;
         if (!userTableBody) { console.error("userTableBody no encontrado!"); isLoadingUsers = false; return; }
         userTableBody.innerHTML = '<tr><td colspan="4" class="text-center py-6 text-gray-500 dark:text-gray-400"><i class="fas fa-spinner fa-spin mr-2"></i>Cargando usuarios...</td></tr>';
         try {
             const users = await backend.get_users();
             renderUserTable(users || []);
         } catch (error) {
             console.error("User Logic: Error llamando a backend.get_users:", error);
             displayGeneralFeedback('error', `Error al cargar usuarios: ${error.message || error}`);
             userTableBody.innerHTML = '<tr><td colspan="4" class="text-center py-6 text-red-500 dark:text-red-400">Error al cargar usuarios. Intente recargar.</td></tr>';
         } finally {
             isLoadingUsers = false;
         }
     }

     function renderUserTable(users) {
         if (!userTableBody) { console.error("renderUserTable: userTableBody no existe."); return; }
         userTableBody.innerHTML = '';
         if (!users || users.length === 0) {
             userTableBody.innerHTML = '<tr><td colspan="4" class="text-center py-6 text-gray-500 dark:text-gray-400">No hay otros usuarios registrados.</td></tr>';
             return;
         }
         let rowsHtml = '';
         users.forEach(user => {
             // Aplicar clases dark a celdas
             const cellClass = "px-4 py-3 whitespace-nowrap text-sm";
             const cellClassGray = `${cellClass} text-gray-600 dark:text-gray-400`;
             const cellClassHeader = `${cellClass} font-medium text-gray-800 dark:text-gray-200`;
             let actionButtonsHtml = '';
             const isCurrentUser = currentUserId !== null && user.id === currentUserId;
             const deleteDisabledAttr = isCurrentUser ? 'disabled title="No puede eliminar su propia cuenta"' : '';
              // Aplicar clases dark a botones de acción
             const editBtnClasses = "text-indigo-600 dark:text-indigo-400 hover:text-indigo-900 dark:hover:text-indigo-300 focus:text-indigo-900 dark:focus:text-indigo-300";
             const resetBtnClasses = "text-yellow-600 dark:text-yellow-400 hover:text-yellow-800 dark:hover:text-yellow-300 focus:text-yellow-800 dark:focus:text-yellow-300";
             const deleteBtnClassesBase = "text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300 focus:text-red-900 dark:focus:text-red-300";
             const deleteBtnClassesDisabled = "text-red-300 dark:text-red-600 cursor-not-allowed";
             const deleteBtnFinalClasses = isCurrentUser ? deleteBtnClassesDisabled : deleteBtnClassesBase;

             const commonBtnClasses = "transition duration-150 px-2 py-1 mx-0.5 focus:outline-none rounded";

             actionButtonsHtml += `<button title="Editar Rol" class="${editBtnClasses} ${commonBtnClasses} edit-user-btn" data-id="${user.id}" data-username="${safe(user.username)}" data-role="${safe(user.role)}"><i class="fas fa-user-edit fa-fw"></i></button>`;
             actionButtonsHtml += `<button title="Resetear Contraseña" class="${resetBtnClasses} ${commonBtnClasses} reset-pass-btn" data-id="${user.id}" data-username="${safe(user.username)}"><i class="fas fa-key fa-fw"></i></button>`;
             actionButtonsHtml += `<button title="Eliminar Usuario" class="${deleteBtnFinalClasses} ${commonBtnClasses} delete-user-btn" data-id="${user.id}" data-username="${safe(user.username)}" ${deleteDisabledAttr}><i class="fas fa-user-times fa-fw"></i></button>`;

             rowsHtml += `<tr class="hover:bg-gray-50 dark:hover:bg-gray-700"><td class="${cellClassHeader}">${user.id}</td><td class="${cellClassGray}">${safe(user.username)}</td><td class="${cellClassGray}">${safe(user.role).replace('_', ' ')}</td><td class="${cellClass} text-center space-x-1">${actionButtonsHtml}</td></tr>`;
         });
         userTableBody.innerHTML = rowsHtml;
     }

     // --- Manejo Modal Usuarios (Add/Edit) ---
     function resetUserForm() {
          if (!userForm) return;
          userForm.reset();
          editingUserId = null;
          if(userIdInput) userIdInput.value = '';
          if(userModalTitle) userModalTitle.textContent = 'Agregar Usuario';
          if(passwordSection) passwordSection.style.display = '';
          if(confirmPasswordSection) confirmPasswordSection.style.display = '';
          if(passwordInput) { passwordInput.required = true; passwordInput.value=''; }
          if(confirmPasswordInput) { confirmPasswordInput.required = true; confirmPasswordInput.value='';}
          if(passwordRequiredIndicator) passwordRequiredIndicator.style.display = '';
          if(confirmPasswordRequiredIndicator) confirmPasswordRequiredIndicator.style.display = '';
          if(usernameInput) usernameInput.disabled = false;
          if(userFormFeedback) {
              userFormFeedback.classList.add('hidden');
              userFormFeedback.textContent='';
              userFormFeedback.className = 'form-feedback mb-5 p-3 rounded text-sm hidden'; // Reset completo
         }
     }
     function openAddUserModal() {
         if (currentUserRole !== 'admin' || !userModal) return;
         resetUserForm();
         showModal(userModal);
         if(usernameInput) usernameInput.focus();
     }
     function openEditUserModal(user) {
         if (currentUserRole !== 'admin' || !userModal) return;
         resetUserForm();
         editingUserId = user.id;
         if(userIdInput) userIdInput.value = user.id;
         if(userModalTitle) userModalTitle.textContent = `Editar Usuario: ${user.username}`;
         if(usernameInput) { usernameInput.value = user.username; usernameInput.disabled = true; }
         if(roleInput) roleInput.value = user.role;
         if(passwordSection) passwordSection.style.display = 'none';
         if(confirmPasswordSection) confirmPasswordSection.style.display = 'none';
         if(passwordInput) passwordInput.required = false;
         if(confirmPasswordInput) confirmPasswordInput.required = false;
         showModal(userModal);
         if(roleInput) roleInput.focus();
     }
     function closeUserModal() {
         if(userModal) hideModal(userModal);
         resetUserForm();
     }

async function handleUserFormSubmit(event) {
    event.preventDefault();
    if (!backend || currentUserRole !== 'admin' || !userForm || !saveUserButton) {
        console.warn("handleUserFormSubmit: Condiciones previas no cumplidas o elementos faltantes.");
        return;
    }

    // Asegúrate de que los elementos del formulario existen antes de leer .value
    if (!usernameInput || !roleInput || !passwordInput || !confirmPasswordInput) {
        console.error("handleUserFormSubmit: Uno o más inputs del formulario no fueron encontrados.");
        displayUserFormFeedback('error', 'Error interno del formulario. Contacte al administrador.');
        return;
    }

    const username = usernameInput.value.trim();
    const role = roleInput.value;
    const password = passwordInput.value; // Se lee aunque no se use siempre
    const confirmPassword = confirmPasswordInput.value; // Se lee aunque no se use siempre

    if (userFormFeedback) userFormFeedback.classList.add('hidden');

    // Validaciones
    if (editingUserId) { 
        rawBackendResponse = await backend.update_user_role(editingUserId, role);
    } else { 
        if (!username || !role) {
            displayUserFormFeedback('error', 'Username y Rol son obligatorios.');
            return;
        }
        if (!password || !confirmPassword) {
            displayUserFormFeedback('error', 'Contraseña y confirmación son requeridas.');
            return;
        }
        if (password !== confirmPassword) {
            displayUserFormFeedback('error', 'Las contraseñas no coinciden.');
            return;
        }
        if (password.length < 4) {
            displayUserFormFeedback('error', 'La contraseña debe tener mínimo 4 caracteres.');
            return;
        }
    }

    const action = editingUserId ? 'actualizar rol' : 'agregar usuario';

    saveUserButton.disabled = true;
    saveUserButton.classList.add('opacity-50', 'cursor-not-allowed');

    try {
        console.log(`JS: Intentando ${action}...`);
        let rawBackendResponse; // Para almacenar la respuesta cruda del backend

        if (editingUserId) {
            // Asumimos que update_user_role también podría devolver un string JSON o un objeto
            rawBackendResponse = await backend.update_user_role(editingUserId, role);
        } else {
            rawBackendResponse = await backend.add_user(username, password, role);
        }

        console.log(`JS: Respuesta CRUDA del backend para '${action}':`, rawBackendResponse);
        console.log(`JS: typeof respuesta CRUDA:`, typeof rawBackendResponse);

        let result = null; // Para almacenar el objeto parseado o asignado

        if (rawBackendResponse && typeof rawBackendResponse === 'string') {
            try {
                result = JSON.parse(rawBackendResponse);
                console.log(`JS: Resultado parseado del string JSON:`, JSON.stringify(result));
            } catch (e) {
                console.error(`JS: Error parseando string JSON del backend para '${action}':`, e, "String recibido:", rawBackendResponse);
                // `result` permanece null si el parseo falla
            }
        } else if (rawBackendResponse && typeof rawBackendResponse === 'object') {
            // Si el backend ya devolvió un objeto (por ejemplo, si quitar `result=dict` funcionó)
            result = rawBackendResponse;
            console.log(`JS: Resultado (ya era objeto) del backend:`, JSON.stringify(result));
        } else if (rawBackendResponse === null ) {
            // Si el backend explícitamente devolvió null (como vimos en tu último log)
             console.warn(`JS: El backend devolvió null explícitamente para '${action}'.`);
             // result ya es null.
        }
        // Si rawBackendResponse es undefined, result también será null.

        // ------------ INICIO DE LA LÓGICA DE INTERPRETACIÓN DE 'result' ------------
        if (result && typeof result === 'object' && result.hasOwnProperty('success')) {
            // Tenemos un objeto con la propiedad 'success'
            if (result.success === true) {
                // ÉXITO REAL
                closeUserModal();
                const successTitle = editingUserId ? "Rol Actualizado" : "Usuario Agregado";
                const successMsg = result.message || (editingUserId ? `El rol del usuario ha sido actualizado.` : `El usuario '${username}' ha sido agregado correctamente.`);
                showSuccessModal(successTitle, successMsg);
            } else {
                // FALLO REPORTADO POR EL BACKEND (result.success es false)
                displayUserFormFeedback('error', result.message || `Fallo al ${action}. El backend no proporcionó un mensaje detallado.`);
            }
        } else {
            // RESPUESTA INESPERADA O MALFORMADA (result es null, no es objeto, o no tiene 'success')
            // Esto incluye el caso donde rawBackendResponse fue null y por ende result es null.
            console.error(`JS: Respuesta final interpretada como inesperada o malformada para '${action}':`, JSON.stringify(result), "(Original crudo:", rawBackendResponse,")");
            let errorMessage = `Error de comunicación con el servidor al ${action}. Respuesta no reconocida.`;
            if (rawBackendResponse === null) { // Específico para el caso que viste
                errorMessage = `El servidor devolvió una respuesta nula al intentar ${action}. Verifique los logs del servidor.`;
            }
            displayUserFormFeedback('error', errorMessage);
        }
        // ------------ FIN DE LA LÓGICA DE INTERPRETACIÓN DE 'result' ------------

    } catch (error) {
        // ERROR EN LA LLAMADA ASÍNCRONA o error en el código JS de este bloque try
        console.error(`JS: Error en la operación '${action}':`, error);
        displayUserFormFeedback('error', `Error inesperado durante la operación: ${error.message || 'Error desconocido'}`);
    } finally {
        saveUserButton.disabled = false;
        saveUserButton.classList.remove('opacity-50', 'cursor-not-allowed');
    }
}

// En logica_users.js

async function handleResetPasswordSubmit(event) {
    event.preventDefault();
    if (!backend || !resetPasswordForm || !newPasswordInput || !confirmNewPasswordInput || !userIdToReset || !usernameToReset) {
        console.error("handleResetPasswordSubmit: Faltan elementos o datos para resetear contraseña.");
        if(resetFormFeedback) displayResetFormFeedback('error', 'Error interno. No se puede procesar.');
        return;
    }
    if (!newPasswordInput || !confirmNewPasswordInput || !resetFormFeedback) {
        console.error("handleResetPasswordSubmit: Elementos del formulario de reseteo faltantes.");
        // No se puede usar displayResetFormFeedback si resetFormFeedback es null
        alert("Error interno del formulario de reseteo. Contacte al administrador.");
        return;
    }

    const newPassword = newPasswordInput.value;
    const confirmPassword = confirmNewPasswordInput.value;

    if (!newPassword || !confirmPassword) {
        displayResetFormFeedback('error', 'Ambos campos de contraseña son requeridos.');
        return;
    }
    if (newPassword.length < 4) {
        displayResetFormFeedback('error', 'La contraseña debe tener al menos 4 caracteres.');
        return;
    }
    if (newPassword !== confirmPassword) {
        displayResetFormFeedback('error', 'Las contraseñas no coinciden.');
        return;
    }

    if (resetFormFeedback) resetFormFeedback.classList.add('hidden');
    if (saveResetPasswordButton) saveResetPasswordButton.disabled = true;

    try {
        console.log(`JS: Intentando resetear contraseña para User ID: ${userIdToReset}`);
        const rawBackendResponse = await backend.reset_password(userIdToReset, newPassword);

        console.log(`JS: Respuesta CRUDA del backend para 'reset_password':`, rawBackendResponse);
        console.log(`JS: typeof respuesta CRUDA:`, typeof rawBackendResponse);

        let result = null;
        if (rawBackendResponse && typeof rawBackendResponse === 'string') {
            try {
                result = JSON.parse(rawBackendResponse);
                console.log(`JS: Resultado parseado del string JSON:`, JSON.stringify(result));
            } catch (e) {
                console.error(`JS: Error parseando string JSON del backend para 'reset_password':`, e, "String recibido:", rawBackendResponse);
            }
        } else if (rawBackendResponse && typeof rawBackendResponse === 'object') {
            result = rawBackendResponse;
            console.log(`JS: Resultado (ya era objeto) del backend:`, JSON.stringify(result));
        } else if (rawBackendResponse === null) {
            console.warn(`JS: El backend devolvió null explícitamente para 'reset_password'.`);
        }


        if (result && typeof result === 'object' && result.hasOwnProperty('success')) {
            if (result.success === true) {
                closeResetPasswordModal();
                showSuccessModal("Contraseña Reseteada", result.message || `La contraseña para '${usernameToReset}' ha sido actualizada.`);
            } else {
                displayResetFormFeedback('error', result.message || 'El backend falló al resetear la contraseña.');
            }
        } else {
            console.error(`JS: Respuesta final interpretada como inesperada o malformada para 'reset_password':`, JSON.stringify(result), "(Original crudo:", rawBackendResponse,")");
            let errorMessage = `Error de comunicación con el servidor al resetear contraseña. Respuesta no reconocida.`;
            if (rawBackendResponse === null) {
                errorMessage = `El servidor devolvió una respuesta nula al intentar resetear la contraseña.`;
            }
            displayResetFormFeedback('error', errorMessage);
        }

    } catch (e) {
        console.error("JS: Error en la operación 'reset_password':", e);
        displayResetFormFeedback('error', `Error de conexión al resetear: ${e.message || e}`);
    } finally {
        if (saveResetPasswordButton) saveResetPasswordButton.disabled = false;
    }
}


     // --- Borrar Usuario ---
      function confirmDeleteUser(user) {
         if (!backend || currentUserRole !== 'admin') return;
         if (currentUserId !== null && user.id === currentUserId) {
             displayGeneralFeedback('error', 'No puede eliminar su propia cuenta.');
             return;
        }
         userToDelete = user;
         if(deleteUserConfirmMessage) deleteUserConfirmMessage.textContent = `¿Seguro que desea eliminar al usuario '${user.username}' (ID: ${user.id})? Esta acción no se puede deshacer.`;
         if(deleteUserConfirmModal) showModal(deleteUserConfirmModal);
         else { console.error("Modal confirmación borrado no encontrado."); }
     }
      function cancelDeleteUserAction() {
          if(deleteUserConfirmModal) hideModal(deleteUserConfirmModal);
          userToDelete = null;
      }
// En logica_users.js

async function executeDeleteUser() {
    if (!backend || !userToDelete || currentUserRole !== 'admin') {
        console.warn("executeDeleteUser: Condiciones previas no cumplidas.");
        return;
    }
    const idToDelete = userToDelete.id;
    const usernameToDelete = userToDelete.username;
    hideModal(deleteUserConfirmModal); // Ocultar modal de confirmación

    // Deshabilitar el botón de confirmación si hubiera uno visible para evitar doble click
    // if (confirmDeleteUserButton) confirmDeleteUserButton.disabled = true;

    try {
        console.log(`JS: Intentando eliminar usuario ID: ${idToDelete}`);
        const rawBackendResponse = await backend.delete_user(idToDelete);

        console.log(`JS: Respuesta CRUDA del backend para 'delete_user':`, rawBackendResponse);
        console.log(`JS: typeof respuesta CRUDA:`, typeof rawBackendResponse);

        let result = null;
        if (rawBackendResponse && typeof rawBackendResponse === 'string') {
            try {
                result = JSON.parse(rawBackendResponse);
                console.log(`JS: Resultado parseado del string JSON:`, JSON.stringify(result));
            } catch (e) {
                console.error(`JS: Error parseando string JSON del backend para 'delete_user':`, e, "String recibido:", rawBackendResponse);
            }
        } else if (rawBackendResponse && typeof rawBackendResponse === 'object') {
            result = rawBackendResponse;
            console.log(`JS: Resultado (ya era objeto) del backend:`, JSON.stringify(result));
        } else if (rawBackendResponse === null) {
            console.warn(`JS: El backend devolvió null explícitamente para 'delete_user'.`);
        }


        if (result && typeof result === 'object' && result.hasOwnProperty('success')) {
            if (result.success === true) {
                showSuccessModal("Eliminación Exitosa", result.message || `El usuario '${usernameToDelete}' ha sido eliminado.`);
                // La tabla se actualizará vía users_updated.emit() desde el backend si la eliminación fue exitosa.
            } else {
                // Fallo reportado por el backend (ej. no se pudo eliminar, permiso denegado por alguna razón no capturada antes)
                displayGeneralFeedback('error', result.message || `No se pudo eliminar al usuario '${usernameToDelete}'.`);
            }
        } else {
             console.error(`JS: Respuesta final interpretada como inesperada o malformada para 'delete_user':`, JSON.stringify(result), "(Original crudo:", rawBackendResponse,")");
            let errorMessage = `Error de comunicación con el servidor al eliminar usuario. Respuesta no reconocida.`;
            if (rawBackendResponse === null) {
                errorMessage = `El servidor devolvió una respuesta nula al intentar eliminar el usuario.`;
            }
            displayGeneralFeedback('error', errorMessage);
        }

    } catch (e) {
        console.error("JS: Error en la operación 'delete_user':", e);
        displayGeneralFeedback('error', `Error al eliminar usuario: ${e.message || e}`);
    } finally {
        userToDelete = null; // Limpiar el usuario a eliminar
        // if (confirmDeleteUserButton) confirmDeleteUserButton.disabled = false; // Habilitar de nuevo si se deshabilitó
    }
}

     // --- Listeners ---
     function setupListeners() {
        console.log("User Logic: Configurando listeners...");

        // Listener Dark Mode Toggle (si existe el botón)
        if (darkModeToggle) {
            darkModeToggle.addEventListener('click', toggleTheme);
        } else {
            console.warn("Botón dark-mode-toggle no encontrado en users.html");
        }

        // Listener Delegado tabla
        userTableBody?.addEventListener('click', (event) => {
            const button = event.target.closest('button');
            if (!button || !userTableBody.contains(button) || button.disabled) return;
            const userId = parseInt(button.dataset.id);
            const username = button.dataset.username;
            if (isNaN(userId)) { console.error("ID inválido en el botón:", button.dataset); return; } // Username puede ser null/undefined temporalmente

            if (button.classList.contains('edit-user-btn')) {
                 const role = button.dataset.role;
                 if(role !== undefined && username !== undefined) openEditUserModal({ id: userId, username: username || 'N/A', role: role });
                 else console.error("Faltan datos para editar:", button.dataset);
            } else if (button.classList.contains('reset-pass-btn')) {
                 if(username !== undefined) openResetPasswordModal(userId, username || 'N/A');
                 else console.error("Falta username para resetear:", button.dataset)
            } else if (button.classList.contains('delete-user-btn')) {
                 if(username !== undefined) confirmDeleteUser({ id: userId, username: username || 'N/A' });
                  else console.error("Falta username para eliminar:", button.dataset)
            }
        });

        // Listeners modales y botones generales
        if (addUserButton) addUserButton.addEventListener('click', openAddUserModal); else console.warn("addUserButton no encontrado");
        if (closeUserModalButton) closeUserModalButton.addEventListener('click', closeUserModal); else console.warn("closeUserModalButton no encontrado");
        if (cancelUserModalButton) cancelUserModalButton.addEventListener('click', closeUserModal); else console.warn("cancelUserModalButton no encontrado");
        if (userForm) userForm.addEventListener('submit', handleUserFormSubmit); else console.warn("userForm no encontrado");
        if (backToInventoryButton) backToInventoryButton.addEventListener('click', () => { if (backend) backend.navigate_to('inventory'); }); else console.warn("backToInventoryButton no encontrado");
        if (confirmDeleteUserButton) confirmDeleteUserButton.addEventListener('click', executeDeleteUser); else console.warn("confirmDeleteUserButton no encontrado");
        if (cancelDeleteUserButton) cancelDeleteUserButton.addEventListener('click', cancelDeleteUserAction); else console.warn("cancelDeleteUserButton no encontrado");
        if (logoutButton) {
            logoutButton.addEventListener('click', () => { if (backend) { backend.request_close_application(); }});
        } else { console.warn("logoutButton no encontrado");}
        // Listener para el botón Aceptar del modal de éxito
        if (acceptSuccessModalButton) acceptSuccessModalButton.addEventListener('click', hideSuccessModal); else console.warn("acceptSuccessModalButton no encontrado");
        // Listeners para el modal de resetear contraseña
        if (resetPasswordForm) resetPasswordForm.addEventListener('submit', handleResetPasswordSubmit); else console.warn("resetPasswordForm no encontrado");
        if (cancelResetModalButton) cancelResetModalButton.addEventListener('click', closeResetPasswordModal); else console.warn("cancelResetModalButton no encontrado");
        if (closeResetModalButton) closeResetModalButton.addEventListener('click', closeResetPasswordModal); else console.warn("closeResetModalButton no encontrado");

        console.log("User Logic: Listeners configurados.");
     }

     // --- Iniciar ---
     loadTheme(); // Carga el tema ANTES de conectar
     connectAndInitialize();
     setupListeners();

});