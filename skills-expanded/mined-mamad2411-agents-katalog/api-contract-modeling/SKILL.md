---
name: api-contract-modeling
version: 1.0.0
description: >
  Modela e gera contratos de API (OpenAPI/TypeScript) focados em resiliência.
  Define códigos de erro estruturados, tipagens discriminadas e estratégias
  de fallback explícitas para cada endpoint. Ative ao projetar ou tipar APIs.
triggers:
  - "modelar contrato de API"
  - "criar OpenAPI com erros"
  - "tipar endpoints com fallback"
  - "definir códigos de erro da API"
  - "API error codes"
---

# API CONTRACT MODELING — Contratos resilientes com erros e fallbacks

> **Propósito**: Gerar especificações e tipagens de API onde o caso de erro é tão bem definido, tipado e documentado quanto o caso de sucesso, eliminando ambiguidade em tempo de build.

## Filosofia Central

1. **Erro é Dado** — O payload de erro não é uma exceção descartável, é a estrutura de dados mais crítica para a recuperação do cliente. Na prática: erro sempre possui `code`, `message` e `details` tipados, nunca strings soltas.
2. **Contrato Não-Violento** — O status HTTP é a verdade absoluta do resultado. Na prática: nunca retorne `200 OK` com um corpo indicando falha; use 4xx/5xx e padronize o schema de erro.
3. **Fallback Explícito** — Toda dependência externa ou estado de falha deve ter um destino definido em tempo de modelagem. Na prática: contratos de endpoints que falham devem definir um campo `fallback_strategy` ou `retry_hint`.
4. **Idempotência por Padrão** — Operações de escrita devem ser seguras para retrial. Na prática: mutações (POST/PUT/PATCH) exigem header `Idempotency-Key` mapeado no contrato.

## Quando Ativar

### ✅ Ativar para:
- Projetar especificações OpenAPI (Swagger) para novos endpoints
- Criar interfaces TypeScript/Zod para request/response de APIs
- Definir catálogos de códigos de erro para um microsserviço
- Estruturar payloads de erro para cenários de fallback/circuit breaker

### ❌ NÃO ativar para:
- Implementar a rota/controller de fato → use `backend-patterns`
- Validar regras de negócio complexas isoladas → responda diretamente
- Configurar proxies ou gateways de API → responda diretamente

## Escopo e Limites

- **Cobre**: Estrutura do contrato, matrix de status code, tipagem forte de erros, definição de headers de resiliência, schemas de fallback.
- **Delega**: Lógica de roteamento (`backend-patterns`), Schema de banco (`database-design`).

## Protocolo de Execução

1. **Mapear** os estados possíveis do endpoint: Happy Path, Client Errors (4xx), Server/Infrastructure Errors (5xx) e Fallback States.
2. **Matricular** a "Matriz de Status Code" (tabela cruzando estado vs. HTTP status vs. código interno).
3. **Tipar** os schemas no formato alvo (YAML para OpenAPI ou TS/Zod para código):
   - `SuccessResponse`
   - `ErrorResponse<ErrorCode>` (Discriminated Union)
   - `FallbackResponse`
4. **Projetar Fallbacks**: Definir o que o cliente recebe se o serviço degrada (ex: dados em cache velho, fila de processamento, desvio de funcionalidade).
5. **Validar** o artefato contra o checklist de qualidade (§7).
6. **Entregar** o código/spec pronto para consumo, sem necessidade de refatoração.

## Padrões Específicos

### 1. Tipagem Discriminada de Erro (TypeScript/Zod)

**Regra**: Erros devem usar union types discriminadas por um campo `code` para permitir `switch` seguros no cliente sem casts.

```typescript
// ✅ PASS — Discriminated union permite exaustão no switch
type ApiError = 
  | { status: 400; code: "VALIDATION_ERROR"; details: ZodIssue[] }
  | { status: 409; code: "CONFLICT"; details: { field: string, value: string } }
  | { status: 503; code: "SERVICE_UNAVAILABLE"; details: { retry_after: number } };

function handleError(err: ApiError) {
  switch (err.code) {
    case "VALIDATION_ERROR": return showFormErrors(err.details);
    case "CONFLICT": return alertDuplicate(err.details.field);
    case "SERVICE_UNAVAILABLE": return scheduleRetry(err.details.retry_after);
  }
}

// ❌ FAIL — String solta ou `any` força uso de `instanceof` ou checagens frágeis
type ApiError = {
  error: string; // O que é essa string? Quais os valores possíveis?
  details?: any; // O que tem aqui? O cliente não sabe.
};
```

**Por que importa**: Permite que o compile-time garanta que o cliente trate todos os casos de erro antes do deploy.

### 2. Matriz de Status Code no OpenAPI

**Regra**: A especificação deve documentar explicitamente os códigos de erro, proibindo o `default` genérico sem tipagem de corpo.

```yaml
# ✅ PASS — Códigos explícitos e schemas referenciados
responses:
  '200':
    description: "Sucesso"
    content:
      application/json:
        schema: { $ref: '#/components/schemas/UserResponse' }
  '404':
    description: "Recurso não encontrado"
    content:
      application/json:
        schema: { $ref: '#/components/schemas/NotFoundError' }
  '503':
    description: "Serviço de e-mail indisponível, ativou fallback"
    content:
      application/json:
        schema: { $ref: '#/components/schemas/FallbackResponse' }

# ❌ FAIL — Uso de 'default' mascara os erros reais esperados
responses:
  '200':
    description: "Sucesso"
  'default':
    description: "Erro genérico"
    content:
      application/json:
        schema: { type: object }
```

