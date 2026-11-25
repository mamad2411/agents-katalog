---
name: gguf-quantization
description: Formato GGUF e quantização llama.cpp para inferência eficiente em CPU/GPU. Use ao implantar modelos em hardware de consumidor, Apple Silicon, ou quando precisar de quantização flexível de 2-8 bits sem requisitos de GPU.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [GGUF, Quantization, llama.cpp, CPU Inference, Apple Silicon, Model Compression, Optimization]
dependencies: [llama-cpp-python>=0.2.0]
---

# GGUF - Formato de Quantização para llama.cpp

GGUF (GPT-Generated Unified Format) é o formato de arquivo padrão para llama.cpp, permitindo inferência eficiente em CPUs, Apple Silicon e GPUs com opções de quantização flexível.

## Quando usar GGUF

**Use GGUF quando:**
- Implantando em hardware de consumidor (laptops, desktops)
- Executando em Apple Silicon (M1/M2/M3) com aceleração Metal
- Precisar de inferência em CPU sem requisitos de GPU
- Quiser quantização flexível (Q2_K a Q8_0)
- Usando ferramentas locais de IA (LM Studio, Ollama, text-generation-webui)

**Principais vantagens:**
- **Hardware universal**: Suporte para CPU, Apple Silicon, NVIDIA, AMD
- **Sem runtime Python**: Inferência pura em C/C++
- **Quantização flexível**: 2-8 bits com vários métodos (K-quants)
- **Suporte do ecossistema**: LM Studio, Ollama, koboldcpp e outros
- **imatrix**: Matriz de importância para melhor qualidade em bits baixos

**Use alternativas em vez disso:**
- **AWQ/GPTQ**: Máxima precisão com calibração em GPUs NVIDIA
- **HQQ**: Quantização rápida sem calibração para HuggingFace
- **bitsandbytes**: Integração simples com a biblioteca transformers
- **TensorRT-LLM**: Implantação NVIDIA em produção com máxima velocidade

## Início rápido

### Instalação

```bash
# Clone llama.cpp
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# Build (CPU)
make

# Build com CUDA (NVIDIA)
make GGML_CUDA=1

# Build com Metal (Apple Silicon)
make GGML_METAL=1

# Instalar bindings Python (opcional)
pip install llama-cpp-python
```

### Converter modelo para GGUF

```bash
# Instalar requisitos
pip install -r requirements.txt

# Converter modelo HuggingFace para GGUF (FP16)
python convert_hf_to_gguf.py ./path/to/model --outfile model-f16.gguf

# Ou especificar tipo de saída
python convert_hf_to_gguf.py ./path/to/model \
    --outfile model-f16.gguf \
    --outtype f16
```

### Quantizar modelo

```bash
# Quantização básica para Q4_K_M
./llama-quantize model-f16.gguf model-q4_k_m.gguf Q4_K_M

# Quantizar com matriz de importância (melhor qualidade)
./llama-imatrix -m model-f16.gguf -f calibration.txt -o model.imatrix
./llama-quantize --imatrix model.imatrix model-f16.gguf model-q4_k_m.gguf Q4_K_M
```

### Executar inferência

```bash
# Inferência CLI
./llama-cli -m model-q4_k_m.gguf -p "Hello, how are you?"

# Modo interativo
./llama-cli -m model-q4_k_m.gguf --interactive

# Com offload de GPU
./llama-cli -m model-q4_k_m.gguf -ngl 35 -p "Hello!"
```

## Tipos de quantização

### Métodos K-quant (recomendados)

| Tipo | Bits | Tamanho (7B) | Qualidade | Caso de Uso |
|------|------|--------------|-----------|------------|
| Q2_K | 2.5 | ~2.8 GB | Baixa | Compressão extrema |
| Q3_K_S | 3.0 | ~3.0 GB | Baixa-Med | Memória limitada |
| Q3_K_M | 3.3 | ~3.3 GB | Média | Equilíbrio |
| Q4_K_S | 4.0 | ~3.8 GB | Med-Alta | Bom equilíbrio |
| Q4_K_M | 4.5 | ~4.1 GB | Alta | **Padrão recomendado** |
| Q5_K_S | 5.0 | ~4.6 GB | Alta | Focado em qualidade |
| Q5_K_M | 5.5 | ~4.8 GB | Muito Alta | Alta qualidade |
| Q6_K | 6.0 | ~5.5 GB | Excelente | Próximo ao original |
| Q8_0 | 8.0 | ~7.2 GB | Melhor | Máxima qualidade |

