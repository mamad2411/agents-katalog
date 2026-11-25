---
name: torchforge-rl-training
description: Fornece orientação para treinamento RL agentico nativo do PyTorch usando torchforge, biblioteca da Meta que separa infraestrutura de algoritmos. Use quando você quer abstrações limpas de RL, fácil experimentação de algoritmos, ou treinamento escalável com Monarch e TorchTitan.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Reinforcement Learning, PyTorch, GRPO, SFT, Monarch, TorchTitan, Meta]
dependencies: [torch>=2.9.0, torchtitan>=0.2.0, vllm, monarch]
---

# torchforge: Biblioteca RL Agentica Nativa do PyTorch

torchforge é a biblioteca RL nativa do PyTorch da Meta que separa infraestrutura de algoritmos. Permite pesquisa rápida em RL deixando você focar em algoritmos enquanto cuida do treinamento distribuído, inference e sincronização de pesos automaticamente.

## Quando Usar torchforge

**Escolha torchforge quando você precisa:**
- Separação limpa entre algoritmos RL e infraestrutura
- Abstrações nativas do PyTorch (sem dependência Ray)
- Fácil experimentação de algoritmos (GRPO, DAPO, SAPO em ~100 linhas)
- Treinamento escalável com sistema de atores Monarch
- Integração com TorchTitan para model parallelism

**Considere alternativas quando:**
- Você precisa de estabilidade pronta para produção → use **miles** ou **verl**
- Você quer treinamento nativo do Megatron → use **slime**
- torchforge é experimental e APIs podem mudar

## Funcionalidades Principais

- **Isolamento de algoritmo**: Implemente algoritmos RL sem tocar infraestrutura
- **Escalabilidade**: De GPU única para milhares via Monarch
- **Stack moderno**: TorchTitan (treinamento), vLLM (inference), TorchStore (sincronização)
- **Funções de perda**: GRPO, DAPO, CISPO, GSPO, SAPO embutidas

## Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│ Application Layer (Your Code)                           │
│ - Define reward models, loss functions, sampling        │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│ Forge API Layer                                         │
│ - Episode, Group dataclasses                           │
│ - Service interfaces (async/await)                      │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│ Distributed Services (Monarch)                          │
│ ├── Trainer (TorchTitan FSDP)                          │
│ ├── Generator (vLLM inference)                          │
│ ├── Reference Model (frozen KL baseline)               │
│ └── Reward Actors (compute rewards)                    │
└─────────────────────────────────────────────────────────┘
```

## Instalação

```bash
# Create environment
conda create -n forge python=3.12
conda activate forge

# Install (handles PyTorch nightly + dependencies)
./scripts/install.sh

# Verify
python -c "import torch, forge, vllm; print('OK')"
```

### Instalação ROCm

```bash
./scripts/install_rocm.sh
```

## Início Rápido

### Treinamento SFT (2+ GPUs)

```bash
python -m apps.sft.main --config apps/sft/llama3_8b.yaml
```

### Treinamento GRPO (3+ GPUs)

```bash
python -m apps.grpo.main --config apps/grpo/qwen3_1_7b.yaml
```

---

## Workflow 1: Treinamento GRPO para Raciocínio Matemático

Use este workflow para treinar modelos de raciocínio com vantagens relativas ao grupo.

### Checklist de Pré-requisitos
- [ ] 3+ GPUs (GPU0: trainer, GPU1: ref_model, GPU2: generator)
- [ ] Modelo do HuggingFace Hub
- [ ] Dataset de treinamento (GSM8K, MATH, etc.)

### Passo 1: Criar Configuração

```yaml
# config/grpo_math.yaml
model: "Qwen/Qwen2.5-7B-Instruct"

dataset:
  path: "openai/gsm8k"
  split: "train"
  streaming: true

training:
  batch_size: 4
  learning_rate: 1e-6
  seq_len: 4096
  dtype: bfloat16
  gradient_accumulation_steps: 4

grpo:
  n_samples: 8           # Responses per prompt
  clip_low: 0.2
  clip_high: 0.28
  beta: 0.1              # KL penalty coefficient
  temperature: 0.7

services:
  generator:
    procs: 1
    num_replicas: 1
    with_gpus: true
  trainer:
    procs: 1
    num_replicas: 1
    with_gpus: true
  ref_model:
    procs: 1
    num_replicas: 1
    with_gpus: true
```

### Passo 2: Definir Função de Recompensa

```python
# rewards.py
# Reward functions are in forge.data.rewards
from forge.data.rewards import MathReward, ThinkingReward
import re

# Or define your own reward function
class CustomMathReward:
    def __call__(self, prompt: str, response: str, target: str) -> float:
        # Extract answer from response
        match = re.search(r'\\boxed{([^}]+)}', response)
        if not match:
            return 0.0

        answer = match.group(1).strip()
        return 1.0 if answer == target else 0.0
```

### Passo 3: Iniciar Treinamento

```bash
python -m apps.grpo.main --config config/grpo_math.yaml
```

### Passo 4: Monitorar Progresso
- [ ] Verificar dashboard W&B para curvas de perda
- [ ] Verificar que entropia está diminuindo (política ficando mais determinística)
- [ ] Monitorar divergência KL (deve permanecer limitada)

---

## Workflow 2: Função de Perda Customizada

Use este workflow para implementar novos algoritmos RL.

### Passo 1: Criar Classe de Perda

```python
# src/forge/losses/custom_loss.py
import torch
import torch.nn as nn

