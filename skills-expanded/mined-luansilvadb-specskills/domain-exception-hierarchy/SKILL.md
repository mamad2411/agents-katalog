---
name: domain-exception-hierarchy
version: 1.0.0
description: >
  Projeta e gera hierarquias de exceções customizadas com contrato explícito,
  resiliência por camada e cobertura de casos excepcionais em cada etapa.
  Ative ao criar, refatorar ou auditar sistemas de erro de um domínio.
triggers:
  - "criar exceções customizadas"
  - "hierarquia de exceções"
  - "contrato de exceções"
  - "tratamento de erros por domínio"
  - "resiliência em exceções"
  - "domain exceptions"
  - "/exception-hierarchy"
---

# DOMAIN EXCEPTION HIERARCHY — Exceções semânticas, contratos explícitos, resiliência por camada

> **Propósito**: Gerar um sistema de exceções que funcione como mapa de falhas do domínio —
> cada tipo descreve *o que quebrou no negócio*, carrega contexto suficiente para diagnóstico
> sem depender de stack trace, e garante que nenhuma falha seja silenciada.

---

## Filosofia Central

1. **Semântica sobre mecânica** — O nome da exceção descreve o evento de negócio, não o mecanismo (`InsufficientFunds` não `InvalidOperationException`). Na prática: ao ler o tipo, qualquer dev entende o cenário sem abrir o código.

2. **Contexto obrigatório no construtor** — Toda exceção carrega os dados mínimos para diagnóstico offline. Na prática: nunca lançar exceção com apenas mensagem de texto — sempre incluir IDs, valores envolvidos, timestamp e correlation ID.

3. **Fronteira de tradução única** — Exceções de infraestrutura são convertidas para exceções de domínio exatamente uma vez, no adapter. Na prática: a camada de domínio nunca importa `HttpException`, `DatabaseError`, etc.

4. **Captura com destino explícito** — Todo `catch` deve ter uma de três saídas: retry, fallback ou propagação enriquecida. Na prática: `catch { log(e) }` sem ação subsequente é proibido.

5. **Estado inalterado em falha** — Se uma operação lança, o estado anterior permanece íntegro. Na prática: operações que mutam estado usam rollback explícito ou executam mutação só após validação total.

6. **Hierarquia reflete árvore de decisão** — A herança segue a pergunta "que categoria de falha é esta?", não "quem lançou". Na prática: `DomainException > ValidationException > ConstraintViolationException`, nunca `UserServiceException`.

---

## Quando Ativar

### ✅ Ativar para:
- Projetar o sistema de exceções de um domínio do zero
- Refatorar exceções genéricas (`throw new Error()`, `RuntimeException`) em hierarquia semântica
- Auditar se um codebase segue contrato de exceções por camada
- Implementar recovery patterns (retry, fallback, circuit breaker) atrelados a tipos de exceção
- Criar mapeamento adapter→domínio para exceções de bibliotecas externas

### ❌ NÃO ativar para:
- Tratamento de erro em UI/frontend → use `frontend-error-handling`
- Logging estratégico → use `logging`; esta skill define *o que* logar, não *como*
- Exceções de framework específico sem contexto de domínio → responda diretamente

---

## Escopo e Limites

| Esta skill cobre | Esta skill delega |
|---|---|
| Definição da classe base e hierarquia | Configuração de linters/TSConfig para `no-any` |
| Contrato de exceção por método/camada | Estrutura de pastas do projeto |
| Padrões de recovery por tipo | Implementação de circuit breaker completo |
| Mapeamento adapter → domínio | Ferramentas de observabilidade (DataDog, Grafana) |
| Exemplos em TypeScript e Java | Testes unitários de exceção (use `testing-patterns`) |

---

## Stack Alvo

| Linguagem | Versão mínima | Convenção |
|---|---|---|
| TypeScript | 5.0+ | Classe `extends Error` com `cause` nativo |
| Java | 17+ | `extends RuntimeException`, records para contexto |
| Python | 3.11+ | `ExceptionGroup` onde aplicável, `__cause__` |

> Exemplos abaixo em TypeScript. Adapte sintaxe para Java/Python mantendo os contratos.

