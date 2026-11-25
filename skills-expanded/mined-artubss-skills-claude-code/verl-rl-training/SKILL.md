---
name: verl-rl-training
description: Fornece orientação para treinar LLMs com aprendizado por reforço usando verl (Volcano Engine RL). Use ao implementar RLHF, GRPO, PPO ou outros algoritmos de RL para pós-treinamento de LLMs em escala com backends de infraestrutura flexíveis.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Reinforcement Learning, RLHF, GRPO, PPO, Post-Training, Distributed Training]
dependencies: [verl>=0.3.0, torch>=2.0.0, ray>=2.41.0, vllm>=0.8.2, transformers>=4.40.0]
---

# verl: Volcano Engine Reinforcement Learning para LLMs

verl é uma biblioteca de treinamento RL flexível, eficiente e pronta para produção para modelos de linguagem grandes do time Seed da ByteDance. Implementa o framework HybridFlow (EuroSys 2025) e capacita modelos como Doubao-1.5-pro alcançando desempenho nível O1 em benchmarks de matemática.

## Quando Usar verl

**Escolha verl quando você precisa de:**
- Treinamento RL pronto para produção em escala (testado até 671B parâmetros)
- Flexibilidade para trocar backends (FSDP ↔ Megatron-LM ↔ vLLM ↔ SGLang)
- Suporte para múltiplos algoritmos de RL (PPO, GRPO, RLOO, REINFORCE++, DAPO)
- Rollout multi-turno com chamada de ferramentas para workflows agentic
- Treinamento RL para modelos de visão-linguagem

**Considere alternativas quando:**
- Você precisa de treinamento nativo Megatron → use **slime** ou **miles**
- Você quer abstrações nativas do PyTorch com Monarch → use **torchforge**
- Você só precisa de SFT/DPO simples → use **TRL** ou **Axolotl**

## Recursos Principais

- **Backends de treinamento**: FSDP, FSDP2, Megatron-LM
- **Engines de rollout**: vLLM, SGLang, HuggingFace Transformers
- **Algoritmos**: PPO, GRPO, DAPO, RLOO, ReMax, REINFORCE++, SPIN, SPPO
- **Modelos**: Qwen-3, Llama-3.1, DeepSeek, Gemma-2 (0.5B a 671B)
- **Avançado**: LoRA RL, sequence parallelism, expert parallelism, ferramentas multi-turno

## Instalação

```bash
# Opção 1: pip install
pip install verl[vllm]  # ou verl[sglang] para backend SGLang

# Opção 2: Docker (recomendado para produção)
docker pull verlai/verl:vllm011.latest

# Opção 3: Do código-fonte
git clone https://github.com/volcengine/verl.git
cd verl && pip install -e .[vllm,math]
```

## Início Rápido: Treinamento GRPO

```bash
python3 -m verl.trainer.main_ppo \
    algorithm.adv_estimator=grpo \
    data.train_files=~/data/gsm8k/train.parquet \
    actor_rollout_ref.model.path=Qwen/Qwen2.5-7B \
    actor_rollout_ref.rollout.n=8 \
    actor_rollout_ref.actor.use_kl_loss=True \
    trainer.n_gpus_per_node=8
```

## Arquitetura Principal

verl usa um modelo de programação **HybridFlow** separando fluxo de controle de computação:

```
┌─────────────────────────────────────────────────────────┐
│ Controlador de Processo Único (Ray)                     │
│ - Orquestra: rollout → reward → train → sync            │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│ Workers Multi-Processo                                  │
│ ├── ActorRolloutRefWorker (policy + generation)        │
│ ├── CriticWorker (value estimation, PPO only)          │
│ └── RewardManager (model-based or rule-based rewards)  │
└─────────────────────────────────────────────────────────┘
```

---

## Workflow 1: Raciocínio Matemático com GRPO

Use este workflow para treinar modelos de raciocínio em tarefas matemáticas como GSM8K ou MATH.

### Checklist de Pré-requisitos
- [ ] Cluster de GPU com 8+ GPUs (H100 recomendado)
- [ ] Dataset em formato parquet com colunas `prompt` e `reward_model`
- [ ] Modelo base do HuggingFace Hub

