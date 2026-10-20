---
name: seed-mock-failure-simulation
version: 1.0.0
description: >
  Engenharia de estado base (seeders/mocks) projetada para simulação de falhas.
  Cobre desde a análise do pedido até o artefato final executável, com resiliência
  em cada etapa. Ative ao criar, refatorar ou auditar seeders, factories ou mocks
  cujo propósito inclua testar cenários de exceção, chaos ou edge cases.
triggers:
  - "criar seeder"
  - "criar mock"
  - "seed de falha"
  - "simulação de falha"
  - "estado base para teste"
  - "factory de teste"
  - "dados de teste edge case"
  - "/seed-failure"
---

# SEED & MOCK — Estado base resiliente para simulação de falhas

> **Propósito**: Gerar artefatos de estado base (seeders, factories, mocks) que sejam
> determinísticos, idempotentes, compostáveis e capazes de reproduzir cenários de falha
> de forma isolada e repetível — desde a recepção da demanda até o build do artefato.

---

## Filosofia Central

1. **Determinismo absoluto** — Mesmo seed produz mesmo estado, em qualquer ambiente.
   Na prática: nunca use `Math.random()`, `Date.now()` ou `uuid()` sem seed controlado;
   use geradores pseudoaleatórios com seed explícito (ex: `chancejs` com seed, ou PRNG manual).

2. **Idempotência por construção** — Executar o seeder N vezes produz estado idêntico a 1 vez.
   Na prática: sempre use `INSERT ... ON CONFLICT DO NOTHING` / `upsert` / `truncate + insert`
   em vez de `INSERT` puro; nunca presuma estado prévio.

3. **Composição em camadas** — Estado base é camada neutra; cenários de falha são overlays.
   Na prática: seeder base popula dados válidos; cada cenário de falha aplica deltas sobre
   esse base sem modificá-lo — como git rebase, não git merge.

4. **Isolamento por cenário** — Cenário A nunca contamina cenário B, nem o estado limpo.
   Na prática: cada cenário executa em transação isolada ou schema separado;
   rollback completo após cada execução de teste.

5. **Falha informativa** — Quando o seeder falha, a mensagem diz exatamente qual registro
   e qual constraint quebrou, não "erro ao inserir dados".
   Na prática: wrap cada operação com try/catch que captura row+constraint e emite
   structured error com `table`, `operation`, `constraint`, `payload`.

6. **Zero dependência de runtime externo** — O artefato final executa sem API externa,
   sem banco de produção, sem secrets.
   Na prática: mocks substituem toda chamada de rede; seeders usam SQLite em memória
   ou container Docker com schema clonado, nunca apontam para ambiente real.

---

## Quando Ativar

### ✅ Ativar para:
- Criar seeders que populam banco com dados de teste
- Criar factories que geram entidades com variações controladas
- Criar mocks/stubs de serviços externos (APIs, filas, storage)
- Projetar cenários de falha (timeout, 500, dados corrompidos, estado vazio)
- Refatorar seeders existentes para adicionar resiliência ou idempotência
- Auditar seeders/mocks quanto a determinismo e isolamento

### ❌ NÃO ativar para:
- Design de schema de produção → use `database-design`
- Estratégia geral de testes (unit vs integration vs e2e) → use `test-strategy`
- Migration de schema → responda diretamente sem skill
- Geração de dados para benchmark/performance (volume, não falha) → responda diretamente

---

## Escopo e Limites

| Esta skill cobre | Esta skill NÃO cobre |
|---|---|
| Estrutura e código de seeders/mocks/factories | Escolha do framework de testes (Jest, Pytest, etc.) |
| Ordenação topológica de dependências entre tabelas | Execução dos testes em si |
| Geração determinística de dados edge-case | CI/CD pipeline configuration |
| Resiliência no processo de build do artefato | Schema DDL de produção |
| Validação pós-seed (consistência referencial) | Ferramentas de chaos engineering em runtime (Chaos Monkey) |

---

## Protocolo de Execução

### Fase 1 — Recepção e Análise

**1.1. Extrair requisitos mínimos do pedido**

Verbo imperativo: **Extrair** do pedido do usuário os seguintes campos obrigatórios.
Se qualquer campo estiver ausente, perguntar antes de prosseguir — nunca inferir silenciosamente.

| Campo | O que é | Exemplo |
|---|---|---|
| `schema_alvo` | Tabelas/views a popular | `users, orders, payments` |
| `volume_por_tabela` | Qtd de registros por tabela | `users: 100, orders: 500` |
| `cenarios_falha` | Lista de falhas a simular | `timeout no gateway, saldo negativo, order sem items` |
| `stack` | Linguagem + ORM + DB | `Python + SQLAlchemy + PostgreSQL` |
| `constraints_conhecidas` | FKs, unique, check constraints | `orders.user_id FK users.id, payments.amount > 0` |

**Critério de conclusão**: Todos os 5 campos preenchidos e confirmados com o usuário.

**1.2. Mapear grafo de dependências**

Verbo imperativo: **Construir** um grafo direcionado acíclico (DAG) onde nó = tabela e aresta = FK.
Identificar ciclos (ex: `users.manager_id → users.id`) e planejar estratégia de quebra
(deferred constraints ou inserção em duas passadas).

