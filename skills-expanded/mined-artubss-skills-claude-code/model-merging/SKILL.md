---
name: model-merging
description: Mescle múltiplos modelos ajustados usando mergekit para combinar capacidades sem retreinar. Use ao criar modelos especializados misturando expertise específica de domínio (math + coding + chat), melhorando performance além de modelos únicos, ou experimentando rapidamente variantes de modelos. Cobre SLERP, TIES-Merging, DARE, Task Arithmetic, mesclagem linear e estratégias de deploy em produção.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Emerging Techniques, Model Merging, Mergekit, SLERP, TIES, DARE, Task Arithmetic, Model Fusion, No Retraining, Multi-Capability, Arcee AI]
dependencies: [mergekit, transformers, torch]
---

# Mesclagem de Modelos: Combinando Modelos Pré-treinados

## Quando Usar Esta Skill

Use Model Merging quando precisar:
- **Combinar capacidades** de múltiplos modelos ajustados sem retreinar
- **Criar modelos especializados** misturando expertise específica de domínio (matemática + codificação + chat)
- **Melhorar performance** além de modelos únicos (frequentemente +5-10% em benchmarks)
- **Reduzir custos de treinamento** - sem GPUs necessárias, mesclagens rodam em CPU
- **Experimentar rapidamente** - criar novas variantes de modelos em minutos, não dias
- **Preservar múltiplas habilidades** - mesclar sem esquecimento catastrófico

**Histórias de Sucesso**: Marcoro14-7B-slerp (melhor no Open LLM Leaderboard 02/2024), muitos modelos top do HuggingFace usam mesclagem

**Ferramentas**: mergekit (Arcee AI), LazyMergekit, Model Soup

## Instalação

```bash
# Instalar mergekit
git clone https://github.com/arcee-ai/mergekit.git
cd mergekit
pip install -e .

# Ou via pip
pip install mergekit

# Opcional: biblioteca Transformer
pip install transformers torch
```

## Início Rápido

### Mesclagem Linear Simples

```yaml
# config.yml - Mesclar dois modelos com pesos iguais
merge_method: linear
models:
  - model: mistralai/Mistral-7B-v0.1
    parameters:
      weight: 0.5
  - model: teknium/OpenHermes-2.5-Mistral-7B
    parameters:
      weight: 0.5
dtype: bfloat16
```

```bash
# Executar mesclagem
mergekit-yaml config.yml ./merged-model --cuda

# Usar modelo mesclado
python -m transformers.models.auto --model_name_or_path ./merged-model
```

### Mesclagem SLERP (Melhor para 2 Modelos)

```yaml
# config.yml - Interpolação esférica
merge_method: slerp
slices:
  - sources:
      - model: mistralai/Mistral-7B-v0.1
        layer_range: [0, 32]
      - model: teknium/OpenHermes-2.5-Mistral-7B
        layer_range: [0, 32]
parameters:
  t: 0.5  # Fator de interpolação (0=modelo1, 1=modelo2)
dtype: bfloat16
```

## Conceitos Principais

### 1. Métodos de Mesclagem

**Linear (Model Soup)**
- Média ponderada simples de parâmetros
- Rápido, funciona bem para modelos similares
- Pode mesclar 2+ modelos

```python
merged_weights = w1 * model1_weights + w2 * model2_weights + w3 * model3_weights
# onde w1 + w2 + w3 = 1
```

**SLERP (Spherical Linear Interpolation)**
- Interpola ao longo de esfera no espaço de pesos
- Preserva magnitude de vetores de peso
- Melhor para mesclar 2 modelos
- Mais suave que linear

```python
# Fórmula SLERP
merged = (sin((1-t)*θ) / sin(θ)) * model1 + (sin(t*θ) / sin(θ)) * model2
# onde θ = arccos(dot(model1, model2))
# t ∈ [0, 1]
```

**Task Arithmetic**
- Extrai "task vectors" (ajustado - base)
- Combina task vectors, adiciona à base
- Bom para mesclar múltiplos modelos especializados

```python
# Task vector
task_vector = finetuned_model - base_model

# Mesclar múltiplos task vectors
merged = base_model + α₁*task_vector₁ + α₂*task_vector₂
```

**TIES-Merging**
- Task arithmetic + esparsificação
- Resolve conflitos de sinal em parâmetros
- Melhor para mesclar muitos modelos específicos de tarefa

**DARE (Drop And REscale)**
- Descarta aleatoriamente parâmetros ajustados
- Reescala parâmetros restantes
- Reduz redundância, mantém performance

### 2. Estrutura de Configuração

```yaml
# Estrutura básica
merge_method: <method>  # linear, slerp, ties, dare_ties, task_arithmetic
base_model: <path>      # Opcional: modelo base para task arithmetic

models:
  - model: <path/to/model1>
    parameters:
      weight: <float>   # Peso de mesclagem
      density: <float>  # Para TIES/DARE

  - model: <path/to/model2>
    parameters:
      weight: <float>

parameters:
  # Parâmetros específicos do método

dtype: <dtype>  # bfloat16, float16, float32

# Opcional
slices:  # Mesclagem por camada
tokenizer:  # Configuração de tokenizador
```

