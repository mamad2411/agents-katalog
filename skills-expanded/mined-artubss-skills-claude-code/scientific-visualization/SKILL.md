---
name: scientific-visualization
description: "Crie figuras para publicação com matplotlib/seaborn/plotly. Layouts multi-painel, barras de erro, marcadores de significância, seguro para daltônicos, exporte PDF/EPS/TIFF para gráficos prontos para periódicos."
---

# Visualização Científica

## Visão Geral

A visualização científica transforma dados em figuras claras e precisas para publicação. Crie gráficos prontos para periódicos com layouts multi-painel, barras de erro, marcadores de significância e paletas seguras para daltônicos. Exporte como PDF/EPS/TIFF usando matplotlib, seaborn e plotly para manuscritos.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Criar gráficos ou visualizações para manuscritos científicos
- Preparar figuras para submissão em periódico (Nature, Science, Cell, PLOS, etc.)
- Garantir que figuras sejam amigáveis para daltônicos e acessíveis
- Fazer figuras multi-painel com estilo consistente
- Exportar figuras em resolução e formato corretos
- Seguir diretrizes específicas de publicação
- Melhorar figuras existentes para atender padrões de publicação
- Criar figuras que funcionem tanto em cor quanto em escala de cinza

## Guia de Início Rápido

### Figura de Qualidade para Publicação Básica

```python
import matplotlib.pyplot as plt
import numpy as np

# Aplicar estilo de publicação (de scripts/style_presets.py)
from style_presets import apply_publication_style
apply_publication_style('default')

# Criar figura com tamanho apropriado (coluna única = 3,5 polegadas)
fig, ax = plt.subplots(figsize=(3.5, 2.5))

# Plotar dados
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# Rotulagem apropriada com unidades
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Amplitude (mV)')
ax.legend(frameon=False)

# Remover espinhas desnecessárias
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Salvar em formatos de publicação (de scripts/figure_export.py)
from figure_export import save_publication_figure
save_publication_figure(fig, 'figure1', formats=['pdf', 'png'], dpi=300)
```

### Usando Estilos Pré-configurados

Aplique estilos específicos de periódicos usando os arquivos de estilo matplotlib em `assets/`:

```python
import matplotlib.pyplot as plt

# Opção 1: Usar arquivo de estilo diretamente
plt.style.use('assets/nature.mplstyle')

# Opção 2: Usar helper style_presets.py
from style_presets import configure_for_journal
configure_for_journal('nature', figure_width='single')

# Agora crie figuras - elas corresponderão automaticamente às especificações da Nature
fig, ax = plt.subplots()
# ... seu código de plotagem ...
```

### Início Rápido com Seaborn

Para gráficos estatísticos, use seaborn com estilo de publicação:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from style_presets import apply_publication_style

# Aplicar estilo de publicação
apply_publication_style('default')
sns.set_theme(style='ticks', context='paper', font_scale=1.1)
sns.set_palette('colorblind')

# Criar figura de comparação estatística
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.boxplot(data=df, x='treatment', y='response', 
            order=['Control', 'Low', 'High'], palette='Set2', ax=ax)
sns.stripplot(data=df, x='treatment', y='response',
              order=['Control', 'Low', 'High'], 
              color='black', alpha=0.3, size=3, ax=ax)
ax.set_ylabel('Response (μM)')
sns.despine()

# Salvar figura
from figure_export import save_publication_figure
save_publication_figure(fig, 'treatment_comparison', formats=['pdf', 'png'], dpi=300)
```

## Princípios Centrais e Melhores Práticas

### 1. Resolução e Formato de Arquivo

**Requisitos críticos** (detalhados em `references/publication_guidelines.md`):
- **Imagens raster** (fotos, microscopia): 300-600 DPI
- **Arte linear** (gráficos, plotagens): 600-1200 DPI ou formato vetorial
- **Formatos vetoriais** (preferidos): PDF, EPS, SVG
- **Formatos raster**: TIFF, PNG (nunca JPEG para dados científicos)

**Implementação:**
```python
# Usar o script figure_export.py para configurações corretas
from figure_export import save_publication_figure

