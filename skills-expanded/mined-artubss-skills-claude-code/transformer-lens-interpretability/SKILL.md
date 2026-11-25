---
name: transformer-lens-interpretability
description: Fornece orientação para pesquisa de interpretabilidade mecanística usando TransformerLens para inspecionar e manipular internals de transformers via HookPoints e caching de ativações. Use ao fazer engenharia reversa de algoritmos de modelos, estudar padrões de atenção ou realizar experimentos de activation patching.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Mechanistic Interpretability, TransformerLens, Activation Patching, Circuit Analysis]
dependencies: [transformer-lens>=2.0.0, torch>=2.0.0]
---

# TransformerLens: Interpretabilidade Mecanística para Transformers

TransformerLens é a biblioteca padrão de facto para pesquisa de interpretabilidade mecanística em modelos de linguagem estilo GPT. Criada por Neel Nanda e mantida por Bryce Meyer, fornece interfaces limpas para inspecionar e manipular internals de modelos via HookPoints em cada ativação.

**GitHub**: [TransformerLensOrg/TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) (2.900+ stars)

## Quando Usar TransformerLens

**Use TransformerLens quando você precisar:**
- Fazer engenharia reversa de algoritmos aprendidos durante o treinamento
- Realizar experimentos de activation patching / causal tracing
- Estudar padrões de atenção e fluxo de informações
- Analisar circuits (ex: induction heads, IOI circuit)
- Cachear e inspecionar ativações intermediárias
- Aplicar direct logit attribution

**Considere alternativas quando:**
- Você precisa trabalhar com arquiteturas não-transformer → Use **nnsight** ou **pyvene**
- Você quer treinar/analisar Sparse Autoencoders → Use **SAELens**
- Você precisa de execução remota em modelos massivos → Use **nnsight** com NDIF
- Você quer abstrações de intervenção causal de nível superior → Use **pyvene**

## Instalação

```bash
pip install transformer-lens
```

Para versão de desenvolvimento:
```bash
pip install git+https://github.com/TransformerLensOrg/TransformerLens
```

## Conceitos Principais

### HookedTransformer

A classe principal que envolve modelos transformer com HookPoints em cada ativação:

```python
from transformer_lens import HookedTransformer

# Carrega um modelo
model = HookedTransformer.from_pretrained("gpt2-small")

# Para modelos com gating (LLaMA, Mistral)
import os
os.environ["HF_TOKEN"] = "your_token"
model = HookedTransformer.from_pretrained("meta-llama/Llama-2-7b-hf")
```

### Modelos Suportados (50+)

| Família | Modelos |
|---------|---------|
| GPT-2 | gpt2, gpt2-medium, gpt2-large, gpt2-xl |
| LLaMA | llama-7b, llama-13b, llama-2-7b, llama-2-13b |
| EleutherAI | pythia-70m to pythia-12b, gpt-neo, gpt-j-6b |
| Mistral | mistral-7b, mixtral-8x7b |
| Outros | phi, qwen, opt, gemma |

### Caching de Ativações

Execute o modelo e cachee todas as ativações intermediárias:

```python
# Obtém todas as ativações
tokens = model.to_tokens("The Eiffel Tower is in")
logits, cache = model.run_with_cache(tokens)

# Acessa ativações específicas
residual = cache["resid_post", 5]  # Residual stream da camada 5
attn_pattern = cache["pattern", 3]  # Padrão de atenção da camada 3
mlp_out = cache["mlp_out", 7]  # Saída MLP da camada 7

# Filtra quais ativações cachear (economiza memória)
logits, cache = model.run_with_cache(
    tokens,
    names_filter=lambda name: "resid_post" in name
)
```

### Chaves do ActivationCache

| Padrão de Chave | Forma | Descrição |
|-----------------|-------|-----------|
| `resid_pre, layer` | [batch, pos, d_model] | Residual antes de atenção |
| `resid_mid, layer` | [batch, pos, d_model] | Residual depois de atenção |
| `resid_post, layer` | [batch, pos, d_model] | Residual depois de MLP |
| `attn_out, layer` | [batch, pos, d_model] | Saída de atenção |
| `mlp_out, layer` | [batch, pos, d_model] | Saída MLP |
| `pattern, layer` | [batch, head, q_pos, k_pos] | Padrão de atenção (pós-softmax) |
| `q, layer` | [batch, pos, head, d_head] | Vetores de query |
| `k, layer` | [batch, pos, head, d_head] | Vetores de key |
| `v, layer` | [batch, pos, head, d_head] | Vetores de value |

