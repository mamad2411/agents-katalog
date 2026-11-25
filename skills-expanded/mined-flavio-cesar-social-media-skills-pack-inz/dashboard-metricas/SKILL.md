---
name: dashboard-metricas
description: "Cria dashboards interativos de métricas e relatórios de performance em HTML profissional com gráficos Chart.js, KPIs animados, tabelas rankeadas e análise estratégica. Use esta skill sempre que alguém pedir para criar um dashboard, relatório de métricas, painel de analytics, relatório visual de performance, ou qualquer tipo de visualização de dados de redes sociais. Também aciona quando mencionarem 'dashboard', 'relatório visual', 'painel de métricas', 'analytics visual', 'relatório HTML', ou pedirem para transformar dados em visualização interativa."
---

# Estrutura completa do relatório HTML

Este documento detalha a implementação técnica de cada seção do relatório. Use como referência ao construir o HTML.

## Table of Contents

1. [Head e dependências](#head)
2. [CSS Variables e Design System](#css)
3. [Topbar](#topbar)
4. [Header](#header)
5. [KPIs](#kpis)
6. [Distribuição por formato](#formato)
7. [Descoberta](#descoberta)
8. [Engajamento detalhado](#engajamento)
9. [Top 10 conteúdos](#top10)
10. [Bottom 5 conteúdos](#bottom5)
11. [Conversão de seguidores](#conversao)
12. [Horários mais ativos](#horarios)
13. [Demografia](#demografia)
14. [Insights estratégicos](#insights)
15. [Recomendações](#recomendacoes)
16. [Footer](#footer)
17. [JavaScript: animações e interatividade](#javascript)

---

## Head e dependências <a name="head"></a>

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
```

Fonte via Google Fonts — usar a fonte da marca do cliente. Default: Inter com pesos 300-900.

```html
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
</style>
```

---

## CSS Variables e Design System <a name="css"></a>

### Tema escuro (padrão — visual de dashboard)

```css
:root {
  --primary: #E8612D;       /* COR PRIMÁRIA DA MARCA */
  --primary-glow: rgba(232,97,45,0.15);
  --secondary: #1A1A2E;     /* COR SECUNDÁRIA */
  --bg: #0F1117;
  --surface: #1A1D27;
  --surface2: #242836;
  --surface3: #2E3345;
  --border: #2E3345;
  --text: #E5E7EB;
  --text2: #9CA3AF;
  --text3: #6B7280;
  --green: #22C55E;
  --green-bg: rgba(34,197,94,0.12);
  --red: #EF4444;
  --red-bg: rgba(239,68,68,0.12);
  --blue: #3B82F6;
  --purple: #8B5CF6;
  --pink: #EC4899;
  --cyan: #06B6D4;
  --yellow: #EAB308;
  --yellow-bg: rgba(234,179,8,0.12);
}
```

### Tema claro (alternativa para marcas com identidade clara)

```css
:root {
  --primary: #E8612D;
  --bg: #F8FAFC;
  --surface: #FFFFFF;
  --surface2: #F1F5F9;
  --surface3: #E2E8F0;
  --border: #E2E8F0;
  --text: #0F172A;
  --text2: #475569;
  --text3: #94A3B8;
  /* greens, reds, etc. ficam iguais */
}
```

### Componentes base

```css
/* Topbar sticky com blur */
.topbar {
  position: sticky; top: 0; z-index: 100;
  background: rgba(15,17,23,0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
  padding: 14px 32px;
  display: flex; align-items: center; justify-content: space-between;
}

/* Cards padrão */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  transition: border-color 0.3s;
}
.card:hover { border-color: rgba(var(--primary-rgb), 0.3); }

/* KPI cards */
.kpi {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px 24px;
}
.kpi-value { font-size: 1.9em; font-weight: 800; }
.kpi-change.up { color: var(--green); background: var(--green-bg); }
.kpi-change.down { color: var(--red); background: var(--red-bg); }

/* Tabs */
.tabs {
  display: flex; gap: 4px;
  background: var(--surface);
  border-radius: 8px; padding: 3px;
  border: 1px solid var(--border);
}
.tab {
  padding: 6px 16px; border-radius: 6px;
  font-size: 0.8em; font-weight: 600;
  color: var(--text3); cursor: pointer;
  border: none; background: none;
}
.tab.active { background: var(--primary); color: #fff; }

/* Seções com animação de entrada */
.section {
  margin: 40px 0;
  opacity: 0; transform: translateY(20px);
  transition: all 0.6s ease;
}
.section.visible { opacity: 1; transform: translateY(0); }
```

---

## Topbar <a name="topbar"></a>

Barra sticky no topo com nome do perfil e crédito.

```html
<div class="topbar">
  <div class="topbar-left">
    <div class="topbar-logo"></div>  <!-- ponto com cor primária -->
    <span>instagram analytics — @perfil</span>
  </div>
  <div class="topbar-right">gerado por [agência/ferramenta]</div>
</div>
```

Se o cliente tiver logo, substituir o ponto por `<img>` com max-height: 24px.

---

## Header <a name="header"></a>

```html
<div class="header">
  <h1>relatório de <span style="color:var(--primary)">performance</span></h1>
  <div class="header-period">
    <svg><!-- ícone calendário --></svg>
    [período] ([duração])
  </div>
</div>
```

---

## KPIs <a name="kpis"></a>

Grid de 4 colunas (responsivo: 2 em tablet, 1 em mobile). Cada KPI:

```html
<div class="kpi">
  <div class="kpi-label">NOME DA MÉTRICA</div>
  <div class="kpi-value"><span class="counter" data-target="[NÚMERO]">0</span></div>
  <div class="kpi-change up">↑ +XX%</div>  <!-- ou .down ou .flat -->
  <div class="kpi-sub">contexto adicional</div>
</div>
```

KPIs típicos para Instagram: visualizações, contas alcançadas, interações, novos seguidores, total seguidores, visitas ao perfil, atividade do perfil, toques em link.

Adaptar conforme a plataforma e os dados disponíveis. Quanto mais KPIs com variação % (comparação com período anterior), melhor.

---

## Distribuição por formato <a name="formato"></a>

Dois gráficos lado a lado: um doughnut para views e um para interações. Com tabs para alternar.

Usar Chart.js doughnut com:
- `cutout: '68%'` para o visual de anel
- `borderColor` igual ao background do card para separar os segmentos
- `hoverOffset: 8` para destaque no hover
- Legend na posição bottom

---

## Descoberta <a name="descoberta"></a>

Doughnut chart mostrando % de seguidores vs não seguidores. Importante para mostrar capacidade de alcançar público novo.

---

## Engajamento detalhado <a name="engajamento"></a>

Tabs alternando entre formatos (reels/posts/stories). Cada tab mostra:

1. **Mini cards** em grid (5 colunas): curtidas, comentários, salvamentos, compartilhamentos, reposts
2. **Gráfico** abaixo: radar chart para reels (mostra equilíbrio entre métricas), bar chart horizontal para posts

---

## Top 10 conteúdos <a name="top10"></a>

Tabela com colunas: #, conteúdo, formato, data, views, link.

```html
<tr onclick="window.open('[URL_DO_POST]', '_blank')">
  <td><span class="rank-num rank-1">1</span></td>
  <td class="post-title">[título]</td>
  <td><span class="post-format format-reel">reel</span></td>
  <td>[data]</td>
  <td class="post-views">[views]</td>
  <td><a class="post-link" href="[URL]" target="_blank">abrir ↗</a></td>
</tr>
```

Ranking visual:
- #1: gradiente dourado
- #2: gradiente prata
- #3: gradiente bronze
- #4+: cor neutra

O link "abrir ↗" aparece no hover da linha. Toda a linha é clicável.

Se o usuário fornecer URLs dos posts, usar os links reais. Senão, linkar para o perfil.

---

## Bottom 5 conteúdos <a name="bottom5"></a>

Mesma estrutura de tabela, mas com estilo diferenciado:
- Badge vermelho nos ranks
- Borda esquerda vermelha no hover
- Coluna extra ou sub-label mostrando o **pilar/tema** do conteúdo (importante para a análise)

Após a tabela, incluir um bloco de análise:

```html
<div class="worst-analysis">
  <h4>análise dos piores [formato] — padrão identificado</h4>
  <p>[análise cruzada identificando o que os piores performers têm em comum:
  tema desalinhado, formato, horário, etc. Comparar com os top performers
  para destacar o contraste. Incluir números específicos.]</p>
</div>
```

Usar tabs se houver dados separados por formato (reels vs posts).

---

## Conversão de seguidores <a name="conversao"></a>

Bar chart horizontal mostrando quais conteúdos trouxeram mais seguidores novos. Dados vêm da seção "conteúdo mais relevante por número de pessoas que começaram a seguir" do Instagram.

---

## Horários mais ativos <a name="horarios"></a>

Bar chart vertical com 8 barras (0h, 3h, 6h, 9h, 12h, 15h, 18h, 21h). Destaque visual no pico (cor primária mais forte). Label abaixo indicando "pico de atividade: XXh — janela ideal de postagem: XXh-XXh".

Usar gradiente de opacidade: barras mais altas = mais opacas/saturadas.

---

## Demografia <a name="demografia"></a>

Tabs alternando entre: faixa etária, cidades, gênero.

- **Faixa etária**: Bar chart vertical. Barra mais alta com cor primária saturada, demais com opacidade reduzida.
- **Cidades**: Horizontal bars CSS (não precisa ser Chart.js). Label da cidade + barra + percentual.
- **Gênero**: Doughnut chart com duas cores.

---

## Insights estratégicos <a name="insights"></a>

Sistema de accordion — cada insight é clicável para expandir/recolher.

```html
<div class="insight-item">
  <div class="insight-header" onclick="toggleInsight(this)">
    <div class="left">
      <span class="badge badge-positive">positivo</span>
      <h3>[título do insight]</h3>
    </div>
    <svg class="arrow"><!-- chevron --></svg>
  </div>
  <div class="insight-body">
    <div class="insight-content">
      [texto analítico com <span class="highlight">destaques</span>
      e <span class="metric-inline">métricas inline</span>]
    </div>
  </div>
</div>
```

Classes de badge: `badge-positive` (verde), `badge-critical` (vermelho), `badge-warning` (amarelo), `badge-info` (azul).

O primeiro insight já vem aberto por padrão.

### Tipos de insight que o relatório deve gerar

Mínimo 5, máximo 8 insights. Sempre incluir:

1. **Visão geral do crescimento** — o perfil está crescendo, estagnado ou caindo? Qual a velocidade?
2. **Formato dominante** — qual formato gera mais alcance e engajamento? Por quê?
3. **Qualidade do engajamento** — razão saves/likes (indicador de autoridade), shares/followers (viralização)
4. **Ponto fraco principal** — sempre identificar o maior gargalo (link na bio, stories, frequência, etc.)
5. **Padrão dos top performers** — o que os melhores conteúdos têm em comum
6. **Perfil demográfico** — a audiência que chega está alinhada com o objetivo do perfil?

Opcionais (se dados permitirem):
- Comparação com período anterior
- Análise de horário vs performance
- Taxa de conversão do funil (impressão → perfil → link → ação)

---

## Recomendações <a name="recomendacoes"></a>

Grid de 2 colunas com cards numerados:

```html
<div class="rec-card">
  <div class="rec-num">[N]</div>
  <div>
    <h4>[título acionável]</h4>
    <p>[descrição com referência a dados específicos]</p>
  </div>
</div>
```

Ordenar por impacto: a recomendação mais importante primeiro. Cada uma deve referenciar uma métrica específica do relatório.

---

## Footer <a name="footer"></a>

```html
<div class="footer">
  <p>relatório gerado por <span class="brand">[agência/ferramenta]</span> — @[perfil] — [mês/ano]</p>
</div>
```

---

## JavaScript: animações e interatividade <a name="javascript"></a>

### Chart.js defaults

```javascript
Chart.defaults.color = '#9CA3AF';
Chart.defaults.font.family = '[FONTE DA MARCA]';
Chart.defaults.font.size = 12;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.pointStyle = 'circle';
Chart.defaults.plugins.legend.labels.padding = 16;
```

### Counter animation (KPIs)

```javascript
function animateCounter(el) {
  const target = parseInt(el.dataset.target);
  const duration = 1800;
  const start = performance.now();
  function update(now) {
    const p = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.floor(eased * target).toLocaleString('pt-BR');
    if (p < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}
```

### Tabs

```javascript
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    const group = tab.closest('[data-group]') || tab.closest('.tabs');
    group.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    const targetId = tab.dataset.tab;
    const section = tab.closest('.section');
    section.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
    document.getElementById(targetId).classList.add('active');
  });
});
```

### Insight accordion

```javascript
function toggleInsight(header) {
  const item = header.closest('.insight-item');
  const wasOpen = item.classList.contains('open');
  document.querySelectorAll('.insight-item').forEach(i => i.classList.remove('open'));
  if (!wasOpen) item.classList.add('open');
}
```

### Scroll animation (IntersectionObserver)

```javascript
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      e.target.querySelectorAll('.counter').forEach(c => animateCounter(c));
    }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.section').forEach(s => obs.observe(s));
```

### Responsividade

```css
@media (max-width: 900px) {
  .kpi-row { grid-template-columns: repeat(2, 1fr); }
  .grid-2, .grid-3, .rec-grid { grid-template-columns: 1fr; }
}
@media (max-width: 600px) {
  .kpi-row { grid-template-columns: 1fr; }
}
```

