---
name: data-build-dashboard
description: Constrói um dashboard HTML interativo com gráficos, filtros e tabelas no tema Evolution (fundo escuro, acento #00FFA7, fonte Inter). Use quando precisar de uma visão executiva com cards de KPI, transformar resultados de query em relatório compartilhável, construir um snapshot de monitoramento de time, ou precisar de múltiplos gráficos com filtros em um arquivo HTML abrível no browser. Fontes: Stripe (`int-stripe`), Omie (`int-omie`), Licensing (`int-licensing`), Evo CRM (`int-evo-crm`).
argument-hint: "<descrição do dashboard> [fonte de dados]"
---

# data-build-dashboard — Construir Dashboards Interativos

Gera um arquivo HTML auto-contido com gráficos, filtros, tabelas e estilo profissional no tema Evolution. Abre diretamente no browser — sem servidor ou dependências externas.

## Uso

```
/data-build-dashboard <descrição do dashboard> [fonte de dados]
```

## Fluxo de Trabalho

### 1. Entender os Requisitos do Dashboard

Determinar:

- **Propósito**: Visão executiva, monitoramento operacional, análise aprofundada, relatório de time
- **Audiência**: Quem vai usar este dashboard?
- **Métricas-chave**: Quais números importam mais?
- **Dimensões**: Por quais campos o usuário deve conseguir filtrar ou segmentar?
- **Fonte de dados**: Query ao vivo, dados colados, arquivo CSV, ou dados de exemplo

### 2. Coletar os Dados

**Se fonte de dados estiver disponível via skill:**
1. Usar `int-stripe`, `int-omie`, `int-licensing` ou `int-evo-crm` conforme necessário
2. Executar as queries PostgreSQL necessárias
3. Incorporar os resultados como JSON dentro do arquivo HTML

**Se dados forem colados ou enviados como arquivo:**
1. Fazer parse e limpeza dos dados
2. Incorporar como JSON no dashboard

**Se trabalhando a partir de uma descrição sem dados:**
1. Criar um dataset de exemplo realista que corresponda ao schema descrito
2. Indicar no dashboard que usa dados de exemplo
3. Fornecer instruções para substituir pelos dados reais

### 3. Desenhar o Layout do Dashboard

Seguir o padrão de layout padrão:

```
┌──────────────────────────────────────────────────┐
│  Título do Dashboard               [Filtros ▼]   │
├────────────┬────────────┬────────────┬───────────┤
│  KPI Card  │  KPI Card  │  KPI Card  │ KPI Card  │
├────────────┴────────────┼────────────┴───────────┤
│                         │                        │
│    Gráfico Principal    │   Gráfico Secundário   │
│    (maior área)         │                        │
│                         │                        │
├─────────────────────────┴────────────────────────┤
│                                                  │
│    Tabela de Detalhes (ordenável, rolável)        │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Adaptar o layout ao conteúdo:**
- 2-4 cards de KPI no topo para números principais
- 1-3 gráficos na seção intermediária para tendências e breakdowns
- Tabela de detalhes opcional na parte inferior para drill-down
- Filtros no cabeçalho ou barra lateral conforme a complexidade

### 4. Construir o Dashboard HTML

Gerar um único arquivo HTML auto-contido seguindo o template base abaixo. O arquivo inclui:

**Estrutura (HTML):**
- Layout HTML5 semântico
- Grid responsivo usando CSS Grid ou Flexbox
- Controles de filtro (dropdowns, seletores de data, toggles)
- Cards de KPI com valores e labels
- Containers de gráficos
- Tabela de dados com cabeçalhos ordenáveis

**Estilo (CSS) — Tema Evolution:**
- Fundo escuro com camadas (#0A0A0A, #111111, #1A1A1A)
- Acento Evolution verde (#00FFA7) para destaques, bordas ativas e valores positivos
- Fonte Inter (Google Fonts CDN)
- Cards com bordas sutis e sombras escuras
- Design responsivo para diferentes tamanhos de tela

**Interatividade (JavaScript):**
- Chart.js para gráficos interativos (via CDN)
- Filtros dropdown que atualizam todos os gráficos e tabelas simultaneamente
- Colunas de tabela ordenáveis
- Tooltips de hover nos gráficos
- Formatação de números (vírgulas, moeda R$, percentuais)

**Dados (JSON incorporado):**
- Todos os dados incorporados diretamente no HTML como variáveis JavaScript
- Sem requisições de dados externos necessárias
- Dashboard funciona completamente offline

### 5. Implementar Tipos de Gráfico

Usar Chart.js para todos os gráficos. Padrões comuns para dashboards:

- **Gráfico de linha**: Tendências de séries temporais
- **Gráfico de barras**: Comparações de categorias
- **Gráfico de rosca (doughnut)**: Composição (quando <6 categorias)
- **Barras empilhadas**: Composição ao longo do tempo
- **Misto (barras + linha)**: Volume com sobreposição de taxa

### 6. Adicionar Interatividade

Usar os padrões de filtro e interatividade abaixo para filtros dropdown, filtros de intervalo de data, lógica de filtro combinada, tabelas ordenáveis e atualizações de gráficos.

### 7. Salvar e Abrir

1. Salvar o dashboard como arquivo HTML com nome descritivo (ex: `dashboard_financeiro_abril.html`)
2. Abrir no browser padrão do usuário
3. Confirmar que renderiza corretamente
4. Fornecer instruções para atualizar dados ou personalizar

---

## Template Base — Tema Evolution Dark

Todo dashboard segue esta estrutura:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Título do Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.1" integrity="sha384-jb8JQMbMoBUzgWatfe6COACi2ljcDdZQ2OxczGA3bGNeWe+6DChMTBJemed7ZnvJ" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns@3.0.0" integrity="sha384-cVMg8E3QFwTvGCDuK+ET4PD341jF3W8nO1auiXfuZNQkzbUUiBGLsIQUE+b1mxws" crossorigin="anonymous"></script>
    <style>
        /* Estilos do dashboard vão aqui */
    </style>
</head>
<body>
    <div class="dashboard-container">
        <header class="dashboard-header">
            <div class="header-left">
                <div class="logo-badge">EVO</div>
                <h1>Título do Dashboard</h1>
            </div>
            <div class="filters">
                <!-- Controles de filtro -->
            </div>
        </header>

        <section class="kpi-row">
            <!-- Cards de KPI -->
        </section>

        <section class="chart-row">
            <!-- Containers de gráficos -->
        </section>

        <section class="table-section">
            <!-- Tabela de dados -->
        </section>

        <footer class="dashboard-footer">
            <span>Dados até: <span id="data-date"></span> • BRT (UTC-3)</span>
        </footer>
    </div>

    <script>
        // Dados incorporados
        const DATA = [];

        // Lógica do dashboard
        class Dashboard {
            constructor(data) {
                this.rawData = data;
                this.filteredData = data;
                this.charts = {};
                this.init();
            }

            init() {
                this.setupFilters();
                this.renderKPIs();
                this.renderCharts();
                this.renderTable();
            }

            applyFilters() {
                this.filteredData = this.rawData.filter(row => {
                    return true; // placeholder
                });
                this.renderKPIs();
                this.updateCharts();
                this.renderTable();
            }
        }

        const dashboard = new Dashboard(DATA);
    </script>
</body>
</html>
```

## Sistema de Cores Evolution Dark

```css
:root {
    /* Camadas de fundo */
    --bg-base: #0A0A0A;
    --bg-surface: #111111;
    --bg-card: #1A1A1A;
    --bg-elevated: #222222;

    /* Texto */
    --text-primary: #F0F0F0;
    --text-secondary: #888888;
    --text-muted: #555555;

    /* Acento Evolution */
    --accent: #00FFA7;
    --accent-dim: rgba(0, 255, 167, 0.15);
    --accent-border: rgba(0, 255, 167, 0.3);

    /* Status */
    --positive: #00FFA7;
    --negative: #FF4D4D;
    --warning: #FFB547;
    --neutral: #888888;

    /* Bordas */
    --border: rgba(255, 255, 255, 0.08);
    --border-accent: rgba(0, 255, 167, 0.3);

    /* Tipografia */
    --font: 'Inter', -apple-system, sans-serif;

    /* Espaçamento */
    --gap: 16px;
    --radius: 10px;
    --radius-sm: 6px;
}
```

## Layout CSS

```css
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: var(--font);
    background: var(--bg-base);
    color: var(--text-primary);
    line-height: 1.5;
}

.dashboard-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: var(--gap);
}

.dashboard-header {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-bottom: 1px solid var(--accent-border);
    padding: 18px 24px;
    border-radius: var(--radius);
    margin-bottom: var(--gap);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-badge {
    background: var(--accent);
    color: #000;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 1px;
    padding: 4px 8px;
    border-radius: 4px;
}

.dashboard-header h1 {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
}

.dashboard-footer {
    text-align: center;
    font-size: 12px;
    color: var(--text-muted);
    padding: 16px 0 8px;
}
```

## Padrão de Card KPI

```html
<div class="kpi-card">
    <div class="kpi-label">Receita Total</div>
    <div class="kpi-value" id="kpi-revenue">R$ 0</div>
    <div class="kpi-change positive" id="kpi-revenue-change">+0%</div>
</div>
```

```css
.kpi-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--gap);
    margin-bottom: var(--gap);
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 24px;
    transition: border-color 0.2s;
}

.kpi-card:hover {
    border-color: var(--accent-border);
}

.kpi-label {
    font-size: 11px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 6px;
}

.kpi-change {
    font-size: 12px;
    font-weight: 500;
}

.kpi-change.positive { color: var(--positive); }
.kpi-change.negative { color: var(--negative); }
.kpi-change.neutral  { color: var(--neutral); }
```

```javascript
function renderKPI(elementId, value, previousValue, format = 'number') {
    const el = document.getElementById(elementId);
    const changeEl = document.getElementById(elementId + '-change');

    el.textContent = formatValue(value, format);

    if (previousValue && previousValue !== 0) {
        const pctChange = ((value - previousValue) / previousValue) * 100;
        const sign = pctChange >= 0 ? '+' : '';
        changeEl.textContent = `${sign}${pctChange.toFixed(1)}% vs período anterior`;
        changeEl.className = `kpi-change ${pctChange >= 0 ? 'positive' : 'negative'}`;
    }
}

function formatValue(value, format) {
    switch (format) {
        case 'currency':
            if (value >= 1e6) return `R$ ${(value / 1e6).toFixed(1)}M`;
            if (value >= 1e3) return `R$ ${(value / 1e3).toFixed(1)}K`;
            return `R$ ${value.toFixed(0)}`;
        case 'currency_usd':
            if (value >= 1e6) return `$${(value / 1e6).toFixed(1)}M`;
            if (value >= 1e3) return `$${(value / 1e3).toFixed(1)}K`;
            return `$${value.toFixed(0)}`;
        case 'percent':
            return `${value.toFixed(1)}%`;
        case 'number':
            if (value >= 1e6) return `${(value / 1e6).toFixed(1)}M`;
            if (value >= 1e3) return `${(value / 1e3).toFixed(1)}K`;
            return value.toLocaleString('pt-BR');
        default:
            return value.toString();
    }
}
```

## Integração Chart.js — Tema Evolution

### Paleta de Cores para Gráficos

```javascript
const COLORS = [
    '#00FFA7',  // Acento principal Evolution
    '#4C9FE8',  // Azul
    '#FFB547',  // Âmbar
    '#FF6B6B',  // Vermelho
    '#A78BFA',  // Roxo
    '#34D399',  // Verde esmeralda
    '#FB923C',  // Laranja
];

// Configuração global Chart.js para tema escuro
Chart.defaults.color = '#888888';
Chart.defaults.borderColor = 'rgba(255,255,255,0.06)';
Chart.defaults.font.family = 'Inter, sans-serif';
```

### Gráfico de Linha

```javascript
function createLineChart(canvasId, labels, datasets) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets.map((ds, i) => ({
                label: ds.label,
                data: ds.data,
                borderColor: COLORS[i % COLORS.length],
                backgroundColor: COLORS[i % COLORS.length] + '18',
                borderWidth: 2,
                fill: ds.fill || false,
                tension: 0.4,
                pointRadius: 3,
                pointHoverRadius: 6,
                pointBackgroundColor: COLORS[i % COLORS.length],
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        color: '#888888',
                    }
                },
                tooltip: {
                    backgroundColor: '#1A1A1A',
                    borderColor: 'rgba(0,255,167,0.3)',
                    borderWidth: 1,
                    titleColor: '#F0F0F0',
                    bodyColor: '#888888',
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.04)' },
                    ticks: { color: '#666666' }
                },
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255,255,255,0.04)' },
                    ticks: {
                        color: '#666666',
                        callback: function(value) {
                            return formatValue(value, 'number');
                        }
                    }
                }
            }
        }
    });
}
```

### Gráfico de Barras

```javascript
function createBarChart(canvasId, labels, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const isHorizontal = options.horizontal || labels.length > 8;

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: options.label || 'Valor',
                data: data,
                backgroundColor: options.singleColor
                    ? COLORS[0] + 'CC'
                    : COLORS.map(c => c + 'CC'),
                borderColor: options.singleColor
                    ? COLORS[0]
                    : COLORS,
                borderWidth: 1,
                borderRadius: 4,
                hoverBackgroundColor: COLORS[0],
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: isHorizontal ? 'y' : 'x',
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1A1A1A',
                    borderColor: 'rgba(0,255,167,0.3)',
                    borderWidth: 1,
                    titleColor: '#F0F0F0',
                    bodyColor: '#888888',
                    callbacks: {
                        label: function(context) {
                            return formatValue(context.parsed[isHorizontal ? 'x' : 'y'], options.format || 'number');
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255,255,255,0.04)', display: isHorizontal },
                    ticks: { color: '#666666' }
                },
                y: {
                    beginAtZero: !isHorizontal,
                    grid: { color: 'rgba(255,255,255,0.04)', display: !isHorizontal },
                    ticks: { color: '#666666' }
                }
            }
        }
    });
}
```

### Gráfico de Rosca

```javascript
function createDoughnutChart(canvasId, labels, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: COLORS.map(c => c + 'CC'),
                borderColor: '#111111',
                borderWidth: 3,
                hoverBorderColor: '#00FFA7',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: { usePointStyle: true, padding: 15, color: '#888888' }
                },
                tooltip: {
                    backgroundColor: '#1A1A1A',
                    borderColor: 'rgba(0,255,167,0.3)',
                    borderWidth: 1,
                    titleColor: '#F0F0F0',
                    bodyColor: '#888888',
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${formatValue(context.parsed, 'number')} (${pct}%)`;
                        }
                    }
                }
            }
        }
    });
}
```

### Atualizar Gráficos ao Filtrar

```javascript
function updateChart(chart, newLabels, newData) {
    chart.data.labels = newLabels;

    if (Array.isArray(newData[0])) {
        newData.forEach((data, i) => {
            chart.data.datasets[i].data = data;
        });
    } else {
        chart.data.datasets[0].data = newData;
    }

    chart.update('none'); // 'none' desativa animação para atualização instantânea
}
```

## Filtros e Interatividade

### Filtro Dropdown

```html
<div class="filter-group">
    <label for="filter-periodo">Período</label>
    <select id="filter-periodo" onchange="dashboard.applyFilters()">
        <option value="all">Todos</option>
    </select>
