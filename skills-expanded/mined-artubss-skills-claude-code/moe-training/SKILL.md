---
name: moe-training
description: Treinar modelos de Mixture of Experts (MoE) usando DeepSpeed ou HuggingFace. Use ao treinar modelos em larga escala com computação limitada (redução de 5× em custos vs modelos densos), implementar arquiteturas esparsas como Mixtral 8x7B ou DeepSeek-V3, ou escalar capacidade de modelo sem aumento proporcional de computação. Cobre arquiteturas MoE, mecanismos de roteamento, balanceamento de carga, paralelismo de especialistas e otimização de inferência.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Emerging Techniques, MoE, Mixture Of Experts, Sparse Models, DeepSpeed, Expert Parallelism, Mixtral, DeepSeek, Routing, Load Balancing, Efficient Training]
dependencies: [deepspeed, transformers, torch, accelerate]
---

# Treinamento MoE: Mixture of Experts

## Quando Usar Esta Habilidade

Use MoE Training quando você precisa:
- **Treinar modelos maiores** com computação limitada (redução de 5× em custos vs modelos densos)
- **Escalar capacidade de modelo** sem aumento proporcional de computação
- **Alcançar melhor performance** por orçamento de computação que modelos densos
- **Especializar especialistas** para diferentes domínios/tarefas/idiomas
- **Reduzir latência de inferência** com ativação esparsa (apenas 13B/47B parâmetros ativos em Mixtral)
- **Implementar modelos SOTA** como Mixtral 8x7B, DeepSeek-V3, Switch Transformers

**Modelos MoE Notáveis**: Mixtral 8x7B (Mistral AI), DeepSeek-V3, Switch Transformers (Google), GLaM (Google), NLLB-MoE (Meta)

## Instalação

```bash
# DeepSpeed com suporte a MoE
pip install deepspeed>=0.6.0

# Megatron-DeepSpeed para treinamento em larga escala
git clone https://github.com/microsoft/Megatron-DeepSpeed
cd Megatron-DeepSpeed
pip install -r requirements.txt

# Alternativa: HuggingFace Transformers
pip install transformers accelerate
```

## Início Rápido

### Arquitetura MoE Básica

```python
import torch
import torch.nn as nn

class MoELayer(nn.Module):
    """Sparse Mixture of Experts layer."""

    def __init__(self, hidden_size, num_experts=8, top_k=2):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k

        # Expert networks (FFN)
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(hidden_size, 4 * hidden_size),
                nn.GELU(),
                nn.Linear(4 * hidden_size, hidden_size)
            )
            for _ in range(num_experts)
        ])

        # Gating network (router)
        self.gate = nn.Linear(hidden_size, num_experts)

    def forward(self, x):
        # x shape: (batch_size, seq_len, hidden_size)
        batch_size, seq_len, hidden_size = x.shape

        # Flatten for routing
        x_flat = x.view(-1, hidden_size)  # (batch_size * seq_len, hidden_size)

        # Compute gate scores
        gate_logits = self.gate(x_flat)  # (batch_size * seq_len, num_experts)

        # Top-k routing
        gate_scores = torch.softmax(gate_logits, dim=-1)
        topk_scores, topk_indices = torch.topk(gate_scores, self.top_k, dim=-1)

        # Normalize top-k scores
        topk_scores = topk_scores / topk_scores.sum(dim=-1, keepdim=True)

        # Dispatch and combine expert outputs
        output = torch.zeros_like(x_flat)

        for i in range(self.top_k):
            expert_idx = topk_indices[:, i]
            expert_scores = topk_scores[:, i].unsqueeze(-1)

            # Route tokens to experts
            for expert_id in range(self.num_experts):
                mask = (expert_idx == expert_id)
                if mask.any():
                    expert_input = x_flat[mask]
                    expert_output = self.experts[expert_id](expert_input)
                    output[mask] += expert_scores[mask] * expert_output

        # Reshape back
        return output.view(batch_size, seq_len, hidden_size)
```

### Treinamento DeepSpeed MoE

```bash
# Script de treinamento com MoE
deepspeed pretrain_gpt_moe.py \
  --num-layers 24 \
  --hidden-size 1024 \
  --num-attention-heads 16 \
  --seq-length 2048 \
  --max-position-embeddings 2048 \
  --micro-batch-size 4 \
  --global-batch-size 256 \
  --train-iters 500000 \
  --lr 0.0001 \
  --min-lr 0.00001 \
  --lr-decay-style cosine \
  --num-experts 128 \
  --moe-expert-parallel-size 4 \
  --moe-loss-coeff 0.01 \
  --moe-train-capacity-factor 1.25 \
  --moe-eval-capacity-factor 2.0 \
  --fp16 \
  --deepspeed_config ds_config.json
```

