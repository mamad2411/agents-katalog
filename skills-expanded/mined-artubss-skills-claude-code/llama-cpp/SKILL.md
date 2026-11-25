---
name: llama-cpp
description: Executa inferência de LLM em CPU, Apple Silicon e GPUs consumer sem hardware NVIDIA. Use para edge deployment, Macs M1/M2/M3, GPUs AMD/Intel ou quando CUDA não está disponível. Suporta quantização GGUF (1,5-8 bits) para redução de memória e aceleração de 4-10× vs PyTorch em CPU.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Inference Serving, Llama.cpp, CPU Inference, Apple Silicon, Edge Deployment, GGUF, Quantization, Non-NVIDIA, AMD GPUs, Intel GPUs, Embedded]
dependencies: [llama-cpp-python]
---

# llama.cpp

Inferência de LLM pura em C/C++ com dependências mínimas, otimizada para CPUs e hardware não-NVIDIA.

## Quando usar llama.cpp

**Use llama.cpp quando:**
- Executar em máquinas apenas com CPU
- Fazer deploy em Apple Silicon (M1/M2/M3/M4)
- Usar GPUs AMD ou Intel (sem CUDA)
- Edge deployment (Raspberry Pi, sistemas embarcados)
- Precisar de deploy simples sem Docker/Python

**Use TensorRT-LLM quando:**
- Tiver GPUs NVIDIA (A100/H100)
- Precisar de throughput máximo (100K+ tok/s)
- Rodando em datacenter com CUDA

**Use vLLM quando:**
- Tiver GPUs NVIDIA
- Precisar de API Python-first
- Quiser PagedAttention

## Guia rápido

### Instalação

```bash
# macOS/Linux
brew install llama.cpp

# Ou compilar do source
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

# Com Metal (Apple Silicon)
make LLAMA_METAL=1

# Com CUDA (NVIDIA)
make LLAMA_CUDA=1

# Com ROCm (AMD)
make LLAMA_HIP=1
```

### Baixar modelo

```bash
# Baixar do HuggingFace (formato GGUF)
huggingface-cli download \
    TheBloke/Llama-2-7B-Chat-GGUF \
    llama-2-7b-chat.Q4_K_M.gguf \
    --local-dir models/

# Ou converter do HuggingFace
python convert_hf_to_gguf.py models/llama-2-7b-chat/
```

### Executar inferência

```bash
# Chat simples
./llama-cli \
    -m models/llama-2-7b-chat.Q4_K_M.gguf \
    -p "Explain quantum computing" \
    -n 256  # Max tokens

# Chat interativo
./llama-cli \
    -m models/llama-2-7b-chat.Q4_K_M.gguf \
    --interactive
```

### Modo server

```bash
# Iniciar servidor compatível com OpenAI
./llama-server \
    -m models/llama-2-7b-chat.Q4_K_M.gguf \
    --host 0.0.0.0 \
    --port 8080 \
    -ngl 32  # Offload 32 layers to GPU

# Requisição do cliente
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-2-7b-chat",
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

## Formatos de quantização

### Visão geral do formato GGUF

| Formato | Bits | Tamanho (7B) | Velocidade | Qualidade | Caso de Uso |
|---------|------|--------------|-----------|-----------|------------|
| **Q4_K_M** | 4,5 | 4,1 GB | Rápido | Bom | **Padrão recomendado** |
| Q4_K_S | 4,3 | 3,9 GB | Mais rápido | Menor | Crítico em velocidade |
| Q5_K_M | 5,5 | 4,8 GB | Médio | Melhor | Crítico em qualidade |
| Q6_K | 6,5 | 5,5 GB | Mais lento | Melhor | Qualidade máxima |
| Q8_0 | 8,0 | 7,0 GB | Lento | Excelente | Degradação mínima |
| Q2_K | 2,5 | 2,7 GB | Mais rápido | Pobre | Apenas testes |

### Escolhendo quantização

```bash
# Uso geral (equilibrado)
Q4_K_M  # 4-bit, qualidade média

