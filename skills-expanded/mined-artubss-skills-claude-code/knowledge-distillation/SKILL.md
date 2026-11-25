---
name: knowledge-distillation
description: Comprima modelos de linguagem grandes usando destilação de conhecimento de modelos professor para aluno. Use ao implantar modelos menores com desempenho retido, transferir capacidades do GPT-4 para modelos de código aberto ou reduzir custos de inferência. Aborda escalamento de temperatura, alvos suaves, KLD reversa, destilação de logits e estratégias de treinamento MiniLLM.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Emerging Techniques, Knowledge Distillation, Model Compression, Teacher-Student, MiniLLM, Reverse KLD, Soft Targets, Temperature Scaling, Logit Distillation, Model Transfer]
dependencies: [transformers, torch, datasets]
---

# Destilação de Conhecimento: Comprimindo LLMs

## Quando Usar Esta Skill

Use Destilação de Conhecimento quando você precisa:
- **Comprimir modelos** de 70B → 7B retendo 90%+ de desempenho
- **Transferir capacidades** de modelos proprietários (GPT-4) para código aberto (LLaMA, Mistral)
- **Reduzir custos de inferência** implantando modelos alunos menores
- **Criar modelos especializados** destilando conhecimento específico de domínio
- **Melhorar modelos pequenos** usando dados sintéticos de professores grandes

**Técnicas-chave**: Escalamento de temperatura, alvos suaves, KLD reversa (MiniLLM), destilação de logits, destilação de resposta

**Papers**: Hinton et al. 2015 (arXiv 1503.02531), MiniLLM (arXiv 2306.08543), KD Survey (arXiv 2402.13116)

## Instalação

```bash
# transformers padrão
pip install transformers datasets accelerate

# Para treinamento
pip install torch deepspeed wandb

# Opcional: implementação MiniLLM
git clone https://github.com/microsoft/LMOps
cd LMOps/minillm
pip install -e .
```

## Início Rápido

### Destilação de Conhecimento Básica

```python
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

# 1. Carregue modelos professor (grande) e aluno (pequeno)
teacher = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-70b-hf",  # Professor grande
    torch_dtype=torch.float16,
    device_map="auto"
)

student = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",  # Aluno pequeno
    torch_dtype=torch.float16,
    device_map="cuda:0"
)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-70b-hf")

# 2. Defina perda de destilação
def distillation_loss(student_logits, teacher_logits, labels, temperature=2.0, alpha=0.5):
    """
    Combine perda dura (cross-entropy) com perda suave (divergência KL).

    Args:
        temperature: Suaviza distribuições de probabilidade (maior = mais suave)
        alpha: Peso para perda de destilação (1-alpha para perda dura)
    """
    # Perda dura: Cross-entropy padrão com rótulos verdadeiros
    hard_loss = F.cross_entropy(student_logits.view(-1, student_logits.size(-1)), labels.view(-1))

    # Perda suave: Divergência KL entre aluno e professor
    soft_targets = F.softmax(teacher_logits / temperature, dim=-1)
    soft_student = F.log_softmax(student_logits / temperature, dim=-1)
    soft_loss = F.kl_div(soft_student, soft_targets, reduction='batchmean') * (temperature ** 2)

    # Perda combinada
    return alpha * soft_loss + (1 - alpha) * hard_loss

# 3. Loop de treinamento
for batch in dataloader:
    # Forward do professor (sem grad)
    with torch.no_grad():
        teacher_outputs = teacher(**batch)
        teacher_logits = teacher_outputs.logits

    # Forward do aluno
    student_outputs = student(**batch)
    student_logits = student_outputs.logits

    # Compute perda de destilação
    loss = distillation_loss(
        student_logits,
        teacher_logits,
        batch['labels'],
        temperature=2.0,
        alpha=0.7  # 70% suave, 30% dura
    )

    # Backward e otimize
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
```

### MiniLLM (KLD Reversa)

**Fonte**: arXiv 2306.08543 (2024)

**Inovação**: Use KLD reversa em vez de KLD direta para melhor destilação de modelos generativos.

```python
def reverse_kl_loss(student_logits, teacher_logits, temperature=1.0):
    """
    Divergência KL reversa: KL(Professor || Aluno)
    Melhor para modelos generativos que KLD direta.
    """
    # Distribuição do professor (alvo)
    p_teacher = F.softmax(teacher_logits / temperature, dim=-1)

    # Distribuição do aluno (modelo)
    log_p_student = F.log_softmax(student_logits / temperature, dim=-1)

    # KL reversa: Soma sobre professor, aluno aprende a cobrir modos do professor
    reverse_kl = -(p_teacher * log_p_student).sum(dim=-1).mean()

    return reverse_kl * (temperature ** 2)

# Treinamento com MiniLLM
for batch in dataloader:
    with torch.no_grad():
        teacher_logits = teacher(**batch).logits

    student_logits = student(**batch).logits

    # KLD reversa (melhor para geração)
    loss = reverse_kl_loss(student_logits, teacher_logits, temperature=1.0)

    loss.backward()
    optimizer.step()
```

