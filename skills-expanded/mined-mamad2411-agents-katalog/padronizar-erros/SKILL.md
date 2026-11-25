---
name: padronizar-erros
description: "Define o formato de resposta de erro e os padrões de código HTTP do serviço. Use quando o arquiteto vai padronizar o tratamento de erros de uma API."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: padronizar-erros

Define o **formato, categorias e convenções de erros** compartilhados entre todos os serviços do projeto, garantindo que consumidores (BFF, frontend, parceiros) tratem erros de forma consistente independentemente de qual serviço os produziu.

**Agente:** arquiteto  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`, `seguranca.md`

---

## Quando usar

- Ao iniciar um novo projeto ou microserviço (definir o padrão antes de implementar)
- Quando serviços diferentes retornam erros em formatos incompatíveis
- Ao adicionar novo tipo de erro de negócio sem categoria existente
- Para auditar se os erros do projeto expõem informações internas indevidamente

---

## Entrada esperada

- Contexto: novo projeto (definir do zero) ou projeto existente (auditar e padronizar)
- Tipos de erros de negócio já conhecidos
- Consumidores dos erros: BFF, frontend, parceiro externo, outro serviço
- Requisitos de localização (mensagens em PT-BR, EN, etc.)

---

## Fundamento: RFC 7807 Problem Details

Conforme `backend.md §4`, o padrão obrigatório para todos os serviços é **RFC 7807** (`application/problem+json`). Esta skill expande esse padrão com categorias e convenções específicas do projeto:

```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Field 'email' must be a valid email address.",
  "instance": "/api/v1/users"
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | URI | Sim | Identificador único do tipo de erro (URL documentável) |
| `title` | string | Sim | Descrição curta e estável (não muda entre ocorrências) |
| `status` | number | Sim | HTTP status code |
| `detail` | string | Não | Descrição da ocorrência específica (pode variar) |
| `instance` | URI | Não | Path da request que gerou o erro |

Campos adicionais são permitidos pelo RFC.

---

## Processo de execução

### Passo 1 — Definir as categorias de erro

| Categoria | Status | `type` URI | Quando usar |
|---|---|---|---|
| Validação de schema | 400 | `.../errors/validation-failed` | Campo inválido, ausente, fora do formato |
| Não autenticado | 401 | `.../errors/unauthorized` | Token ausente, expirado ou inválido |
| Sem permissão | 403 | `.../errors/forbidden` | Autenticado mas sem acesso ao recurso |
| Não encontrado | 404 | `.../errors/not-found` | Recurso inexistente |
| Conflito de estado | 409 | `.../errors/conflict` | Duplicidade, violação de unicidade |
| Regra de negócio | 422 | `.../errors/business-rule-violated` | Request válido, mas viola invariante de negócio |
| Rate limit | 429 | `.../errors/rate-limit-exceeded` | Muitas requisições |
| Erro interno | 500 | `.../errors/internal-server-error` | Falha inesperada — nunca expor detalhes |

### Passo 2 — Definir erros de negócio específicos

Cada regra de negócio que pode falhar recebe seu próprio `type`:

```
https://api.example.com/errors/order-already-cancelled
https://api.example.com/errors/insufficient-balance
https://api.example.com/errors/product-out-of-stock
```

O `type` é estável e documentado — o frontend pode tomar decisões baseadas nele.  
O `detail` varia por ocorrência e é para leitura humana.

### Passo 3 — Definir campos adicionais por categoria

Para erros de validação (400), adicionar campo `errors`:

```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 400,
  "detail": "One or more fields failed validation.",
  "instance": "/api/v1/users",
  "errors": [
    { "field": "email", "message": "Must be a valid email address." },
    { "field": "name", "message": "Must be at least 2 characters." }
  ]
}
```

### Passo 4 — Definir o que nunca aparece em erros

Campos **proibidos** em qualquer resposta de erro (ver `seguranca.md §2`):
- Stack trace (`error.stack`)
- Mensagem de exceção interna (`error.message` de erros de banco, ORM, etc.)
- Caminho de arquivo do servidor
- Versão de dependência ou framework
- Query SQL que falhou
- Detalhes de infraestrutura (nome do pod, IP interno, porta)

O `detail` em erros 500 deve ser genérico: `"An unexpected error occurred. Reference: <correlationId>"`.

### Passo 5 — Definir o `correlationId`

Todo erro inclui o `correlationId` da request para correlação com logs:

```json
{
  "type": "...",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/orders",
  "correlationId": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Passo 6 — Definir implementação no NestJS

```typescript
// exception.filter.ts — filtro global que aplica o padrão em todos os erros
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const status = exception instanceof HttpException
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    // Nunca expor detalhes internos em 500
    const detail = status === 500
      ? 'An unexpected error occurred.'
      : (exception as HttpException).message;

    response.status(status).json({
      type: `https://api.example.com/errors/${getErrorType(status)}`,
      title: getErrorTitle(status),
      status,
      detail,
      instance: request.url,
      correlationId: request.headers['x-correlation-id'],
    });
  }
}
```

---

## Saída produzida

```markdown
## Padrão de Erros: <nome do projeto/serviço>

**Formato base:** RFC 7807 (application/problem+json)  
**Base URL de tipos:** https://api.example.com/errors/

---

### Catálogo de erros

| Tipo | Status | `type` | Campos adicionais |
|---|---|---|---|
| Validação | 400 | validation-failed | `errors[]` com campo e mensagem |
| Não autenticado | 401 | unauthorized | — |
| Sem permissão | 403 | forbidden | — |
| Não encontrado | 404 | not-found | `resource` |
| Conflito | 409 | conflict | `conflictingField` |
| Regra de negócio | 422 | `<nome-especifico>` | Conforme o caso |
| Rate limit | 429 | rate-limit-exceeded | `retryAfter` (segundos) |
| Interno | 500 | internal-server-error | `correlationId` apenas |

---

### Campos sempre presentes

- `type`, `title`, `status`, `instance`, `correlationId`

### Campos nunca presentes

- Stack trace, mensagem de exceção interna, query SQL, path de arquivo

---

### Erros de negócio específicos

| Código de negócio | Status | `type` |
|---|---|---|
| <regra de negócio 1> | 422 | `<slug>` |
```
