---
name: pyvene-interventions
description: Fornece orientação para realizar intervenções causais em modelos PyTorch usando o framework de intervenção declarativa do pyvene. Use ao conduzir rastreamento causal, activation patching, treinamento de intervenção de intercâmbio ou testar hipóteses causais sobre o comportamento do modelo.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Causal Intervention, pyvene, Activation Patching, Causal Tracing, Interpretability]
dependencies: [pyvene>=0.1.8, torch>=2.0.0, transformers>=4.30.0]
---

# pyvene: Intervenções Causais para Redes Neurais

pyvene é a biblioteca do Stanford NLP para realizar intervenções causais em modelos PyTorch. Ela fornece um framework declarativo baseado em dicionário para activation patching, rastreamento causal e treinamento de intervenção de intercâmbio — tornando experimentos de intervenção reproduzíveis e compartilháveis.

**GitHub**: [stanfordnlp/pyvene](https://github.com/stanfordnlp/pyvene) (840+ stars)
**Paper**: [pyvene: A Library for Understanding and Improving PyTorch Models via Interventions](https://aclanthology.org/2024.naacl-demo.16) (NAACL 2024)

## Quando Usar pyvene

**Use pyvene quando você precisar:**
- Realizar rastreamento causal (localização estilo ROME)
- Executar experimentos de activation patching
- Conduzir treinamento de intervenção de intercâmbio (IIT)
- Testar hipóteses causais sobre componentes do modelo
- Compartilhar/reproduzir experimentos de intervenção via HuggingFace
- Trabalhar com qualquer arquitetura PyTorch (não apenas transformers)

**Considere alternativas quando:**
- Você precisa de análise exploratória de ativações → Use **TransformerLens**
- Você quer treinar/analisar SAEs → Use **SAELens**
- Você precisa executar em larga escala em modelos massivos → Use **nnsight**
- Você quer controle de nível inferior → Use **nnsight**

## Instalação

```bash
pip install pyvene
```

Import padrão:
```python
import pyvene as pv
```

## Conceitos Principais

### IntervenableModel

A classe principal que encapsula qualquer modelo PyTorch com capacidades de intervenção:

```python
import pyvene as pv
from transformers import AutoModelForCausalLM, AutoTokenizer

# Carrega o modelo base
model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Define configuração de intervenção
config = pv.IntervenableConfig(
    representations=[
        pv.RepresentationConfig(
            layer=8,
            component="block_output",
            intervention_type=pv.VanillaIntervention,
        )
    ]
)

# Cria modelo intervenável
intervenable = pv.IntervenableModel(config, model)
```

### Tipos de Intervenção

| Tipo | Descrição | Caso de Uso |
|------|-----------|-----------|
| `VanillaIntervention` | Troca ativações entre execuções | Activation patching |
| `AdditionIntervention` | Adiciona ativações à execução base | Steering, ablação |
| `SubtractionIntervention` | Subtrai ativações | Ablação |
| `ZeroIntervention` | Zera ativações | Knockout de componentes |
| `RotatedSpaceIntervention` | Intervenção treinável DAS | Descoberta causal |
| `CollectIntervention` | Coleta ativações | Probing, análise |

### Alvos de Componentes

```python
# Componentes disponíveis para intervir
components = [
    "block_input",      # Entrada para bloco transformer
    "block_output",     # Saída do bloco transformer
    "mlp_input",        # Entrada para MLP
    "mlp_output",       # Saída de MLP
    "mlp_activation",   # Ativações ocultas do MLP
    "attention_input",  # Entrada para attention
    "attention_output", # Saída de attention
    "attention_value_output",  # Vetores de valor de attention
    "query_output",     # Vetores de query
    "key_output",       # Vetores de chave
    "value_output",     # Vetores de valor
    "head_attention_value_output",  # Valores por cabeça
]
```

## Workflow 1: Rastreamento Causal (estilo ROME)

Localize onde associações factuais são armazenadas corrompendo entradas e restaurando ativações.

### Passo a Passo

```python
import pyvene as pv
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained("gpt2-xl")
tokenizer = AutoTokenizer.from_pretrained("gpt2-xl")

# 1. Define entradas limpas e corrompidas
clean_prompt = "The Space Needle is in downtown"
corrupted_prompt = "The ##### ###### ## ## ########"  # Ruído

clean_tokens = tokenizer(clean_prompt, return_tensors="pt")
corrupted_tokens = tokenizer(corrupted_prompt, return_tensors="pt")

# 2. Obtém ativações limpas (fonte)
with torch.no_grad():
    clean_outputs = model(**clean_tokens, output_hidden_states=True)
    clean_states = clean_outputs.hidden_states

# 3. Define intervenção de restauração
def run_causal_trace(layer, position):
    """Restaura ativação limpa em camada e posição específicas."""
    config = pv.IntervenableConfig(
        representations=[
            pv.RepresentationConfig(
                layer=layer,
                component="block_output",
                intervention_type=pv.VanillaIntervention,
                unit="pos",
                max_number_of_units=1,
            )
        ]
    )

    intervenable = pv.IntervenableModel(config, model)

    # Executa com intervenção
    _, patched_outputs = intervenable(
        base=corrupted_tokens,
        sources=[clean_tokens],
        unit_locations={"sources->base": ([[[position]]], [[[position]]])},
        output_original_output=True,
    )

    # Retorna probabilidade do token correto
    probs = torch.softmax(patched_outputs.logits[0, -1], dim=-1)
    seattle_token = tokenizer.encode(" Seattle")[0]
    return probs[seattle_token].item()

# 4. Varre sobre camadas e posições
n_layers = model.config.n_layer
seq_len = clean_tokens["input_ids"].shape[1]

results = torch.zeros(n_layers, seq_len)
for layer in range(n_layers):
    for pos in range(seq_len):
        results[layer, pos] = run_causal_trace(layer, pos)

# 5. Visualiza (mapa de calor camada x posição)
# Valores altos indicam importância causal
```

### Checklist
- [ ] Prepare prompt limpo com associação factual alvo
- [ ] Crie versão corrompida (ruído ou contrafactual)
- [ ] Define config de intervenção para cada (camada, posição)
- [ ] Executa varredura de patching
- [ ] Identifica hotspots causais no mapa de calor

## Workflow 2: Activation Patching para Análise de Circuitos

Teste quais componentes são necessários para um comportamento específico.

### Passo a Passo

```python
import pyvene as pv
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Setup tarefa IOI
clean_prompt = "When John and Mary went to the store, Mary gave a bottle to"
corrupted_prompt = "When John and Mary went to the store, John gave a bottle to"

clean_tokens = tokenizer(clean_prompt, return_tensors="pt")
corrupted_tokens = tokenizer(corrupted_prompt, return_tensors="pt")

john_token = tokenizer.encode(" John")[0]
mary_token = tokenizer.encode(" Mary")[0]

def logit_diff(logits):
    """Diferença de logits IO - S."""
    return logits[0, -1, john_token] - logits[0, -1, mary_token]

# Patch saída de attention em cada camada
def patch_attention(layer):
    config = pv.IntervenableConfig(
        representations=[
            pv.RepresentationConfig(
                layer=layer,
                component="attention_output",
                intervention_type=pv.VanillaIntervention,
            )
        ]
    )

    intervenable = pv.IntervenableModel(config, model)

    _, patched_outputs = intervenable(
        base=corrupted_tokens,
        sources=[clean_tokens],
    )

    return logit_diff(patched_outputs.logits).item()

# Encontra quais camadas importam
results = []
for layer in range(model.config.n_layer):
    diff = patch_attention(layer)
    results.append(diff)
    print(f"Layer {layer}: logit diff = {diff:.3f}")
```

## Workflow 3: Treinamento de Intervenção de Intercâmbio (IIT)

Treine intervenções para descobrir estrutura causal.

### Passo a Passo

```python
import pyvene as pv
from transformers import AutoModelForCausalLM
import torch

model = AutoModelForCausalLM.from_pretrained("gpt2")

# 1. Define intervenção treinável
config = pv.IntervenableConfig(
    representations=[
        pv.RepresentationConfig(
            layer=6,
            component="block_output",
            intervention_type=pv.RotatedSpaceIntervention,  # Treinável
            low_rank_dimension=64,  # Aprende subespaço 64-dim
        )
    ]
)

intervenable = pv.IntervenableModel(config, model)

# 2. Configura treinamento
optimizer = torch.optim.Adam(
    intervenable.get_trainable_parameters(),
    lr=1e-4
)

# 3. Loop de treinamento (simplificado)
for base_input, source_input, target_output in dataloader:
    optimizer.zero_grad()

    _, outputs = intervenable(
        base=base_input,
        sources=[source_input],
    )

    loss = criterion(outputs.logits, target_output)
    loss.backward()
    optimizer.step()

# 4. Analisa intervenção aprendida
# A matriz de rotação revela subespaço causal
rotation = intervenable.interventions["layer.6.block_output"][0].rotate_layer
```

### DAS (Distributed Alignment Search)

```python
# Rotação de baixo rank encontra subespaços interpretáveis
config = pv.IntervenableConfig(
    representations=[
        pv.RepresentationConfig(
            layer=8,
            component="block_output",
            intervention_type=pv.LowRankRotatedSpaceIntervention,
            low_rank_dimension=1,  # Encontra direção causal 1D
        )
    ]
)
```

## Workflow 4: Steering de Modelo (Honest LLaMA)

Conduza o comportamento do modelo durante a geração.

```python
import pyvene as pv
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

# Carrega intervenção de steering pré-treinada
intervenable = pv.IntervenableModel.load(
    "zhengxuanzenwu/intervenable_honest_llama2_chat_7B",
    model=model,
)

# Gera com steering
prompt = "Is the earth flat?"
inputs = tokenizer(prompt, return_tensors="pt")

# Intervenção aplicada durante geração
outputs = intervenable.generate(
    inputs,
    max_new_tokens=100,
    do_sample=False,
)

print(tokenizer.decode(outputs[0]))
```

## Salvando e Compartilhando Intervenções

```python
# Salva localmente
intervenable.save("./my_intervention")

# Carrega de local
intervenable = pv.IntervenableModel.load(
    "./my_intervention",
    model=model,
)

# Compartilha no HuggingFace
intervenable.save_intervention("username/my-intervention")

# Carrega do HuggingFace
intervenable = pv.IntervenableModel.load(
    "username/my-intervention",
    model=model,
)
```

## Problemas Comuns & Soluções

### Problema: Local de intervenção incorreto
```python
# ERRADO: Nome de componente incorreto
config = pv.RepresentationConfig(
    component="mlp",  # Inválido!
)

# CORRETO: Use nome exato do componente
config = pv.RepresentationConfig(
    component="mlp_output",  # Válido
)
```

### Problema: Incompatibilidade de dimensão
```python
# Garanta que fonte e base tenham formas compatíveis
# Para intervenções específicas de posição:
config = pv.RepresentationConfig(
    unit="pos",
    max_number_of_units=1,  # Intervém em posição única
)

# Especifique localizações explicitamente
intervenable(
    base=base_tokens,
    sources=[source_tokens],
    unit_locations={"sources->base": ([[[5]]], [[[5]]])},  # Posição 5
)
```

### Problema: Memória com modelos grandes
```python
# Use gradient checkpointing
model.gradient_checkpointing_enable()

# Ou intervenha em menos componentes
config = pv.IntervenableConfig(
    representations=[
        pv.RepresentationConfig(
            layer=8,  # Camada única em vez de todas
            component="block_output",
        )
    ]
)
```

### Problema: Integração LoRA
```python
# pyvene v0.1.8+ suporta LoRAs como intervenções
config = pv.RepresentationConfig(
    intervention_type=pv.LoRAIntervention,
    low_rank_dimension=16,
)
```

## Referência de Classes Principais

| Classe | Propósito |
|--------|-----------|
| `IntervenableModel` | Wrapper principal para intervenções |
| `IntervenableConfig` | Container de configuração |
| `RepresentationConfig` | Especificação de intervenção única |
| `VanillaIntervention` | Troca de ativações |
| `RotatedSpaceIntervention` | Intervenção DAS treinável |
| `CollectIntervention` | Coleta de ativações |

## Modelos Suportados

pyvene funciona com qualquer modelo PyTorch. Testado em:
- GPT-2 (todos os tamanhos)
- LLaMA / LLaMA-2
- Pythia
- Mistral / Mixtral
- OPT
- BLIP (vision-language)
- ESM (modelos de proteína)
- Mamba (state space)

## Documentação de Referência

Para documentação detalhada da API, tutoriais e uso avançado, veja a pasta `references/`:

| Arquivo | Conteúdo |
|---------|----------|
| [references/README.md](references/README.md) | Visão geral e guia de início rápido |
| [references/api.md](references/api.md) | Referência completa da API para IntervenableModel, tipos de intervenção, configurações |
| [references/tutorials.md](references/tutorials.md) | Tutoriais passo a passo para rastreamento causal, activation patching, DAS |

## Recursos Externos

### Tutoriais
- [pyvene 101](https://stanfordnlp.github.io/pyvene/tutorials/pyvene_101.html)
- [Tutorial de Rastreamento Causal](https://stanfordnlp.github.io/pyvene/tutorials/advanced_tutorials/Causal_Tracing.html)
- [Replicação de Circuito IOI](https://stanfordnlp.github.io/pyvene/tutorials/advanced_tutorials/IOI_Replication.html)
- [Introdução a DAS](https://stanfordnlp.github.io/pyvene/tutorials/advanced_tutorials/DAS_Main_Introduction.html)

### Papers
- [Locating and Editing Factual Associations in GPT](https://arxiv.org/abs/2202.05262) - Meng et al. (2022)
- [Inference-Time Intervention](https://arxiv.org/abs/2306.03341) - Li et al. (2023)
- [Interpretability in the Wild](https://arxiv.org/abs/2211.00593) - Wang et al. (2022)

### Documentação Oficial
- [Docs Oficiais](https://stanfordnlp.github.io/pyvene/)
- [Referência da API](https://stanfordnlp.github.io/pyvene/api/)

## Comparação com Outras Ferramentas

| Funcionalidade | pyvene | TransformerLens | nnsight |
|---|---|---|---|
| Config declarativa | Sim | Não | Não |
| Compartilhamento HuggingFace | Sim | Não | Não |
| Intervenções treináveis | Sim | Limitado | Sim |
| Qualquer modelo PyTorch | Sim | Apenas Transformers | Sim |
| Execução remota | Não | Não | Sim (NDIF) |