## Fluxo de Trabalho 1: Activation Patching (Causal Tracing)

Identifique quais ativações causalmente afetam a saída do modelo ao fazer patch de ativações limpas em execuções corrompidas.

### Passo a Passo

```python
from transformer_lens import HookedTransformer, patching
import torch

model = HookedTransformer.from_pretrained("gpt2-small")

# 1. Define prompts limpos e corrompidos
clean_prompt = "The Eiffel Tower is in the city of"
corrupted_prompt = "The Colosseum is in the city of"

clean_tokens = model.to_tokens(clean_prompt)
corrupted_tokens = model.to_tokens(corrupted_prompt)

# 2. Obtém ativações limpas
_, clean_cache = model.run_with_cache(clean_tokens)

# 3. Define métrica (ex: logit difference)
paris_token = model.to_single_token(" Paris")
rome_token = model.to_single_token(" Rome")

def metric(logits):
    return logits[0, -1, paris_token] - logits[0, -1, rome_token]

# 4. Faz patch de cada posição e camada
results = torch.zeros(model.cfg.n_layers, clean_tokens.shape[1])

for layer in range(model.cfg.n_layers):
    for pos in range(clean_tokens.shape[1]):
        def patch_hook(activation, hook):
            activation[0, pos] = clean_cache[hook.name][0, pos]
            return activation

        patched_logits = model.run_with_hooks(
            corrupted_tokens,
            fwd_hooks=[(f"blocks.{layer}.hook_resid_post", patch_hook)]
        )
        results[layer, pos] = metric(patched_logits)

# 5. Visualiza resultados (heatmap camada x posição)
```

### Checklist
- [ ] Define inputs limpos e corrompidos que diferem minimamente
- [ ] Escolhe métrica que capture diferença de comportamento
- [ ] Cacheia ativações limpas
- [ ] Sistematicamente faz patch de cada combinação (camada, posição)
- [ ] Visualiza resultados como heatmap
- [ ] Identifica hotspots causais

## Fluxo de Trabalho 2: Análise de Circuit (Indirect Object Identification)

Replique a descoberta do circuit IOI de "Interpretability in the Wild".

### Passo a Passo

```python
from transformer_lens import HookedTransformer
import torch

model = HookedTransformer.from_pretrained("gpt2-small")

# Tarefa IOI: "When John and Mary went to the store, Mary gave a bottle to"
# Modelo deve prever "John" (indirect object)

prompt = "When John and Mary went to the store, Mary gave a bottle to"
tokens = model.to_tokens(prompt)

# 1. Obtém logits de baseline
logits, cache = model.run_with_cache(tokens)

john_token = model.to_single_token(" John")
mary_token = model.to_single_token(" Mary")

# 2. Calcula logit difference (IO - S)
logit_diff = logits[0, -1, john_token] - logits[0, -1, mary_token]
print(f"Logit difference: {logit_diff.item():.3f}")

# 3. Direct logit attribution por head
def get_head_contribution(layer, head):
    # Projeta saída de head para logits
    head_out = cache["z", layer][0, :, head, :]  # [pos, d_head]
    W_O = model.W_O[layer, head]  # [d_head, d_model]
    W_U = model.W_U  # [d_model, vocab]

    # Contribuição de head para logits na posição final
    contribution = head_out[-1] @ W_O @ W_U
    return contribution[john_token] - contribution[mary_token]

# 4. Mapeia todos os heads
head_contributions = torch.zeros(model.cfg.n_layers, model.cfg.n_heads)
for layer in range(model.cfg.n_layers):
    for head in range(model.cfg.n_heads):
        head_contributions[layer, head] = get_head_contribution(layer, head)

# 5. Identifica heads com maior contribuição (name movers, backup name movers)
```

### Checklist
- [ ] Configura tarefa com tokens IO/S claros
- [ ] Calcula logit difference de baseline
- [ ] Decompõe por contribuições de attention head
- [ ] Identifica componentes principais do circuit (name movers, S-inhibition, induction)
- [ ] Valida com experimentos de ablation

## Fluxo de Trabalho 3: Detecção de Induction Head

Encontre induction heads que implementam o padrão [A][B]...[A] → [B].

