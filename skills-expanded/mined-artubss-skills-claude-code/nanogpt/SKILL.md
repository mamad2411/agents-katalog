---
name: nanogpt
description: Implementação educacional do GPT em ~300 linhas. Reproduz o GPT-2 (124M) em OpenWebText. Código limpo e hackeável para aprender transformers. Por Andrej Karpathy. Perfeito para entender a arquitetura do GPT do zero. Treine em Shakespeare (CPU) ou OpenWebText (multi-GPU).
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Model Architecture, NanoGPT, GPT-2, Educational, Andrej Karpathy, Transformer, Minimalist, From Scratch, Training]
dependencies: [torch, transformers, datasets, tiktoken, wandb]
---

# nanoGPT - Treinamento GPT Minimalista

## Início rápido

nanoGPT é uma implementação simplificada do GPT projetada para aprendizado e experimentação.

**Instalação**:
```bash
pip install torch numpy transformers datasets tiktoken wandb tqdm
```

**Treine em Shakespeare** (amigável a CPU):
```bash
# Preparar dados
python data/shakespeare_char/prepare.py

# Treinar (5 minutos em CPU)
python train.py config/train_shakespeare_char.py

# Gerar texto
python sample.py --out_dir=out-shakespeare-char
```

**Saída**:
```
ROMEO:
What say'st thou? Shall I speak, and be a man?

JULIET:
I am afeard, and yet I'll speak; for thou art
One that hath been a man, and yet I know not
What thou art.
```

## Workflows comuns

### Workflow 1: Shakespeare em nível de caractere

**Pipeline completo de treinamento**:
```bash
# Passo 1: Preparar dados (cria train.bin, val.bin)
python data/shakespeare_char/prepare.py

# Passo 2: Treinar modelo pequeno
python train.py config/train_shakespeare_char.py

# Passo 3: Gerar texto
python sample.py --out_dir=out-shakespeare-char
```

**Configuração** (`config/train_shakespeare_char.py`):
```python
# Configuração do modelo
n_layer = 6          # 6 camadas transformer
n_head = 6           # 6 cabeças de atenção
n_embd = 384         # embeddings com dimensão 384
block_size = 256     # contexto de 256 caracteres

# Configuração de treinamento
batch_size = 64
learning_rate = 1e-3
max_iters = 5000
eval_interval = 500

# Hardware
device = 'cpu'  # Ou 'cuda'
compile = False # Defina como True para PyTorch 2.0
```

**Tempo de treinamento**: ~5 minutos (CPU), ~1 minuto (GPU)

### Workflow 2: Reproduza GPT-2 (124M)

**Treinamento multi-GPU em OpenWebText**:
```bash
# Passo 1: Preparar OpenWebText (leva ~1 hora)
python data/openwebtext/prepare.py

# Passo 2: Treinar GPT-2 124M com DDP (8 GPUs)
torchrun --standalone --nproc_per_node=8 \
  train.py config/train_gpt2.py

# Passo 3: Amostra do modelo treinado
python sample.py --out_dir=out
```

**Configuração** (`config/train_gpt2.py`):
```python
# Arquitetura GPT-2 (124M)
n_layer = 12
n_head = 12
n_embd = 768
block_size = 1024
dropout = 0.0

# Treinamento
batch_size = 12
gradient_accumulation_steps = 5 * 8  # Batch efetivo ~0.5M tokens
learning_rate = 6e-4
max_iters = 600000
lr_decay_iters = 600000

# Sistema
compile = True  # PyTorch 2.0
```

**Tempo de treinamento**: ~4 dias (8× A100)

### Workflow 3: Fine-tune GPT-2 pré-treinado

**Começar a partir do checkpoint OpenAI**:
```python
# Em train.py ou config
init_from = 'gpt2'  # Opções: gpt2, gpt2-medium, gpt2-large, gpt2-xl

# Modelo carrega pesos OpenAI automaticamente
python train.py config/finetune_shakespeare.py
```

**Config de exemplo** (`config/finetune_shakespeare.py`):
```python
# Começar a partir do GPT-2
init_from = 'gpt2'

# Dataset
dataset = 'shakespeare_char'
batch_size = 1
block_size = 1024

# Fine-tuning
learning_rate = 3e-5  # LR mais baixa para fine-tuning
max_iters = 2000
warmup_iters = 100

# Regularização
weight_decay = 1e-1
```