# Salva em múltiplos formatos com DPI apropriado
save_publication_figure(fig, 'myfigure', formats=['pdf', 'png'], dpi=300)

# Ou salvar para requisitos específicos de periódico
from figure_export import save_for_journal
save_for_journal(fig, 'figure1', journal='nature', figure_type='combination')
```

### 2. Seleção de Cores - Acessibilidade para Daltônicos

**Use sempre paletas amigáveis para daltônicos** (detalhadas em `references/color_palettes.md`):

**Recomendado: Paleta Okabe-Ito** (distinguível por todos os tipos de daltonismo):
```python
# Opção 1: Usar assets/color_palettes.py
from color_palettes import OKABE_ITO_LIST, apply_palette
apply_palette('okabe_ito')

# Opção 2: Especificação manual
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=okabe_ito)
```

**Para mapas de calor/dados contínuos:**
- Use mapas de cores perceptualmente uniformes: `viridis`, `plasma`, `cividis`
- Evite mapas divergentes vermelho-verde (use `PuOr`, `RdBu`, `BrBG` em vez disso)
- Nunca use mapas de cores `jet` ou `rainbow`

**Sempre teste figuras em escala de cinza** para garantir interpretabilidade.

### 3. Tipografia e Texto

**Diretrizes de fonte** (detalhadas em `references/publication_guidelines.md`):
- Fontes sans-serif: Arial, Helvetica, Calibri
- Tamanhos mínimos no **tamanho de impressão final**:
  - Rótulos de eixo: 7-9 pt
  - Rótulos de marcas: 6-8 pt
  - Rótulos de painel: 8-12 pt (negrito)
- Caso sentença para rótulos: "Time (hours)" e não "TIME (HOURS)"
- Sempre incluir unidades entre parênteses

**Implementação:**
```python
# Definir fontes globalmente
import matplotlib as mpl
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.labelsize'] = 9
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7
```

### 4. Dimensões de Figura

**Larguras específicas de periódicos** (detalhadas em `references/journal_requirements.md`):
- **Nature**: Coluna única 89 mm, dupla 183 mm
- **Science**: Coluna única 55 mm, dupla 175 mm
- **Cell**: Coluna única 85 mm, dupla 178 mm

**Verificar conformidade de tamanho de figura:**
```python
from figure_export import check_figure_size

fig = plt.figure(figsize=(3.5, 3))  # 89 mm para Nature
check_figure_size(fig, journal='nature')
```

### 5. Figuras Multi-Painel

**Melhores práticas:**
- Rotular painéis com letras em negrito: **A**, **B**, **C** (maiúsculas para a maioria dos periódicos, minúsculas para Nature)
- Manter estilo consistente em todos os painéis
- Alinhar painéis nas bordas quando possível
- Usar espaço em branco adequado entre painéis

**Implementação de exemplo** (veja `references/matplotlib_examples.md` para código completo):
```python
from string import ascii_uppercase

fig = plt.figure(figsize=(7, 4))
gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.4)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
# ... criar outros painéis ...

# Adicionar rótulos de painel
for i, ax in enumerate([ax1, ax2, ...]):
    ax.text(-0.15, 1.05, ascii_uppercase[i], transform=ax.transAxes,
            fontsize=10, fontweight='bold', va='top')
```

## Tarefas Comuns

### Tarefa 1: Criar um Gráfico de Linha Pronto para Publicação

Veja `references/matplotlib_examples.md` Exemplo 1 para código completo.

**Passos principais:**
1. Aplicar estilo de publicação
2. Definir tamanho de figura apropriado para periódico alvo
3. Usar cores amigáveis para daltônicos
4. Adicionar barras de erro com representação correta (SEM, SD ou IC)
5. Rotular eixos com unidades
6. Remover espinhas desnecessárias
7. Salvar em formato vetorial

**Usando seaborn para intervalos de confiança automáticos:**
```python
import seaborn as sns
fig, ax = plt.subplots(figsize=(5, 3))
sns.lineplot(data=timeseries, x='time', y='measurement',
             hue='treatment', errorbar=('ci', 95), 
             markers=True, ax=ax)
