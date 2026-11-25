---
name: long-context
description: Estenda janelas de contexto de modelos transformer usando RoPE, YaRN, ALiBi e técnicas de interpolação de posição. Use ao processar documentos longos (32k-128k+ tokens), estender modelos pré-treinados além dos limites de contexto originais ou implementar codificações posicionais eficientes. Cobre embeddings rotativos, vieses de atenção, métodos de interpolação e estratégias de extrapolação para LLMs.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Emerging Techniques, Long Context, RoPE, YaRN, ALiBi, Position Interpolation, Extended Context, Rotary Embeddings, Attention Bias, Context Extension, Positional Encoding]
dependencies: [transformers, torch, flash-attn]
---

# Long Context: Estendendo Janelas de Contexto de Transformers

## Quando Usar Esta Skill

Use técnicas de Long Context quando você precisa:
- **Processar documentos longos** (32k, 64k, 128k+ tokens) com modelos transformer
- **Estender janelas de contexto** de modelos pré-treinados (LLaMA, Mistral, etc.)
- **Implementar codificações posicionais eficientes** (RoPE, ALiBi)
- **Treinar modelos** com capacidades de extrapolação de comprimento
- **Fazer deploy de modelos** que lidam com entradas de comprimento variável eficientemente
- **Fine-tunar** modelos existentes para contextos mais longos com mínimo de computação

**Técnicas-chave**: RoPE (Rotary Position Embeddings), YaRN, ALiBi (Attention with Linear Biases), Position Interpolation

**Papers**: RoFormer (arXiv 2104.09864), YaRN (arXiv 2309.00071), ALiBi (arXiv 2108.12409), Position Interpolation (arXiv 2306.15595)

## Instalação

```bash
# HuggingFace Transformers (inclui suporte RoPE, YaRN)
pip install transformers torch

# Para implementações customizadas
pip install einops  # Operações com tensores
pip install rotary-embedding-torch  # RoPE standalone

# Opcional: FlashAttention para eficiência
pip install flash-attn --no-build-isolation
```

## Quick Start

### RoPE (Rotary Position Embeddings)

```python
import torch
import torch.nn as nn

class RotaryEmbedding(nn.Module):
    """Rotary Position Embeddings (RoPE)."""

    def __init__(self, dim, max_seq_len=8192, base=10000):
        super().__init__()
        # Compute inverse frequencies
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq)
        self.max_seq_len = max_seq_len

    def forward(self, seq_len, device):
        # Position indices
        t = torch.arange(seq_len, device=device).type_as(self.inv_freq)

        # Compute frequencies
        freqs = torch.outer(t, self.inv_freq)  # (seq_len, dim/2)

        # Compute sin and cos
        emb = torch.cat((freqs, freqs), dim=-1)  # (seq_len, dim)
        return emb.cos(), emb.sin()

def rotate_half(x):
    """Rotate half the hidden dimensions."""
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)

def apply_rotary_pos_emb(q, k, cos, sin):
    """Apply rotary embeddings to queries and keys."""
    # q, k shape: (batch, heads, seq_len, dim)
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed

# Usage
rope = RotaryEmbedding(dim=64, max_seq_len=8192)
cos, sin = rope(seq_len=2048, device='cuda')

# In attention layer
q_rotated, k_rotated = apply_rotary_pos_emb(query, key, cos, sin)
```

### ALiBi (Attention with Linear Biases)

```python
def get_alibi_slopes(num_heads):
    """Get ALiBi slope values for each attention head."""
    def get_slopes_power_of_2(n):
        start = 2 ** (-(2 ** -(math.log2(n) - 3)))
        ratio = start
        return [start * (ratio ** i) for i in range(n)]

    if math.log2(num_heads).is_integer():
        return get_slopes_power_of_2(num_heads)
    else:
        # Closest power of 2
        closest_power = 2 ** math.floor(math.log2(num_heads))
        slopes = get_slopes_power_of_2(closest_power)
        # Add extra slopes
        extra = get_slopes_power_of_2(2 * closest_power)
        slopes.extend(extra[0::2][:num_heads - closest_power])
        return slopes

def create_alibi_bias(seq_len, num_heads):
    """Create ALiBi attention bias."""
    # Distance matrix
    context_position = torch.arange(seq_len)
    memory_position = torch.arange(seq_len)
    relative_position = memory_position[None, :] - context_position[:, None]

    # Get slopes
    slopes = torch.tensor(get_alibi_slopes(num_heads))

    # Apply slopes to distances
    alibi = slopes[:, None, None] * relative_position[None, :, :]
    return alibi  # (num_heads, seq_len, seq_len)

# Usage in attention
num_heads = 8
seq_len = 2048
alibi_bias = create_alibi_bias(seq_len, num_heads).to('cuda')

# Add bias to attention scores
# attn_scores shape: (batch, num_heads, seq_len, seq_len)
attn_scores = attn_scores + alibi_bias
attn_weights = torch.softmax(attn_scores, dim=-1)
```

