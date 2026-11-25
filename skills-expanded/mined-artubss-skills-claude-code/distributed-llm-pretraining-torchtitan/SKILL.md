---
name: distributed-llm-pretraining-torchtitan
description: Fornece treinamento distribuído de LLM nativo do PyTorch usando torchtitan com paralelismo 4D (FSDP2, TP, PP, CP). Use para fazer pré-treinamento de Llama 3.1, DeepSeek V3 ou modelos customizados em escala de 8 a 512+ GPUs com Float8, torch.compile e checkpoint distribuído.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Model Architecture, Distributed Training, TorchTitan, FSDP2, Tensor Parallel, Pipeline Parallel, Context Parallel, Float8, Llama, Pretraining]
dependencies: [torch>=2.6.0, torchtitan>=0.2.0, torchao>=0.5.0]
---

# TorchTitan - Pré-treinamento Distribuído de LLM Nativo do PyTorch

## Início rápido

TorchTitan é a plataforma oficial do PyTorch para pré-treinamento de LLM em larga escala com paralelismo 4D composável (FSDP2, TP, PP, CP), alcançando speedups de 65%+ em relação aos baselines em GPUs H100.

**Instalação**:
```bash
# Do PyPI (estável)
pip install torchtitan

# Do source (recursos mais recentes, requer PyTorch nightly)
git clone https://github.com/pytorch/torchtitan
cd torchtitan
pip install -r requirements.txt
```

**Baixe o tokenizer**:
```bash
# Obtenha token do HF em https://huggingface.co/settings/tokens
python scripts/download_hf_assets.py --repo_id meta-llama/Llama-3.1-8B --assets tokenizer --hf_token=...
```

**Inicie o treinamento em 8 GPUs**:
```bash
CONFIG_FILE="./torchtitan/models/llama3/train_configs/llama3_8b.toml" ./run_train.sh
```

## Workflows comuns

### Workflow 1: Pré-treinar Llama 3.1 8B em nó único

Copie este checklist:

```
Pré-treinamento em Nó Único:
- [ ] Passo 1: Baixar tokenizer
- [ ] Passo 2: Configurar treinamento
- [ ] Passo 3: Iniciar treinamento
- [ ] Passo 4: Monitorar e fazer checkpoint
```

**Passo 1: Baixar tokenizer**

```bash
python scripts/download_hf_assets.py \
  --repo_id meta-llama/Llama-3.1-8B \
  --assets tokenizer \
  --hf_token=YOUR_HF_TOKEN
```

**Passo 2: Configurar treinamento**

Edite ou crie um arquivo de configuração TOML:

```toml
# llama3_8b_custom.toml
[job]
dump_folder = "./outputs"
description = "Treinamento Llama 3.1 8B"

[model]
name = "llama3"
flavor = "8B"
hf_assets_path = "./assets/hf/Llama-3.1-8B"

[optimizer]
name = "AdamW"
lr = 3e-4

[lr_scheduler]
warmup_steps = 200

[training]
local_batch_size = 2
seq_len = 8192
max_norm = 1.0
steps = 1000
dataset = "c4"

[parallelism]
data_parallel_shard_degree = -1  # Usar todas as GPUs para FSDP

[activation_checkpoint]
mode = "selective"
selective_ac_option = "op"

[checkpoint]
enable = true
folder = "checkpoint"
interval = 500
```

**Passo 3: Iniciar treinamento**

```bash
# 8 GPUs em nó único
CONFIG_FILE="./llama3_8b_custom.toml" ./run_train.sh

# Ou explicitamente com torchrun
torchrun --nproc_per_node=8 \
  -m torchtitan.train \
  --job.config_file ./llama3_8b_custom.toml
```

**Passo 4: Monitorar e fazer checkpoint**

Logs do TensorBoard são salvos em `./outputs/tb/`:
```bash
tensorboard --logdir ./outputs/tb
```

