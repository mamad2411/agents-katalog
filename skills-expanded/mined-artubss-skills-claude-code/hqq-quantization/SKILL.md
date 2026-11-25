---
name: hqq-quantization
description: Quantização Half-Quadratic para LLMs sem dados de calibração. Use ao quantizar modelos com precisão 4/3/2-bit sem necessidade de conjuntos de calibração, para workflows de quantização rápida, ou ao fazer deploy com vLLM ou HuggingFace Transformers.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Quantization, HQQ, Optimization, Memory Efficiency, Inference, Model Compression]
dependencies: [hqq>=0.2.0, torch>=2.0.0]
---

# HQQ - Half-Quadratic Quantization

Quantização de pesos rápida e sem calibração, suportando precisão 8/4/3/2/1-bit com múltiplos backends otimizados.

## Quando usar HQQ

**Use HQQ quando:**
- Quantizar modelos sem dados de calibração (nenhum dataset necessário)
- Precisa de quantização rápida (minutos vs horas para GPTQ/AWQ)
- Fazer deploy com vLLM ou HuggingFace Transformers
- Fine-tuning de modelos quantizados com LoRA/PEFT
- Experimentar quantização extrema (2-bit, 1-bit)

**Principais vantagens:**
- **Sem calibração**: Quantize qualquer modelo instantaneamente sem dados de amostra
- **Múltiplos backends**: PyTorch, ATEN, TorchAO, Marlin, BitBlas para inferência otimizada
- **Precisão flexível**: 8/4/3/2/1-bit com tamanhos de grupo configuráveis
- **Integração com frameworks**: Suporte nativo para HuggingFace e vLLM
- **Compatível com PEFT**: Fine-tune modelos quantizados com LoRA

**Use alternativas no lugar:**
- **AWQ**: Quando precisa de acurácia baseada em calibração, serving em produção
- **GPTQ**: Máxima acurácia com dados de calibração disponíveis
- **bitsandbytes**: Simples 8-bit/4-bit sem backends customizados
- **llama.cpp/GGUF**: Inferência em CPU, deploy em Apple Silicon

## Início rápido

### Instalação

```bash
pip install hqq

# Com backend específico
pip install hqq[torch]      # Backend PyTorch
pip install hqq[torchao]    # Backend TorchAO int4
pip install hqq[bitblas]    # Backend BitBlas
pip install hqq[marlin]     # Backend Marlin
```

### Quantização básica

```python
from hqq.core.quantize import BaseQuantizeConfig, HQQLinear
import torch.nn as nn

# Configure quantização
config = BaseQuantizeConfig(
    nbits=4,           # Quantização 4-bit
    group_size=64,     # Tamanho do grupo para quantização
    axis=1             # Quantize ao longo da dimensão de saída
)

# Quantize uma camada linear
linear = nn.Linear(4096, 4096)
hqq_linear = HQQLinear(linear, config)

# Use normalmente
output = hqq_linear(input_tensor)
```

### Quantizar modelo completo com HuggingFace

```python
from transformers import AutoModelForCausalLM, HqqConfig

# Configure HQQ
quantization_config = HqqConfig(
    nbits=4,
    group_size=64,
    axis=1
)

# Carregue e quantize
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=quantization_config,
    device_map="auto"
)

# Modelo está quantizado e pronto para uso
```

## Conceitos principais

### Configuração de quantização

HQQ usa `BaseQuantizeConfig` para definir parâmetros de quantização:

```python
from hqq.core.quantize import BaseQuantizeConfig

# Config 4-bit padrão
config_4bit = BaseQuantizeConfig(
    nbits=4,           # Bits por peso (1-8)
    group_size=64,     # Pesos por grupo de quantização
    axis=1             # 0=dim entrada, 1=dim saída
)

# Config agressivo 2-bit
config_2bit = BaseQuantizeConfig(
    nbits=2,
    group_size=16,     # Grupos menores para baixo-bit
    axis=1
)

# Precisão mista por tipo de camada
layer_configs = {
    "self_attn.q_proj": BaseQuantizeConfig(nbits=4, group_size=64),
    "self_attn.k_proj": BaseQuantizeConfig(nbits=4, group_size=64),
    "self_attn.v_proj": BaseQuantizeConfig(nbits=4, group_size=64),
    "mlp.gate_proj": BaseQuantizeConfig(nbits=2, group_size=32),
    "mlp.up_proj": BaseQuantizeConfig(nbits=2, group_size=32),
    "mlp.down_proj": BaseQuantizeConfig(nbits=4, group_size=64),
}
```