## Conceitos Principais

### 1. Arquitetura MoE

**Componentes-chave:**
- **Especialistas**: Múltiplas redes FFN especializadas (tipicamente 8-128)
- **Roteador/Gate**: Rede aprendida que seleciona quais especialistas usar
- **Roteamento Top-k**: Ativa apenas k especialistas por token (k=1 ou k=2)
- **Balanceamento de Carga**: Garante utilização uniforme de especialistas

```
Token de Entrada
    ↓
Roteador (Rede Gate)
    ↓
Seleção de Especialistas Top-k (ex: 2 de 8)
    ↓
Especialista 1 (peso: 0,6) + Especialista 5 (peso: 0,4)
    ↓
Combinação Ponderada
    ↓
Saída
```

### 2. Mecanismos de Roteamento

**Roteamento Top-1 (Switch Transformer):**
```python
# Roteamento mais simples: um especialista por token
gate_logits = router(x)  # (batch, seq_len, num_experts)
expert_idx = torch.argmax(gate_logits, dim=-1)  # Roteamento duro
```

**Roteamento Top-2 (Mixtral):**
```python
# Top-2: dois especialistas por token
gate_scores = torch.softmax(router(x), dim=-1)
top2_scores, top2_indices = torch.topk(gate_scores, k=2, dim=-1)

# Normalizar pontuações
top2_scores = top2_scores / top2_scores.sum(dim=-1, keepdim=True)

# Combinar saídas de especialistas
output = (top2_scores[:, :, 0:1] * expert_outputs[top2_indices[:, :, 0]] +
          top2_scores[:, :, 1:2] * expert_outputs[top2_indices[:, :, 1]])
```

**Roteamento por Escolha de Especialista:**
```python
# Especialistas escolhem top-k tokens (ao invés de tokens escolherem especialistas)
# Garante balanceamento perfeito de carga
expert_scores = router(x).transpose(-1, -2)  # (batch, num_experts, seq_len)
topk_tokens = torch.topk(expert_scores, k=capacity_per_expert, dim=-1)
```

### 3. Balanceamento de Carga

**Perda Auxiliar:**
```python
def load_balancing_loss(gate_logits, expert_indices, num_experts):
    """Incentivar uso uniforme de especialistas."""
    # Fração de tokens roteados para cada especialista
    expert_counts = torch.bincount(expert_indices.flatten(), minlength=num_experts)
    expert_fraction = expert_counts.float() / expert_indices.numel()

    # Probabilidade de gate para cada especialista (média entre tokens)
    gate_probs = torch.softmax(gate_logits, dim=-1).mean(dim=0)

    # Perda auxiliar: incentivar alinhamento
    aux_loss = num_experts * (expert_fraction * gate_probs).sum()

    return aux_loss

# Adicionar à perda principal
total_loss = language_model_loss + 0.01 * load_balancing_loss(...)
```

**Perda Z do Roteador (Estabilidade):**
```python
def router_z_loss(logits):
    """Incentivar roteador a ter entropia mais baixa (mais decisivo)."""
    z_loss = torch.logsumexp(logits, dim=-1).pow(2).mean()
    return z_loss

total_loss = lm_loss + 0.01 * aux_loss + 0.001 * router_z_loss(gate_logits)
```

### 4. Paralelismo de Especialistas

```python
# Configuração DeepSpeed
{
  "train_batch_size": 256,
  "fp16": {"enabled": true},
  "moe": {
    "enabled": true,
    "num_experts": 128,
    "expert_parallel_size": 8,  # Distribuir 128 especialistas em 8 GPUs
    "capacity_factor": 1.25,    # Capacidade de especialista = tokens_por_lote * capacity_factor / num_experts
    "drop_tokens": true,        # Descartar tokens excedendo capacidade
    "use_residual": false
  }
}
```

## Configuração de Treinamento

### Configuração DeepSpeed MoE

