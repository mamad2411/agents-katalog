---
name: deadlock-avoidance
version: 1.0.0
description: >
  Projeta e implementa mapeamento de recursos críticos e estratégias de 
  evitação de deadlocks em código. Focado em resiliência, tratamento de 
  exceções e recuperação graciosa em sistemas concorrentes e distribuídos.
triggers:
  - "evitar deadlock"
  - "mapear recursos críticos"
  - "lock ordering"
  - "deadlock no código"
  - "concorrência resiliente"
  - "recursos compartilhados travando"
---

# DEADLOCK AVOIDANCE — Concorrência resiliente sem bloqueios mortos

> **Propósito**: Projetar aquisição e liberação de recursos com ordenação estrita, timeouts e circuit breakers, eliminando deadlocks e garantindo fallback estruturado em cenários de falha.

---

## Filosofia Central

1. **Ordenação Total** — Recursos adquirem um identificador imutável e são travados estritamente por ordem crescente. Na prática: nunca tente travar o Recurso B se já segurou o Recurso A, a menos que ID(A) < ID(B).
2. **Timeout como Direito** — Nenhum *lock* é adquirido indefinidamente. Na prática: toda chamada de `acquire()` deve ter um deadline explícito (ex: 2s).
3. **Falha Rápida e Recuperação** — Um *timeout* de lock não é um erro irrecuperável, é um sinal de contenção. Na prática: encapsule aquisições em try/catch e execute lógica de fallback (abortar, enfileirar, ou retentar com backoff).
4. **Seção Crítica Minimizada** — O tempo segurando um recurso é proporcional à chance de deadlock. Na prática: zero I/O, zero chamadas de rede ou logs pesados dentro de um bloco travado.

---

## Quando Ativar

### ✅ Ativar para:
- Implementar transferências entre múltiplas contas/entidades no mesmo banco.
- Criar sistemas onde threads/processos precisam de 2+ locks simultâneos (ex: Mutex A + Mutex B).
- Projetar travamento pessimista de linhas de banco de dados (`SELECT ... FOR UPDATE`).
- Implementar distributed locks (Redis, Zookeeper) para recursos compartilhados.

### ❌ NÃO ativar para:
- Controle de concorrência via versão otimista (ex: `UPDATE ... WHERE version = X`) → use `database-design`.
- Retry de requisições HTTP falhas → use `api-resilience`.
- Programação assíncrona pura sem estado compartilhado mutável (ex: Node.js event loop) → responda diretamente.

---

## Escopo e Limites

| Coberto por esta skill | Delegado para fora |
| :--- | :--- |
| Ordenação de locks em memória (Mutex/Semaphores) | Design de schema e índices |
| Pessimistic locking em DB (`FOR UPDATE`) | Transações ACID completas |
| Timeouts, cancelation tokens e abort paths | Circuit breakers de rede |
| Mapeamento estático de IDs de recursos | Descoberta dinâmica de nós em cluster |

---

## Protocolo de Execução

*Do recebimento da tarefa até a geração do artefato final, focado em resiliência.*

1. **Mapear Recursos Críticos** — Liste toda e qualquer estrutura de dados, arquivo ou registro de DB que sofrerá mutação concorrente. Atribua a cada um um `resource_id` imutável (ex: UUID, hash da chave primária, ou ordinal de enum).
2. **Definir a Topologia de Aquisição** — Identifique quais operações precisam de múltiplos recursos simultaneamente. Ordene os vetores de `resource_id` de forma crescente.
3. **Codificar a Aquisição com Timeout** — Implemente um loop que tenta adquirir os locks na ordem definida. Se qualquer aquisição exceder o timeout, aborte, libere os já adquiridos e lance/executa o fallback.
4. **Isolar a Seção Crítica (Try/Finally)** — Garanta que a liberação dos recursos esteja em um bloco `finally`. Dentro do bloco `try`, permita **apenas** a mutação de estado na memória ou no DB. Proíba chamadas externas.
5. **Implementar o Fallback de Exceção** — Defina o que acontece quando `TimeoutError` ou `DeadlockLoser` é capturado (ex: retornar erro 429, enfileirar em RabbitMQ para processamento assíncrono).
6. **Escrever Testes de Contenção** — Crie testes unitários que spawnam múltiplas threads/processos tentando adquirir os mesmos recursos em ordens aleatórias, forçando timeouts e validando a ausência de travamento perpétuo.

---

## Padrões Específicos

### 1. Lock Ordering em Memória

**Regra**: Ao travar múltiplos objetos, sempre ordene por um identificador numérico ou lexicográfico antes de chamar `.acquire()`.

```python
# ✅ PASS — Ordenação previne circular wait
def transfer(account_a, account_b, amount):
    # Ordenação explícita por ID previne deadlock circular
    first, second = sorted([account_a.id, account_b.id])
    
    lock_first = get_lock(first)
    lock_second = get_lock(second)
    
    try:
        if not lock_first.acquire(timeout=2.0):
            raise LockTimeoutError(f"Lock timeout on resource {first}")
        if not lock_second.acquire(timeout=2.0):
            raise LockTimeoutError(f"Lock timeout on resource {second}")
            
        # Seção crítica: apenas mutação de estado
        account_a.balance -= amount
        account_b.balance += amount
    finally:
        # Liberação invertida (não estritamente necessário, mas boa prática)
        lock_second.release()
        lock_first.release()

# ❌ FAIL — Sem ordenação, Thread 1 pega A->B, Thread 2 pega B->A = DEADLOCK
def transfer_fail(account_a, account_b, amount):
    lock_a = get_lock(account_a.id)
    lock_b = get_lock(account_b.id)
    lock_a.acquire() # Risco infinito
    lock_b.acquire() # Deadlock aqui se outra thread inverteu a ordem
```

