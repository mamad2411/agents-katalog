---
name: transformers
description: Esta skill deve ser usada ao trabalhar com modelos transformer pré-treinados para processamento de linguagem natural, visão computacional, áudio ou tarefas multimodais. Use para geração de texto, classificação, resposta a perguntas, tradução, sumarização, classificação de imagens, detecção de objetos, reconhecimento de fala e fine-tuning de modelos em datasets personalizados.
---

# Transformers

## Visão Geral

A biblioteca Transformers do Hugging Face fornece acesso a milhares de modelos pré-treinados para tarefas em NLP, visão computacional, áudio e domínios multimodais. Use esta skill para carregar modelos, realizar inferência e fazer fine-tuning em dados personalizados.

## Instalação

Instale transformers e dependências principais:

```bash
uv pip install torch transformers datasets evaluate accelerate
```

Para tarefas de visão, adicione:
```bash
uv pip install timm pillow
```

Para tarefas de áudio, adicione:
```bash
uv pip install librosa soundfile
```

## Autenticação

Muitos modelos no Hugging Face Hub requerem autenticação. Configure o acesso:

```python
from huggingface_hub import login
login()  # Siga os prompts para inserir seu token
```

Ou configure variável de ambiente:
```bash
export HUGGINGFACE_TOKEN="your_token_here"
```

Obtenha tokens em: https://huggingface.co/settings/tokens

## Início Rápido

Use a Pipeline API para inferência rápida sem configuração manual:

```python
from transformers import pipeline

# Text generation
generator = pipeline("text-generation", model="gpt2")
result = generator("The future of AI is", max_length=50)

# Text classification
classifier = pipeline("text-classification")
result = classifier("This movie was excellent!")

# Question answering
qa = pipeline("question-answering")
result = qa(question="What is AI?", context="AI is artificial intelligence...")
```

## Capacidades Principais

### 1. Pipelines para Inferência Rápida

Use para inferência simples e otimizada em muitas tarefas. Suporta geração de texto, classificação, NER, resposta a perguntas, sumarização, tradução, classificação de imagens, detecção de objetos, classificação de áudio e muito mais.

**Quando usar**: Prototipagem rápida, tarefas simples de inferência, sem necessidade de pré-processamento personalizado.

Veja `references/pipelines.md` para cobertura abrangente de tarefas e otimizações.

### 2. Carregamento e Gerenciamento de Modelos

Carregue modelos pré-treinados com controle refinado sobre configuração, posicionamento de dispositivos e precisão.

**Quando usar**: Inicialização personalizada de modelos, gerenciamento avançado de dispositivos, inspeção de modelos.

Veja `references/models.md` para padrões de carregamento e boas práticas.

### 3. Geração de Texto

Gere texto com LLMs usando diversas estratégias de decodificação (greedy, beam search, sampling) e parâmetros de controle (temperature, top-k, top-p).

**Quando usar**: Geração criativa de texto, geração de código, IA conversacional, conclusão de texto.

Veja `references/generation.md` para estratégias de geração e parâmetros.

### 4. Treinamento e Fine-Tuning

Faça fine-tuning de modelos pré-treinados em datasets personalizados usando a Trainer API com precisão mista automática, treinamento distribuído e logging.

**Quando usar**: Adaptação de modelo específica para tarefas, adaptação de domínio, melhoria de desempenho do modelo.

Veja `references/training.md` para workflows de treinamento e boas práticas.

### 5. Tokenização

Converta texto em tokens e IDs de token para entrada do modelo, com padding, truncação e tratamento de tokens especiais.

**Quando usar**: Pipelines de pré-processamento personalizados, compreensão de entradas de modelo, processamento em lote.

Veja `references/tokenizers.md` para detalhes de tokenização.

## Padrões Comuns

### Padrão 1: Inferência Simples
Para tarefas diretas, use pipelines:
```python
pipe = pipeline("task-name", model="model-id")
output = pipe(input_data)
```

### Padrão 2: Uso Personalizado de Modelo
Para controle avançado, carregue modelo e tokenizer separadamente:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("model-id")
model = AutoModelForCausalLM.from_pretrained("model-id", device_map="auto")

inputs = tokenizer("text", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=100)
result = tokenizer.decode(outputs[0])
```

### Padrão 3: Fine-Tuning
Para adaptação de tarefas, use Trainer:
```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

trainer.train()
```

## Documentação de Referência

Para informações detalhadas sobre componentes específicos:
- **Pipelines**: `references/pipelines.md` - Todas as tarefas suportadas e otimizações
- **Models**: `references/models.md` - Carregamento, salvamento e configuração
- **Generation**: `references/generation.md` - Estratégias de geração de texto e parâmetros
- **Training**: `references/training.md` - Fine-tuning com Trainer API
- **Tokenizers**: `references/tokenizers.md` - Tokenização e pré-processamento