---

## Convenções de Nomenclatura

| Elemento | Padrão | Exemplo |
|---|---|---|
| Classe base | `<Domain>Exception` | `OrderException` |
| Categoria | `<Category><Domain>Exception` | `ValidationOrderException` |
| Folha (específica) | `<Evento>Semântico` | `InsufficientStockException` |
| Campo de contexto | `<entidade><atributo>` | `orderId`, `requestedQty` |
| Método que lança | Verbo + `OrThrow` | `findOrThrow()`, `validateOrThrow()` |

---

## Protocolo de Execução

```
ETAPA 1 — MAPEAR LIMITES E PONTOS DE FALHA
│  Caso de exceção: domínio mal delimitado → exceções vagas
│  Resiliência: se limites forem ambíguos, pare e pergunte antes de prosseguir
│
├─ 1.1 Listar bounded contexts do domínio
├─ 1.2 Para cada context, listar operações que podem falhar
├─ 1.3 Classificar cada falha: validação / estado / infra / negócio
├─ 1.4 Marcar falhas que requerem recovery vs. propagação pura
│  Saída verificável: tabela { contexto, operação, tipo de falha, recovery }
│
▼
ETAPA 2 — DEFINIR CLASSE BASE DO DOMÍNIO
│  Caso de exceção: classe base sem campos de contexto → exceções inúteis
│  Resiliência: tipo obrigatório via TypeScript `abstract` + construtor protegido
│
├─ 2.1 Criar classe base abstract com campos: code, message, context, cause, timestamp
├─ 2.2 Definir enum `ExceptionCode` com um valor por folha da hierarquia
├─ 2.3 Implementar `toPayload()` serializável para resposta de API
├─ 2.4 Implementar `toLogEntry()` com campos para observabilidade
│  Saída verificável: compila sem erro, `toPayload()` retorna objeto JSON
│
▼
ETAPA 3 — CONSTRUIR HIERARQUIA POR CATEGORIA
│  Caso de exceção: herança profunda (>3 níveis) → confusão de catch
│  Resiliência: limite de 3 níveis, cada nível com propósito distinto
│
├─ 3.1 Criar subclasses por categoria (Validation, State, Infrastructure, Business)
├─ 3.2 Para cada categoria, criar folhas semânticas com campos específicos
├─ 3.3 Garantir que `instanceof` funcione para catch por categoria E por folha
│  Saída verificável: tabela hierárquica completa, max 3 níveis
│
▼
ETAPA 4 — IMPLEMENTAR FOLHAS COM CONTRATO RICO
│  Caso de exceção: exceção sem campos específicos → diagnóstico impossível
│  Resiliência: validação de contrato em tempo de compilação (tipagem forte)
│
├─ 4.1 Cada folha define interface de contexto (type ou record)
├─ 4.2 Construtor da folha exige todos os campos de contexto
├─ 4.3 Message template usa os campos (nunca string solta)
├─ 4.4 Code enum associado à folha
│  Saída verificável: instanciar cada folha sem `any`, compila limpo
│
▼
ETAPA 5 — DOCUMENTAR CONTRATO POR MÉTODO
│  Caso de exceção: método sem `@throws` → violação de contrato implícito
│  Resiliência: JSDoc/javaDoc com @throws para cada exceção possível
│
├─ 5.1 Para cada método público, listar exceções que pode lançar
├─ 5.2 Classificar cada uma: esperada (caller deve tratar) vs. inesperada (propagar)
├─ 5.3 Marcar métodos que nunca lançam (anotação `@throws never`)
│  Saída verificável: cobertura de @throws em 100% dos métodos públicos
│
▼
ETAPA 6 — IMPLEMENTAR TRADUÇÃO NO ADAPTER
│  Caso de exceção: exceção de infra vazar para domínio → acoplamento
│  Resiliência: try-catch com tradução obrigatória, nunca propagação cruzada
│
├─ 6.1 Identificar todas as exceções de libs externas que podem ocorrer
├─ 6.2 Criar função `translateToDomain(externalError)` por adapter
├─ 6.3 Garantir que `cause` preserva a exceção original para debug
├─ 6.4 Testar: lançar cada exceção externa e verificar que sai como domain exception
│  Saída verificável: tabela { lib externa → exceção dela → domain exception }
│
▼
ETAPA 7 — IMPLEMENTAR HANDLERS POR CAMADA
│  Caso de exceção: handler genérico que loga tudo igual → ruído
│  Resiliência: handler diferencia por categoria, com ação específica
│
├─ 7.1 Adapter layer: traduz (etapa 6) + retorna erro de API formatado
├─ 7.2 Application layer: decide retry/fallback por tipo
├─ 7.3 Domain layer: lança, nunca captura (exceto para converter sub-tipo)
├─ 7.4 Infrastructure layer: implementa retry com backoff para State/Infra exceptions
│  Saída verificável: cada camada tem handler com switch por categoria
│
▼
ETAPA 8 — VALIDAR RESILIÊNCIA
│  Caso de exceção: não testar cenários de falha → exceções quebram em produção
│  Resiliência: simular cada folha e verificar comportamento end-to-end
│
├─ 8.1 Para cada folha: simular lançamento, verificar captura e ação
├─ 8.2 Para cada adapter: simular falha externa, verificar tradução
├─ 8.3 Para cada recovery: simular falha + recovery falhando, verificar fallback final
├─ 8.4 Verificar que estado pré-falha permanece íntegro após exceção
│  Saída verificável: matriz { exceção → camada que captura → ação → estado pós }
```