**Por que KL reversa?**
- **KL direta** (padrão): Aluno aprende a corresponder à *média* do professor
- **KL reversa** (MiniLLM): Aluno aprende a *cobrir* todos os modos do professor
- Melhor para geração diversa de texto

### Destilação de Resposta

```python
# Gere dados sintéticos do professor, treine aluno para imitá-lo

# 1. Gere respostas sintéticas do professor
prompts = ["Explique IA:", "O que é ML?", "Defina PLN:"]

teacher_responses = []
for prompt in prompts:
    inputs = tokenizer(prompt, return_tensors='pt').to(teacher.device)
    outputs = teacher.generate(**inputs, max_new_tokens=256, do_sample=True, temperature=0.7)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    teacher_responses.append(response)

# 2. Treine aluno nas respostas do professor (fine-tuning padrão)
train_dataset = [
    {"text": f"{prompt}\n{response}"}
    for prompt, response in zip(prompts, teacher_responses)
]

# 3. Fine-tune do aluno
trainer = Trainer(
    model=student,
    args=TrainingArguments(output_dir="./student", num_train_epochs=3, learning_rate=2e-5),
    train_dataset=train_dataset,
)
trainer.train()
```

## Conceitos Fundamentais

### 1. Escalamento de Temperatura

**Objetivo**: Suavizar distribuições de probabilidade para expor incerteza do professor.

```python
# Temperatura baixa (T=1): Distribuição pontuda
logits = [3.0, 2.0, 1.0]
probs_T1 = softmax(logits / 1.0)  # [0.67, 0.24, 0.09]

# Temperatura alta (T=4): Distribuição suave
probs_T4 = softmax(logits / 4.0)  # [0.42, 0.34, 0.24]

# T maior revela mais informações sobre rankings relativos
```

**Regra**: Use T=2-5 para destilação (2 é padrão comum).

### 2. Componentes da Função de Perda

```python
# Perda total = alpha * perda_suave + (1 - alpha) * perda_dura

# Perda suave: Aprenda do conhecimento do professor
soft_loss = KL(aluno || professor)

# Perda dura: Aprenda dos rótulos verdadeiros
hard_loss = CrossEntropy(saída_aluno, rótulos_verdadeiros)

# Valores típicos:
alpha = 0.5  # Balanceado
alpha = 0.7  # Mais ênfase no professor
alpha = 0.3  # Mais ênfase nos rótulos
```

### 3. KLD Direta vs Reversa

```python
# KL direta: KL(Aluno || Professor)
# - Aluno corresponde ao comportamento médio do professor
# - Mode-seeking: Aluno foca nos modos de maior probabilidade do professor
# - Bom para classificação

# KL reversa: KL(Professor || Aluno)
# - Aluno cobre todos os comportamentos do professor
# - Mode-covering: Aluno aprende comportamentos diversos
# - Bom para geração (MiniLLM)
```

## Estratégias de Treinamento

### Estratégia 1: Destilação de Logits

```python
# Treine aluno para corresponder aos logits do professor diretamente

def logit_distillation_trainer(student, teacher, dataloader, temperature=2.0):
    optimizer = torch.optim.AdamW(student.parameters(), lr=2e-5)

    for epoch in range(3):
        for batch in dataloader:
            # Obtenha logits
            with torch.no_grad():
                teacher_logits = teacher(**batch).logits

            student_logits = student(**batch).logits

            # MSE em logits (alternativa a KLD)
            loss = F.mse_loss(student_logits, teacher_logits)

            # Ou use KLD
            # loss = F.kl_div(
            #     F.log_softmax(student_logits/temperature, dim=-1),
            #     F.softmax(teacher_logits/temperature, dim=-1),
            #     reduction='batchmean'
            # ) * (temperature ** 2)

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

    return student
```

### Estratégia 2: Destilação em Duas Etapas

```python
# Etapa 1: Destilar do professor
student = distill(teacher, student, epochs=5)

# Etapa 2: Fine-tune em dados específicos de tarefa
student = fine_tune(student, task_data, epochs=3)

# Resulta em melhor desempenho em tarefa que destilação de etapa única
```

### Estratégia 3: Destilação Multi-Professor

