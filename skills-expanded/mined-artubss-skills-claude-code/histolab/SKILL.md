---
name: histolab
description: Kit de ferramentas de processamento de imagens de patologia digital para imagens de lâminas inteiras (WSI). Use essa skill ao trabalhar com lâminas de histopatologia, processar imagens de tecido corado com H&E ou IHC, extrair tiles de imagens de patologia gigapixel, detectar regiões de tecido, segmentar máscaras de tecido ou preparar datasets para pipelines de deep learning de patologia computacional. Aplica-se a formatos WSI (SVS, TIFF, NDPI), análise baseada em tiles e fluxos de trabalho de pré-processamento de imagens histológicas.
---

# Histolab

## Overview

Histolab é uma biblioteca Python para processar imagens de lâminas inteiras (WSI) em patologia digital. Automatiza a detecção de tecido, extrai tiles informativos de imagens gigapixel e prepara datasets para pipelines de deep learning. A biblioteca processa múltiplos formatos de WSI, implementa segmentação sofisticada de tecido e oferece estratégias flexíveis de extração de tiles.

## Instalação

```bash
uv pip install histolab
```

## Quick Start

Fluxo básico para extrair tiles de uma imagem de lâmina inteira:

```python
from histolab.slide import Slide
from histolab.tiler import RandomTiler

# Carregar lâmina
slide = Slide("slide.svs", processed_path="output/")

# Configurar tiler
tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    seed=42
)

# Visualizar localizações dos tiles
tiler.locate_tiles(slide, n_tiles=20)

# Extrair tiles
tiler.extract(slide)
```

## Core Capabilities

### 1. Gerenciamento de Lâminas

Carregar, inspecionar e trabalhar com imagens de lâminas inteiras em diversos formatos.

**Operações comuns:**
- Carregar arquivos WSI (SVS, TIFF, NDPI, etc.)
- Acessar metadados da lâmina (dimensões, magnificação, propriedades)
- Gerar thumbnails para visualização
- Trabalhar com estruturas de imagem piramidal
- Extrair regiões em coordenadas específicas

**Classes principais:** `Slide`

**Referência:** `references/slide_management.md` contém documentação abrangente sobre:
- Inicialização e configuração de lâminas
- Datasets de amostra integrados (próstata, ovário, mama, coração, rins)
- Acesso a propriedades e metadados da lâmina
- Geração e visualização de thumbnails
- Trabalho com níveis de pirâmide
- Fluxos de trabalho de processamento multi-lâmina

**Exemplo de fluxo:**
```python
from histolab.slide import Slide
from histolab.data import prostate_tissue

# Carregar dados de amostra
prostate_svs, prostate_path = prostate_tissue()

# Inicializar lâmina
slide = Slide(prostate_path, processed_path="output/")

# Inspecionar propriedades
print(f"Dimensões: {slide.dimensions}")
print(f"Níveis: {slide.levels}")
print(f"Magnificação: {slide.properties.get('openslide.objective-power')}")

# Salvar thumbnail
slide.save_thumbnail()
```

### 2. Detecção de Tecido e Máscaras

Identificar automaticamente regiões de tecido e filtrar fundo/artefatos.

**Operações comuns:**
- Criar máscaras binárias de tecido
- Detectar a maior região de tecido
- Excluir fundo e artefatos
- Segmentação personalizada de tecido
- Remover anotações em caneta

**Classes principais:** `TissueMask`, `BiggestTissueBoxMask`, `BinaryMask`

**Referência:** `references/tissue_masks.md` contém documentação abrangente sobre:
- TissueMask: Segmenta todas as regiões de tecido usando filtros automatizados
- BiggestTissueBoxMask: Retorna caixa delimitadora da maior região de tecido (padrão)
- BinaryMask: Classe base para implementações de máscara personalizada
- Visualizar máscaras com `locate_mask()`
- Criar máscaras retangulares e máscaras personalizadas de exclusão de anotações
- Integração de máscara com extração de tiles
- Melhores práticas e resolução de problemas

