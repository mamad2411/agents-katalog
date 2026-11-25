---
name: model-pruning
description: Reduza o tamanho de LLMs e acelere a inferência usando técnicas de pruning como Wanda e SparseGPT. Use para comprimir modelos sem retreinamento, alcançando 50% de esparsidade com perda mínima de acurácia, ou ativando inferência mais rápida em aceleradores de hardware. Cobre pruning não estruturado, pruning estruturado, esparsidade N:M, pruning por magnitude e métodos one-shot.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Emerging Techniques, Model Pruning, Wanda, SparseGPT, Sparsity, Model Compression, N:M Sparsity, One-Shot Pruning, Structured Pruning, Unstructured Pruning, Fast Inference]
dependencies: [transformers, torch]
---

# Model Pruning: Comprimindo LLMs

## Quando Usar Esta Skill

Use Model Pruning quando você precisar:
- **Reduzir tamanho do modelo** de 40-60% com <1% de perda de acurácia
- **Acelerar a inferência** usando esparsidade amigável ao hardware (speedup 2-4×)
- **Fazer deploy em hardware limitado** (dispositivos móveis, edge)
- **Comprimir sem retreinamento** usando métodos one-shot
- **Habilitar serving eficiente** com pegada de memória reduzida

**Técnicas-chave**: Wanda (weights × activations), SparseGPT (segunda ordem), pruning estruturado, esparsidade N:M

**Papers**: Wanda ICLR 2024 (arXiv 2306.11695), SparseGPT (arXiv 2301.00774)

## Instalação

```bash
# Implementação Wanda
git clone https://github.com/locuslab/wanda
cd wanda
pip install -r requirements.txt

# Opcional: SparseGPT
git clone https://github.com/IST-DASLab/sparsegpt
cd sparsegpt
pip install -e .

# Dependências
pip install torch transformers accelerate
```

## Quick Start

### Wanda Pruning (One-Shot, Sem Retreinamento)

**Fonte**: ICLR 2024 (arXiv 2306.11695)

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Carrega modelo
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16,
    device_map="cuda"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

# Dados de calibração (pequeno dataset para estatísticas de ativação)
calib_data = [
    "The quick brown fox jumps over the lazy dog.",
    "Machine learning is transforming the world.",
    "Artificial intelligence powers modern applications.",
]

# Função de pruning Wanda
def wanda_prune(model, calib_data, sparsity=0.5):
    """
    Wanda: Prune por magnitude de peso × ativação de entrada.

    Args:
        sparsity: Fração de pesos a fazer prune (0.5 = 50%)
    """
    # 1. Coleta estatísticas de ativação
    activations = {}

    def hook_fn(name):
        def hook(module, input, output):
            # Armazena nomas de ativação de entrada
            activations[name] = input[0].detach().abs().mean(dim=0)
        return hook

    # Registra hooks para todas as camadas lineares
    hooks = []
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Linear):
            hooks.append(module.register_forward_hook(hook_fn(name)))

    # Executa dados de calibração
    model.eval()
    with torch.no_grad():
        for text in calib_data:
            inputs = tokenizer(text, return_tensors="pt").to(model.device)
            model(**inputs)

    # Remove hooks
    for hook in hooks:
        hook.remove()

    # 2. Prune pesos baseado em |weight| × ativação
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Linear) and name in activations:
            W = module.weight.data
            act = activations[name]

            # Computa importância: |weight| × ativação
            importance = W.abs() * act.unsqueeze(0)

            # Achata e encontra threshold
            threshold = torch.quantile(importance.flatten(), sparsity)

            # Cria máscara
            mask = importance >= threshold

            # Aplica máscara (prune)
            W *= mask.float()

    return model

# Aplica pruning Wanda (50% sparsidade, one-shot, sem retreinamento)
pruned_model = wanda_prune(model, calib_data, sparsity=0.5)

# Salva
pruned_model.save_pretrained("./llama-2-7b-wanda-50")
```

### SparseGPT (Pruning de Segunda Ordem)

**Fonte**: arXiv 2301.00774

```python
from sparsegpt import SparseGPT

# Carrega modelo
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")

# Inicializa SparseGPT
pruner = SparseGPT(model)

# Dados de calibração
calib_data = load_calibration_data()  # ~128 amostras

# Prune (one-shot, reconstrução layer-wise)
pruned_model = pruner.prune(
    calib_data=calib_data,
    sparsity=0.5,           # 50% sparsidade
    prunen=0,               # Não estruturado (0) ou N:M estruturado
    prunem=0,
    percdamp=0.01,          # Damping para inversa de Hessian
)

