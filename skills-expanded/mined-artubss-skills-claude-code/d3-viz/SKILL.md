---
name: d3-viz
description: Criando visualizações de dados interativas usando d3.js. Esta habilidade deve ser usada ao criar gráficos customizados, diagramas de rede, visualizações geográficas ou qualquer visualização de dados complexa baseada em SVG que requeira controle fino sobre elementos visuais, transições ou interações. Use isto para visualizações personalizadas além das bibliotecas de gráficos padrão, seja em React, Vue, Svelte, JavaScript vanilla ou qualquer outro ambiente.
---

# Visualização com D3.js

## Visão geral

Esta habilidade fornece orientação para criar visualizações de dados sofisticadas e interativas usando d3.js. D3.js (Data-Driven Documents) se destaca ao vincular dados a elementos DOM e aplicar transformações orientadas por dados para criar visualizações personalizadas, de qualidade para publicação, com controle preciso sobre cada elemento visual. As técnicas funcionam em qualquer ambiente JavaScript, incluindo JavaScript vanilla, React, Vue, Svelte e outros frameworks.

## Quando usar d3.js

**Use d3.js para:**
- Visualizações personalizadas que exigem codificações visuais ou layouts únicos
- Explorações interativas com comportamentos complexos de pan, zoom ou brush
- Visualizações de redes/grafos (layouts força-direcionado, diagramas em árvore, hierarquias, diagramas de acordes)
- Visualizações geográficas com projeções personalizadas
- Visualizações que exigem transições suaves e coreografadas
- Gráficos de qualidade para publicação com controle fino de estilo
- Tipos de gráficos novos não disponíveis em bibliotecas padrão

**Considere alternativas para:**
- Visualizações 3D - use Three.js em vez disso

## Fluxo de trabalho principal

### 1. Configure d3.js

Importe d3 no topo do seu script:

```javascript
import * as d3 from 'd3';
```

Ou use a versão CDN (7.x):

```html
<script src="https://d3js.org/d3.v7.min.js"></script>
```

Todos os módulos (escalas, eixos, formas, transições, etc.) são acessíveis através do namespace `d3`.

### 2. Escolha o padrão de integração

**Padrão A: Manipulação direta do DOM (recomendado para a maioria dos casos)**
Use d3 para selecionar elementos DOM e manipulá-los imperativamente. Isso funciona em qualquer ambiente JavaScript:

```javascript
function drawChart(data) {
  if (!data || data.length === 0) return;

  const svg = d3.select('#chart'); // Selecione por ID, classe ou elemento DOM

  // Limpe conteúdo anterior
  svg.selectAll("*").remove();

  // Configure dimensões
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };

  // Crie escalas, eixos e desenhe visualização
  // ... código d3 aqui ...
}

// Chame quando dados mudarem
drawChart(myData);
```

**Padrão B: Renderização declarativa (para frameworks com templates)**
Use d3 para cálculos de dados (escalas, layouts), mas renderize elementos via seu framework:

```javascript
function getChartElements(data) {
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([0, 400]);

  return data.map((d, i) => ({
    x: 50,
    y: i * 30,
    width: xScale(d.value),
    height: 25
  }));
}

// Em React: {getChartElements(data).map((d, i) => <rect key={i} {...d} fill="steelblue" />)}
// Em Vue: diretiva v-for sobre o array retornado
// Em JS vanilla: Crie elementos manualmente a partir dos dados retornados
```

Use o Padrão A para visualizações complexas com transições, interações ou ao aproveitar as capacidades completas do d3. Use o Padrão B para visualizações mais simples ou quando seu framework prefere renderização declarativa.

### 3. Estruture o código da visualização

Siga esta estrutura padrão em sua função de desenho:

```javascript
function drawVisualization(data) {
  if (!data || data.length === 0) return;

  const svg = d3.select('#chart'); // Ou passe um seletor/elemento
  svg.selectAll("*").remove(); // Limpe renderização anterior

  // 1. Defina dimensões
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // 2. Crie grupo principal com margens
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // 3. Crie escalas
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]); // Nota: invertida para coordenadas SVG

  // 4. Crie e adicione eixos
  const xAxis = d3.axisBottom(xScale);
  const yAxis = d3.axisLeft(yScale);

  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(xAxis);

  g.append("g")
    .call(yAxis);

  // 5. Vincule dados e crie elementos visuais
  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 5)
    .attr("fill", "steelblue");
}

// Chame quando dados mudarem
drawVisualization(myData);
```

