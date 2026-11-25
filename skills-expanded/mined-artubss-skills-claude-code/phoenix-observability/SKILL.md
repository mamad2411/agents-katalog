---
name: phoenix-observability
description: Plataforma de observabilidade de IA de código aberto para rastreamento de LLM, avaliação e monitoramento. Use ao debugar aplicações de LLM com rastreamentos detalhados, executar avaliações em datasets ou monitorar sistemas de IA em produção com insights em tempo real.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Observability, Phoenix, Arize, Tracing, Evaluation, Monitoring, LLM Ops, OpenTelemetry]
dependencies: [arize-phoenix>=12.0.0]
---

# Phoenix - Plataforma de Observabilidade de IA

Plataforma de observabilidade e avaliação de IA de código aberto para aplicações de LLM com rastreamento, avaliação, datasets, experimentos e monitoramento em tempo real.

## Quando usar Phoenix

**Use Phoenix quando:**
- Debugar problemas em aplicações de LLM com rastreamentos detalhados
- Executar avaliações sistemáticas em datasets
- Monitorar sistemas de LLM em produção em tempo real
- Construir pipelines de experimentos para comparação de prompts/modelos
- Usar observabilidade auto-hospedada sem dependência de vendor

**Principais funcionalidades:**
- **Rastreamento**: Coleta de traces baseada em OpenTelemetry para qualquer framework de LLM
- **Avaliação**: Avaliadores LLM-as-judge para avaliação de qualidade
- **Datasets**: Conjuntos de testes versionados para testes de regressão
- **Experimentos**: Comparejar prompts, modelos e configurações
- **Playground**: Testes interativos de prompts com múltiplos modelos
- **Código aberto**: Auto-hospedado com PostgreSQL ou SQLite

**Use alternativas em vez disso:**
- **LangSmith**: Plataforma gerenciada com integração prioritária a LangChain
- **Weights & Biases**: Foco em rastreamento de experimentos de deep learning
- **Arize Cloud**: Phoenix gerenciada com funcionalidades enterprise
- **MLflow**: Ciclo de vida geral de ML, foco em registro de modelos

## Início rápido

### Instalação

```bash
pip install arize-phoenix

# Com backends específicos
pip install arize-phoenix[embeddings]  # Análise de embeddings
pip install arize-phoenix-otel         # Configuração OpenTelemetry
pip install arize-phoenix-evals        # Framework de avaliação
pip install arize-phoenix-client       # Cliente REST leve
```

### Iniciar servidor Phoenix

```python
import phoenix as px

# Iniciar em notebook (modo ThreadServer)
session = px.launch_app()

# Visualizar UI
session.view()  # iframe incorporado
print(session.url)  # http://localhost:6006
```

### Servidor em linha de comando (produção)

```bash
# Iniciar servidor Phoenix
phoenix serve

# Com PostgreSQL
export PHOENIX_SQL_DATABASE_URL="postgresql://user:pass@host/db"
phoenix serve --port 6006
```

### Rastreamento básico

```python
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor

# Configurar OpenTelemetry com Phoenix
tracer_provider = register(
    project_name="my-llm-app",
    endpoint="http://localhost:6006/v1/traces"
)

# Instrumentar SDK do OpenAI
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

# Todas as chamadas OpenAI agora são rastreadas
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Conceitos principais

### Traces e spans

Um **trace** representa um fluxo de execução completo, enquanto **spans** são operações individuais dentro desse trace.

```python
from phoenix.otel import register
from opentelemetry import trace

# Configurar rastreamento
tracer_provider = register(project_name="my-app")
tracer = trace.get_tracer(__name__)

# Criar spans personalizados
with tracer.start_as_current_span("process_query") as span:
    span.set_attribute("input.value", query)

    # Spans filhos são aninhados automaticamente
    with tracer.start_as_current_span("retrieve_context"):
        context = retriever.search(query)

    with tracer.start_as_current_span("generate_response"):
        response = llm.generate(query, context)

    span.set_attribute("output.value", response)