# Resultados: Pruning quasi-sem perda em 50% sparsidade
```

### N:M Structured Pruning (Acelerador de Hardware)

```python
def nm_prune(weight, n=2, m=4):
    """
    Pruning N:M: Mantém N pesos a cada M pesos consecutivos.
    Exemplo: 2:4 = manter 2 a cada 4 pesos.

    Compatível com sparse tensor cores NVIDIA (2:4, 4:8).
    """
    # Reshape peso em grupos de M
    shape = weight.shape
    weight_flat = weight.flatten()

    # Padding para múltiplo de M
    pad_size = (m - weight_flat.numel() % m) % m
    weight_padded = F.pad(weight_flat, (0, pad_size))

    # Reshape em (num_groups, m)
    weight_grouped = weight_padded.reshape(-1, m)

    # Encontra top-N em cada grupo
    _, indices = torch.topk(weight_grouped.abs(), n, dim=-1)

    # Cria máscara
    mask = torch.zeros_like(weight_grouped)
    mask.scatter_(1, indices, 1.0)

    # Aplica máscara
    weight_pruned = weight_grouped * mask

    # Reshape de volta
    weight_pruned = weight_pruned.flatten()[:weight_flat.numel()]
    return weight_pruned.reshape(shape)

# Aplica sparsidade 2:4 (hardware NVIDIA)
for name, module in model.named_modules():
    if isinstance(module, torch.nn.Linear):
        module.weight.data = nm_prune(module.weight.data, n=2, m=4)

# 50% sparsidade, 2× speedup em A100 com sparse tensor cores
```

## Conceitos Principais

### 1. Critérios de Pruning

**Pruning por Magnitude** (baseline):
```python
# Prune pesos com os menores valores absolutos
importance = weight.abs()
threshold = torch.quantile(importance, sparsity)
mask = importance >= threshold
```

**Wanda** (weights × activations):
```python
# Importância = |weight| × input_activation
importance = weight.abs() * activation
# Melhor que magnitude pura (considera uso)
```

**SparseGPT** (segunda ordem):
```python
# Usa Hessian (segunda derivada) para importância
# Mais acurado mas computacionalmente caro
importance = weight^2 / diag(Hessian)
```

### 2. Estruturado vs Não Estruturado

**Não estruturado** (granular fino):
- Prune pesos individuais
- Qualidade superior (melhor acurácia)
- Sem speedup de hardware (esparsidade irregular)

**Estruturado** (granular grosso):
- Prune neurônios, heads ou camadas inteiras
- Qualidade inferior (mais perda de acurácia)
- Speedup de hardware (esparsidade regular)

**Semi-estruturado (N:M)**:
- O melhor dos dois mundos
- 50% sparsidade (2:4) → 2× speedup em GPUs NVIDIA
- Perda mínima de acurácia

### 3. Padrões de Esparsidade

```python
# Não estruturado (aleatório)
# [1, 0, 1, 0, 1, 1, 0, 0]
# Pros: Flexível, alta qualidade
# Cons: Sem speedup

# Estruturado (bloco)
# [1, 1, 0, 0, 1, 1, 0, 0]
# Pros: Amigável ao hardware
# Cons: Mais perda de acurácia

# N:M (semi-estruturado)
# [1, 0, 1, 0] [1, 1, 0, 0]  (padrão 2:4)
# Pros: Speedup de hardware + boa qualidade
# Cons: Requer hardware específico (NVIDIA)
```

## Estratégias de Pruning

### Estratégia 1: Pruning Gradual por Magnitude

```python
def gradual_prune(model, initial_sparsity=0.0, final_sparsity=0.5, num_steps=100):
    """Aumenta gradualmente sparsidade durante o treinamento."""
    for step in range(num_steps):
        # Sparsidade atual
        current_sparsity = initial_sparsity + (final_sparsity - initial_sparsity) * (step / num_steps)

        # Prune na sparsidade atual
        for module in model.modules():
            if isinstance(module, torch.nn.Linear):
                weight = module.weight.data
                threshold = torch.quantile(weight.abs().flatten(), current_sparsity)
                mask = weight.abs() >= threshold
                weight *= mask.float()

        # Treina um passo
        train_step(model)

    return model
```

### Estratégia 2: Pruning Layer-wise

```python
def layer_wise_prune(model, sparsity_per_layer):
    """Sparsidade diferente para camadas diferentes."""
    # Camadas iniciais: Menos pruning (mais importantes)
    # Camadas finais: Mais pruning (menos críticas)

    sparsity_schedule = {
        "layer.0": 0.3,   # 30% sparsidade
        "layer.1": 0.4,
        "layer.2": 0.5,
        "layer.3": 0.6,   # 60% sparsidade
    }

    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Linear):
            # Encontra índice da camada
            for layer_name, sparsity in sparsity_schedule.items():
                if layer_name in name:
                    # Prune em sparsidade específica da camada
                    prune_layer(module, sparsity)
                    break

    return model
```

### Estratégia 3: Pruning Iterativo + Fine-tuning

```python
def iterative_prune_finetune(model, target_sparsity=0.5, iterations=5):
    """Prune gradualmente com fine-tuning entre iterações."""
    current_sparsity = 0.0
    sparsity_increment = target_sparsity / iterations

    for i in range(iterations):
        # Aumenta sparsidade
        current_sparsity += sparsity_increment

        # Prune
        prune_model(model, sparsity=current_sparsity)

        # Fine-tune (recupera acurácia)
        fine_tune(model, epochs=2, lr=1e-5)

    return model