</div>
```

```css
.filters { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
.filter-group { display: flex; align-items: center; gap: 6px; }
.filter-group label { font-size: 11px; color: var(--text-secondary); }
.filter-group select,
.filter-group input[type="date"] {
    padding: 6px 10px;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    background: var(--bg-elevated);
    color: var(--text-primary);
    font-size: 12px;
    font-family: var(--font);
    outline: none;
    cursor: pointer;
}
.filter-group select:focus {
    border-color: var(--accent-border);
}
.filter-group select option { background: var(--bg-card); }
```

### Filtro de Intervalo de Data

```javascript
function filterByDateRange(data, dateField, startDate, endDate) {
    return data.filter(row => {
        const rowDate = new Date(row[dateField]);
        if (startDate && rowDate < new Date(startDate)) return false;
        if (endDate && rowDate > new Date(endDate)) return false;
        return true;
    });
}
```

### Lógica de Filtro Combinado

```javascript
applyFilters() {
    const plano = getFilterValue('filter-plano');
    const status = getFilterValue('filter-status');
    const startDate = document.getElementById('filter-date-start').value;
    const endDate = document.getElementById('filter-date-end').value;

    this.filteredData = this.rawData.filter(row => {
        if (plano && row.plano !== plano) return false;
        if (status && row.status !== status) return false;
        if (startDate && row.data < startDate) return false;
        if (endDate && row.data > endDate) return false;
        return true;
    });

    this.renderKPIs();
    this.updateCharts();
    this.renderTable();
}
```

### Tabela Ordenável

```javascript
function renderTable(containerId, data, columns) {
    const container = document.getElementById(containerId);
    let sortCol = null;
    let sortDir = 'desc';

    function render(sortedData) {
        let html = '<table class="data-table">';
        html += '<thead><tr>';
        columns.forEach(col => {
            const arrow = sortCol === col.field ? (sortDir === 'asc' ? ' ▲' : ' ▼') : '';
            html += `<th onclick="sortTable('${col.field}')" style="cursor:pointer">${col.label}${arrow}</th>`;
        });
        html += '</tr></thead><tbody>';
        sortedData.forEach(row => {
            html += '<tr>';
            columns.forEach(col => {
                const value = col.format ? formatValue(row[col.field], col.format) : row[col.field];
                html += `<td>${value}</td>`;
            });
            html += '</tr>';
        });
        html += '</tbody></table>';
        container.innerHTML = html;
    }

    window.sortTable = function(field) {
        if (sortCol === field) {
            sortDir = sortDir === 'asc' ? 'desc' : 'asc';
        } else {
            sortCol = field;
            sortDir = 'desc';
        }
        const sorted = [...data].sort((a, b) => {
            const aVal = a[field], bVal = b[field];
            const cmp = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
            return sortDir === 'asc' ? cmp : -cmp;
        });
        render(sorted);
    };

    render(data);
}
```

```css
.table-section {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 24px;
    overflow-x: auto;
    margin-bottom: var(--gap);
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

.data-table thead th {
    text-align: left;
    padding: 10px 12px;
    border-bottom: 1px solid var(--border);
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    white-space: nowrap;
    user-select: none;
}

.data-table thead th:hover { color: var(--accent); }
.data-table tbody td { padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.data-table tbody tr:hover { background: rgba(0, 255, 167, 0.03); }
.data-table tbody tr:last-child td { border-bottom: none; }
```

## Containers de Gráfico

```css
.chart-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: var(--gap);
    margin-bottom: var(--gap);
}

.chart-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 24px;
}

.chart-container h3 {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.chart-container canvas { max-height: 280px; }
```

## Design Responsivo

```css
@media (max-width: 768px) {
    .dashboard-header { flex-direction: column; align-items: flex-start; }
    .kpi-row { grid-template-columns: repeat(2, 1fr); }
    .chart-row { grid-template-columns: 1fr; }
    .filters { flex-direction: column; align-items: flex-start; }
}

@media print {
    body { background: #fff; color: #000; }
    .filters, .logo-badge { display: none; }
    .chart-container, .kpi-card { border: 1px solid #ddd; box-shadow: none; break-inside: avoid; }
}
```

## Performance para Datasets Grandes

| Tamanho dos Dados | Abordagem |
|---|---|
| <1.000 linhas | Incorporar diretamente. Interatividade completa. |
| 1.000–10.000 linhas | Incorporar no HTML. Pode precisar pré-agregar para gráficos. |
| 10.000–100.000 linhas | Pré-agregar server-side. Incorporar apenas dados agregados. |
| >100.000 linhas | Não adequado para dashboard client-side. Use BI tool ou pagine. |

```javascript
// Padrão de pré-agregação
const CHART_DATA = {
    receita_mensal: [
        { mes: '2025-01', receita: 150000, assinaturas: 120 },
        // ... 12 linhas em vez de 50.000
    ],
    top_planos: [
        { plano: 'Pro', receita: 45000 },
    ],
    kpis: {
        mrr_total: 198000,
        total_instancias: 15600,
        ticket_medio: 127,
    }
};
```

## Exemplos

```
/data-build-dashboard Dashboard de MRR com tendência mensal, breakdown por plano e mapa de instâncias ativas.
```

```
/data-build-dashboard Aqui estão os dados de instâncias do Licensing [cola CSV]. Montar dashboard com distribuição por país, versão e status.
```

```
/data-build-dashboard Criar dashboard executivo SaaS com MRR, churn, novos clientes e NPS. Usar dados de exemplo.
```

## Dicas

- Dashboards são arquivos HTML totalmente auto-contidos — compartilhe com qualquer pessoa enviando o arquivo
- Para dashboards em tempo real, considere conectar a um BI tool. Esses dashboards são snapshots pontuais
- Peça "modo apresentação" para fontes maiores e mais contraste
- O tema Evolution dark é o padrão; solicite "modo claro" apenas se necessário
