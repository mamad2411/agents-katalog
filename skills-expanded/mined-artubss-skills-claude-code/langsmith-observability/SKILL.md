---
name: langsmith-observability
description: Plataforma de observabilidade para LLM com rastreamento, avaliação e monitoramento. Use ao depurar aplicações LLM, avaliar saídas de modelos em datasets, monitorar sistemas em produção ou construir pipelines de testes sistemáticos para aplicações de IA.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Observability, LangSmith, Tracing, Evaluation, Monitoring, Debugging, Testing, LLM Ops, Production]
dependencies: [langsmith>=0.2.0]
---

# LangSmith - Plataforma de Observabilidade para LLM

Plataforma de desenvolvimento para depuração, avaliação e monitoramento de modelos de linguagem e aplicações de IA.

## Quando usar LangSmith

**Use LangSmith quando:**
- Depurar problemas em aplicações LLM (prompts, chains, agents)
- Avaliar saídas de modelos sistematicamente contra datasets
- Monitorar sistemas LLM em produção
- Construir testes de regressão para features de IA
- Analisar latência, uso de tokens e custos
- Colaborar em engenharia de prompts

**Recursos principais:**
- **Tracing**: Capturar entradas, saídas, latência para todas as chamadas LLM
- **Evaluation**: Testes sistemáticos com avaliadores built-in e customizados
- **Datasets**: Criar conjuntos de testes a partir de traces em produção ou manualmente
- **Monitoring**: Rastrear métricas, erros e custos em produção
- **Integrações**: Funciona com OpenAI, Anthropic, LangChain, LlamaIndex

**Use alternativas:**
- **Weights & Biases**: Rastreamento de experimentos em deep learning, treinamento de modelos
- **MLflow**: Ciclo de vida geral de ML, foco em registro de modelos
- **Arize/WhyLabs**: Monitoramento de ML, detecção de data drift

## Início rápido

### Instalação

```bash
pip install langsmith

# Defina variáveis de ambiente
export LANGSMITH_API_KEY="your-api-key"
export LANGSMITH_TRACING=true
```

### Rastreamento básico com @traceable

```python
from langsmith import traceable
from openai import OpenAI

client = OpenAI()

@traceable
def generate_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Automaticamente rastreado no LangSmith
result = generate_response("What is machine learning?")
```

### Wrapper OpenAI (rastreamento automático)

```python
from langsmith.wrappers import wrap_openai
from openai import OpenAI

# Envolver cliente para rastreamento automático
client = wrap_openai(OpenAI())

# Todas as chamadas automaticamente rastreadas
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Conceitos principais

### Runs e traces

Um **run** é uma unidade de execução única (chamada LLM, chain, tool). Runs formam **traces** hierárquicas mostrando o fluxo completo de execução.

```python
from langsmith import traceable

@traceable(run_type="chain")
def process_query(query: str) -> str:
    # Run pai
    context = retrieve_context(query)  # Run filha
    response = generate_answer(query, context)  # Run filha
    return response

@traceable(run_type="retriever")
def retrieve_context(query: str) -> list:
    return vector_store.search(query)

@traceable(run_type="llm")
def generate_answer(query: str, context: list) -> str:
    return llm.invoke(f"Context: {context}\n\nQuestion: {query}")
```

### Projetos

Projetos organizam runs relacionadas. Configure via ambiente ou código:

```python
import os
os.environ["LANGSMITH_PROJECT"] = "my-project"

# Ou por função
@traceable(project_name="my-project")
def my_function():
    pass
```

## Client API

```python
from langsmith import Client

client = Client()

# Listar runs
runs = list(client.list_runs(
    project_name="my-project",
    filter='eq(status, "success")',
    limit=100
))

# Obter detalhes da run
run = client.read_run(run_id="...")

# Criar feedback
client.create_feedback(
    run_id="...",
    key="correctness",
    score=0.9,
    comment="Good answer"
)
```

## Datasets e avaliação

### Criar dataset

```python
from langsmith import Client

client = Client()

# Criar dataset
dataset = client.create_dataset("qa-test-set", description="QA evaluation")

# Adicionar exemplos
client.create_examples(
    inputs=[
        {"question": "What is Python?"},
        {"question": "What is ML?"}
    ],
    outputs=[
        {"answer": "A programming language"},
        {"answer": "Machine learning"}
    ],
    dataset_id=dataset.id
)
```

### Executar avaliação

```python
from langsmith import evaluate

def my_model(inputs: dict) -> dict:
    # Sua lógica de modelo
    return {"answer": generate_answer(inputs["question"])}

def correctness_evaluator(run, example):
    prediction = run.outputs["answer"]
    reference = example.outputs["answer"]
    score = 1.0 if reference.lower() in prediction.lower() else 0.0
    return {"key": "correctness", "score": score}

results = evaluate(
    my_model,
    data="qa-test-set",
    evaluators=[correctness_evaluator],
    experiment_prefix="v1"
)

