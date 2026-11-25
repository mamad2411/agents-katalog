---
name: quantizing-models-bitsandbytes
description: Quantiza LLMs para 8-bit ou 4-bit com redução de memória de 50-75% e perda mínima de acurácia. Use quando a memória GPU é limitada, precisa ajustar modelos maiores ou quer inferência mais rápida. Suporta formatos INT8, NF4, FP4, treinamento QLoRA e otimizadores 8-bit. Funciona com HuggingFace Transformers.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Optimization, Bitsandbytes, Quantization, 8-Bit, 4-Bit, Memory Optimization, QLoRA, NF4, INT8, HuggingFace, Efficient Inference]
dependencies: [bitsandbytes, transformers, accelerate, torch]
---

# bitsandbytes - Quantização de LLM

## Início rápido

bitsandbytes reduz a memória de LLM em 50% (8-bit) ou 75% (4-bit) com perda <1% de acurácia.

**Instalação**:
```bash
pip install bitsandbytes transformers accelerate
```

**Quantização 8-bit** (redução de 50% de memória):
```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

config = BitsAndBytesConfig(load_in_8bit=True)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=config,
    device_map="auto"
)

# Memória: 14GB → 7GB
```

**Quantização 4-bit** (redução de 75% de memória):
```python
config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=config,
    device_map="auto"
)

# Memória: 14GB → 3.5GB
```

## Workflows comuns

### Workflow 1: Carregar modelo grande com memória GPU limitada

Copie esta checklist:

```
Carregamento com Quantização:
- [ ] Etapa 1: Calcular requisitos de memória
- [ ] Etapa 2: Escolher nível de quantização (4-bit ou 8-bit)
- [ ] Etapa 3: Configurar quantização
- [ ] Etapa 4: Carregar e verificar modelo
```

**Etapa 1: Calcular requisitos de memória**

Estime a memória do modelo:
```
Memória FP16 (GB) = Parâmetros × 2 bytes / 1e9
Memória INT8 (GB) = Parâmetros × 1 byte / 1e9
Memória INT4 (GB) = Parâmetros × 0.5 bytes / 1e9

Exemplo (Llama 2 7B):
FP16: 7B × 2 / 1e9 = 14 GB
INT8: 7B × 1 / 1e9 = 7 GB
INT4: 7B × 0.5 / 1e9 = 3.5 GB
```

**Etapa 2: Escolher nível de quantização**

| VRAM da GPU | Tamanho do Modelo | Recomendado |
|----------|------------|-------------|
| 8 GB | 3B | 4-bit |
| 12 GB | 7B | 4-bit |
| 16 GB | 7B | 8-bit ou 4-bit |
| 24 GB | 13B | 8-bit ou 70B 4-bit |
| 40+ GB | 70B | 8-bit |

**Etapa 3: Configurar quantização**

Para 8-bit (melhor acurácia):
```python
from transformers import BitsAndBytesConfig
import torch

config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0,  # Limiar de outlier
    llm_int8_has_fp16_weight=False
)
```

Para 4-bit (economia máxima de memória):
```python
config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,  # Computar em FP16
    bnb_4bit_quant_type="nf4",  # NormalFloat4 (recomendado)
    bnb_4bit_use_double_quant=True  # Quantização aninhada
)
```

**Etapa 4: Carregar e verificar modelo**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-13b-hf",
    quantization_config=config,
    device_map="auto",  # Posicionamento automático de device
    torch_dtype=torch.float16
)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-hf")

# Teste de inferência
inputs = tokenizer("Hello, how are you?", return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_length=50)
print(tokenizer.decode(outputs[0]))

# Verificar memória
import torch
print(f"Memória alocada: {torch.cuda.memory_allocated()/1e9:.2f}GB")
```

### Workflow 2: Fine-tune com QLoRA (treinamento 4-bit)

QLoRA permite fine-tuning de modelos grandes em GPUs de consumidor.

Copie esta checklist:

```
Fine-tuning QLoRA:
- [ ] Etapa 1: Instalar dependências
- [ ] Etapa 2: Configurar modelo base 4-bit
- [ ] Etapa 3: Adicionar adaptadores LoRA
- [ ] Etapa 4: Treinar com Trainer padrão
```

**Etapa 1: Instalar dependências**

```bash
pip install bitsandbytes transformers peft accelerate datasets
```

**Etapa 2: Configurar modelo base 4-bit**

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto"
)
```

**Etapa 3: Adicionar adaptadores LoRA**

```python
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# Preparar modelo para treinamento
model = prepare_model_for_kbit_training(model)

# Configurar LoRA
lora_config = LoraConfig(
    r=16,  # Rank do LoRA
    lora_alpha=32,  # Alpha do LoRA
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Adicionar adaptadores LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Saída: trainable params: 4.2M || all params: 6.7B || trainable%: 0.06%
```

**Etapa 4: Treinar com Trainer padrão**

```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./qlora-output",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=tokenizer
)

trainer.train()

# Salvar adaptadores LoRA (apenas ~20MB)
model.save_pretrained("./qlora-adapters")
```

### Workflow 3: Otimizador 8-bit para treinamento eficiente em memória

Use Adam/AdamW 8-bit para reduzir memória do otimizador em 75%.

