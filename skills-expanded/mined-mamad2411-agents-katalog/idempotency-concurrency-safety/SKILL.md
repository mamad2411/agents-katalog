---
name: idempotency-concurrency-safety
version: 1.0.0
description: >
  Design de idempotência e segurança de concorrência — do recebimento da
  tarefa ao build final. Cobertura completa de race conditions, retry storms,
  double-write, deadlock e recovery em cada etapa do pipeline.
triggers:
  - "idempotência"
  - "concorrência"
  - "race condition"
  - "double write"
  - "retry storm"
  - "deadlock"
  - "lock otimista"
  - "lock pessimista"
  - "idempotency key"
  - "operações atômicas"
  - "saga pattern"
  - "outbox pattern"
  - "/idempotencia"
  - "segurança de concorrência"
---

# IDEMPOTÊNCIA & CONCORRÊNCIA — Operações seguras do request ao build

> **Propósito**: Garantir que toda operação no pipeline — desde o parse do
> request até a geração do artefato final — seja idempotente, livre de race
> conditions e recuperável de falhas parciais sem corrupção de estado.

---

## Filosofia Central

1. **Idempotência por contrato, não por acaso** — Toda mutação deve ter um
   mecanismo explícito de deduplicação. Na prática: nunca confie em
   "provavelmente não vai ser chamado duas vezes".

2. **Lock mínimo, Lock justo** — Bloqueie apenas o estritamente necessário e
   sempre com timeout. Na prática: lock pessimista para escrita conflitante,
   lock otimista para leitura-then-escrita com baixa contenção.

3. **Falha parcial é a regra, não a exceção** — Toda etapa intermediária pode
   falhar após committed parcialmente. Na prática:设计了 para rollback ou
   compensação em cada boundary transacional.

4. **Retry é perigoso sem idempotência** — Todo mecanismo de retry pressupõe
   que a operação pode ser re-executada com segurança. Na prática: se não
   tiver idempotency key, não adicione retry automático.

5. **Visibilidade antes de consistência** — Em sistemas distribuídos, é melhor
   mostrar "processando" com garantia de eventual consistência do que falhar
   silenciosamente. Na prática: status machine explícita por operação.

6. **Teste o caos, não o caminho feliz** — Race conditions se manifestam sob
   carga e falhas, não em testes unitários sequenciais. Na prática: toda
   operação crítica deve ter teste de concorrência simulada.

---

## Quando Ativar

### ✅ Ativar para:
- Design de endpoints que mutam estado (POST/PUT/PATCH/DELETE)
- Implementação de filas, workers e processamento assíncrono
- Geração de artefatos com etapas intermediárias (builds, exports, reports)
- Migrações que alteram dados existentes
- Integrações com sistemas externos que podem timeout ou responder 5xx
- Qualquer operação com side-effect não reversível

### ❌ NÃO ativar para:
- Leitura pura sem side-effects → responda diretamente
- Design de schema inicial → use `database-design`
- Retry policy genérica → use `error-handling`
- Estratégia de cache → use `caching-strategy`

---

## Escopo e Limites

### Coberto por esta skill:
| Camada | O que cobrimos |
|--------|---------------|
| **Recebimento** | Deduplicação no gateway, idempotency key validation |
| **Parse/Validation** | Estado imutável durante validação, reject rápido |
| **Business Logic** | Lock strategies, transações, saga/outbox |
| **Persistência** | Double-write prevention, optimistic/pessimistic locking |
| **Build/Geração** | Checkpointing, atomic swap, partial recovery |
| **Pós-build** | Cleanup idempotente, notificação deduplicada |

### Delegado para outras skills:
| Concern | Skill |
|---------|-------|
| Schema de tabelas de idempotência | `database-design` |
| Circuit breaker e retry config | `error-handling` |
| Logging estruturado de falhas | `observability` |
| Auth/authorization | `auth-patterns` |

---

## Pipeline de Etapas — Mapa de Riscos