---

## Padrões Específicos

### Padrão 1 — Classe Base com Contrato Fechado

**Regra**: A classe base é `abstract`, não instanciável, e exige `code` + `context` no construtor.

```typescript
// ✅ PASS — contrato fechado, tipo seguro, serializável
abstract class OrderException extends Error {
  public readonly timestamp: string;
  public readonly code: OrderExceptionCode;
  public readonly context: Record<string, unknown>;

  protected constructor(
    code: OrderExceptionCode,
    message: string,
    context: Record<string, unknown>,
    cause?: Error,
  ) {
    super(message, { cause });
    this.name = this.constructor.name;
    this.code = code;
    this.context = Object.freeze({ ...context });
    this.timestamp = new Date().toISOString();
  }

  abstract toPayload(): { code: string; message: string; context: Record<string, unknown> };
}

enum OrderExceptionCode {
  INSUFFICIENT_STOCK = "ORDER.INSUFFICIENT_STOCK",
  INVALID_STATUS_TRANSITION = "ORDER.INVALID_STATUS_TRANSITION",
  PAYMENT_FAILED = "ORDER.PAYMENT_FAILED",
  ORDER_NOT_FOUND = "ORDER.NOT_FOUND",
  DUPLICATE_ORDER = "ORDER.DUPLICATE",
}

// ❌ FAIL — classe base aberta, sem código, sem contexto
class OrderException extends Error {
  constructor(message: string) {
    super(message);
  }
}
```

**Por que importa**: Sem `code`, o front-end não pode mapear erros para i18n. Sem `context`, o SRE não pode diagnosticar sem acessar logs. Sem `abstract`, alguém instancia `new OrderException("erro")` destruindo a semântica.

---

### Padrão 2 — Folha Semântica com Contexto Tipado

**Regra**: Cada folha define um tipo de contexto específico — nunca `Record<string, unknown>` genérico.

```typescript
// ✅ PASS — contexto tipado, message template, code associado
interface InsufficientStockContext {
  readonly orderId: string;
  readonly productId: string;
  readonly requestedQty: number;
  readonly availableQty: number;
}

class InsufficientStockException extends OrderException {
  constructor(ctx: InsufficientStockContext) {
    super(
      OrderExceptionCode.INSUFFICIENT_STOCK,
      `Pedido ${ctx.orderId}: solicitado ${ctx.requestedQty} do produto ${ctx.productId}, disponível ${ctx.availableQty}`,
      ctx,
    );
  }

  toPayload() {
    return { code: this.code, message: this.message, context: this.context };
  }
}

// ❌ FAIL — contexto genérico, sem campos obrigatórios
class InsufficientStockException extends OrderException {
  constructor(orderId: string, message?: string) {
    super(OrderExceptionCode.INSUFFICIENT_STOCK, message ?? "Estoque insuficiente", { orderId });
  }
  toPayload() { return { code: this.code, message: this.message, context: this.context }; }
}
```

