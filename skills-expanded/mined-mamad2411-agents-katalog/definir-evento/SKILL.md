---
name: definir-evento
description: "Define o schema de um evento, a topologia de mensageria e as relações produtor-consumidor. Use quando o arquiteto vai introduzir comunicação assíncrona via eventos."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: definir-evento

Define o **schema, tópico, produtor, consumidor(es) e garantias** de um evento de domínio em arquitetura orientada a eventos. Produz a especificação que governa a produção e o consumo do evento — não escreve o código de publicação ou consumo.

**Agente:** arquiteto  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`, `seguranca.md`

---

## Quando usar

- Ao introduzir comunicação assíncrona entre serviços
- Quando uma ação de negócio precisa notificar múltiplos consumidores
- Ao substituir chamada síncrona (HTTP) por evento para desacoplar serviços
- Para formalizar eventos que já trafegam sem schema declarado

---

## Conceitos fundamentais

**Evento de domínio:** fato passado imutável que representa algo que ocorreu no sistema. Nomeado no passado: `UserCreated`, `OrderCancelled`, `PaymentApproved`.

**Tópico:** canal no broker de mensagens onde o evento é publicado. Um tópico por tipo de evento; consumidores subscrevem ao tópico.

**Garantia de entrega:**

| Garantia | Significado | Quando usar |
|---|---|---|
| At-most-once | Pode perder mensagem; nunca duplica | Métricas, telemetria |
| At-least-once | Nunca perde; pode duplicar | Maioria dos casos — exige idempotência no consumidor |
| Exactly-once | Nunca perde nem duplica | Transações financeiras — custo alto |

---

## Entrada esperada

- Nome da ação de negócio que origina o evento
- Serviço produtor
- Quem precisa reagir ao evento (consumidores conhecidos)
- Dados que o evento deve carregar
- Requisitos de ordem ou idempotência

---

## Processo de execução

### Passo 1 — Nomear o evento

- Formato: `<Entidade><VerboPasado>` em PascalCase
- Exemplos válidos: `UserRegistered`, `OrderShipped`, `PaymentFailed`
- Nunca comandos: ~~`CreateUser`~~, ~~`ProcessPayment`~~

### Passo 2 — Definir o tópico

Convenção de nome de tópico:
```
<dominio>.<entidade>.<evento>
```
Exemplos:
- `users.user.registered`
- `orders.order.shipped`
- `payments.payment.failed`

### Passo 3 — Definir o payload

Campos do evento:

| Campo obrigatório | Tipo | Descrição |
|---|---|---|
| `eventId` | uuid | Identificador único do evento (para deduplicação) |
| `eventType` | string | Nome do evento: `UserRegistered` |
| `occurredAt` | string (ISO 8601) | Momento em que ocorreu |
| `version` | string | Versão do schema: `"1.0"` |
| `payload` | object | Dados específicos do evento |

Campos dentro de `payload`: definir conforme necessidade do negócio.

**Nunca incluir no payload:**
- Senhas, tokens, chaves de API (`seguranca.md §2`)
- Dados pessoais em claro quando não necessário (`seguranca.md §1`)
- Estado completo da entidade se apenas o delta é relevante

### Passo 4 — Definir garantias de entrega e idempotência

- Qual garantia de entrega é necessária?
- O consumidor deve ser idempotente? (obrigatório para at-least-once — ver `validar-idempotencia`)
- O `eventId` deve ser usado como chave de deduplicação?

### Passo 5 — Definir DLQ (Dead Letter Queue)

Para eventos críticos:
- Definir fila de DLQ para mensagens que falham após N tentativas
- Definir alertas e processo de reprocessamento manual

### Passo 6 — Definir evolução do schema

- Campos podem ser adicionados como opcionais (retrocompatível)
- Campos obrigatórios nunca removidos sem nova versão do evento
- Versão nova: novo tópico (`users.user.registered.v2`) com período de coexistência

---

## Saída produzida

```markdown
## Evento: <NomeDoEvento>

**Tópico:** `<dominio>.<entidade>.<evento>`  
**Produtor:** <nome do serviço>  
**Consumidor(es):** <lista de serviços>  
**Garantia de entrega:** At-least-once  
**Idempotência obrigatória no consumidor:** Sim | Não  
**Versão do schema:** 1.0

---

### Schema do payload

```json
{
  "eventId": "uuid",
  "eventType": "UserRegistered",
  "occurredAt": "2024-01-15T10:30:00Z",
  "version": "1.0",
  "payload": {
    "userId": "uuid",
    "email": "u***@example.com",
    "planId": "uuid"
  }
}
```

### Campos do payload

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| userId | uuid | Sim | ID do usuário criado |
| email | string | Sim | Mascarado conforme seguranca.md §1 |
| planId | uuid | Não | Presente apenas quando plano foi selecionado |

---

### Responsabilidades do produtor

- Publicar o evento imediatamente após a transação de criação confirmar
- Garantir que `eventId` é único por evento publicado
- Não modificar schema sem versionar

### Responsabilidades do consumidor

- Implementar deduplicação por `eventId` (at-least-once)
- Ignorar campos desconhecidos no payload
- Não assumir ordem de chegada dos eventos

---

### DLQ

- Fila: `<tópico>.dlq`
- Retenção: 7 dias
- Reprocessamento: manual via script de replay
```
