---
name: dspy
description: Construa sistemas de IA complexos com programação declarativa, otimize prompts automaticamente, crie sistemas RAG modulares e agentes com DSPy - framework de Programação Sistemática de Modelos de Linguagem da Stanford NLP
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Engenharia de Prompts, DSPy, Programação Declarativa, RAG, Agentes, Otimização de Prompts, Programação de LM, Stanford NLP, Otimização Automática, IA Modular]
dependencies: [dspy, openai, anthropic]
---

# DSPy: Programação Declarativa de Modelos de Linguagem

## Quando Usar Esta Skill

Use DSPy quando você precisar:
- **Construir sistemas de IA complexos** com múltiplos componentes e workflows
- **Programar LMs declarativamente** em vez de engenharia manual de prompts
- **Otimizar prompts automaticamente** usando métodos orientados por dados
- **Criar pipelines de IA modulares** que sejam mantíveis e portáveis
- **Melhorar sistematicamente** saídas de modelos com otimizadores
- **Construir sistemas RAG, agentes ou classificadores** com melhor confiabilidade

**GitHub Stars**: 22.000+ | **Criado Por**: Stanford NLP

## Instalação

```bash
# Versão estável
pip install dspy

# Versão mais recente de desenvolvimento
pip install git+https://github.com/stanfordnlp/dspy.git

# Com provedores de LM específicos
pip install dspy[openai]        # OpenAI
pip install dspy[anthropic]     # Anthropic Claude
pip install dspy[all]           # Todos os provedores
```

## Início Rápido

### Exemplo Básico: Resposta a Perguntas

```python
import dspy

# Configure seu modelo de linguagem
lm = dspy.Claude(model="claude-sonnet-4-5-20250929")
dspy.settings.configure(lm=lm)

# Defina uma signature (entrada → saída)
class QA(dspy.Signature):
    """Responda perguntas com respostas factuais breves."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="frequentemente entre 1 e 5 palavras")

# Crie um módulo
qa = dspy.Predict(QA)

# Use-o
response = qa(question="Qual é a capital da França?")
print(response.answer)  # "Paris"
```

### Raciocínio com Cadeia de Pensamento

```python
import dspy

lm = dspy.Claude(model="claude-sonnet-4-5-20250929")
dspy.settings.configure(lm=lm)

# Use ChainOfThought para melhor raciocínio
class MathProblem(dspy.Signature):
    """Resolva problemas matemáticos em linguagem natural."""
    problem = dspy.InputField()
    answer = dspy.OutputField(desc="resposta numérica")

# ChainOfThought gera passos de raciocínio automaticamente
cot = dspy.ChainOfThought(MathProblem)

response = cot(problem="Se João tem 5 maçãs e dá 2 para Maria, quantas ele tem?")
print(response.rationale)  # Mostra passos de raciocínio
print(response.answer)     # "3"
```

## Conceitos Principais

### 1. Signatures

Signatures definem a estrutura da sua tarefa de IA (entradas → saídas):

```python
# Signature inline (simples)
qa = dspy.Predict("question -> answer")

# Signature de classe (detalhada)
class Summarize(dspy.Signature):
    """Resuma texto em pontos-chave."""
    text = dspy.InputField()
    summary = dspy.OutputField(desc="pontos em bullet, 3-5 itens")

summarizer = dspy.ChainOfThought(Summarize)
```

**Quando usar cada:**
- **Inline**: Prototipagem rápida, tarefas simples
- **Classe**: Tarefas complexas, type hints, melhor documentação

### 2. Módulos

Módulos são componentes reutilizáveis que transformam entradas em saídas:

#### dspy.Predict
Módulo de predição básico:

```python
predictor = dspy.Predict("context, question -> answer")
result = predictor(context="Paris é a capital da França",
                   question="Qual é a capital?")
```

#### dspy.ChainOfThought
Gera passos de raciocínio antes de responder:

