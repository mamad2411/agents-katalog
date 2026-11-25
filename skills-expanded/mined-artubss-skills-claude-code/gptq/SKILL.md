---
name: gptq
description: Quantização pós-treinamento em 4-bits para LLMs com perda mínima de precisão. Use para implantar modelos grandes (70B, 405B) em GPUs de consumo, quando você precisa de redução de memória 4× com <2% de degradação de perplexidade, ou para inferência mais rápida (aceleração de 3-4×) vs FP16. Integra com transformers e PEFT para fine-tuning QLoRA.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Optimization, GPTQ, Quantization, 4-Bit, Post-Training, Memory Optimization, Consumer GPUs, Fast Inference, QLoRA, Group-Wise Quantization]
dependencies: [auto-gptq, transformers, optimum, peft]
---

# GPTQ (Generative Pre-trained Transformer Quantization)

Método de quantização pós-treinamento que comprime LLMs para 4-bits com perda mínima de precisão usando quantização group-wise.

## Quando usar GPTQ

**Use GPTQ quando:**
- Precisa encaixar modelos grandes (70B+) em memória GPU limitada
- Quer redução de memória 4× com <2% de perda de precisão
- Implantando em GPUs de consumo (RTX 4090, 3090)
- Precisa de inferência mais rápida (aceleração de 3-4× vs FP16)

**Use AWQ em vez disso quando:**
- Precisa de precisão ligeiramente melhor (<1% de perda)
- Tem GPUs mais novas (Ampere, Ada)
- Quer suporte do kernel Marlin (2× mais rápido em algumas GPUs)

**Use bitsandbytes em vez disso quando:**
- Precisa de integração simples com transformers
- Quer quantização 8-bit (menos compressão, melhor qualidade)
- Não precisa de arquivos de modelo pré-quantizados

## Início rápido

### Instalação

```bash
# Instalar AutoGPTQ
pip install auto-gptq

# Com Triton (apenas Linux, mais rápido)
pip install auto-gptq[triton]

# Com extensões CUDA (mais rápido)
pip install auto-gptq --no-build-isolation

# Instalação completa
pip install auto-gptq transformers accelerate
```

### Carregar modelo pré-quantizado

```python
from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

# Carregar modelo quantizado do HuggingFace
model_name = "TheBloke/Llama-2-7B-Chat-GPTQ"

model = AutoGPTQForCausalLM.from_quantized(
    model_name,
    device="cuda:0",
    use_triton=False  # Defina como True no Linux para velocidade
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

# Gerar
prompt = "Explain quantum computing"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda:0")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0]))
```

### Quantizar seu próprio modelo

```python
from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
from datasets import load_dataset

# Carregar modelo
model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Configuração de quantização
quantize_config = BaseQuantizeConfig(
    bits=4,              # Quantização 4-bit
    group_size=128,      # Tamanho do grupo (recomendado: 128)
    desc_act=False,      # Ordem de ativação (False para kernel CUDA)
    damp_percent=0.01    # Fator de amortecimento
)

# Carregar modelo para quantização
model = AutoGPTQForCausalLM.from_pretrained(
    model_name,
    quantize_config=quantize_config
)

# Preparar dados de calibração
dataset = load_dataset("c4", split="train", streaming=True)
calibration_data = [
    tokenizer(example["text"])["input_ids"][:512]
    for example in dataset.take(128)
]

# Quantizar
model.quantize(calibration_data)

# Salvar modelo quantizado
model.save_quantized("llama-2-7b-gptq")
tokenizer.save_pretrained("llama-2-7b-gptq")

# Enviar para HuggingFace
model.push_to_hub("username/llama-2-7b-gptq")
```

## Quantização group-wise

**Como GPTQ funciona**:
1. **Agrupar pesos**: Divide cada matriz de pesos em grupos (tipicamente 128 elementos)
2. **Quantizar por grupo**: Cada grupo tem sua própria escala/ponto zero
3. **Minimizar erro**: Usa informações de Hessiana para minimizar erro de quantização
4. **Resultado**: Pesos 4-bit com precisão próxima a FP16

**Trade-off de tamanho de grupo**:

| Tamanho do Grupo | Tamanho do Modelo | Precisão | Velocidade | Recomendação |
|------------|------------|----------|-------|----------------|
| -1 (por coluna) | Menor | Melhor | Mais lenta | Apenas pesquisa |
| 32 | Menor | Melhor | Mais lenta | Precisão alta necessária |
| **128** | Médio | Boa | **Rápida** | **Padrão recomendado** |
| 256 | Maior | Menor | Mais rápida | Crítico em velocidade |
| 1024 | Maior | Menor | Mais rápida | Não recomendado |