### Passo 1: Preparar Dataset

```python
import pandas as pd

data = [
    {
        "prompt": [{"role": "user", "content": "Quanto é 15 + 27?"}],
        "reward_model": {"ground_truth": "42"}
    },
    # ... mais exemplos
]
df = pd.DataFrame(data)
df.to_parquet("train.parquet")
```

### Passo 2: Definir Função de Recompensa

```python
# reward_function.py
import re

def compute_reward(responses, ground_truths):
    rewards = []
    for response, gt in zip(responses, ground_truths):
        # Extrai resposta da resposta gerada
        match = re.search(r'\\boxed{([^}]+)}', response)
        if match and match.group(1).strip() == gt.strip():
            rewards.append(1.0)
        else:
            rewards.append(0.0)
    return rewards
```

### Passo 3: Criar Configuração de Treinamento

```yaml
# config/grpo_math.yaml
algorithm:
  adv_estimator: grpo
  gamma: 1.0
  lam: 1.0

data:
  train_files: /path/to/train.parquet
  val_files: /path/to/val.parquet
  train_batch_size: 256
  max_prompt_length: 512
  max_response_length: 2048

actor_rollout_ref:
  model:
    path: Qwen/Qwen2.5-7B-Instruct
  actor:
    use_kl_loss: true
    kl_loss_coef: 0.001
    ppo_mini_batch_size: 64
  rollout:
    name: vllm
    n: 8  # amostras por prompt
    temperature: 0.7
    top_p: 0.95

trainer:
  total_epochs: 3
  n_gpus_per_node: 8
  save_freq: 100
```

### Passo 4: Iniciar Treinamento

```bash
python3 -m verl.trainer.main_ppo \
    --config-path config \
    --config-name grpo_math \
    trainer.experiment_name=grpo_math_qwen7b
```

### Passo 5: Monitorar e Validar
- [ ] Verificar WandB/TensorBoard para curvas de loss
- [ ] Verificar se a recompensa está aumentando ao longo dos passos
- [ ] Executar avaliação no conjunto de testes separado

---

## Workflow 2: PPO com Modelo Critic

Use este workflow quando você precisa de estimação de vantagem baseada em valor (GAE).

### Diferenças-Chave em relação ao GRPO
- Requer modelo critic separado
- Usa Generalized Advantage Estimation (GAE)
- Melhor para tarefas com recompensas densas

### Configuração

```yaml
algorithm:
  adv_estimator: gae  # Use GAE em vez de GRPO
  gamma: 0.99
  lam: 0.95

critic:
  model:
    path: Qwen/Qwen2.5-7B-Instruct  # Pode ser igual ou diferente do actor
  ppo_mini_batch_size: 64

actor_rollout_ref:
  actor:
    use_kl_loss: true
    kl_loss_coef: 0.02
    clip_ratio: 0.2  # Clipping do PPO
```

### Iniciar com Critic

```bash
python3 -m verl.trainer.main_ppo \
    algorithm.adv_estimator=gae \
    critic.model.path=Qwen/Qwen2.5-7B-Instruct \
    trainer.n_gpus_per_node=8
```

---

## Workflow 3: Treinamento em Larga Escala com Megatron

Use este workflow para modelos >70B parâmetros ou quando você precisa de expert parallelism.

### Pré-requisitos
- [ ] Instalar bridge Megatron-LM: `pip install mbridge`
- [ ] Converter modelo para formato Megatron
- [ ] Cluster multi-nó com NVLink/InfiniBand

### Configuração para Modelos 70B+

```yaml
actor_rollout_ref:
  model:
    path: /path/to/megatron/checkpoint
    backend: megatron
  actor:
    strategy: megatron
    tensor_model_parallel_size: 8
    pipeline_model_parallel_size: 2
  rollout:
    name: vllm
    tensor_parallel_size: 8
```

### Iniciar Multi-Nó

```bash
# No nó head
ray start --head --port=6379

# Nos nós workers
ray start --address='head_ip:6379'

# Iniciar treinamento
python3 -m verl.trainer.main_ppo \
    trainer.nnodes=4 \
    trainer.n_gpus_per_node=8
```