```
REQUEST RECEBIDO
    │
    ├─[RISCO] request duplicado por retry do cliente
    │   → IDEMPOTENCY KEY CHECK (Etapa 1)
    │
    ▼
VALIDAÇÃO DE INPUT
    │
    ├─[RISCO] TOCTOU entre validar e processar
    │   → VALIDATE-THEN-LOCK pattern (Etapa 2)
    │
    ▼
BUSINESS LOGIC + PERSISTÊNCIA
    │
    ├─[RISCO] race condition entre requests simultâneos
    ├─[RISCO] double-write em múltiplas tabelas/sockets
    ├─[RISCO] deadlock entre locks adquiridos fora de ordem
    │   → LOCK STRATEGY + TRANSACTION BOUNDARY (Etapa 3)
    │   → SAGA/OUTBOX para cross-boundary (Etapa 4)
    │
    ▼
BUILD / GERAÇÃO DE ARTEFATO
    │
    ├─[RISCO] falha parcial deixando artefato corrompido
    ├─[RISCO] disco cheio no meio do build
    ├─[RISCO] processo morto deixando temp files
    │   → CHECKPOINT + ATOMIC SWAP (Etapa 5)
    │
    ▼
PÓS-BUILD / NOTIFICAÇÃO
    │
    ├─[RISCO] notificar antes do commit confirmado
    ├─[RISCO] enviar notificação duplicada em retry
    │   → NOTIFICATION AFTER CONFIRMED STATE (Etapa 6)
    │
    ▼
DONE
```

---

## Protocolo de Execução

### Etapa 1 — Idempotency Key Check (Recepção)

1. **Extrair** idempotency key do header (`Idempotency-Key`) ou do body
   (`idempotency_key`). Se ausente em operação POST, retornar `422` com
   mensagem explicativa — nunca processe sem key.

2. **Validar** formato do key: deve ser UUID v4 ou hash determinístico dos
   parâmetros da operação. Rejeitar keys com formato inválido (`400`).

3. **Consultar** tabela de idempotência em transação de leitura:
   - **FOUND + status=COMPLETED** → retornar resposta cacheada (`200`/`201`)
   - **FOUND + status=PROCESSING** → retornar `409 Conflict` com header
     `Retry-After: 30`
   - **FOUND + status=FAILED** → permitir re-processamento (incrementar
     attempt_count, verificar max_attempts)
   - **NOT FOUND** → inserir registro com status=PROCESSING, prosseguir

4. **Timestampar** `started_at` e calcular `expires_at = now() + TTL`.
   Se key expirada, tratar como NOT FOUND (re-processar).

**Critério de conclusão**: Registro de idempotência criado ou resposta
cacheada retornada. Zero processamento de negócio antes deste ponto.

---

### Etapa 2 — Validate-Then-Lock

1. **Validar** input completo (schema, regras de negócio, permissões) **antes**
   de adquirir qualquer lock.

2. **Nunca** adquirir lock dentro de validação — validação não deve tocar
   em estado mutável.

3. **Após validação passar**, adquirir lock na ordem canônica (ver §Padrões)
   antes de qualquer leitura de estado para decisão de negócio.

4. **Se lock falhar** (timeout ou deadlock), retornar `409 Conflict` com
   `Retry-After` calculado. Nunca retry automaticamente no request path.

**Critério de conclusão**: Input validado + lock adquirido, ou resposta de
erro retornada sem side-effects.

---

### Etapa 3 — Lock Strategy + Transaction Boundary

1. **Escolher** estratégia baseada na análise de contenção:

   | Contenção esperada | Lock recomendado | Justificativa |
   |-------------------|-----------------|---------------|
   | Baixa (< 5% conflito) | Otimista (version column) | Sem bloqueio, retry barato |
   | Média (5-30% conflito) | Otimista com retry limit | Balanceia throughput |
   | Alta (> 30% conflito) | Pessimista (SELECT FOR UPDATE) | Evita thundering herd |
   | Cross-resource | Saga com compensação | Não existe lock distribuído perfeito |

2. **Definir** boundary transacional: todas as escritas que devem ser
   atômicas ficam dentro da mesma transação. Tudo fora é saga territory.

3. **Adquirir locks em ordem canônica**: estabelecer uma ordenação global
   (ex: por resource_id) e sempre adquirir nessa ordem. Nunca adquirir lock A
   depois de B em um path e B depois de A em outro.