**Por que importa**: O uso de `default` impede que geradores de código client (como OpenAPI Generator) criem tipagens precisas para cenários de falha.

### 3. Headers de Resiliência Obrigatórios

**Regra**: Mutações devem exigir idempotência; endpoints sujeitos a rate limit ou degrade devem expor políticas de retry.

```typescript
// ✅ PASS — Headers mapeados no contrato de Request/Response
interface CreateUserRequest {
  headers: {
    'Idempotency-Key': string; // Obrigatório para POST
    'X-Retry-Count'?: number;  // Opcional, mas mapeado
  };
  body: CreateUserBody;
}

interface CreateUserResponse {
  headers: {
    'X-RateLimit-Remaining': number;
    'Retry-After'?: number; // Presente apenas em 429/503
  };
  body: User;
}

// ❌ FAIL — Contrato ignora a camada de transporte/resiliência
interface CreateUserRequest {
  name: string;
  email: string;
}
```

**Por que importa**: O contrato reflete a realidade distribuída da rede. Omitir headers força o cliente a adivinhar o comportamento de retry.

### 4. Estrutura de Fallback Explícita

**Regra**: Quando um endpoint depende de serviço externo (ex: pagamento, email), o contrato deve prever o estado degradado.

```typescript
// ✅ PASS — O contrato avisa explicitamente que o dado pode vir degradado
type OrderResponse = {
  order_id: string;
  status: "PAID" | "PENDING_PAYMENT_FALLBACK"; // Estado de fallback no domínio
  payment_details: PaymentDetails | { fallback_reason: "GATEWAY_TIMEOUT", scheduled_retry_at: string };
};

// ❌ FAIL — Falha silenciosa. Cliente acha que está tudo certo.
type OrderResponse = {
  order_id: string;
  status: string; // Pode ser qualquer coisa
  payment_details: PaymentDetails; // Vai crashar se o gateway caiu e o backend retornou nulo
};
```

**Por que importa**: Permite que o frontend renderize uma UI degradada (ex: "Pagamento processando, te avisamos por email") em vez de uma tela de erro 500.

## Anti-Padrões Críticos

| Anti-padrão | Consequência | Alternativa Correta |
| :--- | :--- | :--- |
| Retornar `200` com `{ success: false }` | Clientes HTTP, proxies e CDNs cacheiam erros. | Usar status 4xx/5xx e mover `success` para o status. |
| Lançar erro genérico `500` para falhas de API externa | Cliente não consegue diferenciar bug de infraestrutura temporária. | Mapear falhas externas para `502 Bad Gateway` ou `503 Service Unavailable` com `retry_after`. |
| Mensagens de erro dinâmicas (ex: `throw new Error(db.message)`) | Vazamento de stack trace sensível (IP, query SQL) para o cliente. | Capturar exceção e traduzir para código interno (ex: `INTERNAL_ERROR`), logando o detalhe original apenas no servidor. |
| Contratos sem versionamento (`/api/users`) | Mudanças no contrato (adicionar campo obrigatório) quebram clientes antigos. | Sempre incluir versão no contrato (`/api/v1/users`) e usar o campo `deprecated` ao evoluir. |

## Critérios de Qualidade

Antes de entregar, confirme:

- [ ] Frontmatter completo e triggers condizentes com a tarefa
- [ ] Matriz de status code cobrindo no mínimo: 200, 400/422, 404, 429, 500, 503
- [ ] Union types ou `oneOf`/`anyOf` usados para separar sucesso de erros
- [ ] Todos os erros possuem campo `code` (string enum) e `details` (objeto tipado)
- [ ] Headers de Idempotência e Rate Limit mapeados em endpoints de mutação
- [ ] Fallbacks de serviços externos modelados como um estado possível da response
- [ ] Zero uso de `any`, `unknown` sem type guard, ou `default` solto no OpenAPI
- [ ] Exemplos PASS/FAIL cobrem tanto TypeScript quanto YAML/OpenAPI

## Referências Cruzadas

| Precisa de... | Use a skill... |
| :--- | :--- |
| Implementar as rotas a partir deste contrato | `backend-patterns` |
| Modelar o banco de dados por trás da API | `database-design` |
| Gerar documentação visual para stakeholders | `docx` ou `pptx` |
| Criar clients fortemente tipados (SDK) a partir do contrato | `frontend-design` |
```
Esta skill foi construída na categoria **"Skill de Padrão de Código (API)"**, mas com uma adaptação profunda para **resiliência**. A maioria dos contratos de API falha ao tratar o erro como cidadão de segunda classe. Para resolver isso, o protocolo força a criação de uma "Matriz de Status Code" antes de escrever qualquer linha de spec, e os padrões PASS/FAIL exigem o uso de *Discriminated Unions* (TypeScript) e *oneOf* (OpenAPI). Isso garante que, no momento do build do client, o compilador obrigue o desenvolvedor a lidar com os cenários de fallback e erro de infraestrutura, transformando a resiliência de uma decisão de runtime. Salvar em `/docs/api-contract-modeling/`.