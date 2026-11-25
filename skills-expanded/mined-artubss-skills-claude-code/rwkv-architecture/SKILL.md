---
name: rwkv-architecture
description: Híbrido RNN+Transformer com inferência O(n). Tempo linear, contexto infinito, sem cache KV. Treina como GPT (paralelo), infere como RNN (sequencial). Projeto Linux Foundation AI. Produção em Windows, Office, NeMo. RWKV-7 (março de 2025). Modelos até 14B parâmetros.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [RWKV, Model Architecture, RNN, Transformer Hybrid, Linear Complexity, Infinite Context, Efficient Inference, Linux Foundation, Alternative Architecture]
dependencies: [rwkv, torch, transformers]
---

# RWKV - Receptance Weighted Key Value

## Início rápido

RWKV (RwaKuv) combina paralelização de Transformers (treinamento) com eficiência de RNN (inferência).

**Instalação**:
```bash
# Instalar PyTorch
pip install torch --upgrade --extra-index-url https://download.pytorch.org/whl/cu121

# Instalar dependências
pip install pytorch-lightning==1.9.5 deepspeed wandb ninja --upgrade

# Instalar RWKV
pip install rwkv
```

**Uso básico** (modo GPT + modo RNN):
```python
import os
from rwkv.model import RWKV

os.environ["RWKV_JIT_ON"] = '1'
os.environ["RWKV_CUDA_ON"] = '1'  # Use kernel CUDA para velocidade

# Carregar modelo
model = RWKV(
    model='/path/to/RWKV-4-Pile-1B5-20220903-8040',
    strategy='cuda fp16'
)

# Modo GPT (processamento paralelo)
out, state = model.forward([187, 510, 1563, 310, 247], None)
print(out.detach().cpu().numpy())  # Logits

# Modo RNN (processamento sequencial, mesmo resultado)
out, state = model.forward([187, 510], None)  # Primeiros 2 tokens
out, state = model.forward([1563], state)      # Próximo token
out, state = model.forward([310, 247], state)  # Últimos tokens
print(out.detach().cpu().numpy())  # Mesmos logits de cima!
```

## Fluxos de trabalho comuns

### Fluxo 1: Geração de texto (streaming)

**Geração eficiente token por token**:
```python
from rwkv.model import RWKV
from rwkv.utils import PIPELINE

model = RWKV(model='RWKV-4-Pile-14B-20230313-ctx8192-test1050', strategy='cuda fp16')
pipeline = PIPELINE(model, "20B_tokenizer.json")

# Prompt inicial
prompt = "The future of AI is"
state = None

# Gerar token por token
for token in prompt:
    out, state = pipeline.model.forward(pipeline.encode(token), state)

# Continuar geração
for _ in range(100):
    out, state = pipeline.model.forward(None, state)
    token = pipeline.sample_logits(out)
    print(pipeline.decode(token), end='', flush=True)
```

**Vantagem principal**: Memória constante por token (sem cache KV crescente)

### Fluxo 2: Processamento de contexto longo (contexto infinito)

**Processar sequências com milhões de tokens**:
```python
model = RWKV(model='RWKV-4-Pile-14B', strategy='cuda fp16')

# Processar documento muito longo
state = None
long_document = load_document()  # ex: 1M tokens

# Processar todo documento
for chunk in chunks(long_document, chunk_size=1024):
    out, state = model.forward(chunk, state)

# State agora contém informações de todo o documento com 1M tokens
# Uso de memória: O(1) (constante, não O(n)!)
```

### Fluxo 3: Fine-tuning RWKV

**Fluxo de fine-tuning padrão**:
```python
# Script de treinamento
import pytorch_lightning as pl
from rwkv.model import RWKV
from rwkv.trainer import RWKVTrainer

# Configurar modelo
config = {
    'n_layer': 24,
    'n_embd': 1024,
    'vocab_size': 50277,
    'ctx_len': 1024
}

# Configurar trainer
trainer = pl.Trainer(
    accelerator='gpu',
    devices=8,
    precision='bf16',
    strategy='deepspeed_stage_2',
    max_epochs=1
)

# Treinar
model = RWKV(config)
trainer.fit(model, train_dataloader)
```

### Fluxo 4: Comparação RWKV vs Transformer

