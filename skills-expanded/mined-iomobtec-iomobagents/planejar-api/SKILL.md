---
name: planejar-api
description: "Projeta a especificação REST completa de um serviço — endpoints, schemas de request e response e tratamento de erros. Use quando o arquiteto vai definir o contrato de uma nova API."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: planejar-api

Desenha a **especificação completa de uma API REST**: endpoints, verbos, paths, contratos de request/response, códigos de status, versionamento e regras de autenticação. Produz o contrato que governa o desenvolvimento — não escreve implementação.

**Agente:** arquiteto  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`, `seguranca.md`, `appsec.md §14, §15, §16, §17`

---

## Quando usar

- Antes de implementar qualquer endpoint novo em serviço existente
- Ao criar novo serviço (em conjunto com `definir-microservico`)
- Quando há necessidade de versionar uma API com breaking changes
- Para alinhar contrato entre equipes antes do desenvolvimento paralelo

---

## Entrada esperada

- Casos de uso que a API deve suportar (o que o cliente precisa fazer)
- Entidades envolvidas e seus atributos
- Quem consome a API (BFF, Process, frontend externo, parceiro)
- Restrições: autenticação necessária, rate limiting, SLA esperado

---

## Processo de execução

### Passo 1 — Identificar recursos e operações

Mapear cada entidade de negócio como recurso REST e as operações CRUD que fazem sentido:

| Operação | Verbo | Semântica |
|---|---|---|
| Criar | POST | Cria novo recurso; retorna 201 + Location header |
| Listar | GET (coleção) | Retorna lista paginada; nunca retorna coleção sem limite |
| Buscar | GET (item) | Retorna recurso por ID; 404 se não encontrado |
| Atualizar total | PUT | Substitui o recurso inteiro; idempotente |
| Atualizar parcial | PATCH | Atualiza apenas campos enviados |
| Deletar | DELETE | Remove ou soft-deletes; 204 sem body |

### Passo 2 — Definir paths

Regras de nomenclatura:
- Substantivos no plural: `/users`, `/orders`, `/products`
- Hierarquia para recursos aninhados: `/users/{id}/addresses`
- Ações que não se encaixam em CRUD usam sub-resource descritivo: `/orders/{id}/cancel`
- Nunca verbos no path: ~~`/getUser`~~, ~~`/createOrder`~~

### Passo 3 — Definir contratos de request

Para cada endpoint:
- Campos obrigatórios vs opcionais
- Tipos de dados (string, number, boolean, date ISO 8601, uuid)
- Restrições de formato (min/max length, regex, enum values)
- Headers obrigatórios (Authorization, Content-Type, X-Correlation-Id)

### Passo 4 — Definir contratos de response

- Campos retornados e seus tipos
- Campos sensíveis que nunca aparecem na response (senhas, tokens, dados pessoais sem mascaramento — ver `seguranca.md §1`)
- Envelope padrão para listas: `{ data: [], meta: { total, page, pageSize } }`
- Envelope padrão para erros: RFC 7807 (`type`, `title`, `status`, `detail`, `instance`)

### Passo 5 — Definir códigos de status

| Código | Quando usar |
|---|---|
| 200 | Sucesso com body (GET, PATCH, PUT) |
| 201 | Recurso criado (POST) |
| 204 | Sucesso sem body (DELETE, ações) |
| 400 | Request malformado (validação de schema) |
| 401 | Não autenticado |
| 403 | Autenticado mas sem permissão |
| 404 | Recurso não encontrado |
| 409 | Conflito (duplicidade, estado incompatível) |
| 422 | Regra de negócio violada (request válido, mas inaceitável) |
| 429 | Rate limit excedido |
| 500 | Erro interno não esperado |

### Passo 6 — Definir estratégia de versionamento

- **Sem breaking change:** não versionar — adicionar campo opcional é retrocompatível
- **Com breaking change:** versão no path (`/v2/users`) ou header (`API-Version: 2`)
- Versão antiga mantida por período definido (registrar no PR a data de deprecação)

### Passo 7 — Security design por endpoint

Para cada endpoint definido nos passos anteriores, responder:

| Pergunta | Referência |
|---|---|
| Quais propriedades do objeto são expostas nesta resposta? Há campos que não deveriam estar disponíveis para este consumidor? | `appsec.md §14` — BOPLA |
| Quem pode chamar esta função? Há distinção de papel (user / admin / sistema)? O guard é declarado explicitamente? | `appsec.md §15` — Function Level Auth |
| Este endpoint faz parte de um fluxo de negócio sensível (compra, reserva, cupom, registro)? Requer proteção contra automação? | `appsec.md §16` — Business Flows |
| Este endpoint deve existir em todas as versões da API ou apenas na atual? Há data de deprecação para versão anterior? | `appsec.md §17` — Inventory |

Registrar decisões na seção `## Notas de segurança` da especificação de API.

---

## Saída produzida

```markdown
## Especificação de API: <nome do serviço>

**Versão:** v1  
**Base URL:** /api/v1  
**Autenticação:** Bearer JWT | API Key | Público

---

### POST /recursos

**Descrição:** <o que faz>  
**Auth:** Obrigatória

Request:
```json
{
  "campo" (required): "string, min:3, max:100",
  "outrocampo" (optional): "uuid"
}
```

Response 201:
```json
{
  "id": "uuid",
  "campo": "string",
  "createdAt": "ISO 8601"
}
```

Erros:
- 400: campo inválido ou ausente
- 409: recurso já existe com mesmo identificador único

---

### GET /recursos

**Descrição:** Lista recursos paginados  
**Auth:** Obrigatória

Query params:
- `page` (optional, default: 1): número da página
- `pageSize` (optional, default: 20, max: 100): itens por página
- `filter` (optional): filtro por campo X

Response 200:
```json
{
  "data": [{ "id": "uuid", "campo": "string" }],
  "meta": { "total": 42, "page": 1, "pageSize": 20 }
}
```

---

### Campos nunca retornados

- `passwordHash`
- `cpf` em claro (retornar apenas mascarado: `***.***.***-12`)
```
