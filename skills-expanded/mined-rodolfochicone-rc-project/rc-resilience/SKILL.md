---
name: rc-resilience
description: "Guias de resiliência para sistemas distribuídos e orientados a eventos — idempotência, retry com backoff, DLQ, timeouts, circuit breaker, at-least-once. Use ao projetar ou revisar produtores/consumidores de mensagens (EventBridge, SQS) e chamadas entre serviços. Não use para observabilidade (rc-observability) nem debugging local (rc-diagnose)."
user-invocable: true
model: sonnet
effort: medium
---

# Resiliência (event-driven) — guias por tarefa

Leia o guia da tarefa em `references/` antes de agir. A premissa de todo guia aqui é a mesma:
falha de rede, entrega duplicada e consumidor morto **não são exceção** — são o caso normal
em sistemas distribuídos (Lambda, ECS, EventBridge, SQS). Projete para isso, não para o
caminho feliz.

## Roteamento

| Tarefa | Guia |
| ------ | ---- |
| Idempotência, deduplicação e "exactly-once" | `references/idempotency.md` |
| Timeout, retry com backoff/jitter, circuit breaker, bulkhead | `references/retries-timeouts.md` |
| Poison message, DLQ, redrive, partial batch failure | `references/dlq-poison.md` |

## Princípios sempre válidos

- **Assuma at-least-once.** Todo consumidor precisa ser idempotente — a mensagem duplicada vai chegar.
- **Toda chamada remota tem timeout.** E é retryable ou não — decida explicitamente, nunca por padrão implícito da lib.
- **Falha precisa ter destino.** DLQ, não log-e-segue. Se a falha não vai a lugar nenhum, ela vira perda silenciosa de dado.
- **Retry sem backoff+jitter é ataque DDoS ao próprio sistema.** Retry ingênuo em massa derruba o serviço que já está degradado.

## Error Handling

Sem acesso à infra real (fila, tabela de idempotência, alarmes), projete a resiliência no
código e no IaC (Terraform/CDK/SAM) e diga explicitamente que a validação em runtime —
redrive de DLQ, teste de duplicata em ambiente real, disparo do circuit breaker sob carga —
ficou pendente. Para ver o efeito de uma falha em produção (logs, métricas, alarme de
profundidade de DLQ), use `rc-observability`.