### 4. Implemente dimensionamento responsivo

Torne visualizações responsivas ao tamanho do container:

```javascript
function setupResponsiveChart(containerId, data) {
  const container = document.getElementById(containerId);
  const svg = d3.select(`#${containerId}`).append('svg');

  function updateChart() {
    const { width, height } = container.getBoundingClientRect();
    svg.attr('width', width).attr('height', height);

    // Redesenhe visualização com novas dimensões
    drawChart(data, svg, width, height);
  }

  // Atualize no carregamento inicial
  updateChart();

  // Atualize ao redimensionar janela
  window.addEventListener('resize', updateChart);

  // Retorne função de limpeza
  return () => window.removeEventListener('resize', updateChart);
}

// Uso:
// const cleanup = setupResponsiveChart('chart-container', myData);
// cleanup(); // Chame ao desmontar componente ou remover elemento
```

Ou use ResizeObserver para monitoramento mais direto do container:

```javascript
function setupResponsiveChartWithObserver(svgElement, data) {
  const observer = new ResizeObserver(() => {
    const { width, height } = svgElement.getBoundingClientRect();
    d3.select(svgElement)
      .attr('width', width)
      .attr('height', height);

    // Redesenhe visualização
    drawChart(data, d3.select(svgElement), width, height);
  });

  observer.observe(svgElement.parentElement);
  return () => observer.disconnect();
}
```

## Padrões de visualização comuns

### Gráfico de barras

```javascript
function drawBarChart(data, svgElement) {
  if (!data || data.length === 0) return;

  const svg = d3.select(svgElement);
  svg.selectAll("*").remove();

  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleBand()
    .domain(data.map(d => d.category))
    .range([0, innerWidth])
    .padding(0.1);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([innerHeight, 0]);

  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));

  g.append("g")
    .call(d3.axisLeft(yScale));

  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.category))
    .attr("y", d => yScale(d.value))
    .attr("width", xScale.bandwidth())
    .attr("height", d => innerHeight - yScale(d.value))
    .attr("fill", "steelblue");
}

// Uso:
// drawBarChart(myData, document.getElementById('chart'));
```

### Gráfico de linhas

```javascript
const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value))
  .curve(d3.curveMonotoneX); // Curva suave

g.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", "steelblue")
  .attr("stroke-width", 2)
  .attr("d", line);
```

### Gráfico de dispersão

```javascript
g.selectAll("circle")
  .data(data)
  .join("circle")
  .attr("cx", d => xScale(d.x))
  .attr("cy", d => yScale(d.y))
  .attr("r", d => sizeScale(d.size)) // Opcional: codificação de tamanho
  .attr("fill", d => colourScale(d.category)) // Opcional: codificação de cor
  .attr("opacity", 0.7);
