---
name: speculative-decoding
description: Acelere a inferência de LLMs usando especulative decoding, múltiplas cabeças Medusa e técnicas de lookahead decoding. Use ao otimizar velocidade de inferência (aceleração de 1,5-3,6×), reduzir latência em aplicações em tempo real ou fazer deploy de modelos com recursos computacionais limitados. Cobre modelos draft, atenção em árvore, iteração de Jacobi, geração paralela de tokens e estratégias de deploy em produção.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Emerging Techniques, Speculative Decoding, Medusa, Lookahead Decoding, Fast Inference, Draft Models, Tree Attention, Parallel Generation, Latency Reduction, Inference Optimization]
dependencies: [transformers, torch]
---

# Especulative Decoding: Acelerando Inferência de LLMs

## Quando Usar Esta Skill

Use Especulative Decoding quando você precisa:
- **Acelerar inferência** de 1,5-3,6× sem perda de qualidade
- **Reduzir latência** para aplicações em tempo real (chatbots, geração de código)
- **Otimizar throughput** para serving de alto volume
- **Fazer deploy eficiente** em hardware limitado
- **Gerar mais rápido** sem alterar arquitetura de modelo

**Técnicas principais**: Especulative decoding com modelo draft, Medusa (múltiplas cabeças), Lookahead Decoding (iteração de Jacobi)

**Papers**: Medusa (arXiv 2401.10774), Lookahead Decoding (ICML 2024), Speculative Decoding Survey (ACL 2024)

## Instalação

```bash
# Especulative decoding padrão (transformers)
pip install transformers accelerate

# Medusa (múltiplas cabeças de decodificação)
git clone https://github.com/FasterDecoding/Medusa
cd Medusa
pip install -e .

# Lookahead Decoding
git clone https://github.com/hao-ai-lab/LookaheadDecoding
cd LookaheadDecoding
pip install -e .

# Opcional: vLLM com especulative decoding
pip install vllm
```

## Quick Start

### Especulative Decoding Básico (Modelo Draft)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Carregue o modelo alvo (grande, lento)
target_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-70b-hf",
    device_map="auto",
    torch_dtype=torch.float16
)

# Carregue o modelo draft (pequeno, rápido)
draft_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    device_map="auto",
    torch_dtype=torch.float16
)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-70b-hf")

# Gere com especulative decoding
prompt = "Explain quantum computing in simple terms:"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

# Transformers 4.36+ suporta assisted generation
outputs = target_model.generate(
    **inputs,
    assistant_model=draft_model,  # Ativa especulative decoding
    max_new_tokens=256,
    do_sample=True,
    temperature=0.7,
)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

### Medusa (Múltiplas Cabeças de Decodificação)

```python
from medusa.model.medusa_model import MedusaModel

# Carregue modelo aprimorado com Medusa
model = MedusaModel.from_pretrained(
    "FasterDecoding/medusa-vicuna-7b-v1.3",  # Pré-treinado com cabeças Medusa
    torch_dtype=torch.float16,
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained("FasterDecoding/medusa-vicuna-7b-v1.3")

# Gere com Medusa (aceleração de 2-3×)
prompt = "Write a Python function to calculate fibonacci numbers:"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

outputs = model.medusa_generate(
    **inputs,
    max_new_tokens=256,
    temperature=0.7,
    posterior_threshold=0.09,  # Limiar de aceitação
    posterior_alpha=0.3,       # Parâmetro de construção de árvore
)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### Lookahead Decoding (Iteração de Jacobi)

```python
from lookahead.lookahead_decoding import LookaheadDecoding

# Carregue modelo
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

# Inicialize lookahead decoding
lookahead = LookaheadDecoding(
    model=model,
    tokenizer=tokenizer,
    window_size=15,    # Janela de lookahead (W)
    ngram_size=5,      # Tamanho de n-grama (N)
    guess_size=5       # Número de palpites paralelos
)

# Gere (aceleração de 1,5-2,3×)
prompt = "Implement quicksort in Python:"
output = lookahead.generate(prompt, max_new_tokens=256)
print(output)
```

## Conceitos Fundamentais

### 1. Especulative Decoding (Modelo Draft)

**Ideia**: Use um modelo draft pequeno para gerar candidatos, modelo alvo grande para verificar em paralelo.

**Algoritmo**:
1. Modelo draft gera K tokens especulativamente
2. Modelo alvo avalia todos os K tokens em paralelo (um único forward pass)
3. Aceita tokens onde draft e alvo concordam
4. Rejeita primeiro desacordo, continua daí

```python
def speculative_decode(target_model, draft_model, prompt, K=4):
    """Algoritmo de especulative decoding."""
    # 1. Gere K tokens draft
    draft_tokens = draft_model.generate(prompt, max_new_tokens=K)

    # 2. Modelo alvo avalia todos os K tokens em um forward pass
    target_logits = target_model(draft_tokens)  # Paralelo!

    # 3. Aceite/rejeite com base em concordância de probabilidade
    accepted = []
    for i in range(K):
        p_draft = softmax(draft_model.logits[i])
        p_target = softmax(target_logits[i])

        # Probabilidade de aceitação
        if random.random() < min(1, p_target[draft_tokens[i]] / p_draft[draft_tokens[i]]):
            accepted.append(draft_tokens[i])
        else:
            break  # Rejeite, ressample do modelo alvo

    return accepted