4. **Configurar** timeout de lock: `LOCK_TIMEOUT = 5s` para pessimista,
   `OPTIMISTIC_RETRY_LIMIT = 3` para otimista.

5. **Em caso de VersionMismatchError (otimista)**: retry automático até o
   limite, depois `409 Conflict`.

6. **Em caso de deadlock detectado**: logar os locks envolvidos, abortar
   transação, retornar `409` — nunca tentar resolver programaticamente.

**Critério de conclusão**: Transação committed com todas as mutações
atómicas, ou rollback completo sem estado residual.

---

### Etapa 4 — Saga / Outbox para Cross-Boundary

1. **Identificar** boundary transacional: se a operação toca banco + fila +
   API externa, não existe transação que cubra todos.

2. **Para mensagem/fila**: usar **Outbox Pattern** — escrever evento na tabela
   `outbox_events` dentro da mesma transação do estado de negócio. Poller
   separado lê e publica.

3. **Para API externa**: usar **Saga Pattern** com steps compensatórios:

   ```
   Step 1: Reserve estoque (DB)     → Compensação: Libera estoque
   Step 2: Cobrar pagamento (API)   → Compensação: Estorna pagamento
   Step 3: Criar pedido (DB)        → Compensação: Cancela pedido
   ```

4. **Cada step** deve ter: `execute()`, `compensate()`, e um `timeout`.
   Se step N falhar, executar compensate de N-1 até 1 em ordem reversa.

5. **Registrar** saga state em tabela dedicada com columns:
   `saga_id, step_number, step_status, payload, created_at, updated_at`.

6. **Saga recovery**: job periódico escaneia sagas com `step_status=PENDING`
   e `updated_at < now() - timeout` para retomar ou compensar.

**Critério de conclusão**: Todos os steps executados com sucesso OU todos os
steps compensados, com estado final explícito na tabela de saga.

---

### Etapa 5 — Checkpoint + Atomic Swap (Build)

1. **Criar** diretório de build com nome determinístico:
   `/tmp/builds/{operation_id}/{attempt_number}/`

2. **Checkpoint** após cada etapa significativa do build: escrever arquivo
   `.checkpoint-N` com hash dos outputs parciais.

3. **Em retomada de build falho**: ler último checkpoint válido, verificar
   integridade (hash), continuar dali. Nunca reprocessar etapas já
   checkpointadas.

4. **Never write to final destination during build** — todo output vai para
   diretório temporário.

5. **Atomic swap** quando build completa:
   ```bash
   # ✅ PASS — atômico no mesmo filesystem
   mv /tmp/builds/{id}/output /final/destination/{artifact}
   
   # ❌ FAIL — cp não é atômico, pode deixar arquivo parcial
   cp /tmp/builds/{id}/output /final/destination/{artifact}
   ```

6. **Se atomic swap não for possível** (cross-filesystem): usar rename
   temporário + sync:
   ```bash
   cp --reflink=auto /tmp/builds/{id}/output /final/destination/{artifact}.tmp
   sync  # força flush para disco
   mv /final/destination/{artifact}.tmp /final/destination/{artifact}
   ```

7. **Cleanup idempotente**: após swap confirmado, deletar diretório temp.
   Se cleanup falhar, nunca abortar — marcar para cleanup async.
   Cleanup job deve verificar: diretório `started_at > 24h` antes de deletar.

8. **Disco cheio mid-build**: detectar erro de write, abortar build,
   liberar recursos parciais, atualizar status para `FAILED`,
   retornar `507 Insufficient Storage`.

**Critério de conclusão**: Artefato no destino final via atomic swap,
diretório temp limpo, status de idempotência atualizado para COMPLETED.

---

### Etapa 6 — Notification After Confirmed State

1. **Ler** estado confirmado do banco (dentro de nova transação de leitura).
   Nunca usar variável in-memory como fonte de verdade para notificação.

2. **Deduplicar** notificação: tabela `sent_notifications` com
   `(operation_id, channel, recipient)` como unique constraint.