**Por que importa**: A versão FAIL permite omitir `productId`, `requestedQty` e `availableQty` — dados essenciais para o suporte investigar sem acessar o banco.

---

### Padrão 3 — Tradução no Adapter com Causa Preservada

**Regra**: Exceções de infraestrutura são convertidas uma única vez, preservando `cause`.

```typescript
// ✅ PASS — tradução explícita, causa preservada, contexto enriquecido
function translateDbErrorToDomain(err: unknown, operation: string): OrderException {
  if (err instanceof Prisma.PrismaClientKnownRequestError) {
    if (err.code === 'P2025') {
      return new OrderNotFoundException({ operation, prismaCode: err.code });
    }
    if (err.code === 'P2002') {
      const target = (err.meta?.target as string[])?.join(', ') ?? 'unknown';
      return new DuplicateOrderException({ operation, conflictingFields: target });
    }
  }
  // Falha não mapeada → exceção genérica de infra, mas COM causa
  return new OrderInfrastructureException(
    { operation, rawError: err instanceof Error ? err.message : String(err) },
    err instanceof Error ? err : undefined,
  );
}

// Uso no adapter:
try {
  return await prisma.order.create({ data: orderData });
} catch (err) {
  throw translateDbErrorToDomain(err, 'OrderRepository.create');
}

// ❌ FAIL — propagação cruzada de exceção de infra para domínio
try {
  return await prisma.order.create({ data: orderData });
} catch (err) {
  throw err; // Prisma.PrismaClientKnownRequestError vaza para o domínio
}
```

**Por que importa**: Se o ORM mudar de Prisma para Drizzle, só o adapter precisa mudar. O domínio nunca soube que Prisma existia.

---

### Padrão 4 — Handler por Camada com Ação Diferenciada

**Regra**: Cada camada captura apenas categorias que sabe tratar; o resto propaga.

```typescript
// ✅ PASS — Application layer decide retry/fallback por categoria
async function processOrder(command: ProcessOrderCommand): Promise<OrderResult> {
  try {
    return await orderService.process(command);
  } catch (err) {
    if (err instanceof ValidationOrderException) {
      // Esperada: retorna erro de validação sem retry
      return { success: false, error: err.toPayload() };
    }

    if (err instanceof StateOrderException) {
      // Estado inconsistente: loga + propaga para o adapter decidir
      logger.warn('State exception in processOrder', { context: err.context });
      throw err;
    }

    if (err instanceof InfrastructureOrderException) {
      // Infra: tenta retry uma vez antes de falhar
      logger.error('Infrastructure failure, attempting retry', { context: err.context });
      try {
        return await orderService.process(command);
      } catch (retryErr) {
        logger.error('Retry failed, escalating', { cause: retryErr });
        throw err; // propaga para adapter formatar como 503
      }
    }

    // Não é OrderException → exceção inesperada, propaga crua
    throw err;
  }
}

// ❌ FAIL — catch-all que loga e retorna erro genérico
async function processOrder(command: ProcessOrderCommand): Promise<OrderResult> {
  try {
    return await orderService.process(command);
  } catch (err) {
    logger.error('Error processing order', err);
    return { success: false, error: { code: 'INTERNAL_ERROR', message: 'Tente novamente' } };
  }
}
```

**Por que importa**: O catch-all silencia `StateOrderException` (dado corrompido!) como se fosse um erro transitório, mascara o problema real e impede investigação.

---

### Padrão 5 — Enriquecimento Progressivo ao Subir a Pilha

**Regra**: Cada camada que captura e relança adiciona contexto sem perder a causa original.