```python
cot = dspy.ChainOfThought("question -> answer")
result = cot(question="Por que o céu é azul?")
print(result.rationale)  # Passos de raciocínio
print(result.answer)     # Resposta final
```

#### dspy.ReAct
Raciocínio tipo agente com ferramentas:

```python
from dspy.predict import ReAct

class SearchQA(dspy.Signature):
    """Responda perguntas usando busca."""
    question = dspy.InputField()
    answer = dspy.OutputField()

def search_tool(query: str) -> str:
    """Busque na Wikipédia."""
    # Sua implementação de busca
    return results

react = ReAct(SearchQA, tools=[search_tool])
result = react(question="Quando Python foi criado?")
```

#### dspy.ProgramOfThought
Gera e executa código para raciocínio:

```python
pot = dspy.ProgramOfThought("question -> answer")
result = pot(question="Quanto é 15% de 240?")
# Gera: answer = 240 * 0.15
```

### 3. Otimizadores

Otimizadores melhoram seus módulos automaticamente usando dados de treinamento:

#### BootstrapFewShot
Aprende a partir de exemplos:

```python
from dspy.teleprompt import BootstrapFewShot

# Dados de treinamento
trainset = [
    dspy.Example(question="Quanto é 2+2?", answer="4").with_inputs("question"),
    dspy.Example(question="Quanto é 3+5?", answer="8").with_inputs("question"),
]

# Defina métrica
def validate_answer(example, pred, trace=None):
    return example.answer == pred.answer

# Otimize
optimizer = BootstrapFewShot(metric=validate_answer, max_bootstrapped_demos=3)
optimized_qa = optimizer.compile(qa, trainset=trainset)

# Agora optimized_qa funciona melhor!
```

#### MIPRO (Most Important Prompt Optimization)
Melhora iterativamente prompts:

```python
from dspy.teleprompt import MIPRO

optimizer = MIPRO(
    metric=validate_answer,
    num_candidates=10,
    init_temperature=1.0
)

optimized_cot = optimizer.compile(
    cot,
    trainset=trainset,
    num_trials=100
)
```

#### BootstrapFinetune
Cria datasets para fine-tuning de modelos:

```python
from dspy.teleprompt import BootstrapFinetune

optimizer = BootstrapFinetune(metric=validate_answer)
optimized_module = optimizer.compile(qa, trainset=trainset)

# Exporta dados de treinamento para fine-tuning
```

### 4. Construindo Sistemas Complexos

#### Pipeline Multi-Estágio

```python
import dspy

class MultiHopQA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=3)
        self.generate_query = dspy.ChainOfThought("question -> search_query")
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        # Estágio 1: Gere query de busca
        search_query = self.generate_query(question=question).search_query

        # Estágio 2: Recupere contexto
        passages = self.retrieve(search_query).passages
        context = "\n".join(passages)

        # Estágio 3: Gere resposta
        answer = self.generate_answer(context=context, question=question).answer
        return dspy.Prediction(answer=answer, context=context)

# Use o pipeline
qa_system = MultiHopQA()
result = qa_system(question="Quem escreveu o livro que inspirou o filme Blade Runner?")
```

#### Sistema RAG com Otimização

```python
import dspy
from dspy.retrieve.chromadb_rm import ChromadbRM

# Configure o recuperador
retriever = ChromadbRM(
    collection_name="documents",
    persist_directory="./chroma_db"
)

class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)

# Crie e otimize
rag = RAG()

# Otimize com dados de treinamento
from dspy.teleprompt import BootstrapFewShot

optimizer = BootstrapFewShot(metric=validate_answer)
optimized_rag = optimizer.compile(rag, trainset=trainset)
```

## Configuração de Provedor de LM

### Anthropic Claude

```python
import dspy

lm = dspy.Claude(
    model="claude-sonnet-4-5-20250929",
    api_key="your-api-key",  # Ou defina a variável de ambiente ANTHROPIC_API_KEY
    max_tokens=1000,
    temperature=0.7
)
dspy.settings.configure(lm=lm)
```

