---
name: get-available-resources
description: Esta skill deve ser usada no início de qualquer tarefa científica computacionalmente intensiva para detectar e relatar recursos disponíveis do sistema (núcleos de CPU, GPUs, memória, espaço em disco). Ela cria um arquivo JSON com informações de recursos e recomendações estratégicas que orientam decisões sobre abordagem computacional, como usar processamento paralelo (joblib, multiprocessing), computação fora da memória (Dask, Zarr), aceleração GPU (PyTorch, JAX) ou estratégias eficientes em memória. Use esta skill antes de executar análises, treinar modelos, processar grandes datasets ou qualquer tarefa onde restrições de recursos importem.
---

# Obter Recursos Disponíveis

## Visão Geral

Detecte recursos computacionais disponíveis e gere recomendações estratégicas para tarefas de computação científica. Esta skill identifica automaticamente capacidades de CPU, disponibilidade de GPU (NVIDIA CUDA, AMD ROCm, Apple Silicon Metal), restrições de memória e espaço em disco para ajudar na tomada de decisões informadas sobre abordagens computacionais.

## Quando Usar Esta Skill

Use esta skill proativamente antes de qualquer tarefa computacionalmente intensiva:

- **Antes de análise de dados**: Determine se datasets podem ser carregados em memória ou requerem processamento fora da memória
- **Antes do treinamento de modelos**: Verifique se aceleração GPU está disponível e qual backend usar
- **Antes de processamento paralelo**: Identifique número ótimo de workers para joblib, multiprocessing ou Dask
- **Antes de operações com arquivos grandes**: Verifique espaço em disco suficiente e estratégias de armazenamento apropriadas
- **Na inicialização do projeto**: Entenda capacidades iniciais para tomar decisões arquiteturais

**Cenários de exemplo:**
- "Ajude-me a analisar este dataset de genômica de 50GB" → Use esta skill primeiro para determinar se Dask/Zarr são necessários
- "Treinar uma rede neural com estes dados" → Use esta skill para detectar GPUs disponíveis e backends
- "Processar 10.000 arquivos em paralelo" → Use esta skill para determinar número ótimo de workers
- "Executar uma simulação computacionalmente intensiva" → Use esta skill para entender restrições de recursos

## Como Esta Skill Funciona

### Detecção de Recursos

A skill executa `scripts/detect_resources.py` para detectar automaticamente:

1. **Informações de CPU**
   - Contagem de núcleos físicos e lógicos
   - Arquitetura e modelo do processador
   - Informações de frequência da CPU

2. **Informações de GPU**
   - GPUs NVIDIA: Detecta via nvidia-smi, informa VRAM, versão do driver, capacidade de computação
   - GPUs AMD: Detecta via rocm-smi
   - Apple Silicon: Detecta chips M1/M2/M3/M4 com suporte Metal e memória unificada

3. **Informações de Memória**
   - RAM total e disponível
   - Percentual de uso de memória atual
   - Disponibilidade de espaço de troca

4. **Informações de Espaço em Disco**
   - Espaço total e disponível no diretório de trabalho
   - Percentual de uso atual

5. **Informações do Sistema Operacional**
   - Tipo de SO (macOS, Linux, Windows)
   - Versão e lançamento do SO
   - Versão do Python

### Formato de Saída

A skill gera um arquivo `.claude_resources.json` no diretório de trabalho atual contendo:

```json
{
  "timestamp": "2025-10-23T10:30:00",
  "os": {
    "system": "Darwin",
    "release": "25.0.0",
    "machine": "arm64"
  },
  "cpu": {
    "physical_cores": 8,
    "logical_cores": 8,
    "architecture": "arm64"
  },
  "memory": {
    "total_gb": 16.0,
    "available_gb": 8.5,
    "percent_used": 46.9
  },
  "disk": {
    "total_gb": 500.0,
    "available_gb": 200.0,
    "percent_used": 60.0
  },
  "gpu": {
    "nvidia_gpus": [],
    "amd_gpus": [],
    "apple_silicon": {
      "name": "Apple M2",
      "type": "Apple Silicon",
      "backend": "Metal",
      "unified_memory": true
    },
    "total_gpus": 1,
    "available_backends": ["Metal"]
  },
  "recommendations": {
    "parallel_processing": {
      "strategy": "high_parallelism",
      "suggested_workers": 6,
      "libraries": ["joblib", "multiprocessing", "dask"]
    },
    "memory_strategy": {
      "strategy": "moderate_memory",
      "libraries": ["dask", "zarr"],
      "note": "Consider chunking for datasets > 2GB"
    },
    "gpu_acceleration": {
      "available": true,
      "backends": ["Metal"],
      "suggested_libraries": ["pytorch-mps", "tensorflow-metal", "jax-metal"]
    },
    "large_data_handling": {
      "strategy": "disk_abundant",
      "note": "Sufficient space for large intermediate files"
    }
  }
}
```

### Recomendações Estratégicas

A skill gera recomendações sensíveis ao contexto:

**Recomendações de Processamento Paralelo:**
- **Alto paralelismo (8+ núcleos)**: Use Dask, joblib ou multiprocessing com workers = núcleos - 2
- **Paralelismo moderado (4-7 núcleos)**: Use joblib ou multiprocessing com workers = núcleos - 1
- **Sequencial (< 4 núcleos)**: Prefira processamento sequencial para evitar overhead

**Recomendações de Estratégia de Memória:**
- **Memória restrita (< 4GB disponível)**: Use Zarr, Dask ou H5py para processamento fora da memória
- **Memória moderada (4-16GB disponível)**: Use Dask/Zarr para datasets > 2GB
- **Memória abundante (> 16GB disponível)**: Pode carregar a maioria dos datasets em memória diretamente