```typescript
// ✅ PASS — contexto enriquecido em cada camada, causa encadeada
// Domain layer
class OrderDomainException extends OrderException {
  constructor(ctx: { aggregateId: string; reason: string }, cause?: Error) {
    super(OrderExceptionCode.DOMAIN_ERROR, `Erro de domínio no aggregate ${ctx.aggregateId}: ${ctx.reason}`, ctx, cause);
  }
  toPayload() { return { code: this.code, message: this.message, context: this.context }; }
}

// Application layer — enriquece com use case info
try {
  await orderDomainService.cancel(orderId, reason);
} catch (err) {
  if (err instanceof OrderDomainException) {
    throw new OrderDomainException(
      { aggregateId: orderId, reason: err.context.reason, useCase: 'CancelOrder' },
      err, // causa original preservada
    );
  }
  throw err;
}

// ❌ FAIL — re-lança sem enriquecer, perde contexto da camada
try {
  await orderDomainService.cancel(orderId, reason);
} catch (err) {
  throw err; // sem useCase, sem camada que falhou
}
```

**Por que importa**: Quando o log mostra `OrderDomainException` no nível do adapter, sem enriquecimento é impossível saber se veio do `CancelOrder`, `CreateOrder` ou `UpdateShipping`.

---

### Padrão 6 — Recovery com Fallback Explícito

**Regra**: Todo retry tem fallback final — nunca retry infinito nem falha sem mensagem ao usuário.

```typescript
// ✅ PASS — retry com backoff + fallback + exceção descritiva
async function fetchPaymentStatus(paymentId: string): Promise<PaymentStatus> {
  const maxRetries = 2;
  let lastError: Error | undefined;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await paymentGateway.getStatus(paymentId);
    } catch (err) {
      lastError = err instanceof Error ? err : new Error(String(err));

      if (attempt < maxRetries) {
        await delay(Math.pow(2, attempt) * 200); // 200ms, 400ms
        continue;
      }
    }
  }

  // Fallback: consulta banco local (pode estar desatualizado, mas não falha)
  try {
    const cached = await paymentCache.get(paymentId);
    if (cached) {
      logger.warn('Payment gateway failed, using cached status', {
        paymentId,
        error: lastError?.message,
        cacheAge: cached.age,
      });
      return { ...cached, source: 'CACHE_FALLBACK' };
    }
  } catch (cacheErr) {
    // Cache também falhou — lançar com contexto total
    throw new PaymentUnavailableException(
      { paymentId, gatewayError: lastError?.message, cacheError: String(cacheErr) },
      lastError,
    );
  }

  // Sem cache e sem gateway
  throw new PaymentUnavailableException(
    { paymentId, gatewayError: lastError?.message, cacheHit: false },
    lastError,
  );
}

// ❌ FAIL — retry sem fallback, sem log intermediário
async function fetchPaymentStatus(paymentId: string): Promise<PaymentStatus> {
  for (let i = 0; i < 3; i++) {
    try { return await paymentGateway.getStatus(paymentId); }
    catch { continue; }
  }
  throw new Error('Payment service unavailable'); // sem contexto, sem causa, sem fallback
}
```

**Por que importa**: O FAIL silencia todos os erros intermediários (sem log), descarta a causa original e não tenta alternativa — o usuário vê "500 Internal Server Error" sem nenhuma informação acionável.

---

## Anti-Padrões Críticos

| Anti-padrão | Consequência | Alternativa correta |
|---|---|---|
| `catch (e) { console.log(e) }` sem ação | Falha silenciada, estado inconsistente undetectado | Todo catch tem retry, fallback ou `throw` enriquecido |
| `throw new Error("algo falhou")` | Semântica nula, diagnóstico impossível | Lançar folha específica da hierarquia com contexto |
| `catch (e: any)` | Bypass do type system, erros de digitação em tempo de execução | `catch (e: unknown)` + type guard (`instanceof` ou discriminante) |
| Exceção como fluxo de controle | Código ilegível, performance degradada (stack unwinding) | Usar `Result<T, E>` ou early return para casos esperados |
| Herança > 3 níveis | `instanceof` confuso, catch captura mais do que deveria | Max 3 níveis: Base → Categoria → Folha |
| Exceção sem `cause` | Perda da cadeia causal original | Sempre passar `cause` quando wrapping |
| Logar stack trace inteiro em produção | Vazamento de internals, log inchado, custo alto | Logar `toPayload()` + `cause.message`, stack trace só em DEBUG |