# Velocidade máxima (mais degradação)
Q2_K or Q3_K_M

# Qualidade máxima (mais lento)
Q6_K or Q8_0

# Modelos muito grandes (70B, 405B)
Q3_K_M or Q4_K_S  # Bits menores para caber na memória
```

## Aceleração de hardware

### Apple Silicon (Metal)

```bash
# Compilar com Metal
make LLAMA_METAL=1

# Executar com aceleração GPU (automático)
./llama-cli -m model.gguf -ngl 999  # Offload all layers

# Performance: M3 Max 40-60 tokens/sec (Llama 2-7B Q4_K_M)
```

### GPUs NVIDIA (CUDA)

```bash
# Compilar com CUDA
make LLAMA_CUDA=1

# Offload layers para GPU
./llama-cli -m model.gguf -ngl 35  # Offload 35/40 layers

# Híbrido CPU+GPU para modelos grandes
./llama-cli -m llama-70b.Q4_K_M.gguf -ngl 20  # GPU: 20 layers, CPU: rest
```

### GPUs AMD (ROCm)

```bash
# Compilar com ROCm
make LLAMA_HIP=1

# Executar com GPU AMD
./llama-cli -m model.gguf -ngl 999
```

## Padrões comuns

### Processamento em lote

```bash
# Processar múltiplos prompts de arquivo
cat prompts.txt | ./llama-cli \
    -m model.gguf \
    --batch-size 512 \
    -n 100
```

### Geração restrita

```bash
# Saída JSON com grammar
./llama-cli \
    -m model.gguf \
    -p "Generate a person: " \
    --grammar-file grammars/json.gbnf

# Outputs valid JSON only
```

### Tamanho de contexto

```bash
# Aumentar contexto (padrão 512)
./llama-cli \
    -m model.gguf \
    -c 4096  # 4K context window

# Contexto muito longo (se modelo suportar)
./llama-cli -m model.gguf -c 32768  # 32K context
```

## Benchmarks de performance

### Performance em CPU (Llama 2-7B Q4_K_M)

| CPU | Threads | Velocidade | Custo |
|-----|---------|-----------|-------|
| Apple M3 Max | 16 | 50 tok/s | R$ 0 (local) |
| AMD Ryzen 9 7950X | 32 | 35 tok/s | R$ 0,50/hora |
| Intel i9-13900K | 32 | 30 tok/s | R$ 0,40/hora |
| AWS c7i.16xlarge | 64 | 40 tok/s | R$ 2,88/hora |

### Aceleração por GPU (Llama 2-7B Q4_K_M)

| GPU | Velocidade | vs CPU | Custo |
|-----|-----------|--------|-------|
| NVIDIA RTX 4090 | 120 tok/s | 3-4× | R$ 0 (local) |
| NVIDIA A10 | 80 tok/s | 2-3× | R$ 1,00/hora |
| AMD MI250 | 70 tok/s | 2× | R$ 2,00/hora |
| Apple M3 Max (Metal) | 50 tok/s | ~Mesmo | R$ 0 (local) |

## Modelos suportados

**Família LLaMA**:
- Llama 2 (7B, 13B, 70B)
- Llama 3 (8B, 70B, 405B)
- Code Llama

**Família Mistral**:
- Mistral 7B
- Mixtral 8x7B, 8x22B

**Outros**:
- Falcon, BLOOM, GPT-J
- Phi-3, Gemma, Qwen
- LLaVA (vision), Whisper (audio)

**Encontrar modelos**: https://huggingface.co/models?library=gguf

## Referências

- **[Guia de Quantização](references/quantization.md)** - Formatos GGUF, conversão, comparação de qualidade
- **[Deploy de Server](references/server.md)** - Endpoints de API, Docker, monitoramento
- **[Otimização](references/optimization.md)** - Ajuste de performance, CPU+GPU híbrido

## Recursos

- **GitHub**: https://github.com/ggerganov/llama.cpp
- **Modelos**: https://huggingface.co/models?library=gguf
- **Discord**: https://discord.gg/llama-cpp