**Exemplo de fluxo:**
```python
from histolab.masks import TissueMask, BiggestTissueBoxMask

# Criar máscara de tecido para todas as regiões
tissue_mask = TissueMask()

# Visualizar máscara na lâmina
slide.locate_mask(tissue_mask)

# Obter array da máscara
mask_array = tissue_mask(slide)

# Usar a maior região de tecido (padrão para a maioria dos extractors)
biggest_mask = BiggestTissueBoxMask()
```

**Quando usar cada máscara:**
- `TissueMask`: Múltiplas seções de tecido, análise abrangente
- `BiggestTissueBoxMask`: Seção única de tecido principal, excluir artefatos (padrão)
- `BinaryMask` personalizado: ROI específica, excluir anotações, segmentação personalizada

### 3. Extração de Tiles

Extrair regiões menores de WSI grande usando diferentes estratégias.

**Três estratégias de extração:**

**RandomTiler:** Extrair número fixo de tiles posicionados aleatoriamente
- Melhor para: Amostrar regiões diversas, análise exploratória, dados de treinamento
- Parâmetros principais: `n_tiles`, `seed` para reprodutibilidade

**GridTiler:** Extrair sistematicamente tiles através do tecido em padrão de grade
- Melhor para: Cobertura completa, análise espacial, reconstrução
- Parâmetros principais: `pixel_overlap` para janelas deslizantes

**ScoreTiler:** Extrair tiles mais bem classificados com base em funções de pontuação
- Melhor para: Regiões mais informativas, seleção orientada por qualidade
- Parâmetros principais: `scorer` (NucleiScorer, CellularityScorer, personalizado)

**Parâmetros comuns:**
- `tile_size`: Dimensões do tile (ex: (512, 512))
- `level`: Nível de pirâmide para extração (0 = resolução mais alta)
- `check_tissue`: Filtrar tiles por conteúdo de tecido
- `tissue_percent`: Cobertura mínima de tecido (padrão 80%)
- `extraction_mask`: Máscara que define a região de extração

**Referência:** `references/tile_extraction.md` contém documentação abrangente sobre:
- Explicação detalhada de cada estratégia de tiler
- Scorers disponíveis (NucleiScorer, CellularityScorer, personalizado)
- Visualização de tiles com `locate_tiles()`
- Fluxos de trabalho e relatórios de extração
- Padrões avançados (extração multi-nível, hierárquica)
- Otimização de desempenho e resolução de problemas

**Exemplos de fluxo:**

```python
from histolab.tiler import RandomTiler, GridTiler, ScoreTiler
from histolab.scorer import NucleiScorer

# Amostragem aleatória (rápida, diversa)
random_tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    seed=42,
    check_tissue=True,
    tissue_percent=80.0
)
random_tiler.extract(slide)

# Cobertura em grade (abrangente)
grid_tiler = GridTiler(
    tile_size=(512, 512),
    level=0,
    pixel_overlap=0,
    check_tissue=True
)
grid_tiler.extract(slide)

# Seleção baseada em pontuação (mais informativa)
score_tiler = ScoreTiler(
    tile_size=(512, 512),
    n_tiles=50,
    scorer=NucleiScorer(),
    level=0
)
score_tiler.extract(slide, report_path="tiles_report.csv")
```

**Sempre fazer visualização antes de extrair:**
```python
# Visualizar localizações dos tiles na thumbnail
tiler.locate_tiles(slide, n_tiles=20)
```

### 4. Filtros e Pré-processamento

Aplicar filtros de processamento de imagem para detecção de tecido, controle de qualidade e pré-processamento.

**Categorias de filtros:**

**Filtros de imagem:** Conversões de espaço de cor, limiarização, aprimoramento de contraste
- `RgbToGrayscale`, `RgbToHsv`, `RgbToHed`
- `OtsuThreshold`, `AdaptiveThreshold`
- `StretchContrast`, `HistogramEqualization`

