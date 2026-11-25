---
name: fastapi-endpoint
description: Planeja e constrói endpoints FastAPI prontos para produção com SQLAlchemy async, modelos Pydantic v2, injeção de dependência para autenticação e testes pytest. Usa planejamento orientado por entrevista para esclarecer modelos de dados, método de autenticação, estratégia de paginação e cache antes de escrever qualquer código.
tags: [fastapi, python, api, async, pydantic, sqlalchemy, backend]
---

# FastAPI Endpoint Builder

## Quando usar

Use essa habilidade quando você precisar:

- Adicionar novos endpoints à API a um projeto FastAPI existente
- Construir operações CRUD com validação e tratamento de erros apropriados
- Configurar endpoints autenticados com injeção de dependência
- Criar queries assíncronas com SQLAlchemy 2.0
- Gerar cobertura completa de testes para rotas de API

## Fase 1: Explorar (Modo Planejamento)

Entre no modo planejamento. Antes de escrever qualquer código, explore o projeto existente para entender:

### Estrutura do projeto
- Encontre o ponto de entrada da app FastAPI (`main.py`, `app.py`, ou `app/__init__.py`)
- Identifique o padrão de organização de rotas (arquivo único vs diretório `routers/`)
- Verifique se existem diretórios como `models/`, `schemas/`, `crud/`, ou `services/`
- Procure em `pyproject.toml` ou `requirements.txt` pelas dependências instaladas

### Padrões existentes
- Como os endpoints existentes são estruturados? (baseados em função vs baseados em classe)
- Qual ORM é usado? (SQLAlchemy 2.0 async, Tortoise, SQL bruto, nenhum)
- Como a sessão de banco de dados é gerenciada? (`Depends(get_db)`, middleware, outro)
- Que padrão de autenticação existe? (OAuth2PasswordBearer, API key header, customizado)
- Existem modelos base Pydantic ou schemas compartilhados?
- Qual é o formato de resposta padrão? (modelo direto, envolvido `{"data": ..., "meta": ...}`)

### Padrões de teste
- Onde os testes ficam? (`tests/`, `test_*.py`, `*_test.py`)
- Qual cliente de teste é usado? (httpx AsyncClient, TestClient, pytest-asyncio)
- Existem fixtures de teste para banco de dados e autenticação?

## Fase 2: Entrevista (AskUserQuestion)

Use AskUserQuestion para esclarecer requisitos. Pergunte em rodadas — NÃO despeje todas as perguntas de uma vez.

### Rodada 1: Endpoint principal

```
Pergunta: "Qual recurso este endpoint gerencia?"
Cabeçalho: "Recurso"
Opções:
  - "Novo recurso (vou descrever os campos)" — Criando um novo modelo de dados do zero
  - "Modelo existente (estender)" — Adicionando endpoints para um modelo que já existe no código
  - "Endpoint de relacionamento (aninhado)" — ex: /users/{id}/orders — endpoint em um recurso relacionado

Pergunta: "Quais métodos HTTP você precisa?"
Cabeçalho: "Métodos"
multiSelect: true
Opções:
  - "CRUD completo (GET lista, GET detalhe, POST, PUT/PATCH, DELETE)" — Todas as operações padrão
  - "Somente leitura (GET lista + GET detalhe)" — Sem mutações
  - "Ação customizada (POST /resource/{id}/action)" — Endpoint de lógica de negócio, não CRUD padrão
```

### Rodada 2: Modelo de dados (se novo recurso)

```
Pergunta: "Quais campos o recurso possui? (descreva brevemente)"
Cabeçalho: "Campos"
Opções:
  - "Simples (< 6 campos, tipos básicos)" — Strings, ints, booleans, datas
  - "Médio (6-15 campos, alguns relacionamentos)" — Inclui chaves estrangeiras ou enums
  - "Complexo (objetos aninhados, polimórfico)" — Campos JSON, unions discriminadas, campos computados
```

### Rodada 3: Autenticação e controle de acesso

