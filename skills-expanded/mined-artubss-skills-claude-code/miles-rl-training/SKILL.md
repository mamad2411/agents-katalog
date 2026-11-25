---
name: miles-rl-training
description: Fornece orientação para treinamento RL de nível empresarial usando miles, um fork pronto para produção do slime. Use ao treinar grandes modelos MoE com FP8/INT4, necessitando alinhamento treino-inferência ou exigindo RL especulativo para máxima taxa de transferência.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Reinforcement Learning, MoE, FP8, INT4, Enterprise, SGLang, Megatron-LM]
dependencies: [sglang-router>=0.2.3, ray, torch>=2.0.0, transformers>=4.40.0]
---

# miles: RL de Nível Empresarial para Treinamento de Modelos em Larga Escala

miles é um framework RL de alto desempenho, pronto para produção, otimizado para pós-treinamento de modelos em larga escala. Construído como um fork de produção do slime, ele aborda desafios críticos na estabilidade do treinamento MoE, treinamento em baixa precisão e alinhamento treino-inferência.

## Quando Usar miles

**Escolha miles quando você precisa de:**
- Treinamento de modelos MoE com 1TB+ (DeepSeek V3, Qwen3-MoE)
- Treinamento com quantização em FP8 ou INT4
- Alinhamento treino-inferência bit-wise idêntico
- RL especulativo para máxima taxa de transferência
- Estabilidade em produção com suporte empresarial

**Considere alternativas quando:**
- Você quer o original de pesquisa → use **slime**
- Você precisa de troca de backend flexível → use **verl**
- Você quer abstrações nativas do PyTorch → use **torchforge**

## Características Principais

### Treinamento em Baixa Precisão
- **FP8 Unificado**: FP8 de ponta a ponta para inferência e treinamento
- **INT4 QAT**: Modelos de 1TB em VRAM de máquina única (H200)
- **Rollout Routing Replay (R3)**: Alinhamento de experts bit-wise para MoE

### Otimizações de Desempenho
- **RL Especulativo**: Aceleração de rollout de 25%+ com modelos draft SFT online
- **Sincronização de Peso Zero-Copy**: Mapeamento zero-copy IPC CUDA
- **Rollout Parcial**: Reciclagem de trajetórias semi-completas

### Alinhamento Treino-Inferência
- **TIS/MIS**: Importance Sampling Truncado/Mascarado para correção off-policy
- **Otimização em nível de kernel**: Integração FlashAttention-3, DeepGEMM

## Instalação

```bash
# Recomendado: Docker
docker pull radixark/miles:latest
docker run --rm --gpus all --ipc=host --shm-size=16g \
  -it radixark/miles:latest /bin/bash

# A partir do código-fonte
git clone https://github.com/radixark/miles.git
cd miles
pip install -r requirements.txt
pip install -e .
```

## Início Rápido

miles herda o sistema de configuração do slime. Treinamento básico:

```bash
python train.py \
    --advantage-estimator grpo \
    --model-name qwen3-30b-a3b \
    --hf-checkpoint /path/to/qwen3-30b-a3b-hf \
    --rollout-batch-size 512 \
    --n-samples-per-prompt 8
```

---

## Workflow 1: Treinamento MoE em Larga Escala

Use este workflow para treinar grandes modelos MoE como DeepSeek V3 ou Qwen3-MoE.

### Checklist de Pré-requisitos
- [ ] GPUs H100/H200 com suporte a FP8
- [ ] Modelo MoE (DeepSeek V3, Qwen3-MoE)
- [ ] Ambiente Docker com miles

### Passo 1: Configuração do Ambiente

```bash
# Escalamento de bloco FP8 (recomendado para estabilidade)
export NVTE_FP8_BLOCK_SCALING_FP32_SCALES=1
export CUDA_DEVICE_MAX_CONNECTIONS=1
```

### Passo 2: Configurar Treinamento

```bash
python train.py \
    --actor-num-gpus-per-node 8 \
    --rollout-num-gpus 8 \
    --hf-checkpoint /path/to/deepseek-v3 \
    --advantage-estimator grpo \
    --tensor-model-parallel-size 8 \
    --expert-model-parallel-size 4 \
    --prompt-data /path/to/data.jsonl \
    --num-rollout 3000
```

### Checklist de Verificação
- [ ] Modelo carrega sem erros
- [ ] Decisões de roteamento são consistentes
- [ ] Sem valores NaN/Inf nas perdas

---

## Workflow 2: Treinamento RL Especulativo

Use este workflow para máxima taxa de transferência de rollout com decodificação especulativa EAGLE.

### Como Funciona RL Especulativo

1. Modelo draft pequeno gera tokens candidatos
2. Modelo alvo verifica em paralelo
3. Modelo draft atualizado via SFT online para rastrear a política

### Passo 1: Habilitar Decodificação Especulativa

miles suporta decodificação especulativa EAGLE via SGLang:

```bash
python train.py \
    --actor-num-gpus-per-node 8 \
    --hf-checkpoint /path/to/target-model \
    --sglang-speculative-algorithm EAGLE \
    --sglang-speculative-num-steps 3 \
    --sglang-speculative-eagle-topk 1 \
    --sglang-speculative-num-draft-tokens 4 \
    --sglang-speculative-draft-model-path /path/to/draft-model \
    --advantage-estimator grpo \
    --prompt-data /path/to/data.jsonl
```

### Passo 2: Habilitar Treinamento Online MTP (Opcional)

Para SFT online do modelo draft durante o treinamento:

```bash
--mtp-num-layers 1 \
--enable-mtp-training \
--mtp-loss-scaling-factor 0.2
```