**Critério de conclusão**: Lista ordenada de tabelas em ordem topológica, com ciclos anotados.

**Resiliência nesta etapa**:
- Se o usuário não conhece as FKs → extrair do schema DDL ou pedir `pg_dump --schema-only`
- Se há ciclos → anotar como "deferred" e não abortar
- Se tabela não tem PK explícita → flag como erro bloqueante e pedir correção de schema

### Fase 2 — Projeto da API do Seeder

**2.1. Definir interface pública**

Verbo imperativo: **Projetar** a API do seeder seguindo este contrato mínimo:

```typescript
// Contrato de interface — qualquer implementação deve cumprir
interface SeederV1<TContext = Record<string, unknown>> {
  /** Nome único do cenário */
  name: string;

  /** Executa o seeder. Deve ser idempotente. */
  run(ctx: TContext): Promise<SeedResult>;

  /** Remove todo estado criado. Deve ser seguro chamar mesmo sem run prévio. */
  rollback(): Promise<void>;

  /** Valida estado pós-seed. Retorna lista de violações (vazio = ok). */
  validate(): Promise<ValidationError[]>;
}

interface SeedResult {
  rowsInserted: Record<string, number>; // tableName → count
  durationMs: number;
  warnings: string[];
}

interface ValidationError {
  table: string;
  type: 'orphan' | 'missing_fk' | 'constraint_violation' | 'unexpected_row';
  detail: string;
  payload?: Record<string, unknown>;
}
```

**Critério de conclusão**: Interface definida e tipada para a stack alvo.

**Resiliência nesta etapa**:
- Se a stack não tem tipagem estática → reproduzir contrato como JSDoc/docstring com exemplos
- Se ORM limita a API (ex: não suporta transação explícita) → documentar limitação e providenciar fallback com SQL raw

**2.2. Definir modelo de composição de cenários**

Verbo imperativo: **Projetar** o sistema de camadas onde cada cenário é um overlay:

```typescript
// Base layer: dados válidos e completos
const base = createBaseSeed(); // users, orders, payments normais

// Failure layers: deltas sobre o base
const timeoutScenario = compose(base, {
  name: 'gateway-timeout',
  apply(ctx) {
    // Adiciona order em estado "pending" sem payment correspondente
    // Configura mock do gateway para retornar timeout
  },
  rollback(ctx) {
    // Remove apenas o que este cenário adicionou
  }
});

// Execução: base roda primeiro, depois cada overlay em transação isolada
await timeoutScenario.run(ctx);
```

**Critério de conclusão**: Pelo menos 2 cenários de falha compostáveis sobre o mesmo base.

### Fase 3 — Implementação dos Geradores

**3.1. Implementar gerador determinístico**

Verbo imperativo: **Implementar** gerador de dados com seed controlado.

```python
# ✅ PASS — Determinístico, seed explícito, reproduzível
import random
from dataclasses import dataclass

@dataclass
class SeededGenerator:
    seed: int

    def __post_init__(self):
        self._rng = random.Random(self.seed)

    def email(self) -> str:
        idx = self._rng.randint(1, 999_999)
        return f"user-{idx}@seed-test.local"

    def money(self, min_val: float = 0.01, max_val: float = 10_000.0) -> float:
        return round(self._rng.uniform(min_val, max_val), 2)

    def choice(self, options: list):
        return self._rng.choice(options)


# Uso: mesmo seed = mesmo resultado, em qualquer máquina
gen = SeededGenerator(seed=42)
assert gen.email() == "user-82341@seed-test.local"  # sempre
```

```python
# ❌ FAIL — Não-determinístico, quebra em rerun
import uuid
from datetime import datetime

def create_user():
    return {
        "id": uuid.uuid4(),          # diferente a cada chamada
        "email": f"{datetime.now().timestamp()}@test.local",  # timestamp muda
        "created_at": datetime.now() # muda a cada execução
    }
```

**Por que importa**: Testes não-determinísticos produzem flaky tests. Seeder que gera dados
diferentes a cada run impossibilita reprodução de bugs e invalida snapshots.

**Critério de conclusão**: Gerador com pelo menos 5 tipos de dado (string, number, date, email, enum)
todos controlados por seed.

**Resiliência nesta etapa**:
- Se a stack não tem PRNG com seed → implementar LCG simples (5 linhas de código)
- Se dados precisam ser únicos (constraint unique) → usar contador sequencial prefixado pelo seed,
  não random: `f"user-{seed}-{seq:04d}"`

**3.2. Implementar geradores de edge-case**

Verbo imperativo: **Implementar** fábrica de variantes edge-case para cada entidade:

