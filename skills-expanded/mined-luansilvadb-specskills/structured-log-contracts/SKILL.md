---
name: structured-log-contracts
version: 1.0.0
description: >
  Define e implementa contratos de log estruturado (JSON) garantindo rastreabilidade
  ponta-a-ponta, resiliência contra falhas de serialização e isolamento total de
  side-effects. Foco em código de infraestrutura de observabilidade.
triggers:
  - "criar log estruturado"
  - "contrato de log"
  - "rastreabilidade de falhas"
  - "structured logging"
  - "correlation id no log"
  - "log que não quebra a aplicação"
---

# STRUCTURED LOG CONTRACTS — Logs à prova de falhas e rastreáveis por contrato

> **Propósito**: Garantir que toda exceção ou estado anômalo seja emitido como JSON imutável com identificadores de correlação, sem que a falha no processo de logging quebre ou degrade o fluxo principal da aplicação.

---

## Filosofia Central

1. **Contratos Imutáveis** — O shape do JSON de erro nunca varia por contexto.
   Na prática: use Zod/Pydantic/Interfaces rígidas; falha de validação descarta o log, nunca o adapta.
2. **Isolamento de Side-Effects** — O log nunca deve lançar exceção no fluxo de negócio.
   Na prática: a função de log possui `try/catch` infinito; se falhar, falha silenciosamente para `stderr` bruto.
3. **Propagação por Contexto** — `trace_id` não é parâmetro de função, é estado implicitamente propagado.
   Na prática: use `AsyncLocalStorage` (Node) ou `ContextVar` (Python) injetados no primeiro middleware.
4. **Omissão Consciente** — Dados sensíveis ou payloads massivos são retirados antes da serialização.
   Na prática: redactors no nível do contrato cortam campos como `password`, `token` ou `body` maiores que 10KB.

---

## Quando Ativar

### ✅ Ativar para:
- Criar wrappers/facades em torno de lib de logging (Pino, Winston, Serilog, etc.)
- Definir o schema JSON padrão de erros para um microsserviço ou monólito
- Instrumentar middlewares de captura de exceção globais (Express, FastAPI)
- Implementar fallbacks de emissão quando o destino do log (stdout, Datadog) está inacessível

### ❌ NÃO ativar para:
- Configurar dashboards ou alertas no Grafana/Datadog → use infraestrutura específica
- Implementar tracing distribuído (OpenTelemetry) → use `distributed-tracing`
- Tratar erros de negócio (ex: "saldo insuficiente") → use `error-handling`

---

## Escopo e Limites

| Cobertura (O que esta skill faz) | Delegação (O que NÃO faz) |
|---|---|
| Define a interface (schema) do log | Instala ou configura agentes de coleta |
| Garante que a serialização não quebre a app | Decide o destino final (S3, ELK, Kafka) |
| Injeta/Extrai `trace_id` e `span_id` | Gera os `trace_id` (cabe ao gateway/tracer) |
| Sanitiza PII (Dados Pessoais Identificáveis) | Criptografa logs em repouso |

---

## Protocolo de Execução

1. **Definir** o schema strict do contrato (Mandatory x Optional x Forbidden).
2. **Tipar** o contrato na linguagem alvo (TypeScript `interface`/`type`, Python `dataclass`).
3. **Isolar** a função de emissão: separar a construção do payload da escrita em I/O.
4. **Implementar** o redutor de payload (truncar strings longas, remover chaves proibidas).
5. **Envolver** a escrita em I/O com `try/catch` de última instância (fallback para `process.stderr.write`).
6. **Injetar** o middleware de propagação de contexto assíncrono no entrypoint da aplicação.
7. **Testar** o caminho infeliz: simular falha de `JSON.stringify`, objeto circular e queda do stdout.

---

## Padrões Específicos

### 1. O Contrato Base (Schema)

**Regra**: O log deve conter campos obrigatórios de contexto e metadados de falha estritamente tipados, rejeitando objetos não-mapeados.

```typescript
// ✅ PASS — Contrato rígido e explícito
interface StructuredLogContract {
  // Obrigatórios
  timestamp: string; // ISO 8601
  level: 'fatal' | 'error' | 'warn' | 'info' | 'debug';
  message: string;
  service: string;
  trace_id: string | null;
  span_id: string | null;
  
  // Opcionais
  error_code?: string;
  stack_trace?: string;
  context?: Record<string, unknown>;
}

// ❌ FAIL — Tipagem frouxa aceita qualquer coisa
type BadLog = {
  [key: string]: any; // Perde rastreabilidade, admite lixo
};
```

**Por que importa**: Contratos frouxos permitem que desenvolvedores insiram formatos ad-hoc, quebrando parsers downstream e gerando "schema-less hell" no Elasticsearch/Datadog.

---

### 2. Propagação de Contexto Assíncrono