```

### Projetos

Projetos organizam traces relacionados:

```python
import os
os.environ["PHOENIX_PROJECT_NAME"] = "production-chatbot"

# Ou por trace
from phoenix.otel import register
tracer_provider = register(project_name="experiment-v2")
```

## Instrumentação de frameworks

### OpenAI

```python
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor

tracer_provider = register()
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
```

### LangChain

```python
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

tracer_provider = register()
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

# Todas as operações LangChain são rastreadas
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke("Hello!")
```

### LlamaIndex

```python
from phoenix.otel import register
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor

tracer_provider = register()
LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)
```

### Anthropic

```python
from phoenix.otel import register
from openinference.instrumentation.anthropic import AnthropicInstrumentor

tracer_provider = register()
AnthropicInstrumentor().instrument(tracer_provider=tracer_provider)
```

## Framework de avaliação

### Avaliadores integrados

```python
from phoenix.evals import (
    OpenAIModel,
    HallucinationEvaluator,
    RelevanceEvaluator,
    ToxicityEvaluator,
    llm_classify
)

# Configurar modelo para avaliação
eval_model = OpenAIModel(model="gpt-4o")

# Avaliar alucinação
hallucination_eval = HallucinationEvaluator(eval_model)
results = hallucination_eval.evaluate(
    input="What is the capital of France?",
    output="The capital of France is Paris.",
    reference="Paris is the capital of France."
)
```

### Avaliadores personalizados

```python
from phoenix.evals import llm_classify

# Definir avaliação personalizada
def evaluate_helpfulness(input_text, output_text):
    template = """
    Evaluate if the response is helpful for the given question.

    Question: {input}
    Response: {output}

    Is this response helpful? Answer 'helpful' or 'not_helpful'.
    """

    result = llm_classify(
        model=eval_model,
        template=template,
        input=input_text,
        output=output_text,
        rails=["helpful", "not_helpful"]
    )
    return result
```

### Executar avaliações em dataset

```python
from phoenix import Client
from phoenix.evals import run_evals

client = Client()

# Obter spans para avaliar
spans_df = client.get_spans_dataframe(
    project_name="my-app",
    filter_condition="span_kind == 'LLM'"
)

# Executar avaliações
eval_results = run_evals(
    dataframe=spans_df,
    evaluators=[
        HallucinationEvaluator(eval_model),
        RelevanceEvaluator(eval_model)
    ],
    provide_explanation=True
)

# Registrar resultados de volta ao Phoenix
client.log_evaluations(eval_results)
```

## Datasets e experimentos

### Criar dataset

```python
from phoenix import Client

client = Client()

# Criar dataset
dataset = client.create_dataset(
    name="qa-test-set",
    description="QA evaluation dataset"
)

# Adicionar exemplos
client.add_examples_to_dataset(
    dataset_name="qa-test-set",
    examples=[
        {
            "input": {"question": "What is Python?"},
            "output": {"answer": "A programming language"}
        },
        {
            "input": {"question": "What is ML?"},
            "output": {"answer": "Machine learning"}
        }
    ]
)
```

### Executar experimento

```python
from phoenix import Client
from phoenix.experiments import run_experiment

client = Client()

def my_model(input_data):
    """Sua função de modelo."""
    question = input_data["question"]
    return {"answer": generate_answer(question)}

def accuracy_evaluator(input_data, output, expected):
    """Avaliador personalizado."""
    return {
        "score": 1.0 if expected["answer"].lower() in output["answer"].lower() else 0.0,
        "label": "correct" if expected["answer"].lower() in output["answer"].lower() else "incorrect"
    }

# Executar experimento
results = run_experiment(
    dataset_name="qa-test-set",
    task=my_model,
    evaluators=[accuracy_evaluator],
    experiment_name="baseline-v1"
)

print(f"Average accuracy: {results.aggregate_metrics['accuracy']}")
```

## API Client

### Consultar traces e spans

```python
from phoenix import Client