```python
# ✅ PASS — Catálogo explícito de variantes, cada uma nomeada
@dataclass
class UserFactory:
    gen: SeededGenerator

    def valid(self) -> dict:
        return {"name": "João Silva", "email": self.gen.email(), "active": True}

    def with_long_name(self) -> dict:
        """Nome com 300 chars — testa truncamento de DB ou UI"""
        return {**self.valid(), "name": "A" * 300}

    def with_special_chars_email(self) -> dict:
        """Email com chars especiais — testa validação de input"""
        return {**self.valid(), "email": "user+tag@domain.cöm"}

    def inactive(self) -> dict:
        """Usuário inativo — testa fluxo de autenticação negada"""
        return {**self.valid(), "active": False}

    def with_future_birth_date(self) -> dict:
        """Data de nascimento no futuro — testa validação de regra de negócio"""
        return {**self.valid(), "birth_date": "2099-12-31"}

    def with_null_mandatory_field(self) -> dict:
        """Campo obrigatório como null — testa constraint NOT NULL"""
        return {"name": None, "email": self.gen.email(), "active": True}
```

```python
# ❌ FAIL — Edge cases misturados com dados válidos sem nomeação
def create_user(is_edge_case=False):
    if is_edge_case:
        # Qual edge case? Não dá pra saber nem selecionar individualmente
        return {"name": None, "email": "bad"}
    return {"name": "João", "email": "joao@test.com"}
```

**Por que importa**: Sem nomeação individual, não é possível criar cenários específicos
nem debugar qual variante causou falha. Catalogar por nome é essencial para composição.

**Critério de conclusão**: Cada entidade principal tem mínimo de 4 variantes edge-case nomeadas.

**Resiliência nesta etapa**:
- Se não há documentação de constraints → inferir do schema DDL e gerar variantes para cada
  constraint encontrada (NOT NULL → null, UNIQUE → duplicado, CHECK → valor fora do range, FK → id inexistente)
- Se entidade tem 20+ campos → focar variantes nos campos com constraints e nos campos de negócio
  (não gerar edge case para cada `created_at`)

### Fase 4 — Implementação da Orquestração

**4.1. Implementar executor com transação e rollback**

Verbo imperativo: **Implementar** executor que garante atomicidade da operação inteira.

```python
# ✅ PASS — Transação com rollback automático em falha, logging estruturado
import logging
from contextlib import asynccontextmanager
from datetime import datetime

logger = logging.getLogger("seed")

@asynccontextmanager
async def seed_transaction(engine, seed_name: str):
    """Context manager: commit em sucesso, rollback em qualquer exceção."""
    conn = await engine.connect()
    tx = await conn.begin()
    start = datetime.now()
    logger.info({"event": "seed_start", "seed": seed_name, "ts": start.isoformat()})
    try:
        yield conn
        await tx.commit()
        duration = (datetime.now() - start).total_seconds() * 1000
        logger.info({"event": "seed_success", "seed": seed_name, "duration_ms": duration})
    except Exception as e:
        await tx.rollback()
        duration = (datetime.now() - start).total_seconds() * 1000
        logger.error({
            "event": "seed_rollback",
            "seed": seed_name,
            "duration_ms": duration,
            "error": str(e),
            "error_type": type(e).__name__
        })
        raise SeedError(seed_name, e) from e
    finally:
        await conn.close()


class SeedError(Exception):
    def __init__(self, seed_name: str, cause: Exception):
        self.seed_name = seed_name
        self.cause = cause
        super().__init__(f"Seed '{seed_name}' failed: {cause}")
```

```python
# ❌ FAIL — Sem transação, sem rollback, sem logging estruturado
async def run_seed(data: list[dict]):
    for row in data:
        await db.execute(insert(User).values(row))
    # Se a linha 50 falhar, as 49 anteriores ficam no banco — estado parcial
    # Sem log — não dá pra saber o que foi inserido antes da falha
```

**Por que importa**: Estado parcial após falha de seeder é pior que estado vazio.
O próximo run presume estado limpo e gera duplicatas ou viola unique constraints.

**Critério de conclusão**: Executor com transação, rollback automático, log estruturado (JSON).

**Resiliência nesta etapa**:
- Se o DB não suporta transação DDL (MySQL com algumas operações) → separar DDL do DML,
  executar DDL primeiro fora de transação, DML dentro de transação
- Se o DB é SQLite em memória → transação funciona, mas rollback = perder tudo;
  documentar que "rollback em memória = reset completo"
- Se timeout de transação é atingido (seed grande) → implementar batch commit com checkpoint:
  commit a cada N rows, salvar progresso, permitir retomada do último checkpoint

**4.2. Implementar validação pós-seed**

Verbo imperativo: **Implementar** validação que verifica consistência do estado gerado.

```python
# ✅ PASS — Validações nomeadas, retorna lista de violações (não lança)
async def validate_seed(conn) -> list[ValidationError]:
    violations: list[ValidationError] = []

    # 1. Orphans: orders sem user correspondente
    orphans = await conn.execute(text("""
        SELECT o.id, o.user_id FROM orders o
        LEFT JOIN users u ON o.user_id = u.id
        WHERE u.id IS NULL
    """))
    for row in orphans:
        violations.append(ValidationError(
            table="orders", type="orphan",
            detail=f"order {row.id} references non-existent user {row.user_id}",
            payload={"order_id": row.id, "missing_user_id": row.user_id}
        ))

    # 2. Contagem mínima
    for table, min_expected in [("users", 10), ("orders", 50)]:
        count = await conn.scalar(text(f"SELECT COUNT(*) FROM {table}"))
        if count < min_expected:
            violations.append(ValidationError(
                table=table, type="unexpected_row",
                detail=f"Expected >= {min_expected} rows, got {count}"
            ))

    # 3. Constraint de negócio: nenhum pagamento com amount <= 0
    invalid_payments = await conn.execute(text("""
        SELECT id, amount FROM payments WHERE amount <= 0
    """))
    for row in invalid_payments:
        violations.append(ValidationError(
            table="payments", type="constraint_violation",
            detail=f"payment {row.id} has invalid amount {row.amount}",
            payload={"payment_id": row.id, "amount": row.amount}
        ))

    return violations
```

