---
name: awq-quantization
description: Quantização de pesos consciente da ativação para compressão de LLM de 4-bit com aceleração 3x e perda mínima de acurácia. Use ao implantar modelos grandes (7B-70B) em memória GPU limitada, quando precisa de inferência mais rápida que GPTQ com melhor preservação de acurácia, ou para modelos com instruções ajustadas e multimodais. Vencedor do Prêmio Melhor Artigo MLSys 2024.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Optimization, AWQ, Quantization, 4-Bit, Activation-Aware, Memory Optimization, Fast Inference, vLLM Integration, Marlin Kernels]
dependencies: [autoawq, transformers>=4.45.0, torch>=2.0.0]
---

# AWQ (Activation-aware Weight Quantization)

Quantização de 4-bit que preserva pesos salientes com base em padrões de ativação, alcançando aceleração 3x com perda mínima de acurácia.

## Quando usar AWQ

**Use AWQ quando:**
- Precisar de quantização de 4-bit com <5% de perda de acurácia
- Implantando modelos com instruções ajustadas ou chat (AWQ generaliza melhor)
- Quiser aceleração de ~2,5-3x na inferência em relação a FP16
- Usando vLLM para serving em produção
- Tiver GPUs Ampere+ (A100, H100, RTX 40xx) para suporte a kernel Marlin

**Use GPTQ em vez disso quando:**
- Precisar de compatibilidade máxima de ecossistema (mais ferramentas suportam GPTQ)
- Trabalhando especificamente com backend ExLlamaV2
- Tiver GPUs mais antigas sem suporte a Marlin

**Use bitsandbytes em vez disso quando:**
- Precisar de zero overhead de calibração (quantizar na hora)
- Quiser ajustar com QLoRA
- Preferir integração mais simples

## Início rápido

### Instalação

```bash
# Padrão (kernels Triton)
pip install autoawq

# Com kernels CUDA otimizados + Flash Attention
pip install autoawq[kernels]

# Otimização Intel CPU/XPU
pip install autoawq[cpu]
```

**Requisitos**: Python 3.8+, CUDA 11.8+, Compute Capability 7.5+

### Carregar modelo pré-quantizado

```python
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

model_name = "TheBloke/Mistral-7B-Instruct-v0.2-AWQ"

model = AutoAWQForCausalLM.from_quantized(
    model_name,
    fuse_layers=True  # Enable fused attention for speed
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Generate
inputs = tokenizer("Explain quantum computing", return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### Quantizar seu próprio modelo

```python
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

model_path = "mistralai/Mistral-7B-Instruct-v0.2"

# Load model and tokenizer
model = AutoAWQForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Quantization config
quant_config = {
    "zero_point": True,      # Use zero-point quantization
    "q_group_size": 128,     # Group size (128 recommended)
    "w_bit": 4,              # 4-bit weights
    "version": "GEMM"        # GEMM for batch, GEMV for single-token
}

# Quantize (uses pileval dataset by default)
model.quantize(tokenizer, quant_config=quant_config)

# Save
model.save_quantized("mistral-7b-awq")
tokenizer.save_pretrained("mistral-7b-awq")
```

**Tempo**: ~10-15 min para modelos 7B, ~1 hora para modelos 70B.

## AWQ vs GPTQ vs bitsandbytes

| Recurso | AWQ | GPTQ | bitsandbytes |
|---------|-----|------|--------------|
| **Aceleração (4-bit)** | ~2,5-3x | ~2x | ~1,5x |
| **Perda de acurácia** | <5% | ~5-10% | ~5-15% |
| **Calibração** | Mínima (128-1K tokens) | Mais extensa | Nenhuma |
| **Risco de overfitting** | Baixo | Mais alto | N/A |
| **Melhor para** | Inferência em produção | Inferência GPU | Integração fácil |
| **Suporte vLLM** | Nativo | Sim | Limitado |

**Insight principal**: AWQ assume que nem todos os pesos são igualmente importantes. Ele protege ~1% de pesos salientes identificados por padrões de ativação, reduzindo erro de quantização sem overhead de precisão mista.

## Backends de kernel

### GEMM (padrão, inferência em lote)

```python
quant_config = {
    "zero_point": True,
    "q_group_size": 128,
    "w_bit": 4,
    "version": "GEMM"  # Best for batch sizes > 1
}
```

### GEMV (geração de token único)

```python
quant_config = {
    "version": "GEMV"  # 20% faster for batch_size=1
}
```

**Limitação**: Apenas tamanho de lote 1, não é bom para contexto grande.

### Marlin (GPUs Ampere+)

```python
from transformers import AwqConfig, AutoModelForCausalLM

config = AwqConfig(
    bits=4,
    version="marlin"  # 2x faster on A100/H100
)

model = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Mistral-7B-AWQ",
    quantization_config=config
)
```

**Requisitos**: Compute Capability 8.0+ (A100, H100, RTX 40xx)

### ExLlamaV2 (compatível com AMD)

```python
config = AwqConfig(
    bits=4,
    version="exllama"  # Faster prefill, AMD GPU support
)
```

## Integração HuggingFace Transformers

### Carregamento direto

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "TheBloke/zephyr-7B-alpha-AWQ",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("TheBloke/zephyr-7B-alpha-AWQ")
```

### Módulos fundidos (recomendado)

```python
from transformers import AwqConfig, AutoModelForCausalLM

config = AwqConfig(
    bits=4,
    fuse_max_seq_len=512,  # Max sequence length for fusing
    do_fuse=True           # Enable fused attention/MLP
)

model = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Mistral-7B-OpenOrca-AWQ",
    quantization_config=config
)
```

**Nota**: Módulos fundidos não podem ser combinados com FlashAttention2.

## Integração vLLM

```python
from vllm import LLM, SamplingParams

# vLLM auto-detects AWQ models
llm = LLM(
    model="TheBloke/Llama-2-7B-AWQ",
    quantization="awq",
    dtype="half"
)

sampling = SamplingParams(temperature=0.7, max_tokens=200)
outputs = llm.generate(["Explain AI"], sampling)
```

## Benchmarks de desempenho

### Redução de memória

| Modelo | FP16 | AWQ 4-bit | Redução |
|--------|------|-----------|---------|
| Mistral 7B | 14 GB | 5,5 GB | 2,5x |
| Llama 2-13B | 26 GB | 10 GB | 2,6x |
| Llama 2-70B | 140 GB | 35 GB | 4x |

### Velocidade de inferência (RTX 4090)

| Modelo | Prefill (tok/s) | Decode (tok/s) | Memória |
|--------|-----------------|----------------|---------|
| Mistral 7B GEMM | 3.897 | 114 | 5,55 GB |
| TinyLlama 1B GEMV | 5.179 | 431 | 2,10 GB |
| Llama 2-13B GEMM | 2.279 | 74 | 10,28 GB |

### Acurácia (perplexity)

| Modelo | FP16 | AWQ 4-bit | Degradação |
|--------|------|-----------|------------|
| Llama 3 8B | 8,20 | 8,48 | +3,4% |
| Mistral 7B | 5,25 | 5,42 | +3,2% |
| Qwen2 72B | 4,85 | 4,95 | +2,1% |

## Calibração personalizada

```python
# Use custom dataset for domain-specific models
model.quantize(
    tokenizer,
    quant_config=quant_config,
    calib_data="wikitext",       # Or custom list of strings
    max_calib_samples=256,       # More samples = better accuracy
    max_calib_seq_len=512        # Sequence length
)

# Or provide your own samples
calib_samples = [
    "Your domain-specific text here...",
    "More examples from your use case...",
]
model.quantize(tokenizer, quant_config=quant_config, calib_data=calib_samples)
```

## Implantação multi-GPU

```python
model = AutoAWQForCausalLM.from_quantized(
    "TheBloke/Llama-2-70B-AWQ",
    device_map="auto",  # Auto-split across GPUs
    max_memory={0: "40GB", 1: "40GB"}
)
```

## Modelos suportados

35+ arquiteturas incluindo:
- **Família Llama**: Llama 2/3, Code Llama, Mistral, Mixtral
- **Qwen**: Qwen, Qwen2, Qwen2.5-VL
- **Outros**: Falcon, MPT, Phi, Yi, DeepSeek, Gemma
- **Multimodal**: LLaVA, LLaVA-Next, Qwen2-VL

## Problemas comuns

**CUDA OOM durante quantização**:
```python
# Reduce batch size
model.quantize(tokenizer, quant_config=quant_config, max_calib_samples=64)
```

**Inferência lenta**:
```python
# Enable fused layers
model = AutoAWQForCausalLM.from_quantized(model_name, fuse_layers=True)
```

**Suporte GPU AMD**:
```python
# Use ExLlama backend
config = AwqConfig(bits=4, version="exllama")
```

## Aviso de descontinuação

AutoAWQ está oficialmente descontinuado. Para novos projetos, considere:
- **vLLM llm-compressor**: https://github.com/vllm-project/llm-compressor
- **MLX-LM**: Para dispositivos Mac com Apple Silicon

Modelos quantizados existentes continuam utilizáveis.

## Referências

- **Artigo**: AWQ: Activation-aware Weight Quantization (arXiv:2306.00978) - Melhor Artigo MLSys 2024
- **GitHub**: https://github.com/casper-hansen/AutoAWQ
- **MIT Han Lab**: https://github.com/mit-han-lab/llm-awq
- **Modelos**: https://huggingface.co/models?library=awq