```

**Performance**:
- Aceleração: 1,5-2× com bom modelo draft
- Zero perda de qualidade (matematicamente equivalente ao modelo alvo)
- Melhor quando modelo draft é 5-10× menor que o alvo

### 2. Medusa (Múltiplas Cabeças de Decodificação)

**Fonte**: arXiv 2401.10774 (2024)

**Inovação**: Adicione múltiplas cabeças de predição ao modelo existente, preveja tokens futuros sem modelo draft separado.

**Arquitetura**:
```
Input → LLM Base (congelado) → Estado Oculto
                                ├→ Cabeça 1 (prediz token t+1)
                                ├→ Cabeça 2 (prediz token t+2)
                                ├→ Cabeça 3 (prediz token t+3)
                                └→ Cabeça 4 (prediz token t+4)
```

**Treinamento**:
- **Medusa-1**: Congele LLM base, treine apenas cabeças
  - aceleração 2,2×, sem perda
- **Medusa-2**: Fine-tune LLM base + cabeças juntos
  - aceleração 2,3-3,6×, melhor qualidade

**Atenção em Árvore**:
```python
# Medusa constrói árvore de candidatos
# Exemplo: Prediga 2 passos à frente com top-2 por passo

#         Raiz
#        /    \
#      T1a    T1b  (Passo 1: 2 candidatos)
#     /  \    / \
#  T2a  T2b T2c T2d  (Passo 2: 4 candidatos totais)

# Um único forward pass avalia a árvore inteira!
```

**Vantagens**:
- Sem modelo draft separado necessário
- Treinamento mínimo (apenas cabeças)
- Compatível com qualquer LLM

### 3. Lookahead Decoding (Iteração de Jacobi)

**Fonte**: ICML 2024

**Ideia central**: Reformule decodificação autorregressiva como resolução de sistema de equações, resolva em paralelo usando iteração de Jacobi.

**Formulação matemática**:
```
Tradicional:  y_t = f(x, y_1, ..., y_{t-1})  (sequencial)
Jacobi:       y_t^{(k+1)} = f(x, y_1^{(k)}, ..., y_{t-1}^{(k)})  (paralelo)
```

**Dois ramos**:

1. **Ramo Lookahead**: Gere n-gramas em paralelo
   - Tamanho de janela W: Quantos passos olhar adiante
   - Tamanho de n-grama N: Quantos tokens passados usar

2. **Ramo de Verificação**: Verifique n-gramas promissores
   - Combine n-gramas com tokens gerados
   - Aceite se primeiro token combinar

```python
class LookaheadDecoding:
    def __init__(self, model, window_size=15, ngram_size=5):
        self.model = model
        self.W = window_size  # Janela lookahead
        self.N = ngram_size   # Tamanho de n-grama

    def generate_step(self, tokens):
        # Ramo lookahead: Gere W × N candidatos
        candidates = {}
        for w in range(1, self.W + 1):
            for n in range(1, self.N + 1):
                # Gere n-grama começando na posição w
                ngram = self.generate_ngram(tokens, start=w, length=n)
                candidates[(w, n)] = ngram

        # Ramo verificação: Encontre n-gramas combinando
        verified = []
        for ngram in candidates.values():
            if ngram[0] == tokens[-1]:  # Primeiro token combina com última entrada
                if self.verify(tokens, ngram):
                    verified.append(ngram)

        # Aceite n-grama verificado mais longo
        return max(verified, key=len) if verified else [self.model.generate_next(tokens)]
```

**Performance**:
- Aceleração: 1,5-2,3× (até 3,6× para geração de código)
- Sem modelo draft ou treinamento necessário
- Funciona imediatamente com qualquer modelo

## Comparação de Métodos

| Método | Aceleração | Treinamento | Modelo Draft | Perda de Qualidade |
|--------|-----------|-------------|-------------|-------------------|
| **Especulative Draft** | 1,5-2× | Não | Sim (externo) | Nenhuma |
| **Medusa** | 2-3,6× | Mínimo (apenas cabeças) | Não (cabeças integradas) | Nenhuma |
| **Lookahead** | 1,5-2,3× | Nenhum | Não | Nenhuma |
| **Naive Batching** | 1,2-1,5× | Não | Não | Nenhuma |

## Padrões Avançados

### Treinando Cabeças Medusa

```python
from medusa.model.medusa_model import MedusaModel
from medusa.model.kv_cache import initialize_past_key_values
import torch.nn as nn

# 1. Carregue modelo base
base_model = AutoModelForCausalLM.from_pretrained(
    "lmsys/vicuna-7b-v1.3",
    torch_dtype=torch.float16
)

# 2. Adicione cabeças Medusa
num_heads = 4
medusa_heads = nn.ModuleList([
    nn.Linear(base_model.config.hidden_size, base_model.config.vocab_size, bias=False)
    for _ in range(num_heads)
])

