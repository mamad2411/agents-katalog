---
name: azure-function
description: 'Implementar Azure Functions com triggers, idempotência e observabilidade alinhados à stack.'
---

# azure-function skill

Domínio: Azure Functions (isolated/in-process per stack).

## Quando usar

Tarefas `TASK-*` de Azure Functions em `task-memory.md` ou revisão de functions existentes.

## Entradas

- `stack.md`, `task-memory.md`, `instructions/azure-functions.instructions.md`.

## Saídas

- Function(s), configuração, testes/evidence conforme plano.

## Referências

- `instructions/azure-functions.instructions.md`
- `prompts/implement-azure-function.prompt.md`

## Checklist

- [ ] Trigger/binding, contrato e retries alinhados ao `stack.md`.
- [ ] Idempotência para filas, timers e eventos.
- [ ] Configuração via options/Key Vault sem secrets no repo.
- [ ] Observabilidade com correlation id, logs estruturados e métricas.
- [ ] Evidence com `dotnet test`, execução local ou validação equivalente.

## Evidence esperada

- Comandos de build/teste ou execução documentada; correlation em fluxos assíncronos.

## Critério de parada

- Não publicar function com mensageria sem path de poison/DLQ quando exigido pela stack.