### OpenAI

```python
lm = dspy.OpenAI(
    model="gpt-4",
    api_key="your-api-key",
    max_tokens=1000
)
dspy.settings.configure(lm=lm)
```

### Modelos Locais (Ollama)

```python
lm = dspy.OllamaLocal(
    model="llama3.1",
    base_url="http://localhost:11434"
)
dspy.settings.configure(lm=lm)
```

### Múltiplos Modelos

```python
# Diferentes modelos para diferentes tarefas
cheap_lm = dspy.OpenAI(model="gpt-3.5-turbo")
strong_lm = dspy.Claude(model="claude-sonnet-4-5-20250929")

# Use modelo barato para recuperação, modelo forte para raciocínio
with dspy.settings.context(lm=cheap_lm):
    context = retriever(question)

with dspy.settings.context(lm=strong_lm):
    answer = generator(context=context, question=question)
```

## Padrões Comuns

### Padrão 1: Saída Estruturada

```python
from pydantic import BaseModel, Field

class PersonInfo(BaseModel):
    name: str = Field(description="Nome completo")
    age: int = Field(description="Idade em anos")
    occupation: str = Field(description="Profissão atual")

class ExtractPerson(dspy.Signature):
    """Extraia informações de pessoa do texto."""
    text = dspy.InputField()
    person: PersonInfo = dspy.OutputField()

extractor = dspy.TypedPredictor(ExtractPerson)
result = extractor(text="João Silva é um engenheiro de software de 35 anos.")
print(result.person.name)  # "João Silva"
print(result.person.age)   # 35
```

### Padrão 2: Otimização Orientada por Assertions

```python
import dspy
from dspy.primitives.assertions import assert_transform_module, backtrack_handler

class MathQA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.solve = dspy.ChainOfThought("problem -> solution: float")

    def forward(self, problem):
        solution = self.solve(problem=problem).solution

        # Assert que solução é numérica
        dspy.Assert(
            isinstance(float(solution), float),
            "A solução deve ser um número",
            backtrack=backtrack_handler
        )

        return dspy.Prediction(solution=solution)
```

### Padrão 3: Auto-Consistência

```python
import dspy
from collections import Counter

class ConsistentQA(dspy.Module):
    def __init__(self, num_samples=5):
        super().__init__()
        self.qa = dspy.ChainOfThought("question -> answer")
        self.num_samples = num_samples

    def forward(self, question):
        # Gere múltiplas respostas
        answers = []
        for _ in range(self.num_samples):
            result = self.qa(question=question)
            answers.append(result.answer)

        # Retorne resposta mais comum
        most_common = Counter(answers).most_common(1)[0][0]
        return dspy.Prediction(answer=most_common)
```

### Padrão 4: Recuperação com Reranking

```python
class RerankedRAG(dspy.Module):
    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=10)
        self.rerank = dspy.Predict("question, passage -> relevance_score: float")
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        # Recupere candidatos
        passages = self.retrieve(question).passages

        # Faça rerank das passagens
        scored = []
        for passage in passages:
            score = float(self.rerank(question=question, passage=passage).relevance_score)
            scored.append((score, passage))

        # Pegue top 3
        top_passages = [p for _, p in sorted(scored, reverse=True)[:3]]
        context = "\n\n".join(top_passages)

        # Gere resposta
        return self.answer(context=context, question=question)
```

## Avaliação e Métricas

### Métricas Personalizadas

```python
def exact_match(example, pred, trace=None):
    """Métrica de correspondência exata."""
    return example.answer.lower() == pred.answer.lower()

def f1_score(example, pred, trace=None):
    """F1 score para sobreposição de texto."""
    pred_tokens = set(pred.answer.lower().split())
    gold_tokens = set(example.answer.lower().split())

    if not pred_tokens:
        return 0.0

    precision = len(pred_tokens & gold_tokens) / len(pred_tokens)
    recall = len(pred_tokens & gold_tokens) / len(gold_tokens)

    if precision + recall == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)
```