3. **INSERT com ON CONFLICT DO NOTHING**: se notificação já foi enviada,
   não reenviar mesmo em retry de saga.

4. **Se notificação falhar**: não compensar a operação principal —
   notificação é side-effect tolerável. Marcar como `PENDING` para retry
   async.

5. **Atualizar** registro de idempotência: `status = COMPLETED`,
   `response_cache = JSON da resposta`, `completed_at = now()`.

**Critério de conclusão**: Notificação deduplicada enviada (ou pendente para
retry async), registro de idempotência em COMPLETED com cache de resposta.

---

## Padrões Específicos

### P1. Idempotency Key — Tabela e Query

**Regra**: Toda tabela de idempotência deve ter unique constraint no key e
trabalhar com transação serializable para evitar TOCTOU.

```sql
-- ✅ PASS — transação serializable previne TOCTOU
BEGIN ISOLATION LEVEL SERIALIZABLE;

INSERT INTO idempotency_store (idempotency_key, status, request_hash, started_at, expires_at)
VALUES ($1, 'PROCESSING', $2, now(), now() + interval '24 hours')
ON CONFLICT (idempotency_key) DO NOTHING
RETURNING id, status;

-- Se RETURNING vazio: key já existe, fazer SELECT para pegar status
SELECT status, response_cache FROM idempotency_store
WHERE idempotency_key = $1 AND expires_at > now();

COMMIT;

-- ❌ FAIL — SELECT depois INSERT sem transação adequada = TOCTOU
SELECT status FROM idempotency_store WHERE idempotency_key = $1;
-- (gap: outro request pode inserir entre SELECT e INSERT)
INSERT INTO idempotency_store (idempotency_key, status, ...)
VALUES ($1, 'PROCESSING', ...);
```

**Por que importa**: Sem serializable, dois requests simultâneos com o mesmo
key podem ambos ver "não existe" e ambos prosseguir, causando double-processing.

---

### P2. Lock Otimista — Version Column

**Regra**: Toda tabela sujeita a read-then-write deve ter `version integer
DEFAULT 1` incrementada via `WHERE version = $expected`.

```sql
-- ✅ PASS — version check no UPDATE, retorna rows_affected
UPDATE accounts
SET balance = balance - 100, version = version + 1
WHERE id = $1 AND version = $expected_version;

-- rows_affected = 0 → alguém modificou antes → VersionMismatchError
-- rows_affected = 1 → sucesso, novo version = expected_version + 1

-- ❌ FAIL — ler sem versionar, escrever sem checar
balance = SELECT balance FROM accounts WHERE id = $1;
UPDATE accounts SET balance = balance - 100 WHERE id = $1;
-- (outro request pode ter mudado o balance entre as duas linhas)
```

**Por que importa**: Sem version check, a segunda escrita sobrescreve a
primeira baseada em estado stale — perda de atualização.

---

### P3. Lock Pessimista — FOR UPDATE com Ordenação

**Regra**: `SELECT FOR UPDATE` deve sempre filtrar por PK e seguir ordem
canônica de aquisição.

```sql
-- ✅ PASS — lock por PK em ordem canônica (menor ID primeiro)
BEGIN;
SELECT id, balance FROM accounts
WHERE id IN ($1, $2)
ORDER BY id
FOR UPDATE;

-- Processar transferência...
UPDATE accounts SET balance = balance - 100 WHERE id = $1;
UPDATE accounts SET balance = balance + 100 WHERE id = $2;
COMMIT;

-- ❌ FAIL — lock sem ORDER BY = deadlock potencial
-- Request A: SELECT FOR UPDATE WHERE id IN (1, 2) → locka 1 depois 2
-- Request B: SELECT FOR UPDATE WHERE id IN (2, 1) → locka 2 depois 1
-- → DEADLOCK: A espera por 2 (preso por B), B espera por 1 (preso por A)
```

**Por que importa**: Deadlocks ocorrem quando duas transações adquirem
locks em ordens diferentes sobre os mesmos recursos. Ordem canônica elimina
isso matematicamente.

---

### P4. Double-Write Prevention — Outbox

**Regra**: Nunca escrever em banco E em fila separadamente. Tudo passa pela
tabela de outbox na mesma transação.