**Filtros morfológicos:** Operações estruturais em imagens binárias
- `BinaryDilation`, `BinaryErosion`
- `BinaryOpening`, `BinaryClosing`
- `RemoveSmallObjects`, `RemoveSmallHoles`

**Composição:** Encadear múltiplos filtros
- `Compose`: Criar pipelines de filtros

**Referência:** `references/filters_preprocessing.md` contém documentação abrangente sobre:
- Explicação detalhada de cada tipo de filtro
- Composição e encadeamento de filtros
- Pipelines comuns de pré-processamento (detecção de tecido, remoção de caneta, aprimoramento de núcleos)
- Aplicar filtros a tiles
- Filtros de máscara personalizada
- Filtros de controle de qualidade (detecção de desfoque, cobertura de tecido)
- Melhores práticas e resolução de problemas

**Exemplos de fluxo:**

```python
from histolab.filters.compositions import Compose
from histolab.filters.image_filters import RgbToGrayscale, OtsuThreshold
from histolab.filters.morphological_filters import (
    BinaryDilation, RemoveSmallHoles, RemoveSmallObjects
)

# Pipeline padrão de detecção de tecido
tissue_detection = Compose([
    RgbToGrayscale(),
    OtsuThreshold(),
    BinaryDilation(disk_size=5),
    RemoveSmallHoles(area_threshold=1000),
    RemoveSmallObjects(area_threshold=500)
])

# Usar com máscara personalizada
from histolab.masks import TissueMask
custom_mask = TissueMask(filters=tissue_detection)

# Aplicar filtros ao tile
from histolab.tile import Tile
filtered_tile = tile.apply_filters(tissue_detection)
```

### 5. Visualização

Visualizar lâminas, máscaras, localizações de tiles e qualidade de extração.

**Tarefas comuns de visualização:**
- Exibir thumbnails de lâminas
- Visualizar máscaras de tecido
- Visualizar localizações de tiles
- Avaliar qualidade de tiles
- Criar relatórios e figuras

**Referência:** `references/visualization.md` contém documentação abrangente sobre:
- Exibição e salvamento de thumbnail de lâmina
- Visualização de máscara com `locate_mask()`
- Visualização de localização de tiles com `locate_tiles()`
- Exibir tiles extraídos e criar mosaicos
- Avaliação de qualidade (distribuição de pontuações, tiles superiores vs inferiores)
- Visualização multi-lâmina
- Visualização de efeito de filtro
- Exportar figuras e relatórios PDF em alta resolução
- Visualização interativa em notebooks Jupyter

**Exemplos de fluxo:**

```python
import matplotlib.pyplot as plt
from histolab.masks import TissueMask

# Exibir thumbnail de lâmina
plt.figure(figsize=(10, 10))
plt.imshow(slide.thumbnail)
plt.title(f"Lâmina: {slide.name}")
plt.axis('off')
plt.show()

# Visualizar máscara de tecido
tissue_mask = TissueMask()
slide.locate_mask(tissue_mask)

# Visualizar localizações de tiles
tiler = RandomTiler(tile_size=(512, 512), n_tiles=50)
tiler.locate_tiles(slide, n_tiles=20)

# Exibir tiles extraídos em grade
from pathlib import Path
from PIL import Image

tile_paths = list(Path("output/tiles/").glob("*.png"))[:16]
fig, axes = plt.subplots(4, 4, figsize=(12, 12))
axes = axes.ravel()

for idx, tile_path in enumerate(tile_paths):
    tile_img = Image.open(tile_path)
    axes[idx].imshow(tile_img)
    axes[idx].set_title(tile_path.stem, fontsize=8)
    axes[idx].axis('off')

plt.tight_layout()
plt.show()
```

## Typical Workflows

### Workflow 1: Exploratory Tile Extraction

Amostragem rápida de regiões diversas de tecido para análise inicial.