```python
# ❌ FAIL — Validação que lança na primeira violação, sem detalhe
async def validate(conn):
    count = await conn.scalar(text("SELECT COUNT(*) FROM users"))
    if count == 0:
        raise Exception("No users found")  # Para aqui, não verifica o resto
    # Não verifica orphans, não verifica constraints de negócio
```

**Por que importa**: Validação que lança early esconde outros problemas. O desenvolvedor
corrige um, roda de novo, encontra outro — ciclo desperdiçado. Lista completa = correção em lote.

**Critério de conclusão**: Mínimo 3 validações: orphans, contagem mínima, constraint de negócio.

**Resiliência nesta etapa**:
- Se tabela tem self-referência (ex: `users.manager_id → users.id`) → query de orphan precisa
  tratar NULL como válido: `WHERE manager_id IS NOT NULL AND parent.id IS NULL`
- Se schema muda frequentemente → gerar validações automaticamente a partir do DDL
  (para cada FK, gerar query de orphan check)

### Fase 5 — Implementação dos Cenários de Falha

**5.1. Implementar catálogo de cenários com mock associado**

Verbo imperativo: **Implementar** cada cenário como objeto com `apply`, `rollback`, `mock_config`
e `expected_behavior`.

```python
# ✅ PASS — Cenário completo: dados + mock + expectativa
@dataclass
class FailureScenario:
    name: str
    description: str
    apply: Callable  # Modifica estado base
    rollback: Callable  # Remove modificações
    mock_config: dict  # Configura mocks de serviços externos
    expected_behavior: str  # O que o sistema sob teste deve fazer

SCENARIOS: list[FailureScenario] = [
    FailureScenario(
        name="payment-gateway-timeout",
        description="Order existe, pagamento pendente, gateway nunca responde",
        apply=lambda ctx: [
            # Cria order em status "payment_pending"
            insert_order(user_id=ctx["user_id"], status="payment_pending"),
        ],
        rollback=lambda ctx: delete_orders_by_status("payment_pending"),
        mock_config={
            "payment_gateway": {
                "create_charge": {"behavior": "timeout", "delay_ms": 30000}
            }
        },
        expected_behavior="Order permanece em payment_pending. Retry schedulado em 5min."
    ),
    FailureScenario(
        name="order-without-items",
        description="Order criada sem nenhum item associado — regra de negócio violada",
        apply=lambda ctx: [
            insert_order(user_id=ctx["user_id"], status="confirmed"),
            # NOTA: nenhum item inserido — isso é o cenário
        ],
        rollback=lambda ctx: delete_orders_without_items(),
        mock_config={},  # Sem mock externo — a falha é no estado interno
        expected_behavior="Sistema rejeita order ao validar items. Status → 'validation_failed'."
    ),
    FailureScenario(
        name="negative-balance-after-refund",
        description="Refund de valor maior que o pagamento original",
        apply=lambda ctx: [
            insert_order(user_id=ctx["user_id"], total=50.00),
            insert_payment(order_id=ctx["order_id"], amount=50.00),
            # Refund de 100.00 sobre pagamento de 50.00
            insert_refund(payment_id=ctx["payment_id"], amount=100.00),
        ],
        rollback=lambda ctx: delete_refunds_over_payment(),
        mock_config={
            "payment_gateway": {
                "create_refund": {"behavior": "success"}  # Gateway aceita, sistema deve rejeitar
            }
        },
        expected_behavior="Sistema detecta refund > payment. Rejeita com erro 'REFUND_EXCEEDS_PAYMENT'."
    ),
    FailureScenario(
        name="concurrent-duplicate-order",
        description="Duas orders idênticas criadas simultaneamente (idempotency key duplicada)",
        apply=lambda ctx: [
            insert_order(user_id=ctx["user_id"], idempotency_key="key-001", status="confirmed"),
            insert_order(user_id=ctx["user_id"], idempotency_key="key-001", status="confirmed"),
        ],
        rollback=lambda ctx: delete_orders_by_idempotency_key("key-001"),
        mock_config={},
        expected_behavior="Segunda order rejeitada com 409 Conflict. Primeira mantida."
    ),
]
```

```python
# ❌ FAIL — Cenário sem rollback, sem mock, sem expectativa definida
def test_timeout():
    # Cria order... como? Com quais dados?
    # Mocka gateway... onde? Como?
    # O que se espera? Não documentado.
    assert True  # Teste inútil
```

