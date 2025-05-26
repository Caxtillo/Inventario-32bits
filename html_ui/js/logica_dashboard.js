document.addEventListener('DOMContentLoaded', () => {
    const userRoleDisplay = document.getElementById('user-role-display');
    const logoutButton = document.getElementById('logout-button');
    const userMgmtButton = document.getElementById('user-mgmt-button');
    const inventoryMgmtButton = document.getElementById('inventory-mgmt-button');

    // Referencias a contenedores de KPIs
    const kpiTotalEquipos = document.getElementById('kpi-total-equipos');
    const kpiMantenimientosProx = document.getElementById('kpi-mantenimientos-prox');
    const kpiTotalUsuarios = document.getElementById('kpi-total-usuarios');

    // Referencias a contenedores de gráficos
    const chartTiposEl = document.getElementById('chart-tipos-equipo');
    const chartEstatusEl = document.getElementById('chart-estatus-equipo');
    const chartDepartamentosEl = document.getElementById('chart-departamentos');
    const chartMarcasEl = document.getElementById('chart-marcas');

    let backend = null;
    let currentUserRole = 'read_only';

    // Instancias de ECharts
    let chartTipos, chartEstatus, chartDepartamentos, chartMarcas;
    const allCharts = [];

    // --- Lógica Tema Oscuro ELIMINADA ---

    function connectAndInitialize() {
        // initializeTheme(); // ELIMINADO

        const tryConnect = setInterval(() => {
            if (typeof qt !== 'undefined' && qt.webChannelTransport) {
                clearInterval(tryConnect);
                console.log("Dashboard: Conectando a QWebChannel...");
                new QWebChannel(qt.webChannelTransport, (channel) => {
                    if (channel.objects.backend) {
                        backend = channel.objects.backend;
                        console.log("Dashboard: Objeto Backend conectado:", backend);
                        initializeSession();
                    } else {
                        console.error("Dashboard: Error - Objeto 'backend' no encontrado.");
                        showErrorInCharts("Error de conexión con Backend.");
                    }
                });
            } else {
                console.log("Dashboard: Esperando qt.webChannelTransport...");
            }
        }, 200);
        setTimeout(() => {
            if (!backend) {
                clearInterval(tryConnect);
                console.error("Dashboard: Timeout Conexión");
                showErrorInCharts("Timeout de conexión con Backend.");
            }
        }, 10000);
    }

    async function initializeSession() {
        if (!backend) return;
        try {
            currentUserRole = await backend.get_current_role();
            if(userRoleDisplay) userRoleDisplay.textContent = currentUserRole.charAt(0).toUpperCase() + currentUserRole.slice(1);
            adjustUIVisibility();
            loadDashboardData();
        } catch (error) {
            console.error("Dashboard: Error inicializando sesión:", error);
            showErrorInCharts("Error al cargar datos iniciales.");
        }
    }
    
    function adjustUIVisibility() {
        const adminElements = document.querySelectorAll('.requires-admin');
        adminElements.forEach(el => {
            el.style.display = (currentUserRole === 'admin') ? 'inline-block' : 'none';
        });
    }

    async function loadDashboardData() {
        if (!backend) {
            showErrorInCharts("Backend no disponible.");
            return;
        }
        console.log("Dashboard: Solicitando datos del dashboard...");
        showLoadingInCharts();

        try {
            const jsonData = await backend.get_dashboard_data();
            const data = JSON.parse(jsonData);

            if (data.error) {
                console.error("Dashboard: Error del backend:", data.error);
                showErrorInCharts(data.error);
                return;
            }
            console.log("Dashboard: Datos recibidos:", data);

            if (kpiTotalEquipos) kpiTotalEquipos.textContent = data.total_equipos || 0;
            if (kpiMantenimientosProx) kpiMantenimientosProx.textContent = data.mantenimientos_proximos_30d || 0;
            if (kpiTotalUsuarios) kpiTotalUsuarios.textContent = data.total_usuarios || 0;

            allCharts.forEach(chartInstance => chartInstance?.dispose());
            allCharts.length = 0;

            const echartTheme = null; // Siempre tema claro por defecto de ECharts
            console.log("Dashboard: Initializing charts with default theme.");

            if (chartTiposEl && data.equipos_por_tipo) {
                chartTipos = echarts.init(chartTiposEl, echartTheme);
                chartTipos.setOption({
                    backgroundColor: '#ffffff', // Fondo siempre blanco
                    title: { text: 'Equipos por Tipo', left: 'center', textStyle: { color: '#333' } },
                    tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c} ({d}%)' },
                    legend: {
                        type: 'scroll',
                        orient: 'vertical',
                        left: 10,
                        top: 30,
                        bottom: 20,
                        data: data.equipos_por_tipo.map(item => item.name),
                        textStyle: { color: '#333' }
                    },
                    series: [{
                        name: 'Tipo Equipo', type: 'pie', radius: ['45%', '70%'], center: ['60%', '50%'],
                        avoidLabelOverlap: false, itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
                        label: { show: false, position: 'center' }, emphasis: { label: { show: true, fontSize: '20', fontWeight: 'bold' } },
                        labelLine: { show: false }, data: data.equipos_por_tipo
                    }]
                });
                allCharts.push(chartTipos);
            }

            if (chartEstatusEl && data.equipos_por_estatus) {
                chartEstatus = echarts.init(chartEstatusEl, echartTheme);
                chartEstatus.setOption({
                    backgroundColor: '#ffffff', // Fondo siempre blanco
                    title: { text: 'Equipos por Estatus', left: 'center', textStyle: { color: '#333' } },
                    tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c} ({d}%)' },
                    legend: {
                        orient: 'vertical', left: 10, top: 30, data: data.equipos_por_estatus.map(item => item.name),
                        textStyle: { color: '#333' }
                    },
                    series: [{
                        name: 'Estatus', type: 'pie', radius: '65%', center: ['60%', '55%'],
                        data: data.equipos_por_estatus, emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)'}}
                    }]
                });
                allCharts.push(chartEstatus);
            }
            
            if (chartDepartamentosEl && data.equipos_por_departamento) {
                const deptData = data.equipos_por_departamento.sort((a,b) => b.value - a.value);
                chartDepartamentos = echarts.init(chartDepartamentosEl, echartTheme);
                chartDepartamentos.setOption({
                    backgroundColor: '#ffffff', // Fondo siempre blanco
                    title: { text: 'Equipos por Departamento', left: 'center', textStyle: { color: '#333' } },
                    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                    grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
                    xAxis: { type: 'category', data: deptData.map(item => item.name), axisLabel: { interval: 0, rotate: 45, color: '#333' } },
                    yAxis: { type: 'value', axisLabel: { color: '#333' } },
                    series: [{ name: 'Cantidad', type: 'bar', data: deptData.map(item => item.value), barWidth: '60%' }]
                });
                allCharts.push(chartDepartamentos);
            }

            if (chartMarcasEl && data.equipos_por_marca) {
                const marcaData = data.equipos_por_marca.sort((a,b) => b.value - a.value).slice(0, 10);
                chartMarcas = echarts.init(chartMarcasEl, echartTheme);
                chartMarcas.setOption({
                    backgroundColor: '#ffffff', // Fondo siempre blanco
                    title: { text: 'Top 10 Marcas de Equipos', left: 'center', textStyle: { color: '#333' } },
                    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                    grid: { left: '3%', right: '4%', bottom: '3%', top: '15%', containLabel: true },
                    xAxis: { type: 'value', axisLabel: { color: '#333' } },
                    yAxis: { type: 'category', data: marcaData.map(item => item.name).reverse(), axisLabel: { color: '#333' } },
                    series: [{ name: 'Cantidad', type: 'bar', data: marcaData.map(item => item.value).reverse(), barWidth: '60%' }]
                });
                allCharts.push(chartMarcas);
            }

        } catch (error) {
            console.error("Dashboard: Error cargando o parseando datos del dashboard:", error);
            showErrorInCharts("Error al procesar datos del dashboard.");
        }
    }

    function showLoadingInCharts() {
        const chartElements = [chartTiposEl, chartEstatusEl, chartDepartamentosEl, chartMarcasEl];
        chartElements.forEach(el => {
            if (el) {
                const instance = echarts.getInstanceByDom(el);
                if (instance) instance.showLoading();
                else {
                    el.innerHTML = '<p class="text-center text-gray-500 p-4">Cargando gráfico...</p>';
                }
            }
        });
    }
    function showErrorInCharts(message) {
        const chartElements = [chartTiposEl, chartEstatusEl, chartDepartamentosEl, chartMarcasEl];
        chartElements.forEach(el => {
            if (el) {
                const instance = echarts.getInstanceByDom(el);
                if (instance) instance.dispose();
                el.innerHTML = `<p class="text-center text-red-500 p-4">${message}</p>`;
            }
        });
    }

    // --- Asignación de Event Listeners ---
    // darkModeToggle?.addEventListener('click', handleThemeToggle); // ELIMINADO

    logoutButton?.addEventListener('click', () => {
        if (backend) backend.request_close_application();
    });

    userMgmtButton?.addEventListener('click', () => {
        if (backend && currentUserRole === 'admin') {
            backend.navigate_to('users');
        }
    });

    inventoryMgmtButton?.addEventListener('click', () => {
        if (backend) {
            backend.navigate_to('inventory');
        }
    });
    
    window.addEventListener('resize', () => {
        allCharts.forEach(chartInstance => {
            if (chartInstance) {
                chartInstance.resize();
            }
        });
    });

    connectAndInitialize();
});