### Workflow 2: Treinamento multi-nó com SLURM

```
Treinamento Multi-Nó:
- [ ] Passo 1: Configurar paralelismo para escala
- [ ] Passo 2: Configurar script SLURM
- [ ] Passo 3: Enviar job
- [ ] Passo 4: Retomar do checkpoint
```

**Passo 1: Configurar paralelismo para escala**

Para modelo de 70B em 256 GPUs (32 nós):
```toml
[parallelism]
data_parallel_shard_degree = 32  # FSDP em 32 ranks
tensor_parallel_degree = 8        # TP dentro do nó
pipeline_parallel_degree = 1      # Sem PP para 70B
context_parallel_degree = 1       # Aumentar para sequências longas
```

**Passo 2: Configurar script SLURM**

```bash
#!/bin/bash
#SBATCH --job-name=llama70b
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=8
#SBATCH --gpus-per-node=8

srun torchrun \
  --nnodes=32 \
  --nproc_per_node=8 \
  --rdzv_backend=c10d \
  --rdzv_endpoint=$MASTER_ADDR:$MASTER_PORT \
  -m torchtitan.train \
  --job.config_file ./llama3_70b.toml
```

**Passo 3: Enviar job**

```bash
sbatch multinode_trainer.slurm
```

**Passo 4: Retomar do checkpoint**

O treinamento retoma automaticamente se existir checkpoint na pasta configurada.

### Workflow 3: Ativar treinamento Float8 para H100s

Float8 oferece 30-50% de speedup em GPUs H100.

```
Treinamento Float8:
- [ ] Passo 1: Instalar torchao
- [ ] Passo 2: Configurar Float8
- [ ] Passo 3: Iniciar com compile
```

**Passo 1: Instalar torchao**

```bash
USE_CPP=0 pip install git+https://github.com/pytorch/ao.git
```

**Passo 2: Configurar Float8**

Adicione ao seu arquivo de configuração TOML:
```toml
[model]
converters = ["quantize.linear.float8"]

[quantize.linear.float8]
enable_fsdp_float8_all_gather = true
precompute_float8_dynamic_scale_for_fsdp = true
filter_fqns = ["output"]  # Excluir camada de saída

[compile]
enable = true
components = ["model", "loss"]
```

**Passo 3: Iniciar com compile**

```bash
CONFIG_FILE="./llama3_8b.toml" ./run_train.sh \
  --model.converters="quantize.linear.float8" \
  --quantize.linear.float8.enable_fsdp_float8_all_gather \
  --compile.enable
```

### Workflow 4: Paralelismo 4D para modelos 405B

```
Paralelismo 4D (FSDP + TP + PP + CP):
- [ ] Passo 1: Criar checkpoint seed
- [ ] Passo 2: Configurar paralelismo 4D
- [ ] Passo 3: Iniciar em 512 GPUs
```

**Passo 1: Criar checkpoint seed**

Necessário para inicialização consistente entre estágios de PP:
```bash
NGPU=1 CONFIG_FILE=./llama3_405b.toml ./run_train.sh \
  --checkpoint.enable \
  --checkpoint.create_seed_checkpoint \
  --parallelism.data_parallel_shard_degree 1 \
  --parallelism.tensor_parallel_degree 1 \
  --parallelism.pipeline_parallel_degree 1
```

**Passo 2: Configurar paralelismo 4D**

```toml
[parallelism]
data_parallel_shard_degree = 8   # FSDP
tensor_parallel_degree = 8       # TP dentro do nó
pipeline_parallel_degree = 8     # PP entre nós
context_parallel_degree = 1      # CP para sequências longas

[training]
local_batch_size = 32
seq_len = 8192
```

**Passo 3: Iniciar em 512 GPUs**

```bash
# 64 nós x 8 GPUs = 512 GPUs
srun torchrun --nnodes=64 --nproc_per_node=8 \
  -m torchtitan.train \
  --job.config_file ./llama3_405b.toml
```