```python
from transformer_lens import HookedTransformer
import torch

model = HookedTransformer.from_pretrained("gpt2-small")

# Cria sequência repetida: [A][B][A] deve prever [B]
repeated_tokens = torch.tensor([[1000, 2000, 1000]])  # Tokens arbitrários

_, cache = model.run_with_cache(repeated_tokens)

# Induction heads atendem da posição final [A] de volta para a primeira [B]
# Verifica atenção da posição 2 para posição 1
induction_scores = torch.zeros(model.cfg.n_layers, model.cfg.n_heads)

for layer in range(model.cfg.n_layers):
    pattern = cache["pattern", layer][0]  # [head, q_pos, k_pos]
    # Atenção de pos 2 para pos 1
    induction_scores[layer] = pattern[:, 2, 1]

# Heads com scores altos são induction heads
top_heads = torch.topk(induction_scores.flatten(), k=5)
```

## Problemas Comuns e Soluções

### Problema: Hooks persistem após debugging
```python
# ERRADO: Hooks antigos permanecem ativos
model.run_with_hooks(tokens, fwd_hooks=[...])  # Debug, adiciona novos hooks
model.run_with_hooks(tokens, fwd_hooks=[...])  # Hooks antigos ainda lá!

# CORRETO: Sempre reseta hooks
model.reset_hooks()
model.run_with_hooks(tokens, fwd_hooks=[...])
```

### Problema: Pegadinhas de tokenização
```python
# ERRADO: Assumindo tokenização consistente
model.to_tokens("Tim")  # Token único
model.to_tokens("Neel")  # Vira "Ne" + "el" (dois tokens!)

# CORRETO: Verifica tokenização explicitamente
tokens = model.to_tokens("Neel", prepend_bos=False)
print(model.to_str_tokens(tokens))  # ['Ne', 'el']
```

### Problema: LayerNorm ignorado na análise
```python
# ERRADO: Ignorando LayerNorm
pre_activation = residual @ model.W_in[layer]

# CORRETO: Inclui LayerNorm
ln_scale = model.blocks[layer].ln2.w
ln_out = model.blocks[layer].ln2(residual)
pre_activation = ln_out @ model.W_in[layer]
```

### Problema: Explosão de memória com modelos grandes
```python
# Use caching seletivo
logits, cache = model.run_with_cache(
    tokens,
    names_filter=lambda n: "resid_post" in n or "pattern" in n,
    device="cpu"  # Cacheia em CPU
)
```

## Referência de Classes Principais

| Classe | Propósito |
|--------|-----------|
| `HookedTransformer` | Wrapper de modelo principal com hooks |
| `ActivationCache` | Cache tipo dicionário de ativações |
| `HookedTransformerConfig` | Configuração de modelo |
| `FactoredMatrix` | Operações eficientes de matriz fatorada |

## Integração com SAELens

TransformerLens integra com SAELens para análise de Sparse Autoencoder:

```python
from transformer_lens import HookedTransformer
from sae_lens import SAE

model = HookedTransformer.from_pretrained("gpt2-small")
sae = SAE.from_pretrained("gpt2-small-res-jb", "blocks.8.hook_resid_pre")

# Executa com SAE
tokens = model.to_tokens("Hello world")
_, cache = model.run_with_cache(tokens)
sae_acts = sae.encode(cache["resid_pre", 8])
```

## Documentação de Referência

Para documentação detalhada da API, tutoriais e uso avançado, veja a pasta `references/`:

| Arquivo | Conteúdo |
|---------|----------|
| [references/README.md](references/README.md) | Visão geral e guia de início rápido |
| [references/api.md](references/api.md) | Referência completa da API para HookedTransformer, ActivationCache, HookPoints |
| [references/tutorials.md](references/tutorials.md) | Tutoriais passo a passo para activation patching, circuit analysis, logit lens |

## Recursos Externos

### Tutoriais
- [Main Demo Notebook](https://transformerlensorg.github.io/TransformerLens/generated/demos/Main_Demo.html)
- [Activation Patching Demo](https://colab.research.google.com/github/TransformerLensOrg/TransformerLens/blob/main/demos/Activation_Patching_in_TL_Demo.ipynb)
- [ARENA Mech Interp Course](https://arena-foundation.github.io/ARENA/) - 200+ horas de tutoriais

### Artigos
- [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html)
- [In-context Learning and Induction Heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html)
- [Interpretability in the Wild (IOI)](https://arxiv.org/abs/2211.00593)

### Documentação Oficial
- [Official Docs](https://transformerlensorg.github.io/TransformerLens/)
- [Model Properties Table](https://transformerlensorg.github.io/TransformerLens/generated/model_properties_table.html)
- [Neel Nanda's Glossary](https://www.neelnanda.io/mechanistic-interpretability/glossary)

## Notas de Versão

- **v2.0**: Removido HookedSAE (movido para SAELens)
- **v3.0 (alpha)**: TransformerBridge para carregar qualquer nn.Module