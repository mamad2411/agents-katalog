---
name: tensorrt-llm
description: Otimiza inferência de LLM com NVIDIA TensorRT para máxima vazão e latência mínima. Use para implantação em produção em GPUs NVIDIA (A100/H100), quando você precisa de inferência 10-100x mais rápida que PyTorch, ou para servir modelos com quantização (FP8/INT4), batching em voo e escalabilidade multi-GPU.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Inference Serving, TensorRT-LLM, NVIDIA, Inference Optimization, High Throughput, Low Latency, Production, FP8, INT4, In-Flight Batching, Multi-GPU]
dependencies: [tensorrt-llm, torch]
---

# TensorRT-LLM

Biblioteca open-source da NVIDIA para otimizar inferência de LLM com performance de ponta em GPUs NVIDIA.

## Quando usar TensorRT-LLM

**Use TensorRT-LLM quando:**
- Implantar em GPUs NVIDIA (A100, H100, GB200)
- Precisar de máxima vazão (24.000+ tokens/seg em Llama 3)
- Exigir baixa latência para aplicações em tempo real
- Trabalhar com modelos quantizados (FP8, INT4, FP4)
- Escalar entre múltiplas GPUs ou nós

**Use vLLM em vez disso quando:**
- Precisar de configuração mais simples e API Python-first
- Quiser PagedAttention sem compilação TensorRT
- Trabalhar com GPUs AMD ou hardware não-NVIDIA

**Use llama.cpp em vez disso quando:**
- Implantar em CPU ou Apple Silicon
- Precisar de edge deployment sem GPUs NVIDIA
- Quiser formato de quantização GGUF mais simples

## Início rápido

### Instalação

```bash
# Docker (recomendado)
docker pull nvidia/tensorrt_llm:latest

# pip install
pip install tensorrt_llm==1.2.0rc3

# Requer CUDA 13.0.0, TensorRT 10.13.2, Python 3.10-3.12
```

### Inferência básica

```python
from tensorrt_llm import LLM, SamplingParams

# Inicializar modelo
llm = LLM(model="meta-llama/Meta-Llama-3-8B")

# Configurar sampling
sampling_params = SamplingParams(
    max_tokens=100,
    temperature=0.7,
    top_p=0.9
)

# Gerar
prompts = ["Explain quantum computing"]
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(output.text)
```

### Servindo com trtllm-serve

```bash
# Iniciar servidor (download automático e compilação do modelo)
trtllm-serve meta-llama/Meta-Llama-3-8B \
    --tp_size 4 \              # Tensor parallelism (4 GPUs)
    --max_batch_size 256 \
    --max_num_tokens 4096

# Requisição do cliente
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Meta-Llama-3-8B",
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

## Recursos-chave

### Otimizações de performance
- **In-flight batching**: Batching dinâmico durante geração
- **Paged KV cache**: Gestão eficiente de memória
- **Flash Attention**: Kernels de atenção otimizados
- **Quantização**: FP8, INT4, FP4 para inferência 2-4× mais rápida
- **CUDA graphs**: Overhead reduzido de kernel launch

### Paralelismo
- **Tensor parallelism (TP)**: Dividir modelo entre GPUs
- **Pipeline parallelism (PP)**: Distribuição por camadas
- **Expert parallelism**: Para modelos Mixture-of-Experts
- **Multi-node**: Escalar além de uma única máquina

### Recursos avançados
- **Speculative decoding**: Geração mais rápida com modelos draft
- **LoRA serving**: Deploy multi-adapter eficiente
- **Disaggregated serving**: Separar prefill e geração

## Padrões comuns

### Modelo quantizado (FP8)

```python
from tensorrt_llm import LLM

# Carregar modelo quantizado FP8 (2× mais rápido, 50% menos memória)
llm = LLM(
    model="meta-llama/Meta-Llama-3-70B",
    dtype="fp8",
    max_num_tokens=8192
)

# Inferência igual a antes
outputs = llm.generate(["Summarize this article..."])
```

### Deploy multi-GPU

```python
# Tensor parallelism em 8 GPUs
llm = LLM(
    model="meta-llama/Meta-Llama-3-405B",
    tensor_parallel_size=8,
    dtype="fp8"
)
```

### Inferência em batch

```python
# Processar 100 prompts eficientemente
prompts = [f"Question {i}: ..." for i in range(100)]

outputs = llm.generate(
    prompts,
    sampling_params=SamplingParams(max_tokens=200)
)

# Batching automático em voo para máxima vazão
```

## Benchmarks de performance

**Meta Llama 3-8B** (GPU H100):
- Vazão: 24.000 tokens/seg
- Latência: ~10ms por token
- vs PyTorch: **100× mais rápido**

**Llama 3-70B** (8× A100 80GB):
- Quantização FP8: 2× mais rápido que FP16
- Memória: 50% redução com FP8

## Modelos suportados

- **Família LLaMA**: Llama 2, Llama 3, CodeLlama
- **Família GPT**: GPT-2, GPT-J, GPT-NeoX
- **Qwen**: Qwen, Qwen2, QwQ
- **DeepSeek**: DeepSeek-V2, DeepSeek-V3
- **Mixtral**: Mixtral-8x7B, Mixtral-8x22B
- **Vision**: LLaVA, Phi-3-vision
- **100+ modelos** no HuggingFace

## Referências

- **[Guia de Otimização](references/optimization.md)** - Quantização, batching, tuning de KV cache
- **[Setup Multi-GPU](references/multi-gpu.md)** - Tensor/pipeline parallelism, multi-node
- **[Guia de Serving](references/serving.md)** - Deploy em produção, monitoramento, autoscaling

## Recursos

- **Docs**: https://nvidia.github.io/TensorRT-LLM/
- **GitHub**: https://github.com/NVIDIA/TensorRT-LLM
- **Models**: https://huggingface.co/models?library=tensorrt_llm