```

### Diagrama de acordes

Um diagrama de acordes mostra relacionamentos entre entidades em um layout circular, com fitas representando fluxos entre elas:

```javascript
function drawChordDiagram(data) {
  // formato de dados: array de objetos com source, target e value
  // Exemplo: [{ source: 'A', target: 'B', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 600;
  const height = 600;
  const innerRadius = Math.min(width, height) * 0.3;
  const outerRadius = innerRadius + 30;

  // Crie matriz a partir dos dados
  const nodes = Array.from(new Set(data.flatMap(d => [d.source, d.target])));
  const matrix = Array.from({ length: nodes.length }, () => Array(nodes.length).fill(0));

  data.forEach(d => {
    const i = nodes.indexOf(d.source);
    const j = nodes.indexOf(d.target);
    matrix[i][j] += d.value;
    matrix[j][i] += d.value;
  });

  // Crie layout de acordes
  const chord = d3.chord()
    .padAngle(0.05)
    .sortSubgroups(d3.descending);

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

  const ribbon = d3.ribbon()
    .source(d => d.source)
    .target(d => d.target);

  const colourScale = d3.scaleOrdinal(d3.schemeCategory10)
    .domain(nodes);

  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);

  const chords = chord(matrix);

  // Desenhe fitas
  g.append("g")
    .attr("fill-opacity", 0.67)
    .selectAll("path")
    .data(chords)
    .join("path")
    .attr("d", ribbon)
    .attr("fill", d => colourScale(nodes[d.source.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.source.index])).darker());

  // Desenhe grupos (arcos)
  const group = g.append("g")
    .selectAll("g")
    .data(chords.groups)
    .join("g");

  group.append("path")
    .attr("d", arc)
    .attr("fill", d => colourScale(nodes[d.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.index])).darker());

  // Adicione labels
  group.append("text")
    .each(d => { d.angle = (d.startAngle + d.endAngle) / 2; })
    .attr("dy", "0.31em")
    .attr("transform", d => `rotate(${(d.angle * 180 / Math.PI) - 90})translate(${outerRadius + 30})${d.angle > Math.PI ? "rotate(180)" : ""}`)
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
    .text((d, i) => nodes[i])
    .style("font-size", "12px");
}
```

### Mapa de calor

Um mapa de calor usa cor para codificar valores em uma grade bidimensional, útil para mostrar padrões entre categorias:

```javascript
function drawHeatmap(data) {
  // formato de dados: array de objetos com row, column e value
  // Exemplo: [{ row: 'A', column: 'X', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 800;
  const height = 600;
  const margin = { top: 100, right: 30, bottom: 30, left: 100 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // Obtenha linhas e colunas únicas
  const rows = Array.from(new Set(data.map(d => d.row)));
  const columns = Array.from(new Set(data.map(d => d.column)));

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Crie escalas
  const xScale = d3.scaleBand()
    .domain(columns)
    .range([0, innerWidth])
    .padding(0.01);

  const yScale = d3.scaleBand()
    .domain(rows)
    .range([0, innerHeight])
    .padding(0.01);

  // Escala de cores para valores
  const colourScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, d3.max(data, d => d.value)]);

  // Desenhe retângulos
  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.column))
    .attr("y", d => yScale(d.row))
    .attr("width", xScale.bandwidth())
    .attr("height", yScale.bandwidth())
    .attr("fill", d => colourScale(d.value));

  // Adicione labels do eixo x
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(columns)
    .join("text")
    .attr("x", d => xScale(d) + xScale.bandwidth() / 2)
    .attr("y", -10)
    .attr("text-anchor", "middle")
    .text(d => d)
    .style("font-size", "12px");

  // Adicione labels do eixo y
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(rows)
    .join("text")
    .attr("x", -10)
    .attr("y", d => yScale(d) + yScale.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", "end")
    .text(d => d)
    .style("font-size", "12px");

  // Adicione legenda de cores
  const legendWidth = 20;
  const legendHeight = 200;
  const legend = svg.append("g")
    .attr("transform", `translate(${width - 60},${margin.top})`);

  const legendScale = d3.scaleLinear()
    .domain(colourScale.domain())
    .range([legendHeight, 0]);

  const legendAxis = d3.axisRight(legendScale)
    .ticks(5);

  // Desenhe gradiente de cores na legenda
  for (let i = 0; i < legendHeight; i++) {
    legend.append("rect")
      .attr("y", i)
      .attr("width", legendWidth)
      .attr("height", 1)
      .attr("fill", colourScale(legendScale.invert(i)));
  }

  legend.append("g")
    .attr("transform", `translate(${legendWidth},0)`)
    .call(legendAxis);
}
```

### Gráfico de pizza

```javascript
const pie = d3.pie()
  .value(d => d.value)
  .sort(null);

const arc = d3.arc()
  .innerRadius(0)
  .outerRadius(Math.min(width, height) / 2 - 20);

const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

const g = svg.append("g")
  .attr("transform", `translate(${width / 2},${height / 2})`);

