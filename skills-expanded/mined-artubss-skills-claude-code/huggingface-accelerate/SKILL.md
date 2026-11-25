---
name: huggingface-accelerate
description: API de treinamento distribuído mais simples. 4 linhas para adicionar suporte distribuído a qualquer script PyTorch. API unificada para DeepSpeed/FSDP/Megatron/DDP. Posicionamento automático de device, precisão mista (FP16/BF16/FP8). Config interativo, comando de launch único. Padrão do ecossistema HuggingFace.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Distributed Training, HuggingFace, Accelerate, DeepSpeed, FSDP, Mixed Precision, PyTorch, DDP, Unified API, Simple]
dependencies: [accelerate, torch, transformers]
---

# HuggingFace Accelerate - Treinamento Distribuído Unificado

## Início rápido

Accelerate simplifica o treinamento distribuído em 4 linhas de código.

**Instalação**:
```bash
pip install accelerate
```

**Converter script PyTorch** (4 linhas):
```python
import torch
+ from accelerate import Accelerator

+ accelerator = Accelerator()

  model = torch.nn.Transformer()
  optimizer = torch.optim.Adam(model.parameters())
  dataloader = torch.utils.data.DataLoader(dataset)

+ model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)

  for batch in dataloader:
      optimizer.zero_grad()
      loss = model(batch)
-     loss.backward()
+     accelerator.backward(loss)
      optimizer.step()
```

**Executar** (comando único):
```bash
accelerate launch train.py
```

## Workflows comuns

### Workflow 1: De uma GPU para multi-GPU

**Script original**:
```python
# train.py
import torch

model = torch.nn.Linear(10, 2).to('cuda')
optimizer = torch.optim.Adam(model.parameters())
dataloader = torch.utils.data.DataLoader(dataset, batch_size=32)

for epoch in range(10):
    for batch in dataloader:
        batch = batch.to('cuda')
        optimizer.zero_grad()
        loss = model(batch).mean()
        loss.backward()
        optimizer.step()
```

**Com Accelerate** (4 linhas adicionadas):
```python
# train.py
import torch
from accelerate import Accelerator  # +1

accelerator = Accelerator()  # +2

model = torch.nn.Linear(10, 2)
optimizer = torch.optim.Adam(model.parameters())
dataloader = torch.utils.data.DataLoader(dataset, batch_size=32)

model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)  # +3

for epoch in range(10):
    for batch in dataloader:
        # Sem necessidade de .to('cuda') - automático!
        optimizer.zero_grad()
        loss = model(batch).mean()
        accelerator.backward(loss)  # +4
        optimizer.step()
```

**Configurar** (interativo):
```bash
accelerate config
```

**Perguntas**:
- Qual máquina? (single/multi GPU/TPU/CPU)
- Quantas máquinas? (1)
- Precisão mista? (no/fp16/bf16/fp8)
- DeepSpeed? (no/yes)

**Launch** (funciona em qualquer setup):
```bash
# Single GPU
accelerate launch train.py

# Multi-GPU (8 GPUs)
accelerate launch --multi_gpu --num_processes 8 train.py

# Multi-node
accelerate launch --multi_gpu --num_processes 16 \
  --num_machines 2 --machine_rank 0 \
  --main_process_ip $MASTER_ADDR \
  train.py
```

### Workflow 2: Treinamento com precisão mista

**Habilitar FP16/BF16**:
```python
from accelerate import Accelerator

# FP16 (com gradient scaling)
accelerator = Accelerator(mixed_precision='fp16')

# BF16 (sem scaling, mais estável)
accelerator = Accelerator(mixed_precision='bf16')

# FP8 (H100+)
accelerator = Accelerator(mixed_precision='fp8')

model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)

# Tudo mais é automático!
for batch in dataloader:
    with accelerator.autocast():  # Opcional, feito automaticamente
        loss = model(batch)
    accelerator.backward(loss)
```

### Workflow 3: Integração DeepSpeed ZeRO

**Habilitar DeepSpeed ZeRO-2**:
```python
from accelerate import Accelerator

accelerator = Accelerator(
    mixed_precision='bf16',
    deepspeed_plugin={
        "zero_stage": 2,  # ZeRO-2
        "offload_optimizer": False,
        "gradient_accumulation_steps": 4
    }
)

# Mesmo código de antes!
model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)
```

**Ou via config**:
```bash
accelerate config
# Selecione: DeepSpeed → ZeRO-2
```

**deepspeed_config.json**:
```json
{
    "fp16": {"enabled": false},
    "bf16": {"enabled": true},
    "zero_optimization": {
        "stage": 2,
        "offload_optimizer": {"device": "cpu"},
        "allgather_bucket_size": 5e8,
        "reduce_bucket_size": 5e8
    }
}
```