```json
{
  "train_batch_size": 256,
  "gradient_accumulation_steps": 1,
  "optimizer": {
    "type": "Adam",
    "params": {
      "lr": 0.0001,
      "betas": [0.9, 0.999],
      "eps": 1e-8
    }
  },
  "fp16": {
    "enabled": true,
    "loss_scale": 0,
    "initial_scale_power": 16
  },
  "moe": {
    "enabled": true,
    "num_experts": 128,
    "expert_parallel_size": 8,
    "moe_loss_coeff": 0.01,
    "train_capacity_factor": 1.25,
    "eval_capacity_factor": 2.0,
    "min_capacity": 4,
    "drop_tokens": true,
    "use_residual": false,
    "use_tutel": false
  },
  "zero_optimization": {
    "stage": 1
  }
}
```

### Script de Treinamento

```bash
#!/bin/bash

# Treinamento MoE estilo Mixtral
deepspeed --num_gpus 8 pretrain_moe.py \
  --model-parallel-size 1 \
  --num-layers 32 \
  --hidden-size 4096 \
  --num-attention-heads 32 \
  --seq-length 2048 \
  --max-position-embeddings 4096 \
  --micro-batch-size 2 \
  --global-batch-size 256 \
  --train-iters 500000 \
  --save-interval 5000 \
  --eval-interval 1000 \
  --eval-iters 100 \
  --lr 0.0001 \
  --min-lr 0.00001 \
  --lr-decay-style cosine \
  --lr-warmup-iters 2000 \
  --clip-grad 1.0 \
  --weight-decay 0.1 \
  --num-experts 8 \
  --moe-expert-parallel-size 4 \
  --moe-loss-coeff 0.01 \
  --moe-train-capacity-factor 1.25 \
  --moe-eval-capacity-factor 2.0 \
  --disable-moe-token-dropping \
  --fp16 \
  --deepspeed \
  --deepspeed_config ds_config_moe.json \
  --data-path /path/to/data \
  --vocab-file /path/to/vocab.json \
  --merge-file /path/to/merges.txt
```

## Padrões Avançados

### Arquitetura Mixtral 8x7B

```python
class MixtralMoEBlock(nn.Module):
    """Bloco MoE estilo Mixtral com 8 especialistas, roteamento top-2."""

    def __init__(self, config):
        super().__init__()
        self.hidden_dim = config.hidden_size
        self.ffn_dim = config.intermediate_size
        self.num_experts = config.num_local_experts  # 8
        self.top_k = config.num_experts_per_tok       # 2

        # 8 FFNs de especialista
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(self.hidden_dim, self.ffn_dim, bias=False),
                nn.SiLU(),
                nn.Linear(self.ffn_dim, self.hidden_dim, bias=False)
            )
            for _ in range(self.num_experts)
        ])

        # Roteador
        self.gate = nn.Linear(self.hidden_dim, self.num_experts, bias=False)

    def forward(self, hidden_states):
        batch_size, sequence_length, hidden_dim = hidden_states.shape

        # Achatar
        hidden_states = hidden_states.view(-1, hidden_dim)

        # Logits do roteador
        router_logits = self.gate(hidden_states)  # (batch * seq_len, num_experts)

        # Softmax e top-2
        routing_weights = torch.softmax(router_logits, dim=1)
        routing_weights, selected_experts = torch.topk(routing_weights, self.top_k, dim=-1)

        # Normalizar pesos de roteamento
        routing_weights /= routing_weights.sum(dim=-1, keepdim=True)

        # Inicializar saída
        final_hidden_states = torch.zeros_like(hidden_states)

        # Rotear para especialistas
        for expert_idx in range(self.num_experts):
            expert_layer = self.experts[expert_idx]
            idx, top_x = torch.where(selected_experts == expert_idx)

            if idx.shape[0] == 0:
                continue

            # Tokens do especialista atual
            current_hidden_states = hidden_states[idx]

            # Forward do especialista
            current_hidden_states = expert_layer(current_hidden_states)

            # Ponderado pelos scores de roteamento
            current_hidden_states *= routing_weights[idx, top_x, None]

            # Acumular
            final_hidden_states.index_add_(0, idx, current_hidden_states)

        # Reformatar
        return final_hidden_states.view(batch_size, sequence_length, hidden_dim)
```

### PR-MoE (Pyramid-Residual-MoE)

```bash
# DeepSpeed PR-MoE: eficiência de parâmetros 3× melhor
deepspeed pretrain_gpt_moe.py \
  --num-layers 24 \
  --hidden-size 1024 \
  --num-attention-heads 16 \
  --num-experts "[128, 64, 32, 16]" \
  --mlp-type residual \
  --moe-expert-parallel-size 4 \
  --moe-loss-coeff 0.01 \
  --fp16
```

## Melhores Práticas

