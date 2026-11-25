---
name: matplotlib
description: "Biblioteca fundamental de visualização. Crie gráficos de linha, dispersão, barras, histogramas, mapas de calor, 3D, subplots, exporte PNG/PDF/SVG, para visualização científica e figuras para publicação."
---

# Matplotlib

## Visão Geral

Matplotlib é a biblioteca de visualização fundamental do Python para criar gráficos estáticos, animados e interativos. Esta habilidade fornece orientação sobre o uso eficaz do matplotlib, abrangendo tanto a interface pyplot (estilo MATLAB) quanto a API orientada a objetos (Figure/Axes), juntamente com melhores práticas para criar visualizações com qualidade de publicação.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Criar qualquer tipo de gráfico ou chart (linha, dispersão, barra, histograma, mapa de calor, contorno, etc.)
- Gerar visualizações científicas ou estatísticas
- Personalizar a aparência do gráfico (cores, estilos, rótulos, legendas)
- Criar figuras multi-painel com subplots
- Exportar visualizações para vários formatos (PNG, PDF, SVG, etc.)
- Construir gráficos interativos ou animações
- Trabalhar com visualizações 3D
- Integrar gráficos em notebooks Jupyter ou aplicações GUI

## Conceitos Fundamentais

### A Hierarquia do Matplotlib

Matplotlib usa uma estrutura hierárquica de objetos:

1. **Figure** - O contêiner de nível superior para todos os elementos do gráfico
2. **Axes** - A área de plotagem real onde os dados são exibidos (uma Figure pode conter múltiplos Axes)
3. **Artist** - Tudo visível na figura (linhas, texto, ticks, etc.)
4. **Axis** - Os objetos da linha numérica (eixo x, eixo y) que lidam com ticks e rótulos

### Duas Interfaces

**1. Interface pyplot (Implícita, estilo MATLAB)**
```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()
```
- Conveniente para gráficos rápidos e simples
- Mantém estado automaticamente
- Bom para trabalho interativo e scripts simples

**2. Interface Orientada a Objetos (Explícita)**
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4])
ax.set_ylabel('some numbers')
plt.show()
```
- **Recomendado para a maioria dos casos de uso**
- Controle mais explícito sobre figura e axes
- Melhor para figuras complexas com múltiplos subplots
- Mais fácil de manter e depurar

## Workflows Comuns

### 1. Criação Básica de Gráficos

**Workflow de gráfico único:**
```python
import matplotlib.pyplot as plt
import numpy as np

# Create figure and axes (OO interface - RECOMMENDED)
fig, ax = plt.subplots(figsize=(10, 6))