```python
# ✅ PASS — outbox na mesma transação
async def create_order(data: OrderData) -> Order:
    async with db.transaction():
        order = await db.insert(
            "INSERT INTO orders (user_id, total, status) VALUES ($1, $2, 'CREATED')",
            data.user_id, data.total
        )
        
        await db.insert(
            """INSERT INTO outbox_events (aggregate_type, aggregate_id, event_type, payload, created_at)
               VALUES ('order', $1, 'ORDER_CREATED', $2, now())""",
            order.id, json.dumps({"order_id": order.id, "total": data.total})
        )
        
        return order
    # Poller separado lê outbox e publica na fila — eventualmente consistente

# ❌ FAIL — escritas separadas = inconsistência se segunda falhar
async def create_order_bad(data: OrderData) -> Order:
    order = await db.insert("INSERT INTO orders ...", ...)
    # Se esta linha falhar: pedido existe no banco mas evento nunca publicado
    await queue.publish("order.created", {"order_id": order.id})
    return order
```

**Por que importa**: Se a publicação na fila falha após o commit do banco,
o downstream nunca sabe que o pedido foi criado. Outbox garante que evento
e estado estão sempre em sync transacional.

---

### P5. Saga Step com Compensação

**Regra**: Cada step de saga deve ser autonomamente compensável e ter
timeout independente.

```python
# ✅ PASS — step com compensate e timeout explícitos
@dataclass
class SagaStep:
    name: str
    execute: Callable[[], Awaitable[None]]
    compensate: Callable[[], Awaitable[None]]
    timeout_seconds: int

reserve_stock = SagaStep(
    name="reserve_stock",
    execute=lambda: db.execute(
        "UPDATE inventory SET reserved = reserved + $1 WHERE sku = $2",
        qty, sku
    ),
    compensate=lambda: db.execute(
        "UPDATE inventory SET reserved = reserved - $1 WHERE sku = $2",
        qty, sku
    ),
    timeout_seconds=10
)

charge_payment = SagaStep(
    name="charge_payment",
    execute=lambda: payment_gateway.charge(amount, token),
    compensate=lambda: payment_gateway.refund(charge_id),
    timeout_seconds=30  # gateway pode ser lento
)

# ❌ FAIL — step sem compensação
create_shipment = SagaStep(
    name="create_shipment",
    execute=lambda: shipping_api.create_label(order_id),
    compensate=lambda: logger.error("Não consigo desfazer envio!")  # NÃO é compensação
)
```

**Por que importa**: Se um step não tem compensação real, a saga não pode
garantir consistência — ficará em estado permanentemente "meio-feito".

---

### P6. Build Checkpoint

**Regra**: Cada checkpoint deve conter hash de verificação dos outputs
parciais para detectar corrupção.

```python
# ✅ PASS — checkpoint com hash de verificação
CHECKPOINT_DIR = Path(f"/tmp/builds/{operation_id}/{attempt}")

def checkpoint(step: int, files: list[Path]) -> None:
    checksums = {}
    for f in files:
        checksums[f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
    
    checkpoint_file = CHECKPOINT_DIR / f".checkpoint-{step}"
    checkpoint_file.write_text(json.dumps({
        "step": step,
        "timestamp": time.time(),
        "files": checksums
    }))

def resume_from_checkpoint() -> int | None:
    for step in range(10, 0, -1):  # do mais recente para o mais antigo
        cp = CHECKPOINT_DIR / f".checkpoint-{step}"
        if not cp.exists():
            continue
        data = json.loads(cp.read_text())
        # Verificar integridade dos files listados
        for name, expected_hash in data["files"].items():
            actual = hashlib.sha256((CHECKPOINT_DIR / name).read_bytes()).hexdigest()
            if actual != expected_hash:
                logger.error(f"Checkpoint {step} corrompido: {name}")
                return None  # restart from scratch
        return step
    return None

# ❌ FAIL — checkpoint sem verificação
def checkpoint_bad(step: int) -> None:
    open(f"/tmp/builds/{id}/.done-{step}", "w").close()  # arquivo vazio
    # Se o build corrompeu os outputs antes deste ponto, retomada vai falhar silenciosamente
```