# 3. Loop de treinamento (congele modelo base para Medusa-1)
for param in base_model.parameters():
    param.requires_grad = False  # Congele base

optimizer = torch.optim.Adam(medusa_heads.parameters(), lr=1e-3)

for batch in dataloader:
    # Forward pass
    hidden_states = base_model(**batch, output_hidden_states=True).hidden_states[-1]

    # Prediga tokens futuros com cada cabeça
    loss = 0
    for i, head in enumerate(medusa_heads):
        logits = head(hidden_states)
        # Alvo: tokens deslocados por (i+1) posições
        target = batch['input_ids'][:, i+1:]
        loss += F.cross_entropy(logits[:, :-i-1], target)

    # Backward
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

### Híbrido: Especulative + Medusa

```python
# Use Medusa como modelo draft para especulative decoding
draft_medusa = MedusaModel.from_pretrained("medusa-vicuna-7b")
target_model = AutoModelForCausalLM.from_pretrained("vicuna-33b")

# Draft gera múltiplos candidatos com Medusa
draft_tokens = draft_medusa.medusa_generate(prompt, max_new_tokens=5)

# Alvo verifica em um único forward pass
outputs = target_model.generate(
    prompt,
    assistant_model=draft_medusa,  # Use Medusa como draft
    max_new_tokens=256
)

# Combina benefícios: velocidade Medusa + qualidade do modelo grande
```

### Seleção Otimizada de Modelo Draft

```python
def select_draft_model(target_model_size, target):
    """Selecione modelo draft otimizado para especulative decoding."""
    # Regra: Draft deve ser 5-10× menor
    if target_model_size == "70B":
        return "7B"  # 10× menor
    elif target_model_size == "33B":
        return "7B"  # 5× menor
    elif target_model_size == "13B":
        return "1B"  # 13× menor
    else:
        return None  # Alvo muito pequeno, use Medusa/Lookahead instead

# Exemplo
draft = select_draft_model("70B", target_model)
# Retorna "7B" → Use Llama-2-7b como draft para Llama-2-70b
```

## Melhores Práticas

### 1. Escolha o Método Correto

```python
# Novo deploy → Medusa (melhor aceleração geral, sem modelo draft)
if deploying_new_model:
    use_method = "Medusa"

# Deploy existente com versão pequena disponível → Draft especulative
elif have_small_version_of_model:
    use_method = "Draft Model Speculative"

# Quer zero treinamento/setup → Lookahead
elif want_plug_and_play:
    use_method = "Lookahead Decoding"
```

### 2. Ajuste de Hiperparâmetros

**Especulative Draft**:
```python
# K = número de tokens especulativos
K = 4  # Default bom
K = 2  # Conservador (maior aceitação)
K = 8  # Agressivo (menor aceitação, mas mais tokens quando aceito)

# Regra: Maior K → mais aceleração SE modelo draft é bom
```

**Medusa**:
```python
# Limiar posterior (confiança de aceitação)
posterior_threshold = 0.09  # Padrão (do paper)
posterior_threshold = 0.05  # Mais conservador (mais lento, maior qualidade)
posterior_threshold = 0.15  # Mais agressivo (mais rápido, pode degradar qualidade)

# Profundidade de árvore (quantos passos adiante)
medusa_choices = [[0], [0, 0], [0, 1], [0, 0, 0]]  # Profundidade 3 (padrão)
```

**Lookahead**:
```python
# Tamanho de janela W (distância lookahead)
# Tamanho de n-grama N (contexto para geração)

# Modelo 7B (mais recursos)
W, N = 15, 5

# Modelo 13B (moderado)
W, N = 10, 5

# Modelo 33B+ (recursos limitados)
W, N = 7, 5
```

### 3. Deploy em Produção

```python
# vLLM com especulative decoding
from vllm import LLM, SamplingParams

# Inicialize com modelo draft
llm = LLM(
    model="meta-llama/Llama-2-70b-hf",
    speculative_model="meta-llama/Llama-2-7b-hf",  # Modelo draft
    num_speculative_tokens=5,
    use_v2_block_manager=True,
)

# Gere
prompts = ["Tell me about AI:", "Explain quantum physics:"]
sampling_params = SamplingParams(temperature=0.7, max_tokens=256)

outputs = llm.generate(prompts, sampling_params)
for output in outputs:
    print(output.outputs[0].text)
```

## Recursos

- **Paper Medusa**: https://arxiv.org/abs/2401.10774
- **GitHub Medusa**: https://github.com/FasterDecoding/Medusa
- **Lookahead Decoding (ICML 2024)**: https://lmsys.org/blog/2023-11-21-lookahead-decoding/
- **GitHub Lookahead**: https://github.com/hao-ai-lab/LookaheadDecoding
- **Especulative Decoding Survey (ACL 2024)**: https://aclanthology.org/2024.findings-acl.456.pdf
- **Comprehensive Survey**: https://arxiv.org/abs/2401.07851

## Veja Também

- `references/draft_model.md` - Seleção e treinamento de modelo draft
- `references/medusa.md` - Arquitetura Medusa e treinamento
- `references/lookahead.md` - Detalhes de implementação de lookahead decoding