ax.set_xlabel('Time (hours)')
ax.set_ylabel('Measurement (AU)')
sns.despine()
```

### Tarefa 2: Criar uma Figura Multi-Painel

Veja `references/matplotlib_examples.md` Exemplo 2 para código completo.

**Passos principais:**
1. Usar `GridSpec` para layout flexível
2. Garantir estilo consistente entre painéis
3. Adicionar rótulos de painel em negrito (A, B, C, etc.)
4. Alinhar painéis relacionados
5. Verificar se todo texto é legível no tamanho final

### Tarefa 3: Criar um Mapa de Calor com Mapa de Cores Apropriado

Veja `references/matplotlib_examples.md` Exemplo 4 para código completo.

**Passos principais:**
1. Usar mapa de cores perceptualmente uniforme (`viridis`, `plasma`, `cividis`)
2. Incluir barra de cores rotulada
3. Para dados divergentes, usar mapa divergente seguro para daltônicos (`RdBu_r`, `PuOr`)
4. Definir valor central apropriado para mapas divergentes
5. Testar aparência em escala de cinza

**Usando seaborn para matrizes de correlação:**
```python
import seaborn as sns
fig, ax = plt.subplots(figsize=(5, 4))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, square=True,
            linewidths=1, cbar_kws={'shrink': 0.8}, ax=ax)
```

### Tarefa 4: Preparar Figura para Periódico Específico

**Fluxo de trabalho:**
1. Verificar requisitos de periódico: `references/journal_requirements.md`
2. Configurar matplotlib para periódico:
   ```python
   from style_presets import configure_for_journal
   configure_for_journal('nature', figure_width='single')
   ```
3. Criar figura (dimensionará automaticamente corretamente)
4. Exportar com especificações de periódico:
   ```python
   from figure_export import save_for_journal
   save_for_journal(fig, 'figure1', journal='nature', figure_type='line_art')
   ```

### Tarefa 5: Corrigir uma Figura Existente para Atender Padrões de Publicação

**Abordagem de checklist** (checklist completo em `references/publication_guidelines.md`):

1. **Verificar resolução**: Verificar se DPI atende aos requisitos do periódico
2. **Verificar formato de arquivo**: Usar vetorial para gráficos, TIFF/PNG para imagens
3. **Verificar cores**: Garantir amigável para daltônicos
4. **Verificar fontes**: Mínimo 6-7 pt no tamanho final, sans-serif
5. **Verificar rótulos**: Todos os eixos rotulados com unidades
6. **Verificar tamanho**: Corresponder à largura da coluna do periódico
7. **Testar escala de cinza**: Figura interpretável sem cor
8. **Remover poluição visual**: Sem grades desnecessárias, efeitos 3D, sombras

### Tarefa 6: Criar Visualizações Seguras para Daltônicos

**Estratégia:**
1. Usar paletas aprovadas de `assets/color_palettes.py`
2. Adicionar codificação redundante (estilos de linha, marcadores, padrões)
3. Testar com simulador de daltonismo
4. Garantir compatibilidade em escala de cinza

**Exemplo:**
```python
from color_palettes import apply_palette
import matplotlib.pyplot as plt

apply_palette('okabe_ito')

# Adicionar codificação redundante além de cor
line_styles = ['-', '--', '-.', ':']
markers = ['o', 's', '^', 'v']

for i, (data, label) in enumerate(datasets):
    plt.plot(x, data, linestyle=line_styles[i % 4],
             marker=markers[i % 4], label=label)
```

## Rigor Estatístico

**Sempre incluir:**
- Barras de erro (SD, SEM ou IC - especifique qual na legenda)
- Tamanho da amostra (n) na figura ou legenda
- Marcadores de significância estatística (*, **, ***)
- Pontos de dados individuais quando possível (não apenas estatísticas resumidas)

**Exemplo com estatística:**
```python
# Mostrar pontos individuais com estatísticas resumidas
ax.scatter(x_jittered, individual_points, alpha=0.4, s=8)
ax.errorbar(x, means, yerr=sems, fmt='o', capsize=3)