**Por que importa**: Sem verificação de hash, um build retomado de checkpoint
pode produzir artefato corrompido — o checkpoint indica "etapa OK" mas os
dados estão quebrados.

---

### P7. Atomic Swap de Artefato

**Regra**: O artefato final só aparece no destino quando 100% completo.
Nunca escrever incrementalmente no destino final.

```bash
# ✅ PASS — mv é atômico no mesmo filesystem (mesma partição)
BUILD_OUTPUT="/tmp/builds/abc123/output.pdf"
FINAL_DEST="/storage/reports/report-2024-001.pdf"

mv "$BUILD_OUTPUT" "$FINAL_DEST"
# Se mv falhar: ou ficou no source, ou chegou no dest — nunca metade dos dois

# ✅ PASS — cross-filesystem com rename seguro
cp --reflink=auto "$BUILD_OUTPUT" "$FINAL_DEST.tmp"
sync
mv "$FINAL_DEST.tmp" "$FINAL_DEST"
# Se cp falha: .tmp não existe, dest original intacto
# Se sync falha: dados em buffer, mas .tmp existe — retry safe
# Se mv falha: .tmp existe, dest original intacto

# ❌ FAIL — escrita incremental no destino
echo "writing report..." > "/storage/reports/report-2024-001.pdf"
# Processo morre aqui → arquivo truncado no destino → downstream lê lixo
python generate_and_append.py >> "/storage/reports/report-2024-001.pdf"
```

**Por que importa**: Arquivo parcial no destino é indistinguível de arquivo
completo para consumers que pollam o diretório. Atomic swap é a única
garantia de all-or-nothing.

---

### P8. Notificação Deduplicada

**Regra**: Notificação deve ser idempotente no nível de persistência, não
apenas no nível de lógica.

```sql
-- ✅ PASS — ON CONFLICT DO NOTHING como garantia de deduplicação
INSERT INTO sent_notifications (operation_id, channel, recipient, payload, sent_at)
VALUES ($1, 'email', $2, $3, now())
ON CONFLICT (operation_id, channel, recipient) DO NOTHING
RETURNING id;

-- Se RETURNING tem id: notificar agora
-- Se RETURNING vazio: já notificado, skip silenciosamente

-- ❌ FAIL — checagem em memória sem persistência
if operation_id not in already_notified_set:  # set in-memory
    send_email(recipient, payload)
    already_notified_set.add(operation_id)
# Em retry/restart, set está vazio → notificação duplicada
```

**Por que importa**: Em processos que podem restart (deploy, crash, retry),
estado em memória é perdido. Deduplicação só é real se for persistida.

---

## Anti-Padrões Críticos

| Anti-padrão | Consequência | Alternativa correta |
|---|---|---|
| Processar sem idempotency key | Double-processing em retry de cliente ou network glitch | Rejeitar 422 se key ausente em mutação |
| SELECT depois INSERT sem transação adequada | TOCTOU: dois requests passam pela checagem | SERIALIZABLE ou advisory lock |
| Lock em ordem não-canônica | Deadlock sob carga concorrente | ORDER BY id/resource_id em todo FOR UPDATE |
| Escrever no destino final durante build | Artefato parcial visível para consumers | Build em tmp + atomic swap |
| Compensação que "loga e ignora" | Saga em estado permanente de inconsistência | Compensação real que reverte side-effect |
| Retry automático sem backoff exponencial | Retry storm derruba serviço degradado | Exponential backoff + jitter + circuit breaker |
| Notificação antes de commit confirmado | Notifica sucesso mas operação foi rollbacked | Ler estado confirmado em nova transação |
| Cleanup que falha e aborta operação | Build completo mas response 500 por falha de rm | Cleanup é best-effort, nunca bloqueia success |
| Timeout de lock muito alto (60s+) | Recursos presos por minutos sob deadlock | Lock timeout ≤ 5s + retry com backoff |
| Usar NOW() como idempotency key | Mesmo segundo = mesma key = colisão acidental | UUID v4 ou hash(SHA256 dos params) |

---