### Position Interpolation para LLaMA

```python
from transformers import LlamaForCausalLM, LlamaTokenizer

# Contexto original: 2048 tokens
model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")

# Estender para 32k com interpolação de posição
# Modificar frequência base RoPE
model.config.rope_scaling = {
    "type": "linear",
    "factor": 16.0  # 2048 * 16 = 32768
}

# Ou usar scaling dinâmico
model.config.rope_scaling = {
    "type": "dynamic",
    "factor": 16.0
}

# Fine-tunar com documentos longos (apenas passos mínimos necessários)
# Interpolação de posição funciona automaticamente após esta mudança de config
```

## Conceitos Principais

### 1. RoPE (Rotary Position Embeddings)

**Como funciona:**
- Codifica posição absoluta via matriz de rotação
- Fornece dependência de posição relativa em atenção
- Permite extrapolação de comprimento

**Formulação matemática:**
```
q_m = (W_q * x_m) * e^(imθ)
k_n = (W_k * x_n) * e^(inθ)

where θ_j = base^(-2j/d) for j ∈ [0, d/2)
```

**Vantagens:**
- Dependência entre tokens decaindo com distância
- Compatível com atenção linear
- Melhor extrapolação que codificações de posição absoluta

### 2. YaRN (Yet another RoPE extensioN)

**Inovação-chave:**
- Interpolação consciente de NTK (Neural Tangent Kernel)
- Scaling de temperatura de atenção
- Extensão de contexto eficiente (10× menos tokens vs baselines)

**Parâmetros:**
```python
# Configuração YaRN
yarn_config = {
    "scale": 16,                    # Fator de extensão
    "original_max_position": 2048,  # Contexto base
    "extrapolation_factor": 1.0,    # Parâmetro NTK
    "attn_factor": 1.0,             # Scaling de atenção
    "beta_fast": 32,                # Escala de alta frequência
    "beta_slow": 1,                 # Escala de baixa frequência
}
```

**Performance:**
- Estende LLaMA para 128k tokens
- 2.5× menos passos de treinamento que baselines
- Extensão de janela de contexto state-of-the-art

### 3. ALiBi (Attention with Linear Biases)

**Ideia principal:**
- Sem embeddings posicionais adicionados aos tokens
- Aplicar penalidade de distância diretamente aos scores de atenção
- Viés proporcional à distância entre chave e consulta

**Fórmula:**
```
attention_bias[i, j] = -m * |i - j|

where m = slope para cada cabeça de atenção
```

**Vantagens:**
- 11% mais rápido em treinamento vs embeddings sinusoidais
- 11% menos uso de memória
- Extrapolação de comprimento forte (treinar 1k, testar 2k+)
- Viés indutivo para recência

### 4. Position Interpolation

**Técnica:**
- Escalar linearmente para baixo índices de posição
- Interpolar dentro do intervalo treinado (vs extrapolar além)
- Fine-tuning mínimo necessário

**Fórmula:**
```
# Original: índices de posição [0, 1, 2, ..., L]
# Extended: índices de posição [0, 0.5, 1.0, ..., L/2]
# (para extensão 2×)

scaled_position[i] = i / extension_factor
```

**Resultados:**
- LLaMA 7B-65B estendido para 32k tokens
- 1000 passos de fine-tuning suficientes
- 600× melhor estabilidade que extrapolação

## Comparação de Métodos

