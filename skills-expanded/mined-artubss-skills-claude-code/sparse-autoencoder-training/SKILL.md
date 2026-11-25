---
name: sparse-autoencoder-training
description: Fornece orientação para treinar e analisar Autoencodificadores Esparsos (SAEs) usando SAELens para decompor ativações de redes neurais em features interpretáveis. Use ao descobrir features interpretáveis, analisar superposição ou estudar representações monossemânticas em modelos de linguagem.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Sparse Autoencoders, SAE, Mechanistic Interpretability, Feature Discovery, Superposition]
dependencies: [sae-lens>=6.0.0, transformer-lens>=2.0.0, torch>=2.0.0]
---

# SAELens: Autoencodificadores Esparsos para Interpretabilidade Mecanicista

SAELens é a biblioteca principal para treinar e analisar Autoencodificadores Esparsos (SAEs) — uma técnica para decompor ativações polissemânticas de redes neurais em features esparsas e interpretáveis. Baseado na pesquisa groundbreaking da Anthropic sobre monossemânticidade.

**GitHub**: [jbloomAus/SAELens](https://github.com/jbloomAus/SAELens) (1.100+ stars)

## O Problema: Polissemânticidade & Superposição

Neurônios individuais em redes neurais são **polissemânticos** — ativam em múltiplos contextos semanticamente distintos. Isso ocorre porque modelos usam **superposição** para representar mais features do que neurônios possuem, dificultando a interpretabilidade.

**SAEs resolvem isso** decompondo ativações densas em features esparsas e monossemânticas — tipicamente apenas um pequeno número de features ativa para qualquer entrada, e cada feature corresponde a um conceito interpretável.

## Quando Usar SAELens

**Use SAELens quando precisar:**
- Descobrir features interpretáveis em ativações de modelos
- Entender quais conceitos um modelo aprendeu
- Estudar superposição e geometria de features
- Realizar direcionamento ou ablação baseados em features
- Analisar features relevantes para segurança (engano, viés, conteúdo prejudicial)

**Considere alternativas quando:**
- Precisar de análise básica de ativações → Use **TransformerLens** diretamente
- Quiser experimentos de intervenção causal → Use **pyvene** ou **TransformerLens**
- Precisar de direcionamento em produção → Considere engenharia direta de ativações

## Instalação

```bash
pip install sae-lens
```

Requisitos: Python 3.10+, transformer-lens>=2.0.0

## Conceitos Principais

### O Que SAEs Aprendem

SAEs são treinados para reconstruir ativações de modelos através de um gargalo esparso:

```
Ativação Entrada → Encoder → Features Esparsas → Decoder → Ativação Reconstruída
    (d_model)       ↓        (d_sae >> d_model)    ↓         (d_model)
                 penalidade                     perda de
                 de                          reconstrução
                 esparsidade
```

**Função de Perda**: `MSE(original, reconstruída) + L1_coefficient × L1(features)`

### Validação Chave (Pesquisa Anthropic)

Em "Towards Monosemanticity", avaliadores humanos encontraram **70% das features de SAE genuinamente interpretáveis**. Features descobertas incluem:
- Sequências de DNA, linguagem jurídica, requisições HTTP
- Texto em hebraico, declarações nutricionais, sintaxe de código
- Sentimento, entidades nomeadas, estruturas gramaticais

## Workflow 1: Carregando e Analisando SAEs Pré-treinadas

### Passo a Passo

```python
from transformer_lens import HookedTransformer
from sae_lens import SAE

# 1. Carregar modelo e SAE pré-treinada
model = HookedTransformer.from_pretrained("gpt2-small", device="cuda")
sae, cfg_dict, sparsity = SAE.from_pretrained(
    release="gpt2-small-res-jb",
    sae_id="blocks.8.hook_resid_pre",
    device="cuda"
)

# 2. Obter ativações do modelo
tokens = model.to_tokens("The capital of France is Paris")
_, cache = model.run_with_cache(tokens)
activations = cache["resid_pre", 8]  # [batch, pos, d_model]

# 3. Codificar para features de SAE
sae_features = sae.encode(activations)  # [batch, pos, d_sae]
print(f"Active features: {(sae_features > 0).sum()}")

# 4. Encontrar features principais para cada posição
for pos in range(tokens.shape[1]):
    top_features = sae_features[0, pos].topk(5)
    token = model.to_str_tokens(tokens[0, pos:pos+1])[0]
    print(f"Token '{token}': features {top_features.indices.tolist()}")

# 5. Reconstruir ativações
reconstructed = sae.decode(sae_features)
reconstruction_error = (activations - reconstructed).norm()
```

### SAEs Pré-treinadas Disponíveis

| Release | Modelo | Camadas |
|---------|--------|---------|
| `gpt2-small-res-jb` | GPT-2 Small | Múltiplos fluxos residuais |
| `gemma-2b-res` | Gemma 2B | Fluxos residuais |
| Vários no HuggingFace | Pesquisar tag `saelens` | Vários |

### Checklist
- [ ] Carregar modelo com TransformerLens
- [ ] Carregar SAE correspondente para camada alvo
- [ ] Codificar ativações para features esparsas
- [ ] Identificar features principais ativadas por token
- [ ] Validar qualidade de reconstrução

## Workflow 2: Treinando uma SAE Personalizada

### Passo a Passo

```python
from sae_lens import SAE, LanguageModelSAERunnerConfig, SAETrainingRunner

# 1. Configurar treinamento
cfg = LanguageModelSAERunnerConfig(
    # Modelo
    model_name="gpt2-small",
    hook_name="blocks.8.hook_resid_pre",
    hook_layer=8,
    d_in=768,  # Dimensão do modelo

    # Arquitetura SAE
    architecture="standard",  # ou "gated", "topk"
    d_sae=768 * 8,  # Fator de expansão de 8
    activation_fn="relu",

    # Treinamento
    lr=4e-4,
    l1_coefficient=8e-5,  # Penalidade de esparsidade
    l1_warm_up_steps=1000,
    train_batch_size_tokens=4096,
    training_tokens=100_000_000,

    # Dados
    dataset_path="monology/pile-uncopyrighted",
    context_size=128,

    # Logging
    log_to_wandb=True,
    wandb_project="sae-training",

    # Checkpointing
    checkpoint_path="checkpoints",
    n_checkpoints=5,
)

# 2. Treinar
trainer = SAETrainingRunner(cfg)
sae = trainer.run()

# 3. Avaliar
print(f"L0 (features ativas em média): {trainer.metrics['l0']}")
print(f"CE Loss Recuperada: {trainer.metrics['ce_loss_score']}")
```

### Hiperparâmetros Principais

| Parâmetro | Valor Típico | Efeito |
|-----------|--------------|--------|
| `d_sae` | 4-16× d_model | Mais features, capacidade maior |
| `l1_coefficient` | 5e-5 a 1e-4 | Maior = mais esparso, menos preciso |
| `lr` | 1e-4 a 1e-3 | LR padrão de otimizador |
| `l1_warm_up_steps` | 500-2000 | Previne morte prematura de features |

### Métricas de Avaliação

| Métrica | Alvo | Significado |
|---------|------|-------------|
| **L0** | 50-200 | Features ativas em média por token |
| **CE Loss Score** | 80-95% | Cross-entropy recuperada vs. original |
| **Dead Features** | <5% | Features que nunca ativam |
| **Explained Variance** | >90% | Qualidade de reconstrução |

### Checklist
- [ ] Escolher camada alvo e hook point
- [ ] Definir fator de expansão (d_sae = 4-16× d_model)
- [ ] Ajustar coeficiente L1 para esparsidade desejada
- [ ] Habilitar warm-up de L1 para prevenir dead features
- [ ] Monitorar métricas durante treinamento (W&B)
- [ ] Validar L0 e recuperação de CE loss
- [ ] Verificar razão de dead features

## Workflow 3: Análise de Features e Direcionamento

### Analisando Features Individuais

```python
from transformer_lens import HookedTransformer
from sae_lens import SAE
import torch

model = HookedTransformer.from_pretrained("gpt2-small", device="cuda")
sae, _, _ = SAE.from_pretrained(
    release="gpt2-small-res-jb",
    sae_id="blocks.8.hook_resid_pre",
    device="cuda"
)

# Encontrar o que ativa uma feature específica
feature_idx = 1234
test_texts = [
    "The scientist conducted an experiment",
    "I love chocolate cake",
    "The code compiles successfully",
    "Paris is beautiful in spring",
]

for text in test_texts:
    tokens = model.to_tokens(text)
    _, cache = model.run_with_cache(tokens)
    features = sae.encode(cache["resid_pre", 8])
    activation = features[0, :, feature_idx].max().item()
    print(f"{activation:.3f}: {text}")
```

### Direcionamento de Features

```python
def steer_with_feature(model, sae, prompt, feature_idx, strength=5.0):
    """Adicionar direção de feature de SAE ao fluxo residual."""
    tokens = model.to_tokens(prompt)

    # Obter direção de feature do decoder
    feature_direction = sae.W_dec[feature_idx]  # [d_model]

    def steering_hook(activation, hook):
        # Adicionar direção de feature escalada em todas as posições
        activation += strength * feature_direction
        return activation

    # Gerar com direcionamento
    output = model.generate(
        tokens,
        max_new_tokens=50,
        fwd_hooks=[("blocks.8.hook_resid_pre", steering_hook)]
    )
    return model.to_string(output[0])
```

### Atribuição de Features

```python
# Quais features mais afetam um output específico?
tokens = model.to_tokens("The capital of France is")
_, cache = model.run_with_cache(tokens)

# Obter features na posição final
features = sae.encode(cache["resid_pre", 8])[0, -1]  # [d_sae]

# Obter atribuição de logit por feature
# Contribuição = ativação_feature × peso_decoder × unembedding
W_dec = sae.W_dec  # [d_sae, d_model]
W_U = model.W_U    # [d_model, vocab]

# Contribuição para logit "Paris"
paris_token = model.to_single_token(" Paris")
feature_contributions = features * (W_dec @ W_U[:, paris_token])

top_features = feature_contributions.topk(10)
print("Features principais para previsão de 'Paris':")
for idx, val in zip(top_features.indices, top_features.values):
    print(f"  Feature {idx.item()}: {val.item():.3f}")
```

## Problemas Comuns & Soluções

### Problema: Alta razão de dead features
```python
# ERRADO: Sem warm-up, features morrem cedo
cfg = LanguageModelSAERunnerConfig(
    l1_coefficient=1e-4,
    l1_warm_up_steps=0,  # Ruim!
)

# CORRETO: Warm-up de penalidade L1
cfg = LanguageModelSAERunnerConfig(
    l1_coefficient=8e-5,
    l1_warm_up_steps=1000,  # Aumentar gradualmente
    use_ghost_grads=True,   # Reviver dead features
)
```

### Problema: Reconstrução ruim (baixa recuperação de CE)
```python
# Reduzir penalidade de esparsidade
cfg = LanguageModelSAERunnerConfig(
    l1_coefficient=5e-5,  # Menor = melhor reconstrução
    d_sae=768 * 16,       # Mais capacidade
)
```

### Problema: Features não interpretáveis
```python
# Aumentar esparsidade (L1 maior)
cfg = LanguageModelSAERunnerConfig(
    l1_coefficient=1e-4,  # Maior = mais esparso, mais interpretável
)
# Ou usar arquitetura TopK
cfg = LanguageModelSAERunnerConfig(
    architecture="topk",
    activation_fn_kwargs={"k": 50},  # Exatamente 50 features ativas
)
```

### Problema: Erros de memória durante treinamento
```python
cfg = LanguageModelSAERunnerConfig(
    train_batch_size_tokens=2048,  # Reduzir tamanho de batch
    store_batch_size_prompts=4,    # Menos prompts no buffer
    n_batches_in_buffer=8,         # Buffer de ativações menor
)
```

## Integração com Neuronpedia

Navegar por features de SAE pré-treinadas em [neuronpedia.org](https://neuronpedia.org):

```python
# Features são indexadas por SAE ID
# Exemplo: gpt2-small layer 8 feature 1234
# → neuronpedia.org/gpt2-small/8-res-jb/1234
```

## Referência de Classes Principais

| Classe | Propósito |
|--------|-----------|
| `SAE` | Modelo de Autoencodificador Esparso |
| `LanguageModelSAERunnerConfig` | Configuração de treinamento |
| `SAETrainingRunner` | Gerenciador do loop de treinamento |
| `ActivationsStore` | Coleta e batching de ativações |
| `HookedSAETransformer` | Integração TransformerLens + SAE |

## Documentação de Referência

Para documentação detalhada da API, tutoriais e uso avançado, veja a pasta `references/`:

| Arquivo | Conteúdo |
|---------|----------|
| [references/README.md](references/README.md) | Visão geral e guia de início rápido |
| [references/api.md](references/api.md) | Referência completa da API para SAE, TrainingSAE, configurações |
| [references/tutorials.md](references/tutorials.md) | Tutoriais passo a passo para treinamento, análise, direcionamento |

## Recursos Externos

### Tutoriais
- [Basic Loading & Analysis](https://github.com/jbloomAus/SAELens/blob/main/tutorials/basic_loading_and_analysing.ipynb)
- [Training a Sparse Autoencoder](https://github.com/jbloomAus/SAELens/blob/main/tutorials/training_a_sparse_autoencoder.ipynb)
- [ARENA SAE Curriculum](https://www.lesswrong.com/posts/LnHowHgmrMbWtpkxx/intro-to-superposition-and-sparse-autoencoders-colab)

### Artigos
- [Towards Monosemanticity](https://transformer-circuits.pub/2023/monosemantic-features) - Anthropic (2023)
- [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/) - Anthropic (2024)
- [Sparse Autoencoders Find Highly Interpretable Features](https://arxiv.org/abs/2309.08600) - Cunningham et al. (ICLR 2024)

### Documentação Oficial
- [SAELens Docs](https://jbloomaus.github.io/SAELens/)
- [Neuronpedia](https://neuronpedia.org) - Navegador de features

## Arquiteturas de SAE

| Arquitetura | Descrição | Caso de Uso |
|-------------|-----------|-------------|
| **Standard** | ReLU + penalidade L1 | Propósito geral |
| **Gated** | Mecanismo de gating aprendido | Melhor controle de esparsidade |
| **TopK** | Exatamente K features ativas | Esparsidade consistente |

```python
# SAE TopK (exatamente 50 features ativas)
cfg = LanguageModelSAERunnerConfig(
    architecture="topk",
    activation_fn="topk",
    activation_fn_kwargs={"k": 50},
)
```