**Por que importa**: A condição necessária para deadlock é a "Espera Circular". A ordenação matemática quebra essa condição por axiomatização.

### 2. Pessimistic Locking em Banco de Dados

**Regra**: Em consultas `FOR UPDATE`, trave as linhas na mesma ordem do seu critério de ordenação e trate `LockWaitTimeout` como exceção de negócio.

```sql
-- ✅ PASS — Ordenação no ORDER BY força o DB a travar na mesma sequência sempre
BEGIN;
SELECT id, balance FROM accounts 
WHERE id IN (100, 200) 
ORDER BY id ASC 
FOR UPDATE;

-- (Lógica de aplicação valida saldo e aplica update)

COMMIT;
```

```sql
-- ❌ FAIL — IN sem ORDER BY. O DB pode travar na ordem de leitura do disco, gerando deadlock aleatório
BEGIN;
SELECT id, balance FROM accounts 
WHERE id IN (100, 200) 
FOR UPDATE;
COMMIT;
```

**Por que importa**: Bancos relacionais como PostgreSQL travam na ordem de execução física. `ORDER BY` garante determinismo e evita deadlocks invisíveis no nível de storage.

### 3. Tratamento de Exceção e Fallback (Resiliência)

**Regra**: Nunca deixe um timeout de lock vazar como erro genérico 500. Transforme em ação de recuperação.

```python
# ✅ PASS — Fallback estruturado
try:
    execute_transfer(account_a, account_b, amount)
except LockTimeoutError as e:
    # Resiliência: enfileira para processamento assíncrono
    logger.warning(f"Contenção alta detectada: {e}. Enfileirando tarefa.")
    message_broker.publish(
        queue="pending_transfers", 
        payload={"a": account_a.id, "b": account_b.id, "amount": amount}
    )
    return Response({"status": "processing", "retry_later": True}, status=202)

# ❌ FAIL — Vazar exceção de infraestrutura para o cliente
except Exception as e:
    return Response({"error": str(e)}, status=500)
```

**Por que importa**: Timeouts em concorrência são esperados sob carga. O sistema deve degradar graciosamente (enfileirar, recusar temporariamente) em vez de quebrar.

### 4. Cancelamento de Contexto (Go / Node / C#)

**Regra**: Passe contextos de cancelamento através de todas as camadas de aquisição de recurso.

```go
// ✅ PASS — Timeout no contexto dita o limite de toda a operação
func ProcessOrder(ctx context.Context, orderID string, inventoryID string) error {
    ctxTimeout, cancel := context.WithTimeout(ctx, 3*time.Second)
    defer cancel()

    // Se este lock falhar, o ctxTimeout sinaliza as outras funções a abortarem
    if err := acquireLock(ctxTimeout, "order:"+orderID); err != nil {
        return fmt.Errorf("abortado: %w", err)
    }
    // ...
}

// ❌ FAIL — Sem contexto, uma chamada de rede lenta segura o lock indefinidamente
func ProcessOrderBad(orderID string) {
    acquireLock("order:"+orderID) // Sem timeout!
    callSlowExternalPaymentAPI()   // Segura o lock enquanto aguarda rede
}
```

**Por que importa**: O pior cenário de resiliência é segurar um lock enquanto espera I/O não-trivial. Contextos propagam a decisão de "desistir" instantaneamente através das camadas.

---

## Anti-Padrões Críticos

| Anti-padrão | Consequência | Alternativa Correta |
| :--- | :--- | :--- |
| **Sleep/Time.sleep dentro de um lock** | Multiplica o tempo de contenção exponencialmente sob carga | Calcule valores antes do lock; use variáveis de condição (`notify()`) se precisar esperar |
| **Lock de Leitura/Escrita misturado sem cautela** | `RLock` bloqueia upgrade para `Lock`, causando deadlock | Implemente upgrade explícito: liberar `RLock`, adquirir `Lock` e re-validar o estado |
| **Chamada de API / Rede dentro de seção crítica** | Se a API demorar, o sistema inteiro para (thread starvation) | Fazer I/O *antes* de adquirir o lock. O lock deve conter apenas matemática/estado em memória |
| **Ignorar erros de release()** | Lock permanece travado se a mutação falhar no meio | Colocar `.release()` estritamente no bloco `finally` e logar erros de release |
| **Depender apenas de 'Lock Timeout' no DB** | Mascara problemas de design e gera rollbacks custosos | Use Optimistic Locking para contenção baixa; Pessimistic apenas para contenção alta e conhecida |

---

## Critérios de Qualidade

Antes de entregar o código, confirme:

- [ ] Recursos críticos foram explicitamente mapeados com IDs imutáveis no início da função/classe.
- [ ] Vetores de aquisição de múltiplos locks são ordenados (Sort) antes do loop de aquisição.
- [ ] Nenhum `acquire()` ou `FOR UPDATE` é chamado sem um timeout associado.
- [ ] Bloco `try/finally` (ou equivalente `defer`) garante a liberação em caso de exceção.
- [ ] Seção crítica não contém I/O, logs síncronos pesados ou chamadas externas.
- [ ] Exceção de `Timeout` foi capturada e transformada em lógica de fallback (fila, 429, etc.).
- [ ] Teste de contenção (stress test) foi incluído para validar a ausência de bloqueios perpétuos.

---

## Referências Cruzadas

| Precisa de... | Use a skill... |
| :--- | :--- |
| Transações complexas, níveis de isolamento ou versionamento otimista | `database-design` |
| Retries, backoff e circuit breakers em chamadas HTTP/gRPC | `api-resilience` |
| Gerenciar concorrência assíncrona (Promises, Futures, Event Loop) | `async-patterns` |
| Como estruturar testes de carga e contention | `testing-strategies` |