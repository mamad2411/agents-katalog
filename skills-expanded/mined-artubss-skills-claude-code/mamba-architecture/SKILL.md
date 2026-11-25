---
name: mamba-architecture
description: Modelo de espaço de estados com complexidade O(n) versus O(n²) dos Transformers. Inferência 5× mais rápida, sequências de milhão de tokens, sem cache KV. SSM seletivo com design aware de hardware. Mamba-1 (d_state=16) e Mamba-2 (d_state=128, multi-head). Modelos 130M-2.8B no HuggingFace.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Model Architecture, Mamba, State Space Models, SSM, Linear Complexity, Long Context, Efficient Inference, Hardware-Aware, Alternative To Transformers]
dependencies: [mamba-ssm, torch, transformers, causal-conv1d]
---

# Mamba - Selective State Space Models

## Início rápido

Mamba é uma arquitetura de modelo de espaço de estados alcançando complexidade linear O(n) para modelagem de sequências.

**Instalação**:
```bash
# Instalar causal-conv1d (opcional, para eficiência)
pip install causal-conv1d>=1.4.0

# Instalar Mamba
pip install mamba-ssm
# Ou ambos juntos
pip install mamba-ssm[causal-conv1d]
```

**Pré-requisitos**: Linux, GPU NVIDIA, PyTorch 1.12+, CUDA 11.6+

**Uso básico** (bloco Mamba):
```python
import torch
from mamba_ssm import Mamba

batch, length, dim = 2, 64, 16
x = torch.randn(batch, length, dim).to("cuda")

model = Mamba(
    d_model=dim,      # Model dimension
    d_state=16,       # SSM state dimension
    d_conv=4,         # Conv1d kernel size
    expand=2          # Expansion factor
).to("cuda")

y = model(x)  # O(n) complexity!
assert y.shape == x.shape
```

## Workflows comuns

### Workflow 1: Modelo de linguagem com Mamba-2

**LM completo com geração**:
```python
from mamba_ssm.models.mixer_seq_simple import MambaLMHeadModel
from mamba_ssm.models.config_mamba import MambaConfig
import torch

# Configurar Mamba-2 LM
config = MambaConfig(
    d_model=1024,           # Hidden dimension
    n_layer=24,             # Number of layers
    vocab_size=50277,       # Vocabulary size
    ssm_cfg=dict(
        layer="Mamba2",     # Use Mamba-2
        d_state=128,        # Larger state for Mamba-2
        headdim=64,         # Head dimension
        ngroups=1           # Number of groups
    )
)

model = MambaLMHeadModel(config, device="cuda", dtype=torch.float16)

# Gerar texto
input_ids = torch.randint(0, 1000, (1, 20), device="cuda", dtype=torch.long)
output = model.generate(
    input_ids=input_ids,
    max_length=100,
    temperature=0.7,
    top_p=0.9
)
```

### Workflow 2: Usar modelos Mamba pré-treinados

**Carregar do HuggingFace**:
```python
from transformers import AutoTokenizer
from mamba_ssm.models.mixer_seq_simple import MambaLMHeadModel

# Carregar modelo pré-treinado
model_name = "state-spaces/mamba-2.8b"
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neox-20b")  # Use compatible tokenizer
model = MambaLMHeadModel.from_pretrained(model_name, device="cuda", dtype=torch.float16)

# Gerar
prompt = "The future of AI is"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
output_ids = model.generate(
    input_ids=input_ids,
    max_length=200,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.2
)
generated_text = tokenizer.decode(output_ids[0])
print(generated_text)
```

**Modelos disponíveis**:
- `state-spaces/mamba-130m`
- `state-spaces/mamba-370m`
- `state-spaces/mamba-790m`
- `state-spaces/mamba-1.4b`
- `state-spaces/mamba-2.8b`

### Workflow 3: Mamba-1 vs Mamba-2

**Mamba-1** (estado menor):
```python
from mamba_ssm import Mamba

model = Mamba(
    d_model=256,
    d_state=16,      # Smaller state dimension
    d_conv=4,
    expand=2
).to("cuda")
```

**Mamba-2** (multi-head, estado maior):
```python
from mamba_ssm import Mamba2

model = Mamba2(
    d_model=256,
    d_state=128,     # Larger state dimension
    d_conv=4,
    expand=2,
    headdim=64,      # Head dimension for multi-head
    ngroups=1        # Parallel groups
).to("cuda")
```