### Métodos herdados

| Tipo | Descrição |
|------|-----------|
| Q4_0 | 4-bit, básico |
| Q4_1 | 4-bit com delta |
| Q5_0 | 5-bit, básico |
| Q5_1 | 5-bit com delta |

**Recomendação**: Use métodos K-quant (Q4_K_M, Q5_K_M) para melhor proporção qualidade/tamanho.

## Fluxos de conversão

### Fluxo 1: HuggingFace para GGUF

```bash
# 1. Baixar modelo
huggingface-cli download meta-llama/Llama-3.1-8B --local-dir ./llama-3.1-8b

# 2. Converter para GGUF (FP16)
python convert_hf_to_gguf.py ./llama-3.1-8b \
    --outfile llama-3.1-8b-f16.gguf \
    --outtype f16

# 3. Quantizar
./llama-quantize llama-3.1-8b-f16.gguf llama-3.1-8b-q4_k_m.gguf Q4_K_M

# 4. Testar
./llama-cli -m llama-3.1-8b-q4_k_m.gguf -p "Hello!" -n 50
```

### Fluxo 2: Com matriz de importância (melhor qualidade)

```bash
# 1. Converter para GGUF
python convert_hf_to_gguf.py ./model --outfile model-f16.gguf

# 2. Criar texto de calibração (amostras diversas)
cat > calibration.txt << 'EOF'
The quick brown fox jumps over the lazy dog.
Machine learning is a subset of artificial intelligence.
Python is a popular programming language.
# Adicionar mais amostras de texto diversas...
EOF

# 3. Gerar matriz de importância
./llama-imatrix -m model-f16.gguf \
    -f calibration.txt \
    --chunk 512 \
    -o model.imatrix \
    -ngl 35  # Camadas GPU se disponível

# 4. Quantizar com imatrix
./llama-quantize --imatrix model.imatrix \
    model-f16.gguf \
    model-q4_k_m.gguf \
    Q4_K_M
```

### Fluxo 3: Múltiplas quantizações

```bash
#!/bin/bash
MODEL="llama-3.1-8b-f16.gguf"
IMATRIX="llama-3.1-8b.imatrix"

# Gerar imatrix uma vez
./llama-imatrix -m $MODEL -f wiki.txt -o $IMATRIX -ngl 35

# Criar múltiplas quantizações
for QUANT in Q4_K_M Q5_K_M Q6_K Q8_0; do
    OUTPUT="llama-3.1-8b-${QUANT,,}.gguf"
    ./llama-quantize --imatrix $IMATRIX $MODEL $OUTPUT $QUANT
    echo "Created: $OUTPUT ($(du -h $OUTPUT | cut -f1))"
done
```

## Uso em Python

### llama-cpp-python

```python
from llama_cpp import Llama

# Carregar modelo
llm = Llama(
    model_path="./model-q4_k_m.gguf",
    n_ctx=4096,          # Janela de contexto
    n_gpu_layers=35,     # Offload de GPU (0 apenas CPU)
    n_threads=8          # Threads de CPU
)

# Gerar
output = llm(
    "What is machine learning?",
    max_tokens=256,
    temperature=0.7,
    stop=["</s>", "\n\n"]
)
print(output["choices"][0]["text"])
```

### Conclusão de chat

```python
from llama_cpp import Llama

llm = Llama(
    model_path="./model-q4_k_m.gguf",
    n_ctx=4096,
    n_gpu_layers=35,
    chat_format="llama-3"  # Ou "chatml", "mistral", etc.
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"}
]

response = llm.create_chat_completion(
    messages=messages,
    max_tokens=256,
    temperature=0.7
)
print(response["choices"][0]["message"]["content"])
```

### Streaming

```python
from llama_cpp import Llama

llm = Llama(model_path="./model-q4_k_m.gguf", n_gpu_layers=35)

# Transmitir tokens
for chunk in llm(
    "Explain quantum computing:",
    max_tokens=256,
    stream=True
):
    print(chunk["choices"][0]["text"], end="", flush=True)
```

## Modo servidor

### Iniciar servidor compatível com OpenAI