## Guia de Métodos de Mesclagem

### Mesclagem Linear

**Melhor para**: Combinações simples de modelos, ponderação igual

```yaml
merge_method: linear
models:
  - model: WizardLM/WizardMath-7B-V1.1
    parameters:
      weight: 0.4
  - model: teknium/OpenHermes-2.5-Mistral-7B
    parameters:
      weight: 0.3
  - model: NousResearch/Nous-Hermes-2-Mistral-7B-DPO
    parameters:
      weight: 0.3
dtype: bfloat16
```

### Mesclagem SLERP

**Melhor para**: Dois modelos, interpolação suave

```yaml
merge_method: slerp
slices:
  - sources:
      - model: mistralai/Mistral-7B-v0.1
        layer_range: [0, 32]
      - model: teknium/OpenHermes-2.5-Mistral-7B
        layer_range: [0, 32]
parameters:
  t: 0.5  # 0.0 = primeiro modelo, 1.0 = segundo modelo
dtype: bfloat16
```

**SLERP específica por camada:**

```yaml
merge_method: slerp
slices:
  - sources:
      - model: model_a
        layer_range: [0, 32]
      - model: model_b
        layer_range: [0, 32]
parameters:
  t:
    - filter: self_attn    # Camadas de atenção
      value: 0.3
    - filter: mlp          # Camadas MLP
      value: 0.7
    - value: 0.5           # Padrão para outras camadas
dtype: bfloat16
```

### Task Arithmetic

**Melhor para**: Combinar habilidades especializadas

```yaml
merge_method: task_arithmetic
base_model: mistralai/Mistral-7B-v0.1
models:
  - model: WizardLM/WizardMath-7B-V1.1  # Matemática
    parameters:
      weight: 0.5
  - model: teknium/OpenHermes-2.5-Mistral-7B  # Chat
    parameters:
      weight: 0.3
  - model: ajibawa-2023/Code-Mistral-7B  # Código
    parameters:
      weight: 0.2
dtype: bfloat16
```

### TIES-Merging

**Melhor para**: Muitos modelos, resolvendo conflitos

```yaml
merge_method: ties
base_model: mistralai/Mistral-7B-v0.1
models:
  - model: WizardLM/WizardMath-7B-V1.1
    parameters:
      density: 0.5  # Manter top 50% dos parâmetros
      weight: 1.0
  - model: teknium/OpenHermes-2.5-Mistral-7B
    parameters:
      density: 0.5
      weight: 1.0
  - model: NousResearch/Nous-Hermes-2-Mistral-7B-DPO
    parameters:
      density: 0.5
      weight: 1.0
parameters:
  normalize: true
dtype: bfloat16
```

### Mesclagem DARE

**Melhor para**: Reduzir redundância

```yaml
merge_method: dare_ties
base_model: mistralai/Mistral-7B-v0.1
models:
  - model: WizardLM/WizardMath-7B-V1.1
    parameters:
      density: 0.5    # Descartar 50% dos deltas
      weight: 0.6
  - model: teknium/OpenHermes-2.5-Mistral-7B
    parameters:
      density: 0.5
      weight: 0.4
parameters:
  int8_mask: true  # Usar int8 para máscaras (economiza memória)
dtype: bfloat16
```

## Padrões Avançados

### Mesclagem Por Camada

```yaml
# Diferentes modelos para diferentes camadas
merge_method: passthrough
slices:
  - sources:
      - model: mistralai/Mistral-7B-v0.1
        layer_range: [0, 16]   # Primeira metade
  - sources:
      - model: teknium/OpenHermes-2.5-Mistral-7B
        layer_range: [16, 32]  # Segunda metade
dtype: bfloat16
```

### MoE de Modelos Mesclados

```yaml
# Criar Mixture of Experts
merge_method: moe
base_model: mistralai/Mistral-7B-v0.1
experts:
  - source_model: WizardLM/WizardMath-7B-V1.1
    positive_prompts:
      - "math"
      - "calculate"
  - source_model: teknium/OpenHermes-2.5-Mistral-7B
    positive_prompts:
      - "chat"
      - "conversation"
  - source_model: ajibawa-2023/Code-Mistral-7B
    positive_prompts:
      - "code"
      - "python"
dtype: bfloat16
```

### Mesclagem de Tokenizador

```yaml
merge_method: linear
models:
  - model: mistralai/Mistral-7B-v0.1
  - model: custom/specialized-model

tokenizer:
  source: "union"  # Combinar vocabulários de ambos modelos
  tokens:
    <|special_token|>:
      source: "custom/specialized-model"
```

## Melhores Práticas

### 1. Compatibilidade de Modelos

```python
# ✅ Bom: Mesma arquitetura
models = [
    "mistralai/Mistral-7B-v0.1",
    "teknium/OpenHermes-2.5-Mistral-7B",  # Ambos Mistral 7B
]

# ❌ Ruim: Arquiteturas diferentes
models = [
    "meta-llama/Llama-2-7b-hf",  # Llama
    "mistralai/Mistral-7B-v0.1",  # Mistral (incompatível!)
]
```

