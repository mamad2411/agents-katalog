---
name: training-llms-megatron
description: Treina modelos de linguagem grandes (2B-462B de parâmetros) usando NVIDIA Megatron-Core com estratégias avançadas de paralelismo. Use ao treinar modelos >1B de parâmetros, precisar de máxima eficiência de GPU (47% MFU em H100), ou necessitar de paralelismo tensor/pipeline/sequência/contexto/expert. Framework pronto para produção usado em Nemotron, LLaMA, DeepSeek.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Megatron-Core, Large-Scale Training, NVIDIA, Tensor Parallelism, Pipeline Parallelism, Model Parallelism, H100, Distributed Training, Production]
dependencies: [megatron-core, torch, apex, transformer-engine]
---

# Megatron-Core - Treinamento de LLMs em Larga Escala

## Início rápido

Megatron-Core treina LLMs de 2B a 462B de parâmetros com até 47% de Model FLOP Utilization em GPUs H100 através de estratégias avançadas de paralelismo.

**Instalação**:
```bash
# Docker (recomendado)
docker run --gpus all -it --rm nvcr.io/nvidia/pytorch:25.04-py3

# Ou pip
pip install megatron-core
```

**Treinamento distribuído simples**:
```bash
# Treinar com 2 GPUs usando data parallelism
torchrun --nproc_per_node=2 examples/run_simple_mcore_train_loop.py

# Ou treinamento LLaMA-3 8B
./examples/llama/train_llama3_8b_fp8.sh
```

## Fluxos de trabalho comuns

### Fluxo 1: Treinar modelo estilo LLaMA com paralelismo 3D

Copie esta lista de verificação:

```
Configuração de Treinamento LLaMA:
- [ ] Passo 1: Escolher configuração de paralelismo
- [ ] Passo 2: Configurar hiperparâmetros de treinamento
- [ ] Passo 3: Lançar treinamento distribuído
- [ ] Passo 4: Monitorar métricas de desempenho
```

**Passo 1: Escolher configuração de paralelismo**

O tamanho do modelo determina a estratégia de paralelismo:

| Tamanho do Modelo | GPUs | Tensor Parallel | Pipeline Parallel | Data Parallel | Context Parallel |
|------------------|------|-----------------|-------------------|---------------|------------------|
| 7B | 8 | 1 | 1 | 8 | 1 |
| 13B | 8 | 2 | 1 | 4 | 1 |
| 70B | 64 | 4 | 4 | 4 | 1 |
| 405B | 128 | 8 | 8 | 2 | 2 |

**Passo 2: Configurar hiperparâmetros de treinamento**

```bash
#!/bin/bash
# train_llama_70b.sh

GPUS_PER_NODE=8
NNODES=8  # 64 GPUs total
TP=4      # Tensor parallel
PP=4      # Pipeline parallel
CP=1      # Context parallel

# Configuração LLaMA 70B
MODEL_SIZE=70  # Billion parameters
HIDDEN_SIZE=8192
NUM_LAYERS=80
NUM_HEADS=64
SEQ_LENGTH=4096

# Hiperparâmetros de treinamento
MICRO_BATCH=1
GLOBAL_BATCH=1024
LR=3e-4

torchrun \
  --nproc_per_node=$GPUS_PER_NODE \
  --nnodes=$NNODES \
  pretrain_gpt.py \
  --tensor-model-parallel-size $TP \
  --pipeline-model-parallel-size $PP \
  --context-parallel-size $CP \
  --sequence-parallel \
  --num-layers $NUM_LAYERS \
  --hidden-size $HIDDEN_SIZE \
  --num-attention-heads $NUM_HEADS \
  --seq-length $SEQ_LENGTH \
  --max-position-embeddings $SEQ_LENGTH \
  --micro-batch-size $MICRO_BATCH \
  --global-batch-size $GLOBAL_BATCH \
  --lr $LR \
  --train-iters 100000 \
  --lr-decay-style cosine \
  --lr-warmup-iters 2000 \
  --weight-decay 0.1 \
  --clip-grad 1.0 \
  --bf16 \
  --use-mcore-models \
  --transformer-impl transformer_engine \
  --data-path /path/to/data \
  --vocab-file /path/to/vocab.json \
  --merge-file /path/to/merges.txt
```

**Passo 3: Lançar treinamento distribuído**