**Launch**:
```bash
accelerate launch --config_file deepspeed_config.json train.py
```

### Workflow 4: FSDP (Fully Sharded Data Parallel)

**Habilitar FSDP**:
```python
from accelerate import Accelerator, FullyShardedDataParallelPlugin

fsdp_plugin = FullyShardedDataParallelPlugin(
    sharding_strategy="FULL_SHARD",  # Equivalente a ZeRO-3
    auto_wrap_policy="TRANSFORMER_AUTO_WRAP",
    cpu_offload=False
)

accelerator = Accelerator(
    mixed_precision='bf16',
    fsdp_plugin=fsdp_plugin
)

model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)
```

**Ou via config**:
```bash
accelerate config
# Selecione: FSDP → Full Shard → No CPU Offload
```

### Workflow 5: Acumulação de gradientes

**Acumular gradientes**:
```python
from accelerate import Accelerator

accelerator = Accelerator(gradient_accumulation_steps=4)

model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)

for batch in dataloader:
    with accelerator.accumulate(model):  # Lida com acumulação
        optimizer.zero_grad()
        loss = model(batch)
        accelerator.backward(loss)
        optimizer.step()
```

**Tamanho efetivo de batch**: `batch_size * num_gpus * gradient_accumulation_steps`

## Quando usar vs alternativas

**Use Accelerate quando**:
- Quer o treinamento distribuído mais simples
- Precisa de um único script para qualquer hardware
- Usa o ecossistema HuggingFace
- Quer flexibilidade (DDP/DeepSpeed/FSDP/Megatron)
- Precisa de prototipagem rápida

**Principais vantagens**:
- **4 linhas**: Mudanças mínimas de código
- **API unificada**: Mesmo código para DDP, DeepSpeed, FSDP, Megatron
- **Automático**: Posicionamento de device, precisão mista, sharding
- **Config interativo**: Sem necessidade de setup manual de launcher
- **Launch único**: Funciona em qualquer lugar

**Use alternativas em vez disso**:
- **PyTorch Lightning**: Precisa de callbacks, abstrações de alto nível
- **Ray Train**: Orquestração multi-node, tuning de hiperparâmetros
- **DeepSpeed**: Controle direto de API, recursos avançados
- **DDP bruto**: Controle máximo, abstração mínima

## Problemas comuns

**Problema: Posicionamento errado de device**

Não mova manualmente para device:
```python
# ERRADO
batch = batch.to('cuda')

# CORRETO
# Accelerate lida automaticamente após prepare()
```

**Problema: Acumulação de gradientes não funciona**

Use context manager:
```python
# CORRETO
with accelerator.accumulate(model):
    optimizer.zero_grad()
    accelerator.backward(loss)
    optimizer.step()
```

**Problema: Checkpoint em distribuído**

Use métodos do accelerator:
```python
# Salve apenas no processo principal
if accelerator.is_main_process:
    accelerator.save_state('checkpoint/')

# Carregue em todos os processos
accelerator.load_state('checkpoint/')
```

**Problema: Resultados diferentes com FSDP**

Garanta a mesma seed aleatória:
```python
from accelerate.utils import set_seed
set_seed(42)
```

## Tópicos avançados

**Integração Megatron**: Veja [references/megatron-integration.md](references/megatron-integration.md) para tensor parallelism, pipeline parallelism e setup de sequence parallelism.

**Plugins customizados**: Veja [references/custom-plugins.md](references/custom-plugins.md) para criar plugins distribuídos customizados e configuração avançada.

**Tuning de performance**: Veja [references/performance.md](references/performance.md) para profiling, otimização de memória e melhores práticas.

## Requisitos de hardware

- **CPU**: Funciona (lento)
- **Single GPU**: Funciona
- **Multi-GPU**: DDP (padrão), DeepSpeed ou FSDP
- **Multi-node**: DDP, DeepSpeed, FSDP, Megatron
- **TPU**: Suportado
- **Apple MPS**: Suportado

**Requisitos de launcher**:
- **DDP**: `torch.distributed.run` (built-in)
- **DeepSpeed**: `deepspeed` (pip install deepspeed)
- **FSDP**: PyTorch 1.12+ (built-in)
- **Megatron**: Setup customizado

## Recursos

- Docs: https://huggingface.co/docs/accelerate
- GitHub: https://github.com/huggingface/accelerate
- Version: 1.11.0+
- Tutorial: "Accelerate your scripts"
- Examples: https://github.com/huggingface/accelerate/tree/main/examples
- Usado por: HuggingFace Transformers, TRL, PEFT, todas as bibliotecas HF