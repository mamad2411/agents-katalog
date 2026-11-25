---
name: nowait-reasoning-optimizer
description: Implementa a técnica NOWAIT para raciocínio eficiente em LLMs estilo R1. Use ao otimizar inferência de modelos de raciocínio (QwQ, DeepSeek-R1, Phi4-Reasoning, Qwen3, Kimi-VL, QvQ), reduzindo o uso de tokens chain-of-thought em 27-51% enquanto preserva a acurácia. Acionado por "otimizar raciocínio", "reduzir tokens de pensamento", "inferência eficiente", "suprimir tokens de reflexão" ou ao trabalhar com saídas CoT verbosas.
---

# NOWAIT Reasoning Optimizer

Implementa a técnica NOWAIT do paper "Wait, We Don't Need to 'Wait'! Removing Thinking Tokens Improves Reasoning Efficiency" (Wang et al., 2025).

## Visão Geral

NOWAIT é uma intervenção em tempo de inferência sem treinamento que suprime tokens de autorreflexão (ex: "Wait", "Hmm", "Alternatively") durante a geração, reduzindo o comprimento da trajetória chain-of-thought (CoT) em **27-51%** sem comprometer a utilidade do modelo.

## Quando Usar

- Deploying modelos de raciocínio estilo R1 com computação limitada
- Reduzindo latência de inferência para sistemas em produção
- Otimizando custos de tokens para tarefas de raciocínio
- Trabalhando com saídas CoT verbosas que precisam ser otimizadas

## Modelos Suportados

| Série de Modelos | Tipo | Redução de Tokens |
|------------------|------|-------------------|
| QwQ-32B | Baseado em RL | 16-31% |
| Phi4-Reasoning-Plus | Baseado em RL | 23-28% |
| Qwen3-32B | Baseado em RL | 13-16% |
| Kimi-VL-A3B | Multimodal | 40-60% |
| QvQ-72B-Preview | Multimodal | 20-30% |

**Importante**: NOWAIT funciona melhor com modelos baseados em RL. Modelos destilados (Qwen3-4B/8B/14B) mostram desempenho degradado quando tokens de reflexão são suprimidos.

## Início Rápido

### 1. Implementação Básica

```python
from scripts.nowait_processor import NOWAITLogitProcessor

# Inicializar processador para o tokenizer do seu modelo
processor = NOWAITLogitProcessor(tokenizer)

# Usar durante a geração
outputs = model.generate(
    inputs,
    logits_processor=[processor],
    max_new_tokens=32768
)
```

### 2. Palavras-chave Suprimidas

Veja `references/keywords.md` para a lista completa. Palavras-chave principais:

```
wait, alternatively, hmm, but, however, check, 
double-check, maybe, verify, again, oh, ah
```

## Como Funciona

1. **Inicializar Palavras-chave**: Identificar palavras-chave de reflexão a partir de análise empírica
2. **Expandir para Variantes de Tokens**: Mapear palavras-chave para todas as variantes de tokens no vocabulário (ex: "wait" → " wait", "Wait", " Wait", ".wait", "WAIT")
3. **Suprimir Durante Inferência**: Definir logits de tokens de reflexão como valores negativos grandes durante a decodificação

```
Logits (Antes)          Logits (Depois)
Wait     0.8     →     Wait     -inf
First    0.6     →     First    0.6
Hmm      0.5     →     Hmm      -inf
Let      0.4     →     Let      0.4
```

## Achados Principais

### Por que Funciona

- NOWAIT não elimina a autorreflexão inteiramente—guia modelos a pular raciocínio **desnecessário** de "espera"
- Modelos ainda realizam verificação essencial em pontos-chave de decisão
- Resulta em caminhos de raciocínio mais lineares e diretos

### Modelos Baseados em RL vs Destilados

| Tipo de Modelo | Efeito NOWAIT | Recomendação |
|---|---|---|
| Baseado em RL (QwQ, Phi4, Qwen3-32B) | Acurácia estável, redução significativa de tokens | ✅ Recomendado |
| Destilado (Qwen3-4B/8B/14B) | Degradação de acurácia em tarefas difíceis | ⚠️ Use com cautela |

Modelos destilados dependem fortemente da estrutura CoT dos dados de treinamento—remover tokens de reflexão desrupta seus padrões de raciocínio.

## Exemplos de Integração

### HuggingFace Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from scripts.nowait_processor import NOWAITLogitProcessor

model = AutoModelForCausalLM.from_pretrained("Qwen/QwQ-32B")
tokenizer = AutoTokenizer.from_pretrained("Qwen/QwQ-32B")

processor = NOWAITLogitProcessor(tokenizer)

response = model.generate(
    tokenizer(prompt, return_tensors="pt").input_ids,
    logits_processor=[processor],
    max_new_tokens=32768,
    do_sample=True,
    temperature=0.7
)
```

### vLLM

```python
from vllm import LLM, SamplingParams
from scripts.nowait_processor import get_nowait_bad_words_ids

llm = LLM(model="Qwen/QwQ-32B")
bad_words_ids = get_nowait_bad_words_ids(llm.get_tokenizer())

sampling_params = SamplingParams(
    max_tokens=32768,
    bad_words_ids=bad_words_ids
)
```

## Resultados Esperados

| Tipo de Tarefa | Tokens Originais | Tokens NOWAIT | Redução |
|---|---|---|---|
| Matemática (AIME) | 15.000 | 10.500 | 30% |
| Visual QA (MMMU) | 2.900 | 1.450 | 50% |
| Video QA (MMVU) | 1.700 | 1.250 | 27% |

## Limitações

- Menos eficaz em problemas muito simples onde o overhead de CoT já é mínimo
- Modelos destilados podem sofrer perda de acurácia em tarefas desafiadoras
- Alguns domínios podem exigir ajuste de palavras-chave específicas do modelo

## Referências

- Paper: arXiv:2506.08343v2
- Lista completa de palavras-chave: `references/keywords.md`
- Implementação: `scripts/nowait_processor.py`