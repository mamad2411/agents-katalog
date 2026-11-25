---
name: slime-rl-training
description: Fornece orientação para pós-treinamento de LLM com RL usando slime, um framework Megatron+SGLang. Use ao treinar modelos GLM, implementar fluxos de trabalho personalizados de geração de dados, ou precisar de integração estreita com Megatron-LM para escalabilidade em RL.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Reinforcement Learning, Megatron-LM, SGLang, GRPO, Post-Training, GLM]
dependencies: [sglang-router>=0.2.3, ray, torch>=2.0.0, transformers>=4.40.0]
---

# slime: Framework de Pós-Treinamento de LLM para Escalabilidade em RL

slime é um framework de pós-treinamento de LLM do time THUDM de Tsinghua, potencializando GLM-4.5, GLM-4.6 e GLM-4.7. Conecta Megatron-LM para treinamento com SGLang para geração de rollout de alta taxa de transferência.

## Quando Usar slime

**Escolha slime quando você precisar:**
- Treinamento nativo com Megatron-LM e inferência com SGLang
- Fluxos de trabalho de geração de dados personalizados com buffers flexíveis
- Treinar modelos GLM, Qwen3, DeepSeek V3, ou Llama 3
- Framework de pesquisa com respaldo em produção (Z.ai)

**Considere alternativas quando:**
- Você precisar de recursos de estabilidade de nível empresarial → use **miles**
- Você quiser troca flexível de backend → use **verl**
- Você precisar de abstrações nativas do PyTorch → use **torchforge**

## Características-Chave

- **Treinamento**: Megatron-LM com suporte completo de paralelismo (TP, PP, DP, SP)
- **Rollout**: Geração de alta taxa de transferência baseada em SGLang com router
- **Buffer de Dados**: Gerenciamento flexível de prompts e armazenamento de amostras
- **Modelos**: GLM-4.x, Qwen3, DeepSeek V3/R1, Llama 3

## Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    Data Buffer                          │
│ - Prompt initialization and management                  │
│ - Custom data generation and filtering                  │
│ - Rollout sample storage                                │
└─────────────┬───────────────────────────┬───────────────┘
              │                           │
┌─────────────▼───────────┐ ┌─────────────▼───────────────┐
│ Training (Megatron-LM)  │ │ Rollout (SGLang + Router)   │
│ - Actor model training  │ │ - Response generation       │
│ - Critic (optional)     │ │ - Reward/verifier output    │
│ - Weight sync to rollout│ │ - Multi-turn support        │
└─────────────────────────┘ └─────────────────────────────┘
```

## Instalação

```bash
# Recomendado: Docker
docker pull slimerl/slime:latest
docker run --rm --gpus all --ipc=host --shm-size=16g \
  -it slimerl/slime:latest /bin/bash

# Dentro do container
cd /root/slime && pip install -e . --no-deps
```

### Do Código-Fonte

```bash
git clone https://github.com/THUDM/slime.git
cd slime
pip install -r requirements.txt
pip install -e .
```

## Início Rápido: Treinamento GRPO

```bash
# Configuração do modelo de origem
source scripts/models/qwen3-4B.sh

# Iniciar treinamento
python train.py \
    --actor-num-nodes 1 \
    --actor-num-gpus-per-node 4 \
    --rollout-num-gpus 4 \
    --advantage-estimator grpo \
    --use-kl-loss --kl-loss-coef 0.001 \
    --rollout-batch-size 32 \
    --n-samples-per-prompt 8 \
    --global-batch-size 256 \
    --num-rollout 3000 \
    --prompt-data /path/to/data.jsonl \
    ${MODEL_ARGS[@]} ${CKPT_ARGS[@]}
```

---

## Fluxo de Trabalho 1: Treinamento GRPO Padrão

Use este fluxo de trabalho para treinar modelos de raciocínio com vantagens relativas a grupos.

### Checklist de Pré-Requisitos
- [ ] Ambiente Docker ou Megatron-LM + SGLang instalados
- [ ] Checkpoint do modelo (formato HuggingFace ou Megatron)
- [ ] Dados de treinamento em formato JSONL

### Passo 1: Preparar Dados

```python
# Formato data.jsonl
{"prompt": "What is 2 + 2?", "label": "4"}
{"prompt": "Solve: 3x = 12", "label": "x = 4"}
```

Ou com formato de chat:
```python
{
    "prompt": [
        {"role": "system", "content": "You are a math tutor."},
        {"role": "user", "content": "What is 15 + 27?"}
    ],
    "label": "42"
}
```

### Passo 2: Configurar Modelo

Escolha um script de modelo pré-configurado:

```bash
# Listar modelos disponíveis
ls scripts/models/
# glm4-9B.sh, qwen3-4B.sh, qwen3-30B-A3B.sh, deepseek-v3.sh, llama3-8B.sh, ...