**Regra**: O `trace_id` deve ser extraído automaticamente do contexto de execução assíncrona, nunca passado manualmente pelos services.

```typescript
// ✅ PASS — Injeção via AsyncLocalStorage (Node.js)
import { AsyncLocalStorage } from 'node:async_hooks';

export const TraceContext = new AsyncLocalStorage<{ traceId: string; spanId: string }>();

export function getLoggerContext(): Pick<StructuredLogContract, 'trace_id' | 'span_id'> {
  const store = TraceContext.getStore();
  return {
    trace_id: store?.traceId ?? null,
    span_id: store?.spanId ?? null,
  };
}

// ❌ FAIL — Poluição de parâmetros em tudo
function processOrder(orderId: string, traceId: string, spanId: string) {
  // Acopla lógica de negócio a observabilidade. Escala de forma horrível.
}
```

**Por que importa**: Passar IDs manualmente resulta em falhas de rastreabilidade quando uma função profunda na pilha esquece o parâmetro.

---

### 3. Resiliência na Serialização (O escudo de isolamento)

**Regra**: A função que transforma o objeto contract em string nunca pode lançar exceção (ex: por `TypeError: Converting circular structure to JSON` ou campos `BigInt`).

```typescript
// ✅ PASS — Safe stringify com fallback definido
import safeStringify from 'fast-safe-stringify';

export function safeSerialize(payload: StructuredLogContract): string {
  try {
    // fast-safe-stringify lida com circular refs e BigInt nativamente
    return safeStringify(payload); 
  } catch (serialError) {
    // Fallback de emergência: log bruto não estruturado, mas não quebra a app
    const fallbackMsg = `[LOG_SERIALIZATION_FAILED] ${payload.level} - ${payload.message}`;
    return fallbackMsg;
  }
}

// ❌ FAIL — Confiança cega no ambiente
export function emitLog(payload: StructuredLogContract) {
  console.log(JSON.stringify(payload)); // Boom se tiver circular ref. Quebra a request do usuário.
}
```

**Por que importa**: Em sistemas de alta requisição, um erro de serialização não tratado derruba o event loop ou a thread, gerando um incidente de disponibilidade causado pela ferramenta de observabilidade.

---

### 4. Redação de PII e Limitação de Tamanho

**Regra**: Antes de entrar no contrato, o objeto `context` deve passar por um redutor que corta dados sensíveis e trunca payloads massivos (ex: base64 de imagens).

```typescript
// ✅ PASS — Sanitização defensiva
const FORBIDDEN_KEYS = ['password', 'token', 'credit_card', 'authorization'];
const MAX_STRING_LENGTH = 1024;

function sanitizeContext(context: Record<string, unknown>): Record<string, unknown> {
  const sanitized: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(context)) {
    if (FORBIDDEN_KEYS.includes(key.toLowerCase())) continue;
    
    if (typeof value === 'string' && value.length > MAX_STRING_LENGTH) {
      sanitized[key] = `${value.substring(0, MAX_STRING_LENGTH)}...[TRUNCATED]`;
    } else {
      sanitized[key] = value;
    }
  }
  return sanitized;
}

// ❌ FAIL — Log cego do request inteiro
const context = { body: req.body }; // Pode conter senha do usuário ou upload de 50MB
```

**Por que importa**: Vazar PII em logs é um vazamento de segurança. Logar payloads de megabytes causa lentidão no processo de I/O e estouro de memória do agregador de logs.

---

### 5. Fallback de I/O (Quando o destino morre)

**Regra**: Se a stream de destino do log estiver destruída ou congestionada (ex: `EPIPE` no stdout redirecionado), a aplicação NÃO pode travar.

```typescript
// ✅ PASS — Captura de erro de I/O no emitter
import process from 'node:process';

function writeToStream(data: string) {
  try {
    process.stdout.write(data + '\n');
  } catch (ioError) {
    // Último recurso. Se até o stderr falhar, ignoramos silenciosamente.
    // A regra de ouro: a observabilidade não pode matar o paciente.
    try { process.stderr.write(`[LOG_IO_FAILED] ${String(ioError)}\n`); } 
    catch (finalError) { /* Silêncio total */ }
  }
}

// ❌ FAIL — Pipe sem tratamento
process.stdout.on('error', (err) => { throw err; }); // Derruba a aplicação
```

**Por que importa**: Em orquestradores como Kubernetes, se o container runtime matar o processo de coleta de logs, os logs da aplicação geram `EPIPE`. Se a app não tratar isso, ela entra em crash loop.

---

## Anti-Padrões Críticos