g.selectAll("path")
  .data(pie(data))
  .join("path")
  .attr("d", arc)
  .attr("fill", (d, i) => colourScale(i))
  .attr("stroke", "white")
  .attr("stroke-width", 2);
```

### Rede força-direcionada

```javascript
const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id).distance(100))
  .force("charge", d3.forceManyBody().strength(-300))
  .force("center", d3.forceCenter(width / 2, height / 2));

const link = g.selectAll("line")
  .data(links)
  .join("line")
  .attr("stroke", "#999")
  .attr("stroke-width", 1);

const node = g.selectAll("circle")
  .data(nodes)
  .join("circle")
  .attr("r", 8)
  .attr("fill", "steelblue")
  .call(d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended));

simulation.on("tick", () => {
  link
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);
  
  node
    .attr("cx", d => d.x)
    .attr("cy", d => d.y);
});

function dragstarted(event) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  event.subject.fx = event.subject.x;
  event.subject.fy = event.subject.y;
}

function dragged(event) {
  event.subject.fx = event.x;
  event.subject.fy = event.y;
}

function dragended(event) {
  if (!event.active) simulation.alphaTarget(0);
  event.subject.fx = null;
  event.subject.fy = null;
}
```

## Adicionando interatividade

### Tooltips

```javascript
// Crie div tooltip (fora do SVG)
const tooltip = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("position", "absolute")
  .style("visibility", "hidden")
  .style("background-color", "white")
  .style("border", "1px solid #ddd")
  .style("padding", "10px")
  .style("border-radius", "4px")
  .style("pointer-events", "none");

// Adicione a elementos
circles
  .on("mouseover", function(event, d) {
    d3.select(this).attr("opacity", 1);
    tooltip
      .style("visibility", "visible")
      .html(`<strong>${d.label}</strong><br/>Value: ${d.value}`);
  })
  .on("mousemove", function(event) {
    tooltip
      .style("top", (event.pageY - 10) + "px")
      .style("left", (event.pageX + 10) + "px");
  })
  .on("mouseout", function() {
    d3.select(this).attr("opacity", 0.7);
    tooltip.style("visibility", "hidden");
  });
```

### Zoom e pan

```javascript
const zoom = d3.zoom()
  .scaleExtent([0.5, 10])
  .on("zoom", (event) => {
    g.attr("transform", event.transform);
  });

svg.call(zoom);
```

### Interações ao clicar

```javascript
circles
  .on("click", function(event, d) {
    // Trate clique (dispare evento, atualize estado da app, etc.)
    console.log("Clicked:", d);

    // Feedback visual
    d3.selectAll("circle").attr("fill", "steelblue");
    d3.select(this).attr("fill", "orange");

    // Opcional: dispare evento customizado para sua framework/app escutar
    // window.dispatchEvent(new CustomEvent('chartClick', { detail: d }));
  });
```

## Transições e animações

Adicione transições suaves a mudanças visuais:

```javascript
// Transição básica
circles
  .transition()
  .duration(750)
  .attr("r", 10);

// Transições encadeadas
circles
  .transition()
  .duration(500)
  .attr("fill", "orange")
  .transition()
  .duration(500)
  .attr("r", 15);

// Transições escalonadas
circles
  .transition()
  .delay((d, i) => i * 50)
  .duration(500)
  .attr("cy", d => yScale(d.value));

// Easing customizado
circles
  .transition()
  .duration(1000)
  .ease(d3.easeBounceOut)
  .attr("r", 10);
```

## Referência de escalas

### Escalas quantitativas

```javascript
// Escala linear
const xScale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

// Escala logarítmica (para dados exponenciais)
const logScale = d3.scaleLog()
  .domain([1, 1000])
  .range([0, 500]);

// Escala de potência
const powScale = d3.scalePow()
  .exponent(2)
  .domain([0, 100])
  .range([0, 500]);

// Escala de tempo
const timeScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2024, 0, 1)])
  .range([0, 500]);
```

### Escalas ordinais

```javascript
// Escala band (para gráficos de barras)
const bandScale = d3.scaleBand()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400])
  .padding(0.1);

// Escala point (para categorias de linhas/dispersão)
const pointScale = d3.scalePoint()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400]);