```
Pergunta: "Como este endpoint deve ser autenticado?"
Cabeçalho: "Autenticação"
Opções:
  - "JWT Bearer token (Recomendado)" — OAuth2PasswordBearer com decodificação JWT
  - "API Key header" — Validação de header X-API-Key
  - "Sem autenticação (público)" — Endpoint aberto, sem autenticação necessária
  - "Usar autenticação existente" — Reutilizar a dependência de autenticação já no projeto

Pergunta: "Você precisa de controle de acesso baseado em função?"
Cabeçalho: "RBAC"
Opções:
  - "Não — qualquer usuário autenticado" — Nível único de permissão
  - "Sim — verificação de função (admin, user, etc.)" — Exigir funções específicas por endpoint
  - "Sim — verificação de propriedade" — Usuários podem acessar apenas seus próprios recursos
```

### Rodada 4: Paginação, filtros, cache

```
Pergunta: "Qual estilo de paginação para endpoints de lista?"
Cabeçalho: "Paginação"
Opções:
  - "Baseada em cursor (Recomendado)" — Melhor para dados em tempo real, sem drift de offset
  - "Offset/limit" — Simples, bom para painéis administrativos com números de página
  - "Sem paginação" — Datasets pequenos, retornar todos os resultados

Pergunta: "Você precisa de cache de resposta?"
Cabeçalho: "Cache"
Opções:
  - "Sem cache" — Dados frescos em cada requisição
  - "Headers Cache-Control" — Cache do lado do cliente via headers HTTP
  - "Redis/cache em memória" — Cache do lado do servidor com TTL
```

## Fase 3: Planejamento (ExitPlanMode)

Escreva um plano de implementação concreto cobrindo:

1. **Arquivos para criar/modificar** — caminhos exatos baseados na estrutura descoberta na Fase 1
2. **Schemas Pydantic** — schemas `Create`, `Update`, `Response`, e `List` com tipos de campo
3. **Modelo SQLAlchemy** — nome da tabela, colunas, relacionamentos, índices
4. **Camada CRUD/service** — funções assíncronas para cada operação
5. **Router** — assinaturas de endpoint, códigos de status, modelos de resposta
6. **Dependências** — dependências de autenticação, paginação, filtro
7. **Testes** — casos de teste para caminho feliz, erros de validação, falhas de autenticação, não encontrado

Apresente via ExitPlanMode para aprovação do usuário.

## Fase 4: Executar

Após aprovação, implemente seguindo esta ordem:

### Passo 1: Schemas Pydantic

```python
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class ResourceBase(BaseModel):
    """Campos compartilhados entre criação e resposta."""
    name: str
    # ... campos da entrevista

class ResourceCreate(ResourceBase):
    """Campos obrigatórios para criar o recurso."""
    pass

class ResourceUpdate(BaseModel):
    """Todos os campos opcionais para atualizações parciais."""
    name: str | None = None

class ResourceResponse(ResourceBase):
    """Recurso completo com campos gerados pelo BD."""
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    updated_at: datetime

class ResourceListResponse(BaseModel):
    """Resposta de lista paginada."""
    data: list[ResourceResponse]
    next_cursor: str | None = None
    has_more: bool
```

### Passo 2: Modelo SQLAlchemy

```python
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from app.database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

### Passo 3: Camada CRUD/service

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

async def get_resource(db: AsyncSession, resource_id: UUID) -> Resource | None:
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    return result.scalar_one_or_none()

async def list_resources(
    db: AsyncSession,
    cursor: str | None = None,
    limit: int = 20,
) -> tuple[list[Resource], str | None]:
    query = select(Resource).order_by(Resource.created_at.desc()).limit(limit + 1)
    if cursor:
        query = query.where(Resource.created_at < decode_cursor(cursor))
    result = await db.execute(query)
    items = list(result.scalars().all())
    next_cursor = encode_cursor(items[-1].created_at) if len(items) > limit else None
    return items[:limit], next_cursor

async def create_resource(db: AsyncSession, data: ResourceCreate) -> Resource:
    resource = Resource(**data.model_dump())
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource

async def update_resource(
    db: AsyncSession, resource_id: UUID, data: ResourceUpdate
) -> Resource | None:
    resource = await get_resource(db, resource_id)
    if not resource:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)
    await db.commit()
    await db.refresh(resource)
    return resource

async def delete_resource(db: AsyncSession, resource_id: UUID) -> bool:
    resource = await get_resource(db, resource_id)
    if not resource:
        return False
    await db.delete(resource)
    await db.commit()
    return True
```

### Passo 4: Router com dependências

