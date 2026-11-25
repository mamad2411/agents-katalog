---
name: rc-observability
description: "Guias de observabilidade para serviços em produção — logging estruturado, correlation/trace IDs, métricas RED e USE, tracing distribuído, SLOs e alertas, causa raiz e postmortem. Use ao instrumentar código ou conduzir análise de incidente. Não use para debugging local (rc-diagnose), profiling de código, ou configurar um vendor de APM."
user-invocable: true
model: sonnet
effort: medium
---

# Observabilidade — guias por tarefa

Leia o guia da tarefa em `references/` antes de agir. A meta de qualquer instrumentação,
alerta ou postmortem é a mesma: responder "está quebrado? por quê?" rápido, sem adivinhação —
seja numa Lambda que falhou silenciosamente, num consumer de SQS travado, ou numa task ECS
que reiniciou em loop.

## Roteamento

| Tarefa | Guia |
| ------ | ---- |
| Instrumentar código (logs, correlation/trace ID, métricas RED/USE, tracing distribuído) | `references/instrumentation.md` |
| Definir SLI/SLO/error budget e alertas acionáveis, montar dashboards | `references/alerting-slo.md` |
| Resposta a incidente, causa raiz e postmortem | `references/incident-postmortem.md` |

## Princípios sempre válidos

- **Logue para o leitor futuro do incidente, não para o dev de hoje.** Se o log não ajuda alguém sem contexto às 3h da manhã, ele está incompleto.
- **Nunca logue PII, secret ou token.** Nem em debug, nem truncado, nem mascarado "só um pouco".
- **Alerte em sintoma que dói pro usuário, não em causa.** CPU alta não é alerta; latência/erro que o usuário sente, sim.
- **Instrumente antes de precisar, não durante o incêndio.** Se a pergunta "por que isso falhou?" não tem resposta nos logs/métricas existentes, a instrumentação já chegou tarde.

## Error Handling

- Sem acesso aos sinais de produção (logs, métricas, traces, dashboards reais): oriente a instrumentação no código a partir do que existe no repositório e diga explicitamente que a validação em runtime (volume de log, cardinalidade real, comportamento do alerta) ficou pendente.
