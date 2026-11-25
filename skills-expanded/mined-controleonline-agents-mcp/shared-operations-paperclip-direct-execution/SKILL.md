# Paperclip Direct Execution

Esta skill transversal define o canal operacional atual do ecossistema ControleOnline.

## Regra central

O Paperclip executa os agents diretamente usando `agents/roles/*/agent.md` e as
skills deste repositorio. Nao existe delegacao para wrappers externos, assignee
tecnico, worker automatico de push ou outro executor paralelo.

## Como executar

1. Leia `config/ecosystem.config.json`.
2. Leia `agents/skills/controleonline/shared-operations-agent-execution-baseline/SKILL.md`.
3. Leia `agents/skills/controleonline/shared-operations-issue-queue-discovery/SKILL.md`.
4. Leia `agents/skills/controleonline/shared-operations-agent-handoff-governance/SKILL.md`.
5. Leia as skills do papel em `by-role-*`.
6. Leia `agents/skills/controleonline/shared-github-github-flow/SKILL.md` quando houver codigo, branch, RC ou publicacao.

## Proibicoes

- Nao cite nem use outro coding agent como executor operacional.
- Nao reative workflow por `push` ou `schedule` como canal principal.
- Nao use assignee GitHub como ownership.
- Nao crie fila paralela fora de GitHub Project #1 + tasks Paperclip.
- Nao trate comentario, diagnostico ou handoff sem mutacao verificavel como entrega.

## Output minimo

- superficie usada: `Paperclip direct execution`
- task da fila no formato `owner/repo#numero`
- branch, SHA, labels/coluna ou task Paperclip alterada
- resultado: `DELIVERY_PROOF`, `DONE` ou `NEXT_ACTION`
