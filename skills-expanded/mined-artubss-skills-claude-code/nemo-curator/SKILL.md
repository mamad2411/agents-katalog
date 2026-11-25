---
name: nemo-curator
description: Curação de dados acelerada por GPU para treinamento de LLM. Suporta texto/imagem/vídeo/áudio. Recursos incluem deduplicação fuzzy (16× mais rápida), filtragem de qualidade (30+ heurísticas), deduplicação semântica, redação de PII, detecção NSFW. Escala em GPUs com RAPIDS. Use para preparar datasets de treinamento de alta qualidade, limpar dados web ou deduplicar grandes corpora.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Data Processing, NeMo Curator, Data Curation, GPU Acceleration, Deduplication, Quality Filtering, NVIDIA, RAPIDS, PII Redaction, Multimodal, LLM Training Data]
dependencies: [nemo-curator, cudf, dask, rapids]
---

# NeMo Curator - Curação de Dados Acelerada por GPU

Toolkit da NVIDIA para preparar dados de treinamento de alta qualidade para LLMs.

## Quando usar NeMo Curator

**Use NeMo Curator quando:**
- Preparar dados de treinamento de LLM a partir de web scrapes (Common Crawl)
- Precisar de deduplicação rápida (16× mais rápida que CPU)
- Curar datasets multimodais (texto, imagens, vídeo, áudio)
- Filtrar conteúdo de baixa qualidade ou tóxico
- Escalar processamento de dados em cluster de GPUs

**Desempenho**:
- **16× mais rápida** deduplicação fuzzy (8TB RedPajama v2)
- **40% TCO mais baixo** vs alternativas CPU
- **Escalabilidade quase linear** em nós GPU

**Use alternativas em vez disso**:
- **datatrove**: Processamento de dados open-source baseado em CPU
- **dolma**: Toolkit de dados da Allen AI
- **Ray Data**: Processamento de dados ML geral (sem foco em curação)

## Início rápido

### Instalação

```bash
# Curação de texto (CUDA 12)
uv pip install "nemo-curator[text_cuda12]"

# Todas as modalidades
uv pip install "nemo-curator[all_cuda12]"

# Apenas CPU (mais lento)
uv pip install "nemo-curator[cpu]"
```

### Pipeline básico de curação de texto

```python
from nemo_curator import ScoreFilter, Modify
from nemo_curator.datasets import DocumentDataset
import pandas as pd

# Carregar dados
df = pd.DataFrame({"text": ["Good document", "Bad doc", "Excellent text"]})
dataset = DocumentDataset(df)

# Filtragem de qualidade
def quality_score(doc):
    return len(doc["text"].split()) > 5  # Filtrar docs curtos

filtered = ScoreFilter(quality_score)(dataset)

# Deduplicação
from nemo_curator.modules import ExactDuplicates
deduped = ExactDuplicates()(filtered)

# Salvar
deduped.to_parquet("curated_data/")
```

## Pipeline de curação de dados

### Estágio 1: Filtragem de qualidade

```python
from nemo_curator.filters import (
    WordCountFilter,
    RepeatedLinesFilter,
    UrlRatioFilter,
    NonAlphaNumericFilter
)

# Aplicar 30+ filtros heurísticos
from nemo_curator import ScoreFilter

# Filtro de contagem de palavras
dataset = dataset.filter(WordCountFilter(min_words=50, max_words=100000))

# Remover conteúdo repetitivo
dataset = dataset.filter(RepeatedLinesFilter(max_repeated_line_fraction=0.3))

# Filtro de proporção de URL
dataset = dataset.filter(UrlRatioFilter(max_url_ratio=0.2))
```

### Estágio 2: Deduplicação

**Deduplicação exata**:
```python
from nemo_curator.modules import ExactDuplicates

# Remover duplicatas exatas
deduped = ExactDuplicates(id_field="id", text_field="text")(dataset)
```

