// logica_dashboard.js (COMPLETO)

document.addEventListener('DOMContentLoaded', () => {
    const userRoleDisplay = document.getElementById('user-role-display');
    const logoutButton = document.getElementById('logout-button');
    const userMgmtButton = document.getElementById('user-mgmt-button');
    const inventoryMgmtButton = document.getElementById('inventory-mgmt-button');

    const kpiTotalEquipos = document.getElementById('kpi-total-equipos');
    const kpiMantenimientosProx = document.getElementById('kpi-mantenimientos-prox');
    const kpiTotalUsuarios = document.getElementById('kpi-total-usuarios');

    const chartTiposEl = document.getElementById('chart-tipos-equipo');
    const chartEstatusEl = document.getElementById('chart-estatus-equipo');
    const chartDepartamentosEl = document.getElementById('chart-departamentos');
    const chartSedesEl = document.getElementById('chart-sedes');
    const sedeSelectorDashboard = document.getElementById('sede-selector-dashboard');
    const kpiEquiposSedeActual = document.getElementById('kpi-equipos-sede-actual');
    const kpiEquiposSedeActualLabel = document.getElementById('kpi-equipos-sede-actual-label');

    let backend = null;
    let currentUserRole = 'read_only';
    let chartTipos, chartEstatus, chartDepartamentos, chartSedes;
    const allCharts = [];

    function connectAndInitialize() {
        const tryConnect = setInterval(() => {
            if (typeof qt !== 'undefined' && qt.webChannelTransport) {
                clearInterval(tryConnect);
                new QWebChannel(qt.webChannelTransport, (channel) => {
                    if (channel.objects.backend) {
                        backend = channel.objects.backend;
                        initializeSession();
                    } else {
                        showErrorInAllCharts("Error de conexión con Backend.");
                    }
                });
            }
        }, 200);
        setTimeout(() => {
            if (!backend) {
                clearInterval(tryConnect);
                showErrorInAllCharts("Timeout de conexión con Backend.");
            }
        }, 10000);
    }

    async function initializeSession() {
        if (!backend) return;
        try {
            currentUserRole = await backend.get_current_role();
            if(userRoleDisplay) userRoleDisplay.textContent = currentUserRole.charAt(0).toUpperCase() + currentUserRole.slice(1);
            adjustUIVisibility();
            await loadDashboardData(); // Carga inicial
        } catch (error) {
            showErrorInAllCharts("Error al cargar datos de sesión.");
        }
    }
    
    function adjustUIVisibility() {
        document.querySelectorAll('.requires-admin').forEach(el => {
            el.style.display = (currentUserRole === 'admin') ? 'inline-block' : 'none';
        });
    }

    async function loadDashboardData() {
        if (!backend) {
            showErrorInAllCharts("Backend no disponible.");
            return;
        }
        showLoadingInAllCharts();
        const sedeSeleccionada = sedeSelectorDashboard ? sedeSelectorDashboard.value : "";
        console.log(`Dashboard JS: Cargando datos para sede: '${sedeSeleccionada || "TODAS"}'`);

        try {
            const jsonData = await backend.get_dashboard_data(sedeSeleccionada);
            const data = JSON.parse(jsonData);

            if (data.error) {
                showErrorInAllCharts(data.error);
                return;
            }
            console.log("Dashboard JS: Datos recibidos:", data);

            if (kpiTotalEquipos) kpiTotalEquipos.textContent = data.total_equipos ?? '-';
            if (kpiMantenimientosProx) kpiMantenimientosProx.textContent = data.mantenimientos_proximos_30d ?? '-';
            if (kpiTotalUsuarios) kpiTotalUsuarios.textContent = data.total_usuarios ?? '-';

            if (sedeSelectorDashboard && (sedeSelectorDashboard.options.length <= 1 && data.lista_sedes?.length > 0)) {
                const valorActual = sedeSelectorDashboard.value;
                while (sedeSelectorDashboard.options.length > 1) sedeSelectorDashboard.remove(1);
                data.lista_sedes.sort().forEach(sede => {
                    if (sede?.trim()) {
                        const option = new Option(sede.trim(), sede.trim());
                        sedeSelectorDashboard.add(option);
                    }
                });
                if (Array.from(sedeSelectorDashboard.options).some(opt => opt.value === valorActual)) {
                    sedeSelectorDashboard.value = valorActual;
                } else {
                     sedeSelectorDashboard.value = "";
                }
            }
            if (kpiEquiposSedeActual) kpiEquiposSedeActual.textContent = data.equipos_en_sede_seleccionada ?? '-';
            if (kpiEquiposSedeActualLabel) {
            if (sedeSeleccionada && sedeSeleccionada.trim() !== "") {
                kpiEquiposSedeActualLabel.textContent = `Equipos en ${sedeSeleccionada}`;
            } else {
                kpiEquiposSedeActualLabel.textContent = "Total Equipos (Todas Sedes)"; // O igual que el KPI 1
            }
            }
            allCharts.forEach(chartInstance => chartInstance?.dispose());
            allCharts.length = 0;
            const echartTheme = null;
            const defaultBgColor = '#FFFFFF';
            const defaultTextColor = '#333333';
            const sedeSubtext = sedeSeleccionada ? ` (Sede: ${sedeSeleccionada})` : ' (Todas las Sedes)';

            // Gráfico 1: Equipos por Tipo
            if (chartTiposEl && data.equipos_por_tipo) {
                chartTipos = echarts.init(chartTiposEl, echartTheme);
                chartTipos.setOption({
                    backgroundColor: defaultBgColor,
                    title: { text: 'Equipos por Tipo' + sedeSubtext, left: 'center', textStyle: { color: defaultTextColor, fontSize: 16 } },
                    tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c} ({d}%)' },
                    legend: { type: 'scroll', orient: 'vertical', left: 10, top: 40, bottom: 20, data: data.equipos_por_tipo.map(item => item.name), textStyle: { color: defaultTextColor } },
                    series: [{ name: 'Tipo', type: 'pie', radius: ['45%', '70%'], center: ['60%', '55%'], data: data.equipos_por_tipo, itemStyle: { borderRadius: 8, borderColor: defaultBgColor, borderWidth: 2 } }]
                });
                allCharts.push(chartTipos);
            } else if (chartTiposEl) { showErrorInChart("Datos no disponibles para 'Equipos por Tipo'.", chartTiposEl); }

            // Gráfico 2: Equipos por Estatus
            if (chartEstatusEl && data.equipos_por_estatus) {
                chartEstatus = echarts.init(chartEstatusEl, echartTheme);
                chartEstatus.setOption({
                    backgroundColor: defaultBgColor,
                    title: { text: 'Equipos por Estatus' + sedeSubtext, left: 'center', textStyle: { color: defaultTextColor, fontSize: 16 } },
                    tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c} ({d}%)' },
                    legend: { orient: 'vertical', left: 10, top: 40, data: data.equipos_por_estatus.map(item => item.name), textStyle: { color: defaultTextColor } },
                    series: [{ name: 'Estatus', type: 'pie', radius: '60%', center: ['60%', '55%'], data: data.equipos_por_estatus }]
                });
                allCharts.push(chartEstatus);
            } else if (chartEstatusEl) { showErrorInChart("Datos no disponibles para 'Equipos por Estatus'.", chartEstatusEl); }

            // Gráfico 3: Equipos por Departamento
            if (chartDepartamentosEl && data.equipos_por_departamento) {
                const deptDataOriginal = data.equipos_por_departamento.sort((a, b) => b.value - a.value);
                const MAX_DEPT_NAME_LENGTH = 15;
                const deptLabelsShortened = deptDataOriginal.map(item => (item.name?.length > MAX_DEPT_NAME_LENGTH ? item.name.substring(0, MAX_DEPT_NAME_LENGTH - 3) + "..." : item.name || "N/A"));
                chartDepartamentos = echarts.init(chartDepartamentosEl, echartTheme);
                chartDepartamentos.setOption({
                    backgroundColor: defaultBgColor,
                    title: { text: 'Equipos por Departamento' + sedeSubtext, left: 'center', textStyle: { color: defaultTextColor, fontSize: 16 }, subtext: deptDataOriginal.length === 0 ? 'Sin datos para esta selección' : '', subtextStyle: {color: '#777'} },
                    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, formatter: p => `${deptDataOriginal[p[0].dataIndex]?.name || 'N/A'}<br/>${p[0].marker}${p[0].seriesName}: ${p[0].value}` },
                    grid: { left: '3%', right: '4%', bottom: '5%', top: '22%', containLabel: true },
                    xAxis: { type: 'category', data: deptLabelsShortened, axisLabel: { interval: 0, rotate: 40, color: defaultTextColor, fontSize: 9 }, axisTick: { alignWithLabel: true } },
                    yAxis: { type: 'value', axisLabel: { color: defaultTextColor } },
                    dataZoom: deptDataOriginal.length > 12 ? [{ type: 'slider', bottom: 5, height: 18, startValue: 0, endValue: 11 }] : [],
                    series: [{ name: 'Cantidad', type: 'bar', data: deptDataOriginal.map(item => item.value), barWidth: '50%', itemStyle: { borderRadius: [4, 4, 0, 0] } }]
                });
                allCharts.push(chartDepartamentos);
            } else if (chartDepartamentosEl) { showErrorInChart(`Datos no disponibles para 'Equipos por Departamento'${sedeSubtext}.`, chartDepartamentosEl); }

            // Gráfico 4: Equipos por Sede (No se filtra por sede seleccionada)
            if (chartSedesEl && data.equipos_por_sede) {
                const sedeData = data.equipos_por_sede.sort((a,b) => b.value - a.value).slice(0, 15);
                chartSedes = echarts.init(chartSedesEl, echartTheme);
                chartSedes.setOption({
                    backgroundColor: defaultBgColor,
                    title: { text: 'Equipos por Sede (Top 15)', left: 'center', textStyle: { color: defaultTextColor, fontSize: 16 } },
                    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                    grid: { left: '3%', right: '4%', bottom: '3%', top: '18%', containLabel: true },
                    xAxis: { type: 'value', axisLabel: { color: defaultTextColor } },
                    yAxis: { type: 'category', data: sedeData.map(item => item.name || "N/A").reverse(), axisLabel: { color: defaultTextColor, fontSize: 10 } },
                    series: [{ name: 'Cantidad', type: 'bar', data: sedeData.map(item => item.value).reverse(), barWidth: '50%', itemStyle: { borderRadius: [0, 4, 4, 0] } }]
                });
                allCharts.push(chartSedes);
            } else if (chartSedesEl) { showErrorInChart("Datos no disponibles para 'Equipos por Sede'.", chartSedesEl); }

        } catch (error) {
            console.error("Dashboard JS: Error fatal cargando o parseando datos:", error);
            showErrorInAllCharts("Error al procesar datos del dashboard.");
        }
    }

    function showLoadingInAllCharts() {
        [chartTiposEl, chartEstatusEl, chartDepartamentosEl, chartSedesEl].forEach(el => {
            if (el) {
                const instance = echarts.getInstanceByDom(el);
                if (instance?.showLoading) instance.showLoading('default', { text: 'Cargando...', color: '#0078D4', maskColor: 'rgba(255, 255, 255, 0.7)' });
                else el.innerHTML = '<p class="text-center text-gray-500 p-4">Cargando...</p>';
            }
        });
    }

    function showErrorInChart(message, specificElement) { // Para un solo gráfico
        if (specificElement) {
            const instance = echarts.getInstanceByDom(specificElement);
            if (instance) instance.dispose();
            specificElement.innerHTML = `<div class="flex items-center justify-center h-full"><p class="text-center text-red-600 p-4"><i class="fas fa-exclamation-triangle mr-2"></i>${message}</p></div>`;
        }
    }
    
    function showErrorInAllCharts(message) { // Para todos los gráficos
        [chartTiposEl, chartEstatusEl, chartDepartamentosEl, chartSedesEl].forEach(el => showErrorInChart(message, el));
    }


    // --- Event Listeners ---
    logoutButton?.addEventListener('click', () => backend?.request_close_application());
    userMgmtButton?.addEventListener('click', () => (backend && currentUserRole === 'admin') && backend.navigate_to('users'));
    inventoryMgmtButton?.addEventListener('click', () => backend?.navigate_to('inventory'));
    
    if (sedeSelectorDashboard) {
        sedeSelectorDashboard.addEventListener('change', () => {
            console.log(`Dashboard JS: Filtro de sede cambiado a: ${sedeSelectorDashboard.value}`);
            loadDashboardData();
        });
    }
    
    window.addEventListener('resize', () => {
        allCharts.forEach(chart => chart?.resize());
    });

    connectAndInitialize();
});