| Anti-padrão | Consequência | Alternativa Correta |
|---|---|---|
| Interpolação de string no log (`Erro: ${err}`) | Quebra o JSON, dificulta parsing por ferramentas | Passar `err` inteiro no campo `context` ou `stack_trace` |
| `console.log` misturado com `logger.error` | Perda de `trace_id`, poluição de formato | Proibir `console.*` via ESLint (`no-console`) |
| Logar o request/response HTTP inteiro | Vazamento de headers sensíveis, logs gigantes | Sanitizar headers (remover Auth) e truncar body |
| Usar log síncrono bloqueante (ex: `fs.appendFileSync`) | Bloqueia a thread/event loop, degrada performance | Usar streams assíncronas ou bibliotecas non-blocking |
| Lançar erro dentro do Error Mapper | Disfarça o erro original, gera loop de exceção | Retornar objeto de fallback "Unmapped Error" |

---

## Critérios de Qualidade

Antes de finalizar o build do artefato de logging, confirme:

- [ ] O contrato está definido como tipagem rígida (`interface`/`type`/`zod`).
- [ ] `trace_id` é populado via contexto assíncrono, nunca por parâmetro manual.
- [ ] A função de serialização possui `try/catch` com fallback para string bruta.
- [ ] A escrita em disco/stream possui tratamento para `EPIPE` e erros de I/O.
- [ ] Existe um utilitário de sanitização ativo no payload de entrada.
- [ ] Nenhum `console.log/warn/error` é usado diretamente no código de negócio.
- [ ] Testes unitários cobrem: objeto circular, campo `BigInt`, stream morta.
- [ ] Comprimento total do módulo de log: < 150 linhas (lógica delegada, não reescrita).

---

## Referências Cruzadas

| Precisa de... | Use a skill... |
|---|---|
| Gerar o `trace_id` e espalhar na rede | `distributed-tracing` |
| Definir o que fazer quando um erro de negócio ocorre | `error-handling` |
| Configurar OpenTelemetry no nível de infra | Documentação oficial da lib alvo |

---

## Exemplo Completo End-to-End (Build do Artefato)

Abaixo, o módulo completo em TypeScript que implementa o contrato com resiliência máxima, pronto para salvar em `src/infra/logging/StructuredLogger.ts`:

```typescript
import { AsyncLocalStorage } from 'node:async_hooks';
import process from 'node:process';

// --- 1. CONTRATO ---
type LogLevel = 'fatal' | 'error' | 'warn' | 'info' | 'debug';

interface LogContract {
  timestamp: string;
  level: LogLevel;
  message: string;
  service: string;
  trace_id: string | null;
  span_id: string | null;
  error_code?: string;
  stack_trace?: string;
  context?: Record<string, unknown>;
}

// --- 2. CONTEXTO ---
const TraceStore = new AsyncLocalStorage<{ traceId: string; spanId: string }>();

function getTrace(): Pick<LogContract, 'trace_id' | 'span_id'> {
  const s = TraceStore.getStore();
  return { trace_id: s?.traceId ?? null, span_id: s?.spanId ?? null };
}

// --- 3. SANITIZAÇÃO ---
const FORBIDDEN = new Set(['password', 'passwd', 'token', 'secret', 'authorization']);
const MAX_LEN = 1024;

function sanitize(obj: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(obj)) {
    if (FORBIDDEN.has(k.toLowerCase())) continue;
    out[k] = (typeof v === 'string' && v.length > MAX_LEN) ? `${v.slice(0, MAX_LEN)}...[TRUNCATED]` : v;
  }
  return out;
}

// --- 4. SERIALIZE (SAFE) ---
function safeStringify(obj: LogContract): string {
  try {
    // Em produção real, use 'fast-safe-stringify' aqui para lidar com 
    // erros complexos que contenham referências circulares internas.
    return JSON.stringify(obj);
  } catch {
    return `[SERIALIZATION_FAILED] level=${obj.level} msg=${obj.message}`;
  }
}

// --- 5. I/O FALLBACK ---
function writeToStdout(data: string): void {
  try {
    process.stdout.write(data + '\n');
  } catch (ioErr) {
    try { process.stderr.write(`[LOG_IO_ERROR] ${String(ioErr)}\n`); } 
    catch { /* Silêncio absoluto. A app sobrevive. */ }
  }
}

// --- 6. API PÚBLICA (O FACADE) ---
export const logger = {
  error: (message: string, ctx?: Record<string, unknown>, err?: Error) => {
    const contract: LogContract = {
      timestamp: new Date().toISOString(),
      level: 'error',
      message,
      service: process.env.SERVICE_NAME || 'unknown-service',
      ...getTrace(),
      error_code: err?.name,
      stack_trace: err?.stack,
      context: ctx ? sanitize(ctx) : undefined,
    };
    writeToStdout(safeStringify(contract));
  }
};

// --- 7. MIDDLEWARE DE INJEÇÃO (Exemplo Express) ---
export function traceMiddleware(req: any, res: any, next: () => void) {
  const traceId = req.headers['x-trace-id'] || crypto.randomUUID();
  TraceStore.run({ traceId, spanId: crypto.randomUUID() }, () => next());
}