```bash
# Nó único (8 GPUs)
bash train_llama_70b.sh

# Multi-nó com SLURM
sbatch --nodes=8 --gpus-per-node=8 train_llama_70b.sh
```

**Passo 4: Monitorar métricas de desempenho**

Métricas-chave para acompanhar:
```
Model FLOP Utilization (MFU): Meta >40% em H100
Throughput: Tokens/seg/GPU
Uso de memória: <80GB por GPU para modelo 70B
Loss: Deve diminuir constantemente
```

### Fluxo 2: Configurar treinamento Mixture of Experts (MoE)

Para modelos MoE esparsos como Mixtral.

```
Treinamento MoE:
- [ ] Passo 1: Configurar expert parallelism
- [ ] Passo 2: Definir hiperparâmetros MoE
- [ ] Passo 3: Lançar treinamento com EP
```

**Passo 1: Configurar expert parallelism**

```bash
# Exemplo Mixtral 8x7B
TENSOR_PARALLEL=2
PIPELINE_PARALLEL=1
EXPERT_PARALLEL=4  # Dividir 8 experts entre 4 GPUs
DATA_PARALLEL=4

TOTAL_GPUS=$((TENSOR_PARALLEL * PIPELINE_PARALLEL * EXPERT_PARALLEL * DATA_PARALLEL))
# = 2 * 1 * 4 * 4 = 32 GPUs
```

**Passo 2: Definir hiperparâmetros MoE**

```bash
torchrun \
  --nproc_per_node=8 \
  pretrain_gpt.py \
  --tensor-model-parallel-size 2 \
  --pipeline-model-parallel-size 1 \
  --expert-model-parallel-size 4 \
  --num-experts 8 \
  --moe-router-topk 2 \
  --moe-router-load-balancing-type aux_loss \
  --moe-aux-loss-coeff 0.01 \
  --hidden-size 4096 \
  --num-layers 32 \
  --num-attention-heads 32 \
  --seq-length 4096 \
  --max-position-embeddings 4096 \
  --bf16 \
  --use-mcore-models \
  --transformer-impl transformer_engine \
  --data-path /path/to/data \
  --vocab-file /path/to/vocab.json \
  --merge-file /path/to/merges.txt
```

**Passo 3: Lançar treinamento com EP**

Expert parallelism distribui diferentes experts entre GPUs, reduzindo memória enquanto mantém a capacidade.

```
Memória sem EP: 8 experts × 7B = 56GB por GPU
Memória com EP=4: 2 experts × 7B = 14GB por GPU
Economia: redução de 75% em memória
```

### Fluxo 3: Otimizar para máximo throughput

Alcançar 47% MFU em H100.

```
Otimização de Desempenho:
- [ ] Passo 1: Habilitar Flash Attention
- [ ] Passo 2: Usar precisão FP8 (H100)
- [ ] Passo 3: Otimizar tamanho de micro-batch
- [ ] Passo 4: Ajustar graus de paralelismo
```

**Passo 1: Habilitar otimizações**

```bash
--use-mcore-models  # Usar modelos Megatron Core
--transformer-impl transformer_engine  # Usar Transformer Engine
--sequence-parallel  # Reduzir memória de ativações (usar com TP)
```

**Passo 2: Usar precisão FP8 (apenas H100)**

```bash
--fp8-hybrid  # Treinamento com precisão mista FP8
# Transformer Engine cuida de FP8 automaticamente
```

Resultado: aceleração de 1,5-2x em H100 vs BF16.

**Passo 3: Otimizar tamanho de micro-batch**

Encontre o maior micro-batch que cabe em memória:

```bash
# Começar com 1, aumentar até OOM
for MBS in 1 2 4 8; do
  echo "Testando micro-batch-size=$MBS"
  torchrun ... --micro-batch-size $MBS
done
```

Valores típicos:
- Modelo 7B: 4-8
- Modelo 70B: 1-2
- Modelo 405B: 1

**Passo 4: Ajustar graus de paralelismo**

Regras práticas:
```
Tensor Parallel: Usar ≤8 (limitado por NVLink dentro do nó)
Pipeline Parallel: Usar para >70B de modelos
Context Parallel: Usar para sequências >8K tokens
Data Parallel: Preencher GPUs restantes
```

