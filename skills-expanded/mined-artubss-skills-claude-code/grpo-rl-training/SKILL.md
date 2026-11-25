---
name: grpo-rl-training
description: Orientação especializada para ajuste fino com GRPO/RL usando TRL para treinamento de modelos com raciocínio e tarefas específicas
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Post-Training, Reinforcement Learning, GRPO, TRL, RLHF, Reward Modeling, Reasoning, DPO, PPO, Structured Output]
dependencies: [transformers>=4.47.0, trl>=0.14.0, datasets>=3.2.0, peft>=0.14.0, torch]
---

# Treinamento GRPO/RL com TRL

Orientação em nível especializado para implementar Group Relative Policy Optimization (GRPO) usando a biblioteca Transformer Reinforcement Learning (TRL). Esta skill fornece padrões testados em produção, insights críticos e workflows prontos para produção no ajuste fino de modelos de linguagem com funções de recompensa customizadas.

## Quando Usar Esta Skill

Use treinamento GRPO quando precisar:
- **Impor formatos de saída específicos** (ex: tags XML, JSON, raciocínio estruturado)
- **Ensinar tarefas verificáveis** com métricas de correção objetivas (matemática, coding, verificação de fatos)
- **Melhorar capacidades de raciocínio** recompensando padrões chain-of-thought
- **Alinhar modelos a comportamentos específicos de domínio** sem dados de preferência rotulados
- **Otimizar múltiplos objetivos** simultaneamente (formato + correção + estilo)

**NÃO use GRPO para:**
- Tarefas simples de ajuste fino supervisionado (use SFT em vez disso)
- Tarefas sem sinais de recompensa claros
- Quando você já possui pares de preferência de alta qualidade (use DPO/PPO em vez disso)

---

## Conceitos Fundamentais

### 1. Fundamentos do Algoritmo GRPO

**Mecanismo Chave:**
- Gera **múltiplas conclusões** para cada prompt (tamanho do grupo: 4-16)
- Compara conclusões dentro de cada grupo usando funções de recompensa
- Atualiza a política para favorecer respostas com recompensa maior em relação ao grupo

**Diferença Crítica do PPO:**
- Não requer modelo de recompensa separado
- Mais eficiente em amostragem (aprende de comparações dentro do grupo)
- Mais simples de implementar e debugar

**Intuição Matemática:**
```
Para cada prompt p:
  1. Gera N conclusões: {c₁, c₂, ..., cₙ}
  2. Calcula recompensas: {r₁, r₂, ..., rₙ}
  3. Aprende a aumentar a probabilidade de conclusões com alta recompensa
     relativas às de baixa recompensa no mesmo grupo
```

### 2. Filosofia de Design de Função de Recompensa

**Regras de Ouro:**
1. **Componha múltiplas funções de recompensa** - Cada uma lida com um aspecto (formato, correção, estilo)
2. **Dimensione recompensas apropriadamente** - Peso maior = sinal mais forte
3. **Use recompensas incrementais** - Crédito parcial para conformidade parcial
4. **Teste recompensas independentemente** - Debugue cada função em isolamento

**Tipos de Função de Recompensa:**

| Tipo | Caso de Uso | Peso Exemplo |
|------|----------|----------------|
| **Correção** | Tarefas verificáveis (matemática, código) | 2.0 (maior) |
| **Formato** | Imposição de estrutura rigorosa | 0.5-1.0 |
| **Comprimento** | Encorajar verbosidade/concisão | 0.1-0.5 |
| **Estilo** | Penalizar padrões indesejados | -0.5 a 0.5 |

---

## Workflow de Implementação

### Passo 1: Preparação de Dataset

**Requisitos Críticos:**
- Prompts em formato chat (lista de dicts com 'role' e 'content')
- Incluir prompts de sistema para definir expectativas
- Para tarefas verificáveis, incluir respostas de verdade fundamental como colunas adicionais

**Exemplo de Estrutura:**
```python
from datasets import load_dataset, Dataset

SYSTEM_PROMPT = """
Responda no seguinte formato:
<reasoning>
[Seu pensamento passo a passo]
</reasoning>
<answer>
[Resposta final]
</answer>
"""

def prepare_dataset(raw_data):
    """
    Transforma dados brutos em formato compatível com GRPO.

    Retorna: Dataset com colunas:
    - 'prompt': List[Dict] com role/content (mensagens de sistema + usuário)
    - 'answer': str (verdade fundamental, opcional mas recomendado)
    """
    return raw_data.map(lambda x: {
        'prompt': [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': x['question']}
        ],
        'answer': extract_answer(x['raw_answer'])
    })
```