### 1. Seleção de Contagem de Especialistas

```python
# Regra prática: Mais especialistas = mais capacidade, mas retornos diminutos
# Configurações típicas:
# - Modelos pequenos (1B-7B): 8-16 especialistas
# - Modelos médios (7B-30B): 8-64 especialistas
# - Modelos grandes (30B+): 64-256 especialistas

# Exemplo: Mixtral 8x7B
# Parâmetros totais: 47B (8 especialistas × 7B cada)
# Parâmetros ativos: 13B (2 especialistas × 7B, roteamento top-2)
# Eficiência: 47B capacidade com 13B computação
```

### 2. Ajuste de Fator de Capacidade

```python
# Capacidade = (tokens_por_lote / num_experts) * capacity_factor

# Treinamento: Capacidade menor (mais rápido, descarta alguns tokens)
train_capacity_factor = 1.25  # Buffer de 25%

# Avaliação: Capacidade maior (sem descartes)
eval_capacity_factor = 2.0    # Buffer de 100%

# Fórmula:
expert_capacity = int((seq_len * batch_size / num_experts) * capacity_factor)
```

### 3. Diretrizes de Taxa de Aprendizado

```python
# Modelos MoE precisam de LR menor que modelos densos
# - Modelo denso: lr = 6e-4
# - Modelo MoE: lr = 1e-4 (3-6× menor)

# Também estender schedule de decay
dense_lr_decay_iters = 300000
moe_lr_decay_iters = 500000  # 1,5-2× mais longo
```

### 4. Ajuste de Coeficiente de Perda

```python
# Começar com valores padrão
moe_loss_coeff = 0.01    # Perda auxiliar (balanceamento de carga)
router_z_loss_coeff = 0.001  # Entropia de roteador (estabilidade)

# Se desbalanceamento de carga persistir, aumentar perda auxiliar
if max_expert_usage / min_expert_usage > 2.0:
    moe_loss_coeff = 0.1  # Balanceamento mais forte

# Se treinamento instável, aumentar z-loss
if grad_norm > 10.0:
    router_z_loss_coeff = 0.01
```

### 5. Evitar Armadilhas Comuns

```python
# ❌ Ruim: Usando mesma LR que modelo denso
optimizer = Adam(model.parameters(), lr=6e-4)

# ✅ Bom: LR menor para MoE
optimizer = Adam([
    {'params': model.non_moe_params, 'lr': 6e-4},
    {'params': model.moe_params, 'lr': 1e-4}
])

# ❌ Ruim: Sem balanceamento de carga
loss = lm_loss

# ✅ Bom: Adicionar perda auxiliar
loss = lm_loss + 0.01 * aux_loss + 0.001 * z_loss

# ❌ Ruim: Muitos especialistas para dataset pequeno
num_experts = 128  # Risco de overfitting

# ✅ Bom: Corresponder especialistas à diversidade de dados
num_experts = 8  # Melhor para datasets pequenos
```

## Otimização de Inferência

### Inferência Esparsa

```python
# Ativar apenas top-k especialistas (enormes economias de memória)
@torch.no_grad()
def moe_inference(x, model, top_k=2):
    """Inferência MoE esparsa: carregar apenas k especialistas."""
    # Roteador
    gate_logits = model.gate(x)
    topk_scores, topk_indices = torch.topk(
        torch.softmax(gate_logits, dim=-1),
        k=top_k,
        dim=-1
    )

    # Carregar e executar apenas top-k especialistas
    output = torch.zeros_like(x)
    for i in range(top_k):
        expert_idx = topk_indices[:, i]
        # Carregar especialista de disco/offload se necessário
        expert = model.load_expert(expert_idx)
        output += topk_scores[:, i:i+1] * expert(x)

    return output
```

## Recursos

- **Tutorial DeepSpeed MoE**: https://www.deepspeed.ai/tutorials/mixture-of-experts-nlg/
- **Artigo Mixtral**: https://arxiv.org/abs/2401.04088
- **Switch Transformers**: https://arxiv.org/abs/2101.03961
- **Guia HuggingFace MoE**: https://huggingface.co/blog/moe
- **Blog NVIDIA MoE**: https://developer.nvidia.com/blog/applying-mixture-of-experts-in-llm-architectures/

## Veja Também

- `references/architectures.md` - Arquiteturas de modelos MoE (Mixtral, Switch, DeepSeek-V3)
- `references/training.md` - Técnicas avançadas de treinamento e otimização
- `references/inference.md` - Padrões de deployment e serving em produção