# Generate and plot data
x = np.linspace(0, 2*np.pi, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# Customize
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Trigonometric Functions')
ax.legend()
ax.grid(True, alpha=0.3)

# Save and/or display
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

### 2. Múltiplos Subplots

**Criando layouts de subplot:**
```python
# Method 1: Regular grid
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].plot(x, y1)
axes[0, 1].scatter(x, y2)
axes[1, 0].bar(categories, values)
axes[1, 1].hist(data, bins=30)

# Method 2: Mosaic layout (more flexible)
fig, axes = plt.subplot_mosaic([['left', 'right_top'],
                                 ['left', 'right_bottom']],
                                figsize=(10, 8))
axes['left'].plot(x, y)
axes['right_top'].scatter(x, y)
axes['right_bottom'].hist(data)

# Method 3: GridSpec (maximum control)
from matplotlib.gridspec import GridSpec
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(3, 3, figure=fig)
ax1 = fig.add_subplot(gs[0, :])  # Top row, all columns
ax2 = fig.add_subplot(gs[1:, 0])  # Bottom two rows, first column
ax3 = fig.add_subplot(gs[1:, 1:])  # Bottom two rows, last two columns
```

### 3. Tipos de Gráficos e Casos de Uso

**Gráficos de linha** - Séries temporais, dados contínuos, tendências
```python
ax.plot(x, y, linewidth=2, linestyle='--', marker='o', color='blue')
```

**Gráficos de dispersão** - Relações entre variáveis, correlações
```python
ax.scatter(x, y, s=sizes, c=colors, alpha=0.6, cmap='viridis')
```

**Gráficos de barras** - Comparações categóricas
```python
ax.bar(categories, values, color='steelblue', edgecolor='black')
# For horizontal bars:
ax.barh(categories, values)
```

**Histogramas** - Distribuições
```python
ax.hist(data, bins=30, edgecolor='black', alpha=0.7)
```

**Mapas de calor** - Dados de matriz, correlações
```python
im = ax.imshow(matrix, cmap='coolwarm', aspect='auto')
plt.colorbar(im, ax=ax)
```

**Gráficos de contorno** - Dados 3D em plano 2D
```python
contour = ax.contour(X, Y, Z, levels=10)
ax.clabel(contour, inline=True, fontsize=8)
```

**Box plots** - Distribuições estatísticas
```python
ax.boxplot([data1, data2, data3], labels=['A', 'B', 'C'])
```

**Violin plots** - Densidades de distribuição
```python
ax.violinplot([data1, data2, data3], positions=[1, 2, 3])
```

Para exemplos abrangentes de tipos de gráficos e variações, consulte `references/plot_types.md`.

### 4. Estilos e Personalização

**Métodos de especificação de cor:**
- Cores nomeadas: `'red'`, `'blue'`, `'steelblue'`
- Códigos hexadecimais: `'#FF5733'`
- Tuplas RGB: `(0.1, 0.2, 0.3)`
- Colormaps: `cmap='viridis'`, `cmap='plasma'`, `cmap='coolwarm'`

**Usando stylesheets:**
```python
plt.style.use('seaborn-v0_8-darkgrid')  # Apply predefined style
# Available styles: 'ggplot', 'bmh', 'fivethirtyeight', etc.
print(plt.style.available)  # List all available styles
```

**Personalizando com rcParams:**
```python
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.titlesize'] = 18
```

**Texto e anotações:**
```python
ax.text(x, y, 'annotation', fontsize=12, ha='center')
ax.annotate('important point', xy=(x, y), xytext=(x+1, y+1),
            arrowprops=dict(arrowstyle='->', color='red'))
```

Para opções detalhadas de estilo e diretrizes de colormap, consulte `references/styling_guide.md`.

### 5. Salvando Figuras

**Exportando para vários formatos:**
```python
# High-resolution PNG for presentations/papers
plt.savefig('figure.png', dpi=300, bbox_inches='tight', facecolor='white')

# Vector format for publications (scalable)
plt.savefig('figure.pdf', bbox_inches='tight')
plt.savefig('figure.svg', bbox_inches='tight')

# Transparent background
plt.savefig('figure.png', dpi=300, bbox_inches='tight', transparent=True)
```

**Parâmetros importantes:**
- `dpi`: Resolução (300 para publicações, 150 para web, 72 para tela)
- `bbox_inches='tight'`: Remove espaço em branco excessivo
- `facecolor='white'`: Garante fundo branco (útil para temas transparentes)
- `transparent=True`: Fundo transparente

### 6. Trabalhando com Gráficos 3D

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Surface plot
ax.plot_surface(X, Y, Z, cmap='viridis')

# 3D scatter
ax.scatter(x, y, z, c=colors, marker='o')

# 3D line plot
ax.plot(x, y, z, linewidth=2)

# Labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
```

## Melhores Práticas

### 1. Seleção de Interface
- **Use a interface orientada a objetos** (fig, ax = plt.subplots()) para código de produção
- Reserve a interface pyplot apenas para exploração interativa rápida
- Sempre crie figuras explicitamente em vez de confiar no estado implícito

### 2. Tamanho da Figura e DPI
- Defina figsize na criação: `fig, ax = plt.subplots(figsize=(10, 6))`
- Use DPI apropriado para meio de saída:
  - Tela/notebook: 72-100 dpi
  - Web: 150 dpi
  - Impressão/publicações: 300 dpi

### 3. Gerenciamento de Layout
- Use `constrained_layout=True` ou `tight_layout()` para evitar sobreposição de elementos
- `fig, ax = plt.subplots(constrained_layout=True)` é recomendado para espaçamento automático

### 4. Seleção de Colormap
- **Sequencial** (viridis, plasma, inferno): Dados ordenados com progressão consistente
- **Divergente** (coolwarm, RdBu): Dados com ponto central significativo (ex: zero)
- **Qualitativo** (tab10, Set3): Dados categóricos/nominais
- Evite colormaps arco-íris (jet) - eles não são perceptualmente uniformes

### 5. Acessibilidade
- Use colormaps amigos de daltônicos (viridis, cividis)
- Adicione padrões/hachuras para gráficos de barras além de cores
- Garanta contraste suficiente entre elementos
- Inclua rótulos e legendas descritivas

### 6. Desempenho
- Para grandes conjuntos de dados, use `rasterized=True` em chamadas de plot para reduzir tamanho de arquivo
- Use redução apropriada de dados antes de plotar (ex: redimensionar série temporal densa)
- Para animações, use blitting para melhor desempenho

### 7. Organização de Código
```python
# Good practice: Clear structure
def create_analysis_plot(data, title):
    """Create standardized analysis plot."""
    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    # Plot data
    ax.plot(data['x'], data['y'], linewidth=2)

    # Customize
    ax.set_xlabel('X Axis Label', fontsize=12)
    ax.set_ylabel('Y Axis Label', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    return fig, ax

# Use the function
fig, ax = create_analysis_plot(my_data, 'My Analysis')
plt.savefig('analysis.png', dpi=300, bbox_inches='tight')
```

## Scripts de Referência Rápida

Esta habilidade inclui scripts auxiliares no diretório `scripts/`:

### `plot_template.py`
Script de template demonstrando vários tipos de plot com melhores práticas. Use isto como ponto de partida para criar novas visualizações.

**Uso:**
```bash
python scripts/plot_template.py
```

### `style_configurator.py`
Utilitário interativo para configurar preferências de estilo do matplotlib e gerar stylesheets customizados.

**Uso:**
```bash
python scripts/style_configurator.py
```

## Referências Detalhadas

Para informações abrangentes, consulte os documentos de referência:

- **`references/plot_types.md`** - Catálogo completo de tipos de plot com exemplos de código e casos de uso
- **`references/styling_guide.md`** - Opções detalhadas de estilo, colormaps e personalização
- **`references/api_reference.md`** - Referência de classes e métodos principais
- **`references/common_issues.md`** - Guia de solução de problemas para problemas comuns

## Integração com Outras Ferramentas

Matplotlib se integra bem com:
- **NumPy/Pandas** - Plot direto de arrays e DataFrames
- **Seaborn** - Visualizações estatísticas de alto nível construídas sobre matplotlib
- **Jupyter** - Plotting interativo com `%matplotlib inline` ou `%matplotlib widget`
- **Frameworks GUI** - Embedding em aplicações Tkinter, Qt, wxPython

## Pegadinhas Comuns

1. **Elementos sobrepostos**: Use `constrained_layout=True` ou `tight_layout()`
2. **Confusão de estado**: Use interface OO para evitar problemas com máquina de estado pyplot
3. **Problemas de memória com muitas figuras**: Feche figuras explicitamente com `plt.close(fig)`
4. **Avisos de fonte**: Instale fontes ou suprima avisos com `plt.rcParams['font.sans-serif']`
5. **Confusão de DPI**: Lembre-se que figsize está em polegadas, não pixels: `pixels = dpi * inches`

## Recursos Adicionais

- Documentação oficial: https://matplotlib.org/
- Galeria: https://matplotlib.org/stable/gallery/index.html
- Cheatsheets: https://matplotlib.org/cheatsheets/
- Tutoriais: https://matplotlib.org/stable/tutorials/index.html