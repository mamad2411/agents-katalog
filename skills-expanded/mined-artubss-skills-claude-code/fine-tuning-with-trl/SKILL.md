---
name: fine-tuning-with-trl
description: Ajuste fino de LLMs usando reinforcement learning com TRL - SFT para ajuste de instruções, DPO para alinhamento de preferências, PPO/GRPO para otimização de recompensas e treinamento de modelo de recompensas. Use quando precisar de RLHF, alinhar modelo com preferências ou treinar a partir de feedback humano. Funciona com HuggingFace Transformers.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Post-Training, TRL, Reinforcement Learning, Fine-Tuning, SFT, DPO, PPO, GRPO, RLHF, Preference Alignment, HuggingFace]
dependencies: [trl, transformers, datasets, peft, accelerate, torch]
---

# TRL - Transformer Reinforcement Learning

## Início rápido

TRL fornece métodos de pós-treinamento para alinhar modelos de linguagem com preferências humanas.

**Instalação**:
```bash
pip install trl transformers datasets peft accelerate
```

**Supervised Fine-Tuning** (ajuste de instruções):
```python
from trl import SFTTrainer

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset,  # Pares prompt-completamento
)
trainer.train()
```

**DPO** (alinhar com preferências):
```python
from trl import DPOTrainer, DPOConfig

config = DPOConfig(output_dir="model-dpo", beta=0.1)
trainer = DPOTrainer(
    model=model,
    args=config,
    train_dataset=preference_dataset,  # Pares escolhido/rejeitado
    processing_class=tokenizer
)
trainer.train()
```

## Fluxos de trabalho comuns

### Fluxo 1: Pipeline RLHF completo (SFT → Modelo de Recompensas → PPO)

Pipeline completo desde o modelo base até um modelo alinhado com humanos.

Copie esta lista de verificação:

```
Treinamento RLHF:
- [ ] Etapa 1: Supervised fine-tuning (SFT)
- [ ] Etapa 2: Treinar modelo de recompensas
- [ ] Etapa 3: Reinforcement learning com PPO
- [ ] Etapa 4: Avaliar modelo alinhado
```

**Etapa 1: Supervised fine-tuning**

Treine o modelo base em dados de seguimento de instruções:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

# Carregar modelo
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B")

# Carregar dataset de instruções
dataset = load_dataset("trl-lib/Capybara", split="train")

# Configurar treinamento
training_args = SFTConfig(
    output_dir="Qwen2.5-0.5B-SFT",
    per_device_train_batch_size=4,
    num_train_epochs=1,
    learning_rate=2e-5,
    logging_steps=10,
    save_strategy="epoch"
)

# Treinar
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer
)
trainer.train()
trainer.save_model()
```

**Etapa 2: Treinar modelo de recompensas**

Treine um modelo para prever preferências humanas:

```python
from transformers import AutoModelForSequenceClassification
from trl import RewardTrainer, RewardConfig

# Carregar modelo SFT como base
model = AutoModelForSequenceClassification.from_pretrained(
    "Qwen2.5-0.5B-SFT",
    num_labels=1  # Pontuação única de recompensa
)
tokenizer = AutoTokenizer.from_pretrained("Qwen2.5-0.5B-SFT")

# Carregar dados de preferência (pares escolhido/rejeitado)
dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")

# Configurar treinamento
training_args = RewardConfig(
    output_dir="Qwen2.5-0.5B-Reward",
    per_device_train_batch_size=2,
    num_train_epochs=1,
    learning_rate=1e-5
)

# Treinar modelo de recompensas
trainer = RewardTrainer(
    model=model,
    args=training_args,
    processing_class=tokenizer,
    train_dataset=dataset
)
trainer.train()
trainer.save_model()
```

**Etapa 3: Reinforcement learning com PPO**

Otimize a política usando o modelo de recompensas:

```bash
python -m trl.scripts.ppo \
    --model_name_or_path Qwen2.5-0.5B-SFT \
    --reward_model_path Qwen2.5-0.5B-Reward \
    --dataset_name trl-internal-testing/descriptiveness-sentiment-trl-style \
    --output_dir Qwen2.5-0.5B-PPO \
    --learning_rate 3e-6 \
    --per_device_train_batch_size 64 \
    --total_episodes 10000
```

**Etapa 4: Avaliar**

```python
from transformers import pipeline