```python
# Aprenda de múltiplos professores especialistas

def multi_teacher_distillation(student, teachers, batch):
    """Destilar de conjunto de professores."""
    teacher_logits_list = []

    # Obtenha logits de todos os professores
    with torch.no_grad():
        for teacher in teachers:
            logits = teacher(**batch).logits
            teacher_logits_list.append(logits)

    # Média das predições do professor
    avg_teacher_logits = torch.stack(teacher_logits_list).mean(dim=0)

    # Aluno aprende do conjunto
    student_logits = student(**batch).logits
    loss = F.kl_div(
        F.log_softmax(student_logits, dim=-1),
        F.softmax(avg_teacher_logits, dim=-1),
        reduction='batchmean'
    )

    return loss
```

## Implantação em Produção

### Script de Treinamento Completo

```python
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling

def train_distilled_model(
    teacher_name="meta-llama/Llama-2-70b-hf",
    student_name="meta-llama/Llama-2-7b-hf",
    output_dir="./distilled-llama-7b",
    temperature=2.0,
    alpha=0.7,
):
    # Carregue modelos
    teacher = AutoModelForCausalLM.from_pretrained(teacher_name, torch_dtype=torch.float16, device_map="auto")
    student = AutoModelForCausalLM.from_pretrained(student_name, torch_dtype=torch.float16)
    tokenizer = AutoTokenizer.from_pretrained(teacher_name)

    # Trainer customizado com destilação
    class DistillationTrainer(Trainer):
        def compute_loss(self, model, inputs, return_outputs=False):
            # Forward do aluno
            outputs_student = model(**inputs)
            student_logits = outputs_student.logits

            # Forward do professor (sem grad)
            with torch.no_grad():
                outputs_teacher = teacher(**inputs)
                teacher_logits = outputs_teacher.logits

            # Perda de destilação
            soft_targets = F.softmax(teacher_logits / temperature, dim=-1)
            soft_student = F.log_softmax(student_logits / temperature, dim=-1)
            soft_loss = F.kl_div(soft_student, soft_targets, reduction='batchmean') * (temperature ** 2)

            # Perda dura
            hard_loss = outputs_student.loss

            # Combinada
            loss = alpha * soft_loss + (1 - alpha) * hard_loss

            return (loss, outputs_student) if return_outputs else loss

    # Argumentos de treinamento
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=8,
        learning_rate=2e-5,
        warmup_steps=500,
        logging_steps=100,
        save_steps=1000,
        bf16=True,
        gradient_checkpointing=True,
    )

    # Treine
    trainer = DistillationTrainer(
        model=student,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    trainer.train()
    student.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

# Uso
train_distilled_model(
    teacher_name="meta-llama/Llama-2-70b-hf",
    student_name="meta-llama/Llama-2-7b-hf",
    temperature=2.0,
    alpha=0.7
)
```

## Melhores Práticas

### 1. Seleção de Hiperparâmetros

```python
# Temperatura
T = 1.0  # Pontuda (menos transferência de conhecimento)
T = 2.0  # Padrão (bom equilíbrio)
T = 5.0  # Suave (mais transferência de conhecimento)

# Alpha (peso)
alpha = 0.5  # Balanceado
alpha = 0.7  # Enfatizar conhecimento do professor
alpha = 0.9  # Destilação forte

# Regra: T maior + alpha maior = destilação mais forte
```

### 2. Razão de Tamanho de Modelo

```python
# Boas razões (professor/aluno)
70B / 7B = 10×    # Excelente
13B / 1B = 13×    # Bom
7B / 1B = 7×      # Aceitável

# Evite diferença muito grande
70B / 1B = 70×    # Muito grande, ineficaz
```

### 3. Qualidade dos Dados

```python
# Melhor: Use dados gerados pelo professor + dados reais
train_data = {
    "teacher_generated": 70%,  # Diverso, alta qualidade
    "real_data": 30%            # Verdade fundamental
}

# Evite: Apenas dados reais (não aproveita professor totalmente)
```

## Avaliação

```python
from transformers import pipeline

# Compare aluno vs professor
teacher_pipe = pipeline("text-generation", model=teacher)
student_pipe = pipeline("text-generation", model=student)

prompts = ["Explique computação quântica:", "O que é IA?"]

for prompt in prompts:
    teacher_out = teacher_pipe(prompt, max_new_tokens=100)
    student_out = student_pipe(prompt, max_new_tokens=100)

    print(f"Prompt: {prompt}")
    print(f"Professor: {teacher_out[0]['generated_text']}")
    print(f"Aluno: {student_out[0]['generated_text']}")
    print(f"Qualidade de correspondência: {calculate_similarity(teacher_out, student_out):.2f}")
```

## Recursos

- **Hinton et al. 2015 (Fundacional)**: https://arxiv.org/abs/1503.02531
- **MiniLLM (KLD Reversa)**: https://arxiv.org/abs/2306.08543
- **KD Survey para LLMs (2024)**: https://arxiv.org/abs/2402.13116
- **MiniLLM GitHub**: https://github.com/microsoft/LMOps/tree/main/minillm