// Escala ordinal (para cores)
const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
```

### Escalas sequenciais

```javascript
// Escala de cores sequencial
const colourScale = d3.scaleSequential(d3.interpolateBlues)
  .domain([0, 100]);

// Escala de cores divergente
const divScale = d3.scaleDiverging(d3.interpolateRdBu)
  .domain([-10, 0, 10]);
```

## Boas práticas

### Preparação de dados

Sempre valide e prepare dados antes da visualização:

```javascript
// Filtre valores inválidos
const cleanData = data.filter(d => d.value != null && !isNaN(d.value));

// Ordene dados se a ordem importar
const sortedData = [...data].sort((a, b) => b.value - a.value);

// Analise datas
const parsedData = data.map(d => ({
  ...d,
  date: d3.timeParse("%Y-%m-%d")(d.date)
}));
```

### Otimização de performance

Para conjuntos de dados grandes (>1000 elementos):

```javascript
// Use canvas em vez de SVG para muitos elementos
// Use quadtree para detecção de colisão
// Simplifique caminhos com d3.line().curve(d3.curveStep)
// Implemente virtual scrolling para listas grandes
// Use requestAnimationFrame para animações customizadas
```

### Acessibilidade

Torne visualizações acessíveis:

```javascript
// Adicione labels ARIA
svg.attr("role", "img")
   .attr("aria-label", "Gráfico de barras mostrando receita trimestral");

// Adicione título e descrição
svg.append("title").text("Receita Trimestral 2024");
svg.append("desc").text("Gráfico de barras mostrando crescimento de receita em quatro trimestres");

// Garanta contraste de cor suficiente
// Forneça navegação por teclado para elementos interativos
// Inclua tabela de dados como alternativa
```

### Estilo

Use estilo consistente e profissional:

```javascript
// Defina paletas de cores antecipadamente
const colours = {
  primary: '#4A90E2',
  secondary: '#7B68EE',
  background: '#F5F7FA',
  text: '#333333',
  gridLines: '#E0E0E0'
};

// Aplique tipografia consistente
svg.selectAll("text")
  .style("font-family", "Inter, sans-serif")
  .style("font-size", "12px");

// Use linhas de grade sutis
g.selectAll(".tick line")
  .attr("stroke", colours.gridLines)
  .attr("stroke-dasharray", "2,2");
```

## Problemas comuns e soluções

**Problema**: Eixos não aparecem
- Garanta que escalas têm domínios válidos (verifique valores NaN)
- Verifique que o eixo foi anexado ao grupo correto
- Verifique que as translações de transform estão corretas

**Problema**: Transições não funcionam
- Chame `.transition()` antes de mudanças de atributo
- Garanta que elementos têm chaves únicas para vinculação de dados apropriada
- Verifique que dependências useEffect incluem todos dados em mudança

**Problema**: Dimensionamento responsivo não funciona
- Use ResizeObserver ou listener de resize de janela
- Atualize dimensões no state para acionador re-render
- Garanta que SVG tem atributos width/height ou viewBox

**Problema**: Problemas de performance
- Limite número de elementos DOM (considere canvas para >1000 itens)
- Debounce resize handlers
- Use `.join()` em vez de seleções enter/update/exit separadas
- Evite re-renders desnecessários verificando dependências

## Recursos

### references/
Contém materiais de referência detalhados:
- `d3-patterns.md` - Coleção abrangente de padrões de visualização e exemplos de código
- `scale-reference.md` - Guia completo de escalas d3 com exemplos
- `colour-schemes.md` - Esquemas de cores d3 e recomendações de paleta

### assets/

Contém templates boilerplate:

- `chart-template.js` - Template inicial para gráfico básico
- `interactive-template.js` - Template com tooltips, zoom e interações
- `sample-data.json` - Conjuntos de dados de exemplo para teste

Estes templates funcionam com JavaScript vanilla, React, Vue, Svelte ou qualquer outro ambiente JavaScript. Adapte-os conforme necessário para seu framework específico.

Para usar esses recursos, leia os arquivos relevantes quando orientação detalhada for necessária para tipos específicos de visualização ou padrões.