## Tabelas de Schema Obrigatórias

### idempotency_store

```sql
CREATE TABLE idempotency_store (
    idempotency_key  TEXT PRIMARY KEY,
    status           TEXT NOT NULL CHECK (status IN ('PROCESSING', 'COMPLETED', 'FAILED')),
    request_hash     TEXT NOT NULL,          -- SHA256 do body para detectar mudança de params
    response_cache   JSONB,                 -- resposta completa para retorno em cache hit
    attempt_count    INT NOT NULL DEFAULT 1,
    max_attempts     INT NOT NULL DEFAULT 5,
    started_at       TIMESTAMPTZ NOT NULL,
    completed_at     TIMESTAMPTZ,
    expires_at       TIMESTAMPTZ NOT NULL,
    
    CONSTRAINT valid_status_transition CHECK (
        -- FAILED pode virar PROCESSING (retry)
        -- PROCESSING pode virar COMPLETED ou FAILED
        -- COMPLETED é terminal
        true
    )
);

CREATE INDEX idx_idempotency_expires ON idempotency_store (expires_at)
    WHERE status = 'COMPLETED';  -- partial index para cleanup

-- Cleanup job: deletar keys expiradas completadas
DELETE FROM idempotency_store
WHERE status = 'COMPLETED' AND expires_at < now() - interval '7 days';
```

### saga_state

```sql
CREATE TABLE saga_state (
    saga_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    saga_type       TEXT NOT NULL,
    current_step    INT NOT NULL DEFAULT 0,
    step_status     TEXT NOT NULL CHECK (step_status IN ('PENDING', 'EXECUTING', 'COMPLETED', 'COMPENSATING', 'COMPENSATED', 'FAILED')),
    payload         JSONB NOT NULL,
    error_message   TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    timeout_at      TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_saga_recovery ON saga_state (step_status, timeout_at)
    WHERE step_status IN ('PENDING', 'EXECUTING');
```

### outbox_events

```sql
CREATE TABLE outbox_events (
    id              BIGSERIAL PRIMARY KEY,
    aggregate_type  TEXT NOT NULL,
    aggregate_id    UUID NOT NULL,
    event_type      TEXT NOT NULL,
    payload         JSONB NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    published_at    TIMESTAMPTZ,
    
    UNIQUE (aggregate_type, aggregate_id, event_type, created_at)
);

CREATE INDEX idx_outbox_pending ON outbox_events (created_at)
    WHERE published_at IS NULL;
```

### sent_notifications

```sql
CREATE TABLE sent_notifications (
    id              BIGSERIAL PRIMARY KEY,
    operation_id    UUID NOT NULL,
    channel         TEXT NOT NULL,
    recipient       TEXT NOT NULL,
    payload         JSONB NOT NULL,
    sent_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    UNIQUE (operation_id, channel, recipient)
);
```

---

## Tratamento de Exceções por Etapa

| Etapa | Exceção | Ação | Response |
|-------|---------|------|----------|
| 1. Idempotency Check | Key já COMPLETED | Retornar cache | `200` com response_cache |
| 1. Idempotency Check | Key PROCESSING | Indicar conflito | `409` + `Retry-After: 30` |
| 1. Idempotency Check | Key FAILED + attempts < max | Permitir retry | Prosseguir (incrementar attempt) |
| 1. Idempotency Check | Key FAILED + attempts >= max | Bloquear | `429 Too Many Requests` |
| 1. Idempotency Check | Key ausente | Rejeitar | `422` com mensagem |
| 2. Validação | Schema inválido | Rejeitar rápido | `400` com detalhes |
| 2. Validação | Sem permissão | Rejeitar rápido | `403` |
| 3. Lock | Timeout de lock | Falha controlada | `409` + `Retry-After` |
| 3. Lock | Deadlock detectado | Abortar transação | `409` + log dos locks |
| 3. Lock | Version mismatch | Retry automático | Retry até limite, depois `409` |
| 4. Saga | Step falha | Compensar steps anteriores | `500` (ou async se tolerável) |
| 4. Saga | Compensação falha | Marcar para recovery manual | `500` + alerta |
| 5. Build | Falha de write (disco) | Abortar + liberar parcial | `507 Insufficient Storage` |
| 5. Build | Processo morto (OOM) | Detectar via timeout + checkpoint recovery | `504 Gateway Timeout` |
| 5. Build | Corrupção de checkpoint | Restart from scratch | Log + retry |
| 6. Notificação | Falha de envio | Marcar PENDING para async retry | Não bloqueia response |