**Dicas Profissionais:**
- Use exemplos one-shot ou few-shot no prompt de sistema para formatos complexos
- Mantenha prompts concisos (max_prompt_length: 256-512 tokens)
- Valide qualidade de dados antes do treinamento (lixo dentro = lixo fora)

### Passo 2: Implementação de Função de Recompensa

**Estrutura de Template:**
```python
def reward_function_name(
    prompts,        # List[List[Dict]]: Prompts originais
    completions,    # List[List[Dict]]: Gerações do modelo
    answer=None,    # Opcional: Verdade fundamental do dataset
    **kwargs        # Colunas adicionais do dataset
) -> list[float]:
    """
    Avalia conclusões e retorna recompensas.

    Retorna: Lista de floats (um por conclusão)
    """
    # Extrai texto de conclusão
    responses = [comp[0]['content'] for comp in completions]

    # Calcula recompensas
    rewards = []
    for response in responses:
        score = compute_score(response)
        rewards.append(score)

    return rewards
```

**Exemplo 1: Recompensa de Correção (Matemática/Coding)**
```python
def correctness_reward(prompts, completions, answer, **kwargs):
    """Recompensa respostas corretas com score alto."""
    responses = [comp[0]['content'] for comp in completions]
    extracted = [extract_final_answer(r) for r in responses]
    return [2.0 if ans == gt else 0.0
            for ans, gt in zip(extracted, answer)]
```

**Exemplo 2: Recompensa de Formato (Saída Estruturada)**
```python
import re

def format_reward(completions, **kwargs):
    """Recompensa formato estruturado tipo XML."""
    pattern = r'<reasoning>.*?</reasoning>\s*<answer>.*?</answer>'
    responses = [comp[0]['content'] for comp in completions]
    return [1.0 if re.search(pattern, r, re.DOTALL) else 0.0
            for r in responses]
```

**Exemplo 3: Recompensa de Formato Incremental (Crédito Parcial)**
```python
def incremental_format_reward(completions, **kwargs):
    """Concede crédito parcial para conformidade de formato."""
    responses = [comp[0]['content'] for comp in completions]
    rewards = []

    for r in responses:
        score = 0.0
        if '<reasoning>' in r:
            score += 0.25
        if '</reasoning>' in r:
            score += 0.25
        if '<answer>' in r:
            score += 0.25
        if '</answer>' in r:
            score += 0.25
        # Penaliza texto extra após tag de fechamento
        if r.count('</answer>') == 1:
            extra_text = r.split('</answer>')[-1].strip()
            score -= len(extra_text) * 0.001
        rewards.append(score)

    return rewards
```

**Insight Crítico:**
Combine 3-5 funções de recompensa para treinamento robusto. A ordem importa menos que a diversidade de sinais.

### Passo 3: Configuração de Treinamento

**Config Otimizada para Memória (GPU Pequena)**
```python
from trl import GRPOConfig

training_args = GRPOConfig(
    output_dir="outputs/grpo-model",

    # Taxa de aprendizado
    learning_rate=5e-6,          # Menor = mais estável
    adam_beta1=0.9,
    adam_beta2=0.99,
    weight_decay=0.1,
    warmup_ratio=0.1,
    lr_scheduler_type='cosine',

    # Configurações de batch
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,  # Batch efetivo = 4

    # Específico de GRPO
    num_generations=8,            # Tamanho do grupo: 8-16 recomendado
    max_prompt_length=256,
    max_completion_length=512,

    # Duração do treinamento
    num_train_epochs=1,
    max_steps=None,               # Ou defina passos fixos (ex: 500)

    # Otimização
    bf16=True,                    # Mais rápido em A100/H100
    optim="adamw_8bit",          # Otimizador eficiente em memória
    max_grad_norm=0.1,

    # Logging
    logging_steps=1,
    save_steps=100,
    report_to="wandb",            # Ou "none" para sem logging
)
```

**Config de Alto Desempenho (GPU Grande)**
```python
training_args = GRPOConfig(
    output_dir="outputs/grpo-model",
    learning_rate=1e-5,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    num_generations=16,           # Grupos maiores = sinal melhor
    max_prompt_length=512,
    max_completion_length=1024,
    num_train_epochs=1,
    bf16=True,
    use_vllm=True,                # Geração rápida com vLLM
    logging_steps=10,
)
```

**Hiperparâmetros Críticos:**

| Parâmetro | Impacto | Dica de Ajuste |
|-----------|--------|----------------|
| `num_generations` | Tamanho do grupo para comparação | Comece com 8, aumente para 16 se GPU permitir |
| `learning_rate` | Velocidade de convergência/estabilidade | 5e-6 (seguro), 1e-5 (mais rápido, arriscado) |
| `max_completion_length` | Verbosidade de saída | Corresponda sua tarefa (512 para raciocínio, 256 para respostas curtas) |
| `gradient_accumulation_steps` | Tamanho de batch efetivo | Aumente se memória de GPU limitada |