**Por que importa**: Cenário sem `rollback` polui o estado entre testes. Sem `mock_config`,
o teste pode atingir serviços reais. Sem `expected_behavior`, o teste não tem asserção real.

**Critério de conclusão**: Cada cenário tem os 5 campos preenchidos e é executável isoladamente.

**Resiliência nesta etapa**:
- Se cenário depende de estado que outro cenário criou → é bug de design; cada cenário
  deve ser auto-suficiente (compor sobre o base, não sobre outro cenário)
- Se mock precisa de estado sequencial (ex: "primeira chamada timeout, segunda sucesso") →
  usar array de respostas em vez de resposta única: `{"responses": [{"timeout"}, {"success"}]}`
- Se cenário simula falha de infraestrutura (ex: "conexão com DB cai") → usar mock no nível
  de conexão/adapter, não tentar derrubar o DB real

### Fase 6 — Implementação dos Mocks de Serviço

**6.1. Implementar mock com estados configuráveis**

Verbo imperativo: **Implementar** camada de mock que suporta comportamento por cenário.

```python
# ✅ PASS — Mock com registro de chamadas, estados configuráveis, reset entre testes
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

class MockBehavior(Enum):
    SUCCESS = "success"
    TIMEOUT = "timeout"
    ERROR_500 = "error_500"
    ERROR_400 = "error_400"
    EMPTY_RESPONSE = "empty_response"
    MALFORMED_RESPONSE = "malformed_response"

@dataclass
class MockEndpoint:
    name: str
    behavior: MockBehavior = MockBehavior.SUCCESS
    response_body: Any = None
    delay_ms: int = 0
    error_message: str = ""
    call_count: int = 0
    call_history: list[dict] = field(default_factory=list)

    def record_call(self, request: dict) -> dict:
        self.call_count += 1
        entry = {"index": self.call_count, "request": request, "timestamp": time.time()}
        self.call_history.append(entry)
        return entry

    def reset(self):
        self.call_count = 0
        self.call_history.clear()

@dataclass
class MockService:
    name: str
    endpoints: dict[str, MockEndpoint] = field(default_factory=dict)

    def configure(self, endpoint_name: str, behavior: MockBehavior, **kwargs):
        if endpoint_name not in self.endpoints:
            self.endpoints[endpoint_name] = MockEndpoint(name=endpoint_name)
        ep = self.endpoints[endpoint_name]
        ep.behavior = behavior
        ep.response_body = kwargs.get("response_body")
        ep.delay_ms = kwargs.get("delay_ms", 0)
        ep.error_message = kwargs.get("error_message", "")

    def reset_all(self):
        for ep in self.endpoints.values():
            ep.reset()

    def assert_call_count(self, endpoint_name: str, expected: int):
        actual = self.endpoints[endpoint_name].call_count
        if actual != expected:
            raise AssertionError(
                f"Mock '{self.name}.{endpoint_name}': expected {expected} calls, got {actual}. "
                f"History: {self.endpoints[endpoint_name].call_history}"
            )


# Uso no cenário:
gateway = MockService(name="payment_gateway")
gateway.configure("create_charge", MockBehavior.TIMEOUT, delay_ms=30000)
# ... roda teste ...
gateway.assert_call_count("create_charge", 1)
gateway.reset_all()
```

```python
# ❌ FAIL — Mock hard-coded sem configuração, sem histórico, sem reset
class FakeGateway:
    def charge(self, amount):
        return {"status": "ok"}  # Sempre sucesso, impossível simular falha
        # Sem registro de chamadas — impossível assertir quantas vezes foi chamado
        # Sem reset — estado vaza entre testes
```

**Por que importa**: Mock sem histórico de chamadas não permite assertir_side_effects.
Mock sem reset vaza estado entre cenários. Mock hard-coded precisa ser editado manualmente
para cada cenário, eliminando a composição.

**Critério de conclusão**: Mock com configure, record_call, assert_call_count, reset_all.

**Resiliência nesta etapa**:
- Se serviço tem autenticação (API key, OAuth) → mock deve aceitar qualquer credencial
  e logar qual foi usada, sem validar
- Se serviço retorna streaming (SSE, WebSocket) → mock deve suportar emitter de eventos
  configurável (ex: emitir 3 eventos depois de delay)
- Se serviço tem rate limiting → mock deve aceitar config de rate limit para testar
  comportamento do cliente sob throttling

### Fase 7 — Build do Artefato Final

**7.1. Empacotar seeder como módulo executável**

Verbo imperativo: **Empacotar** tudo em um artefato auto-suficiente com CLI.