```
Configuração de Otimizador 8-bit:
- [ ] Etapa 1: Substituir otimizador padrão
- [ ] Etapa 2: Configurar treinamento
- [ ] Etapa 3: Monitorar economia de memória
```

**Etapa 1: Substituir otimizador padrão**

```python
import bitsandbytes as bnb
from transformers import Trainer, TrainingArguments

# Em vez de torch.optim.AdamW
model = AutoModelForCausalLM.from_pretrained("model-name")

training_args = TrainingArguments(
    output_dir="./output",
    per_device_train_batch_size=8,
    optim="paged_adamw_8bit",  # Otimizador 8-bit
    learning_rate=5e-5
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

trainer.train()
```

**Uso manual do otimizador**:
```python
import bitsandbytes as bnb

optimizer = bnb.optim.AdamW8bit(
    model.parameters(),
    lr=1e-4,
    betas=(0.9, 0.999),
    eps=1e-8
)

# Loop de treinamento
for batch in dataloader:
    loss = model(**batch).loss
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
```

**Etapa 2: Configurar treinamento**

Compare memória:
```
Memória do otimizador AdamW padrão = model_params × 8 bytes (estados)
Memória do AdamW 8-bit = model_params × 2 bytes
Economia = 75% de memória do otimizador

Exemplo (Llama 2 7B):
Padrão: 7B × 8 = 56 GB
8-bit: 7B × 2 = 14 GB
Economia: 42 GB
```

**Etapa 3: Monitorar economia de memória**

```python
import torch

before = torch.cuda.memory_allocated()

# Passo de treinamento
optimizer.step()

after = torch.cuda.memory_allocated()
print(f"Memória usada: {(after-before)/1e9:.2f}GB")
```

## Quando usar vs alternativas

**Use bitsandbytes quando:**
- Memória GPU limitada (precisa ajustar modelo maior)
- Treinamento com QLoRA (fine-tune 70B em GPU única)
- Apenas inferência (redução de 50-75% de memória)
- Usando HuggingFace Transformers
- Degradação de acurácia de 0-2% aceitável

**Use alternativas em vez disso:**
- **GPTQ/AWQ**: Serving em produção (inferência mais rápida que bitsandbytes)
- **GGUF**: Inferência em CPU (llama.cpp)
- **FP8**: GPUs H100 (FP8 de hardware mais rápido)
- **Precisão total**: Acurácia crítica, memória não restrita

## Problemas comuns

**Problema: Erro CUDA durante carregamento**

Instale versão CUDA compatível:
```bash
# Verificar versão CUDA
nvcc --version

# Instalar bitsandbytes compatível
pip install bitsandbytes --no-cache-dir
```

**Problema: Carregamento de modelo lento**

Use offload de CPU para modelos grandes:
```python
model = AutoModelForCausalLM.from_pretrained(
    "model-name",
    quantization_config=config,
    device_map="auto",
    max_memory={0: "20GB", "cpu": "30GB"}  # Offload para CPU
)
```

**Problema: Acurácia menor que esperado**

Tente 8-bit em vez de 4-bit:
```python
config = BitsAndBytesConfig(load_in_8bit=True)
# 8-bit tem <0.5% perda de acurácia vs 1-2% para 4-bit
```

Ou use NF4 com quantização dupla:
```python
config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",  # Melhor que fp4
    bnb_4bit_use_double_quant=True  # Acurácia extra
)
```

**Problema: OOM mesmo com 4-bit**

Ativar offload de CPU:
```python
model = AutoModelForCausalLM.from_pretrained(
    "model-name",
    quantization_config=config,
    device_map="auto",
    offload_folder="offload",  # Offload para disco
    offload_state_dict=True
)
```

## Tópicos avançados

**Guia de treinamento QLoRA**: Veja [references/qlora-training.md](references/qlora-training.md) para workflows de fine-tuning completos, ajuste de hiperparâmetros e treinamento multi-GPU.

**Formatos de quantização**: Veja [references/quantization-formats.md](references/quantization-formats.md) para comparação INT8, NF4, FP4, quantização dupla e configs de quantização customizadas.

**Otimização de memória**: Veja [references/memory-optimization.md](references/memory-optimization.md) para estratégias de offload de CPU, gradient checkpointing e profiling de memória.

## Requisitos de hardware

- **GPU**: NVIDIA com compute capability 7.0+ (Turing, Ampere, Hopper)
- **VRAM**: Depende do modelo e quantização
  - 4-bit Llama 2 7B: 4GB
  - 4-bit Llama 2 13B: 8GB
  - 4-bit Llama 2 70B: 24GB
- **CUDA**: 11.1+ (12.0+ recomendado)
- **PyTorch**: 2.0+

**Plataformas suportadas**: GPUs NVIDIA (primária), AMD ROCm, Intel GPUs (experimental)

## Recursos

- GitHub: https://github.com/bitsandbytes-foundation/bitsandbytes
- Docs HuggingFace: https://huggingface.co/docs/transformers/quantization/bitsandbytes
- Paper QLoRA: "QLoRA: Efficient Finetuning of Quantized LLMs" (2023)
- Paper LLM.int8(): "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale" (2022)