---

## Estrutura de Diretórios (Referência)

```
src/
├── domain/
│   └── order/
│       └── exceptions/
│           ├── OrderException.ts          ← classe base abstract
│           ├── OrderExceptionCode.ts      ← enum de códigos
│           ├── ValidationOrderException.ts ← categoria
│           │   ├── InsufficientStockException.ts
│           │   └── InvalidStatusTransitionException.ts
│           ├── StateOrderException.ts      ← categoria
│           │   └── OrderAlreadyCompletedException.ts
│           ├── BusinessOrderException.ts   ← categoria
│           │   └── PaymentDeclinedException.ts
│           └── InfrastructureOrderException.ts ← categoria
│               └── OrderNotFoundException.ts
├── application/
│   └── order/
│       └── handlers/
│           └── OrderExceptionHandler.ts   ← retry/fallback por categoria
└── infrastructure/
    └── adapters/
        └── PrismaExceptionTranslator.ts   ← infra → domínio
```

**Regra**: Nunca importar exceções de `infrastructure/` em `domain/`. A seta de dependência é unidirecional: infra conhece domínio, domínio não conhece infra.

---

## Critérios de Qualidade

Antes de entregar, confirme:

- [ ] Classe base `abstract` com `code`, `context`, `timestamp`, `cause`
- [ ] Enum de códigos com um valor por folha da hierarquia (prefixo `<DOMAIN>.`)
- [ ] Hierarquia com no máximo 3 níveis (Base → Categoria → Folha)
- [ ] Cada folha tem interface de contexto tipado (zero `any`)
- [ ] Cada folha implementa `toPayload()` retornando objeto JSON serializável
- [ ] Construtor de cada folha exige todos os campos de contexto
- [ ] Tradução de exceções externas isolada no adapter, com `cause` preservado
- [ ] Nenhuma exceção de infra importada em `domain/`
- [ ] Todo `catch` tem destino: retry, fallback ou `throw` enriquecido
- [ ] Zero `catch (e: any)` no codebase
- [ ] Handler por camada com ação diferenciada por categoria
- [ ] Recovery patterns (retry + fallback) implementados para `InfrastructureException`
- [ ] `@throws` documentado em 100% dos métodos públicos
- [ ] Matriz de resiliência preenchida: { exceção → camada → ação → estado pós }

---

## Referências Cruzadas

| Precisa de... | Use a skill... |
|---|---|
| Estrutura de camadas (clean arch, DDD) | `backend-patterns` |
| Emitir eventos de falha para observabilidade | `logging` |
| Result type em vez de exceção para casos esperados | `result-pattern` |
| Testes de cenários de falha | `testing-patterns` |
| Retry com circuit breaker completo | `resilience-patterns` |

---

## Exemplo Completo — End-to-End

### Cenário: Domínio de Pedidos, fluxo de cancelamento

