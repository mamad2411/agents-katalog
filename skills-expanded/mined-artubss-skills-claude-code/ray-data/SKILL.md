---
name: ray-data
description: Processamento escalável de dados para workloads de ML. Execução em streaming em CPU/GPU, suporta Parquet/CSV/JSON/imagens. Integra-se com Ray Train, PyTorch, TensorFlow. Escala de uma única máquina para centenas de nós. Use para inferência em lote, pré-processamento de dados, carregamento de dados multi-modal ou pipelines distribuídos de ETL.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Data Processing, Ray Data, Distributed Computing, ML Pipelines, Batch Inference, ETL, Scalable, Ray, PyTorch, TensorFlow]
dependencies: [ray[data], pyarrow, pandas]
---

# Ray Data - Processamento Escalável de Dados para ML

Biblioteca de processamento distribuído de dados para workloads de ML e IA.

## Quando usar Ray Data

**Use Ray Data quando:**
- Processar grandes datasets (>100GB) para treinamento de ML
- Precisar de pré-processamento distribuído de dados em cluster
- Construir pipelines de inferência em lote
- Carregar dados multi-modal (imagens, áudio, vídeo)
- Escalar processamento de dados de laptop para cluster

**Funcionalidades principais**:
- **Execução em streaming**: Processe dados maiores que a memória
- **Suporte a GPU**: Acelere transformações com GPUs
- **Integração com frameworks**: PyTorch, TensorFlow, HuggingFace
- **Multi-modal**: Imagens, Parquet, CSV, JSON, áudio, vídeo

**Use alternativas**:
- **Pandas**: Dados pequenos (<1GB) em uma única máquina
- **Dask**: Dados tabulares, operações tipo SQL
- **Spark**: ETL empresarial, queries SQL

## Guia rápido

### Instalação

```bash
pip install -U 'ray[data]'
```

### Carregar e transformar dados

```python
import ray

# Ler arquivos Parquet
ds = ray.data.read_parquet("s3://bucket/data/*.parquet")

# Transformar dados (execução lazy)
ds = ds.map_batches(lambda batch: {"processed": batch["text"].str.lower()})

# Consumir dados
for batch in ds.iter_batches(batch_size=100):
    print(batch)
```

### Integração com Ray Train

```python
import ray
from ray.train import ScalingConfig
from ray.train.torch import TorchTrainer

# Criar dataset
train_ds = ray.data.read_parquet("s3://bucket/train/*.parquet")

def train_func(config):
    # Acessar dataset no treinamento
    train_ds = ray.train.get_dataset_shard("train")

    for epoch in range(10):
        for batch in train_ds.iter_batches(batch_size=32):
            # Treinar com batch
            pass

# Treinar com Ray
trainer = TorchTrainer(
    train_func,
    datasets={"train": train_ds},
    scaling_config=ScalingConfig(num_workers=4, use_gpu=True)
)
trainer.fit()
```

## Lendo dados

### Do cloud storage

```python
import ray

# Parquet (recomendado para ML)
ds = ray.data.read_parquet("s3://bucket/data/*.parquet")

# CSV
ds = ray.data.read_csv("s3://bucket/data/*.csv")

# JSON
ds = ray.data.read_json("gs://bucket/data/*.json")

# Imagens
ds = ray.data.read_images("s3://bucket/images/")
```

### De objetos Python

```python
# De lista
ds = ray.data.from_items([{"id": i, "value": i * 2} for i in range(1000)])

# De range
ds = ray.data.range(1000000)  # Dados sintéticos

# De pandas
import pandas as pd
df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
ds = ray.data.from_pandas(df)
```

## Transformações

### Map batches (vetorizado)

```python
# Transformação em batch (rápido)
def process_batch(batch):
    batch["doubled"] = batch["value"] * 2
    return batch

ds = ds.map_batches(process_batch, batch_size=1000)
```

### Transformações de linha

```python
# Linha por linha (mais lento)
def process_row(row):
    row["squared"] = row["value"] ** 2
    return row

ds = ds.map(process_row)
```

### Filtro

```python
# Filtrar linhas
ds = ds.filter(lambda row: row["value"] > 100)
```

### Agrupar e agregar

```python
# Agrupar por coluna
ds = ds.groupby("category").count()

# Agregação customizada
ds = ds.groupby("category").map_groups(lambda group: {"sum": group["value"].sum()})
```