```python
# ✅ PASS — Artefato executável com subcomandos, help, e saída estruturada
# arquivo: seed_tool.py
import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Seed tool — estado base para simulação de falhas"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Subcomando: rodar seeder base
    run_base = sub.add_parser("run-base", help="Popula estado base válido")
    run_base.add_argument("--seed", type=int, default=42, help="PRNG seed")
    run_base.add_argument("--dry-run", action="store_true", help="Mostra SQL sem executar")
    run_base.add_argument("--validate-only", action="store_true", help="Valida estado sem inserir")

    # Subcomando: rodar cenário de falha
    run_scenario = sub.add_parser("run-scenario", help="Aplica cenário de falha sobre o base")
    run_scenario.add_argument("scenario_name", help="Nome do cenário (ex: payment-gateway-timeout)")
    run_scenario.add_argument("--seed", type=int, default=42)
    run_scenario.add_argument("--keep-state", action="store_true", help="Não faz rollback após")

    # Subcomando: listar cenários disponíveis
    sub.add_parser("list", help="Lista cenários de falha disponíveis")

    # Subcomando: validar estado atual
    sub.add_parser("validate", help="Valida consistência do estado atual")

    args = parser.parse_args()

    try:
        if args.command == "run-base":
            result = execute_base_seed(seed=args.seed, dry_run=args.dry_run)
            print(json.dumps(result, indent=2, default=str))
        elif args.command == "run-scenario":
            result = execute_scenario(
                name=args.scenario_name,
                seed=args.seed,
                rollback=not args.keep_state
            )
            print(json.dumps(result, indent=2, default=str))
        elif args.command == "list":
            for s in SCENARIOS:
                print(f"  {s.name:40s} {s.description}")
        elif args.command == "validate":
            violations = validate_seed(get_connection())
            if violations:
                print(json.dumps([v.__dict__ for v in violations], indent=2))
                sys.exit(1)
            else print('{"status":"ok","violations":0}')
    except SeedError as e:
        print(json.dumps({"error": str(e), "seed": e.seed_name}, indent=2))
        sys.exit(2)
    except Exception as e:
        print(json.dumps({"error": str(e), "unexpected": True}, indent=2))
        sys.exit(3)

if __name__ == "__main__":
    main()
```

```bash
# Uso:
python seed_tool.py run-base --seed 42 --dry-run          # Preview sem executar
python seed_tool.py run-base --seed 42                     # Executa base
python seed_tool.py list                                    # Lista cenários
python seed_tool.py run-scenario payment-gateway-timeout   # Aplica cenário
python seed_tool.py validate                               # Verifica consistência
```

```python
# ❌ FAIL — Script monolítico sem CLI, sem dry-run, sem validação separada
# arquivo: seed.py
def main():
    # Tudo hardcoded, sem opção de selecionar cenário
    # Sem dry-run — ouro sobre lixo
    # Sem validação — não sabe se funcionou
    conn = create_connection()
    for user in generate_users():
        conn.execute(insert(User).values(user))
    conn.commit()
```

**Por que importa**: Artefato sem CLI não é operável por CI nem por outros devs.
Sem dry-run, não é possível revisar o que será executado antes de rodar em ambiente compartilhado.
Sem subcomando de validação, não há como verificar integridade pós-fato.

**Critério de conclusão**: Artefato com `run-base`, `run-scenario`, `list`, `validate`.
Todos com `--help` funcional. Saída sempre JSON estruturado. Exit codes diferentes por tipo de erro.

**Resiliência nesta etapa**:
- Se o artefato precisa de variáveis de ambiente (DB_URL, etc.) → aceitar via `--db-url`
  com fallback para env var, com validação de conectividade antes de qualquer operação
- Se o artefato vai rodar em Docker → incluir Dockerfile inline como comentário no topo do arquivo
- Se o artefato precisa de dependências não-standard → gerar `requirements.txt` ou `package.json`
  ao lado do arquivo principal

**7.2. Gerar manifest do artefato**

Verbo imperativo: **Gerar** arquivo `MANIFEST.json` ao lado do artefato com metadata de build.

```json
{
  "artifact": "seed_tool.py",
  "generated_at": "2025-01-15T10:30:00Z",
  "schema_version": "1.0.0",
  "stack": {"language": "python", "orm": "sqlalchemy", "db": "postgresql"},
  "tables_seeded": ["users", "orders", "order_items", "payments", "refunds"],
  "row_counts": {"users": 100, "orders": 500, "order_items": 1500, "payments": 500, "refunds": 50},
  "scenarios": [
    {
      "name": "payment-gateway-timeout",
      "description": "Order existe, pagamento pendente, gateway nunca responde",
      "mocks_affected": ["payment_gateway.create_charge"],
      "tables_modified": ["orders"]
    }
  ],
  "dependencies": ["sqlalchemy>=2.0", "psycopg2-binary"],
  "seed_default": 42,
  "idempotent": true,
  "requires_external_services": false
}
```

**Critério de conclusão**: `MANIFEST.json` presente ao lado do artefato com todos os campos.

---

## Padrões Específicos

### Padrão 1: Inserção Idempotente

**Regra**: Toda inserção deve usar upsert. Nunca presuma que a tabela está vazia.

```sql
-- ✅ PASS — Upsert com identidade natural
INSERT INTO users (id, email, name, active)
VALUES (1, 'user-1@seed.local', 'Test User', true)
ON CONFLICT (id) DO UPDATE SET
  email = EXCLUDED.email,
  name = EXCLUDED.name,
  active = EXCLUDED.active;

-- ❌ FAIL — Insert puro, falha na segunda execução
INSERT INTO users (id, email, name, active)
VALUES (1, 'user-1@seed.local', 'Test User', true);
-- ERROR: duplicate key value violates unique constraint "users_pkey"
```

