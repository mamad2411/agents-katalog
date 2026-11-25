---
name: python-patterns
description: Princípios de desenvolvimento Python e tomada de decisão. Seleção de framework, padrões async, type hints, estrutura de projeto. Ensina a pensar, não a copiar.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Python Patterns

> Princípios de desenvolvimento Python e tomada de decisão para 2025.
> **Aprenda a PENSAR, não memorize padrões.**

---

## ⚠️ Como Usar Esta Skill

Esta skill ensina **princípios de tomada de decisão**, não código fixo para copiar.

- PERGUNTE ao usuário a preferência de framework quando estiver em dúvida
- Escolha async vs sync com base no CONTEXTO
- Não padrão para o mesmo framework todas as vezes

---

## 1. Seleção de Framework (2025)

### Árvore de Decisão

```
O que você está construindo?
│
├── API-first / Microserviços
│   └── FastAPI (async, moderno, rápido)
│
├── Web full-stack / CMS / Admin
│   └── Django (batteries-included)
│
├── Simples / Script / Aprendizado
│   └── Flask (mínimo, flexível)
│
├── Servindo API de IA/ML
│   └── FastAPI (Pydantic, async, uvicorn)
│
└── Workers em background
    └── Celery + qualquer framework
```

### Princípios de Comparação

| Fator | FastAPI | Django | Flask |
|-------|---------|--------|-------|
| **Melhor para** | APIs, microserviços | Full-stack, CMS | Simples, aprendizado |
| **Async** | Nativo | Django 5.0+ | Via extensões |
| **Admin** | Manual | Built-in | Via extensões |
| **ORM** | Escolha a sua | Django ORM | Escolha a sua |
| **Curva de aprendizado** | Baixa | Média | Baixa |

### Perguntas de Seleção:
1. Isso é apenas API ou full-stack?
2. Precisa de interface admin?
3. Time familiarizado com async?
4. Infraestrutura existente?

---

## 2. Decisão Async vs Sync

### Quando Usar Async

```
async def é melhor quando:
├── Operações I/O-bound (banco de dados, HTTP, arquivo)
├── Muitas conexões simultâneas
├── Recursos em tempo real
├── Comunicação entre microserviços
└── FastAPI/Starlette/Django ASGI

def (sync) é melhor quando:
├── Operações CPU-bound
├── Scripts simples
├── Base de código legada
├── Time não familiarizado com async
└── Bibliotecas bloqueantes (sem versão async)
```

### A Regra Ouro

```
I/O-bound → async (esperando algo externo)
CPU-bound → sync + multiprocessing (computando)

Não faça:
├── Misture sync e async desatentamente
├── Use bibliotecas sync em código async
└── Force async para trabalho CPU
```

### Seleção de Biblioteca Async

| Necessidade | Biblioteca Async |
|-------------|------------------|
| HTTP client | httpx |
| PostgreSQL | asyncpg |
| Redis | aioredis / redis-py async |
| File I/O | aiofiles |
| Database ORM | SQLAlchemy 2.0 async, Tortoise |

---

## 3. Estratégia de Type Hints

### Quando Usar Type Hints

```
Sempre use type hints:
├── Parâmetros de função
├── Tipos de retorno
├── Atributos de classe
├── APIs públicas

Pode pular:
├── Variáveis locais (deixe a inferência trabalhar)
├── Scripts únicos
├── Testes (geralmente)
```

### Padrões de Type Comuns

```python
# Estes são padrões, entenda-os:

# Optional → pode ser None
from typing import Optional
def find_user(id: int) -> Optional[User]: ...

# Union → um de múltiplos tipos
def process(data: str | dict) -> None: ...

# Coleções genéricas
def get_items() -> list[Item]: ...
def get_mapping() -> dict[str, int]: ...

# Callable
from typing import Callable
def apply(fn: Callable[[int], str]) -> str: ...
```

### Pydantic para Validação

```
Quando usar Pydantic:
├── Modelos de request/response de API
├── Configuração/settings
├── Validação de dados
├── Serialização

Benefícios:
├── Validação em tempo de execução
├── JSON schema gerado automaticamente
├── Funciona nativamente com FastAPI
└── Mensagens de erro claras
```

---

## 4. Princípios de Estrutura de Projeto

### Seleção de Estrutura

```
Projeto pequeno / Script:
├── main.py
├── utils.py
└── requirements.txt

API média:
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── schemas/
├── tests/
└── pyproject.toml

Aplicação grande:
├── src/
│   └── myapp/
│       ├── core/
│       ├── api/
│       ├── services/
│       ├── models/
│       └── ...
├── tests/
└── pyproject.toml
```

### Princípios de Estrutura FastAPI

```
Organize por feature ou camada:

Por camada:
├── routes/ (endpoints de API)
├── services/ (lógica de negócio)
├── models/ (modelos de banco de dados)
├── schemas/ (modelos Pydantic)
└── dependencies/ (dependências compartilhadas)

Por feature:
├── users/
│   ├── routes.py
│   ├── service.py
│   └── schemas.py
└── products/
    └── ...
```