## Transformações aceleradas por GPU

```python
# Usar GPU para pré-processamento
def preprocess_images_gpu(batch):
    import torch
    images = torch.tensor(batch["image"]).cuda()
    # Pré-processamento em GPU
    processed = images * 255
    return {"processed": processed.cpu().numpy()}

ds = ds.map_batches(
    preprocess_images_gpu,
    batch_size=64,
    num_gpus=1  # Solicitar GPU
)
```

## Escrevendo dados

```python
# Escrever para Parquet
ds.write_parquet("s3://bucket/output/")

# Escrever para CSV
ds.write_csv("output/")

# Escrever para JSON
ds.write_json("output/")
```

## Otimização de performance

### Reparticionar

```python
# Controlar paralelismo
ds = ds.repartition(100)  # 100 blocos para cluster com 100 cores
```

### Ajuste de tamanho de batch

```python
# Batches maiores = operações vetorizadas mais rápidas
ds.map_batches(process_fn, batch_size=10000)  # vs batch_size=100
```

### Execução em streaming

```python
# Processar dados maiores que a memória
ds = ray.data.read_parquet("s3://huge-dataset/")
for batch in ds.iter_batches(batch_size=1000):
    process(batch)  # Feito em streaming, não carregado em memória
```

## Padrões comuns

### Inferência em lote

```python
import ray

# Carregar modelo
def load_model():
    # Carregar uma vez por worker
    return MyModel()

# Função de inferência
class BatchInference:
    def __init__(self):
        self.model = load_model()

    def __call__(self, batch):
        predictions = self.model(batch["input"])
        return {"prediction": predictions}

# Executar inferência distribuída
ds = ray.data.read_parquet("s3://data/")
predictions = ds.map_batches(BatchInference, batch_size=32, num_gpus=1)
predictions.write_parquet("s3://output/")
```

### Pipeline de pré-processamento de dados

```python
# Pipeline multi-etapa
ds = (
    ray.data.read_parquet("s3://raw/")
    .map_batches(clean_data)
    .map_batches(tokenize)
    .map_batches(augment)
    .write_parquet("s3://processed/")
)
```

## Integração com frameworks de ML

### PyTorch

```python
# Converter para PyTorch
torch_ds = ds.to_torch(label_column="label", batch_size=32)

for batch in torch_ds:
    # batch é dict com tensores
    inputs, labels = batch["features"], batch["label"]
```

### TensorFlow

```python
# Converter para TensorFlow
tf_ds = ds.to_tf(feature_columns=["image"], label_column="label", batch_size=32)

for features, labels in tf_ds:
    # Treinar modelo
    pass
```

## Formatos de dados suportados

| Formato | Leitura | Escrita | Caso de uso |
|---------|---------|---------|-------------|
| Parquet | ✅ | ✅ | Dados de ML (recomendado) |
| CSV | ✅ | ✅ | Dados tabulares |
| JSON | ✅ | ✅ | Semi-estruturado |
| Imagens | ✅ | ❌ | Visão computacional |
| NumPy | ✅ | ✅ | Arrays |
| Pandas | ✅ | ❌ | DataFrames |

## Benchmarks de performance

**Escala** (processando 100GB de dados):
- 1 nó (16 cores): ~30 minutos
- 4 nós (64 cores): ~8 minutos
- 16 nós (256 cores): ~2 minutos

**Aceleração com GPU** (pré-processamento de imagens):
- Apenas CPU: 1.000 imagens/seg
- 1 GPU: 5.000 imagens/seg
- 4 GPUs: 18.000 imagens/seg

## Casos de uso

**Implementações em produção**:
- **Pinterest**: Processamento de dados de última milha para treinamento de modelo
- **ByteDance**: Escalar inferência offline com LLMs multi-modal
- **Spotify**: Plataforma de ML para inferência em lote

## Referências

- **[Guia de Transformações](references/transformations.md)** - Operações map, filter, groupby
- **[Guia de Integração](references/integration.md)** - Ray Train, PyTorch, TensorFlow

## Recursos

- **Docs**: https://docs.ray.io/en/latest/data/data.html
- **GitHub**: https://github.com/ray-project/ray ⭐ 36.000+
- **Versão**: Ray 2.40.0+
- **Exemplos**: https://docs.ray.io/en/latest/data/examples/overview.html