**Recomendações de Aceleração GPU:**
- **GPUs NVIDIA detectadas**: Use PyTorch, TensorFlow, JAX, CuPy ou RAPIDS
- **GPUs AMD detectadas**: Use PyTorch-ROCm ou TensorFlow-ROCm
- **Apple Silicon detectado**: Use PyTorch com backend MPS, TensorFlow-Metal ou JAX-Metal
- **Nenhuma GPU detectada**: Use bibliotecas otimizadas para CPU

**Recomendações de Manipulação de Dados Grandes:**
- **Disco restrito (< 10GB)**: Use estratégias de streaming ou compressão
- **Disco moderado (10-100GB)**: Use formatos Zarr, H5py ou Parquet
- **Disco abundante (> 100GB)**: Pode criar livremente arquivos intermediários grandes

## Instruções de Uso

### Passo 1: Executar Detecção de Recursos

Execute o script de detecção no início de qualquer tarefa computacionalmente intensiva:

```bash
python scripts/detect_resources.py
```

Argumentos opcionais:
- `-o, --output <path>`: Especifique caminho de saída personalizado (padrão: `.claude_resources.json`)
- `-v, --verbose`: Imprima informações completas de recursos no stdout

### Passo 2: Ler e Aplicar Recomendações

Após executar a detecção, leia o arquivo `.claude_resources.json` gerado para informar decisões computacionais:

```python
# Exemplo: Usar recomendações no código
import json

with open('.claude_resources.json', 'r') as f:
    resources = json.load(f)

# Verificar estratégia de processamento paralelo
if resources['recommendations']['parallel_processing']['strategy'] == 'high_parallelism':
    n_jobs = resources['recommendations']['parallel_processing']['suggested_workers']
    # Use joblib, Dask ou multiprocessing com n_jobs workers

# Verificar estratégia de memória
if resources['recommendations']['memory_strategy']['strategy'] == 'memory_constrained':
    # Use Dask, Zarr ou H5py para processamento fora da memória
    import dask.array as da
    # Carregue dados em chunks

# Verificar disponibilidade de GPU
if resources['recommendations']['gpu_acceleration']['available']:
    backends = resources['recommendations']['gpu_acceleration']['backends']
    # Use biblioteca GPU apropriada baseado no backend disponível
```

### Passo 3: Tomar Decisões Informadas

Use as informações de recursos e recomendações para fazer escolhas estratégicas:

**Para carregamento de dados:**
```python
memory_available_gb = resources['memory']['available_gb']
dataset_size_gb = 10

if dataset_size_gb > memory_available_gb * 0.5:
    # Dataset é grande relativo à memória, use Dask
    import dask.dataframe as dd
    df = dd.read_csv('large_file.csv')
else:
    # Dataset cabe em memória, use pandas
    import pandas as pd
    df = pd.read_csv('large_file.csv')
```

**Para processamento paralelo:**
```python
from joblib import Parallel, delayed

n_jobs = resources['recommendations']['parallel_processing'].get('suggested_workers', 1)

results = Parallel(n_jobs=n_jobs)(
    delayed(process_function)(item) for item in data
)
```

**Para aceleração GPU:**
```python
import torch

if 'CUDA' in resources['gpu']['available_backends']:
    device = torch.device('cuda')
elif 'Metal' in resources['gpu']['available_backends']:
    device = torch.device('mps')
else:
    device = torch.device('cpu')

model = model.to(device)
```

## Dependências

O script de detecção requer os seguintes pacotes Python:

```bash
uv pip install psutil
```

Toda outra funcionalidade usa módulos da biblioteca padrão do Python (json, os, platform, subprocess, sys, pathlib).

## Suporte de Plataforma

- **macOS**: Suporte completo incluindo detecção de GPU Apple Silicon (M1/M2/M3/M4)
- **Linux**: Suporte completo incluindo detecção de GPU NVIDIA (nvidia-smi) e AMD (rocm-smi)
- **Windows**: Suporte completo incluindo detecção de GPU NVIDIA

## Melhores Práticas

1. **Executar cedo**: Execute a detecção de recursos no início de projetos ou antes de tarefas computacionais principais
2. **Re-executar periodicamente**: Recursos do sistema mudam ao longo do tempo (uso de memória, espaço em disco)
3. **Verificar antes de escalar**: Verifique recursos antes de escalar workers paralelos ou tamanhos de dados
4. **Documentar decisões**: Mantenha o arquivo `.claude_resources.json` em diretórios de projeto para documentar decisões conscientes de recursos
5. **Usar com versionamento**: Máquinas diferentes têm capacidades diferentes; arquivos de recursos ajudam a manter portabilidade

## Solução de Problemas

**GPU não detectada:**
- Garanta que drivers GPU estão instalados (nvidia-smi, rocm-smi ou system_profiler para Apple Silicon)
- Verifique que utilitários GPU estão no PATH do sistema
- Verifique que GPU não está sendo usada por outros processos

**Script falha ao executar:**
- Garanta que psutil está instalado: `uv pip install psutil`
- Verifique compatibilidade de versão Python (Python 3.6+)
- Verifique que script tem permissões de execução: `chmod +x scripts/detect_resources.py`

**Leituras de memória imprecisas:**
- Leituras de memória são snapshots; memória disponível atual muda constantemente
- Feche outras aplicações antes da detecção para leituras precisas de memória "disponível"
- Considere executar detecção múltiplas vezes e calcular média dos resultados