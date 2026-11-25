---
name: Pydantic & Data Modeling
description: Modelagem de dados com Pydantic v2, validação de schemas, computed fields, serialização, e contratos de dados para o pipeline de memória.
---

# Pydantic & Data Modeling

## Quando Usar

- Ao criar ou modificar modelos de dados do pipeline
- Ao definir schemas para structured outputs do LLM
- Ao validar entrada/saída de tools MCP

## Modelos do Pipeline

O pipeline tem 3 modelos core que representam estágios:

```
RawEvent (Landing Zone) → MemoryCandidate (Extração) → MemoryItem (Persistência)
```

### RawEvent — Dado Bruto

```python
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class SourceKind(str, Enum):
    CONVERSATION = "conversation"
    COMMIT = "commit"
    DIFF = "diff"
    DOCUMENT = "document"
    GUIDELINE = "guideline"
    TOOL_OUTPUT = "tool_output"

class RawEvent(BaseModel):
    event_id: str
    source_kind: SourceKind
    payload: str
    project_hint: str | None = None
    domain_hint: str | None = None
    author: str | None = None
    correlation_id: str | None = None
    metadata: dict | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### MemoryCandidate — Candidato Extraído

```python
class MemoryCandidate(BaseModel):
    project: str
    type: str  # BusinessRule, DesignPattern, DesignRule, ArchitecturalDecision
    domain: list[str] = Field(default_factory=list)
    title: str
    summary: str
    details: str = ""
    examples: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    proposed_weight: float = Field(ge=0.0, le=1.0, default=0.5)
    evidence: list[EvidenceRef] = Field(default_factory=list)
```

### MemoryItem — Memória Canônica

```python
class MemoryItem(BaseModel):
    memory_id: str  # hash(project+type+title)
    project: str
    category: str
    domain: list[str] = Field(default_factory=list)
    title: str
    summary: str
    details: str = ""
    status: MemoryStatus = MemoryStatus.PROPOSED
    weight_manual: float = Field(ge=0.0, le=1.0, default=0.5)
    weight_confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    weight_usage: float = Field(ge=0.0, le=1.0, default=0.0)
    weight_feedback: float = Field(ge=0.0, le=1.0, default=0.0)
    effective_weight: float = Field(ge=0.0, le=1.0, default=0.5)
```

## Padrões de Validação Pydantic v2

```python
# Validação com Field
weight: float = Field(ge=0.0, le=1.0)  # 0.0 <= weight <= 1.0

# Computed fields
from pydantic import computed_field

class Item(BaseModel):
    first: str
    last: str
    
    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first} {self.last}"

# Enum validation
class Status(str, Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"

# Custom validators
from pydantic import field_validator

class MyModel(BaseModel):
    title: str
    
    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()
```

## ID Canônico

```python
import hashlib

def generate_memory_id(project: str, type: str, title: str) -> str:
    normalized = f"{project}:{type}:{title.lower().strip()}"
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]
```

## Regras

- `Field(description=...)` para documentação inline
- `Field(default_factory=...)` para valores mutáveis (listas, dicts, datetime)
- Nunca usar `dict` como tipo — sempre criar um model específico
- Enums para valores finitos e conhecidos
- Validadores custom para regras de negócio no nível do modelo
- Serialização: `.model_dump()` para dict, `.model_dump_json()` para JSON