Exemplo 405B em 128 H100s:
```
TP=8 (1 nó)
PP=8 (entre nós)
CP=2 (sequências longas)
DP=1
Total = 8 × 8 × 2 × 1 = 128 GPUs
```

## Quando usar vs alternativas

**Use Megatron-Core quando:**
- Treinar modelos >10B de parâmetros
- Precisa de máxima eficiência (alvo >40% MFU)
- Usando GPUs NVIDIA (A100, H100)
- Treinamento em produção em larga escala
- Quer controle fino sobre paralelismo

**Use alternativas em vez disso:**
- **PyTorch FSDP**: Modelos <70B, API mais simples, nativo do PyTorch
- **DeepSpeed**: Configuração mais fácil, bom para <100B de modelos
- **HuggingFace Accelerate**: Prototipagem, fluxos de trabalho mais simples
- **LitGPT**: Educacional, implementações em arquivo único

## Problemas comuns

**Problema: Baixa utilização de GPU (<30% MFU)**

Causas:
1. Micro-batch muito pequeno
2. Muita sobrecarga de paralelismo
3. Não usando Flash Attention

Correções:
```bash
# Aumentar micro-batch
--micro-batch-size 4  # Era 1

# Habilitar otimizações
--use-flash-attn
--sequence-parallel

# Reduzir TP se >8
--tensor-model-parallel-size 4  # Era 16
```

**Problema: Memória insuficiente**

Reduzir memória com:
```bash
--tensor-model-parallel-size 2  # Dividir modelo entre GPUs
--recompute-granularity full  # Gradient checkpointing
--recompute-method block  # Checkpoint de blocos transformer
--recompute-num-layers 1  # Checkpoint de cada camada
```

Ou usar offloading em CPU/NVMe:
```bash
--cpu-optimizer  # Offload do otimizador para CPU
--cpu-optimizer-type ADAM  # Variante Adam em CPU
```

**Problema: Treinamento mais lento do que esperado**

Verificar:
1. **Gargalo de rede**: Garantir InfiniBand/NVLink habilitado
2. **Pipeline bubbles**: Usar schedule de pipeline intercalado
   ```bash
   --num-layers-per-virtual-pipeline-stage 2
   ```
3. **Carregamento de dados**: Usar data loader rápido
   ```bash
   --dataloader-type cyclic
   ```

**Problema: Loss divergindo**

Estabilizar treinamento:
```bash
--lr-warmup-iters 2000  # Warmup mais longo
--clip-grad 1.0  # Gradient clipping
--init-method-std 0.006  # Inicialização menor
--attention-dropout 0.0  # Sem dropout em attention
--hidden-dropout 0.0  # Sem dropout em FFN
```

## Tópicos avançados

**Estratégias de paralelismo**: Veja [references/parallelism-guide.md](references/parallelism-guide.md) para comparação detalhada de TP/PP/DP/CP/EP com análise de desempenho e quando usar cada uma.

**Benchmarks de desempenho**: Veja [references/benchmarks.md](references/benchmarks.md) para números de MFU em diferentes tamanhos de modelo e configurações de GPU.

**Configurações para produção**: Veja [references/production-examples.md](references/production-examples.md) para setups do mundo real de LLaMA 3 405B, Nemotron-4 340B e DeepSeek-V3 671B.

**Receitas de treinamento**: Veja [references/training-recipes.md](references/training-recipes.md) para configurações completas de hiperparâmetros para arquiteturas GPT/LLaMA/Mixtral.

## Requisitos de hardware

- **GPU**: NVIDIA Ampere+ (A100, H100, B200)
  - Turing funciona mas mais lento
  - FP8 requer Hopper/Ada/Blackwell
- **Rede**: InfiniBand ou Ethernet 400Gb+ para multi-nó
- **Memória por GPU**:
  - Modelo 7B: 40GB+
  - Modelo 70B: 80GB (com TP=4)
  - Modelo 405B: 80GB (com TP=8, PP=8)
- **Armazenamento**: NVMe rápido para checkpoints (1TB+ para modelos 70B+)

## Recursos

- Docs: https://docs.nvidia.com/megatron-core/
- GitHub: https://github.com/NVIDIA/Megatron-LM
- Papers:
  - "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism" (2019)
  - "Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM" (2021)
- NeMo Framework: https://docs.nvidia.com/nemo-framework/ (construído sobre Megatron-Core)