# Carregar seu modelo
source scripts/models/qwen3-4B.sh
```

### Passo 3: Iniciar Treinamento

```bash
python train.py \
    --actor-num-nodes 1 \
    --actor-num-gpus-per-node 8 \
    --rollout-num-gpus 8 \
    --advantage-estimator grpo \
    --use-kl-loss \
    --kl-loss-coef 0.001 \
    --prompt-data /path/to/train.jsonl \
    --input-key prompt \
    --label-key label \
    --apply-chat-template \
    --rollout-batch-size 32 \
    --n-samples-per-prompt 8 \
    --global-batch-size 256 \
    --num-rollout 3000 \
    --save-interval 100 \
    --eval-interval 50 \
    ${MODEL_ARGS[@]}
```

### Passo 4: Monitorar Treinamento
- [ ] Verificar TensorBoard: `tensorboard --logdir outputs/`
- [ ] Verificar se as curvas de recompensa estão aumentando
- [ ] Monitorar utilização de GPU entre nós

---

## Fluxo de Trabalho 2: Treinamento Assíncrono

Use modo assíncrono para maior taxa de transferência sobrepondo rollout e treinamento.

### Quando Usar Assíncrono
- Modelos grandes com longos tempos de geração
- Alto tempo ocioso de GPU em modo síncrono
- Memória suficiente para buffering

### Iniciar Treinamento Assíncrono

```bash
python train_async.py \
    --actor-num-nodes 1 \
    --actor-num-gpus-per-node 8 \
    --rollout-num-gpus 8 \
    --advantage-estimator grpo \
    --async-buffer-size 4 \
    --prompt-data /path/to/train.jsonl \
    ${MODEL_ARGS[@]}
```

### Parâmetros Específicos do Modo Assíncrono

```bash
--async-buffer-size 4        # Número de rollouts para buffer
--update-weights-interval 2  # Sincronizar pesos a cada N rollouts
```

---

## Fluxo de Trabalho 3: Treinamento Agentic Multi-Turn

Use este fluxo de trabalho para treinar agentes com uso de ferramentas ou raciocínio multi-etapa.

### Pré-Requisitos
- [ ] Função de geração personalizada para lógica multi-turn
- [ ] Interface de ferramenta/ambiente

### Passo 1: Definir Função de Geração Personalizada

```python
# custom_generate.py
async def custom_generate(args, samples, evaluation=False):
    """Geração multi-turn com chamada de ferramentas."""
    for sample in samples:
        conversation = sample.prompt

        for turn in range(args.max_turns):
            # Gerar resposta
            response = await generate_single(conversation)

            # Verificar chamada de ferramenta
            tool_call = extract_tool_call(response)
            if tool_call:
                tool_result = execute_tool(tool_call)
                conversation.append({"role": "assistant", "content": response})
                conversation.append({"role": "tool", "content": tool_result})
            else:
                break

        sample.response = response
        sample.reward = compute_reward(sample)

    return samples
```

### Passo 2: Iniciar com Função Personalizada

```bash
python train.py \
    --custom-generate-function-path custom_generate.py \
    --max-turns 5 \
    --prompt-data /path/to/agent_data.jsonl \
    ${MODEL_ARGS[@]}
```

Veja `examples/search-r1/` para um exemplo completo de busca multi-turn.

---

## Referência de Configuração

### Três Categorias de Argumentos

slime usa três tipos de argumentos:

**1. Argumentos Megatron** (passados diretamente):
```bash
--tensor-model-parallel-size 2
--pipeline-model-parallel-size 1
--num-layers 32
--hidden-size 4096
```

**2. Argumentos SGLang** (prefixados com `--sglang-`):
```bash
--sglang-mem-fraction-static 0.8
--sglang-context-length 8192
--sglang-log-level INFO
```

**3. Argumentos slime**:
```bash
# Alocação de recursos
--actor-num-nodes 1
--actor-num-gpus-per-node 8
--rollout-num-gpus 8
--colocate  # Compartilhar GPUs entre treinamento/inferência