**Por que importa**: Segunda execução de seeder deve ser no-op, não erro.
Sem isso, CI reexecutando pipeline inteiro falha no passo de seed.

---

### Padrão 2: Ordenação por Dependência

**Regra**: Inserir na ordem topológica do DAG de FKs. Ciclos requerem deferred constraints.

```python
# ✅ PASS — Ordem explícita, ciclos anotados
SEED_ORDER = [
    ("users",         "no dependencies"),
    ("addresses",     "depends on users"),
    ("products",      "no dependencies"),
    ("orders",        "depends on users, addresses"),
    ("order_items",   "depends on orders, products"),
    ("payments",      "depends on orders"),
    ("refunds",       "depends on payments"),
    # Ciclo: users.manager_id → users.id
    # Estratégia: inserir users sem manager_id, depois UPDATE com SET manager_id
]

# ❌ FAIL — Sem ordem, insert de orders antes de users
tables_to_seed = ["orders", "users", "payments"]  # ordem aleatória
for table in tables_to_seed:
    insert_into(table)  # Falha: orders.user_id FK para users.id que não existe ainda
```

**Por que importa**: Inserção fora de ordem gera FK violation. A mensagem de erro
não diz qual era a ordem correta — só diz que a constraint falhou.

---

### Padrão 3: Limpeza Reversa

**Regra**: Rollback deleta na ordem inversa da inserção. Filhos antes de pais.

```python
# ✅ PASS — Ordem reversa, proteção contra tabela inexistente
ROLLBACK_ORDER = [
    "refunds", "payments", "order_items", "orders",
    "addresses", "products", "users"
]

async def rollback_all(conn):
    for table in ROLLBACK_ORDER:
        try:
            await conn.execute(text(f"DELETE FROM {table}"))
        except UndefinedTableError:
            logger.warning({"event": "rollback_skip", "table": table, "reason": "table_not_found"})
        except Exception as e:
            logger.error({"event": "rollback_error", "table": table, "error": str(e)})
            raise  # Não silencia erros de FK — indica rollback fora de ordem

# ❌ FAIL — Ordem errada, TRUNCATE sem CASCADE
async def bad_rollback(conn):
    await conn.execute(text("DELETE FROM users"))  # Falha: payments referencia users
    # Ou pior: TRUNCATE users — falha com FK violation a menos que CASCADE
```

**Por que importa**: Rollback que falha deixa estado residual. Se o próximo seed
rodar sobre esse estado, dados antigos contaminam o cenário.

---

### Padrão 4: Log Estruturado (nunca print)

**Regra**: Toda operação de seed emite log como dict/JSON, nunca string livre.

```python
# ✅ PASS — Log estruturado, pesquisável, parseável
logger.info({
    "event": "batch_insert",
    "table": "orders",
    "batch_size": 100,
    "batch_index": 3,
    "total_batches": 5,
    "rows_so_far": 300
})

# ❌ FAIL — Log humano, não pesquisável
print(f"Inserindo lote 3 de 5 na tabela orders...")  # Não é parseável, não tem metadata
```

**Por que importa**: Em CI, logs precisam ser filtráveis por `event`, `table`, `batch_index`.
String livre não permite grep estruturado nem dashboarding.

---

### Padrão 5: Dry-Run como Primeiro Cidadão

**Regra**: Todo seeder suporta modo dry-run que mostra o que faria sem executar.

```python
# ✅ PASS — Dry-run coleta statements sem executar
async def run_seed(conn, dry_run: bool = False):
    statements: list[str] = []

    for user in generate_users():
        stmt = insert(User).values(user).on_conflict_do_nothing()
        if dry_run:
            statements.append(str(stmt.compile(dialect=conn.dialect)))
        else:
            await conn.execute(stmt)

    if dry_run:
        return {"dry_run": True, "statements": statements, "count": len(statements)}
    return {"dry_run": False, "rows_inserted": len(generate_users())}
```

**Por que importa**: Sem dry-run, a única forma de saber o que o seeder faz é rodando.
Em ambiente compartilhado, isso é inaceitável.

---

### Padrão 6: Seeds com Sequência Determinística para Unique Constraints

**Regra**: Quando a constraint é UNIQUE e o dado precisa ser único, use sequência, não random.

```python
# ✅ PASS — Sequência prefixada pelo seed, sempre única, sempre determinística
def generate_unique_emails(seed: int, count: int) -> list[str]:
    return [f"user-{seed}-{i:05d}@seed.local" for i in range(count)]
# seed=42, count=3 → ["user-42-00000@seed.local", "user-42-00001@seed.local", "user-42-00002@seed.local"]

# ❌ FAIL — Random pode colidir, não é reproduzível
def generate_emails(count: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    return [f"{rng.randint(1,999999)}@test.local" for _ in range(count)]
# Com count > raiz do range, colisões são matematicamente prováveis (paradoxo do aniversário)
```

**Por que importa**: Colisão em unique constraint durante seed = falha não-determinística.
Às vezes passa, às vezes falha — o pior tipo de bug.

---