```bash
# Iniciar servidor
./llama-server -m model-q4_k_m.gguf \
    --host 0.0.0.0 \
    --port 8080 \
    -ngl 35 \
    -c 4096

# Ou com bindings Python
python -m llama_cpp.server \
    --model model-q4_k_m.gguf \
    --n_gpu_layers 35 \
    --host 0.0.0.0 \
    --port 8080
```

### Usar com cliente OpenAI

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="local-model",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=256
)
print(response.choices[0].message.content)
```

## Otimização de hardware

### Apple Silicon (Metal)

```bash
# Build com Metal
make clean && make GGML_METAL=1

# Executar com aceleração Metal
./llama-cli -m model.gguf -ngl 99 -p "Hello"

# Python com Metal
llm = Llama(
    model_path="model.gguf",
    n_gpu_layers=99,     # Offload de todas as camadas
    n_threads=1          # Metal gerencia o paralelismo
)
```

### NVIDIA CUDA

```bash
# Build com CUDA
make clean && make GGML_CUDA=1

# Executar com CUDA
./llama-cli -m model.gguf -ngl 35 -p "Hello"

# Especificar GPU
CUDA_VISIBLE_DEVICES=0 ./llama-cli -m model.gguf -ngl 35
```

### Otimização de CPU

```bash
# Build com AVX2/AVX512
make clean && make

# Executar com threads otimizados
./llama-cli -m model.gguf -t 8 -p "Hello"

# Configuração Python apenas CPU
llm = Llama(
    model_path="model.gguf",
    n_gpu_layers=0,      # Apenas CPU
    n_threads=8,         # Corresponder aos núcleos físicos
    n_batch=512          # Tamanho do lote para processamento de prompt
)
```

## Integração com ferramentas

### Ollama

```bash
# Criar Modelfile
cat > Modelfile << 'EOF'
FROM ./model-q4_k_m.gguf
TEMPLATE """{{ .System }}
{{ .Prompt }}"""
PARAMETER temperature 0.7
PARAMETER num_ctx 4096
EOF

# Criar modelo Ollama
ollama create mymodel -f Modelfile

# Executar
ollama run mymodel "Hello!"
```

### LM Studio

1. Colocar arquivo GGUF em `~/.cache/lm-studio/models/`
2. Abrir LM Studio e selecionar o modelo
3. Configurar comprimento de contexto e offload de GPU
4. Iniciar inferência

### text-generation-webui

```bash
# Colocar na pasta de modelos
cp model-q4_k_m.gguf text-generation-webui/models/

# Iniciar com loader llama.cpp
python server.py --model model-q4_k_m.gguf --loader llama.cpp --n-gpu-layers 35
```

## Melhores práticas

1. **Use K-quants**: Q4_K_M oferece melhor equilíbrio qualidade/tamanho
2. **Use imatrix**: Sempre use matriz de importância para Q4 e abaixo
3. **Offload de GPU**: Descarregue o máximo de camadas permitido pela VRAM
4. **Comprimento de contexto**: Comece com 4096, aumente se necessário
5. **Contagem de threads**: Corresponda aos núcleos físicos da CPU, não lógicos
6. **Tamanho do lote**: Aumente n_batch para processamento mais rápido de prompt

## Problemas comuns

**Modelo carrega lentamente:**
```bash
# Use mmap para carregamento mais rápido
./llama-cli -m model.gguf --mmap
```

**Memória insuficiente:**
```bash
# Reduzir camadas de GPU
./llama-cli -m model.gguf -ngl 20  # Reduzir de 35

# Ou usar quantização menor
./llama-quantize model-f16.gguf model-q3_k_m.gguf Q3_K_M
```

**Qualidade fraca em bits baixos:**
```bash
# Sempre use imatrix para Q4 e abaixo
./llama-imatrix -m model-f16.gguf -f calibration.txt -o model.imatrix
./llama-quantize --imatrix model.imatrix model-f16.gguf model-q4_k_m.gguf Q4_K_M
```

## Referências

- **[Advanced Usage](references/advanced-usage.md)** - Batching, speculative decoding, builds personalizados
- **[Troubleshooting](references/troubleshooting.md)** - Problemas comuns, debugging, benchmarks

## Recursos

- **Repository**: https://github.com/ggml-org/llama.cpp
- **Python Bindings**: https://github.com/abetlen/llama-cpp-python
- **Pre-quantized Models**: https://huggingface.co/TheBloke
- **GGUF Converter**: https://huggingface.co/spaces/ggml-org/gguf-my-repo
- **License**: MIT