# Resultados: Melhor acurácia que one-shot em alta sparsidade
```

## Deployment em Produção

### Pipeline Completo de Pruning

```python
from transformers import Trainer, TrainingArguments

def production_pruning_pipeline(
    model_name="meta-llama/Llama-2-7b-hf",
    target_sparsity=0.5,
    method="wanda",  # ou "sparsegpt"
):
    # 1. Carrega modelo
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # 2. Carrega dados de calibração
    calib_dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train[:1000]")

    # 3. Aplica pruning
    if method == "wanda":
        pruned_model = wanda_prune(model, calib_dataset, sparsity=target_sparsity)
    elif method == "sparsegpt":
        pruner = SparseGPT(model)
        pruned_model = pruner.prune(calib_dataset, sparsity=target_sparsity)

    # 4. (Opcional) Fine-tune para recuperar acurácia
    training_args = TrainingArguments(
        output_dir="./pruned-model",
        num_train_epochs=1,
        per_device_train_batch_size=4,
        learning_rate=1e-5,
        bf16=True,
    )

    trainer = Trainer(
        model=pruned_model,
        args=training_args,
        train_dataset=finetune_dataset,
    )

    trainer.train()

    # 5. Salva
    pruned_model.save_pretrained("./pruned-llama-7b-50")
    tokenizer.save_pretrained("./pruned-llama-7b-50")

    return pruned_model

# Uso
pruned_model = production_pruning_pipeline(
    model_name="meta-llama/Llama-2-7b-hf",
    target_sparsity=0.5,
    method="wanda"
)
```

### Avaliação

```python
from lm_eval import evaluator

# Avalia modelo pruned vs original
original_results = evaluator.simple_evaluate(
    model="hf",
    model_args="pretrained=meta-llama/Llama-2-7b-hf",
    tasks=["arc_easy", "hellaswag", "winogrande"],
)

pruned_results = evaluator.simple_evaluate(
    model="hf",
    model_args="pretrained=./pruned-llama-7b-50",
    tasks=["arc_easy", "hellaswag", "winogrande"],
)

# Compara
print(f"Original: {original_results['results']['arc_easy']['acc']:.3f}")
print(f"Pruned:   {pruned_results['results']['arc_easy']['acc']:.3f}")
print(f"Degradation: {(original_results - pruned_results):.3f}")

# Resultados típicos em 50% sparsidade:
# - Wanda: <1% perda de acurácia
# - SparseGPT: <0.5% perda de acurácia
# - Magnitude: 2-3% perda de acurácia
```

## Melhores Práticas

### 1. Seleção de Sparsidade

```python
# Conservador (seguro)
sparsity = 0.3  # 30%, <0.5% perda

# Balanceado (recomendado)
sparsity = 0.5  # 50%, ~1% perda

# Agressivo (arriscado)
sparsity = 0.7  # 70%, 2-5% perda

# Extremo (depende do modelo)
sparsity = 0.9  # 90%, degradação significativa
```

### 2. Seleção de Método

```python
# One-shot, sem retreinamento → Wanda ou SparseGPT
if no_retraining_budget:
    use_method = "wanda"  # Mais rápido

# Melhor qualidade → SparseGPT
if need_best_quality:
    use_method = "sparsegpt"  # Mais acurado

# Speedup de hardware → N:M estruturado
if need_speedup:
    use_method = "nm_prune"  # 2:4 ou 4:8
```

### 3. Evite Armadilhas Comuns

```python
# ❌ Ruim: Prune sem dados de calibração
prune_random(model)  # Sem estatísticas de ativação

# ✅ Bom: Use dados de calibração
prune_wanda(model, calib_data)

# ❌ Ruim: Sparsidade muito alta de uma vez
prune(model, sparsity=0.9)  # Perda maciça de acurácia

# ✅ Bom: Gradual ou iterativo
iterative_prune(model, target=0.9, steps=10)
```

## Comparação de Performance

**Métodos de pruning em 50% sparsidade** (LLaMA-7B):

| Método | Perda de Acurácia | Velocidade | Memória | Retreinamento Necessário |
|--------|-------------------|------------|---------|--------------------------|
| **Magnitude** | -2.5% | 1.0× | -50% | Não |
| **Wanda** | -0.8% | 1.0× | -50% | Não |
| **SparseGPT** | -0.4% | 1.0× | -50% | Não |
| **N:M (2:4)** | -1.0% | 2.0× | -50% | Não |
| **Structured** | -3.0% | 2.0× | -50% | Não |

**Fonte**: Paper Wanda (ICLR 2024), Paper SparseGPT

## Recursos

- **Paper Wanda (ICLR 2024)**: https://arxiv.org/abs/2306.11695
- **GitHub Wanda**: https://github.com/locuslab/wanda
- **Paper SparseGPT**: https://arxiv.org/abs/2301.00774
- **GitHub SparseGPT**: https://github.com/IST-DASLab/sparsegpt
- **NVIDIA Sparse Tensor Cores**: https://developer.nvidia.com/blog/accelerating-inference-with-sparsity-using-ampere-and-tensorrt/