## Quando usar vs alternativas

**Use TorchTitan quando:**
- Fazer pré-treinamento de LLMs do zero (8B a 405B+)
- Precisar de solução nativa do PyTorch sem dependências de terceiros
- Exigir paralelismo 4D composável (FSDP2, TP, PP, CP)
- Treinar em H100s com suporte Float8
- Querer checkpoints interoperáveis com torchtune/HuggingFace

**Use alternativas:**
- **Megatron-LM**: Desempenho máximo para deployments exclusivos de NVIDIA
- **DeepSpeed**: Ecossistema ZeRO mais amplo, suporte a inference
- **Axolotl/TRL**: Fine-tuning em vez de pré-treinamento
- **LitGPT**: Treinamento educacional em escala menor

## Problemas comuns

**Problema: Falta de memória em modelos grandes**

Ative checkpoint de ativação e reduza tamanho do batch:
```toml
[activation_checkpoint]
mode = "full"  # Em vez de "selective"

[training]
local_batch_size = 1
```

Ou use gradient accumulation:
```toml
[training]
local_batch_size = 1
global_batch_size = 32  # Acumula gradientes
```

**Problema: TP causa alta memória com async collectives**

Defina variável de ambiente:
```bash
export TORCH_NCCL_AVOID_RECORD_STREAMS=1
```

**Problema: Treinamento Float8 não é mais rápido**

Float8 só beneficia GEMMs grandes. Filtre camadas pequenas:
```toml
[quantize.linear.float8]
filter_fqns = ["attention.wk", "attention.wv", "output", "auto_filter_small_kn"]
```

**Problema: Falha ao carregar checkpoint após mudança de paralelismo**

Use capacidade de resharding do DCP:
```bash
# Converter checkpoint sharded em arquivo único
python -m torch.distributed.checkpoint.format_utils \
  dcp_to_torch checkpoint/step-1000 checkpoint.pt
```

**Problema: Inicialização de pipeline parallelism**

Crie checkpoint seed primeiro (ver Workflow 4, Passo 1).

## Modelos suportados

| Modelo | Tamanhos | Status |
|-------|----------|--------|
| Llama 3.1 | 8B, 70B, 405B | Produção |
| Llama 4 | Vários | Experimental |
| DeepSeek V3 | 16B, 236B, 671B (MoE) | Experimental |
| GPT-OSS | 20B, 120B (MoE) | Experimental |
| Qwen 3 | Vários | Experimental |
| Flux | Diffusion | Experimental |

## Benchmarks de desempenho (H100)

| Modelo | GPUs | Paralelismo | TPS/GPU | Técnicas |
|-------|------|-------------|---------|----------|
| Llama 8B | 8 | FSDP | 5.762 | Baseline |
| Llama 8B | 8 | FSDP+compile+FP8 | 8.532 | +48% |
| Llama 70B | 256 | FSDP+TP+AsyncTP | 876 | Paralelo 2D |
| Llama 405B | 512 | FSDP+TP+PP | 128 | Paralelo 3D |

## Tópicos avançados

**Configuração FSDP2**: Ver [references/fsdp.md](references/fsdp.md) para comparação detalhada FSDP2 vs FSDP1 e equivalentes ZeRO.

**Treinamento Float8**: Ver [references/float8.md](references/float8.md) para receitas de scaling tensorwise vs rowwise.

**Checkpointing**: Ver [references/checkpoint.md](references/checkpoint.md) para conversão HuggingFace e checkpointing async.

**Adicionar modelos customizados**: Ver [references/custom-models.md](references/custom-models.md) para protocolo TrainSpec.

## Recursos

- GitHub: https://github.com/pytorch/torchtitan
- Paper: https://arxiv.org/abs/2410.06511
- ICLR 2025: https://iclr.cc/virtual/2025/poster/29620
- PyTorch Forum: https://discuss.pytorch.org/c/distributed/torchtitan/44