### 2. Seleção de Pesos

```yaml
# ✅ Bom: Pesos somam 1.0
models:
  - model: model_a
    parameters:
      weight: 0.6
  - model: model_b
    parameters:
      weight: 0.4  # 0.6 + 0.4 = 1.0

# ⚠️  Aceitável: Pesos não somam 1 (para task arithmetic)
models:
  - model: model_a
    parameters:
      weight: 0.8
  - model: model_b
    parameters:
      weight: 0.8  # Pode potencializar performance
```

### 3. Seleção de Método

```python
# Escolher método de mesclagem baseado no caso de uso:

# 2 modelos, mistura suave → SLERP
merge_method = "slerp"

# 3+ modelos, média simples → Linear
merge_method = "linear"

# Múltiplos modelos específicos de tarefa → Task Arithmetic ou TIES
merge_method = "ties"

# Quer reduzir redundância → DARE
merge_method = "dare_ties"
```

### 4. Ajuste de Densidade (TIES/DARE)

```yaml
# Começar conservador (manter mais parâmetros)
parameters:
  density: 0.8  # Manter 80%

# Se performance boa, aumentar esparsidade
parameters:
  density: 0.5  # Manter 50%

# Se performance degenera, reduzir esparsidade
parameters:
  density: 0.9  # Manter 90%
```

### 5. Mesclagem Específica Por Camada

```yaml
# Preservar início e fim do modelo base
merge_method: passthrough
slices:
  - sources:
      - model: base_model
        layer_range: [0, 2]     # Manter primeiras camadas
  - sources:
      - model: merged_middle    # Mesclar camadas do meio
        layer_range: [2, 30]
  - sources:
      - model: base_model
        layer_range: [30, 32]   # Manter últimas camadas
```

## Avaliação e Testes

### Benchmark Modelos Mesclados

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Carregar modelo mesclado
model = AutoModelForCausalLM.from_pretrained("./merged-model")
tokenizer = AutoTokenizer.from_pretrained("./merged-model")

# Testar em várias tarefas
test_prompts = {
    "math": "Calcule: 25 * 17 =",
    "code": "Escreva uma função Python para inverter uma string:",
    "chat": "Qual é a capital da França?",
}

for task, prompt in test_prompts.items():
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100)
    print(f"{task}: {tokenizer.decode(outputs[0])}")
```

### Benchmarks Comuns

- **Open LLM Leaderboard**: Capacidades gerais
- **MT-Bench**: Conversa multi-turno
- **MMLU**: Precisão multitarefa
- **HumanEval**: Geração de código
- **GSM8K**: Raciocínio matemático

## Deploy em Produção

### Salvar e Fazer Upload

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Carregar modelo mesclado
model = AutoModelForCausalLM.from_pretrained("./merged-model")
tokenizer = AutoTokenizer.from_pretrained("./merged-model")

# Fazer upload para Hub HuggingFace
model.push_to_hub("username/my-merged-model")
tokenizer.push_to_hub("username/my-merged-model")
```

### Quantizar Modelo Mesclado

```bash
# Quantizar com GGUF
python convert.py ./merged-model --outtype f16 --outfile merged-model.gguf

# Quantizar com GPTQ
python quantize_gptq.py ./merged-model --bits 4 --group_size 128
```

## Armadilhas Comuns

### ❌ Armadilha 1: Mesclar Modelos Incompatíveis

```yaml
# Errado: Arquiteturas diferentes
models:
  - model: meta-llama/Llama-2-7b  # Arquitetura Llama
  - model: mistralai/Mistral-7B   # Arquitetura Mistral
```

**Solução**: Mesclar apenas modelos com mesma arquitetura

### ❌ Armadilha 2: Sobre-ponderar Um Modelo

```yaml
# Subótimo: Um modelo domina
models:
  - model: model_a
    parameters:
      weight: 0.95  # Muito alto
  - model: model_b
    parameters:
      weight: 0.05  # Muito baixo
```

**Solução**: Usar pesos mais balanceados (intervalo 0.3-0.7)

### ❌ Armadilha 3: Não Avaliar

```bash
# Errado: Mesclar e fazer deploy sem testes
mergekit-yaml config.yml ./merged-model
# Fazer deploy imediatamente (arriscado!)
```

**Solução**: Sempre fazer benchmark antes de fazer deploy

## Recursos

- **mergekit GitHub**: https://github.com/arcee-ai/mergekit
- **Tutorial HuggingFace**: https://huggingface.co/blog/mlabonne/merge-models
- **LazyMergekit**: Notebook de mesclagem automatizada
- **Artigo TIES**: https://arxiv.org/abs/2306.01708
- **Artigo DARE**: https://arxiv.org/abs/2311.03099

## Veja também

- `references/methods.md` - Aprofundamento em algoritmos de mesclagem
- `references/examples.md` - Configurações de mesclagem do mundo real
- `references/evaluation.md` - Estratégias de benchmark e testes