### Passo 4: Setup de Modelo e Treinamento

**Setup Padrão (Transformers)**
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig
from trl import GRPOTrainer

# Carrega modelo
model_name = "Qwen/Qwen2.5-1.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",  # 2-3x mais rápido
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# Opcional: LoRA para treinamento eficiente em parâmetros
peft_config = LoraConfig(
    r=16,                         # Rank (maior = mais capacidade)
    lora_alpha=32,               # Fator de escala (tipicamente 2*r)
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    task_type="CAUSAL_LM",
    lora_dropout=0.05,
)

# Inicializa trainer
trainer = GRPOTrainer(
    model=model,
    processing_class=tokenizer,
    reward_funcs=[
        incremental_format_reward,
        format_reward,
        correctness_reward,
    ],
    args=training_args,
    train_dataset=dataset,
    peft_config=peft_config,      # Remova para ajuste fino completo
)

# Treina
trainer.train()

# Salva
trainer.save_model("final_model")
```

**Setup Unsloth (2-3x Mais Rápido)**
```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="google/gemma-3-1b-it",
    max_seq_length=1024,
    load_in_4bit=True,
    fast_inference=True,
    max_lora_rank=32,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=32,
    use_gradient_checkpointing="unsloth",
)

# O resto é idêntico ao setup padrão
trainer = GRPOTrainer(model=model, ...)
trainer.train()
```

---

## Insights Críticos de Treinamento

### 1. Comportamento de Loss (PADRÃO ESPERADO)
- **Loss começa perto de 0 e AUMENTA durante treinamento**
- Isto é CORRETO - loss mede divergência KL da política inicial
- O modelo está aprendendo (divergindo do comportamento original para otimizar recompensas)
- Monitore métricas de recompensa em vez de loss para acompanhar progresso

### 2. Rastreamento de Recompensa
Métricas principais a acompanhar:
- `reward`: Média em todas as conclusões
- `reward_std`: Diversidade dentro de grupos (deve permanecer > 0)
- `kl`: Divergência KL de referência (deve crescer moderadamente)

**Padrão de Treinamento Saudável:**
```
Passo   Recompensa    Recompensa_Std   KL
100    0.5       0.3          0.02
200    0.8       0.25         0.05
300    1.2       0.2          0.08  ← Progressão boa
400    1.5       0.15         0.12
```

**Sinais de Aviso:**
- Recompensa std → 0 (modelo colapsando para resposta única)
- KL explodindo (> 0.5) (divergindo muito, reduza LR)
- Recompensa presa (funções de recompensa muito rigorosas ou problema de capacidade do modelo)

### 3. Armadilhas Comuns e Soluções

| Problema | Sintoma | Solução |
|---------|---------|----------|
| **Colapso de modo** | Todas as conclusões idênticas | Aumente `num_generations`, adicione penalidade de diversidade |
| **Sem aprendizado** | Recompensas planas | Verifique lógica de função de recompensa, aumente LR |
| **Erros OOM** | Memória de GPU excedida | Reduza `num_generations`, ative gradient checkpointing |
| **Treinamento lento** | < 1 it/s | Ative `use_vllm=True`, use Unsloth, reduza tamanho de seq |
| **Formato ignorado** | Modelo não segue estrutura | Aumente peso de recompensa de formato, adicione recompensas incrementais |

---

## Padrões Avançados

### 1. Treinamento em Multi-Estágios
Para tarefas complexas, treine em estágios:

```python
# Estágio 1: Conformidade de formato (epochs=1)
trainer_stage1 = GRPOTrainer(
    model=model,
    reward_funcs=[incremental_format_reward, format_reward],
    ...
)
trainer_stage1.train()

# Estágio 2: Correção (epochs=1)
trainer_stage2 = GRPOTrainer(
    model=model,
    reward_funcs=[format_reward, correctness_reward],
    ...
)
trainer_stage2.train()
```

### 2. Dimensionamento Adaptativo de Recompensa
```python
class AdaptiveReward:
    def __init__(self, base_reward_func, initial_weight=1.0):
        self.func = base_reward_func
        self.weight = initial_weight

    def __call__(self, *args, **kwargs):
        rewards = self.func(*args, **kwargs)
        return [r * self.weight for r in rewards]

    def adjust_weight(self, success_rate):
        """Aumenta peso se modelo com dificuldade, diminui se sucessos."""
        if success_rate < 0.3:
            self.weight *= 1.2
        elif success_rate > 0.8:
            self.weight *= 0.9
