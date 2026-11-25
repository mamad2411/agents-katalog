---
name: pydantic-ai
description: "Construa agentes de IA prontos para produção com PydanticAI — type-safe tool use, structured outputs, dependency injection, e suporte multi-modelo."
category: ai-agents
risk: safe
source: community
date_added: "2026-03-18"
author: suhaibjanjua
tags: [pydantic-ai, ai-agents, llm, openai, anthropic, gemini, tool-use, structured-output, python]
tools: [claude, cursor, gemini]
---

# PydanticAI — Agentes de IA Tipados em Python

## Visão Geral

PydanticAI é um framework de agentes Python da equipe Pydantic que traz as mesmas garantias de type-safety e validação do Pydantic para aplicações baseadas em LLM. Suporta saídas estruturadas (validadas com modelos Pydantic), dependency injection para testabilidade, respostas em streaming, conversas multi-turno e tool use — em OpenAI, Anthropic, Google Gemini, Groq, Mistral e Ollama. Use essa habilidade ao construir agentes de IA em produção, chatbots ou pipelines de LLM onde correção e testabilidade são importantes.

## Quando Usar Essa Habilidade

- Use ao construir agentes de IA em Python que chamam ferramentas e retornam dados estruturados
- Use quando precisa de saídas de LLM validadas e tipadas (não strings brutas)
- Use quando quer escrever testes unitários para lógica de agentes sem chamar um LLM real
- Use quando trocando entre provedores de LLM sem reescrever código de agente
- Use quando o usuário pergunta sobre `Agent`, `@agent.tool`, `RunContext`, `ModelRetry`, ou `result_type`

## Como Funciona

### Passo 1: Instalação

```bash
pip install pydantic-ai

# Instale extras para provedores específicos
pip install 'pydantic-ai[openai]'       # OpenAI / Azure OpenAI
pip install 'pydantic-ai[anthropic]'    # Anthropic Claude
pip install 'pydantic-ai[gemini]'       # Google Gemini
pip install 'pydantic-ai[groq]'         # Groq
pip install 'pydantic-ai[vertexai]'     # Google Vertex AI
```

### Passo 2: Um Agente Mínimo

```python
from pydantic_ai import Agent

# Agente simples — retorna uma string simples
agent = Agent(
    'anthropic:claude-sonnet-4-6',
    system_prompt='You are a helpful assistant. Be concise.',
)

result = agent.run_sync('What is the capital of Japan?')
print(result.data)  # "Tokyo"
print(result.usage())  # Usage(requests=1, request_tokens=..., response_tokens=...)
```

### Passo 3: Saída Estruturada com Modelos Pydantic

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class MovieReview(BaseModel):
    title: str
    year: int
    rating: float  # 0.0 to 10.0
    summary: str
    recommended: bool

agent = Agent(
    'openai:gpt-4o',
    result_type=MovieReview,
    system_prompt='You are a film critic. Return structured reviews.',
)

result = agent.run_sync('Review Inception (2010)')
review = result.data  # Fully typed MovieReview instance
print(f"{review.title} ({review.year}): {review.rating}/10")
print(f"Recommended: {review.recommended}")
```

### Passo 4: Tool Use

Registre ferramentas com `@agent.tool` — o LLM pode chamá-las durante uma execução:

```python
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
import httpx

class WeatherReport(BaseModel):
    city: str
    temperature_c: float
    condition: str

weather_agent = Agent(
    'anthropic:claude-sonnet-4-6',
    result_type=WeatherReport,
    system_prompt='Get current weather for the requested city.',
)