### Camada HQQLinear

A camada quantizada principal que substitui `nn.Linear`:

```python
from hqq.core.quantize import HQQLinear
import torch

# Crie camada quantizada
linear = torch.nn.Linear(4096, 4096)
hqq_layer = HQQLinear(linear, config)

# Acesse pesos quantizados
W_q = hqq_layer.W_q           # Pesos quantizados
scale = hqq_layer.scale       # Fatores de escala
zero = hqq_layer.zero         # Pontos zero

# Dequantize para inspeção
W_dequant = hqq_layer.dequantize()
```

### Backends

HQQ suporta múltiplos backends de inferência para diferentes hardwares:

```python
from hqq.core.quantize import HQQLinear

# Backends disponíveis
backends = [
    "pytorch",          # PyTorch puro (padrão)
    "pytorch_compile",  # Otimizado com torch.compile
    "aten",            # Kernels CUDA customizados
    "torchao_int4",    # Matmul int4 TorchAO
    "gemlite",         # Kernels CUDA GemLite
    "bitblas",         # Otimizado BitBlas
    "marlin",          # Kernels 4-bit Marlin
]

# Defina backend globalmente
HQQLinear.set_backend("torchao_int4")

# Ou por camada
hqq_layer.set_backend("marlin")
```

**Guia de seleção de backend:**
| Backend | Melhor para | Requisitos |
|---------|-------------|-----------|
| pytorch | Compatibilidade | Qualquer GPU |
| pytorch_compile | Speedup moderado | torch>=2.0 |
| aten | Bom equilíbrio | GPU CUDA |
| torchao_int4 | Inferência 4-bit | torchao instalado |
| marlin | Máxima velocidade 4-bit | GPU Ampere+ |
| bitblas | Bit-widths flexíveis | bitblas instalado |

## Integração HuggingFace

### Carregue modelos pré-quantizados

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Carregue modelo HQQ-quantizado do Hub
model = AutoModelForCausalLM.from_pretrained(
    "mobiuslabsgmbh/Llama-3.1-8B-HQQ-4bit",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")

# Use normalmente
inputs = tokenizer("Hello, world!", return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=50)
```

### Quantize e salve

```python
from transformers import AutoModelForCausalLM, HqqConfig

# Quantize
config = HqqConfig(nbits=4, group_size=64)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=config,
    device_map="auto"
)

# Salve modelo quantizado
model.save_pretrained("./llama-8b-hqq-4bit")

# Faça push para Hub
model.push_to_hub("my-org/Llama-3.1-8B-HQQ-4bit")
```

### Quantização de precisão mista

```python
from transformers import AutoModelForCausalLM, HqqConfig

# Precisão diferente por tipo de camada
config = HqqConfig(
    nbits=4,
    group_size=64,
    # Camadas de atenção: precisão maior
    # Camadas MLP: precisão menor para economia de memória
    dynamic_config={
        "attn": {"nbits": 4, "group_size": 64},
        "mlp": {"nbits": 2, "group_size": 32}
    }
)
```

## Integração vLLM

### Sirva modelos HQQ com vLLM

```python
from vllm import LLM, SamplingParams

# Carregue modelo HQQ-quantizado
llm = LLM(
    model="mobiuslabsgmbh/Llama-3.1-8B-HQQ-4bit",
    quantization="hqq",
    dtype="float16"
)

# Gere
sampling_params = SamplingParams(temperature=0.7, max_tokens=100)
outputs = llm.generate(["What is machine learning?"], sampling_params)
```

### vLLM com config HQQ customizado

```python
from vllm import LLM