| Método | Max Context | Treinamento Necessário | Memória | Extrapolação | Melhor Para |
|--------|-------------|------------------------|---------|--------------|------------|
| **RoPE** | 8k-32k | Pré-treinamento completo | Moderado | Bom | Novos modelos |
| **YaRN** | 32k-128k | Mínimo (10× eficiente) | Moderado | Excelente | Estender modelos existentes |
| **ALiBi** | Ilimitado | Pré-treinamento completo | Baixo (-11%) | Excelente | Treinar do zero |
| **Position Interpolation** | 32k+ | Mínimo (1k passos) | Moderado | Fraco (por design) | Extensão rápida |

## Padrões de Implementação

### Integração HuggingFace Transformers

```python
from transformers import AutoModelForCausalLM, AutoConfig

# RoPE com scaling YaRN
config = AutoConfig.from_pretrained("mistralai/Mistral-7B-v0.1")
config.rope_scaling = {
    "type": "yarn",
    "factor": 8.0,
    "original_max_position_embeddings": 8192,
    "attention_factor": 1.0
}

model = AutoModelForCausalLM.from_config(config)

# Position interpolation (mais simples)
config.rope_scaling = {
    "type": "linear",
    "factor": 4.0
}

# Dynamic scaling (ajusta baseado no comprimento da entrada)
config.rope_scaling = {
    "type": "dynamic",
    "factor": 8.0
}
```

### Implementação RoPE Customizada

```python
class LongContextAttention(nn.Module):
    """Atenção multi-cabeça com RoPE."""

    def __init__(self, hidden_size, num_heads, max_seq_len=32768):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = hidden_size // num_heads

        # Projeções Q, K, V
        self.q_proj = nn.Linear(hidden_size, hidden_size)
        self.k_proj = nn.Linear(hidden_size, hidden_size)
        self.v_proj = nn.Linear(hidden_size, hidden_size)
        self.o_proj = nn.Linear(hidden_size, hidden_size)

        # RoPE
        self.rotary_emb = RotaryEmbedding(
            dim=self.head_dim,
            max_seq_len=max_seq_len
        )

    def forward(self, hidden_states):
        batch_size, seq_len, _ = hidden_states.shape

        # Projetar para Q, K, V
        q = self.q_proj(hidden_states)
        k = self.k_proj(hidden_states)
        v = self.v_proj(hidden_states)

        # Remodelar para multi-cabeça
        q = q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        k = k.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        v = v.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        # Aplicar RoPE
        cos, sin = self.rotary_emb(seq_len, device=hidden_states.device)
        q, k = apply_rotary_pos_emb(q, k, cos, sin)

        # Atenção padrão
        attn_output = F.scaled_dot_product_attention(q, k, v)

        # Remodelar e projetar
        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.view(batch_size, seq_len, -1)
        output = self.o_proj(attn_output)

        return output
```

## Fine-tuning para Long Context

### Fine-tuning Mínimo (Position Interpolation)

```python
from transformers import Trainer, TrainingArguments

# Estender config do modelo
model.config.max_position_embeddings = 32768
model.config.rope_scaling = {"type": "linear", "factor": 16.0}

# Argumentos de treinamento (passos mínimos necessários)
training_args = TrainingArguments(
    output_dir="./llama-32k",
    num_train_epochs=1,
    max_steps=1000,           # Apenas 1000 passos!
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,
    learning_rate=2e-5,
    warmup_steps=100,
    logging_steps=10,
    save_steps=500,
)

# Treinar em documentos longos
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=long_document_dataset,  # Sequências de 32k tokens
)

trainer.train()
```

### Fine-tuning com YaRN

```bash
# Clonar implementação YaRN
git clone https://github.com/jquesnelle/yarn
cd yarn

# Fine-tunar LLaMA com YaRN
python scripts/train.py \
    --model meta-llama/Llama-2-7b-hf \
    --scale 16 \
    --rope_theta 10000 \
    --max_length 32768 \
    --batch_size 1 \
    --gradient_accumulation 16 \
    --steps 400 \
    --learning_rate 2e-5
```

## Boas Práticas

### 1. Escolher o Método Correto