---

## Configuração de Retry

```yaml
# retry-config.yaml — template para qualquer operação com retry
retry:
  max_attempts: 3
  base_delay_ms: 500
  max_delay_ms: 30000
  exponential_base: 2
  jitter: true          # sempre true para evitar thundering herd
  jitter_range: 0.5     # ±50% do delay calculado
  
  # Quais erros são retryáveis
  retryable_errors:
    - "ConnectionError"
    - "TimeoutError"
    - "DeadlockDetected"
    - "VersionMismatch"
    - "LockTimeout"
    - "ServiceUnavailable"  # 503
    - "GatewayTimeout"      # 504
  
  # Quais erros NUNCA retryar
  non_retryable_errors:
    - "ValidationError"
    - "AuthenticationError"
    - "AuthorizationError"
    - "InsufficientStorage"
    - "IdempotencyExhausted"
    - "SagaStepNonCompensatable"
```

---

## Critérios de Qualidade

Antes de entregar qualquer implementação usando esta skill, confirme:

- [ ] Idempotency key obrigatório em toda mutação, 422 se ausente
- [ ] Tabela de idempotência com constraint UNIQUE e transação adequada
- [ ] Lock strategy escolhida baseada em análise de contenção (não default)
- [ ] Locks adquiridos em ordem canônica documentada
- [ ] Timeout de lock configurado (≤ 5s pessimista, ≤ 3 retries otimista)
- [ ] Double-write prevenido via outbox ou saga — zero escritas separadas
- [ ] Saga com compensate real (não log-only) para cada step
- [ ] Build em diretório temporário, nunca no destino final
- [ ] Checkpoint com hash de verificação para retomada de build
- [ ] Atomic swap no final do build (mv ou tmp+sync+mv)
- [ ] Cleanup idempotente e non-blocking
- [ ] Notificação deduplicada via ON CONFLICT DO NOTHING
- [ ] Notificação lê estado confirmado, não variável in-memory
- [ ] Retry com exponential backoff + jitter, lista explícita de retryáveis
- [ ] Tabela de exceções preenchida para todas as etapas
- [ ] Teste de concorrência simulando ≥ 10 requests simultâneos

---

## Referências Cruzadas

| Precisa de... | Use a skill... |
|---|---|
| Schema detalhado das tabelas acima | `database-design` |
| Circuit breaker e retry config avançada | `error-handling` |
| Logging estruturado de falhas de concorrência | `observability` |
| Padrões de código backend geral | `backend-patterns` |
| Padrões de API RESTful | `api-design` |
| Testes de concorrência | `testing-strategy` |
```

---

**Racional das escolhas de design:**

Esta skill foi estruturada como um **pipeline linear** (request → build → done) em vez de uma coleção de padrões isolados porque idempotência e concorrência não são decisões pontuais — são **invariantes que atravessam todas as camadas**. Um lock perfeito na camada de persistência é inútil se o build escreve incrementalmente no destino final. Um idempotency key impecável é inútil se a notificação não é deduplicada. O mapa de riscos no início força a visão end-to-end antes de qualquer implementação.

Os 8 padrões PASS/FAIL cobrem os pontos de falha mais comuns em produção: TOCTOU no idempotency check, stale read no lock otimista, deadlock por ordem incorreta, double-write sem outbox, saga sem compensação real, checkpoint sem verificação, swap não-atômico, e notificação não-deduplicada. Cada um inclui o código exato do erro e da correção para eliminar ambiguidade.

A tabela de exceções por etapa é o checkpoint de resiliência: qualquer desenvolvedor ou modelo que implemente esta skill deve conseguir mapear uma falha específica para a ação correta sem interpretar nada. Salvar em `/docs/idempotency-concurrency-safety.md`.