## Anti-Padrões Críticos

| Anti-padrão | Consequência | Alternativa correta |
|---|---|---|
| `SELECT *` em validação pós-seed | Validação quebra ao adicionar coluna | Listar colunas explicitamente |
| Seeder que chama API real | Teste depende de disponibilidade externa; flaky | Mock no nível de adapter/HTTP client |
| Seed sem `--dry-run` | Impossível revisar antes de executar em staging | Coletar statements em lista, imprimir sem executar |
| Dados de teste com PII real | Vazamento de dados pessoais em logs e CI | Gerar dados sintéticos com domínio `@seed.local` |
| Um seeder monolítico para todos os cenários | Impossível rodar cenário isolado; qualquer mudança quebra tudo | Composição em camadas: base + overlays |
| `TRUNCATE CASCADE` como cleanup | Remove dados de outros testes rodando em paralelo | Deletar apenas registros criados por este seeder (marcar com `seed_id`) |
| Ignorar erro em rollback ("try/except pass") | Estado residual silencioso contamina próximos testes | Logar erro + falhar explicitamente + indicar qual tabela não conseguiu limpar |
| Gerador sem seed | Dados diferentes a cada run = flaky tests | PRNG com seed explícito passado como parâmetro |
| Cenário de falha sem `expected_behavior` | Teste passa sem testar nada (assert True implícito) | Documentar comportamento esperado; traduzir em asserção no teste |

---

## Critérios de Qualidade

Antes de entregar o artefato, confirme:

- [ ] Frontmatter completo (name, version, description, triggers, scope, quality_bar)
- [ ] Gerador determinístico com seed controlado — zero `random()`, `uuid()`, `Date.now()` sem seed
- [ ] Inserção idempotente (upsert/on conflict) em todas as tabelas
- [ ] Ordem topológica de inserção documentada e implementada
- [ ] Rollback na ordem inversa com tratamento de erro por tabela
- [ ] Transação envolvendo todo o DML (commit all ou rollback all)
- [ ] Mínimo 4 variantes edge-case por entidade principal
- [ ] Cada cenário de falha com `apply`, `rollback`, `mock_config`, `expected_behavior`
- [ ] Mock com `configure`, `record_call`, `assert_call_count`, `reset_all`
- [ ] Validação pós-seed retorna lista de violações (não lança na primeira)
- [ ] Log estruturado (dict/JSON) em toda operação — zero `print()`
- [ ] CLI com `run-base`, `run-scenario`, `list`, `validate` e `--dry-run`
- [ ] `MANIFEST.json` com metadata completa do artefato
- [ ] Zero dependência de serviço externo (API, banco de produção, secrets)
- [ ] Zero PII real — todos os dados são sintéticos
- [ ] Exit codes diferentes: 0=ok, 1=validation_failed, 2=seed_error, 3=unexpected_error
- [ ] Comprimento total do artefato: proporcional à complexidade, nunca abaixo de 150 linhas

---

## Referências Cruzadas

| Precisa de... | Use a skill... |
|---|---|
| Design de schema e normalização | `database-design` |
| Padrões de arquitetura de repositório | `backend-patterns` |
| Estratégia geral de testes (coverage, pirâmide) | `test-strategy` |
| Padrões de código frontend para testes de UI | `frontend-design` |
| Ler arquivos DDL enviados pelo usuário | `file-reading` |

---

## Exemplo Completo — Execução End-to-End

**Input do usuário**: "Preciso de um seeder para meu e-commerce. Tabelas: users, orders, order_items, payments. Quero simular: 1) gateway timeout, 2) order sem items, 3) refund maior que pagamento. Stack: Python + SQLAlchemy + PostgreSQL."

**Saída esperada do processo**:

```
Arquivos gerados:
├── seed_tool.py          # Artefato executável (CLI)
├── manifest.json         # Metadata do build
├── seeders/
│   ├── base.py           # Estado base válido (100 users, 500 orders, etc.)
│   ├── generators.py     # SeededGenerator + UserFactory, OrderFactory, etc.
│   └── validators.py     # Validações pós-seed
├── scenarios/
│   ├── gateway_timeout.py
│   ├── order_without_items.py
│   └── refund_exceeds_payment.py
└── mocks/
    └── payment_gateway.py # MockService com endpoints configuráveis

Execução:
$ python seed_tool.py run-base --seed 42 --dry-run
{"dry_run": true, "statements": [...], "count": 2150}

$ python seed_tool.py run-base --seed 42
{"dry_run": false, "rows_inserted": {"users": 100, "orders": 500, ...}, "duration_ms": 340}

$ python seed_tool.py run-scenario gateway-timeout
{"scenario": "gateway-timeout", "status": "applied", "duration_ms": 12}

$ python seed_tool.py validate
{"status": "ok", "violations": 0}
```

---

> **Lembrete final**: O objetivo deste artefato não é "popular dados de teste".
> É criar uma máquina de estados controlável onde cada cenário de falha é um botão
> que se pressiona e o sistema responde de forma previsível e observável.
> Se o seeder não permite rodar cenário X isoladamente e observar a resposta Y,
> ele não está cumprindo seu contrato.