# Carregar modelo alinhado
generator = pipeline("text-generation", model="Qwen2.5-0.5B-PPO")

# Testar
prompt = "Explique computação quântica para uma criança de 10 anos"
output = generator(prompt, max_length=200)[0]["generated_text"]
print(output)
```

### Fluxo 2: Alinhamento simples de preferências com DPO

Alinhe o modelo com preferências sem modelo de recompensas.

Copie esta lista de verificação:

```
Treinamento DPO:
- [ ] Etapa 1: Preparar dataset de preferências
- [ ] Etapa 2: Configurar DPO
- [ ] Etapa 3: Treinar com DPOTrainer
- [ ] Etapa 4: Avaliar alinhamento
```

**Etapa 1: Preparar dataset de preferências**

Formato do dataset:
```json
{
  "prompt": "Qual é a capital da França?",
  "chosen": "A capital da França é Paris.",
  "rejected": "Não sei."
}
```

Carregar dataset:
```python
from datasets import load_dataset

dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")
# Ou carregar seu próprio
# dataset = load_dataset("json", data_files="preferences.json")
```

**Etapa 2: Configurar DPO**

```python
from trl import DPOConfig

config = DPOConfig(
    output_dir="Qwen2.5-0.5B-DPO",
    per_device_train_batch_size=4,
    num_train_epochs=1,
    learning_rate=5e-7,
    beta=0.1,  # Força da penalidade KL
    max_prompt_length=512,
    max_length=1024,
    logging_steps=10
)
```

**Etapa 3: Treinar com DPOTrainer**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import DPOTrainer

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")

trainer = DPOTrainer(
    model=model,
    args=config,
    train_dataset=dataset,
    processing_class=tokenizer
)

trainer.train()
trainer.save_model()
```

**Alternativa CLI**:
```bash
trl dpo \
    --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
    --dataset_name argilla/Capybara-Preferences \
    --output_dir Qwen2.5-0.5B-DPO \
    --per_device_train_batch_size 4 \
    --learning_rate 5e-7 \
    --beta 0.1
```

### Fluxo 3: RL online com eficiência de memória usando GRPO

Treine com reinforcement learning usando memória mínima.

Copie esta lista de verificação:

```
Treinamento GRPO:
- [ ] Etapa 1: Definir função de recompensas
- [ ] Etapa 2: Configurar GRPO
- [ ] Etapa 3: Treinar com GRPOTrainer
```

**Etapa 1: Definir função de recompensas**

```python
def reward_function(completions, **kwargs):
    """
    Calcule recompensas para completamentos.

    Args:
        completions: Lista de textos gerados

    Returns:
        Lista de pontuações de recompensas (floats)
    """
    rewards = []
    for completion in completions:
        # Exemplo: recompensa baseada em comprimento e palavras únicas
        score = len(completion.split())  # Favoreça respostas mais longas
        score += len(set(completion.lower().split()))  # Recompense palavras únicas
        rewards.append(score)
    return rewards
```

Ou use um modelo de recompensas:
```python
from transformers import pipeline

reward_model = pipeline("text-classification", model="reward-model-path")

def reward_from_model(completions, prompts, **kwargs):
    # Combine prompt + completamento
    full_texts = [p + c for p, c in zip(prompts, completions)]
    # Obtenha pontuações de recompensas
    results = reward_model(full_texts)
    return [r["score"] for r in results]
```

**Etapa 2: Configurar GRPO**

```python
from trl import GRPOConfig

config = GRPOConfig(
    output_dir="Qwen2-GRPO",
    per_device_train_batch_size=4,
    num_train_epochs=1,
    learning_rate=1e-5,
    num_generations=4,  # Gere 4 completamentos por prompt
    max_new_tokens=128
)
```

**Etapa 3: Treinar com GRPOTrainer**

```python
from datasets import load_dataset
from trl import GRPOTrainer

# Carregar dataset apenas com prompts
dataset = load_dataset("trl-lib/tldr", split="train")

trainer = GRPOTrainer(
    model="Qwen/Qwen2-0.5B-Instruct",
    reward_funcs=reward_function,  # Sua função de recompensas
    args=config,
    train_dataset=dataset
)

trainer.train()
```

**CLI**:
```bash
trl grpo \
    --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
    --dataset_name trl-lib/tldr \
    --output_dir Qwen2-GRPO \
    --num_generations 4
```

## Quando usar vs alternativas

