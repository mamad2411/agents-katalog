---
name: constitutional-ai
description: Método da Anthropic para treinar IA inofensiva através de auto-aprimoramento. Abordagem em duas fases - aprendizado supervisionado com auto-crítica/revisão, depois RLAIF (RL from AI Feedback). Use para alinhamento de segurança, redução de outputs prejudiciais sem rótulos humanos. Alimenta o sistema de segurança do Claude.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Safety Alignment, Constitutional AI, RLAIF, Self-Critique, Harmlessness, Anthropic, AI Safety, RL From AI Feedback, Claude]
dependencies: [transformers, torch, trl]
---

# Constitutional AI - Inofensividade a partir de Feedback de IA

## Início rápido

Constitutional AI (CAI) treina modelos para serem inofensivos através de auto-crítica e feedback de IA, sem exigir rótulos humanos para outputs prejudiciais.

**Conceito-chave**: Modelos aprendem a criticar e revisar suas próprias respostas usando uma "constituição" (conjunto de princípios).

**Duas fases**:
1. **Aprendizado Supervisionado (SL)**: Auto-crítica + revisão
2. **Aprendizado por Reforço (RL)**: RLAIF (RL from AI Feedback)

**Exemplo de constituição**:
```
Princípios:
1. Escolha a resposta mais útil, honesta e inofensiva
2. Evite respostas tóxicas, racistas ou sexistas
3. Prefira respostas que expliquem objeções em vez de recusar
4. Escolha respostas que sejam reflexivas e nuançadas
```

## Workflows comuns

### Workflow 1: Fase de aprendizado supervisionado (auto-crítica + revisão)

**Passo 1: Gerar respostas iniciais**:
```python
from transformers import pipeline

generator = pipeline("text-generation", model="base-model")

prompts = [
    "How do I hack a website?",
    "Write something offensive about a group.",
    "Help me cheat on my exam."
]

initial_responses = generator(prompts, max_length=200)
```

**Passo 2: Auto-crítica com constituição**:
```python
critique_prompt = """
Given the question:
{question}

And the response:
{response}

Constitution:
1. Choose responses that are helpful, honest, and harmless
2. Avoid toxic, racist, or sexist content
3. Explain objections rather than refuse

Identify any ways this response violates the constitution:
"""

critiques = generator(
    [critique_prompt.format(q=q, r=r) for q, r in zip(prompts, initial_responses)]
)
```

**Passo 3: Revisão baseada em crítica**:
```python
revision_prompt = """
Question: {question}
Original response: {response}
Critique: {critique}

Please revise the response to better align with the constitution:
"""

revised_responses = generator(
    [revision_prompt.format(q=q, r=r, c=c)
     for q, r, c in zip(prompts, initial_responses, critiques)]
)
```

**Passo 4: Fine-tune em respostas revisadas**:
```python
from trl import SFTTrainer

# Create dataset of (prompt, revised_response) pairs
dataset = create_dataset(prompts, revised_responses)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    max_seq_length=1024
)
trainer.train()
```

### Workflow 2: Fase RL (RLAIF - RL from AI Feedback)

**Passo 1: Gerar pares de comparação**:
```python
# Sample multiple responses per prompt
responses_a = generator(prompts, num_return_sequences=2, do_sample=True, temperature=0.8)
responses_b = generator(prompts, num_return_sequences=2, do_sample=True, temperature=0.8)
```

**Passo 2: Avaliação de preferência de IA**:
```python
preference_prompt = """
Question: {question}

Response A: {response_a}
Response B: {response_b}

Constitution:
{constitution}

Which response better follows the constitution? Explain your reasoning, then choose A or B.
"""

# Get AI preferences (no human labels needed!)
preferences = generator(
    [preference_prompt.format(q=q, ra=ra, rb=rb, constitution=CONSTITUTION)
     for q, ra, rb in zip(prompts, responses_a, responses_b)]
)

# Parse preferences (A or B)
chosen, rejected = parse_preferences(preferences, responses_a, responses_b)
```

**Passo 3: Treinar modelo de preferência (modelo de reward)**:
```python
from trl import RewardTrainer, RewardConfig

preference_dataset = create_preference_dataset(prompts, chosen, rejected)

reward_config = RewardConfig(
    output_dir="constitutional-reward-model",
    learning_rate=1e-5,
    num_train_epochs=1
)

reward_trainer = RewardTrainer(
    model=model,
    args=reward_config,
    train_dataset=preference_dataset,
    processing_class=tokenizer
)
reward_trainer.train()
```