```python
# Para NOVOS modelos (treinando do zero)
use_method = "ALiBi"  # Melhor extrapolação, menor memória

# Para ESTENDER modelos RoPE existentes
use_method = "YaRN"  # Extensão mais eficiente (10× menos dados)

# Para EXTENSÃO RÁPIDA com mínimo de computação
use_method = "Position Interpolation"  # 1000 passos

# Para EXTENSÃO MODERADA com boa eficiência
use_method = "Linear RoPE Scaling"  # Built-in, simples
```

### 2. Seleção do Fator de Scaling

```python
# Conservador (mais seguro, melhor qualidade)
scaling_factor = 2.0  # 8k → 16k

# Moderado (bom equilíbrio)
scaling_factor = 4.0  # 8k → 32k

# Agressivo (requer mais fine-tuning)
scaling_factor = 8.0  # 8k → 64k
scaling_factor = 16.0  # 8k → 128k

# Regra: Fatores maiores precisam de mais passos de fine-tuning
steps_needed = 100 * scaling_factor  # Estimativa aproximada
```

### 3. Dados para Fine-tuning

```python
# ✅ Bom: Documentos longos combinando comprimento alvo
train_data = [
    {"text": long_doc_32k_tokens},  # 32k completo
    {"text": long_doc_24k_tokens},  # Comprimentos variados
    {"text": long_doc_16k_tokens},
]

# ❌ Ruim: Documentos curtos (não aprenderá contexto longo)
train_data = [
    {"text": short_doc_2k_tokens},
]

# Use datasets como:
# - PG-19 (livros, textos longos)
# - Artigos arXiv
# - Conversas longas
# - Repositórios GitHub (arquivos concatenados)
```

### 4. Evitar Armadilhas Comuns

```python
# ❌ Ruim: Aplicar position interpolation sem fine-tuning
model.config.rope_scaling = {"type": "linear", "factor": 16.0}
# Modelo terá performance ruim sem fine-tuning!

# ✅ Bom: Fine-tunar após scaling
model.config.rope_scaling = {"type": "linear", "factor": 16.0}
fine_tune(model, long_documents, steps=1000)

# ❌ Ruim: Scaling muito agressivo sem dados
scale_to_1M_tokens()  # Não funcionará sem fine-tuning massivo

# ✅ Bom: Scaling incremental
# 8k → 16k → 32k → 64k (fine-tunar em cada passo)
```

## Deploy em Produção

### Inferência com Long Context

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Carregar modelo com long-context
model = AutoModelForCausalLM.from_pretrained(
    "togethercomputer/LLaMA-2-7B-32K",  # 32k de contexto
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("togethercomputer/LLaMA-2-7B-32K")

# Processar documento longo
long_text = "..." * 30000  # 30k tokens
inputs = tokenizer(long_text, return_tensors="pt", truncation=False).to('cuda')

# Gerar
outputs = model.generate(
    **inputs,
    max_new_tokens=512,
    temperature=0.7,
)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### Otimização de Memória

```python
# Usar gradient checkpointing para fine-tuning
model.gradient_checkpointing_enable()

# Usar Flash Attention 2
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    attn_implementation="flash_attention_2",  # 2-3× mais rápido
    torch_dtype=torch.float16
)

# Usar paged attention (vLLM)
from vllm import LLM

llm = LLM(
    model="togethercomputer/LLaMA-2-7B-32K",
    max_model_len=32768,  # 32k de contexto
    gpu_memory_utilization=0.9
)
```

## Recursos

- **Paper RoPE**: https://arxiv.org/abs/2104.09864 (RoFormer)
- **Paper YaRN**: https://arxiv.org/abs/2309.00071
- **Paper ALiBi**: https://arxiv.org/abs/2108.12409 (Train Short, Test Long)
- **Position Interpolation**: https://arxiv.org/abs/2306.15595
- **HuggingFace RoPE Utils**: https://github.com/huggingface/transformers/blob/main/src/transformers/modeling_rope_utils.py
- **Implementação YaRN**: https://github.com/jquesnelle/yarn
- **Blog Together AI**: https://www.together.ai/blog/llama-2-7b-32k

## Veja Também

- `references/rope.md` - Implementação detalhada e teoria de RoPE
- `references/extension_methods.md` - Comparações YaRN, ALiBi, Position Interpolation
- `references/fine_tuning.md` - Guia completo de fine-tuning para extensão de contexto