**Comparação de memória** (sequência de 1M tokens):
```python
# Transformer (GPT)
# Memória: O(n²) para atenção
# Cache KV: 1M × hidden_dim × n_layers × 2 (chaves + valores)
# Exemplo: 1M × 4096 × 24 × 2 = ~400GB (impraticável!)

# RWKV
# Memória: O(1) por token
# State: hidden_dim × n_layers = 4096 × 24 = ~400KB
# 1.000.000× mais eficiente!
```

**Comparação de velocidade** (inferência):
```python
# Transformer: O(n) por token (quadrático no geral)
# Primeiro token: 1 computação
# Segundo token: 2 computações
# ...
# 1000º token: 1000 computações

# RWKV: O(1) por token (linear no geral)
# Cada token: 1 computação
# 1000º token: 1 computação (igual ao primeiro!)
```

## Quando usar vs alternativas

**Use RWKV quando**:
- Precisar de contexto muito longo (100K+ tokens)
- Quiser uso de memória constante
- Estiver construindo aplicações com streaming
- Precisar de eficiência RNN com performance Transformer
- Tiver restrições de memória no deployment

**Principais vantagens**:
- **Tempo linear**: O(n) vs O(n²) para Transformers
- **Sem cache KV**: Memória constante por token
- **Contexto infinito**: Sem limite de janela fixa
- **Treinamento paralelizável**: Como GPT
- **Inferência sequencial**: Como RNN

**Use alternativas em vez disso**:
- **Transformers**: Precisa da melhor performance absoluta, tem poder computacional
- **Mamba**: Quer modelos de espaço de estados
- **RetNet**: Precisa de mecanismo de retenção
- **Hyena**: Quer abordagem baseada em convolução

## Problemas comuns

**Problema: Falta de memória durante treinamento**

Use gradient checkpointing e DeepSpeed:
```python
trainer = pl.Trainer(
    strategy='deepspeed_stage_3',  # ZeRO-3 completo
    precision='bf16'
)
```

**Problema: Inferência lenta**

Ative kernel CUDA:
```python
os.environ["RWKV_CUDA_ON"] = '1'
```

**Problema: Modelo não carrega**

Verifique o caminho do modelo e estratégia:
```python
model = RWKV(
    model='/absolute/path/to/model.pth',
    strategy='cuda fp16'  # Ou 'cpu fp32' para CPU
)
```

**Problema: Gerenciamento de state em modo RNN**

Sempre passe state entre chamadas forward:
```python
# ERRADO: State perdido
out1, _ = model.forward(tokens1, None)
out2, _ = model.forward(tokens2, None)  # Sem contexto de tokens1!

# CORRETO: State preservado
out1, state = model.forward(tokens1, None)
out2, state = model.forward(tokens2, state)  # Tem contexto de tokens1
```

## Tópicos avançados

**Time-mixing e channel-mixing**: Veja [references/architecture-details.md](references/architecture-details.md) para operação WKV, mecanismo de time-decay e gates de receptância.

**Gerenciamento de state**: Veja [references/state-management.md](references/state-management.md) para states att_x_prev, att_kv, ffn_x_prev e considerações de estabilidade numérica.

**Melhorias RWKV-7**: Veja [references/rwkv7.md](references/rwkv7.md) para as últimas melhorias arquiteturais (março de 2025) e capacidades multimodais.

## Requisitos de hardware

- **GPU**: NVIDIA (CUDA 11.6+) ou CPU
- **VRAM** (FP16):
  - Modelo 169M: 1GB
  - Modelo 430M: 2GB
  - Modelo 1.5B: 4GB
  - Modelo 3B: 8GB
  - Modelo 7B: 16GB
  - Modelo 14B: 32GB
- **Inferência**: Memória O(1) por token
- **Treinamento**: Paralelizável como GPT

**Performance** (vs Transformers):
- **Velocidade**: Treinamento similar, inferência mais rápida
- **Memória**: 1000× menos para sequências longas
- **Escalabilidade**: Linear vs quadrática

## Recursos

- Paper (RWKV): https://arxiv.org/abs/2305.13048 (maio de 2023)
- Paper (RWKV-7): https://arxiv.org/abs/2503.14456 (março de 2025)
- GitHub: https://github.com/BlinkDL/RWKV-LM ⭐ 12.000+
- Docs: https://wiki.rwkv.com/
- Modelos: https://huggingface.co/BlinkDL
- Linux Foundation AI: Projeto oficial
- Produção: Integração Microsoft Windows, Office, suporte NeMo