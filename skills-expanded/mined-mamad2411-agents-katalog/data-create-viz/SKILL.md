---
name: data-create-viz
description: Cria visualizações de dados de qualidade profissional com Python no tema Evolution (fundo escuro, acento #00FFA7, fonte Inter). Use quando precisar transformar resultados de query ou um DataFrame em um gráfico, selecionar o tipo de gráfico correto para uma tendência ou comparação, gerar um plot para relatório ou apresentação, ou precisar de um gráfico interativo com hover e zoom. Fontes: Stripe, Omie, Licensing, Evo CRM, ou dados colados/CSV.
argument-hint: "<fonte de dados> [tipo de gráfico] [instruções adicionais]"
---

# data-create-viz — Criar Visualizações de Dados

Cria visualizações de dados de qualidade profissional usando Python. Gera gráficos a partir de dados com boas práticas de clareza, precisão e design no tema Evolution.

## Uso

```
/data-create-viz <fonte de dados> [tipo de gráfico] [instruções adicionais]
```

## Fluxo de Trabalho

### 1. Entender a Requisição

Determinar:

- **Fonte de dados**: Resultados de query, dados colados, arquivo CSV/Excel, ou dados a serem consultados
- **Tipo de gráfico**: Explicitamente solicitado ou precisa ser recomendado
- **Propósito**: Exploração, apresentação, relatório, componente de dashboard
- **Audiência**: Time técnico, executivos, stakeholders externos

### 2. Obter os Dados

**Se fonte de dados do workspace (Stripe, Omie, Licensing, Evo CRM):**
1. Usar a skill correspondente para buscar os dados
2. Carregar os resultados em um pandas DataFrame
3. Limpar e preparar conforme necessário

**Se dados forem colados ou enviados como arquivo:**
1. Fazer parse dos dados em um pandas DataFrame
2. Limpar e preparar conforme necessário (conversões de tipo, tratamento de nulos)

**Se dados vierem de uma análise anterior na conversa:**
1. Referenciar os dados existentes

### 3. Selecionar o Tipo de Gráfico

Se o usuário não especificou um tipo de gráfico, recomendar um com base nos dados e na pergunta:

| Relacionamento dos Dados | Gráfico Recomendado |
|---|---|
| Tendência ao longo do tempo | Gráfico de linha |
| Comparação entre categorias | Gráfico de barras (horizontal se muitas categorias) |
| Composição parte-todo | Barras empilhadas ou área (evitar pizza a menos que <6 categorias) |
| Distribuição de valores | Histograma ou box plot |
| Correlação entre duas variáveis | Scatter plot |
| Comparação de duas variáveis ao longo do tempo | Linha de eixo duplo ou barras agrupadas |
| Dados geográficos | Mapa coroplético |
| Ranking | Gráfico de barras horizontal |
| Fluxo ou processo | Diagrama Sankey |
| Matriz de relacionamentos | Heatmap |

Explicar brevemente a recomendação se o usuário não especificou.

### 4. Gerar a Visualização

Escrever código Python usando uma destas bibliotecas com base na necessidade:

- **matplotlib + seaborn**: Melhor para gráficos estáticos de qualidade profissional. Escolha padrão.
- **plotly**: Melhor para gráficos interativos ou quando o usuário solicitar interatividade.

**Tema Evolution Dark — Configuração Base:**

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np

# ── Tema Evolution Dark ──────────────────────────────────────────
EVO_BG       = '#0A0A0A'
EVO_SURFACE  = '#1A1A1A'
EVO_ACCENT   = '#00FFA7'
EVO_TEXT     = '#F0F0F0'
EVO_MUTED    = '#666666'
EVO_BORDER   = '#2A2A2A'

EVO_PALETTE = [
    '#00FFA7',  # Acento principal Evolution
    '#4C9FE8',  # Azul
    '#FFB547',  # Âmbar
    '#FF6B6B',  # Vermelho
    '#A78BFA',  # Roxo
    '#34D399',  # Verde esmeralda
    '#FB923C',  # Laranja
]

# Configurar estilo global
plt.rcParams.update({
    'figure.facecolor': EVO_BG,
    'axes.facecolor': EVO_SURFACE,
    'axes.edgecolor': EVO_BORDER,
    'axes.labelcolor': EVO_MUTED,
    'axes.titlecolor': EVO_TEXT,
    'xtick.color': EVO_MUTED,
    'ytick.color': EVO_MUTED,
    'text.color': EVO_TEXT,
    'grid.color': '#222222',
    'grid.alpha': 0.8,
    'legend.facecolor': '#1A1A1A',
    'legend.edgecolor': EVO_BORDER,
    'legend.labelcolor': EVO_TEXT,
    'font.family': 'DejaVu Sans',  # Fallback para Inter
    'figure.dpi': 150,
})

def apply_evo_style(ax):
    """Aplicar estilo Evolution a um eixo."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(EVO_BORDER)
    ax.spines['bottom'].set_color(EVO_BORDER)
    ax.grid(True, alpha=0.3, color='#2A2A2A', linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
```

**Requisitos de código:**

```python
# Criar figura com tamanho apropriado
fig, ax = plt.subplots(figsize=(12, 6), facecolor=EVO_BG)

# [código específico do gráfico]

# Sempre incluir:
ax.set_title('Título Claro e Descritivo', fontsize=14, fontweight='bold',
             color=EVO_TEXT, pad=16)
ax.set_xlabel('Label do Eixo X', fontsize=11, color=EVO_MUTED)
ax.set_ylabel('Label do Eixo Y', fontsize=11, color=EVO_MUTED)

# Aplicar estilo Evolution
apply_evo_style(ax)

# Formatar números adequadamente
# - Percentuais: '45,2%' não '0,452'
# - Moeda BRL: 'R$ 1,2M' não '1200000'
# - Moeda USD: '$1.2M' não '1200000'
# - Números grandes: '2,3K' ou '1,5M' não '2300' ou '1500000'

plt.tight_layout(pad=2.0)
plt.savefig('nome_do_grafico.png', dpi=150, bbox_inches='tight',
            facecolor=EVO_BG)
plt.show()
```

### 5. Aplicar Boas Práticas de Design

**Cores:**
- Usar a paleta Evolution consistente e amigável para daltônicos
- Usar cor significativamente (não decorativamente)
- Destacar o ponto de dado ou tendência principal com #00FFA7 (acento Evolution)
- Usar cinza (#444444) para dados de referência menos importantes

**Tipografia:**
- Título descritivo que enuncia o insight, não apenas a métrica (ex: "MRR cresceu 23% YoY" não "MRR por Mês")
- Labels de eixo legíveis (não rotacionadas 90 graus se possível)
- Labels de dados nos pontos-chave quando adicionam clareza

**Layout:**
- Espaçamento e margens apropriados
- Posicionamento de legenda que não obscurece os dados
- Categorias ordenadas por valor (não alfabeticamente) a menos que haja uma ordem natural

**Precisão:**
- Eixo Y começa em zero para gráficos de barras
- Sem quebras de eixo enganosas sem notação clara
- Escalas consistentes ao comparar painéis
- Precisão apropriada (não mostrar 10 casas decimais)

### 6. Salvar e Apresentar

1. Salvar o gráfico como arquivo PNG com nome descritivo
2. Exibir o gráfico para o usuário
3. Fornecer o código usado para que possam modificar
4. Sugerir variações (tipo de gráfico diferente, agrupamento diferente, intervalo de tempo ampliado)

---

## Exemplos de Código por Tipo de Gráfico

### Gráfico de Linha (Tendência Temporal)

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

fig, ax = plt.subplots(figsize=(12, 6), facecolor=EVO_BG)

# Plotar linhas com estilo Evolution
for i, (col, label) in enumerate(series):
    ax.plot(df['data'], df[col],
            color=EVO_PALETTE[i],
            linewidth=2.5,
            label=label,
            marker='o', markersize=4,
            markerfacecolor=EVO_BG,
            markeredgecolor=EVO_PALETTE[i],
            markeredgewidth=1.5)

    # Área sob a linha (sutil)
    ax.fill_between(df['data'], df[col],
                    alpha=0.08, color=EVO_PALETTE[i])

# Destacar o último ponto
last_val = df[col].iloc[-1]
ax.annotate(f'R$ {last_val/1e3:.1f}K',
            xy=(df['data'].iloc[-1], last_val),
            xytext=(8, 0), textcoords='offset points',
            color=EVO_ACCENT, fontsize=10, fontweight='bold')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
plt.xticks(rotation=0)
apply_evo_style(ax)
ax.set_title('Tendência de MRR — Últimos 12 Meses', fontsize=14,
             fontweight='bold', color=EVO_TEXT, pad=16)
ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig('mrr_trend.png', dpi=150, bbox_inches='tight', facecolor=EVO_BG)
```

### Gráfico de Barras (Comparação de Categorias)

```python
fig, ax = plt.subplots(figsize=(10, 6), facecolor=EVO_BG)

# Barras horizontais para muitas categorias
categorias = df['plano'].values
valores = df['total'].values

# Ordenar por valor
idx = np.argsort(valores)
categorias, valores = categorias[idx], valores[idx]

# Colorir a maior barra com acento Evolution
cores = [EVO_ACCENT if v == valores.max() else '#2A4A3A' for v in valores]

bars = ax.barh(categorias, valores, color=cores,
               edgecolor='none', height=0.6)

# Adicionar labels de valor
for bar, val in zip(bars, valores):
    ax.text(val + valores.max() * 0.01, bar.get_y() + bar.get_height()/2,
            f'{val:,.0f}', va='center', color=EVO_TEXT, fontsize=10)

apply_evo_style(ax)
ax.set_xlabel('Total', color=EVO_MUTED)
ax.set_title('Instâncias por Versão', fontsize=14, fontweight='bold',
             color=EVO_TEXT, pad=16)
ax.grid(True, axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('instancias_versao.png', dpi=150, bbox_inches='tight', facecolor=EVO_BG)
```

### Heatmap (Matriz de Correlação ou Volume)

```python
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 8), facecolor=EVO_BG)

# Heatmap com tema escuro
cmap = sns.diverging_palette(150, 0, s=80, l=40,
                              center='light', as_cmap=True)

sns.heatmap(pivot_df,
            ax=ax,
            cmap='RdYlGn',
            annot=True, fmt='.0f',
            linewidths=1, linecolor=EVO_BG,
            cbar_kws={'shrink': 0.8})

ax.set_facecolor(EVO_SURFACE)
ax.tick_params(colors=EVO_MUTED)
ax.set_title('Volume por Dia e Hora', fontsize=14, fontweight='bold',
             color=EVO_TEXT, pad=16)

plt.tight_layout()
plt.savefig('heatmap_volume.png', dpi=150, bbox_inches='tight', facecolor=EVO_BG)
```

### Gráfico de Eixo Duplo (Volume + Taxa)

```python
fig, ax1 = plt.subplots(figsize=(12, 6), facecolor=EVO_BG)
ax2 = ax1.twinx()

# Barras para volume (eixo esquerdo)
ax1.bar(df['mes'], df['instancias'], color='#2A4A3A',
        alpha=0.8, label='Novas Instâncias')
ax1.set_ylabel('Novas Instâncias', color=EVO_MUTED)
ax1.tick_params(axis='y', colors=EVO_MUTED)

# Linha para taxa (eixo direito)
ax2.plot(df['mes'], df['churn_pct'], color=EVO_ACCENT,
         linewidth=2.5, marker='o', markersize=5,
         markerfacecolor=EVO_BG, markeredgecolor=EVO_ACCENT,
         label='Churn (%)', zorder=5)
ax2.set_ylabel('Churn (%)', color=EVO_ACCENT)
ax2.tick_params(axis='y', colors=EVO_ACCENT)

ax1.set_facecolor(EVO_SURFACE)
apply_evo_style(ax1)

# Legenda combinada
handles = [
    mpatches.Patch(color='#2A4A3A', label='Novas Instâncias'),
    plt.Line2D([0], [0], color=EVO_ACCENT, linewidth=2, label='Churn (%)'),
]
ax1.legend(handles=handles, loc='upper left',
           facecolor='#1A1A1A', edgecolor=EVO_BORDER)

ax1.set_title('Crescimento vs Churn', fontsize=14, fontweight='bold',
              color=EVO_TEXT, pad=16)

plt.tight_layout()
plt.savefig('crescimento_churn.png', dpi=150, bbox_inches='tight', facecolor=EVO_BG)
```

### Histograma (Distribuição)

```python
fig, ax = plt.subplots(figsize=(10, 6), facecolor=EVO_BG)

ax.hist(df['valor'], bins=30, color=EVO_ACCENT, alpha=0.8,
        edgecolor=EVO_BG, linewidth=0.5)

# Linha de mediana e média
mediana = df['valor'].median()
media = df['valor'].mean()
ax.axvline(mediana, color='#FFB547', linewidth=2, linestyle='--',
           label=f'Mediana: R$ {mediana:,.0f}')
ax.axvline(media, color='#FF6B6B', linewidth=2, linestyle=':',
           label=f'Média: R$ {media:,.0f}')

apply_evo_style(ax)
ax.legend(facecolor='#1A1A1A', edgecolor=EVO_BORDER)
ax.set_xlabel('Valor (R$)', color=EVO_MUTED)
ax.set_ylabel('Frequência', color=EVO_MUTED)
ax.set_title('Distribuição de MRR por Cliente', fontsize=14,
             fontweight='bold', color=EVO_TEXT, pad=16)

plt.tight_layout()
plt.savefig('distribuicao_mrr.png', dpi=150, bbox_inches='tight', facecolor=EVO_BG)
```

### Gráfico Interativo com Plotly (tema Evolution)

```python
import plotly.graph_objects as go
import plotly.express as px

# Layout tema Evolution para Plotly
evo_layout = dict(
    paper_bgcolor='#0A0A0A',
    plot_bgcolor='#1A1A1A',
    font=dict(color='#F0F0F0', family='Inter, sans-serif'),
    xaxis=dict(gridcolor='#2A2A2A', linecolor='#2A2A2A'),
    yaxis=dict(gridcolor='#2A2A2A', linecolor='#2A2A2A'),
    legend=dict(bgcolor='#1A1A1A', bordercolor='#2A2A2A'),
    colorway=EVO_PALETTE,
)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['data'], y=df['mrr'],
    mode='lines+markers',
    name='MRR',
    line=dict(color='#00FFA7', width=2.5),
    marker=dict(color='#0A0A0A', size=6, line=dict(color='#00FFA7', width=2)),
    fill='tozeroy',
    fillcolor='rgba(0, 255, 167, 0.08)',
    hovertemplate='<b>%{x}</b><br>MRR: R$ %{y:,.0f}<extra></extra>'
))

fig.update_layout(
    title=dict(text='Tendência de MRR', font=dict(size=16, color='#F0F0F0')),
    **evo_layout
)

fig.write_html('mrr_interativo.html')
fig.show()
```

## Exemplos

```
/data-create-viz Mostrar MRR mensal dos últimos 12 meses como gráfico de linha com a tendência destacada
```

```
/data-create-viz Aqui estão nossos dados de instâncias por país [cola os dados]. Criar gráfico de barras horizontal ranking por total.
```

```
/data-create-viz Consultar os dados de churn do Stripe e criar um heatmap de taxa de churn por cohort (mês de cadastro vs. mês de churn)
```

```
/data-create-viz Dados do Licensing — criar grid 2x2 mostrando: distribuição por versão, tendência de instâncias ativas, mapa de países, e crescimento semanal
```

## Dicas

- Se quiser gráficos interativos (hover, zoom, filtro), mencionar "interativo" e será usado Plotly
- Especificar "apresentação" se precisar de fontes maiores e maior contraste
- Pode solicitar múltiplos gráficos de uma vez (ex: "criar um grid 2x2 de gráficos mostrando...")
- Gráficos são salvos no diretório atual como arquivos PNG
- O tema Evolution dark é o padrão — compatível com dashboards e relatórios internos
- Para embed em dashboard HTML, usar `data-build-dashboard` em vez desta skill