class CustomLoss(nn.Module):
    def __init__(self, clip_range: float = 0.2, beta: float = 0.1):
        super().__init__()
        self.clip_range = clip_range
        self.beta = beta

    def forward(
        self,
        logprobs: torch.Tensor,
        ref_logprobs: torch.Tensor,
        advantages: torch.Tensor,
        padding_mask: torch.Tensor,
    ) -> torch.Tensor:
        # Compute importance ratio
        ratio = torch.exp(logprobs - ref_logprobs)

        # Clipped policy gradient
        clipped_ratio = torch.clamp(
            ratio,
            1 - self.clip_range,
            1 + self.clip_range
        )
        pg_loss = -torch.min(ratio * advantages, clipped_ratio * advantages)

        # KL penalty
        kl = ref_logprobs - logprobs

        # Apply mask and aggregate
        masked_loss = (pg_loss + self.beta * kl) * padding_mask
        loss = masked_loss.sum() / padding_mask.sum()

        return loss
```

### Passo 2: Integrar na Aplicação

```python
# apps/custom/main.py
from forge.losses.custom_loss import CustomLoss

loss_fn = CustomLoss(clip_range=0.2, beta=0.1)

# In training loop
loss = loss_fn(
    logprobs=logprobs,
    ref_logprobs=ref_logprobs,
    advantages=advantages,
    padding_mask=padding_mask,
)
```

---

## Workflow 3: Treinamento Distribuído Multi-GPU

Use este workflow para escalar para múltiplas GPUs ou nós.

### Configuração para Distribuído

```yaml
# config/distributed.yaml
model: "meta-llama/Meta-Llama-3.1-8B-Instruct"

parallelism:
  tensor_parallel_degree: 2    # Split model across GPUs
  pipeline_parallel_degree: 1
  data_parallel_shard_degree: 2

services:
  generator:
    procs: 2                   # 2 processes for TP=2
    num_replicas: 1
    with_gpus: true
  trainer:
    procs: 2
    num_replicas: 1
    with_gpus: true
```

### Lançar com SLURM

```bash
# Submit job
sbatch --nodes=2 --gpus-per-node=8 run_grpo.sh
```

### Lançar Localmente (Multi-GPU)

```bash
# 8 GPU setup
python -m apps.grpo.main \
    --config config/distributed.yaml \
    --trainer.procs 4 \
    --generator.procs 4
```

---

## Referência da API Principal

### Formato de Batch de Treinamento

torchforge usa batches baseados em dicionário para treinamento:

```python
# inputs: list of dicts with torch.Tensor values
inputs = [{"tokens": torch.Tensor}]

# targets: list of dicts with training signals
targets = [{
    "response": torch.Tensor,
    "ref_logprobs": torch.Tensor,
    "advantages": torch.Tensor,
    "padding_mask": torch.Tensor
}]

# train_step returns loss as float
loss = trainer.train_step(inputs, targets)
```

### Completion

Saída gerada do vLLM:

```python
@dataclass
class Completion:
    text: str              # Generated text
    token_ids: list[int]   # Token IDs
    logprobs: list[float]  # Log probabilities
    metadata: dict         # Custom metadata
```

---

## Funções de Perda Embutidas

### Funções de Perda

Funções de perda estão no módulo `forge.losses`:

```python
from forge.losses import SimpleGRPOLoss, ReinforceLoss

# SimpleGRPOLoss for GRPO training
loss_fn = SimpleGRPOLoss(beta=0.1)

# Forward pass
loss = loss_fn(
    logprobs=logprobs,
    ref_logprobs=ref_logprobs,
    advantages=advantages,
    padding_mask=padding_mask
)
```

### ReinforceLoss

```python
from forge.losses.reinforce_loss import ReinforceLoss

# With optional importance ratio clipping
loss_fn = ReinforceLoss(clip_ratio=0.2)
```

---

## Problemas Comuns e Soluções

### Problema: GPUs Insuficientes

**Sintomas**: Erro "Insufficient GPU resources"

**Soluções**:
```yaml
# Reduce service requirements
services:
  generator:
    procs: 1
    with_gpus: true
  trainer:
    procs: 1
    with_gpus: true
  # Remove ref_model (uses generator weights)
```

Ou use CPU para modelo de referência:
```yaml
ref_model:
  with_gpus: false
```

### Problema: OOM Durante Geração

**Sintomas**: CUDA OOM no vLLM

**Soluções**:
```yaml
# Reduce batch size
grpo:
  n_samples: 4  # Reduce from 8

# Or reduce sequence length
training:
  seq_len: 2048
```

### Problema: Sincronização de Pesos Lenta

**Sintomas**: Pausas longas entre treinamento e geração

**Soluções**:
```bash
# Enable RDMA (if available)
export TORCHSTORE_USE_RDMA=1

# Or reduce sync frequency
training:
  sync_interval: 10  # Sync every 10 steps
```

### Problema: Colapso de Política

**Sintomas**: Entropia cai para zero, recompensa para de melhorar

**Soluções**:
```yaml
# Increase KL penalty
grpo:
  beta: 0.2  # Increase from 0.1

# Or add entropy bonus
training:
  entropy_coef: 0.01
```

---

## Recursos

- **Documentation**: https://meta-pytorch.org/torchforge
- **GitHub**: https://github.com/meta-pytorch/torchforge
- **Discord**: https://discord.gg/YsTYBh6PD9
- **TorchTitan**: https://github.com/pytorch/torchtitan
- **Monarch**: https://github.com/meta-pytorch/monarch