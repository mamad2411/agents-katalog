---
name: LLM Structured Outputs
description: Extração estruturada usando LLMs com Instructor/Pydantic, JSON Schema validation, retry strategies, e prompts de extração de conhecimento.
---

# LLM Structured Outputs

## Quando Usar

- Ao extrair candidatos de memória de texto bruto
- Ao integrar com APIs de LLM para output tipado
- Ao criar prompts de extração de conhecimento

## Conceito

**Structured Output** = forçar o LLM a retornar JSON que valida contra um schema Pydantic. Elimina parsing manual e garante tipo-segurança.

```
Texto bruto → LLM + Schema → JSON validado → Pydantic model
```

## Instructor — Biblioteca de Referência

```python
import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

class ExtractionResult(BaseModel):
    candidates: list[MemoryCandidate] = Field(
        description="Lista de conhecimentos duráveis extraídos"
    )

base_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = instructor.from_openai(base_client)

result = await client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=ExtractionResult,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ],
    max_retries=2  # Retry automático se JSON inválido
)
```

## System Prompt de Extração

```python
def system_prompt(project: str, category: str | None) -> str:
    return f"""Você é um extrator de conhecimento durável para o projeto {project}.

EXTRAIA APENAS conhecimento que vale a pena reter a longo prazo:
- Regras de negócio (BusinessRule)
- Padrões de design (DesignPattern)
- Regras de implementação (DesignRule)
- Decisões arquiteturais (ArchitecturalDecision)

IGNORE informação efêmera, bugs temporários, ou detalhes triviais.

REGRAS RÍGIDAS:
1. Cada candidato PRECISA de pelo menos 1 evidência
2. O title deve ser em inglês técnico descritivo
3. proposed_weight: 0.8+ para decisões arquiteturais, 0.6+ para regras, 0.5+ para padrões
4. Se não houver conhecimento durável, retorne lista vazia
5. Prefira poucos candidatos de alta qualidade a muitos de baixa"""
```

## Alternativas ao Instructor

| Biblioteca | Use Case |
|-----------|----------|
| **Instructor** | OpenAI, Anthropic, Gemini — Pydantic-first |
| **OpenAI JSON Mode** | `response_format={"type": "json_object"}` nativo |
| **Outlines** | Modelos open-source (Llama, Mistral) — constrained decoding |
| **LangChain** | Chains complexas com structured output |

## Retry Strategy

```python
result = await client.chat.completions.create(
    response_model=ExtractionResult,
    max_retries=2,                         # Máximo 2 retries
    # Instructor automaticamente:
    # 1. Detecta JSON inválido
    # 2. Inclui o erro de validação no retry
    # 3. Pede ao LLM corrigir
)
```

## Edge Cases

| Situação | Comportamento |
|----------|--------------|
| Texto sem conhecimento durável | Retornar `candidates: []` |
| LLM alucina evidência | Validação via Pydantic catch; evidência vira obrigatória |
| Texto muito longo | Truncar ou chunkar antes da extração |
| Rate limit da API | Implementar exponential backoff |

## Regras

- Sempre definir `max_retries` (2-3 é razoável)
- response_model Pydantic = single source of truth para o schema
- System prompt deve ser prescritivo (REGRAS RÍGIDAS)
- Instruir retorno de lista vazia quando não há conhecimento durável
- Usar `gpt-4o-mini` para extração (custo-benefício) e `gpt-4o` para casos complexos