### Workflow 4: Dataset customizado

**Treine em seu próprio texto**:
```python
# data/custom/prepare.py
import numpy as np

# Carregue seus dados
with open('my_data.txt', 'r') as f:
    text = f.read()

# Crie mapeamentos de caracteres
chars = sorted(list(set(text)))
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

# Tokenize
data = np.array([stoi[ch] for ch in text], dtype=np.uint16)

# Divida train/val
n = len(data)
train_data = data[:int(n*0.9)]
val_data = data[int(n*0.9):]

# Salve
train_data.tofile('data/custom/train.bin')
val_data.tofile('data/custom/val.bin')
```

**Treine**:
```bash
python data/custom/prepare.py
python train.py --dataset=custom
```

## Quando usar vs alternativas

**Use nanoGPT quando**:
- Aprender como GPT funciona
- Experimentar variantes de transformer
- Fins educacionais/ensino
- Prototipagem rápida
- Computação limitada (pode rodar em CPU)

**Vantagens de simplicidade**:
- **~300 linhas**: Modelo inteiro em `model.py`
- **~300 linhas**: Loop de treinamento em `train.py`
- **Hackeável**: Fácil de modificar
- **Sem abstrações**: PyTorch puro

**Use alternativas em vez disso**:
- **HuggingFace Transformers**: Uso em produção, muitos modelos
- **Megatron-LM**: Treinamento distribuído em larga escala
- **LitGPT**: Mais arquiteturas, pronto para produção
- **PyTorch Lightning**: Precisa de framework de alto nível

## Problemas comuns

**Problema: CUDA fora de memória**

Reduza tamanho de batch ou comprimento de contexto:
```python
batch_size = 1  # Reduza de 12
block_size = 512  # Reduza de 1024
gradient_accumulation_steps = 40  # Aumente para manter batch efetivo
```

**Problema: Treinamento muito lento**

Ative compilação (PyTorch 2.0+):
```python
compile = True  # Speedup de 2×
```

Use precisão mista:
```python
dtype = 'bfloat16'  # Ou 'float16'
```

**Problema: Qualidade de geração ruim**

Treine por mais tempo:
```python
max_iters = 10000  # Aumente de 5000
```

Reduza temperatura:
```python
# Em sample.py
temperature = 0.7  # Reduza de 1.0
top_k = 200       # Adicione amostragem top-k
```

**Problema: Não consegue carregar pesos GPT-2**

Instale transformers:
```bash
pip install transformers
```

Verifique nome do modelo:
```python
init_from = 'gpt2'  # Válido: gpt2, gpt2-medium, gpt2-large, gpt2-xl
```

## Tópicos avançados

**Arquitetura do modelo**: Veja [references/architecture.md](references/architecture.md) para estrutura de bloco GPT, atenção multi-cabeça e camadas MLP explicadas de forma simples.

**Loop de treinamento**: Veja [references/training.md](references/training.md) para agenda de taxa de aprendizado, acúmulo de gradiente e configuração distribuída de paralelismo de dados.

**Preparação de dados**: Veja [references/data.md](references/data.md) para estratégias de tokenização (nível de caractere vs BPE) e detalhes do formato binário.

## Requisitos de hardware

- **Shakespeare (nível de caractere)**:
  - CPU: 5 minutos
  - GPU (T4): 1 minuto
  - VRAM: <1GB

- **GPT-2 (124M)**:
  - 1× A100: ~1 semana
  - 8× A100: ~4 dias
  - VRAM: ~16GB por GPU

- **GPT-2 Medium (350M)**:
  - 8× A100: ~2 semanas
  - VRAM: ~40GB por GPU

**Performance**:
- Com `compile=True`: speedup de 2×
- Com `dtype=bfloat16`: redução de 50% em memória

## Recursos

- GitHub: https://github.com/karpathy/nanoGPT ⭐ 48.000+
- Vídeo: "Let's build GPT" por Andrej Karpathy
- Paper: "Attention is All You Need" (Vaswani et al.)
- OpenWebText: https://huggingface.co/datasets/Skylion007/openwebtext
- Educacional: Melhor para entender transformers do zero