```python
from histolab.slide import Slide
from histolab.tiler import RandomTiler
import logging

# Ativar logging para rastreamento de progresso
logging.basicConfig(level=logging.INFO)

# Carregar lâmina
slide = Slide("slide.svs", processed_path="output/random_tiles/")

# Inspecionar lâmina
print(f"Dimensões: {slide.dimensions}")
print(f"Níveis: {slide.levels}")
slide.save_thumbnail()

# Configurar tiler aleatório
random_tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    seed=42,
    check_tissue=True,
    tissue_percent=80.0
)

# Visualizar localizações
random_tiler.locate_tiles(slide, n_tiles=20)

# Extrair tiles
random_tiler.extract(slide)
```

### Workflow 2: Comprehensive Grid Extraction

Cobertura completa de tecido para análise de lâmina inteira.

```python
from histolab.slide import Slide
from histolab.tiler import GridTiler
from histolab.masks import TissueMask

# Carregar lâmina
slide = Slide("slide.svs", processed_path="output/grid_tiles/")

# Usar TissueMask para todas as seções de tecido
tissue_mask = TissueMask()
slide.locate_mask(tissue_mask)

# Configurar tiler em grade
grid_tiler = GridTiler(
    tile_size=(512, 512),
    level=1,  # Usar nível 1 para extração mais rápida
    pixel_overlap=0,
    check_tissue=True,
    tissue_percent=70.0
)

# Visualizar grade
grid_tiler.locate_tiles(slide)

# Extrair todos os tiles
grid_tiler.extract(slide, extraction_mask=tissue_mask)
```

### Workflow 3: Quality-Driven Tile Selection

Extrair tiles mais informativos baseado em densidade de núcleos.

```python
from histolab.slide import Slide
from histolab.tiler import ScoreTiler
from histolab.scorer import NucleiScorer
import pandas as pd
import matplotlib.pyplot as plt

# Carregar lâmina
slide = Slide("slide.svs", processed_path="output/scored_tiles/")

# Configurar score tiler
score_tiler = ScoreTiler(
    tile_size=(512, 512),
    n_tiles=50,
    level=0,
    scorer=NucleiScorer(),
    check_tissue=True
)

# Visualizar tiles superiores
score_tiler.locate_tiles(slide, n_tiles=15)

# Extrair com relatório
score_tiler.extract(slide, report_path="tiles_report.csv")

# Analisar pontuações
report_df = pd.read_csv("tiles_report.csv")
plt.hist(report_df['score'], bins=20, edgecolor='black')
plt.xlabel('Pontuação do Tile')
plt.ylabel('Frequência')
plt.title('Distribuição de Pontuações de Tiles')
plt.show()
```

### Workflow 4: Multi-Slide Processing Pipeline

Processar coleção inteira de lâminas com parâmetros consistentes.

```python
from pathlib import Path
from histolab.slide import Slide
from histolab.tiler import RandomTiler
import logging

logging.basicConfig(level=logging.INFO)

# Configurar tiler uma vez
tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=50,
    level=0,
    seed=42,
    check_tissue=True
)

# Processar todas as lâminas
slide_dir = Path("slides/")
output_base = Path("output/")

for slide_path in slide_dir.glob("*.svs"):
    print(f"\nProcessando: {slide_path.name}")

    # Criar diretório de saída específico da lâmina
    output_dir = output_base / slide_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    # Carregar e processar lâmina
    slide = Slide(slide_path, processed_path=output_dir)

    # Salvar thumbnail para revisão
    slide.save_thumbnail()

    # Extrair tiles
    tiler.extract(slide)

    print(f"Concluído: {slide_path.name}")
```

### Workflow 5: Custom Tissue Detection and Filtering

Tratar lâminas com artefatos, anotações ou coloração incomum.