```

### 3. Integração Customizada de Dataset
```python
def load_custom_knowledge_base(csv_path):
    """Exemplo: Docs de plataforma de comunicação escolar."""
    import pandas as pd
    df = pd.read_csv(csv_path)

    dataset = Dataset.from_pandas(df).map(lambda x: {
        'prompt': [
            {'role': 'system', 'content': CUSTOM_SYSTEM_PROMPT},
            {'role': 'user', 'content': x['question']}
        ],
        'answer': x['expert_answer']
    })
    return dataset
```

---

## Deployment e Inference

### Salvar e Mesclar LoRA
```python
# Mescla adaptadores LoRA no modelo base
if hasattr(trainer.model, 'merge_and_unload'):
    merged_model = trainer.model.merge_and_unload()
    merged_model.save_pretrained("production_model")
    tokenizer.save_pretrained("production_model")
```

### Exemplo de Inference
```python
from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="production_model",
    tokenizer=tokenizer
)

result = generator(
    [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': "Quanto é 15 + 27?"}
    ],
    max_new_tokens=256,
    do_sample=True,
    temperature=0.7,
    top_p=0.9
)
print(result[0]['generated_text'])
```

---

## Checklist de Melhores Práticas

**Antes do Treinamento:**
- [ ] Valide formato de dataset (prompts como List[Dict])
- [ ] Teste funções de recompensa em dados de amostra
- [ ] Calcule max_prompt_length esperado dos dados
- [ ] Escolha num_generations apropriado baseado em memória de GPU
- [ ] Configure logging (wandb recomendado)

**Durante o Treinamento:**
- [ ] Monitore progressão de recompensa (deve aumentar)
- [ ] Verifique reward_std (deve permanecer > 0.1)
- [ ] Observe erros de OOM (reduza batch size se necessário)
- [ ] Amostre gerações a cada 50-100 passos
- [ ] Valide conformidade de formato em conjunto de retenção

**Após o Treinamento:**
- [ ] Mescle pesos de LoRA se usando PEFT
- [ ] Teste em prompts diversos
- [ ] Compare ao modelo baseline
- [ ] Documente pesos de recompensa e hiperparâmetros
- [ ] Salve config de reprodutibilidade

---

## Guia de Troubleshooting

### Workflow de Debug
1. **Isole funções de recompensa** - Teste cada uma independentemente
2. **Verifique distribuição de dados** - Garanta diversidade em prompts
3. **Reduza complexidade** - Comece com recompensa única, adicione gradualmente
4. **Monitore gerações** - Imprima amostras a cada N passos
5. **Valide lógica de extração** - Garanta que parsing de resposta funciona

### Correções Rápidas
```python
# Debug de função de recompensa
def debug_reward(completions, **kwargs):
    responses = [comp[0]['content'] for comp in completions]
    for i, r in enumerate(responses[:2]):  # Imprime as 2 primeiras
        print(f"Resposta {i}: {r[:200]}...")
    return [1.0] * len(responses)  # Recompensas dummy

# Teste sem treinamento
trainer = GRPOTrainer(..., reward_funcs=[debug_reward])
trainer.generate_completions(dataset[:1])  # Gera sem atualizar
```

---

## Referências e Recursos

**Documentação Oficial:**
- TRL GRPO Trainer: https://huggingface.co/docs/trl/grpo_trainer
- Artigo DeepSeek R1: https://arxiv.org/abs/2501.12948
- Docs Unsloth: https://docs.unsloth.ai/

**Repositórios de Exemplo:**
- Implementação Open R1: https://github.com/huggingface/open-r1
- Exemplos TRL: https://github.com/huggingface/trl/tree/main/examples

**Leitura Recomendada:**
- Padrão de Progressive Disclosure para instruções de agent
- Reward shaping em RL (Ng et al.)
- Artigo LoRA (Hu et al., 2021)

---

## Instruções de Uso para Agents

Quando esta skill é carregada:

1. **Leia este arquivo inteiro** antes de implementar treinamento GRPO
2. **Comece com a função de recompensa mais simples** (ex: baseada em comprimento) para validar setup
3. **Use os templates** no diretório `templates/` como pontos de partida
4. **Referencie exemplos** em `examples/` para implementações específicas de tarefa
5. **Siga o workflow** sequencialmente (não pule passos)
6. **Debugue incrementalmente** - adicione uma função de recompensa por vez

**Lembretes Críticos:**
- Sempre use múltiplas funções de recompensa (3-5 é ótimo)
- Monitore métricas de recompensa, não loss
- Teste funções de recompensa antes do treinamento
- Comece pequeno (num_generations=4), dimensione gradualmente
- Salve checkpoints frequentemente (a cada 100 passos)

Esta skill é projetada para **implementação em nível especializado**. Iniciantes devem começar com ajuste fino supervisionado antes de tentar GRPO.