```python
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

router = APIRouter(prefix="/resources", tags=["resources"])

@router.get("", response_model=ResourceListResponse)
async def list_resources_endpoint(
    cursor: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),  # se auth for obrigatória
):
    items, next_cursor = await list_resources(db, cursor=cursor, limit=limit)
    return ResourceListResponse(
        data=items,
        next_cursor=next_cursor,
        has_more=next_cursor is not None,
    )

@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource_endpoint(
    resource_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resource = await get_resource(db, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.post("", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource_endpoint(
    data: ResourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_resource(db, data)

@router.patch("/{resource_id}", response_model=ResourceResponse)
async def update_resource_endpoint(
    resource_id: UUID,
    data: ResourceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resource = await update_resource(db, resource_id, data)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource_endpoint(
    resource_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = await delete_resource(db, resource_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Resource not found")
```

### Passo 5: Testes

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_resource(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/resources",
        json={"name": "Test Resource"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Resource"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_resource_not_found(client: AsyncClient, auth_headers: dict):
    response = await client.get(
        "/resources/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_resources_pagination(client: AsyncClient, auth_headers: dict):
    # Criar múltiplos recursos primeiro
    for i in range(5):
        await client.post(
            "/resources",
            json={"name": f"Resource {i}"},
            headers=auth_headers,
        )
    response = await client.get("/resources?limit=2", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["has_more"] is True
    assert data["next_cursor"] is not None

@pytest.mark.asyncio
async def test_create_resource_unauthorized(client: AsyncClient):
    response = await client.post("/resources", json={"name": "Test"})
    assert response.status_code in (401, 403)

@pytest.mark.asyncio
async def test_update_resource_partial(client: AsyncClient, auth_headers: dict):
    # Criar
    create_resp = await client.post(
        "/resources",
        json={"name": "Original"},
        headers=auth_headers,
    )
    resource_id = create_resp.json()["id"]
    # Atualização parcial
    response = await client.patch(
        f"/resources/{resource_id}",
        json={"name": "Updated"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"

@pytest.mark.asyncio
async def test_delete_resource(client: AsyncClient, auth_headers: dict):
    create_resp = await client.post(
        "/resources",
        json={"name": "To Delete"},
        headers=auth_headers,
    )
    resource_id = create_resp.json()["id"]
    response = await client.delete(
        f"/resources/{resource_id}", headers=auth_headers
    )
    assert response.status_code == 204
    # Verificar se foi deletado
    get_resp = await client.get(
        f"/resources/{resource_id}", headers=auth_headers
    )
    assert get_resp.status_code == 404
```

## Padrões-chave a seguir

### Injeção de dependência para autenticação

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = decode_jwt(token)
    user = await db.get(User, payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

def require_role(*roles: str):
    """Factory para controle de acesso baseado em função."""
    async def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return checker
```

### Helper de paginação baseada em cursor

```python
import base64
from datetime import datetime

def encode_cursor(dt: datetime) -> str:
    return base64.urlsafe_b64encode(dt.isoformat().encode()).decode()

def decode_cursor(cursor: str) -> datetime:
    return datetime.fromisoformat(base64.urlsafe_b64decode(cursor).decode())
```

### Respostas de erro

Sempre use `HTTPException` do FastAPI com mensagens de detalhe consistentes. Para erros de validação, Pydantic v2 lida com eles automaticamente via `RequestValidationError` (422).

```python
# 404 — não encontrado
raise HTTPException(status_code=404, detail="Resource not found")

# 409 — conflito (duplicado)
raise HTTPException(status_code=409, detail="Resource with this name already exists")

# 403 — proibido
raise HTTPException(status_code=403, detail="Not allowed to modify this resource")
```

## Checklist antes de finalizar

- [ ] Todos os endpoints retornam códigos de status apropriados (201 para POST, 204 para DELETE)
- [ ] Schemas Pydantic usam `model_config = ConfigDict(from_attributes=True)` para modo ORM
- [ ] Endpoint de lista tem paginação com limit configurável
- [ ] Dependência de autenticação é aplicada a todos os endpoints não-públicos
- [ ] Testes cobrem: caminho feliz, não encontrado, não autorizado, erros de validação
- [ ] Router é registrado na app FastAPI principal
- [ ] Modelo de banco de dados tem índices apropriados em colunas filtradas/ordenadas