```typescript
// ===== 1. CLASSE BASE =====
enum OrderExceptionCode {
  NOT_FOUND = "ORDER.NOT_FOUND",
  INSUFFICIENT_STOCK = "ORDER.INSUFFICIENT_STOCK",
  INVALID_TRANSITION = "ORDER.INVALID_TRANSITION",
  ALREADY_CANCELLED = "ORDER.ALREADY_CANCELLED",
  PAYMENT_REFUND_FAILED = "ORDER.PAYMENT_REFUND_FAILED",
  INFRASTRUCTURE = "ORDER.INFRASTRUCTURE",
}

abstract class OrderException extends Error {
  constructor(
    public readonly code: OrderExceptionCode,
    message: string,
    public readonly context: Record<string, unknown>,
    cause?: Error,
  ) {
    super(message, { cause });
    this.name = this.constructor.name;
  }
  abstract toPayload(): { code: string; message: string; context: Record<string, unknown> };
}

// ===== 2. CATEGORIAS =====
abstract class ValidationOrderException extends OrderException {
  protected constructor(code: OrderExceptionCode, message: string, ctx: Record<string, unknown>, cause?: Error) {
    super(code, message, ctx, cause);
  }
}

abstract class StateOrderException extends OrderException {
  protected constructor(code: OrderExceptionCode, message: string, ctx: Record<string, unknown>, cause?: Error) {
    super(code, message, ctx, cause);
  }
}

abstract class InfrastructureOrderException extends OrderException {
  protected constructor(code: OrderExceptionCode, message: string, ctx: Record<string, unknown>, cause?: Error) {
    super(code, message, ctx, cause);
  }
}

// ===== 3. FOLHAS =====
class OrderNotFoundException extends InfrastructureOrderException {
  constructor(ctx: { orderId: string; operation: string }, cause?: Error) {
    super(OrderExceptionCode.NOT_FOUND, `Pedido ${ctx.orderId} não encontrado em ${ctx.operation}`, ctx, cause);
  }
  toPayload() { return { code: this.code, message: this.message, context: this.context }; }
}

class InvalidStatusTransitionException extends StateOrderException {
  constructor(ctx: { orderId: string; from: string; to: string; allowed: string[] }) {
    super(
      OrderExceptionCode.INVALID_TRANSITION,
      `Pedido ${ctx.orderId}: transição "${ctx.from}" → "${ctx.to}" invália. Permitidas: [${ctx.allowed.join(', ')}]`,
      ctx,
    );
  }
  toPayload() { return { code: this.code, message: this.message, context: this.context }; }
}

class AlreadyCancelledException extends StateOrderException {
  constructor(ctx: { orderId: string; cancelledAt: string }) {
    super(OrderExceptionCode.ALREADY_CANCELLED, `Pedido ${ctx.orderId} já cancelado em ${ctx.cancelledAt}`, ctx);
  }
  toPayload() { return { code: this.code, message: this.message, context: this.context }; }
}

class PaymentRefundFailedException extends InfrastructureOrderException {
  constructor(ctx: { orderId: string; paymentId: string; refundAmount: number; gatewayError: string }, cause?: Error) {
    super(OrderExceptionCode.PAYMENT_REFUND_FAILED, `Reembolso de ${ctx.refundAmount} falhou para pagamento ${ctx.paymentId}`, ctx, cause);
  }
  toPayload() { return { code: this.code, message: this.message, context: this.context }; }
}

// ===== 4. DOMÍNIO — lança, nunca captura =====
class OrderAggregate {
  private constructor(
    public readonly id: string,
    public readonly status: OrderStatus,
    public readonly cancelledAt: string | null,
    // ...
  ) {}

  static readonly ALLOWED_TRANSITIONS: Record<string, string[]> = {
    PENDING: ['CONFIRMED', 'CANCELLED'],
    CONFIRMED: ['SHIPPED', 'CANCELLED'],
    SHIPPED: ['DELIVERED'],
    DELIVERED: [],
    CANCELLED: [],
  };

  /** @throws InvalidStatusTransitionException se transição não for permitida */
  /** @throws AlreadyCancelledException se pedido já estiver cancelado */
  requestCancellation(reason: string): void {
    if (this.status === 'CANCELLED') {
      throw new AlreadyCancelledException({ orderId: this.id, cancelledAt: this.cancelledAt! });
    }
    const allowed = OrderAggregate.ALLOWED_TRANSITIONS[this.status] ?? [];
    if (!allowed.includes('CANCELLED')) {
      throw new InvalidStatusTransitionException({
        orderId: this.id, from: this.status, to: 'CANCELLED', allowed,
      });
    }
    // validação passou — transição é segura
  }
}

// ===== 5. APPLICATION — retry/fallback por categoria =====
async function cancelOrderUseCase(orderId: string, reason: string): Promise<CancelOrderResult> {
  try {
    // Busca aggregate
    const order = await orderRepo.findById(orderId);
    if (!order) {
      throw new OrderNotFoundException({ orderId, operation: 'cancelOrderUseCase' });
    }

    // Validação de domínio
    order.requestCancellation(reason);

    // Estorno de pagamento — ponto de infra com recovery
    const payment = await paymentRepo.findByOrderId(orderId);
    try {
      await paymentGateway.refund(payment.id, payment.amount);
    } catch (gwErr) {
      // Retry uma vez com backoff
      await delay(500);
      try {
        await paymentGateway.refund(payment.id, payment.amount);
      } catch (retryErr) {
        throw new PaymentRefundFailedException({
          orderId, paymentId: payment.id, refundAmount: payment.amount,
          gatewayError: retryErr instanceof Error ? retryErr.message : String(retryErr),
        }, retryErr instanceof Error ? retryErr : undefined);
      }
    }

    // Se chegou aqui: tudo ok, persiste
    await orderRepo.updateStatus(orderId, 'CANCELLED', reason);
    return { success: true };
  } catch (err) {
    if (err instanceof ValidationOrderException || err instanceof StateOrderException) {
      // Esperada: retorna para o adapter formatar como 4xx
      return { success: false, error: err.toPayload() };
    }
    if (err instanceof InfrastructureOrderException) {
      // Infra: propaga para o adapter decidir (5xx + alerta)
      logger.error('Infrastructure failure in cancelOrder', { payload: err.toPayload() });
      throw err;
    }
    // Inesperada: propaga crua
    throw err;
  }
}

// ===== 6. ADAPTER — tradução e formatação final =====
async function cancelOrderHandler(req: Request, res: Response): Promise<void> {
  try {
    const result = await cancelOrderUseCase(req.params.orderId, req.body.reason);
    if (result.success) {
      res.json({ success: true });
    } else {
      res.status(400).json(result.error); // Validation/State → 400
    }
  } catch (err) {
    if (err instanceof InfrastructureOrderException) {
      res.status(503).json({
        code: err.code,
        message: 'Serviço temporariamente indisponível. Tente novamente em instantes.',
        referenceId: req.id, // para o usuário referenciar no suporte
      });
      alertOps('ORDER_INFRA_FAILURE', err.toPayload()); // pagerduty/slack
      return;
    }
    res.status(500).json({ code: 'INTERNAL', message: 'Erro interno inesperado' });
    logger.error('Unexpected error in cancelOrderHandler', { error: err });
  }
}
```