**Nota**: Treinamento MTP online requer um checkpoint de distribuição torch com pesos MTP. Adicione `--mtp-num-layers 1` durante a conversão do checkpoint de HuggingFace.

### Aceleração Esperada

- **Rollout padrão**: Linha de base
- **RL Especulativo**: Rollout 25-40% mais rápido
- **Com rollout parcial**: Taxa de transferência adicional de 10-15%

---

## Referência de Configuração

miles herda todos os argumentos do slime. Veja [Referência da API do slime](../slime/references/api-reference.md) para a lista completa.

### Recursos de Cluster (do slime)

```bash
--actor-num-nodes 1
--actor-num-gpus-per-node 8
--rollout-num-gpus 8
--rollout-num-gpus-per-engine 2
--colocate
```

### Paralelismo Megatron (do slime)

```bash
--tensor-model-parallel-size 8
--pipeline-model-parallel-size 2
--expert-model-parallel-size 4    # Paralelismo de experts MoE
```

### Decodificação Especulativa (específico do miles)

```bash
--sglang-speculative-algorithm EAGLE
--sglang-speculative-num-steps 3
--sglang-speculative-eagle-topk 1
--sglang-speculative-num-draft-tokens 4
--sglang-enable-draft-weights-cpu-backup
--sglang-speculative-draft-model-path /your/draft/model/path
```

### Treinamento MTP Online (específico do miles)

```bash
--mtp-num-layers 1
--enable-mtp-training
--mtp-loss-scaling-factor 0.2
```

---

## Características Principais (Conceituais)

As seguintes características são documentadas no miles, mas flags CLI específicas podem variar. Consulte o repositório miles para a configuração mais recente.

### Pipeline FP8 Unificado

Amostragem FP8 de ponta a ponta e treinamento que elimina discrepância induzida por quantização causando colapso RL em modelos MoE.

### Rollout Routing Replay (R3)

Registra decisões de roteamento de experts durante inferência SGLang e as reproduz durante treinamento Megatron para alinhamento bit-wise de experts.

**Como R3 Funciona**:
1. Durante inferência SGLang, decisões de roteamento de experts são registradas
2. Decisões de roteamento armazenadas em `sample.rollout_routed_experts`
3. Durante treinamento Megatron, o roteamento é reproduzido em vez de recomputado
4. Garante seleção idêntica de experts entre treino e inferência

### Treinamento com Quantização INT4

Permite implantação em máquina única de modelos com 1TB+ (ex: em H200).

**Economias de Memória com INT4**:

| Tamanho do Modelo | VRAM BF16 | VRAM INT4 | Redução |
|-------------------|-----------|-----------|----------|
| 70B | 140GB | 45GB | 3.1x |
| 235B | 470GB | 150GB | 3.1x |
| 671B | 1.3TB | 420GB | 3.1x |

### Alinhamento Treino-Inferência

miles alcança "divergência KL exatamente 0" entre treinamento e inferência por meio de:
- Flash Attention 3
- DeepGEMM
- Kernels invariantes a lote do Thinking Machines Lab
- Integração `torch.compile`

---

## Estrutura de Dados de Exemplo

miles usa a mesma dataclass `Sample` do slime com o campo `rollout_routed_experts` para reprodução de roteamento MoE:

```python
@dataclass
class Sample:
    prompt: str | list[dict]
    tokens: list[int]
    response: str
    reward: float | dict
    loss_mask: list[int]
    status: Status
    metadata: dict
    rollout_log_probs: list[float]
    rollout_routed_experts: list[list[int]]  # Roteamento MoE para R3
```

Veja [Referência da API do slime](../slime/references/api-reference.md) para a definição completa de Sample.

---

## Problemas Comuns e Soluções

### Problema: Colapso de Treinamento FP8

**Sintomas**: Perda explode, valores NaN

**Soluções**:
- Use escalamento de bloco: `export NVTE_FP8_BLOCK_SCALING_FP32_SCALES=1`
- Reduza a taxa de aprendizado: `--lr 5e-7`
- Garanta que o roteamento MoE seja consistente entre treino/inferência

### Problema: Desvio Especulativo de Draft

**Sintomas**: Baixa taxa de aceitação ao longo do tempo

**Soluções**:
- Habilite treinamento MTP online para manter modelo draft alinhado
- Reduza passos especulativos: `--sglang-speculative-num-steps 2`
- Use backup em CPU: `--sglang-enable-draft-weights-cpu-backup`

### Problema: Incompatibilidade Treino-Inferência

**Sintomas**: Divergência de política, colapso de recompensa

**Soluções**:
- Use TIS para correção off-policy: `--use-tis --tis-threshold 0.9`
- Verifique se log probs correspondem entre SGLang e Megatron
- Habilite R3 para modelos MoE

---

## Modelos Suportados

| Família | Modelos | Suporte MoE |
|---------|---------|------------|
| DeepSeek | R1, V3, V3.2 | Completo |
| Qwen | 2, 2.5, 3 (incluindo MoE) | Completo |
| Llama | 3, 3.1, 3.3, 4 | Apenas denso |
| Gemma | 2, 3, 3N | Apenas denso |
| GLM | 4.5, 4.6, 4.7 | Apenas denso |
| MiniMax | M2, M2.1 | Completo |

---

## Recursos

- **GitHub**: https://github.com/radixark/miles
- **Blog de Introdução**: https://lmsys.org/blog/2025-11-19-miles/
- **Slime (upstream)**: https://github.com/THUDM/slime
- **SGLang**: https://github.com/sgl-project/sglang