```python
from histolab.slide import Slide
from histolab.masks import TissueMask
from histolab.tiler import RandomTiler
from histolab.filters.compositions import Compose
from histolab.filters.image_filters import RgbToGrayscale, OtsuThreshold
from histolab.filters.morphological_filters import (
    BinaryDilation, RemoveSmallObjects, RemoveSmallHoles
)

# Definir pipeline de filtros personalizado para remoção agressiva de artefatos
aggressive_filters = Compose([
    RgbToGrayscale(),
    OtsuThreshold(),
    BinaryDilation(disk_size=10),
    RemoveSmallHoles(area_threshold=5000),
    RemoveSmallObjects(area_threshold=3000)  # Remover artefatos maiores
])

# Criar máscara personalizada
custom_mask = TissueMask(filters=aggressive_filters)

# Carregar lâmina e visualizar máscara
slide = Slide("slide.svs", processed_path="output/")
slide.locate_mask(custom_mask)

# Extrair com máscara personalizada
tiler = RandomTiler(tile_size=(512, 512), n_tiles=100)
tiler.extract(slide, extraction_mask=custom_mask)
```

## Best Practices

### Slide Loading and Inspection
1. Sempre inspecionar propriedades da lâmina antes do processamento
2. Salvar thumbnails para revisão visual rápida
3. Verificar níveis de pirâmide e dimensões
4. Verificar se a lâmina contém tecido usando thumbnails

### Tissue Detection
1. Visualizar máscaras com `locate_mask()` antes da extração
2. Usar `TissueMask` para múltiplas seções, `BiggestTissueBoxMask` para seções únicas
3. Personalizar filtros para colorações específicas (H&E vs IHC)
4. Tratar anotações em caneta com máscaras personalizado
5. Testar máscaras em lâminas diversas

### Tile Extraction
1. **Sempre visualizar com `locate_tiles()` antes de extrair**
2. Escolher tiler apropriado:
   - RandomTiler: Amostragem e exploração
   - GridTiler: Cobertura completa
   - ScoreTiler: Seleção orientada por qualidade
3. Definir limiar `tissue_percent` apropriado (70-90% típico)
4. Usar seeds para reprodutibilidade em RandomTiler
5. Extrair em nível de pirâmide apropriado para resolução de análise
6. Ativar logging para datasets grandes

### Performance
1. Extrair em níveis inferiores (1, 2) para processamento mais rápido
2. Usar `BiggestTissueBoxMask` em vez de `TissueMask` quando apropriado
3. Ajustar `tissue_percent` para reduzir tentativas de tile inválido
4. Limitar `n_tiles` para exploração inicial
5. Usar `pixel_overlap=0` para grades não sobrepostas

### Quality Control
1. Validar qualidade de tiles (verificar desfoque, artefatos, foco)
2. Revisar distribuições de pontuação para ScoreTiler
3. Inspecionar tiles com maior e menor pontuação
4. Monitorar estatísticas de cobertura de tecido
5. Filtrar tiles extraídos por métricas de qualidade adicionais se necessário

## Common Use Cases

### Training Deep Learning Models
- Extrair datasets balanceados usando RandomTiler em múltiplas lâminas
- Usar ScoreTiler com NucleiScorer para focar em regiões ricas em células
- Extrair em resolução consistente (nível 0 ou nível 1)
- Gerar relatórios CSV para rastreamento de metadados de tiles

### Whole Slide Analysis
- Usar GridTiler para cobertura completa de tecido
- Extrair em múltiplos níveis de pirâmide para análise hierárquica
- Manter relações espaciais com posições em grade
- Usar `pixel_overlap` para abordagens de janela deslizante

### Tissue Characterization
- Amostrar regiões diversas com RandomTiler
- Quantificar cobertura de tecido com máscaras
- Extrair informações específicas de coloração com decomposição HED
- Comparar padrões de tecido entre lâminas

### Quality Assessment
- Identificar regiões de foco ótimo com ScoreTiler
- Detectar artefatos usando máscaras e filtros personalizados
- Avaliar qualidade de coloração em coleção de lâminas
- Sinalizar lâminas problemáticas para revisão manual

### Dataset Curation
- Usar ScoreTiler para priorizar tiles informativos
- Filtrar tiles por porcentagem de tecido
- Gerar relatórios com pontuações de tiles e metadados
- Criar datasets estratificados entre lâminas e tipos de tecido

