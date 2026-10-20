---
name: validar-idempotencia
description: "Verifica se uma operação é segura para múltiplas execuções sem corromper estado. Use quando o arquiteto ou o dev-backend precisa garantir idempotência em endpoints ou consumers."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: validar-idempotencia

Verifica se uma operação (endpoint, handler de evento, job) é **segura para ser executada múltiplas vezes com o mesmo input sem produzir efeitos colaterais adicionais**. Produz diagnóstico e, quando necessário, especificação de como tornar a operação idempotente.

**Agente:** arquiteto  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`, `dados.md`

---

## Quando usar

- Antes de marcar endpoint como seguro para retry automático
- Ao desenhar consumidor de evento com garantia at-least-once
- Ao implementar job ou worker que pode ser executado mais de uma vez
- Ao revisar operação crítica (pagamento, criação de recurso, envio de notificação) exposta a rede instável

---

## Conceitos

**Idempotente:** executar N vezes produz o mesmo resultado que executar 1 vez. O estado final do sistema é idêntico independentemente de quantas vezes a operação foi executada com o mesmo input.

**Safe:** operação que não modifica estado (GET, HEAD) — automaticamente idempotente.

**Idempotency key:** identificador único fornecido pelo cliente para permitir que o servidor detecte e ignore duplicatas.

| Método HTTP | Idempotente por spec? | Observação |
|---|---|---|
| GET, HEAD, OPTIONS | Sim | Leitura pura |
| PUT | Sim | Substitui o recurso inteiro |
| DELETE | Sim | Deletar o que já foi deletado = 204 |
| POST | Não (por padrão) | Requer implementação explícita |
| PATCH | Não (por padrão) | Depende da semântica da operação |

---

## Entrada esperada

- Descrição da operação (endpoint, handler de evento, job)
- O que a operação faz (escrita em banco, chamada externa, publicação de evento, envio de e-mail)
- Contexto de retry: quem pode chamar múltiplas vezes (rede, fila, scheduler)

---

## Processo de execução

### Passo 1 — Inventariar os efeitos colaterais da operação

Para cada efeito colateral, classificar:

| Efeito colateral | Tipo | Idempotente naturalmente? |
|---|---|---|
| INSERT no banco | Escrita | Não — segunda execução cria duplicata |
| UPDATE com valor fixo | Escrita | Sim — `SET status = 'active'` duas vezes = mesmo resultado |
| UPDATE incremental | Escrita | Não — `SET balance = balance + 100` dobra o valor |
| Publicar evento | Efeito externo | Não — consumidor recebe duas vezes |
| Chamar API externa | Efeito externo | Depende da API externa |
| Enviar e-mail / SMS | Notificação | Não — usuário recebe duas vezes |

### Passo 2 — Identificar os riscos de duplicata

Para cada efeito não idempotente:
- Qual é o impacto de executar duas vezes? (cobrança dupla, usuário criado duas vezes, estoque duplicado)
- Qual é a probabilidade de retry neste contexto? (alta em filas, média em HTTP com retry automático)
- Risco = impacto × probabilidade

### Passo 3 — Recomendar estratégia de idempotência

**Estratégia A — Chave de idempotência (para POST)**

```
Header: Idempotency-Key: <uuid-gerado-pelo-cliente>
```

O servidor armazena `(idempotencyKey, response)` por período configurado. Segunda chamada com mesma chave retorna a resposta cacheada sem reexecutar.

**Estratégia B — Constraint de unicidade no banco**

```sql
-- Garante que segundo INSERT com mesmo ID de negócio falha silenciosamente
CREATE UNIQUE INDEX idx_orders_external_id ON orders(external_id);
```

No código: usar `INSERT ... ON CONFLICT DO NOTHING` ou `upsert`.

**Estratégia C — Verificação antes de executar (check-then-act)**

```typescript
// Verificar se já foi processado antes de executar
const existing = await repo.findByExternalId(event.eventId);
if (existing) return existing; // já processado, retornar sem reexecutar
```

**Estratégia D — Operações naturalmente idempotentes**

Redesenhar a operação para ser idempotente por natureza:
- Usar `upsert` ao invés de `insert` + `update`
- Usar valor absoluto ao invés de incremental: `SET balance = 500` não `SET balance = balance + 100`

### Passo 4 — Verificar o consumidor de evento

Para consumidores de tópico (at-least-once):
- O `eventId` é armazenado após processamento?
- Segunda chegada do mesmo `eventId` é detectada e ignorada?
- A verificação de duplicata é feita dentro de uma transação com o efeito colateral?

### Passo 5 — Emitir veredicto

---

## Saída produzida

```markdown
## Validação de Idempotência: <nome da operação>

**Operação:** POST /recursos | handler de UserCreated | job de cobrança  
**Contexto de retry:** Fila at-least-once | HTTP retry automático | scheduler  
**Veredicto:** ✅ Idempotente | ⚠️ Parcialmente idempotente | ⛔ Não idempotente

---

### Efeitos colaterais analisados

| Efeito | Idempotente? | Risco | Estratégia recomendada |
|---|---|---|---|
| INSERT orders | Não | Alto (cobrança dupla) | Constraint UNIQUE + ON CONFLICT DO NOTHING |
| Publicar evento OrderCreated | Não | Médio (processamento duplo) | eventId como chave de dedup no consumidor |
| Enviar e-mail de confirmação | Não | Baixo (e-mail duplicado) | Idempotency key no serviço de e-mail |

---

### Implementação recomendada

<código ou especificação de como tornar cada efeito idempotente>

---

### O que muda no contrato da API (se aplicável)

- Adicionar header `Idempotency-Key` como opcional na request
- Armazenar chave por 24h após primeira execução
- Retornar 200 (não 201) em execuções subsequentes com mesma chave
```