# Marcar significância
ax.text(1.5, max_y * 1.1, '***', ha='center', fontsize=8)
```

## Trabalhando com Diferentes Bibliotecas de Plotagem

### Matplotlib
- Maior controle sobre detalhes de publicação
- Melhor para figuras multi-painel complexas
- Usar arquivos de estilo fornecidos para formatação consistente
- Veja `references/matplotlib_examples.md` para exemplos extensivos

### Seaborn

Seaborn fornece uma interface de alto nível e orientada a dados para gráficos estatísticos, construída sobre matplotlib. Excela na criação de visualizações estatísticas prontas para publicação com código mínimo, mantendo compatibilidade total com personalização matplotlib.

**Vantagens principais para visualização científica:**
- Estimativa estatística automática e intervalos de confiança
- Suporte integrado para figuras multi-painel (faceting)
- Paletas amigáveis para daltônicos por padrão
- API orientada a dados usando pandas DataFrames
- Mapeamento semântico de variáveis para propriedades visuais

#### Início Rápido com Estilo de Publicação

Sempre aplique estilos de publicação matplotlib primeiro, depois configure seaborn:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from style_presets import apply_publication_style

# Aplicar estilo de publicação
apply_publication_style('default')

# Configurar seaborn para publicação
sns.set_theme(style='ticks', context='paper', font_scale=1.1)
sns.set_palette('colorblind')  # Usar paleta segura para daltônicos

# Criar figura
fig, ax = plt.subplots(figsize=(3.5, 2.5))
sns.scatterplot(data=df, x='time', y='response', 
                hue='treatment', style='condition', ax=ax)
sns.despine()  # Remover espinhas superior e direita
```

#### Tipos de Gráfico Comuns para Publicações

**Comparações estatísticas:**
```python
# Gráfico de caixa com pontos individuais para transparência
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.boxplot(data=df, x='treatment', y='response', 
            order=['Control', 'Low', 'High'], palette='Set2', ax=ax)
sns.stripplot(data=df, x='treatment', y='response',
              order=['Control', 'Low', 'High'], 
              color='black', alpha=0.3, size=3, ax=ax)
ax.set_ylabel('Response (μM)')
sns.despine()
```

**Análise de distribuição:**
```python
# Gráfico de violino com comparação dividida
fig, ax = plt.subplots(figsize=(4, 3))
sns.violinplot(data=df, x='timepoint', y='expression',
               hue='treatment', split=True, inner='quartile', ax=ax)
ax.set_ylabel('Gene Expression (AU)')
sns.despine()
```

**Matrizes de correlação:**
```python
# Mapa de calor com mapa de cores apropriado e anotações
fig, ax = plt.subplots(figsize=(5, 4))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))  # Mostrar apenas triângulo inferior
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, square=True,
            linewidths=1, cbar_kws={'shrink': 0.8}, ax=ax)
plt.tight_layout()
```

**Série temporal com faixas de confiança:**
```python
# Gráfico de linha com cálculo automático de IC
fig, ax = plt.subplots(figsize=(5, 3))
sns.lineplot(data=timeseries, x='time', y='measurement',
             hue='treatment', style='replicate',
             errorbar=('ci', 95), markers=True, dashes=False, ax=ax)
ax.set_xlabel('Time (hours)')
ax.set_ylabel('Measurement (AU)')
sns.despine()
```

#### Figuras Multi-Painel com Seaborn

**Usando FacetGrid para faceting automático:**
```python
# Criar gráfico em facetas
g = sns.relplot(data=df, x='dose', y='response',
                hue='treatment', col='cell_line', row='timepoint',
                kind='line', height=2.5, aspect=1.2,
                errorbar=('ci', 95), markers=True)
g.set_axis_labels('Dose (μM)', 'Response (AU)')
g.set_titles('{row_name} | {col_name}')
sns.despine()

# Salvar com DPI correto
from figure_export import save_publication_figure
save_publication_figure(g.figure, 'figure_facets', 
                       formats=['pdf', 'png'], dpi=300)
```