---

## 5. Princípios Django (2025)

### Django Async (Django 5.0+)

```
Django suporta async:
├── Views async
├── Middleware async
├── ORM async (limitado)
└── Deploy ASGI

Quando usar async no Django:
├── Chamadas de API externa
├── WebSocket (Channels)
├── Views de alta concorrência
└── Gatilho de tarefas em background
```

### Melhores Práticas Django

```
Design de modelo:
├── Models ricos, views magras
├── Use managers para queries comuns
├── Classes base abstratas para campos compartilhados

Views:
├── Class-based para CRUD complexo
├── Function-based para endpoints simples
├── Use viewsets com DRF

Queries:
├── select_related() para FKs
├── prefetch_related() para M2M
├── Evite queries N+1
└── Use .only() para campos específicos
```

---

## 6. Princípios FastAPI

### async def vs def no FastAPI

```
Use async def quando:
├── Usando drivers de banco de dados async
├── Fazendo chamadas HTTP async
├── Operações I/O-bound
└── Quer lidar com concorrência

Use def quando:
├── Operações bloqueantes
├── Drivers de banco de dados sync
├── Trabalho CPU-bound
└── FastAPI executa em threadpool automaticamente
```

### Injeção de Dependência

```
Use dependências para:
├── Sessões de banco de dados
├── Usuário atual / Autenticação
├── Configuração
├── Recursos compartilhados

Benefícios:
├── Testabilidade (mock de dependências)
├── Separação limpa
├── Limpeza automática (yield)
```

### Integração Pydantic v2

```python
# FastAPI + Pydantic são fortemente integrados:

# Validação de request
@app.post("/users")
async def create(user: UserCreate) -> UserResponse:
    # user já está validado
    ...

# Serialização de response
# Tipo de retorno torna-se schema de resposta
```

---

## 7. Tarefas em Background

### Guia de Seleção

| Solução | Melhor Para |
|---------|-------------|
| **BackgroundTasks** | Tarefas simples, in-process |
| **Celery** | Workflows distribuídos, complexos |
| **ARQ** | Async, baseado em Redis |
| **RQ** | Fila Redis simples |
| **Dramatiq** | Baseado em actors, mais simples que Celery |

### Quando Usar Cada Um

```
FastAPI BackgroundTasks:
├── Operações rápidas
├── Sem necessidade de persistência
├── Fire-and-forget
└── Mesmo processo

Celery/ARQ:
├── Tarefas de longa duração
├── Precisa de lógica de retry
├── Workers distribuídos
├── Fila persistente
└── Workflows complexos
```

---

## 8. Princípios de Tratamento de Erros

### Estratégia de Exceção

```
No FastAPI:
├── Crie classes de exceção customizadas
├── Registre manipuladores de exceção
├── Retorne formato de erro consistente
└── Registre sem expor internals

Padrão:
├── Levante exceções de domínio em services
├── Capture e transforme em manipuladores
└── Cliente recebe resposta de erro limpa
```

### Filosofia de Resposta de Erro

```
Inclua:
├── Código de erro (programático)
├── Mensagem (legível para humano)
├── Detalhes (nível de campo quando aplicável)
└── NÃO stack traces (segurança)
```

---

## 9. Princípios de Teste

### Estratégia de Teste

| Tipo | Propósito | Ferramentas |
|------|----------|-------------|
| **Unitário** | Lógica de negócio | pytest |
| **Integração** | Endpoints de API | pytest + httpx/TestClient |
| **E2E** | Workflows completos | pytest + BD |

### Teste Async

```python
# Use pytest-asyncio para testes async

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/users")
        assert response.status_code == 200
```

### Estratégia de Fixtures

```
Fixtures comuns:
├── db_session → Conexão de banco de dados
├── client → Cliente de teste
├── authenticated_user → Usuário com token
└── sample_data → Setup de dados de teste
```

---

## 10. Checklist de Decisão

Antes de implementar:

- [ ] **Perguntou ao usuário sobre preferência de framework?**
- [ ] **Escolheu framework para ESTE contexto?** (não só padrão)
- [ ] **Decidiu async vs sync?**
- [ ] **Planejou estratégia de type hints?**
- [ ] **Definiu estrutura de projeto?**
- [ ] **Planejou tratamento de erros?**
- [ ] **Considerou tarefas em background?**

---

## 11. Anti-Padrões para Evitar

### ❌ NÃO FAÇA:
- Padrão Django para APIs simples (FastAPI pode ser melhor)
- Use bibliotecas sync em código async
- Pule type hints para APIs públicas
- Coloque lógica de negócio em routes/views
- Ignore queries N+1
- Misture async e sync desatentamente

### ✅ FAÇA:
- Escolha framework com base em contexto
- Pergunte sobre requisitos async
- Use Pydantic para validação
- Separe concerns (routes → services → repos)
- Teste caminhos críticos

---

> **Lembre-se**: Padrões Python tratam de tomada de decisão para SEU contexto específico. Não copie código—pense sobre o que funciona melhor para sua aplicação.