**Diferenças principais**:
- **Tamanho do estado**: Mamba-1 (d_state=16) vs Mamba-2 (d_state=128)
- **Arquitetura**: Mamba-2 possui estrutura multi-head
- **Normalização**: Mamba-2 usa RMSNorm
- **Distribuído**: Mamba-2 suporta tensor parallelism

### Workflow 4: Benchmark vs Transformers

**Comparação de velocidade de geração**:
```bash
# Benchmark Mamba
python benchmarks/benchmark_generation_mamba_simple.py \
  --model-name "state-spaces/mamba-2.8b" \
  --prompt "The future of machine learning is" \
  --topp 0.9 --temperature 0.7 --repetition-penalty 1.2

# Benchmark Transformer
python benchmarks/benchmark_generation_mamba_simple.py \
  --model-name "EleutherAI/pythia-2.8b" \
  --prompt "The future of machine learning is" \
  --topp 0.9 --temperature 0.7 --repetition-penalty 1.2
```

**Resultados esperados**:
- **Mamba**: Inferência 5× mais rápida
- **Memória**: Sem cache KV
- **Escalabilidade**: Linear com comprimento da sequência

## Quando usar versus alternativas

**Use Mamba quando**:
- Precisa de sequências longas (100K+ tokens)
- Quer inferência mais rápida que Transformers
- Memória limitada (sem cache KV)
- Construindo aplicações com streaming
- Escalabilidade linear é importante

**Vantagens**:
- **Complexidade O(n)**: Linear versus quadrática
- **Inferência 5× mais rápida**: Sem overhead de atenção
- **Sem cache KV**: Menor uso de memória
- **Sequências de milhão de tokens**: Hardware-eficiente
- **Streaming**: Memória constante por token

**Use alternativas em vez disso**:
- **Transformers**: Precisa de melhor desempenho, tem poder computacional
- **RWKV**: Quer híbrido RNN+Transformer
- **RetNet**: Precisa de arquitetura baseada em retenção
- **Hyena**: Quer abordagem baseada em convolução

## Problemas comuns

**Problema: CUDA sem memória**

Reduza o tamanho do batch ou use gradient checkpointing:
```python
model = MambaLMHeadModel(config, device="cuda", dtype=torch.float16)
model.gradient_checkpointing_enable()  # Enable checkpointing
```

**Problema: Instalação lenta**

Instale wheels binários (não do código-fonte):
```bash
pip install mamba-ssm --no-build-isolation
```

**Problema: causal-conv1d ausente**

Instale separadamente:
```bash
pip install causal-conv1d>=1.4.0
```

**Problema: Modelo não carrega do HuggingFace**

Use `MambaLMHeadModel.from_pretrained` (não `AutoModel`):
```python
from mamba_ssm.models.mixer_seq_simple import MambaLMHeadModel
model = MambaLMHeadModel.from_pretrained("state-spaces/mamba-2.8b")
```

## Tópicos avançados

**SSM Seletivo**: Veja [references/selective-ssm.md](references/selective-ssm.md) para formulação matemática, equações de espaço de estados e como a seletividade possibilita complexidade O(n).

**Arquitetura Mamba-2**: Veja [references/mamba2-details.md](references/mamba2-details.md) para estrutura multi-head, tensor parallelism e configuração de treinamento distribuído.

**Otimização de desempenho**: Veja [references/performance.md](references/performance.md) para design aware de hardware, kernels CUDA e técnicas de eficiência de memória.

## Requisitos de hardware

- **GPU**: NVIDIA com CUDA 11.6+
- **VRAM**:
  - Modelo 130M: 2GB
  - Modelo 370M: 4GB
  - Modelo 790M: 8GB
  - Modelo 1.4B: 14GB
  - Modelo 2.8B: 28GB (FP16)
- **Inferência**: 5× mais rápida que Transformers
- **Memória**: Sem cache KV (menor que Transformers)

**Desempenho** (vs Transformers):
- **Velocidade**: Inferência 5× mais rápida
- **Memória**: 50% menor (sem cache KV)
- **Escalabilidade**: Linear versus quadrática

## Recursos

- Paper (Mamba-1): https://arxiv.org/abs/2312.00752 (Dez 2023)
- Paper (Mamba-2): https://arxiv.org/abs/2405.21060 (Mai 2024)
- GitHub: https://github.com/state-spaces/mamba ⭐ 13,000+
- Modelos: https://huggingface.co/state-spaces
- Docs: README do repositório e wiki