**Combinando seaborn com subplots matplotlib:**
```python
# Criar layout multi-painel personalizado
fig, axes = plt.subplots(2, 2, figsize=(7, 6))

# Painel A: Dispersão com regressão
sns.regplot(data=df, x='predictor', y='response', ax=axes[0, 0])
axes[0, 0].text(-0.15, 1.05, 'A', transform=axes[0, 0].transAxes,
                fontsize=10, fontweight='bold')

# Painel B: Comparação de distribuição
sns.violinplot(data=df, x='group', y='value', ax=axes[0, 1])
axes[0, 1].text(-0.15, 1.05, 'B', transform=axes[0, 1].transAxes,
                fontsize=10, fontweight='bold')

# Painel C: Mapa de calor
sns.heatmap(correlation_data, cmap='viridis', ax=axes[1, 0])
axes[1, 0].text(-0.15, 1.05, 'C', transform=axes[1, 0].transAxes,
                fontsize=10, fontweight='bold')

# Painel D: Série temporal
sns.lineplot(data=timeseries, x='time', y='signal', 
             hue='condition', ax=axes[1, 1])
axes[1, 1].text(-0.15, 1.05, 'D', transform=axes[1, 1].transAxes,
                fontsize=10, fontweight='bold')

plt.tight_layout()
sns.despine()
```

#### Paletas de Cores para Publicações

Seaborn inclui várias paletas seguras para daltônicos:

```python
# Usar paleta colorblind integrada (recomendada)
sns.set_palette('colorblind')

# Ou especificar cores personalizadas seguras para daltônicos (Okabe-Ito)
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
sns.set_palette(okabe_ito)

# Para mapas de calor e dados contínuos
sns.heatmap(data, cmap='viridis')  # Perceptualmente uniforme
sns.heatmap(corr, cmap='RdBu_r', center=0)  # Divergente, centralizado
```

#### Escolhendo Entre Funções em Nível de Axes e Nível de Figure

**Funções em nível de axes** (ex: `scatterplot`, `boxplot`, `heatmap`):
- Use ao construir layouts multi-painel personalizados
- Aceitam parâmetro `ax=` para colocação precisa
- Integração melhor com subplots matplotlib
- Mais controle sobre composição de figura

```python
fig, ax = plt.subplots(figsize=(3.5, 2.5))
sns.scatterplot(data=df, x='x', y='y', hue='group', ax=ax)
```

**Funções em nível de figure** (ex: `relplot`, `catplot`, `displot`):
- Use para faceting automático por variáveis categóricas
- Criam figuras completas com estilo consistente
- Ótimas para análise exploratória
- Use `height` e `aspect` para dimensionamento

```python
g = sns.relplot(data=df, x='x', y='y', col='category', kind='scatter')
```

#### Rigor Estatístico com Seaborn

Seaborn calcula e exibe automaticamente incerteza:

```python
# Gráfico de linha: mostra média ± IC 95% por padrão
sns.lineplot(data=df, x='time', y='value', hue='treatment',
             errorbar=('ci', 95))  # Pode mudar para 'sd', 'se', etc.

# Gráfico de barras: mostra média com IC bootstrapped
sns.barplot(data=df, x='treatment', y='response',
            errorbar=('ci', 95), capsize=0.1)

# Sempre especifique tipo de erro na legenda da figura:
# "Error bars represent 95% confidence intervals"
```

#### Melhores Práticas para Figuras Seaborn Prontas para Publicação

1. **Sempre defina tema de publicação primeiro:**
   ```python
   sns.set_theme(style='ticks', context='paper', font_scale=1.1)
   ```

2. **Use paletas seguras para daltônicos:**
   ```python
   sns.set_palette('colorblind')
   ```