llm = LLM(
    model="meta-llama/Llama-3.1-8B",
    quantization="hqq",
    quantization_config={
        "nbits": 4,
        "group_size": 64
    }
)
```

## Fine-tuning PEFT/LoRA

### Fine-tune modelos quantizados

```python
from transformers import AutoModelForCausalLM, HqqConfig
from peft import LoraConfig, get_peft_model

# Carregue modelo quantizado
quant_config = HqqConfig(nbits=4, group_size=64)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=quant_config,
    device_map="auto"
)

# Aplique LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# Treine normalmente com Trainer ou loop customizado
```

### Treinamento estilo QLoRA

```python
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./hqq-lora-output",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    num_train_epochs=3,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator
)

trainer.train()
```

## Workflows de quantização

### Workflow 1: Compressão rápida de modelo

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, HqqConfig

# 1. Configure quantização
config = HqqConfig(nbits=4, group_size=64)

# 2. Carregue e quantize (sem calibração necessária!)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=config,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")

# 3. Verifique qualidade
prompt = "The capital of France is"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=20)
print(tokenizer.decode(outputs[0]))

# 4. Salve
model.save_pretrained("./llama-8b-hqq")
tokenizer.save_pretrained("./llama-8b-hqq")
```

### Workflow 2: Otimize para velocidade de inferência

```python
from hqq.core.quantize import HQQLinear
from transformers import AutoModelForCausalLM, HqqConfig

# 1. Quantize com backend ótimo
config = HqqConfig(nbits=4, group_size=64)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=config,
    device_map="auto"
)

# 2. Defina backend rápido
HQQLinear.set_backend("marlin")  # ou "torchao_int4"

# 3. Compile para speedup adicional
import torch
model = torch.compile(model)

# 4. Faça benchmark
import time
inputs = tokenizer("Hello", return_tensors="pt").to(model.device)
start = time.time()
for _ in range(10):
    model.generate(**inputs, max_new_tokens=100)
print(f"Avg time: {(time.time() - start) / 10:.2f}s")
```

## Melhores práticas

1. **Comece com 4-bit**: Melhor tradeoff qualidade/tamanho para maioria dos modelos
2. **Use group_size=64**: Bom equilíbrio; menor para quantização extrema
3. **Escolha backend com cuidado**: Marlin para 4-bit Ampere+, TorchAO para flexibilidade
4. **Verifique qualidade**: Sempre teste qualidade de geração após quantização
5. **Precisão mista**: Mantenha atenção em precisão maior, comprima MLP mais
6. **Treinamento PEFT**: Use LoRA r=16-32 para bons resultados de fine-tuning

## Problemas comuns

**Falta de memória durante quantização:**
```python
# Quantize camada por camada
from hqq.models.hf.base import AutoHQQHFModel

model = AutoHQQHFModel.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=config,
    device_map="sequential"  # Carregue camadas sequencialmente
)
```

**Inferência lenta:**
```python
# Mude para backend otimizado
from hqq.core.quantize import HQQLinear
HQQLinear.set_backend("marlin")  # Requer GPU Ampere+

# Ou compile
model = torch.compile(model, mode="reduce-overhead")
```

**Qualidade ruim em 2-bit:**
```python
# Use tamanho de grupo menor
config = BaseQuantizeConfig(
    nbits=2,
    group_size=16,  # Grupos menores ajudam em baixo-bit
    axis=1
)
```

## Referências

- **[Uso Avançado](references/advanced-usage.md)** - Backends customizados, precisão mista, otimização
- **[Resolução de problemas](references/troubleshooting.md)** - Problemas comuns, debug, benchmarks

## Recursos

- **Repositório**: https://github.com/mobiusml/hqq
- **Paper**: Half-Quadratic Quantization
- **Modelos HuggingFace**: https://huggingface.co/mobiuslabsgmbh
- **Versão**: 0.2.0+
- **Licença**: Apache 2.0