**Use TRL quando:**
- Precisar alinhar o modelo com preferências humanas
- Tiver dados de preferência (pares escolhido/rejeitado)
- Quiser usar reinforcement learning (PPO, GRPO)
- Precisar treinar modelo de recompensas
- Estiver fazendo RLHF (pipeline completo)

**Seleção de método**:
- **SFT**: Ter pares prompt-completamento, deseja seguimento básico de instruções
- **DPO**: Ter preferências, deseja alinhamento simples (sem modelo de recompensas)
- **PPO**: Ter modelo de recompensas, precisa de máximo controle sobre RL
- **GRPO**: Memória limitada, deseja RL online
- **Modelo de Recompensas**: Construir pipeline RLHF, precisa pontuar gerações

**Use alternativas em vez disso:**
- **HuggingFace Trainer**: Ajuste fino básico sem RL
- **Axolotl**: Configuração de treinamento baseada em YAML
- **LitGPT**: Educacional, ajuste fino mínimo
- **Unsloth**: Treinamento LoRA rápido

## Problemas comuns

**Problema: OOM durante treinamento DPO**

Reduza o tamanho do batch e comprimento da sequência:
```python
config = DPOConfig(
    per_device_train_batch_size=1,  # Reduza de 4
    max_length=512,  # Reduza de 1024
    gradient_accumulation_steps=8  # Mantenha batch efetivo
)
```

Ou use gradient checkpointing:
```python
model.gradient_checkpointing_enable()
```

**Problema: Qualidade de alinhamento ruim**

Ajuste o parâmetro beta:
```python
# Beta mais alto = mais conservador (fica mais próximo da referência)
config = DPOConfig(beta=0.5)  # Padrão 0.1

# Beta mais baixo = alinhamento mais agressivo
config = DPOConfig(beta=0.01)
```

**Problema: Modelo de recompensas não aprendendo**

Verifique tipo de loss e taxa de aprendizado:
```python
config = RewardConfig(
    learning_rate=1e-5,  # Tente taxa de aprendizado diferente
    num_train_epochs=3  # Treine por mais tempo
)
```

Garanta que o dataset de preferências tenha vencedores claros:
```python
# Verifique dataset
print(dataset[0])
# Deve ter escolhido > rejeitado claramente
```

**Problema: Treinamento PPO instável**

Ajuste o coeficiente KL:
```python
config = PPOConfig(
    kl_coef=0.1,  # Aumente de 0.05
    cliprange=0.1  # Reduza de 0.2
)
```

## Tópicos avançados

**Guia de treinamento SFT**: Veja [references/sft-training.md](references/sft-training.md) para formatos de dataset, templates de chat, estratégias de packing e treinamento multi-GPU.

**Variantes DPO**: Veja [references/dpo-variants.md](references/dpo-variants.md) para IPO, cDPO, RPO e outras funções de loss DPO com hiperparâmetros recomendados.

**Modelagem de recompensas**: Veja [references/reward-modeling.md](references/reward-modeling.md) para recompensas de resultado vs processo, loss Bradley-Terry e avaliação de modelo de recompensas.

**Métodos RL online**: Veja [references/online-rl.md](references/online-rl.md) para PPO, GRPO, RLOO e OnlineDPO com configurações detalhadas.

## Requisitos de hardware

- **GPU**: NVIDIA (CUDA obrigatório)
- **VRAM**: Depende do modelo e método
  - SFT 7B: 16GB (com LoRA)
  - DPO 7B: 24GB (armazena modelo de referência)
  - PPO 7B: 40GB (política + modelo de recompensas)
  - GRPO 7B: 24GB (mais eficiente em memória)
- **Multi-GPU**: Suportado via `accelerate`
- **Precisão mista**: BF16 recomendado (A100/H100)

**Otimização de memória**:
- Use LoRA/QLoRA para todos os métodos
- Ative gradient checkpointing
- Use tamanhos de batch menores com acumulação de gradientes

## Recursos

- Documentação: https://huggingface.co/docs/trl/
- GitHub: https://github.com/huggingface/trl
- Papers:
  - "Training language models to follow instructions with human feedback" (InstructGPT, 2022)
  - "Direct Preference Optimization: Your Language Model is Secretly a Reward Model" (DPO, 2023)
  - "Group Relative Policy Optimization" (GRPO, 2024)
- Exemplos: https://github.com/huggingface/trl/tree/main/examples/scripts