**Deduplicação fuzzy** (16× mais rápida em GPU):
```python
from nemo_curator.modules import FuzzyDuplicates

# Deduplicação MinHash + LSH
fuzzy_dedup = FuzzyDuplicates(
    id_field="id",
    text_field="text",
    num_hashes=260,      # Parâmetros MinHash
    num_buckets=20,
    hash_method="md5"
)

deduped = fuzzy_dedup(dataset)
```

**Deduplicação semântica**:
```python
from nemo_curator.modules import SemanticDuplicates

# Deduplicação baseada em embedding
semantic_dedup = SemanticDuplicates(
    id_field="id",
    text_field="text",
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    threshold=0.8  # Limite de similaridade de cosseno
)

deduped = semantic_dedup(dataset)
```

### Estágio 3: Redação de PII

```python
from nemo_curator.modules import Modify
from nemo_curator.modifiers import PIIRedactor

# Redigir informações de identificação pessoal
pii_redactor = PIIRedactor(
    supported_entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "PERSON", "LOCATION"],
    anonymize_action="replace"  # ou "redact"
)

redacted = Modify(pii_redactor)(dataset)
```

### Estágio 4: Filtragem com classificador

```python
from nemo_curator.classifiers import QualityClassifier

# Classificação de qualidade
quality_clf = QualityClassifier(
    model_path="nvidia/quality-classifier-deberta",
    batch_size=256,
    device="cuda"
)

# Filtrar documentos de baixa qualidade
high_quality = dataset.filter(lambda doc: quality_clf(doc["text"]) > 0.5)
```

## Aceleração por GPU

### Desempenho GPU vs CPU

| Operação | CPU (16 cores) | GPU (A100) | Speedup |
|----------|----------------|------------|---------|
| Dedup fuzzy (8TB) | 120 horas | 7,5 horas | 16× |
| Dedup exata (1TB) | 8 horas | 0,5 horas | 16× |
| Filtragem de qualidade | 2 horas | 0,2 horas | 10× |

### Escalamento multi-GPU

```python
from nemo_curator import get_client
import dask_cuda

# Inicializar cluster de GPU
client = get_client(cluster_type="gpu", n_workers=8)

# Processar com 8 GPUs
deduped = FuzzyDuplicates(...)(dataset)
```

## Curação multimodal

### Curação de imagem

```python
from nemo_curator.image import (
    AestheticFilter,
    NSFWFilter,
    CLIPEmbedder
)

# Pontuação estética
aesthetic_filter = AestheticFilter(threshold=5.0)
filtered_images = aesthetic_filter(image_dataset)

# Detecção NSFW
nsfw_filter = NSFWFilter(threshold=0.9)
safe_images = nsfw_filter(filtered_images)

# Gerar embeddings CLIP
clip_embedder = CLIPEmbedder(model="openai/clip-vit-base-patch32")
image_embeddings = clip_embedder(safe_images)
```

### Curação de vídeo

```python
from nemo_curator.video import (
    SceneDetector,
    ClipExtractor,
    InternVideo2Embedder
)

# Detectar cenas
scene_detector = SceneDetector(threshold=27.0)
scenes = scene_detector(video_dataset)

# Extrair clipes
clip_extractor = ClipExtractor(min_duration=2.0, max_duration=10.0)
clips = clip_extractor(scenes)

# Gerar embeddings
video_embedder = InternVideo2Embedder()
video_embeddings = video_embedder(clips)
```

### Curação de áudio

```python
from nemo_curator.audio import (
    ASRInference,
    WERFilter,
    DurationFilter
)

# Transcrição ASR
asr = ASRInference(model="nvidia/stt_en_fastconformer_hybrid_large_pc")
transcribed = asr(audio_dataset)

# Filtrar por WER (taxa de erro de palavra)
wer_filter = WERFilter(max_wer=0.3)
high_quality_audio = wer_filter(transcribed)

# Filtragem de duração
duration_filter = DurationFilter(min_duration=1.0, max_duration=30.0)
filtered_audio = duration_filter(high_quality_audio)
```