### Matriz de Resiliência — CancelOrder

| Exceção lançada | Camada que captura | Ação | Estado pós-falha |
|---|---|---|---|
| `OrderNotFoundException` | Application | Retorna 400 com payload | Pedido inexistente, nada mutado |
| `AlreadyCancelledException` | Application | Retorna 400 com payload | Pedido já cancelado, nada mutado |
| `InvalidStatusTransitionException` | Application | Retorna 400 com payload | Pedido em estado inválido para cancelamento, nada mutado |
| `PaymentRefundFailedException` (1ª tentativa) | Application | Retry com 500ms backoff | Pagamento não estornado ainda |
| `PaymentRefundFailedException` (2ª tentativa) | Application | Lança para Adapter | Pagamento não estornado, pedido NÃO cancelado |
| `PaymentRefundFailedException` | Adapter | Retorna 503 + alerta Ops | Pedido NÃO cancelado, estado consistente |
| `Error` inesperada (bug) | Adapter | Retorna 500 genérico + log | Indeterminado — requer investigação |

**Nota sobre consistência**: O estorno é tentado *antes* do `updateStatus`. Se o estorno falha, o status do pedido nunca muda — estado permanece íntegro. Esta é a aplicação do princípio "Estado inalterado em falha".
```

---

**Racional das escolhas**: Esta skill foca em **exceções como contrato de domínio**, não como mecanismo de linguagem. A decisão de exigir `abstract` na base, `context` tipado em cada folha e tradução única no adapter elimina as 3 fontes mais comuns de degradação em sistemas de erro: (1) exceções genéricas sem diagnóstico, (2) vazamento de acoplamento de infra para domínio, e (3) captura silenciosa que mascara falhas. A matriz de resiliência ao final garante que cada exceção tem destino conhecido antes de ir para produção.

**Sugestão de salvamento**: `/docs/domain-exception-hierarchy/SKILL.md`

**Complementa**: `backend-patterns` (estrutura de camadas), `logging` (emissão dos eventos), `resilience-patterns` (circuit breaker avançado).