**Exemplo**:
```
Matriz de pesos: [1024, 4096] = 4.2M elementos

Tamanho de grupo = 128:
- Grupos: 4.2M / 128 = 32.768 grupos
- Cada grupo: escala 4-bit própria + ponto zero
- Resultado: Melhor granularidade → melhor precisão
```

## Configurações de quantização

### 4-bit padrão (recomendado)

```python
from auto_gptq import BaseQuantizeConfig

config = BaseQuantizeConfig(
    bits=4,              # Quantização 4-bit
    group_size=128,      # Tamanho de grupo padrão
    desc_act=False,      # Kernel CUDA mais rápido
    damp_percent=0.01    # Fator de amortecimento
)
```

**Performance**:
- Memória: Redução 4× (modelo 70B: 140GB → 35GB)
- Precisão: ~1.5% de aumento de perplexidade
- Velocidade: 3-4× mais rápido que FP16

### Alta precisão (3-bit com grupos maiores)

```python
config = BaseQuantizeConfig(
    bits=3,              # 3-bit (mais compressão)
    group_size=128,      # Manter tamanho de grupo padrão
    desc_act=True,       # Melhor precisão (mais lenta)
    damp_percent=0.01
)
```

**Trade-off**:
- Memória: Redução 5×
- Precisão: ~3% de aumento de perplexidade
- Velocidade: 5× mais rápido (mas menos preciso)

### Máxima precisão (4-bit com grupos pequenos)

```python
config = BaseQuantizeConfig(
    bits=4,
    group_size=32,       # Grupos menores (melhor precisão)
    desc_act=True,       # Reordenação de ativação
    damp_percent=0.005   # Amortecimento menor
)
```

**Trade-off**:
- Memória: Redução 3.5× (ligeiramente maior)
- Precisão: ~0.8% de aumento de perplexidade (melhor)
- Velocidade: 2-3× mais rápido (overhead de kernel)

## Backends de kernel

### ExLlamaV2 (padrão, mais rápido)

```python
model = AutoGPTQForCausalLM.from_quantized(
    model_name,
    device="cuda:0",
    use_exllama=True,      # Usar ExLlamaV2
    exllama_config={"version": 2}
)
```

**Performance**: 1.5-2× mais rápido que Triton

### Marlin (GPUs Ampere+)

```python
# Quantizar com formato Marlin
config = BaseQuantizeConfig(
    bits=4,
    group_size=128,
    desc_act=False  # Obrigatório para Marlin
)

model.quantize(calibration_data, use_marlin=True)

# Carregar com Marlin
model = AutoGPTQForCausalLM.from_quantized(
    model_name,
    device="cuda:0",
    use_marlin=True  # 2× mais rápido em A100/H100
)
```

**Requisitos**:
- NVIDIA Ampere ou mais novo (A100, H100, RTX 40xx)
- Capacidade de computação ≥ 8.0

### Triton (apenas Linux)

```python
model = AutoGPTQForCausalLM.from_quantized(
    model_name,
    device="cuda:0",
    use_triton=True  # Apenas Linux
)
```

**Performance**: 1.2-1.5× mais rápido que backend CUDA

## Integração com transformers

### Uso direto do transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Carregar modelo quantizado (transformers detecta automaticamente GPTQ)
model = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Llama-2-13B-Chat-GPTQ",
    device_map="auto",
    trust_remote_code=False
)

tokenizer = AutoTokenizer.from_pretrained("TheBloke/Llama-2-13B-Chat-GPTQ")

# Usar como qualquer modelo transformers
inputs = tokenizer("Hello", return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=100)
```

### Fine-tuning QLoRA (GPTQ + LoRA)

```python
from transformers import AutoModelForCausalLM
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model

# Carregar modelo GPTQ
model = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Llama-2-7B-GPTQ",
    device_map="auto"
)

# Preparar para treinamento LoRA
model = prepare_model_for_kbit_training(model)

# Configuração LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Adicionar adaptadores LoRA
model = get_peft_model(model, lora_config)