### Avaliação

```python
from dspy.evaluate import Evaluate

# Crie um avaliador
evaluator = Evaluate(
    devset=testset,
    metric=exact_match,
    num_threads=4,
    display_progress=True
)

# Avalie modelo
score = evaluator(qa_system)
print(f"Acurácia: {score}")

# Compare otimizado vs não otimizado
score_before = evaluator(qa)
score_after = evaluator(optimized_qa)
print(f"Melhora: {score_after - score_before:.2%}")
```

## Melhores Práticas

### 1. Comece Simples, Itere

```python
# Comece com Predict
qa = dspy.Predict("question -> answer")

# Adicione raciocínio se necessário
qa = dspy.ChainOfThought("question -> answer")

# Adicione otimização quando tiver dados
optimized_qa = optimizer.compile(qa, trainset=data)
```

### 2. Use Signatures Descritivas

```python
# ❌ Ruim: Vago
class Task(dspy.Signature):
    input = dspy.InputField()
    output = dspy.OutputField()

# ✅ Bom: Descritivo
class SummarizeArticle(dspy.Signature):
    """Resuma artigos de notícias em 3-5 pontos-chave."""
    article = dspy.InputField(desc="texto do artigo completo")
    summary = dspy.OutputField(desc="pontos em bullet, 3-5 itens")
```

### 3. Otimize com Dados Representativos

```python
# Crie exemplos de treinamento diversos
trainset = [
    dspy.Example(question="fatorial", answer="...").with_inputs("question"),
    dspy.Example(question="raciocínio", answer="...").with_inputs("question"),
    dspy.Example(question="cálculo", answer="...").with_inputs("question"),
]

# Use conjunto de validação para métrica
def metric(example, pred, trace=None):
    return example.answer in pred.answer
```

### 4. Salve e Carregue Modelos Otimizados

```python
# Salve
optimized_qa.save("models/qa_v1.json")

# Carregue
loaded_qa = dspy.ChainOfThought("question -> answer")
loaded_qa.load("models/qa_v1.json")
```

### 5. Monitore e Depure

```python
# Ative rastreamento
dspy.settings.configure(lm=lm, trace=[])

# Execute predição
result = qa(question="...")

# Inspecione rastreamento
for call in dspy.settings.trace:
    print(f"Prompt: {call['prompt']}")
    print(f"Resposta: {call['response']}")
```

## Comparação com Outras Abordagens

| Recurso | Prompting Manual | LangChain | DSPy |
|---------|-----------------|-----------|------|
| Engenharia de Prompts | Manual | Manual | Automática |
| Otimização | Tentativa e erro | Nenhuma | Orientada por dados |
| Modularidade | Baixa | Média | Alta |
| Type Safety | Não | Limitado | Sim (Signatures) |
| Portabilidade | Baixa | Média | Alta |
| Curva de Aprendizado | Baixa | Média | Média-Alta |

**Quando escolher DSPy:**
- Você tem dados de treinamento ou pode gerá-los
- Precisa de melhoria sistemática de prompts
- Está construindo sistemas multi-estágio complexos
- Quer otimizar em diferentes LMs

**Quando escolher alternativas:**
- Protótipos rápidos (prompting manual)
- Cadeias simples com ferramentas existentes (LangChain)
- Lógica de otimização customizada necessária

## Recursos

- **Documentação**: https://dspy.ai
- **GitHub**: https://github.com/stanfordnlp/dspy (22k+ stars)
- **Discord**: https://discord.gg/XCGy2WDCQB
- **Twitter**: @DSPyOSS
- **Artigo**: "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"

## Veja Também

- `references/modules.md` - Guia detalhado de módulos (Predict, ChainOfThought, ReAct, ProgramOfThought)
- `references/optimizers.md` - Algoritmos de otimização (BootstrapFewShot, MIPRO, BootstrapFinetune)
- `references/examples.md` - Exemplos do mundo real (RAG, agentes, classificadores)