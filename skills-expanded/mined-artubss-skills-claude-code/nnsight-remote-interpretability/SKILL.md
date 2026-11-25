---
name: nnsight-remote-interpretability
description: Fornece orientação para interpretar e manipular internals de redes neurais usando nnsight com execução remota NDIF opcional. Use quando precisar executar experimentos de interpretabilidade em modelos massivos (70B+) sem recursos locais de GPU, ou ao trabalhar com qualquer arquitetura PyTorch.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [nnsight, NDIF, Remote Execution, Mechanistic Interpretability, Model Internals]
dependencies: [nnsight>=0.5.0, torch>=2.0.0]
---

# nnsight: Acesso Transparente aos Internals de Redes Neurais

nnsight (/ɛn.saɪt/) permite que pesquisadores interpretem e manipulem os internals de qualquer modelo PyTorch, com a capacidade única de executar o mesmo código localmente em modelos pequenos ou remotamente em modelos massivos (70B+) via NDIF.

**GitHub**: [ndif-team/nnsight](https://github.com/ndif-team/nnsight) (730+ stars)
**Paper**: [NNsight and NDIF: Democratizing Access to Foundation Model Internals](https://arxiv.org/abs/2407.14561) (ICLR 2025)

## Proposta de Valor Principal

**Escreva uma vez, execute em qualquer lugar**: O mesmo código de interpretabilidade funciona em GPT-2 localmente ou em Llama-3.1-405B remotamente. Basta alternar `remote=True`.

```python
# Execução local (modelo pequeno)
with model.trace("Hello world"):
    hidden = model.transformer.h[5].output[0].save()

# Execução remota (modelo massivo) - mesmo código!
with model.trace("Hello world", remote=True):
    hidden = model.model.layers[40].output[0].save()
```

## Quando Usar nnsight

**Use nnsight quando você precisa:**
- Executar experimentos de interpretabilidade em modelos grandes demais para GPUs locais (70B, 405B)
- Trabalhar com qualquer arquitetura PyTorch (transformers, Mamba, modelos customizados)
- Realizar intervenções de geração multi-token
- Compartilhar ativações entre diferentes prompts
- Acessar os internals completos do modelo sem reimplementação

**Considere alternativas quando:**
- Você quer API consistente entre modelos → Use **TransformerLens**
- Você precisa de intervenções declarativas e compartilháveis → Use **pyvene**
- Você está treinando SAEs → Use **SAELens**
- Você trabalha apenas com modelos pequenos localmente → **TransformerLens** pode ser mais simples

## Instalação

```bash
# Instalação básica
pip install nnsight

# Para suporte vLLM
pip install "nnsight[vllm]"
```

Para execução remota NDIF, inscreva-se em [login.ndif.us](https://login.ndif.us) para obter uma chave de API.

## Conceitos Principais

### Wrapper LanguageModel

```python
from nnsight import LanguageModel

# Carrega modelo (usa HuggingFace internamente)
model = LanguageModel("openai-community/gpt2", device_map="auto")

# Para modelos maiores
model = LanguageModel("meta-llama/Llama-3.1-8B", device_map="auto")
```

### Contexto de Tracing

O context manager `trace` permite execução diferida - operações são coletadas em um grafo computacional:

```python
from nnsight import LanguageModel

model = LanguageModel("gpt2", device_map="auto")

with model.trace("The Eiffel Tower is in") as tracer:
    # Acessa a saída de qualquer módulo
    hidden_states = model.transformer.h[5].output[0].save()

    # Acessa padrões de atenção
    attn = model.transformer.h[5].attn.attn_dropout.input[0][0].save()

    # Modifica ativações
    model.transformer.h[8].output[0][:] = 0  # Zera a camada 8

    # Obtém saída final
    logits = model.output.save()

# Após sair do contexto, acessa valores salvos
print(hidden_states.shape)  # [batch, seq, hidden]
```

### Objetos Proxy

Dentro de `trace`, acessos a módulos retornam objetos Proxy que registram operações:

```python
with model.trace("Hello"):
    # Estes são todos objetos Proxy - operações são diferidas
    h5_out = model.transformer.h[5].output[0]  # Proxy
    h5_mean = h5_out.mean(dim=-1)              # Proxy
    h5_saved = h5_mean.save()                   # Salva para acesso posterior
```

## Workflow 1: Análise de Ativações

### Passo a Passo

```python
from nnsight import LanguageModel
import torch

model = LanguageModel("gpt2", device_map="auto")

prompt = "The capital of France is"

with model.trace(prompt) as tracer:
    # 1. Coleta ativações de múltiplas camadas
    layer_outputs = []
    for i in range(12):  # GPT-2 tem 12 camadas
        layer_out = model.transformer.h[i].output[0].save()
        layer_outputs.append(layer_out)

    # 2. Obtém padrões de atenção
    attn_patterns = []
    for i in range(12):
        # Acessa pesos de atenção (após softmax)
        attn = model.transformer.h[i].attn.attn_dropout.input[0][0].save()
        attn_patterns.append(attn)

    # 3. Obtém logits finais
    logits = model.output.save()

# 4. Analisa fora do contexto
for i, layer_out in enumerate(layer_outputs):
    print(f"Saída camada {i}: {layer_out.shape}")
    print(f"Norma camada {i}: {layer_out.norm().item():.3f}")

# 5. Encontra principais predições
probs = torch.softmax(logits[0, -1], dim=-1)
top_tokens = probs.topk(5)
for token, prob in zip(top_tokens.indices, top_tokens.values):
    print(f"{model.tokenizer.decode(token)}: {prob.item():.3f}")
```

### Checklist
- [ ] Carrega modelo com wrapper LanguageModel
- [ ] Usa contexto trace para operações
- [ ] Chama `.save()` em valores que você precisa após o contexto
- [ ] Acessa valores salvos fora do contexto
- [ ] Usa `.shape`, `.norm()`, etc. para análise

## Workflow 2: Patching de Ativações

### Passo a Passo

```python
from nnsight import LanguageModel
import torch

model = LanguageModel("gpt2", device_map="auto")

prompt_limpo = "The Eiffel Tower is in"
prompt_corrompido = "The Colosseum is in"

# 1. Obtém ativações limpas
with model.trace(prompt_limpo) as tracer:
    hidden_limpo = model.transformer.h[8].output[0].save()

# 2. Faz patch limpo em execução corrompida
with model.trace(prompt_corrompido) as tracer:
    # Substitui saída da camada 8 com ativações limpas
    model.transformer.h[8].output[0][:] = hidden_limpo

    logits_patch = model.output.save()

# 3. Compara predições
paris_token = model.tokenizer.encode(" Paris")[0]
rome_token = model.tokenizer.encode(" Rome")[0]

probs_patch = torch.softmax(logits_patch[0, -1], dim=-1)
print(f"Prob Paris: {probs_patch[paris_token].item():.3f}")
print(f"Prob Roma: {probs_patch[rome_token].item():.3f}")
```

### Varredura Sistemática de Patching

```python
def patch_layer_position(layer, position, clean_cache, prompt_corrompido):
    """Faz patch de camada/posição única de limpo para corrompido."""
    with model.trace(prompt_corrompido) as tracer:
        # Obtém ativação atual
        current = model.transformer.h[layer].output[0]

        # Faz patch apenas de posição específica
        current[:, position, :] = clean_cache[layer][:, position, :]

        logits = model.output.save()

    return logits

# Varre todas as camadas e posições
results = torch.zeros(12, seq_len)
for layer in range(12):
    for pos in range(seq_len):
        logits = patch_layer_position(layer, pos, hidden_limpo, prompt_corrompido)
        results[layer, pos] = compute_metric(logits)
```

## Workflow 3: Execução Remota com NDIF

Execute os mesmos experimentos em modelos massivos sem GPUs locais.

### Passo a Passo

```python
from nnsight import LanguageModel

# 1. Carrega modelo grande (será executado remotamente)
model = LanguageModel("meta-llama/Llama-3.1-70B")

# 2. Mesmo código, basta adicionar remote=True
with model.trace("The meaning of life is", remote=True) as tracer:
    # Acessa internals do modelo 70B!
    layer_40_out = model.model.layers[40].output[0].save()
    logits = model.output.save()

# 3. Resultados retornados de NDIF
print(f"Forma camada 40: {layer_40_out.shape}")

# 4. Geração com intervenções
with model.trace(remote=True) as tracer:
    with tracer.invoke("What is 2+2?"):
        # Intervém durante geração
        model.model.layers[20].output[0][:, -1, :] *= 1.5

    output = model.generate(max_new_tokens=50)
```

### Setup NDIF

1. Inscreva-se em [login.ndif.us](https://login.ndif.us)
2. Obtenha chave de API
3. Defina variável de ambiente ou passe para nnsight:

```python
import os
os.environ["NDIF_API_KEY"] = "your_key"

# Ou configure diretamente
from nnsight import CONFIG
CONFIG.API_KEY = "your_key"
```

### Modelos Disponíveis em NDIF

- Llama-3.1-8B, 70B, 405B
- Modelos DeepSeek-R1
- Vários modelos open-weight (verifique [ndif.us](https://ndif.us) para lista atual)

## Workflow 4: Compartilhamento de Ativações Entre Prompts

Compartilha ativações entre diferentes inputs em um único trace.

```python
from nnsight import LanguageModel

model = LanguageModel("gpt2", device_map="auto")

with model.trace() as tracer:
    # Primeiro prompt
    with tracer.invoke("The cat sat on the"):
        hidden_gato = model.transformer.h[6].output[0].save()

    # Segundo prompt - injeta ativações do gato
    with tracer.invoke("The dog ran through the"):
        # Substitui com ativações do gato na camada 6
        model.transformer.h[6].output[0][:] = hidden_gato
        cachorro_com_gato = model.output.save()

# O prompt do cachorro agora tem representações internas do gato
```

## Workflow 5: Análise Baseada em Gradientes

Acessa gradientes durante backward pass.

```python
from nnsight import LanguageModel
import torch

model = LanguageModel("gpt2", device_map="auto")

with model.trace("The quick brown fox") as tracer:
    # Salva ativações e habilita gradiente
    hidden = model.transformer.h[5].output[0].save()
    hidden.retain_grad()

    logits = model.output

    # Computa loss em token específico
    target_token = model.tokenizer.encode(" jumps")[0]
    loss = -logits[0, -1, target_token]

    # Backward pass
    loss.backward()

# Acessa gradientes
grad = hidden.grad
print(f"Forma gradiente: {grad.shape}")
print(f"Norma gradiente: {grad.norm().item():.3f}")
```

**Nota**: Acesso a gradientes não é suportado para vLLM ou execução remota.

## Problemas Comuns e Soluções

### Problema: Caminho do módulo diferente entre modelos
```python
# Estrutura GPT-2
model.transformer.h[5].output[0]

# Estrutura LLaMA
model.model.layers[5].output[0]

# Solução: Verifica estrutura do modelo
print(model._model)  # Vê nomes reais dos módulos
```

### Problema: Esqueceu de salvar
```python
# ERRADO: Valor não acessível fora do trace
with model.trace("Hello"):
    hidden = model.transformer.h[5].output[0]  # Não salvo!

print(hidden)  # Erro ou valor errado

# CORRETO: Chama .save()
with model.trace("Hello"):
    hidden = model.transformer.h[5].output[0].save()

print(hidden)  # Funciona!
```

### Problema: Timeout remoto
```python
# Para operações longas, aumenta timeout
with model.trace("prompt", remote=True, timeout=300) as tracer:
    # Operação longa...
```

### Problema: Memória com muitas ativações salvas
```python
# Salva apenas o que você precisa
with model.trace("prompt"):
    # Não salva tudo
    for i in range(100):
        model.transformer.h[i].output[0].save()  # Pesado em memória!

    # Melhor: salva camadas específicas
    camadas_chave = [0, 5, 11]
    for i in camadas_chave:
        model.transformer.h[i].output[0].save()
```

### Problema: Limitação de gradiente vLLM
```python
# vLLM não suporta gradientes
# Use execução padrão para análise de gradientes
model = LanguageModel("gpt2", device_map="auto")  # Não vLLM
```

## Referência de API Chave

| Método/Propriedade | Propósito |
|-----------------|---------|
| `model.trace(prompt, remote=False)` | Inicia contexto de tracing |
| `proxy.save()` | Salva valor para acesso após trace |
| `proxy[:]` | Slice/índice de proxy (assignment faz patch) |
| `tracer.invoke(prompt)` | Adiciona prompt dentro de trace |
| `model.generate(...)` | Gera com intervenções |
| `model.output` | Logits de saída final do modelo |
| `model._model` | Modelo HuggingFace subjacente |

## Comparação com Outras Ferramentas

| Funcionalidade | nnsight | TransformerLens | pyvene |
|---------|---------|-----------------|--------|
| Qualquer arquitetura | Sim | Apenas Transformers | Sim |
| Execução remota | Sim (NDIF) | Não | Não |
| API consistente | Não | Sim | Sim |
| Execução diferida | Sim | Não | Não |
| HuggingFace nativo | Sim | Reimplementado | Sim |
| Configs compartilháveis | Não | Não | Sim |

## Documentação de Referência

Para documentação detalhada de API, tutoriais e uso avançado, veja a pasta `references/`:

| Arquivo | Conteúdo |
|------|----------|
| [references/README.md](references/README.md) | Visão geral e guia de início rápido |
| [references/api.md](references/api.md) | Referência completa de API para LanguageModel, tracing, objetos proxy |
| [references/tutorials.md](references/tutorials.md) | Tutoriais passo a passo para interpretabilidade local e remota |

## Recursos Externos

### Tutoriais
- [Getting Started](https://nnsight.net/start/)
- [Features Overview](https://nnsight.net/features/)
- [Remote Execution](https://nnsight.net/notebooks/features/remote_execution/)
- [Applied Tutorials](https://nnsight.net/applied_tutorials/)

### Documentação Oficial
- [Official Docs](https://nnsight.net/documentation/)
- [NDIF Info](https://ndif.us/)
- [Community Forum](https://discuss.ndif.us/)

### Artigos
- [NNsight and NDIF Paper](https://arxiv.org/abs/2407.14561) - Fiotto-Kaufman et al. (ICLR 2025)

## Suporte a Arquiteturas

nnsight funciona com qualquer modelo PyTorch:
- **Transformers**: GPT-2, LLaMA, Mistral, etc.
- **Modelos State Space**: Mamba
- **Modelos Vision**: ViT, CLIP
- **Arquiteturas customizadas**: Qualquer nn.Module

A chave é conhecer a estrutura do módulo para acessar os componentes certos.