# Fine-tune (muito eficiente em memória!)
# Modelo 70B treináv em um único A100 80GB
```

## Benchmarks de performance

### Redução de memória

| Modelo | FP16 | GPTQ 4-bit | Redução |
|-------|------|------------|-----------|
| Llama 2-7B | 14 GB | 3.5 GB | 4× |
| Llama 2-13B | 26 GB | 6.5 GB | 4× |
| Llama 2-70B | 140 GB | 35 GB | 4× |
| Llama 3-405B | 810 GB | 203 GB | 4× |

**Habilita**:
- 70B em um único A100 80GB (vs 2× A100 necessários para FP16)
- 405B em 3× A100 80GB (vs 11× A100 necessários para FP16)
- 13B em RTX 4090 24GB (vs OOM com FP16)

### Velocidade de inferência (Llama 2-7B, A100)

| Precisão | Tokens/seg | vs FP16 |
|-----------|------------|---------|
| FP16 | 25 tok/s | 1× |
| GPTQ 4-bit (CUDA) | 85 tok/s | 3.4× |
| GPTQ 4-bit (ExLlama) | 105 tok/s | 4.2× |
| GPTQ 4-bit (Marlin) | 120 tok/s | 4.8× |

### Precisão (perplexidade em WikiText-2)

| Modelo | FP16 | GPTQ 4-bit (g=128) | Degradação |
|-------|------|---------------------|-------------|
| Llama 2-7B | 5.47 | 5.55 | +1.5% |
| Llama 2-13B | 4.88 | 4.95 | +1.4% |
| Llama 2-70B | 3.32 | 3.38 | +1.8% |

**Preservação de qualidade excelente** - menos de 2% de degradação!

## Padrões comuns

### Implantação multi-GPU

```python
# Mapeamento automático de dispositivo
model = AutoGPTQForCausalLM.from_quantized(
    "TheBloke/Llama-2-70B-GPTQ",
    device_map="auto",  # Divide automaticamente entre GPUs
    max_memory={0: "40GB", 1: "40GB"}  # Limite por GPU
)

# Mapeamento manual de dispositivo
device_map = {
    "model.embed_tokens": 0,
    "model.layers.0-39": 0,  # Primeiras 40 camadas na GPU 0
    "model.layers.40-79": 1,  # Últimas 40 camadas na GPU 1
    "model.norm": 1,
    "lm_head": 1
}

model = AutoGPTQForCausalLM.from_quantized(
    model_name,
    device_map=device_map
)
```

### Offloading para CPU

```python
# Descarregar algumas camadas para CPU (para modelos muito grandes)
model = AutoGPTQForCausalLM.from_quantized(
    "TheBloke/Llama-2-405B-GPTQ",
    device_map="auto",
    max_memory={
        0: "80GB",  # GPU 0
        1: "80GB",  # GPU 1
        2: "80GB",  # GPU 2
        "cpu": "200GB"  # Descarregar overflow para CPU
    }
)
```

### Inferência em batch

```python
# Processar múltiplos prompts eficientemente
prompts = [
    "Explain AI",
    "Explain ML",
    "Explain DL"
]

inputs = tokenizer(prompts, return_tensors="pt", padding=True).to("cuda")

outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    pad_token_id=tokenizer.eos_token_id
)

for i, output in enumerate(outputs):
    print(f"Prompt {i}: {tokenizer.decode(output)}")
```

## Encontrando modelos pré-quantizados

**TheBloke no HuggingFace**:
- https://huggingface.co/TheBloke
- 1000+ modelos em formato GPTQ
- Múltiplos tamanhos de grupo (32, 128)
- Formatos CUDA e Marlin

**Pesquisar**:
```bash
# Encontrar modelos GPTQ no HuggingFace
https://huggingface.co/models?library=gptq
```

**Download**:
```python
from auto_gptq import AutoGPTQForCausalLM

# Baixa automaticamente do HuggingFace
model = AutoGPTQForCausalLM.from_quantized(
    "TheBloke/Llama-2-70B-Chat-GPTQ",
    device="cuda:0"
)
```

## Modelos suportados

- **Família LLaMA**: Llama 2, Llama 3, Code Llama
- **Mistral**: Mistral 7B, Mixtral 8x7B, 8x22B
- **Qwen**: Qwen, Qwen2, QwQ
- **DeepSeek**: V2, V3
- **Phi**: Phi-2, Phi-3
- **Yi, Falcon, BLOOM, OPT**
- **100+ modelos** no HuggingFace

## Referências

- **[Guia de Calibração](references/calibration.md)** - Seleção de dataset, processo de quantização, otimização de qualidade
- **[Guia de Integração](references/integration.md)** - Transformers, PEFT, vLLM, TensorRT-LLM
- **[Solução de Problemas](references/troubleshooting.md)** - Problemas comuns, otimização de performance

## Recursos

- **GitHub**: https://github.com/AutoGPTQ/AutoGPTQ
- **Paper**: GPTQ: Accurate Post-Training Quantization (arXiv:2210.17323)
- **Modelos**: https://huggingface.co/models?library=gptq
- **Discord**: https://discord.gg/autogptq