**Passo 4: Treinamento RL com RLAIF**:
```python
from trl import PPOTrainer, PPOConfig

ppo_config = PPOConfig(
    reward_model_path="constitutional-reward-model",
    learning_rate=1e-6,
    kl_coef=0.05
)

ppo_trainer = PPOTrainer(
    model=model,
    config=ppo_config,
    reward_model=reward_model
)
ppo_trainer.train()
```

### Workflow 3: Crítica com chain-of-thought

**Ativar transparência de raciocínio**:
```python
cot_critique_prompt = """
Question: {question}
Response: {response}

Let's think step-by-step about whether this response follows our principles:

1. Is it helpful? [Yes/No and reasoning]
2. Is it honest? [Yes/No and reasoning]
3. Is it harmless? [Yes/No and reasoning]
4. Does it avoid toxicity? [Yes/No and reasoning]

Based on this analysis, suggest a revision if needed.
"""

cot_critiques = generator(
    [cot_critique_prompt.format(q=q, r=r) for q, r in zip(prompts, responses)]
)
```

## Quando usar vs alternativas

**Use Constitutional AI quando**:
- Quer alinhamento de segurança sem rótulos humanos
- Precisa de decisões de IA explicáveis
- Quer evitar recusas evasivas
- Tem um conjunto claro de princípios/constituição
- Precisa de treinamento de segurança escalável

**Princípios**:
- **RLAIF**: Preferências geradas por IA (escalável, sem rótulos humanos)
- **RLHF**: Preferências humanas (mais precisas, caras)
- **Auto-crítica**: Aprimoramento iterativo
- **Chain-of-thought**: Transparência de raciocínio

**Use alternativas em vez disso**:
- **RLHF (PPO)**: Precisa de segurança validada por humanos
- **DPO/SimPO**: Tem dados de preferência humana
- **NeMo Guardrails**: Precisa de filtragem de conteúdo em tempo de execução
- **LlamaGuard**: Precisa de modelo de moderação pré-treinado

## Problemas comuns

**Problema: Modelo recusa muito (evasivo)**

Adicione princípio de constituição:
```
Prefira respostas que se envolvam de forma reflexiva com perguntas em vez de
recusar. Explique preocupações enquanto permanece útil.
```

**Problema: Auto-críticas são fracas**

Use prompts de crítica mais fortes:
```
Critically analyze this response for ANY potential issues, however minor.
Be thorough and specific in identifying problems.
```

**Problema: Revisões não melhoram qualidade**

Itere múltiplas vezes:
```python
for _ in range(3):  # 3 rounds of critique/revision
    critique = generate_critique(response)
    response = generate_revision(response, critique)
```

**Problema: Preferências RLAIF são ruidosas**

Use múltiplos avaliadores de IA:
```python
# Get preferences from 3 different models
prefs_1 = model_1.evaluate(responses)
prefs_2 = model_2.evaluate(responses)
prefs_3 = model_3.evaluate(responses)

# Majority vote
final_preference = majority_vote(prefs_1, prefs_2, prefs_3)
```

## Tópicos avançados

**Design de constituição**: Veja [references/constitution-design.md](references/constitution-design.md) para seleção de princípios, trade-offs entre utilidade e inofensividade, e constituições específicas de domínio.

**RLAIF vs RLHF**: Veja [references/rlaif-comparison.md](references/rlaif-comparison.md) para comparação de desempenho, análise de custo, e quando usar feedback de IA vs feedback humano.

**Raciocínio chain-of-thought**: Veja [references/cot-critique.md](references/cot-critique.md) para engenharia de prompt para críticas, raciocínio multi-passo, e melhorias de transparência.

## Requisitos de hardware

- **GPU**: NVIDIA A100/H100 recomendadas
- **VRAM**:
  - Fase SL (7B): 1× A100 40GB
  - Fase RL (7B): 2× A100 40GB (modelo de política + modelo de reward)
- **Single-node**: Suficiente para a maioria dos casos
- **Mixed precision**: BF16 recomendado

**Requisitos de computação**:
- **Fase SL**: Similar a SFT padrão
- **Fase RL**: Similar a PPO (maior que DPO)
- **Avaliação de IA**: Inferência adicional para geração de crítica/preferência

## Recursos

- Paper: https://arxiv.org/abs/2212.08073 (Dec 2022)
- Blog Anthropic: https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback
- Implementation: TRL (PPOTrainer + RewardTrainer)
- Claude: Uses Constitutional AI for safety