## Troubleshooting

### No tiles extracted
- Reduzir limiar `tissue_percent`
- Verificar se a lâmina contém tecido (verificar thumbnail)
- Garantir que extraction_mask capture regiões de tecido
- Verificar se tile_size é apropriado para resolução da lâmina

### Many background tiles
- Ativar `check_tissue=True`
- Aumentar limiar `tissue_percent`
- Usar máscara apropriada (TissueMask vs BiggestTissueBoxMask)
- Personalizar filtros de máscara para melhor detecção de tecido

### Extraction very slow
- Extrair em nível de pirâmide inferior (nível=1 ou 2)
- Reduzir `n_tiles` para RandomTiler/ScoreTiler
- Usar RandomTiler em vez de GridTiler para amostragem
- Usar BiggestTissueBoxMask em vez de TissueMask

### Tiles have artifacts
- Implementar máscaras personalizadas de exclusão de anotações
- Ajustar parâmetros de filtro para remoção de artefatos
- Aumentar limiar de remoção de objetos pequenos
- Aplicar filtragem de qualidade pós-extração

### Inconsistent results across slides
- Usar mesma seed para RandomTiler
- Normalizar coloração com filtros de pré-processamento
- Ajustar `tissue_percent` por qualidade de coloração
- Implementar personalização de máscara específica da lâmina

## Resources

Essa skill inclui documentação de referência detalhada no diretório `references/`:

### references/slide_management.md
Guia abrangente para carregar, inspecionar e trabalhar com imagens de lâminas inteiras:
- Inicialização e configuração de lâminas
- Datasets de amostra integrados
- Propriedades e metadados de lâminas
- Geração e visualização de thumbnails
- Trabalho com níveis de pirâmide
- Fluxos de trabalho de processamento multi-lâmina
- Melhores práticas e padrões comuns

### references/tissue_masks.md
Documentação completa sobre detecção e mascaramento de tecido:
- Classes TissueMask, BiggestTissueBoxMask, BinaryMask
- Como funcionam os filtros de detecção de tecido
- Personalizar máscaras com cadeias de filtros
- Visualizar máscaras
- Criar máscaras retangulares personalizadas e máscaras de exclusão de anotações
- Integração com extração de tiles
- Melhores práticas e resolução de problemas

### references/tile_extraction.md
Explicação detalhada das estratégias de extração de tiles:
- Comparação RandomTiler, GridTiler, ScoreTiler
- Scorers disponíveis (NucleiScorer, CellularityScorer, personalizado)
- Parâmetros comuns e específicos de estratégia
- Visualização de tiles com locate_tiles()
- Fluxos de trabalho e relatórios CSV
- Padrões avançados (multi-nível, hierárquico)
- Otimização de desempenho
- Resolução de problemas comuns

### references/filters_preprocessing.md
Referência completa de filtros e guia de pré-processamento:
- Filtros de imagem (conversão de cor, limiarização, contraste)
- Filtros morfológicos (dilatação, erosão, abertura, fechamento)
- Composição e encadeamento de filtros
- Pipelines comuns de pré-processamento
- Aplicar filtros a tiles
- Filtros de máscara personalizada
- Filtros de controle de qualidade
- Melhores práticas e resolução de problemas

### references/visualization.md
Guia abrangente de visualização:
- Exibição e salvamento de thumbnail de lâmina
- Técnicas de visualização de máscara
- Visualização de localização de tiles
- Exibir tiles extraídos e criar mosaicos
- Visualizações de avaliação de qualidade
- Comparação multi-lâmina
- Visualização de efeito de filtro
- Exportar figuras em alta resolução e PDFs
- Visualização interativa em notebooks Jupyter

**Padrão de uso:** Arquivos de referência contêm informações detalhadas para suportar fluxos de trabalho descritos neste documento de skill principal. Carregar arquivos de referência específicos conforme necessário para orientação de implementação detalhada, resolução de problemas ou recursos avançados.