client = Client(endpoint="http://localhost:6006")

# Obter spans como DataFrame
spans_df = client.get_spans_dataframe(
    project_name="my-app",
    filter_condition="span_kind == 'LLM'",
    limit=1000
)

# Obter span específico
span = client.get_span(span_id="abc123")

# Obter trace
trace = client.get_trace(trace_id="xyz789")
```

### Registrar feedback

```python
from phoenix import Client

client = Client()

# Registrar feedback do usuário
client.log_annotation(
    span_id="abc123",
    name="user_rating",
    annotator_kind="HUMAN",
    score=0.8,
    label="helpful",
    metadata={"comment": "Good response"}
)
```

### Exportar dados

```python
# Exportar para pandas
df = client.get_spans_dataframe(project_name="my-app")

# Exportar traces
traces = client.list_traces(project_name="my-app")
```

## Deployment em produção

### Docker

```bash
docker run -p 6006:6006 arizephoenix/phoenix:latest
```

### Com PostgreSQL

```bash
# Definir URL do banco de dados
export PHOENIX_SQL_DATABASE_URL="postgresql://user:pass@host:5432/phoenix"

# Iniciar servidor
phoenix serve --host 0.0.0.0 --port 6006
```

### Variáveis de ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `PHOENIX_PORT` | Porta do servidor HTTP | `6006` |
| `PHOENIX_HOST` | Endereço de binding do servidor | `127.0.0.1` |
| `PHOENIX_GRPC_PORT` | Porta gRPC/OTLP | `4317` |
| `PHOENIX_SQL_DATABASE_URL` | Conexão do banco de dados | SQLite temp |
| `PHOENIX_WORKING_DIR` | Diretório de armazenamento de dados | Temp do OS |
| `PHOENIX_ENABLE_AUTH` | Habilitar autenticação | `false` |
| `PHOENIX_SECRET` | Segredo para assinatura JWT | Obrigatório se auth habilitado |

### Com autenticação

```bash
export PHOENIX_ENABLE_AUTH=true
export PHOENIX_SECRET="your-secret-key-min-32-chars"
export PHOENIX_ADMIN_SECRET="admin-bootstrap-token"

phoenix serve
```

## Melhores práticas

1. **Use projetos**: Separe traces por ambiente (dev/staging/prod)
2. **Adicione metadados**: Inclua IDs de usuário, IDs de sessão para debugging
3. **Avalie regularmente**: Execute avaliações automatizadas em CI/CD
4. **Versionize datasets**: Rastreie mudanças em conjuntos de testes ao longo do tempo
5. **Monitore custos**: Rastreie uso de tokens via dashboards do Phoenix
6. **Auto-hospede**: Use PostgreSQL para deployments em produção

## Problemas comuns

**Traces não aparecem:**
```python
from phoenix.otel import register

# Verificar endpoint
tracer_provider = register(
    project_name="my-app",
    endpoint="http://localhost:6006/v1/traces"  # Endpoint correto
)

# Forçar flush
from opentelemetry import trace
trace.get_tracer_provider().force_flush()
```

**Alta memória em notebook:**
```python
# Fechar sessão quando concluído
session = px.launch_app()
# ... fazer trabalho ...
session.close()
px.close_app()
```

**Problemas de conexão com banco de dados:**
```bash
# Verificar conexão PostgreSQL
psql $PHOENIX_SQL_DATABASE_URL -c "SELECT 1"

# Verificar logs do Phoenix
phoenix serve --log-level debug
```

## Referências

- **[Uso avançado](references/advanced-usage.md)** - Avaliadores personalizados, experimentos, setup em produção
- **[Troubleshooting](references/troubleshooting.md)** - Problemas comuns, debugging, performance

## Recursos

- **Documentação**: https://docs.arize.com/phoenix
- **Repositório**: https://github.com/Arize-ai/phoenix
- **Docker Hub**: https://hub.docker.com/r/arizephoenix/phoenix
- **Versão**: 12.0.0+
- **Licença**: Apache 2.0