---

## Referência de Configuração

### Seleção de Algoritmo

| Algoritmo | `adv_estimator` | Caso de Uso |
|-----------|-----------------|----------|
| GRPO | `grpo` | Sem critic, matemática/raciocínio |
| PPO/GAE | `gae` | Recompensas densas, estimação de valor |
| REINFORCE++ | `reinforce_plus_plus` | Redução de variância |
| RLOO | `rloo` | Baseline leave-one-out |
| ReMax | `remax` | Baseline de recompensa máxima |
| OPO | `opo` | Otimização de política ótima |

### Parâmetros-Chave

```yaml
# Parâmetros de rollout
actor_rollout_ref.rollout.n: 8              # Amostras por prompt
actor_rollout_ref.rollout.temperature: 0.7  # Temperatura de amostragem
actor_rollout_ref.rollout.top_p: 0.95       # Amostragem nucleus

# Parâmetros de treinamento
actor_rollout_ref.actor.lr: 1e-6            # Taxa de aprendizado
actor_rollout_ref.actor.ppo_mini_batch_size: 64
actor_rollout_ref.actor.clip_ratio: 0.2     # Intervalo de clip do PPO

# Controle KL
actor_rollout_ref.actor.use_kl_loss: true
actor_rollout_ref.actor.kl_loss_coef: 0.001
algorithm.kl_ctrl.target_kl: 0.1            # Para controle KL adaptativo
```

---

## Problemas Comuns e Soluções

### Problema: OOM Durante Rollout

**Sintomas**: CUDA fora de memória durante fase de geração

**Soluções**:
```yaml
# Reduzir tamanho de batch
actor_rollout_ref.rollout.log_prob_micro_batch_size: 4

# Ativar gradient checkpointing
actor_rollout_ref.model.enable_gradient_checkpointing: true

# Usar FSDP2 com offloading para CPU
actor_rollout_ref.actor.strategy: fsdp2
actor_rollout_ref.actor.fsdp_config.offload_policy: true
```

### Problema: Instabilidade no Treinamento

**Sintomas**: Picos de loss, colapso de recompensa

**Soluções**:
```yaml
# Reduzir taxa de aprendizado
actor_rollout_ref.actor.lr: 5e-7

# Aumentar penalidade KL
actor_rollout_ref.actor.kl_loss_coef: 0.01

# Ativar clipping de gradiente
actor_rollout_ref.actor.max_grad_norm: 1.0
```

### Problema: Sincronização de Peso Lenta

**Sintomas**: Pausas longas entre rollout e treinamento

**Soluções**:
```bash
# Usar FSDP2 para resharding mais rápido
actor_rollout_ref.actor.strategy=fsdp2

# Ativar transferência assíncrona de peso
trainer.async_weight_update=true
```

### Problema: Incompatibilidade de Versão vLLM

**Sintomas**: Erros de import ou falhas na geração

**Solução**: Use versões compatíveis:
```bash
pip install vllm>=0.8.5,<=0.12.0
# Evite vLLM 0.7.x (bugs conhecidos)
```

---

## Tópicos Avançados

### Chamada de Ferramentas Multi-Turno

Veja [references/multi-turn.md](references/multi-turn.md) para workflows agentic com uso de ferramentas.

### Modelos de Visão-Linguagem

```yaml
actor_rollout_ref:
  model:
    path: Qwen/Qwen2.5-VL-7B-Instruct
  rollout:
    name: vllm
    enable_vision: true
```

### Treinamento LoRA

```yaml
actor_rollout_ref:
  actor:
    lora:
      enabled: true
      r: 16
      alpha: 32
      target_modules: ["q_proj", "v_proj"]
```

---

## Recursos

- **Documentação**: https://verl.readthedocs.io/
- **Paper**: https://arxiv.org/abs/2409.19256
- **GitHub**: https://github.com/volcengine/verl
- **Recipes**: https://github.com/verl-project/verl-recipe (DAPO, GSPO, etc.)
- **Comunidade**: Slack em verl-project