3. **Remova elementos desnecessários:**
   ```python
   sns.despine()  # Remover espinhas superior e direita
   ```

4. **Controle tamanho de figura apropriadamente:**
   ```python
   # Nível de axes: usar figsize de matplotlib
   fig, ax = plt.subplots(figsize=(3.5, 2.5))
   
   # Nível de figure: usar height e aspect
   g = sns.relplot(..., height=3, aspect=1.2)
   ```

5. **Mostre pontos de dados individuais quando possível:**
   ```python
   sns.boxplot(...)  # Estatísticas resumidas
   sns.stripplot(..., alpha=0.3)  # Pontos individuais
   ```

6. **Inclua rótulos apropriados com unidades:**
   ```python
   ax.set_xlabel('Time (hours)')
   ax.set_ylabel('Expression (AU)')
   ```

7. **Exporte em resolução correta:**
   ```python
   from figure_export import save_publication_figure
   save_publication_figure(fig, 'figure_name', 
                          formats=['pdf', 'png'], dpi=300)
   ```

#### Técnicas Avançadas de Seaborn

**Relacionamentos múltiplos para análise exploratória:**
```python
# Visão geral rápida de todos os relacionamentos
g = sns.pairplot(data=df, hue='condition', 
                 vars=['gene1', 'gene2', 'gene3'],
                 corner=True, diag_kind='kde', height=2)
```

**Mapa de calor com agrupamento hierárquico:**
```python
# Agrupar amostras e características
g = sns.clustermap(expression_data, method='ward', 
                   metric='euclidean', z_score=0,
                   cmap='RdBu_r', center=0, 
                   figsize=(10, 8), 
                   row_colors=condition_colors,
                   cbar_kws={'label': 'Z-score'})
```

**Distribuições conjuntas com marginais:**
```python
# Distribuição bivariada com contexto
g = sns.jointplot(data=df, x='gene1', y='gene2',
                  hue='treatment', kind='scatter',
                  height=6, ratio=4, marginal_kws={'kde': True})
```

#### Problemas Comuns de Seaborn e Soluções

**Problema: Legenda fora da área do gráfico**
```python
g = sns.relplot(...)
g._legend.set_bbox_to_anchor((0.9, 0.5))
```

**Problema: Rótulos sobrepostos**
```python
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
```

**Problema: Texto muito pequeno no tamanho final**
```python
sns.set_context('paper', font_scale=1.2)  # Aumentar se necessário
```

#### Recursos Adicionais

Para informações mais detalhadas sobre seaborn, veja:
- `scientific-packages/seaborn/SKILL.md` - Documentação seaborn abrangente
- `scientific-packages/seaborn/references/examples.md` - Casos de uso práticos
- `scientific-packages/seaborn/references/function_reference.md` - Referência de API completa
- `scientific-packages/seaborn/references/objects_interface.md` - API declarativa moderna

### Plotly
- Figuras interativas para exploração
- Exportar imagens estáticas para publicação
- Configurar para qualidade de publicação:
```python
fig.update_layout(
    font=dict(family='Arial, sans-serif', size=10),
    plot_bgcolor='white',
    # ... veja matplotlib_examples.md Exemplo 8
)
fig.write_image('figure.png', scale=3)  # scale=3 fornece ~300 DPI
```

## Recursos

### Diretório de Referências

**Carregue estes conforme necessário para informações detalhadas:**

- **`publication_guidelines.md`**: Melhores práticas abrangentes
  - Requisitos de resolução e formato de arquivo
  - Diretrizes de tipografia
  - Regras de layout e composição
  - Requisitos de rigor estatístico
  - Checklist de publicação completo

- **`color_palettes.md`**: Guia de uso de cores
  - Especificações de paleta segura para daltônicos com valores RGB
  - Recomendações de mapa de cores sequencial e divergente
  - Procedimentos de teste para acessibilidade
  - Paletas específicas de domínio (genômica, microscopia)

- **`journal_requirements.md`**: Especificações específicas de periódico
  - Requisitos técnicos por editora
  - Especificações de formato de arquivo e DPI
  -