@weather_agent.tool
async def get_temperature(ctx: RunContext, city: str) -> dict:
    """Fetch the current temperature for a city from the weather API."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f'https://wttr.in/{city}?format=j1')
        data = r.json()
        return {
            'temp_c': float(data['current_condition'][0]['temp_C']),
            'description': data['current_condition'][0]['weatherDesc'][0]['value'],
        }

import asyncio
result = asyncio.run(weather_agent.run('What is the weather in Tokyo?'))
print(result.data)
```

### Passo 5: Dependency Injection

Injete serviços (banco de dados, clientes HTTP, config) em agentes para testabilidade:

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel

@dataclass
class Deps:
    db: Database
    user_id: str

class SupportResponse(BaseModel):
    message: str
    escalate: bool

support_agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=Deps,
    result_type=SupportResponse,
    system_prompt='You are a support agent. Use the tools to help customers.',
)

@support_agent.tool
async def get_order_history(ctx: RunContext[Deps]) -> list[dict]:
    """Fetch recent orders for the current user."""
    return await ctx.deps.db.get_orders(ctx.deps.user_id, limit=5)

@support_agent.tool
async def create_refund(ctx: RunContext[Deps], order_id: str, reason: str) -> dict:
    """Initiate a refund for a specific order."""
    return await ctx.deps.db.create_refund(order_id, reason, ctx.deps.user_id)

# Uso
async def handle_support(user_id: str, message: str):
    deps = Deps(db=get_db(), user_id=user_id)
    result = await support_agent.run(message, deps=deps)
    return result.data
```

### Passo 6: Testes com TestModel

Escreva testes unitários sem chamar LLMs reais:

```python
from pydantic_ai.models.test import TestModel

def test_support_agent_escalates():
    with support_agent.override(model=TestModel()):
        # TestModel retorna uma resposta mínima válida correspondendo a result_type
        result = support_agent.run_sync(
            'I want to cancel my account',
            deps=Deps(db=FakeDb(), user_id='user-123'),
        )
    # Teste a estrutura, não as palavras exatas do LLM
    assert isinstance(result.data, SupportResponse)
    assert isinstance(result.data.escalate, bool)
```

**FunctionModel** para respostas de teste determinísticas:

```python
from pydantic_ai.models.function import FunctionModel, ModelContext

def my_model(messages, info):
    return ModelResponse(parts=[TextPart('Always this response')])

with agent.override(model=FunctionModel(my_model)):
    result = agent.run_sync('anything')
```

### Passo 7: Streaming de Respostas

```python
import asyncio
from pydantic_ai import Agent

agent = Agent('anthropic:claude-sonnet-4-6')

async def stream_response():
    async with agent.run_stream('Write a haiku about Python') as result:
        async for chunk in result.stream_text():
            print(chunk, end='', flush=True)
    print()  # newline
    print(f"Total tokens: {result.usage()}")

asyncio.run(stream_response())
```

### Passo 8: Conversas Multi-Turno

```python
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessagesTypeAdapter

agent = Agent('openai:gpt-4o', system_prompt='You are a helpful assistant.')

# Primeiro turno
result1 = agent.run_sync('My name is Alice.')
history = result1.all_messages()

# Segundo turno — passa histórico de conversa
result2 = agent.run_sync('What is my name?', message_history=history)
print(result2.data)  # "Your name is Alice."
```

## Exemplos

### Exemplo 1: Agente de Revisão de Código

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import Literal

class CodeReview(BaseModel):
    quality: Literal['excellent', 'good', 'needs_work', 'poor']
    issues: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    approved: bool

code_review_agent = Agent(
    'anthropic:claude-sonnet-4-6',
    result_type=CodeReview,
    system_prompt="""
    You are a senior engineer performing code review.
    Evaluate code quality, identify issues, and provide actionable suggestions.
    Set approved=True only for good or excellent quality code with no security issues.
    """,
)

def review_code(diff: str) -> CodeReview:
    result = code_review_agent.run_sync(f"Review this code:\n\n{diff}")
    return result.data
```

### Exemplo 2: Agente com Lógica de Retry

```python
from pydantic_ai import Agent, ModelRetry
from pydantic import BaseModel, field_validator

class StrictJson(BaseModel):
    value: int

    @field_validator('value')
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('value must be positive')
        return v

agent = Agent('openai:gpt-4o-mini', result_type=StrictJson)

@agent.result_validator
async def validate_result(ctx, result: StrictJson) -> StrictJson:
    if result.value > 1000:
        raise ModelRetry('Value must be under 1000. Try again with a smaller number.')
    return result
```

### Exemplo 3: Pipeline Multi-Agente

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class ResearchSummary(BaseModel):
    key_points: list[str]
    conclusion: str

class BlogPost(BaseModel):
    title: str
    body: str
    meta_description: str

researcher = Agent('openai:gpt-4o', result_type=ResearchSummary)
writer = Agent('anthropic:claude-sonnet-4-6', result_type=BlogPost)

async def research_and_write(topic: str) -> BlogPost:
    # Estágio 1: pesquisa
    research = await researcher.run(f'Research the topic: {topic}')

    # Estágio 2: escrever baseado na pesquisa
    post = await writer.run(
        f'Write a blog post about: {topic}\n\nResearch:\n' +
        '\n'.join(f'- {p}' for p in research.data.key_points) +
        f'\n\nConclusion: {research.data.conclusion}'
    )
    return post.data
```

## Boas Práticas

- ✅ Sempre defina `result_type` com um modelo Pydantic — evite retornar strings brutas em produção
- ✅ Use `deps_type` com um dataclass para dependency injection — torna agentes testáveis
- ✅ Use `TestModel` em testes unitários — nunca chame um LLM real em CI
- ✅ Adicione `@agent.result_validator` para verificações de lógica de negócio além da validação Pydantic
- ✅ Use `run_stream` para saídas longas em aplicações viradas ao usuário para mostrar resultados progressivos
- ❌ Não coloque secrets (chaves de API) em argumentos `Agent()` — use variáveis de ambiente
- ❌ Não compartilhe uma única instância `Agent` entre tarefas async se as deps diferirem — crie instâncias por requisição ou use `agent.run()` com `deps` por chamada
- ❌ Não capture `ValidationError` amplamente — deixe PydanticAI fazer retry com `ModelRetry` para erros de saída de LLM recuperáveis

## Notas de Segurança e Privacidade

- Configure chaves de API via variáveis de ambiente (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.) — nunca as escreva em código.
- Valide todas as entradas de ferramentas antes de passar para sistemas externos — use modelos Pydantic ou verificações manuais.
- Ferramentas que mutam dados (escrever em BD, enviar emails, chamar APIs de pagamento) devem exigir confirmação explícita do usuário antes do agente invocá-las em produção.
- Registre `result.all_messages()` para trilhas de auditoria quando agentes realizam ações consequentes.
- Configure limites de `retries=` em `Agent()` para evitar loops descontrolados em falhas de validação persistentes.

## Armadilhas Comuns

- **Problema:** `ValidationError` em toda resposta de LLM — saída estruturada nunca valida
  **Solução:** Simplifique campos de `result_type`. Use `Optional` e `default` quando apropriado. O modelo pode lutar com schemas muito estritos.

- **Problema:** Ferramenta nunca é chamada pelo LLM
  **Solução:** Escreva um docstring claro e específico para a função de ferramenta — PydanticAI envia o docstring como descrição de ferramenta ao LLM.

- **Problema:** Dependência `RunContext` é `None` dentro de uma ferramenta
  **Solução:** Passe `deps=` ao chamar `agent.run()` ou `agent.run_sync()`. Dependências não são configuradas globalmente.

- **Problema:** Erro `asyncio.run()` ao chamar `agent.run()` dentro de FastAPI
  **Solução:** Use `await agent.run()` diretamente em handlers de rota FastAPI async — não envolva em `asyncio.run()`.

## Habilidades Relacionadas

- `@langchain-architecture` — Framework alternativo de IA em Python (mais flexível, menos type-safe)
- `@llm-application-dev-ai-assistant` — Padrões gerais de desenvolvimento de aplicações LLM
- `@fastapi-templates` — Servindo agentes PydanticAI via endpoints FastAPI
- `@agent-orchestration-multi-agent-optimize` — Orquestrando múltiplos agentes PydanticAI