## Padrões comuns

### Curação de web scrape (Common Crawl)

```python
from nemo_curator import ScoreFilter, Modify
from nemo_curator.filters import *
from nemo_curator.modules import *
from nemo_curator.datasets import DocumentDataset

# Carregar dados de Common Crawl
dataset = DocumentDataset.read_parquet("common_crawl/*.parquet")

# Pipeline
pipeline = [
    # 1. Filtragem de qualidade
    WordCountFilter(min_words=100, max_words=50000),
    RepeatedLinesFilter(max_repeated_line_fraction=0.2),
    SymbolToWordRatioFilter(max_symbol_to_word_ratio=0.3),
    UrlRatioFilter(max_url_ratio=0.3),

    # 2. Filtragem de idioma
    LanguageIdentificationFilter(target_languages=["en"]),

    # 3. Deduplicação
    ExactDuplicates(id_field="id", text_field="text"),
    FuzzyDuplicates(id_field="id", text_field="text", num_hashes=260),

    # 4. Redação de PII
    PIIRedactor(),

    # 5. Filtragem NSFW
    NSFWClassifier(threshold=0.8)
]

# Executar
for stage in pipeline:
    dataset = stage(dataset)

# Salvar
dataset.to_parquet("curated_common_crawl/")
```

### Processamento distribuído

```python
from nemo_curator import get_client
from dask_cuda import LocalCUDACluster

# Cluster multi-GPU
cluster = LocalCUDACluster(n_workers=8)
client = get_client(cluster=cluster)

# Processar dataset grande
dataset = DocumentDataset.read_parquet("s3://large_dataset/*.parquet")
deduped = FuzzyDuplicates(...)(dataset)

# Limpeza
client.close()
cluster.close()
```

## Benchmarks de desempenho

### Deduplicação fuzzy (8TB RedPajama v2)

- **CPU (256 cores)**: 120 horas
- **GPU (8× A100)**: 7,5 horas
- **Speedup**: 16×

### Deduplicação exata (1TB)

- **CPU (64 cores)**: 8 horas
- **GPU (4× A100)**: 0,5 horas
- **Speedup**: 16×

### Filtragem de qualidade (100GB)

- **CPU (32 cores)**: 2 horas
- **GPU (2× A100)**: 0,2 horas
- **Speedup**: 10×

## Comparação de custos

**Curação baseada em CPU** (AWS c5.18xlarge × 10):
- Custo: R$ 3,60/hora × 10 = R$ 36/hora
- Tempo para 8TB: 120 horas
- **Total**: R$ 4.320

**Curação baseada em GPU** (AWS p4d.24xlarge × 2):
- Custo: R$ 32,77/hora × 2 = R$ 65,54/hora
- Tempo para 8TB: 7,5 horas
- **Total**: R$ 491,55

**Economia**: Redução de 89% (R$ 3.828 economizados)

## Formatos de dados suportados

- **Entrada**: Parquet, JSONL, CSV
- **Saída**: Parquet (recomendado), JSONL
- **WebDataset**: Arquivos TAR para multimodal

## Casos de uso

**Deployments em produção**:
- NVIDIA usou NeMo Curator para preparar dados de treinamento Nemotron-4
- Datasets open-source curados: RedPajama v2, The Pile

## Referências

- **[Filtering Guide](references/filtering.md)** - 30+ filtros de qualidade, heurísticas
- **[Deduplication Guide](references/deduplication.md)** - Métodos exato, fuzzy e semântico

## Recursos

- **GitHub**: https://github.com/NVIDIA/NeMo-Curator ⭐ 500+
- **Docs**: https://docs.nvidia.com/nemo-framework/user-guide/latest/datacuration/
- **Version**: 0.4.0+
- **License**: Apache 2.0