# Dados
--prompt-data /path/to/data.jsonl
--input-key prompt
--label-key label

# Loop de treinamento
--num-rollout 3000
--rollout-batch-size 32
--n-samples-per-prompt 8
--global-batch-size 256

# Algoritmo
--advantage-estimator grpo  # ou: gspo, ppo, reinforce_plus_plus
--use-kl-loss
--kl-loss-coef 0.001
```

### Restrições-Chave

```
rollout_batch_size × n_samples_per_prompt = global_batch_size × num_steps_per_rollout
```

Exemplo: 32 × 8 = 256 × 1

---

## Sistema de Buffer de Dados

O buffer de dados do slime permite gerenciamento flexível de dados:

### Fonte de Dados Básica

```python
class RolloutDataSource:
    def get_samples(self, num_samples):
        """Buscar prompts do dataset."""
        return self.dataset.sample(num_samples)

    def add_samples(self, samples):
        """Chamado após geração (sem operação por padrão)."""
        pass
```

### Fonte de Dados com Buffer (Off-Policy)

```python
class RolloutDataSourceWithBuffer(RolloutDataSource):
    def __init__(self):
        self.buffer = []

    def add_samples(self, samples):
        """Armazenar amostras geradas para reuso."""
        self.buffer.extend(samples)

    def buffer_filter(self, args, buffer, num_samples):
        """Lógica de seleção personalizada (priorizada, estratificada, etc.)."""
        return select_best(buffer, num_samples)
```

---

## Problemas Comuns e Soluções

### Problema: Falha da Engine SGLang

**Sintomas**: Engine de inferência morre durante o treinamento

**Soluções**:
```bash
# Habilitar tolerância a falhas
--use-fault-tolerance

# Aumentar alocação de memória
--sglang-mem-fraction-static 0.85

# Reduzir tamanho do lote
--rollout-batch-size 16
```

### Problema: Timeout de Sincronização de Pesos

**Sintomas**: Treinamento trava após rollout

**Soluções**:
```bash
# Aumentar intervalo de sincronização
--update-weights-interval 5

# Usar modo colocalizado (sem transferência de rede)
--colocate
```

### Problema: OOM Durante Treinamento

**Sintomas**: OOM CUDA na etapa de backward

**Soluções**:
```bash
# Habilitar gradient checkpointing
--recompute-activations

# Reduzir tamanho de micro-lote
--micro-batch-size 1

# Habilitar paralelismo de sequência
--sequence-parallel
```

### Problema: Carregamento de Dados Lento

**Sintomas**: GPU inativa durante busca de dados

**Soluções**:
```bash
# Aumentar workers de dados
--num-data-workers 4

# Usar dataset streaming
--streaming-data
```

---

## Modelos Suportados

| Família de Modelos | Configurações |
|--------------|----------------|
| GLM | GLM-4.5, GLM-4.6, GLM-4.7, GLM-Z1-9B |
| Qwen | Qwen3 (4B, 8B, 30B-A3B), Qwen3-MoE, Qwen2.5 |
| DeepSeek | V3, V3.1, R1 |
| Llama | Llama 3 (8B, 70B) |
| Outros | Kimi K2, Moonlight-16B |

Cada modelo possui scripts pré-configurados em `scripts/models/`.

---

## Tópicos Avançados

### Modo Co-localizado

Compartilhe GPUs entre treinamento e inferência para reduzir memória:

```bash
python train.py \
    --colocate \
    --actor-num-gpus-per-node 8 \
    --sglang-mem-fraction-static 0.4 \
    ${MODEL_ARGS[@]}
```

### Modelo de Recompensa Personalizado

```python
# custom_rm.py
class CustomRewardModel:
    def __init__(self, model_path):
        self.model = load_model(model_path)

    def compute_reward(self, prompts, responses):
        inputs = self.tokenize(prompts, responses)
        scores = self.model(inputs)
        return scores.tolist()
```

```bash
--custom-rm-path custom_rm.py
```

### Avaliação Multi-Tarefa

```bash
--eval-prompt-data aime /path/to/aime.jsonl \
--eval-prompt-data gsm8k /path/to/gsm8k.jsonl \
--n-samples-per-eval-prompt 16
```

---

## Recursos

- **Documentação**: https://thudm.github.io/slime/
- **GitHub**: https://github.com/THUDM/slime
- **Blog**: https://lmsys.org/blog/2025-07-09-slime/
- **Exemplos**: Veja diretório `examples/` para 14+ exemplos práticos