print(f"Average score: {results.aggregate_metrics['correctness']}")
```

### Avaliadores built-in

```python
from langsmith.evaluation import LangChainStringEvaluator

# Usar avaliadores LangChain
results = evaluate(
    my_model,
    data="qa-test-set",
    evaluators=[
        LangChainStringEvaluator("qa"),
        LangChainStringEvaluator("cot_qa")
    ]
)
```

## Rastreamento avançado

### Contexto de rastreamento

```python
from langsmith import tracing_context

with tracing_context(
    project_name="experiment-1",
    tags=["production", "v2"],
    metadata={"version": "2.0"}
):
    # Todas as chamadas traceable herdam o contexto
    result = my_function()
```

### Runs manuais

```python
from langsmith import trace

with trace(
    name="custom_operation",
    run_type="tool",
    inputs={"query": "test"}
) as run:
    result = do_something()
    run.end(outputs={"result": result})
```

### Processar entradas/saídas

```python
def sanitize_inputs(inputs: dict) -> dict:
    if "password" in inputs:
        inputs["password"] = "***"
    return inputs

@traceable(process_inputs=sanitize_inputs)
def login(username: str, password: str):
    return authenticate(username, password)
```

### Sampling

```python
import os
os.environ["LANGSMITH_TRACING_SAMPLING_RATE"] = "0.1"  # 10% sampling
```

## Integração com LangChain

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Rastreamento habilitado automaticamente com LANGSMITH_TRACING=true
llm = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

chain = prompt | llm

# Todas as runs da chain rastreadas automaticamente
response = chain.invoke({"input": "Hello!"})
```

## Monitoramento em produção

### Hub prompts

```python
from langsmith import Client

client = Client()

# Buscar prompt do hub
prompt = client.pull_prompt("my-org/qa-prompt")

# Usar na aplicação
result = prompt.invoke({"question": "What is AI?"})
```

### Client assíncrono

```python
from langsmith import AsyncClient

async def main():
    client = AsyncClient()

    runs = []
    async for run in client.list_runs(project_name="my-project"):
        runs.append(run)

    return runs
```

### Coleta de feedback

```python
from langsmith import Client

client = Client()

# Coletar feedback do usuário
def record_feedback(run_id: str, user_rating: int, comment: str = None):
    client.create_feedback(
        run_id=run_id,
        key="user_rating",
        score=user_rating / 5.0,  # Normalizar para 0-1
        comment=comment
    )

# Na sua aplicação
record_feedback(run_id="...", user_rating=4, comment="Helpful response")
```

## Integração de testes

### Integração com Pytest

```python
from langsmith import test

@test
def test_qa_accuracy():
    result = my_qa_function("What is Python?")
    assert "programming" in result.lower()
```

### Avaliação em CI/CD

```python
from langsmith import evaluate

def run_evaluation():
    results = evaluate(
        my_model,
        data="regression-test-set",
        evaluators=[accuracy_evaluator]
    )

    # Falhar CI se a acurácia cair
    assert results.aggregate_metrics["accuracy"] >= 0.9, \
        f"Accuracy {results.aggregate_metrics['accuracy']} below threshold"
```

## Melhores práticas

1. **Nomenclatura estruturada** - Use convenções consistentes para nomes de projetos/runs
2. **Adicionar metadados** - Inclua versão, ambiente, informações do usuário
3. **Sampling em produção** - Use taxa de sampling para controlar volume
4. **Criar datasets** - Construa conjuntos de testes a partir de casos interessantes em produção
5. **Automatizar avaliação** - Execute avaliações em pipelines CI/CD
6. **Monitorar custos** - Rastreie tendências de uso de tokens e latência

## Problemas comuns

**Traces não aparecem:**
```python
import os
# Garanta que o rastreamento está habilitado
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "your-key"

# Verifique a conexão
from langsmith import Client
client = Client()
print(client.list_projects())  # Deve funcionar
```

**Alta latência do rastreamento:**
```python
# Habilitar batching em background (padrão)
from langsmith import Client
client = Client(auto_batch_tracing=True)

# Ou use sampling
os.environ["LANGSMITH_TRACING_SAMPLING_RATE"] = "0.1"
```

**Payloads grandes:**
```python
# Ocultar campos sensíveis/grandes
@traceable(
    process_inputs=lambda x: {k: v for k, v in x.items() if k != "large_field"}
)
def my_function(data):
    pass
```

## Referências

- **[Uso avançado](references/advanced-usage.md)** - Avaliadores customizados, rastreamento distribuído, hub prompts
- **[Solução de problemas](references/troubleshooting.md)** - Problemas comuns, depuração, performance

## Recursos

- **Documentação**: https://docs.smith.langchain.com
- **Python SDK**: https://github.com/langchain-ai/langsmith-sdk
- **Web App**: https://smith.langchain.com
- **Versão**: 0.2.0+
- **Licença**: MIT