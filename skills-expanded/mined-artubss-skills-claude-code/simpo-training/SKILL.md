---
name: simpo-training
description: Simple Preference Optimization para alinhamento de LLMs. Alternativa sem modelo de referência ao DPO com melhor desempenho (+6.4 pontos no AlpacaEval 2.0). Sem modelo de referência necessário, mais eficiente que DPO. Use para alinhamento de preferências quando quer treinamento mais simples e rápido que DPO/PPO.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Post-Training, SimPO, Preference Optimization, Alignment, DPO Alternative, Reference-Free, LLM Alignment, Efficient Training]
dependencies: [torch, transformers, datasets, trl, accelerate]
---

# SimPO - Simple Preference Optimization

## Quick start

SimPO é um método de otimização de preferências sem modelo de referência que supera o DPO sem precisar de um modelo de referência.

**Instalação**:
```bash
# Create environment
conda create -n simpo python=3.10 && conda activate simpo

# Install PyTorch 2.2.2
# Visit: https://pytorch.org/get-started/locally/

# Install alignment-handbook
git clone https://github.com/huggingface/alignment-handbook.git
cd alignment-handbook
python -m pip install .

# Install Flash Attention 2
python -m pip install flash-attn --no-build-isolation
```

**Treinamento** (Mistral 7B):
```bash
ACCELERATE_LOG_LEVEL=info accelerate launch \
  --config_file accelerate_configs/deepspeed_zero3.yaml \
  scripts/run_simpo.py \
  training_configs/mistral-7b-base-simpo.yaml
```

## Workflows comuns

### Workflow 1: Treinar a partir de modelo base (Mistral 7B)

**Config** (`mistral-7b-base-simpo.yaml`):
```yaml
# Model
model_name_or_path: mistralai/Mistral-7B-v0.1
torch_dtype: bfloat16

# Dataset
dataset_mixer:
  HuggingFaceH4/ultrafeedback_binarized: 1.0
dataset_splits:
  - train_prefs
  - test_prefs

# SimPO hyperparameters
beta: 2.0                  # Reward scaling (2.0-10.0)
gamma_beta_ratio: 0.5       # Target margin (0-1)
loss_type: sigmoid          # sigmoid or hinge
sft_weight: 0.0             # Optional SFT regularization

# Training
learning_rate: 5e-7         # Critical: 3e-7 to 1e-6
num_train_epochs: 1
per_device_train_batch_size: 1
gradient_accumulation_steps: 8

# Output
output_dir: ./outputs/mistral-7b-simpo
```

**Iniciar treinamento**:
```bash
accelerate launch --config_file accelerate_configs/deepspeed_zero3.yaml \
  scripts/run_simpo.py training_configs/mistral-7b-base-simpo.yaml
```

### Workflow 2: Fine-tune de modelo instruct (Llama 3 8B)

**Config** (`llama3-8b-instruct-simpo.yaml`):
```yaml
model_name_or_path: meta-llama/Meta-Llama-3-8B-Instruct

dataset_mixer:
  argilla/ultrafeedback-binarized-preferences-cleaned: 1.0

beta: 2.5
gamma_beta_ratio: 0.5
learning_rate: 5e-7
sft_weight: 0.1             # Add SFT loss to preserve capabilities

num_train_epochs: 1
per_device_train_batch_size: 2
gradient_accumulation_steps: 4
output_dir: ./outputs/llama3-8b-simpo
```

**Iniciar**:
```bash
accelerate launch --config_file accelerate_configs/deepspeed_zero3.yaml \
  scripts/run_simpo.py training_configs/llama3-8b-instruct-simpo.yaml
```

### Workflow 3: Tarefas com raciocínio intensivo (LR mais baixo)

**Para tarefas de matemática/código**:
```yaml
model_name_or_path: deepseek-ai/deepseek-math-7b-base

dataset_mixer:
  argilla/distilabel-math-preference-dpo: 1.0

beta: 5.0                   # Higher for stronger signal
gamma_beta_ratio: 0.7       # Larger margin
learning_rate: 3e-7         # Lower LR for reasoning
sft_weight: 0.0

num_train_epochs: 1
per_device_train_batch_size: 1
gradient_accumulation_steps: 16
```

## Quando usar vs alternativas

**Use SimPO quando**:
- Quer treinamento mais simples que DPO (sem modelo de referência)
- Tem dados de preferência (pares escolhido/rejeitado)
- Precisa de melhor desempenho que DPO
- Recursos computacionais limitados
- Treinamento em nó único é suficiente

**Seleção de algoritmo**:
- **SimPO**: Mais simples, melhor desempenho, sem modelo de referência
- **DPO**: Precisa de baseline de modelo de referência, mais conservador
- **PPO**: Controle máximo, precisa de modelo de recompensa, setup complexo
- **GRPO**: RL eficiente em memória, sem critic

**Use alternativas em vez disso**:
- **OpenRLHF**: Treinamento distribuído multi-node, PPO/GRPO
- **TRL**: Precisa de múltiplos métodos em um framework
- **DPO**: Baseline de comparação estabelecido

## Problemas comuns

**Problema: Divergência de loss**

Reduza a taxa de aprendizado:
```yaml
learning_rate: 3e-7  # Reduce from 5e-7
```

Reduza beta:
```yaml
beta: 1.0  # Reduce from 2.0
```

**Problema: Modelo esquece capacidades**

Adicione regularização SFT:
```yaml
sft_weight: 0.1  # Add SFT loss component
```

**Problema: Separação de preferência ruim**

Aumente beta e margem:
```yaml
beta: 5.0            # Increase from 2.0
gamma_beta_ratio: 0.8  # Increase from 0.5
```

**Problema: OOM durante treinamento**

Reduza o tamanho do batch:
```yaml
per_device_train_batch_size: 1
gradient_accumulation_steps: 16  # Maintain effective batch
```

Habilite gradient checkpointing:
```yaml
gradient_checkpointing: true
```

## Tópicos avançados

**Funções de loss**: Veja [references/loss-functions.md](references/loss-functions.md) para sigmoid vs hinge loss, formulações matemáticas e quando usar cada uma.

**Ajuste de hiperparâmetros**: Veja [references/hyperparameters.md](references/hyperparameters.md) para guia de seleção de beta, gamma, taxa de aprendizado, e recomendações específicas por tamanho de modelo.

**Preparação de dataset**: Veja [references/datasets.md](references/datasets.md) para formatos de dados de preferência, filtragem de qualidade e criação de datasets customizados.

## Requisitos de hardware

- **GPU**: NVIDIA A100/H100 recomendado
- **VRAM**:
  - Modelo 7B: 1× A100 40GB (DeepSpeed ZeRO-3)
  - Modelo 8B: 2× A100 40GB
  - Modelo 70B: 8× A100 80GB
- **Single-node**: DeepSpeed ZeRO-3 é suficiente
- **Precisão mista**: BF16 recomendado

**Otimização de memória**:
- DeepSpeed ZeRO-3 (config padrão)
- Gradient checkpointing
- Flash Attention 2

## Recursos

- Paper: https://arxiv.org/abs/2405.14734 (NeurIPS 2024)
- GitHub: https://github.com/princeton-nlp/SimPO
- Models: https://huggingface.co/princeton-nlp
- Alignment Handbook: https://github.com/huggingface/alignment-handbook